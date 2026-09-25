# Trl Grpo Mechanics
_auto-created from wave lane_ · wave 16 · 2026-09-13 · [‹ catalog index](README.md)

4 techniques · 3 recommended · 1 measured-on-rig. Narrative + plan: [dispatch](../waves/wave-01-foundation/dispatch.md).

| ↓ | Technique | Method | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|-----------|--------|---------|----------|------|-----|--------|---|
| 1 | clip_ratio is identically zero at the default num_iterations=1 | grpo | text | ▣ measured | ✅ yes | 5 | 4 | ✓ |
| 5 | A group-constant reward term has exactly zero gradient under GRPO | grpo | text | measured-in-source | ✅ yes | 5 | 5 | ✓ |
| 5 | GRPOConfig.seed does not control LoRA initialisation | peft | both | measured-in-source | ✅ yes | 5 | 5 | ✓ |
| 9 | TRL exposes no advantage hook — a fixed-reference advantage is a build | grpo | text | measured-in-source | ✅ yes | 4 | 3 | ✓ |

## Detail

### clip_ratio is identically zero at the default num_iterations=1 · `recommended` · ▣ measured
**With one optimizer pass per generation batch, the sampling policy IS the policy being updated, the importance ratio is ~1 by construction, and neither epsilon bound is reachable. Every epsilon/clip-higher lever is decoration.**
num_iterations defaults to 1 (grpo_config.py:684). Measured: all five clip_ratio/* series are exactly 0 across all 800 logged steps of a four-arm 200-step run, and again on an independent fresh run. A configuration running DAPO-style eps_low 0.2 / eps_high 0.28 was therefore running with both bounds inert.
- **For the pipeline:** Before tuning epsilon or adopting clip-higher, assert num_iterations > 1 or the change does nothing. Check clip_ratio/high_mean in the logs: identically zero means the trust region never engaged.
- **Method:** grpo · **Applies to:** text · **Base:** general · **Kind:** gotcha
- **Output license:** commercial **yes** — Apache-2.0 (TRL).
- **Fit:** rig 5/5 · studio 4/5
- **Verify:** verdict=confirmed | currency=2026-09-13 | Read in installed source at p2/trainer/.venv/.../trl 1.13.0 with file:line, not from docs or recall; each claim re-derived by a second reader the same day. Corroborated on 800 logged steps plus an independent fresh run.
- **Sources:** [TRL 1.13.0 grpo_config.py:684 + measured run logs (800 steps)](https://github.com/huggingface/trl) — num_iterations defaults to 1; clip_ratio series identically zero. ; [DAPO: An Open-Source LLM Reinforcement Learning System at Scale](https://arxiv.org/abs/2503.14476) — Introduces clip-higher (eps_low 0.2 / eps_high 0.28) motivated by near-identical sampled responses within groups.

### A group-constant reward term has exactly zero gradient under GRPO · `recommended` · measured-in-source
**Under group-mean-centred advantage, any reward component identical across all G rollouts of a group cancels exactly, so a group-level diversity/quality term trains identically to no term at all.**
grpo_trainer.py:2811-2813 computes advantages = rewards - mean_grouped_rewards, mean taken per group and repeat_interleaved, with scale_rewards defaulting to 'group'. A term that is constant within the group is removed by the subtraction. There is no error and no warning; every logged metric looks normal.
- **For the pipeline:** A diversity reward MUST be per-completion novelty against its siblings, never a per-group count. Verified independently in installed source and corroborated by Nie et al. 2026, whose title names the same centring failure. This was caught before a planned arm was built on it.
- **Method:** grpo · **Applies to:** text · **Base:** general · **Kind:** mechanism
- **Output license:** commercial **yes** — Apache-2.0 (TRL).
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** verdict=confirmed | currency=2026-09-13 | Read in installed source at p2/trainer/.venv/.../trl 1.13.0 with file:line, not from docs or recall; each claim re-derived by a second reader the same day.
- **Sources:** [TRL 1.13.0 grpo_trainer.py:2811-2813 and grpo_config.py:226,784](https://github.com/huggingface/trl) — advantages = rewards - mean_grouped_rewards; scale_rewards defaults to 'group'. ; [Gradient Starvation in Binary-Reward GRPO: Why Group-Mean Centering Fails and Why the Simplest Fix Works](https://arxiv.org/abs/2605.07689) — Group-mean centring gives exactly zero advantage on homogeneous groups; a fixed-reference Sign advantage A=2r-1 outperforms it at small group size.

### GRPOConfig.seed does not control LoRA initialisation · `recommended` · measured-in-source
**The seed is applied well after get_peft_model, so two runs at the same seed have different initial adapter weights. They are independent runs sharing a data order, not replicates.**
Documented in the trainer's own module docstring as TRL issue #6688(b). Pin initialisation by artifact instead: --save-init-adapter once, then --init-adapter on every arm.
- **For the pipeline:** Never treat same-seed runs as replicates, and never attribute a same-seed difference to the remaining variable (platform, hardware) without pinning init first. This exact reasoning error produced a published mechanism claim that three replications then refuted.
- **Method:** peft · **Applies to:** both · **Base:** general · **Kind:** gotcha
- **Output license:** commercial **yes** — Apache-2.0 (TRL).
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** verdict=confirmed | currency=2026-09-13 | Read in installed source at p2/trainer/.venv/.../trl 1.13.0 with file:line, not from docs or recall; each claim re-derived by a second reader the same day.
- **Sources:** [TRL issue #6688(b), asserted in p2/trainer/train.py docstring and handled at grpo_trainer init](https://github.com/huggingface/trl/issues/6688) — GRPOConfig.seed is applied after get_peft_model, so LoRA init is not seed-controlled.

### TRL exposes no advantage hook — a fixed-reference advantage is a build · `situational` · measured-in-source
**Both multi_objective_aggregation paths hard-code mean subtraction inside a ~500-line _generate_and_score_completions. No config value yields A = 2r - 1.**
Implementing a Sign or other fixed-reference advantage requires subclassing and overriding that method, and the override needs a probe proving it fired — an override that silently does not fire is invisible in metrics.
- **For the pipeline:** Price a fixed-reference-advantage experiment as a build with its own verification probe, not as a flag.
- **Method:** grpo · **Applies to:** text · **Base:** general · **Kind:** gotcha
- **Output license:** commercial **yes** — Apache-2.0 (TRL).
- **Fit:** rig 4/5 · studio 3/5
- **Verify:** verdict=confirmed | currency=2026-09-13 | Read in installed source at p2/trainer/.venv/.../trl 1.13.0 with file:line, not from docs or recall; each claim re-derived by a second reader the same day.
- **Sources:** [TRL 1.13.0 grpo_trainer.py:2347-2830](https://github.com/huggingface/trl) — Advantage computation is inline in _generate_and_score_completions; both aggregation paths subtract a mean.

