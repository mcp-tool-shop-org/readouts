import type { SiteConfig } from '@mcptoolshop/site-theme';
// The corpus map, generated from the databases by shared/gen_root_index.py. Every number
// on this page comes from here, so the page cannot drift from the data it describes.
import corpus from '../../index.json';

const n = (x: number) => x.toLocaleString('en-US');
const t = corpus.totals;

const clip = (s: string, max = 150) => {
  if (s.length <= max) return s;
  const cut = s.slice(0, max);
  return `${cut.slice(0, cut.lastIndexOf(' '))}…`;
};

const REPO = 'https://github.com/mcp-tool-shop-org/readouts';

export const config: SiteConfig = {
  title: 'readouts',
  description:
    'Verified, source-backed SQLite knowledge bases on game development and local AI tooling, each grown in waves and checked by a separate verifier.',
  logoBadge: 'RO',
  brandName: 'readouts',
  repoUrl: REPO,
  footerText:
    'MIT Licensed — built by <a href="https://mcp-tool-shop.github.io/" style="color:var(--color-muted);text-decoration:underline">MCP Tool Shop</a>',

  hero: {
    badge: 'Open data',
    headline: 'readouts',
    headlineAccent: 'knowledge an agent can check.',
    description:
      `${t.knowledge_bases} SQLite knowledge bases on Rust, Godot, Blender, sprites, local AI models, the sung voice and the XRP Ledger. ` +
      `${n(t.entries)} entries and ${n(t.sources)} cited sources. ` +
      `<strong>${n(t.verified)}</strong> entries are verified, and only a verdict from a separate verifier can make them so.`,
    primaryCta: { href: '#knowledge-bases', label: 'See the knowledge bases' },
    secondaryCta: { href: 'handbook/', label: 'Read the Handbook' },
    previews: [
      { label: 'Get it', code: `git clone ${REPO}` },
      { label: 'Search', code: "WHERE recipes_fts MATCH 'rapier'" },
      { label: 'Check it', code: 'python verify.py' },
    ],
  },

  sections: [
    {
      kind: 'data-table',
      id: 'knowledge-bases',
      title: 'The knowledge bases',
      subtitle: `Generated from index.json on ${corpus.generated}. Verified means an external verdict confirmed the entry.`,
      // Three columns, not five: the theme's table clips rather than scrolls, and five
      // columns cut off the numbers on a phone.
      columns: ['Knowledge base', 'What it covers', 'Status'],
      rows: corpus.knowledge_bases.map((k) => [
        k.kb,
        clip(k.what, 120),
        `${n(k.entries)} ${k.noun} · ${n(k.verified)} verified · ${k.waves} waves`,
      ]),
    },
    {
      kind: 'features',
      id: 'how-it-works',
      title: 'How an entry earns verified',
      subtitle: 'The flag is set by someone other than the author. Everything else follows from that.',
      features: [
        {
          title: 'Waves of sourced research',
          desc: 'Each wave runs one research lane per domain. Every entry cites its sources as url-and-claim pairs and records the wave that produced it.',
        },
        {
          title: 'A verifier that never saw the reasoning',
          desc: 'A second agent checks each entry against the pages it cites and returns a verdict. It only sees the claims and the citations.',
        },
        {
          title: 'One definition of verified',
          desc: 'verified = 1 only when an external verdict says so. With no verdict, an entry stays unverified: a lead, not a fact.',
        },
        {
          title: 'A compiler where there is code',
          desc: 'Every code check in rust-knowledge is compiled, and where it says so run, by rustc 1.98.1. A recipe whose own example fails is never verified.',
        },
        {
          title: 'Provenance you can open',
          desc: "Each wave's dispatch, raw research and verification record sit next to the database, so any verdict can be traced to its evidence.",
        },
        {
          title: 'A floor that runs in CI',
          desc: 'verify.py checks that the indexes, counts and links are true about the databases, with a stable code and a hint for every failure.',
        },
      ],
    },
    {
      kind: 'code-cards',
      id: 'usage',
      title: 'Use it',
      subtitle: 'Plain SQLite files and standard-library Python.',
      cards: [
        {
          title: 'Search one knowledge base',
          code:
            "-- sqlite3 rust-knowledge/rust.db\nSELECT r.name, r.verified\nFROM recipes_fts f\nJOIN recipes r ON r.id = f.rowid\nWHERE recipes_fts MATCH 'rapier'\n  AND r.verified = 1\nLIMIT 5;",
        },
        {
          title: 'Check the corpus',
          code: 'python verify.py\n# exit 0 clean, 1 FAIL, 2 crashed\n\npython verify.py --json\n# code, message, hint per check',
        },
        {
          title: 'Route an agent to one slice',
          code: 'npx @mcptoolshop/loadout-os \\\n  resolve --project .',
        },
        {
          title: 'Read the map',
          code: 'index.md    # the map, for agents\nindex.json  # the same, for programs',
        },
      ],
    },
  ],
};
