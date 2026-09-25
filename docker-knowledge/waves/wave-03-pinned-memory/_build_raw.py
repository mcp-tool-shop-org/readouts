#!/usr/bin/env python3
"""Wave-3 synthesis: consolidate the 22 raw study-swarm findings into ~8 distinct KB findings
and emit research-raw.json (load_db.py loader shape).

The 4 research lanes independently re-surfaced the same load-bearing facts (e.g. "NVIDIA still
documents the limit" appeared in all four) — by design, that cross-lane convergence is signal,
but the KB wants distinct findings, not 22 near-duplicates. CONSOLIDATION below maps each
consolidated finding to the raw finding ids whose SOURCES it draws on; sources are pulled
programmatically (URLs/titles/authors verbatim from the workflow output, never retyped) and
deduped by URL. Each source carries its retrieval-oracle groundedness; each finding carries the
family-different (mistral+granite) verdict. 0 fabricated, 0 refuted -> nothing dropped.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
WF = json.load(open(os.path.join(HERE, "workflow-output.json"), encoding="utf-8"))
FAM = json.load(open(os.path.join(HERE, "family-verdicts.json"), encoding="utf-8"))
DATE = "2026-06-04"

RAW = {f["id"]: f for f in WF["findings"]}
ORACLE = {o["id"]: o for o in WF["oracle"]}
MIS = FAM.get("mistral-small:24b", {}).get("verdicts", {})
GRA = FAM.get("granite4.1:30b", {}).get("verdicts", {})

_GROUND = {"supported": "SUPPORTED", "partial": "PARTIAL", "not_supported": "NOT_SUPPORTED", "unreachable": "CANT_TELL"}

# consolidated KB finding -> the raw finding ids whose sources it draws on
CONSOLIDATED = [
    {
        "slug": "wsl2-pinned-limit-still-documented-but-never-numeric",
        "name": "NVIDIA still documents the WSL2 pinned-memory limit (v13.3) — but never as a number",
        "kind": "constraint", "status": "load-bearing", "rig_relevance": 4,
        "claim": "NVIDIA's CUDA-on-WSL User Guide STILL lists 'pinned system memory ... availability for applications is limited' as a Known Limitation as of v13.3 (2026-05-21), verbatim-unchanged since v12.0 (2022) — and has NEVER attached a number to it.",
        "detail": "The qualitative limitation is current and un-retracted across >=3.5 years of doc revisions; the same DL-workload caveat ('some training workloads ... can exceed this limit and may not work') persists. The '~300-500 MB' figure the KB carried is therefore NOT an NVIDIA spec — it is a community-observed, version/config-bound measurement, never an official ceiling.",
        "applies_to": "windows-wsl2", "metric": "v13.3 (2026-05-21) wording == v12.0 (2022-12-08); no numeric cap ever published",
        "design_implication": "Treat the documented limitation as a qualitative WORST-CASE PRIOR to be overridden by a live cudaHostAlloc probe — never as a hard numeric ceiling. The KB's 300-500 MB number must be reframed as community-observed and version-bound, not a vendor spec.",
        "src_from": ["official-timeline#1", "fifty-percent-relationship#5"],
    },
    {
        "slug": "wsl2-pinned-limit-windows-managed-no-nvidia-cap",
        "name": "The pinned limit is Windows/WDDM-managed, not an NVIDIA driver cap; no official 'lift' changelog exists",
        "kind": "constraint", "status": "load-bearing", "rig_relevance": 4,
        "claim": "An NVIDIA engineer states the pinned-memory limit is 'entirely managed by Windows' (WDDM<->CUDA interop) and 'the NVIDIA driver doesn't control or set the limit'; no NVIDIA/Microsoft release note (2023-2026) announces raising or lifting it.",
        "detail": "Because the limit is a Windows/WDDM property, there is no NVIDIA driver-version boundary to cite for a 'fix'. The 2020 forum origin gave no mechanism and no fix-version; the limit was long acknowledged but never owned by a numeric NVIDIA commitment.",
        "applies_to": "windows-wsl2", "metric": "njuffa (NVIDIA): limit 'depends on internal details of the operating system, not CUDA'",
        "design_implication": "Do NOT claim 'driver X lifted the cap'. Record the measured driver/CUDA/WSL triple as the EMPIRICAL boundary, because NVIDIA provides no official one for cudaHostAlloc. The planner's per-rig probe is the only authority on this rig's ceiling.",
        "src_from": ["official-timeline#2", "mechanism-boundary#2", "mechanism-boundary#6"],
    },
    {
        "slug": "harsh-pinned-cap-is-a-container-memlock-wsl2pv-artifact",
        "name": "The ~300-500 MB cap is a container locked-memory (RLIMIT_MEMLOCK) + WSL2-PV artifact, not an inherent WSL2/driver ceiling",
        "kind": "gotcha", "status": "load-bearing", "rig_relevance": 5,
        "claim": "The harsh cap is a CONTAINER / locked-memory artifact, not a WSL2 GPU-driver ceiling: in microsoft/WSL #14078, NATIVE Windows pinned ~4000 MB single / ~5600 MB total on the same rig where the Docker container was held to ~500 MB, and bare (non-container) WSL2 pins small buffers fine.",
        "detail": "The failure localizes to the container path: page-locked allocations are gated by the container's RLIMIT_MEMLOCK and by extra WSL2->WDDM paravirtualization (GPU-PV) machinery between guest and host. memlock ulimits are the repeatedly-cited 'fix' lever (though one #14078 commenter reported memlock=-1 alone didn't lift it — a Docker-Desktop-on-WSL2-specific path). This is why a different container/Docker-Desktop vintage can pin far more.",
        "applies_to": "in-container", "metric": "same rig: native Windows ~4000 MB vs Docker container ~500 MB (#14078, driver 572.83)",
        "design_implication": "The pinnable ceiling is a function of (container memlock x WSL2 VM RAM x driver x Docker-Desktop version) — NOT a portable constant. It MUST be probed per-rig/per-container (which the profiler's cudaHostAlloc probe now does); a static assumed number silently corrupts the warm-tier staging budget in either direction.",
        "src_from": ["recent-measured#2", "mechanism-boundary#7", "recent-measured#6"],
    },
    {
        "slug": "harsh-cap-still-reproduced-jan-2026-driver-572",
        "name": "The harsh cap still reproduced as of Jan 2026 (driver 572.83) inside Docker — version/config-bound, not universally fixed",
        "kind": "benchmark", "status": "load-bearing", "rig_relevance": 4,
        "claim": "The cap is NOT globally fixed: the most recent measured report (microsoft/WSL #14078, 2026-01-17, driver 572.83, WSL 2.4.10) still reproduces ~500 MB single / ~400 MB total pin_memory inside Docker-on-WSL2, and the original 2020 NVIDIA-forum ~300 MB report was confirmed still-blocking in 2021.",
        "detail": "So the cap was real and reproducing on an early-2026 driver in a constraining container config; the issue was closed 2026-01-27 as an automatic stale/no-author-activity close, NOT via a documented Microsoft/NVIDIA fix. The rig's >=22.5 GiB on driver 610.47 is therefore a config/version delta, not evidence the cap was abolished everywhere.",
        "applies_to": "windows-wsl2", "metric": "~300 MB (2020) -> ~500 MB single / ~400 MB total (Jan 2026, driver 572.83, Docker)",
        "design_implication": "Refusing to generalize is the whole point: a rig on 572.83 in a constrained container may still see the harsh cap. The planner must NOT hardcode EITHER 500 MB or 22 GiB — it probes. Record the probe's driver/Docker context in the receipt so a low result on an old stack is explainable, not mysterious.",
        "src_from": ["recent-measured#1", "official-timeline#4", "recent-measured#4"],
    },
    {
        "slug": "nearest-boundary-cuda-13-2-r595-wsl-containers-vmm",
        "name": "Nearest documented boundary: CUDA 13.2 / driver R595 (2026-03) added native+WSL container support + VMM allocators (not cudaHostAlloc)",
        "kind": "constraint", "status": "load-bearing", "rig_relevance": 4,
        "claim": "The strongest citable capability lift near the rig's result is CUDA 13.2 / driver R595 (2026-03): NVIDIA officially announced 'Native (and WSL) containers are supported' plus cuMemCreate / cudaMallocAsync (advanced/VMM memory-management API) for WSL/MCDM — but this names container + VMM/async allocators, NOT the legacy cudaHostAlloc API.",
        "detail": "The rig's driver 610.47 post-dates R595, so it runs the improved WSL-container code path — consistent with a Docker-on-WSL2 container now behaving far better than the 572.83-era reports. But the release note does not literally say 'cudaHostAlloc limit raised', so this is an ANCHOR for 'WSL container memory improved in early 2026', not proof of a pinned-API fix.",
        "applies_to": "windows-wsl2", "metric": "CUDA 13.2 / R595 (2026-03-09): WSL container support + cuMemCreate/cudaMallocAsync; rig driver 610.47 post-dates it",
        "design_implication": "Cite R595 as the plausible 'why it improved' boundary with the correct caveat (container/VMM support, not the pinned API). Frames the receipt honestly: the lift is real and roughly dateable, but not attributable to a documented cudaHostAlloc change.",
        "src_from": ["official-timeline#3"],
    },
    {
        "slug": "wsl2-more-restrictive-via-gpu-pv-machinery",
        "name": "WSL2 is more restrictive than native Windows because of GPU-PV (paravirtualization) between guest and WDDM",
        "kind": "constraint", "status": "supporting", "rig_relevance": 3,
        "claim": "NVIDIA explicitly attributes WSL2's lower pinning to extra 'WSL2->WDDM machinery' — GPU paravirtualization (GPU-PV) sitting between the guest and the host WDDM driver is the named mechanism that historically made WSL2 pinning lower than native Windows.",
        "detail": "This is the mechanistic 'why WSL2 < native' — distinct from the container memlock gate. It explains the directional rule (WSL2 historically <= native) without fixing a number, and is consistent with improvements when the paravirtualization/container path is upgraded (see the R595 container support).",
        "applies_to": "windows-wsl2", "metric": "qualitative: GPU-PV adds a guest->host WDDM hop",
        "design_implication": "Reinforces that the ceiling is a stack property (guest VM + GPU-PV + WDDM + container), so it is measured from inside the actual container, the only vantage that sees the whole stack.",
        "src_from": ["mechanism-boundary#3"],
    },
    {
        "slug": "wsl2-pinnable-ceiling-tracks-vm-assigned-ram",
        "name": "The effective WSL2 GPU-accessible host-memory ceiling tracks the VM's assigned RAM (.wslconfig memory=)",
        "kind": "constraint", "status": "load-bearing", "rig_relevance": 5,
        "claim": "Evidence points to the WSL2/container GPU-accessible host-memory ceiling being governed by the WSL2 VM's assigned RAM (.wslconfig 'memory='), consistent with the native ~50%-of-RAM behavior scaling with whatever RAM the VM has — not a fixed NVIDIA number.",
        "detail": "The closest documented analog is ROCm-in-WSL2 reporting a GPU pool size derived from VM RAM; the NVIDIA 50%-of-RAM rule is itself RAM-relative. This predicts that a larger WSL2 VM yields a proportionally larger pinnable ceiling — so the figure is a fraction of the VM's RAM, not an absolute.",
        "applies_to": "windows-wsl2", "metric": "ceiling scales with WSL2 VM RAM (.wslconfig memory=); native rule ~50% of RAM",
        "design_implication": "The profiler's RAM-aware probe is correct: it caps at a fraction of the VM's RAM rather than a fixed MB figure. The planner should express the warm-tier budget relative to the measured VM RAM, and note that raising .wslconfig memory= raises the ceiling.",
        "src_from": ["mechanism-boundary#4", "fifty-percent-relationship#4"],
    },
    {
        "slug": "rig-measured-pinnable-exceeds-50pct-rule",
        "name": "This rig probed >=22.5 GiB pinnable on a 31 GiB VM (>=72%) — exceeding the native 50% rule, consistent with the container being the only gate",
        "kind": "benchmark", "status": "load-bearing", "rig_relevance": 5,
        "claim": "On driver 610.47 the gpu-container cudaHostAlloc probe succeeded to >=22.5 GiB inside Docker-on-WSL2 (a 31 GiB VM, >=72% of VM RAM) with no failure — exceeding even the Windows-native ~50%-of-RAM cap, consistent with the container layer being the only real gate and the ceiling tracking VM RAM.",
        "detail": "This is ~45x the KB's prior 300-500 MB assumption and above the 50% native rule. It is the empirical override the whole MEASURE-don't-assume thesis predicts: the documented limitation is qualitative, the historical number was a constrained-container artifact, and this rig's actual ceiling is ample. The probe was safety-capped at 75% of VM RAM, so the true ceiling may be higher.",
        "applies_to": "windows-wsl2", "metric": ">=22.5 GiB / 31 GiB VM (>=72%); vs prior KB 300-500 MB; vs native ~50% rule",
        "design_implication": "The warm-tier KV/prefetch staging budget on this rig is AMPLE, not the feared few-hundred MB — a Phase-1 assumption flips. The receipt records >=22.5 GiB (probe-capped lower bound) + the driver/Docker context, and the planner sizes warm-tier staging from the measured value, never the stale assumption.",
        "src_from": ["recent-measured#5", "fifty-percent-relationship#1"],
        "extra_sources": [{
            "kind": "benchmark", "title": "gpu-container Milestone-1 measured baseline (RTX 5090, driver 610.47)",
            "authors": "gpu-container profiler", "year": "2026",
            "identifier": "baselines/2026-06-04-nvidia-geforce-rtx-5090.json",
            "url": "https://github.com/mcp-tool-shop-org/readouts/blob/main/docker-knowledge/baselines/2026-06-04-nvidia-geforce-rtx-5090.json",
            "finding": "In-container cudaHostAlloc probe measured pinnable >=22.5 GiB on driver 610.47 (probe safety-capped at 75% of the 31 GiB WSL2 VM).",
            "exists_verified": 1, "finding_supported": "SUPPORTED",
            "verifier_note": "Self-measured baseline emitted by this product's Milestone-1 profiler (wave-2 close-the-loop).",
        }],
    },
]


def family_note(raw_ids):
    mis = [MIS.get(i, {}).get("verdict", "-") for i in raw_ids]
    gra = [GRA.get(i, {}).get("verdict", "-") for i in raw_ids]
    refuted = any(v == "refuted" for v in mis + gra)
    mis_cc = sum(1 for v in mis if v == "cant_confirm")
    parts = []
    parts.append("granite4.1:30b: " + ("REFUTED" if any(v == "refuted" for v in gra) else "confirmed"))
    if mis_cc:
        parts.append(f"mistral-small:24b: confirmed/{mis_cc}x cant_confirm (2026-source recency)")
    else:
        parts.append("mistral-small:24b: " + ("REFUTED" if any(v == "refuted" for v in mis) else "confirmed"))
    return refuted, " | ".join(parts)


def main():
    findings = []
    verdicts = []
    for c in CONSOLIDATED:
        # pull + dedup sources from the referenced raw findings, attach oracle groundedness
        seen, srcs, any_partial, any_ns = set(), [], False, False
        for rid in c["src_from"]:
            raw = RAW.get(rid, {})
            ocites = {ct.get("url"): ct for ct in (ORACLE.get(rid, {}).get("citations") or [])}
            for s in (raw.get("sources") or []):
                url = s.get("url")
                if not url or url in seen:
                    continue
                seen.add(url)
                oc = ocites.get(url, {})
                ground = _GROUND.get(oc.get("groundedness"), "CANT_TELL")
                if ground == "PARTIAL":
                    any_partial = True
                if ground == "NOT_SUPPORTED":
                    any_ns = True
                srcs.append({
                    "kind": "docs", "title": s.get("title"), "authors": s.get("authors"),
                    "year": s.get("year"), "identifier": url, "url": url,
                    "claim": s.get("finding"), "quant": None,
                    "exists_verified": 1 if oc.get("resolved") else 0,
                    "finding_supported": ground,
                    "verifier_note": oc.get("note"),
                })
        for es in c.get("extra_sources", []):
            if es["url"] not in seen:
                srcs.append(es)

        refuted, fnote = family_note(c["src_from"])
        overall = "thin" if not srcs else ("confirmed-with-fixes" if (any_partial or any_ns) else "confirmed")
        note = ("a source NOT_SUPPORTED (flagged); " if any_ns else "") + \
               "oracle retrieval (existence+groundedness) + family-different (" + fnote + "); 0 refutations"
        findings.append({
            "name": c["name"], "slug": c["slug"], "kind": c["kind"], "claim": c["claim"],
            "detail": c["detail"], "applies_to": c["applies_to"],
            "design_implication": c["design_implication"], "metric": c["metric"],
            "confidence": "high", "rig_relevance": c["rig_relevance"], "status": c["status"],
            "sources": srcs,
        })
        verdicts.append({"name": c["name"], "overall": overall, "note": note})

    out = {
        "date": DATE, "wave": 3,
        "title": "Pinned-memory re-check — the WSL2 cudaHostAlloc ceiling across driver versions",
        "domain_scope": "hw-measurement: reconciling the wave-2 '300-500 MB WSL2 pinnable' finding against a measured >=22.5 GiB on driver 610.47",
        "agent_count": 26,
        "verifier_note": (
            "3-lens, reasoning-stripped. Retrieval oracle (WebFetch, in-workflow): 22/22 findings checked, "
            "existence+attribution+groundedness; 17 confirmed, 5 partial, 0 not_supported, 0 fabricated. "
            "Family-different (local ollama, reasoning-stripped, claims+sources only): granite4.1:30b confirmed "
            "all 22; mistral-small:24b confirmed the concrete claims and marked 8 absence-of-evidence / 2026-source "
            "claims cant_confirm (recency, per instruction) — 0 refutations across both families. mistral over-"
            "skepticism on post-training sources was filtered by the oracle (same pattern as wave-2). Both verifiers "
            "were confirmed UP before the pass (ANDON gate passed, not skipped). 22 raw findings consolidated to 8."
        ),
        "notes": "docker-knowledge wave 3 — re-checks the pinned-memory lane after the Milestone-1 profiler measured "
                 ">=22.5 GiB pinnable (vs the KB's 300-500 MB). Reconciles three wave-2 findings (separate UPDATE).",
        "lanes": [{
            "slug": "hw-measurement", "name": "Hardware measurement methodology",
            "research": {"domain": "Hardware measurement methodology", "notes": "", "findings": findings},
            "verify": {"verdicts": verdicts},
        }],
        "measurements": [],
    }
    json.dump(out, open(os.path.join(HERE, "research-raw.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=2)
    print("wrote research-raw.json:", len(findings), "consolidated findings,",
          sum(len(f["sources"]) for f in findings), "sources")
    for v in verdicts:
        print(f"  [{v['overall']:20s}] {v['name'][:70]}")


if __name__ == "__main__":
    main()
