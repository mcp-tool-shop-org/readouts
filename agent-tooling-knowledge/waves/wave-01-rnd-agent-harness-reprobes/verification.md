# Wave 1 — verification

**Runner:** the R&D seat, 2026-10-20.

**How each finding was checked:** each verdict in `research-raw.json` names the receipt or document that checked it,
and the date. The checks are:
- live re-probes;
- read-only sandbox checks;
- primary documents: Claude Code's permissions page, the sbx CLI help, and the GitHub API for licences.

No second model family checked. These are measurements and documents, so per the studio's proportional-verification
rule a receipt check is the right depth.

**Model use: 13 plan-route turns of claude-haiku-5-5,** all with `apiKeySource: none` and no API key. The Director
approved 12, then 2 more for the `~` pair.

| Probe | Turns | What it ran |
|---|---|---|
| B1, MCP at the first turn | 6 | 2.1.197 with no hold and with a 10 s hold; 2.1.280 with no hold (×3) and with a 10 s hold |
| B2, Read deny against Grep | 6 | the one-slash rule form, 2.1.197 + 2.1.280 (a probe-design slip, kept as the one-slash finding); `//` form, 2.1.197 + 2.1.280; `~` form, 2.1.197 ×2 |
| B4, NeMo Relay | 1 | one transparent `nemo-relay claude` run |

**Where:**
- the `atlas-pilot` Docker sandbox (sbx 0.48.0), under sbx's Balanced network policy, unchanged;
- every sbx command run from a C: working directory;
- each job's start and stop reported to the Publisher, which approved both jobs.

## Receipts

The receipts are kept in the R&D seat's private store, not published. Stream-json starts carry session ids, and one
Relay file carries account identity. Each is named here with its SHA-256.

**Job B (2026-10-20, 17:07Z–17:14Z):**

| file | SHA-256 |
|---|---|
| `b1-cur-0.jsonl` | 91dab37461470a89f92b4c9419f43e858207dedd8e2857010d346b79e1ba48e0 |
| `b1-cur-10.jsonl` | beb7c4ae9a230896b43138bfa6afa1f59e24c6b6413e002a88c2f6fa48adadcf |
| `b1-pin-0.jsonl` | 006c688752fdaf3e75fb356348efd981c7cabab9da129bfdfc795280038345db |
| `b1-pin-10.jsonl` | 70a33a28b6a5c9aecb4e9fc29434ed456f152e981ffec53efc6a9efc41a7f5a6 |
| `b1-summary.jsonl` | 4aadf700566f85d0908ab5fc8e430f28858d1e6e18cda5c8cb4ba3badc864855 |
| `b1rep-cur-0-1.jsonl` | 3fb1eac9f59fa138597c398b4632476b78205b9ff4cb6f32f49aa850caa09f58 |
| `b1rep-cur-0-2.jsonl` | 0c81a93716f69914c7a94298ae1a8a929b6a162fac88f2d52aa92ee830eed080 |
| `b1rep-summary.jsonl` | 5d18f6cfe7f14e3b75a2bc8bf337eb277275130a0c12c8cf889f6609cef818a3 |
| `b2-cur.jsonl` | 867c01eb2eef87942035e5a868c1b7c751b2d2f337fe51af169e5bbc71dc23ac |
| `b2-pin.jsonl` | 9d5ddbb7737d7f6e7112070b2b99ace86aa11d1a84c6ce5d49ef3eb6cc4569e8 |
| `b2-summary.jsonl` | 9c12d3b756186631ee714e6df0e81a1e081c85834085283cff7c11bd34fa5f56 |
| `b2abs-cur.jsonl` | 1cb5c104b784e9688863054676e6ae2b9073c4b6f93f61414b919d13f4f2d7f5 |
| `b2abs-pin.jsonl` | 97b59a8672d85da91b93a29d55c3a814a14521683833e5c28ff9023887ab1df2 |
| `b2abs-summary.jsonl` | e709576f84422a3a6ee5191dc791591cdb9aff48feebb4ad8283c0a316b1cd4d |
| `b2home-pin-1.jsonl` | 72453b559ef4fee296ed24c33fa8f0fae014110e78f8ee93c38fd33517f4fa03 |
| `b2home-pin-2.jsonl` | 9d9d4ec4ec36afcba71af40dd3d67ef5f3f35955d33bb8ff472a70a5272f63ec |
| `b4-policylog-after.json` | 424a7f688523d431e01f90632d25d2eb5b853a11edf1d3591ae66c0b85653e54 |
| `b4-policylog-before.json` | d11cbf4af12f0ba8428bd6e57f1ccba696717354b93ff1076a5a1f09dcf11169 |
| `b3-credentials.txt` | b0bda13865ca2d075e18920c6d81d9132d439f8d73cc8abd6304deb767447910 |
| `b3-ollama-binding.txt` | 2b11e77da223f36b0da3e64f788c5f40ae521bd4e20164f10322c31c3d399092 |
| `b4-start.txt` | 8f07f8217c5c54b72b80f799841b0c8e1499e5c51a9734d84b3f719d67582c87 |
| `recon.txt` | e96b367ca2f296d8b952d36dec0a502e3a3a2d3d43f8e47caad86ce32b284c40 |

**Job A (2026-10-20, read-only, recovered from the sandbox):**

| file | SHA-256 |
|---|---|
| `root__halted-shakedown-1__results__pilot__probe-report.json` | 6b7c583e7bef04df4b582f2525c44acae1f68c32ce109a38562b43c250732505 |
| `root__plan-haiku-start.jsonl` | 7b4eba1680eac41354c57198ccca0ecbb38ab74f61dd8e057ea6e8d5fbf260a1 |
| `root__round3__results__pilot__probe-report.json` | 2a5f34de60145be7d7b4581b4fdda2dfe714d17af22460254e9689d2cea6b0ae |
| `root__round4__results__pilot__probe-report.json` | 2a5f34de60145be7d7b4581b4fdda2dfe714d17af22460254e9689d2cea6b0ae |
| `srv__atlas-mcp-utility__results__pilot__probe-report.json` | 2a5f34de60145be7d7b4581b4fdda2dfe714d17af22460254e9689d2cea6b0ae |

## Result

18 findings loaded, 18 verified. A claim that failed its re-probe, or wasn't re-probed, doesn't load. Those stay in rnd,
and the dispatch lists them.

## Privacy

- The identity scan found the account's email address in Relay's local ATOF file. That file stays private. The finding
  records the fact, not the value.
- The credentials check read the file's shape only: key names, lengths, and whether a value looks like a placeholder.
