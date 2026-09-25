/**
 * Wave-9 Move #2 e2e: prove the full-abstract fix end-to-end through role-os's REAL shipped panel
 * code (buildEvidence + runOffloadPanel from src/citation-panel.mjs), on the 3 e2e-dispatch.md
 * citations. arXiv retrieval is 429-throttled on this host, so prism's existence floor can't run
 * live; we stub prism's RETRIEVED evidence from the sha-pinned abstracts-cache.json (exactly what
 * prism's groundedness lens would see), the same workaround wave-6 used.
 *
 * The variable under test is the evidence GRANULARITY the panel judges against — the one thing the
 * fix changes:
 *   span_only      buildEvidence({source_title, span})              (wave-6: a single tangential span)
 *   full_abstract  buildEvidence({source_title, source_abstract})   (the fix: prism's full abstract)
 *
 * Expected: the two FAITHFUL claims flip insufficient(span) -> supported(abstract); the PLANTED
 * inversion stays caught under the abstract (the fix adds no false-confirm).
 *
 * Run AFTER llama-swap is free. Pins the wave-9 per-family panel via OFFLOAD_PANEL_SEATS.
 *   node e2e_full_abstract.mjs
 */
import { readFileSync, writeFileSync } from "node:fs";
import { buildEvidence, runOffloadPanel } from "../../../role-os/src/citation-panel.mjs";

process.env.OFFLOAD_PANEL_SEATS ||= "qwen3-14b,mistral-nemo-12b,granite-3.3-8b";
const SRC = JSON.parse(readFileSync(new URL("./abstracts-cache.json", import.meta.url)));

// The 3 e2e-dispatch.md citations. `span` = a REAL sentence from each abstract that is tangential to
// the claim (what prism's lens may surface) — so span-only under-confirms while the full abstract
// (which states the claim) confirms. The inversion's claim contradicts the abstract either way.
const CASES = [
  {
    id: "c1", identifier: "arXiv:2402.01817", kind: "faithful",
    claim: "Auto-regressive LLMs cannot, by themselves, do planning or self-verification.",
    span: "We present a vision of LLM-Modulo Frameworks that combine the strengths of LLMs with external model-based verifiers in a tighter bi-directional interaction regime.",
  },
  {
    id: "c2", identifier: "arXiv:2310.01798", kind: "faithful",
    claim: "Without external feedback, LLMs struggle to self-correct their reasoning and can even degrade after self-correction.",
    span: "A contemporary methodology, self-correction, has been proposed as a remedy to these issues.",
  },
  {
    id: "c3", identifier: "arXiv:2404.13076", kind: "planted-inversion",
    claim: "The paper concludes that self-preference bias is unrelated to whether an LLM can recognize its own outputs.",
    span: "Self-evaluation using large language models (LLMs) has proven valuable not only in benchmarking but also methods like reward modeling.",
  },
];

const arxivId = (ident) => ident.replace(/^arXiv:/i, "");

function runRegime(useAbstract) {
  const input = CASES.map((c) => {
    const s = SRC[arxivId(c.identifier)];
    const ev = useAbstract
      ? buildEvidence({ source_title: s.title, source_abstract: s.abstract, span: c.span })
      : buildEvidence({ source_title: s.title, span: c.span });
    return { id: c.id, identifier: c.identifier, claim: c.claim, evidence: ev };
  });
  const panel = runOffloadPanel(input, { timeout: 300_000 });
  return panel;
}

console.log(`seats: ${process.env.OFFLOAD_PANEL_SEATS}\n`);
const regimes = {};
for (const [name, useAbs] of [["span_only", false], ["full_abstract", true]]) {
  console.log(`=== regime: ${name} ===`);
  const panel = runRegime(useAbs);
  const byId = Object.fromEntries(panel.perCitation.map((p) => [p.id, p.panel_verdict]));
  for (const c of CASES) {
    console.log(`  ${c.id} (${c.kind.padEnd(17)}) -> ${byId[c.id]}`);
  }
  regimes[name] = { seats: panel.seats, perCitation: panel.perCitation };
  console.log("");
}

// Verdict: faithful claims should flip to supported under the abstract; the inversion must NOT be
// supported under either regime.
const get = (r, id) => regimes[r].perCitation.find((p) => p.id === id)?.panel_verdict;
const faithfulFixed = ["c1", "c2"].filter((id) => get("span_only", id) !== "supported" && get("full_abstract", id) === "supported");
const inversionCaught = get("full_abstract", "c3") !== "supported";

console.log("=== verdict ===");
console.log(`  faithful claims fixed by the full abstract (insufficient/span -> supported/abstract): ${JSON.stringify(faithfulFixed)}`);
console.log(`  planted inversion still caught under the full abstract (not supported): ${inversionCaught} (got '${get("full_abstract", "c3")}')`);

const receipt = {
  schema: "tensor-engine-knowledge/e2e-full-abstract-receipt/v1",
  wave: 9, date: "2026-06-03", kind: "move2-e2e",
  note: "arXiv 429-throttled; prism evidence stubbed from sha-pinned abstracts-cache.json (wave-6 workaround). Exercises role-os buildEvidence + runOffloadPanel (shipped code) against llama-swap.",
  seats: regimes.full_abstract.seats,
  regimes,
  faithful_fixed_by_abstract: faithfulFixed,
  inversion_caught_under_abstract: inversionCaught,
};
writeFileSync(new URL("./e2e-full-abstract-receipt.json", import.meta.url), JSON.stringify(receipt, null, 2));
console.log("\nreceipt -> e2e-full-abstract-receipt.json");
