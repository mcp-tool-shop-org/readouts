# Combat animation craft
_The designed-not-generated principles: anticipation -> active/hit frame -> follow-through -> recovery; smears, hit-stop, readable silhouettes, attack timing -- the animation principles that make combat game-readable._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

19 recipes · 10 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | Attack structure: anticipation → active/hit frame → follow-through → recovery | n/a | attack | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Author the 6 battle key-poses to biomechanical targets (hand-author, don't retarget, don't guess) | blender | all-motion | ▸ reproduced | ✅ yes | 5 | 5 | · |
| 2 | Exaggeration for small sprites: push poses 30–50% beyond naturalistic to survive the pixel grid | n/a | attack | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Follow-through and overlapping action: capes, hair, cloth settle after the primary motion ends | n/a | all-motion | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Hit-stop / freeze frame: the moment of impact is held to deliver game feel | n/a | attack | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Idle loop discipline: seamless loop, breathing breath, foot-contact discipline | n/a | idle | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Key-pose-first authoring: extremes before breakdowns before inbetweens | n/a | attack | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Readable silhouette: every key pose reads at thumbnail size in all 8 directions | n/a | attack | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Slow-in / slow-out (ease in/out): spacing that makes attacks feel weighted, not mechanical | n/a | attack | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Smear / multi-position blur frame: one frame captures the full arc of a fast swing | n/a | attack | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 9 | DQS Kavan — dual-quaternion vs LBS peer | docs | all-motion | docs | check | 4 | 4 | · |
| 9 | LLVM phi/SSA identity merge analog (hold-with-limit) | docs | all-motion | analog | check | 4 | 4 | · |
| 9 | Twelve principles pose-to-pose analog (hold-with-limit) | docs | all-motion | analog | check | 4 | 4 | · |
| 9 | Twelve principles — pose-to-pose + anticipation peer | docs | all-motion | docs | check | 4 | 4 | · |
| 9 | Unity IK foot/grip lock analog (hold-with-limit) | docs | all-motion | analog | check | 4 | 4 | · |
| 9 | Unity IK — Humanoid IK Pass / hand-foot goals | docs | all-motion | docs | check | 4 | 4 | · |
| 9 | Unity Root Motion anti-slide analog (hold-with-limit) | docs | all-motion | analog | check | 4 | 4 | · |
| 9 | Unity Root Motion — Bake Into Pose / Feet Root Y | docs | all-motion | docs | check | 4 | 4 | · |
| 9 | Unity Transform — child inherits parent weapon-chain peer | docs | all-motion | docs | check | 4 | 4 | · |

## Detail

### Attack structure: anticipation → active/hit frame → follow-through → recovery · `recommended` · ▸ reproduced
**A readable attack is authored in four beats — anticipation, active/hit frame, follow-through, recovery — not generated as uniform motion.**
Pull back to telegraph (anticipation), snap to the active/hit key frame (the moment the blow lands), continue the arc (follow-through), then settle to an idle-compatible end (recovery). The hit frame is the clearest, most exaggerated pose in the animation; the anticipation sells the weight that precedes it. For a 10-frame slash: ~2f anticipation/wind-up, 1f launch, 1–2f active+smear, 2f follow-through, 2f recovery, 1f return to idle-ready. Compressing any beat muddles the read; skipping anticipation makes the attack feel teleported rather than struck.
- **For the pipeline:** Every combat attack in the roster is storyboarded to these four beats before any rig or AI work begins. The hit frame is the storyboard's anchor — motion-verify checks for it explicitly. Recovery must land on a pose compatible with the idle loop so the character doesn't pop when the action ends.
- **Engine:** n/a · **Applies to:** attack · **Kind:** principle
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a) — Animation principle, no license.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| attack_slash_frames | 10 frames | ○ | 10f budget: 2 anticipation, 1 launch, 2 active/smear, 2 follow-through, 2 recovery, 1 return |
| attack_heavy_frames | 16 frames | ○ | Heavy/cast attacks can stretch to 14–16f; add more anticipation and longer recovery, not more smear |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Uniform-speed motion across all beats — the swing looks mechanical, not weighty |  |  |  |
| Missing anticipation — attack reads as teleport, player cannot react |  |  |  |
| Recovery that doesn't resolve to idle-compatible pose — causes visible pop on loop |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [The Animator's Survival Kit](https://www.amazon.com/Animators-Survival-Kit-Richard-Williams/dp/0571202284) (Richard Williams, 2001) — Codifies anticipation, the extreme key-pose method, and timing/spacing as the foundation of readable action in every animation medium including games. ; [The Illusion of Life: Disney Animation](https://www.amazon.com/Illusion-Life-Disney-Animation/dp/0786860707) (Frank Thomas, Ollie Johnston, 1981) — Introduces and defines the 12 principles of animation including anticipation and follow-through as the structural grammar of believable motion. ; [Animation Bootcamp: Fluid and Powerful Animation within Frame Restrictions](https://gdcvault.com/play/1020575/Animation-Bootcamp-Fluid-and-Powerful) (Mariel Cartwright (Lab Zero Games), 2014) — Demonstrates via Skullgirls and Street Fighter III that strong key frames plus anticipation and timing are the irreducible elements of readable combat animation, even within six-frame budgets.

### Author the 6 battle key-poses to biomechanical targets (hand-author, don't retarget, don't guess) · `recommended` · ▸ reproduced
**For static combat key-poses (idle-ready, guard, anticipation, strike, recovery, hurt) on an auto-rigged custom character, hand-author to biomechanical/silhouette targets solved numerically — it is faster than retarget-and-scrub for one frame, it is what shipped 2.5D/2D-from-3D games do, and it keeps restrictive mocap licenses out of the project.**
The combat-craft principles (key-pose-first, exaggerate 30-50%, silhouette-reads-8-ways) say WHAT makes a pose read but not the joint angles. This recipe instantiates the 6 canonical poses with construction targets: idle-ready = lowered COM, flexed hips/knees, weight on balls of feet, ASYMMETRIC (no twinning). guard = bladed/staggered feet, bent knees, hands raised to chest/face, ELBOWS TUCKED IN (boxing guard; longsword Pflug/Ochs). anticipation = move OPPOSITE the strike first (weapon drawn back, rear foot loaded, torso counter-rotated). strike = held extreme at the far end of the wind-up arc, clean profile silhouette. recovery = overshoot then settle, loose parts (cape) drag after the main mass. hurt = COM thrown outside the base of support (a discrete labelable class). Author by SOLVING joint angles to a target hand/foot position (numeric forward-kinematics), not eyeballing — the sprite-motion poser uses world-axis delta rotations solved to chest-height hand targets; a single-axis guess threw the arms up (a touchdown). Mocap libraries amortize MOTION, not a single frame, and the clean-licensed humanoid libraries (CMU, 100STYLE, Mixamo) rarely beat hand-posing for one key-frame; the non-commercial traps (AMASS/SMPL, Ubisoft LaFAN1) are blocked for a shipped game and retargeting does NOT relicense them.
- **For the pipeline:** Build a numeric pose-solver into the rig-proxy lane: name each key-pose's end-effector targets (hand at chest for guard, weapon-back for anticipation) and solve the bone rotations, then verify the silhouette in 8 directions. Cap authored joint flexion (see the rigging-lane deform recipe). The pose representation is role-keyed world-axis deltas (port across skeletons) resolved via the per-character roleMap. Never retarget AMASS/LaFAN1/Unreal-Lyra into a shippable asset.
- **Engine:** blender · **Applies to:** all-motion · **Kind:** technique
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a) — Animation principles + biomechanics; hand-authored poses are studio IP. AMASS/SMPL and Ubisoft LaFAN1 are NON-COMMERCIAL and must not be retargeted into shipped assets; CMU Mocap / 100STYLE (CC BY) / Mixamo (in-product) are the clean fallbacks if a clip is ever used.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Hand-authored pose looks wrong / arms thrown up (a 'touchdown' instead of a guard) | Guessing joint angles, or a single world-axis rotation that cannot express a real stance (a guard needs >1 axis per joint) | Solve the bone rotations numerically to a named end-effector target (hand at chest height, elbows tucked); use a multi-axis-per-role pose format | summary |
| All propless/posed characters default to the same splayed pose | No per-pose target authored; the rig falls back to a neutral spread | Author distinct body-attached targets per pose AND per character; validate the pose is deliberate and distinct, not just defect-free | summary |

- **Best for:** combat-keypose (-, fit -) ; rig-proxy-lane (-, fit -) ; pose-authoring (-, fit -)
- **Verify:** no external verdict — not checked
- **Sources:** [The Illusion of Life: Disney Animation](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation) (Frank Thomas, Ollie Johnston, 1981) — Staging, anticipation (move opposite first), and solid drawing without twinning are the structural grammar of a readable pose; the pose must read in silhouette before any detail. ; [The Animator's Survival Kit](https://archive.org/details/TheAnimatorsSurvivalKitRichardWilliams) (Richard Williams, 2001) — Test every key-pose in profile silhouette; the strike is the held extreme at the far end of the wind-up arc that then recoils. ; [GDC Animation Bootcamp: Fluid and Powerful Animation within Frame Restrictions](https://www.gdcvault.com/play/1020017) (Mariel Cartwright (Lab Zero Games), 2014) — With a ~6-frame punch budget, spend it on a distinct wind-up key + a held strike key (Skullgirls) — strong exaggerated extremes carry the read, not frame count. ; [NTU RGB+D: A Large Scale Dataset for 3D Human Activity Analysis](https://arxiv.org/abs/1604.02808) (Amir Shahroudy, Jun Liu, Tian-Tsong Ng, Gang Wang, 2016) — Strike and stagger are enumerated reproducible action classes (punch/kick/push and staggering/falling), confirming the key-pose set maps to real labeled poses. ; [Art Design Deep Dive: Using a 3D pipeline for 2D animation in Dead Cells](https://www.gamedeveloper.com/production/art-design-deep-dive-using-a-3d-pipeline-for-2d-animation-in-i-dead-cells-i-) (Thomas Vasseur (Motion Twin), 2018) — Dead Cells renders hand-keyframed 3D rigs down to pixel sprites ('animations are designed, like 2D animations, on key frames'); the 3D-to-2D win is asset reuse, not motion capture. ; [AMASS dataset license](https://amass.is.tue.mpg.de/license.html) (Max Planck Institute (Mahmood et al.), 2019) — AMASS prohibits 'any use for commercial purposes... incorporation in a commercial product' and bars training methods for commercial use; retargeting does not relicense it.

### Exaggeration for small sprites: push poses 30–50% beyond naturalistic to survive the pixel grid · `recommended` · ▸ reproduced
**At sprite resolutions of 32–64px, naturalistic poses lose their read — anticipation looks like micro-motion, weight looks like stillness; exaggerating every extreme pose by 30–50% beyond what feels right restores the intended read.**
Exaggeration (Thomas & Johnston principle 11) is not caricature for its own sake — it is the calibration required to preserve the intended read when images are scaled down to game resolution. A realistic pull-back of 15° in an attack anticipation becomes 2 pixels of shoulder shift at 32px; the player reads it as idle noise. Push the pull-back to 35–40° and the same pixel budget suddenly reads as an obvious wind-up. The rule of thumb from game animation practice: 'whatever feels about right, push it 30% further.' For attack poses this means weapon arm fully extended, torso leaned beyond comfort, weight planted on back foot. For hurt poses, the stagger is a full 45° lean, not a modest sway.
- **For the pipeline:** After posing the rig proxy, the animator runs a 50% scale check in the viewport — if the read is lost at 50%, the pose is not exaggerated enough. This test is cheaper than the full render pass. The AI polish step is explicitly warned not to 'normalize' or 'correct' extreme poses toward anatomical neutrality.
- **Engine:** n/a · **Applies to:** attack · **Kind:** principle
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a) — Animation principle, no license.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Naturalistic pose at small resolution — reads as idle or ambiguous; player cannot parse the beat |  |  |  |
| Exaggeration in only one direction (e.g. only the arm) — reads as distortion, not energy; push whole-body lean |  |  |  |
| AI polish normalizing extreme poses — if the diffusion pass 'corrects' anatomy, the exaggeration collapses and must be re-posed |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [The Illusion of Life: Disney Animation](https://www.amazon.com/Illusion-Life-Disney-Animation/dp/0786860707) (Frank Thomas, Ollie Johnston, 1981) — Exaggeration (principle 11) does not mean distortion for its own sake, but rather finding the essence of an action and amplifying it so the intended read survives reproduction — the smaller or faster the output medium, the more exaggeration is required. ; [Game Anim: Video Game Animation Explained (2nd ed.)](https://www.amazon.com/Game-Anim-Video-Animation-Explained/dp/0367707659) (Jonathan Cooper, 2021) — 'Real life never looks real enough' — game animators must create a hyper-real version of actions with poses accentuated and held longer than reality to read unmistakably from all angles and at all display scales. ; [Animation Bootcamp: Fluid and Powerful Animation within Frame Restrictions](https://gdcvault.com/play/1020575/Animation-Bootcamp-Fluid-and-Powerful) (Mariel Cartwright (Lab Zero Games), 2014) — Demonstrates that exaggerated extreme poses — not frame count — are the primary carrier of animation readability in fighting game sprites; examples from Skullgirls and Darkstalkers show extreme body lean and limb angle as the mechanism of weight communication.

### Follow-through and overlapping action: capes, hair, cloth settle after the primary motion ends · `recommended` · ▸ reproduced
**Secondary elements — cape, hair, scarf, loose belt — continue moving and settle after the character's primary mass stops, giving the attack weight and the idle loop organic life.**
Follow-through means parts of the body continue past the action and settle over time (sword arm swings past the hit line before returning). Overlapping action means different parts of the body move at different rates out of phase — the torso leads, the weapon arm lags; the cape lags the torso. Together these prevent the 'all parts stop simultaneously' rigidity that makes sprite characters feel hollow. For a 10-frame slash, the primary arm settles by frame 8; the cape or scarf adds 2–3 extra frames of trail (frames 9–11) before the idle loop starts. At 32×32 resolution, even 1–2 extra pixels of cloth shift per frame communicates the principle. In idle animations, subtle overlapping motion in hair or armor trim transforms a looping-position hold into a living character.
- **For the pipeline:** The studio's sprite authoring standard adds a 2-frame 'settle tail' to every attack strip beyond the nominal frame budget for any character with secondary geometry (cape, scarf, loose hair, tails). AI polish is explicitly told not to remove these trailing frames. Idle animations include at minimum one secondary element (hair, cloth edge, or armor piece) animated with a 1–2 frame phase offset from the breathing motion.
- **Engine:** n/a · **Applies to:** all-motion · **Kind:** principle
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a) — Animation principle, no license.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| settle_tail_frames | 2 frames | ○ | Add 2 settle frames past the recovery beat for characters with cloth/hair secondary geometry |
| overlap_phase_offset_idle | 2 frames | ○ | Secondary element (hair, cloth) lags the primary breathing motion by 2 frames in the idle loop |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| All body parts stop on the same frame — character feels frozen, not settled |  |  |  |
| Cape or hair that teleports back to idle position — breaks the weight read entirely |  |  |  |
| Settle tail not looped correctly — idle loop shows a visible seam where the cape pops back to start |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [The Illusion of Life: Disney Animation](https://www.amazon.com/Illusion-Life-Disney-Animation/dp/0786860707) (Frank Thomas, Ollie Johnston, 1981) — Principles 5 (follow-through and overlapping action): 'nothing stops all at once' — different parts of a body continue moving after the main action ends, driven by inertia; loose materials lead and lag the primary mass. ; [12 Principles for Game Animation](https://www.gamedeveloper.com/game-platforms/12-principles-for-game-animation) (Christopher Totten, 2021) — Follow-through and overlapping action add visual appeal and weight to game sprites; even at low resolutions, secondary elements with a phase offset from the primary motion communicate organic weight.

### Hit-stop / freeze frame: the moment of impact is held to deliver game feel · `recommended` · ▸ reproduced
**Holding the active/hit frame for 6–14 frames on successful contact (hit-stop) transforms a visual animation event into a physical sensation — the player feels the weight of the blow.**
Hit-stop (also called impact freeze) pauses both the attacker and the hit target at the moment of contact, converting the tail of the active period into held frames. The duration scales with attack weight: light attacks ~6–9f freeze, medium ~11f, heavy ~13–14f. During the freeze the hit-flash VFX and sound cue fire, compressing the sensory signal. Without hit-stop, attacks feel like they pass through enemies; with it, even a simple sprite animation communicates mass and consequence. The principle is engine-agnostic — it is applied at the state-machine level, not in the sprite frames themselves.
- **For the pipeline:** In the studio's combat system, the sprite sheet contains the active/hit key frame as a discrete frame. The engine state machine holds that frame index for the hit-stop duration, then resumes the follow-through strip. This means the sprite artist draws one definitive hit frame — the engine multiplies its screen time. Hit-stop duration is a tuning parameter (not baked into the sprite), so it can be adjusted without re-exporting assets.
- **Engine:** n/a · **Applies to:** attack · **Kind:** technique
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a) — Animation principle/technique, no license.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| hitstop_light_frames | 8 frames | ○ | Light attack hit-stop: 6–9f typical |
| hitstop_medium_frames | 11 frames | ○ | Medium attack hit-stop: 10–12f typical |
| hitstop_heavy_frames | 13 frames | ○ | Heavy/magic hit-stop: 12–14f; scale up for boss-level impact |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Zero hit-stop — attack looks like it passes through the enemy, no physical weight communicated |  |  |  |
| Hit-stop duration baked into the sprite sheet rather than the engine — makes tuning require re-export |  |  |  |
| Asymmetric hit-stop (only attacker freezes, target animates freely) — breaks the visual lock and reduces impact |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Impact Freeze](https://sonichurricane.com/?p=1043) (Maj (sonichurricane.com), 2010) — Defines and measures impact freeze in Street Fighter series: light attacks freeze ~9f, medium ~11f, hard ~13f; the freeze window is the primary mechanism for making contact feel weighty and enables cancel timing windows. ; [Game Feel: A Game Designer's Guide to Virtual Sensation](https://www.amazon.com/Game-Feel-Designers-Sensation-Kaufmann/dp/0123743281) (Steve Swink, 2008) — Identifies freeze frames and time distortion as core mechanisms of virtual sensation — brief pauses at moment of impact amplify the perceived weight of an action far beyond what continuous animation can achieve.

### Idle loop discipline: seamless loop, breathing breath, foot-contact discipline · `recommended` · ▸ reproduced
**An idle loop must hold foot contact points locked (no sliding), have its first and last frames match within 1px, and breathe through the torso or shoulders — not a uniform bob — to read as alive rather than oscillating.**
Foot-contact discipline is the most-violated idle rule: any lateral or vertical drift of the planted foot between frames appears as skating. Lock both foot positions as hard constraints when posing the idle — the torso and pelvis may move, the feet do not. Loop seam integrity requires that frame 1 and frame N are identical (or held for 2+ frames on each side) so the playback loop is invisible. Breathing motion is best carried through the chest/shoulder rise (2–4 pixels over 8–16 frames at rest) rather than through a whole-body bob, which looks like the character is on a spring. A subtle overlap in hair or cloth (offset by 2 frames from the breath) converts a mechanical oscillation into an organic loop.
- **For the pipeline:** The idle strip is the single most-played animation in any JRPG — it runs during every out-of-combat scene, every dialogue, and at the battle select screen. Idle quality is therefore a higher multiplier on perceived production tier than attack quality. The studio's idle QA checklist: (1) foot pixel drift < 1px frame-to-frame, (2) loop seam invisible at 1× scale, (3) at least one secondary element (cloth, hair) with a phase offset, (4) idle-end pose is compatible with attack-start anticipation pose.
- **Engine:** n/a · **Applies to:** idle · **Kind:** technique
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a) — Animation technique, no license.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| idle_frames_standard | 12 frames | ○ | 12f is a common idle loop budget at 12fps playback; 8–16f range depending on character expressiveness |
| breath_cycle_frames | 16 frames | ○ | A 16f breath at 12fps is ~1.3 seconds — naturalistic resting rate for a combat-ready character |
| foot_drift_tolerance | 1 pixels | ○ | Max 1px lateral or vertical drift per frame at the planted foot position |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Foot pixel drift — skating read at any playback speed; most common idle failure in sprite animation |  |  |  |
| Uniform whole-body bob — character appears to oscillate on a spring rather than breathe |  |  |  |
| Loop seam visible — first/last frame mismatch causes a pop that breaks immersion every few seconds |  |  |  |
| Idle pose incompatible with attack anticipation pose — transition into combat shows a hard snap |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [The Animator's Survival Kit](https://www.amazon.com/Animators-Survival-Kit-Richard-Williams/dp/0571202284) (Richard Williams, 2001) — Foot contact must be held as a fixed constraint in walk and idle animations; any lateral foot movement during a grounded contact frame reads as sliding, undermining physical weight and credibility. ; [2D Animation at Klei Entertainment](https://gdcvault.com/play/1020165/2D-Animation-at-Klei) (Jeff Agala (Klei Entertainment), 2014) — Klei's production standard for 2D character animation prioritizes quality of the looping idle as the baseline read of the character's weight and personality — loop seam integrity and contact discipline are non-negotiable.

### Key-pose-first authoring: extremes before breakdowns before inbetweens · `recommended` · ▸ reproduced
**Author the extreme key poses first — the clearest, most readable silhouettes of each beat — then place breakdowns, then inbetweens; never animate straight-ahead for combat.**
Pose-to-pose (key poses → breakdowns → inbetweens) gives the animator control over every important moment: you know exactly what frame the hit lands, what frame the anticipation peaks, what the recovery silhouette looks like. Straight-ahead animation drifts — characters migrate on-canvas and intent blurs into procedural motion. For sprite combat, draw the five load-bearing extremes first (idle-ready, anticipation peak, launch, active/hit, recovery) at full exaggeration, then populate inbetweens. If the extremes don't read at thumbnail size, adding inbetweens makes them worse, not better.
- **For the pipeline:** In the studio pipeline, the rig proxy's extremes are posed, rendered, and reviewed before any in-between frames are committed. This gives motion-verify a ground truth to check before AI polish is applied — catching silhouette failures cheaply rather than after the diffusion pass.
- **Engine:** n/a · **Applies to:** attack · **Kind:** principle
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a) — Animation principle, no license.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| extremes_count_attack_slash | 5 key poses | ○ | idle-ready / anticipation-peak / launch / active-hit / recovery |
| breakdowns_per_beat | 1 breakdown frames | ○ | One breakdown between each adjacent pair of extremes is usually enough at 8–12f total |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Straight-ahead sprite animation — character migrates across the canvas, hit frame loses its position |  |  |  |
| Adding inbetweens before fixing a weak extreme — propagates the bad pose rather than correcting it |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [The Animator's Survival Kit](https://www.amazon.com/Animators-Survival-Kit-Richard-Williams/dp/0571202284) (Richard Williams, 2001) — Contrasts pose-to-pose and straight-ahead methods, establishing that pose-to-pose gives the animator control over key dramatic moments; inbetweens only work if extremes are strong. ; [12 Principles for Game Animation](https://www.gamedeveloper.com/game-platforms/12-principles-for-game-animation) (Christopher Totten, 2021) — Explains that pose-to-pose is the foundation of readability for game sprites: 'draw the key ones (key poses and extremes) and one or two breakdowns, which were enough to define the motion.'

### Readable silhouette: every key pose reads at thumbnail size in all 8 directions · `recommended` · ▸ reproduced
**A combat pose must communicate its beat (anticipation, active, recovery) from its silhouette alone — no fill color, no detail — at every cardinal and diagonal direction.**
The staging principle (Thomas & Johnston) applied to 2.5D game sprites: if you fill the character with flat grey and can still identify the beat, the pose reads. This matters especially for 8-direction sprites because the oblique directions (NE/NW/SE/SW) often collapse depth cues: a side-slash that reads clearly at 0° can look like a forward-push at 45°. Each directional variant needs its own silhouette check. In pixel art, the rule tightens further — at 32×32 you may have 4–6 pixels of weapon arc to carry the read. Exaggerate limb separation and weapon angle beyond what feels right; it will read correctly at game resolution.
- **For the pipeline:** Every extreme key pose is silhouette-checked (desaturated flat render) before approval. The 8-direction render matrix exposes collapsed reads at oblique angles. Directional variants with failed silhouettes go back to the pose stage, not the inbetween stage.
- **Engine:** n/a · **Applies to:** attack · **Kind:** principle
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a) — Animation principle, no license.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Poses that read at the side angle but collapse at oblique — looks like a push or stumble instead of a slash |  |  |  |
| Over-reliance on color or shading to carry the read — when colors are flattened, the beat disappears |  |  |  |
| Small-sprite anticipation that is too subtle — body pull-back of 2px reads as idle micro-motion, not telegraph |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [The Illusion of Life: Disney Animation](https://www.amazon.com/Illusion-Life-Disney-Animation/dp/0786860707) (Frank Thomas, Ollie Johnston, 1981) — Staging principle: 'the presentation of any idea so that it is completely and unmistakably clear' — the pose must communicate through silhouette before any secondary information is added. ; [Game Anim: Video Game Animation Explained (2nd ed.)](https://www.amazon.com/Game-Anim-Video-Animation-Explained/dp/0367707659) (Jonathan Cooper, 2021) — Emphasizes hyper-real pose exaggeration for game animation: 'real life never looks real enough' — poses must be held and accentuated beyond naturalistic positions to read from all angles. ; [GDC 2015: Animating Ori and the Blind Forest](https://zyzyz.github.io/en/2018/01/GDC2015-Animating-Ori/) (James Benson (Moon Studios), 2015) — The team rendered the protagonist as a pure white silhouette against detailed backgrounds to ensure the character read clearly at all times — silhouette is the primary communication channel, not detail.

### Slow-in / slow-out (ease in/out): spacing that makes attacks feel weighted, not mechanical · `recommended` · ▸ reproduced
**Attacks that accelerate into the strike and decelerate out of it read as physically real; uniform-speed motion across all frames reads as mechanical puppet animation regardless of pose quality.**
Slow-in/slow-out (Thomas & Johnston principle 6) describes spacing: more frames (closer together in position) near the extremes, fewer and further-apart frames in the middle of an arc. Applied to a 10-frame slash: the anticipation pullback moves slowly at first (2–3 small-step frames), snaps fast through the active zone (smear + hit frame — wide spacing, few frames), then slows again in the follow-through settling frames. The deceleration into the recovery reads as inertia absorbed. The snap in the middle is what delivers impact. Flipping this (fast start, slow through, fast end) produces a floaty, underpowered read.
- **For the pipeline:** When posing the rig proxy, the animator deliberately over-spaces the active frames (large angular difference per frame) and under-spaces the recovery frames (small increments). Inbetween placement is checked against the spacing chart before AI polish, because diffusion models tend to average spacing toward uniform.
- **Engine:** n/a · **Applies to:** attack · **Kind:** principle
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a) — Animation principle, no license.
- **Fit:** rig 5/5 · studio 5/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Uniform spacing across all 10 frames — swing looks robotic; player perceives no weight |  |  |  |
| Fast start / slow end — reads as a limp push, not a strike; power feels absent at the active frame |  |  |  |
| Ease-in only (slow start, fast end with no follow-through deceleration) — character feels like it has no mass after the hit |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [The Illusion of Life: Disney Animation](https://www.amazon.com/Illusion-Life-Disney-Animation/dp/0786860707) (Frank Thomas, Ollie Johnston, 1981) — Slow-in/slow-out (principle 6): most natural actions accelerate from rest and decelerate before stopping; even spacing between key poses produces mechanical, lifeless motion. ; [The Animator's Survival Kit](https://www.amazon.com/Animators-Survival-Kit-Richard-Williams/dp/0571202284) (Richard Williams, 2001) — Devotes extended chapters to spacing and timing as the primary mechanism of weight; demonstrates how inbetween placement (not pose) is what makes an action feel heavy or light.

### Smear / multi-position blur frame: one frame captures the full arc of a fast swing · `recommended` · ▸ reproduced
**On the fastest frame of a swing, draw the limb or weapon as a smeared arc across its full travel path rather than as a frozen position — one smear frame sells speed that no inbetween can.**
A smear frame distorts, stretches, or ghost-multiples a limb across the frame to simulate motion blur in a medium that has no sub-frame timing. Instead of the sword at one angle, you draw a color-trail arc showing the path from entry to exit. At game playback speed (60fps or 24fps) this single frame registers as blinding velocity; paused or scrubbed it looks abstract. Three smear types (Thomas & Johnston codify these implicitly, later game-animation literature names them explicitly): elongated inbetween (limb stretched along path), motion trail (fading ghost copies), multiples (multiple limb positions overlaid). For 32×32 pixel sprites a 2–3 pixel wide color trail is sufficient.
- **For the pipeline:** The smear frame is the 3rd–4th frame of the 10-frame slash budget, placed immediately after launch and before the hold on the hit-pose. The AI polish pass must not remove or blur the smear — it is an authored intent frame, not a motion artifact. In sprite QA, the smear frame is checked to confirm it is distinct from its neighbors (not a duplicate), covers the expected arc, and doesn't bleed into the background boundary.
- **Engine:** n/a · **Applies to:** attack · **Kind:** technique
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: n/a) — Animation technique, no license.
- **Fit:** rig 5/5 · studio 5/5

**Hyperparameters**

| Param | Value | Req | Note |
|---|---|---|---|
| smear_frame_count | 1 frames | ○ | Usually 1 smear frame per fast swing beat; heavy attacks may use 2 sequential smear frames for a longer arc |
| smear_frame_position | 3 frame index (1-based) | ○ | In 10-frame slash: frame 3 = smear (launch→active transition) |


**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| No smear frame — the swing looks choppy or slow regardless of hit-stop |  |  |  |
| Smear that is too similar to adjacent frames — AI polish may average it away; make the shape distinct |  |  |  |
| Smear applied to slow attacks — smears only read as speed; on slow/heavy swings, use slow-in/slow-out instead |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Smearframes in Video Games](https://theses.fh-hagenberg.at/system/files/pdf/Lendenfeld18.pdf) (Christoph Lendenfeld, 2018) — Surveys smear frame types (elongated inbetweens, motion trails, multiples) and their use in game animation, with case studies from Overwatch, showing that smear frames communicate rapid motion in real-time interactive contexts without increasing frame rates. ; [The Illusion of Life: Disney Animation](https://www.amazon.com/Illusion-Life-Disney-Animation/dp/0786860707) (Frank Thomas, Ollie Johnston, 1981) — Overlapping action and follow-through principles imply that extreme fast-moving limbs between key poses must communicate the arc of travel, not a frozen intermediate position — the conceptual basis for smear frames.

### DQS Kavan — dual-quaternion vs LBS peer · `situational` · docs
**Dual-quaternion vs LBS artifacts — plate/weapon skinning peer**
STUDY-058 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [Geometric Skinning with Approximate Dual Quaternion Blending](https://users.cs.utah.edu/~ladislav/kavan08geometric/kavan08geometric.html) — Dual-quaternion vs LBS artifacts.

### LLVM phi/SSA identity merge analog (hold-with-limit) · `situational` · analog
**One identity value at a merge from predecessors — hold for cross-frame identity continuity; CFG ≠ CLIP drift.**
STUDY-058 Analogist Verifier ✅ hold-with-limit.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [LLVM LangRef phi](https://llvm.org/docs/LangRef.html#phi-instruction) — SSA phi merges predecessor values.

### Twelve principles pose-to-pose analog (hold-with-limit) · `situational` · analog
**Pose-to-pose before filling intervals — hold for authored 4–6 keyposes→inbetween→cleanup; squash ≠ rigid weapon length.**
STUDY-058 Analogist Verifier ✅ hold-with-limit.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [Twelve basic principles of animation](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation) — Pose-to-pose before filling intervals.

### Twelve principles — pose-to-pose + anticipation peer · `situational` · docs
**Pose-to-pose + anticipation — keypose craft analog peer**
STUDY-058 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [Twelve basic principles of animation](https://en.wikipedia.org/wiki/Twelve_basic_principles_of_animation) — Pose-to-pose + anticipation.

### Unity IK foot/grip lock analog (hold-with-limit) · `situational` · analog
**IK goals pose chains from end effectors — hold for foot-contact/grip lock; Mecanim ≠ orthographic 8-dir sprite cage.**
STUDY-058 Analogist Verifier ✅ hold-with-limit.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [Unity Inverse Kinematics](https://docs.unity3d.com/Manual/InverseKinematics.html) — IK goals (hands/feet) pose chains from end effectors.

### Unity IK — Humanoid IK Pass / hand-foot goals · `situational` · docs
**Humanoid IK Pass / hand-foot goals — foot/grip lock surface**
STUDY-058 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [Unity Inverse Kinematics](https://docs.unity3d.com/Manual/InverseKinematics.html) — Humanoid IK Pass / hand-foot goals.

### Unity Root Motion anti-slide analog (hold-with-limit) · `situational` · analog
**Root/Body + Bake Into Pose keeps orientation/displacement controlled — hold for root/anchor gates; ≠ diffusion canvas drift alone.**
STUDY-058 Analogist Verifier ✅ hold-with-limit.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [Unity Root Motion](https://docs.unity3d.com/Manual/RootMotion.html) — Root/Body transform + Bake Into Pose anti-slide.

### Unity Root Motion — Bake Into Pose / Feet Root Y · `situational` · docs
**Bake Into Pose; Feet for Root Y — root/anchor peer**
STUDY-058 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [Unity Root Motion](https://docs.unity3d.com/Manual/RootMotion.html) — Bake Into Pose; Feet for Root Y.

### Unity Transform — child inherits parent weapon-chain peer · `situational` · docs
**Child inherits parent — rigid weapon-chain peer**
STUDY-058 Practitioner Verifier ✅.
- **For the pipeline:** STUDY-058 Verifier ✅.
- **Engine:** docs · **Applies to:** all-motion · **Base:** general · **Kind:** technique
- **Output license:** commercial **check** (license: see-source) — STUDY-058 leftover minus prism deepen; verified=0
- **Fit:** rig 4/5 · studio 4/5
- **Verify:** STUDY-058 deepen; [no external verdict — not checked]
- **Sources:** [Unity Transform](https://docs.unity3d.com/Manual/class-Transform.html) — Child inherits parent.

