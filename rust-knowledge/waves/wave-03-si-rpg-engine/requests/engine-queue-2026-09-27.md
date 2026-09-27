# si-rpg-engine queue, checked 2026-09-27

This is a check of the engine's working state against GitHub. It is not a measurement of the law. The engine's own queue is `docs/HANDOFF.md` at `09e3bf7`. Where this note and that file disagree, that file wins, except for the dispatch check below, which `HANDOFF.md` does not contain.

The afternoon overseer handoff of 2026-09-26 (open issues through #132, hand runs not yet done) is behind `main`. Do not dispatch from it.

## Open work

- **#144 merged** as `5ef97f9`. The bars were recomputed from the committed reports at `4c504a5`, not from the summary. Safety passes: 80 outputs, every proposal an intent for the walker with a catalog verb; 9 admitted, all walker moves. Value fails: arm M and arm G are 0 and 0 on all seven changes. `test-instrument` stays frozen.
- **#136 merged** as `895b2bf` on 2026-09-27. Commit `c0d3f55` corrects the red: an overlapping box, or a box that meets the head and is not carried. A carried box stays at speed 0. The law slice is the next build.

No other pull requests are open. Open issues: #97, #101, #109, #121, #128, #129, #131.

## Main's CI

`origin/main` has moved past `09e3bf7`: #136 merged as `895b2bf` and #144 as `5ef97f9`. `ci.yml` does not run on a docs-only push. The #144 merge touches fixtures, so it gets its own run.

The merge of #139, `828e825`, did run. Job `engines` in run `36283896661` failed in `npm audit` because the registry returned Bad Request. The suite did not start, and `arm` was skipped. That is not a failing test. The last green `engines` job on `main` in the recent list is the #142 merge, `06c18db`, which is before #139, #140, and #143. The README's test count has not been read off a CI `# tests` line for current `main`.

## Order

1. The T7c bars are recomputed and #144 is on `main`. `test-instrument` stays frozen.
2. Dispatch 128 is on `main`. Its law slice is the next build.
3. v0.3.0, after both are on `main`. The README, its seven translations, the handbook, and the CHANGELOG land before the tag. The release is a GitHub release. The package is not published to npm.
4. #97, #109, #129, and #131 can share one builder.
5. The Rapier 0.36.0 bump, with #101 folded into the same re-pin.
6. Mesh collision. No dispatch yet.

## Where the checkout is

The clone at the usual engine folder is on `dispatch-t7c-rewrite` at `19652d8`, which is not `main`. A measurement belongs on a fresh checkout of `origin/main`.

## This repository

`requests/crate-eject.md` is the #114 and #121 measurement. `requests/character-throw.md` is the relay of #128 and the carried-box check. The scratch line in the crate-eject note is a placeholder.
