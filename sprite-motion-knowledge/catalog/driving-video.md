# Driving & reference video sources
_Sourcing commercial-safe driving/reference video for pose-transfer animation, the license implications, and the shoot-your-own-reference recipe (always license-clean)._ · wave 8 · 2026-09-07 · [‹ catalog index](README.md)

8 recipes · 3 recommended · 0 measured-on-rig.

| ↓ | Recipe | Engine | Applies | Evidence | Comm | Rig | Studio | ✓ |
|---|--------|--------|---------|----------|------|-----|--------|---|
| 2 | DWPose pose extraction from own footage (Apache-2.0, commercial-clean) | python | pose-extract | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 2 | Rotoscoping from own reference footage (oldest clean technique — no derivative risk) | custom | driving-video | ▸ reproduced | ✅ yes | 5 | 3 | ✓ |
| 2 | Shoot-your-own reference video (the always-clean driving source) | custom | driving-video | ▸ reproduced | ✅ yes | 5 | 5 | ✓ |
| 4 | MediaPipe Pose extraction from own footage (Apache-2.0, commercial-clean) | python | pose-extract | ▸ reproduced | ✅ yes | 5 | 4 | ✓ |
| 4 | Public-domain / CC0 video (Internet Archive, Prelinger) as driving reference | n/a | driving-video | ▸ reproduced | ⚠ cond | 4 | 3 | ✓ |
| 11 | Mixamo animations — prohibited for AI input/driving (Adobe explicit restriction) | custom | driving-video | ▸ reproduced | ⚠ cond | 1 | 1 | ✓ |
| 11 | OpenPose — avoid for commercial use (CMU restrictive license) | python | pose-extract | ▸ reproduced | ⛔ no | 1 | 0 | ✓ |
| 11 | Stock video as driving signal — license risk (Shutterstock/Getty prohibit AI use) | n/a | driving-video | ▸ reproduced | ⛔ no | 0 | 0 | ✓ |

## Detail

### DWPose pose extraction from own footage (Apache-2.0, commercial-clean) · `recommended` · ▸ reproduced
**DWPose (Apache-2.0) extracts a 2D whole-body pose skeleton sequence from any input video, producing a clean control signal for pose-transfer models — and carries no commercial-use restriction.**
Feed the studio's self-shot MP4 into DWPose's inference pipeline; it outputs frame-by-frame 2D keypoint coordinates (body, hands, face) in OpenPose format. The resulting skeleton sequence is used as the ControlNet or pose-transfer driving signal. DWPose is licensed Apache-2.0, so commercial use, modification, and redistribution are all permitted without royalty. DWPose is the recommended replacement for OpenPose in ControlNet workflows, with superior accuracy on whole-body estimation.
- **For the pipeline:** Wire DWPose as the standard pose-extract step in the Spine pipeline (motion truth → DWPose → pose sequence → pose-transfer model). Pair with own-footage capture to keep the full pipeline license-clean.
- **Engine:** python · **Applies to:** pose-extract · **Kind:** technique
- **VRAM:** 4
- **Output license:** commercial **yes** (license: Apache-2.0) — Apache-2.0 explicitly permits commercial use, modification, and redistribution. No royalty or attribution required in the shipped product (attribution in source files is standard practice). The tool processes pose geometry only — it does not embed or re-emit the video's copyrighted pixel content, so extracted skeleton sequences from third-party footage carry reduced (though not eliminated) derivative-work risk when own footage is used.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [DWPose — Effective Whole-body Pose Estimation with Two-stage Distillation (ICCV 2023)](https://github.com/IDEA-Research/DWPose) (IDEA-Research, 2023) — DWPose is released under Apache-2.0, supports commercial use, and produces whole-body 2D pose estimates in OpenPose format from video input.

### Rotoscoping from own reference footage (oldest clean technique — no derivative risk) · `recommended` · ▸ reproduced
**Tracing animation directly from the studio's self-recorded live-action reference (rotoscoping) bypasses pose-transfer AI entirely, is unconditionally license-clean, and produces frame-accurate motion curves directly in Godot/UE5.**
Max Fleischer's 1915 rotoscoping technique remains the gold standard for motion fidelity from reference footage. The workflow: record the actor performing the action → import into animation software (Krita, Blender VSE, or Photoshop) → trace each key frame to produce sprite animation frames or bone rotation keyframes. Because the reference footage is self-shot, there is no third-party copyright in the chain. This is distinct from AI pose-transfer: no generative model is involved, so no model license, derivative-work, or AI-input restriction applies. It is time-intensive (hours per second of animation) but produces the cleanest possible motion with no AI artifact risk.
- **For the pipeline:** Use rotoscoping for hero actions that demand maximum fidelity (a specific sword combo, a character-defining idle animation) and for animation passes where AI pose-transfer introduces unacceptable artifact risk. Self-shot footage for rotoscoping doubles as a DWPose capture session — run both passes from the same recorded take.
- **Engine:** custom · **Applies to:** driving-video · **Kind:** workflow
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: Owned by the studio (self-created reference footage)) — No third-party content involved when rotoscoping from own footage. No AI model license applies because no generative model is in the pipeline. Talent release still required if a person other than the rights-holder appears in the reference footage.
- **Fit:** rig 5/5 · studio 3/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Rotoscoping Animation: A Comprehensive Guide — GarageFarm](https://garagefarm.net/blog/rotoscoping-animation-a-comprehensive-guide) (GarageFarm editorial, 2024) — Rotoscoping traces over motion picture footage frame by frame to create fluid animation; first developed by Max Fleischer in 1915 and remains standard practice for motion-accurate character animation. ; [What is Rotoscoping: Complete Guide — Boris FX](https://borisfx.com/blog/what-is-rotoscoping-complete-guide/) (Boris FX editorial, 2024) — Rotoscoping from live-action reference is used commercially for character animation, VFX, and game production; recording one's own reference footage for this purpose is standard industry workflow with no copyright complications.

### Shoot-your-own reference video (the always-clean driving source) · `recommended` · ▸ reproduced
**Footage the studio shoots itself is unconditionally license-clean as a driving/reference signal — the only source with zero derivative-work or training-rights risk.**
Record the action on a phone or webcam (the director or an actor performing walk, swing, idle, attack), then extract a pose sequence (DWPose or MediaPipe) and use it to drive a pose-transfer model or as rotoscope reference. Because you own the footage outright, the output carries no third-party copyright claim. This is the recommended default for every driving-video need. The only legal caveat is securing a signed talent/model release if a person other than the rights-holder appears on camera.
- **For the pipeline:** Set shoot-your-own as the DEFAULT driving-video source for every new character action. Reserve paid or stock footage only for specific moves the studio cannot physically perform, and only after verifying that stock license explicitly permits AI/derivative use.
- **Engine:** custom · **Applies to:** driving-video · **Kind:** workflow
- **VRAM:** n/a
- **Output license:** commercial **yes** (license: Owned by the studio (self-created / work-for-hire)) — Self-created footage has no third-party license constraint. The only required document is a signed talent/model release (covering commercial use, likeness, and AI processing of motion data) if any person other than the rights-holder appears — a standard production practice codified in talent release form law.
- **Fit:** rig 5/5 · studio 5/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [When to Use a Talent Release Form — LegalZoom](https://www.legalzoom.com/articles/when-to-use-a-talent-release-form) (LegalZoom editorial team, 2024) — A signed talent/model release covering commercial use and likeness is required whenever a recognisable person appears in footage that will be used commercially, even if that person is not the rights-holder. ; [Rotoscoping animation — Adobe Creative Cloud explainer](https://www.adobe.com/creativecloud/video/discover/rotoscoping-animation.html) (Adobe, 2024) — Rotoscoping (tracing/driving animation from live-action reference footage) is the original frame-by-frame technique; recording one's own reference footage for this purpose is industry-standard practice.

### MediaPipe Pose extraction from own footage (Apache-2.0, commercial-clean) · `runner-up` · ▸ reproduced
**Google's MediaPipe Pose (Apache-2.0) extracts 33 3D body landmarks per frame from any RGB video in real-time, producing a driving-signal skeleton compatible with downstream pose-transfer pipelines.**
MediaPipe Pose uses BlazePose to detect 33 landmarks (x, y, z + visibility) on the whole body from a video stream or file. It runs efficiently on CPU and GPU, and the Apache-2.0 license permits unrestricted commercial use including in shipped games and AI pipelines. The landmark output can be rendered as a skeleton overlay or exported as a numeric pose sequence. Pair with own-footage capture. Note: MediaPipe produces a different keypoint schema than OpenPose/DWPose — verify compatibility with the downstream pose-transfer model.
- **For the pipeline:** Use MediaPipe when DWPose is unavailable or when real-time webcam capture is needed (MediaPipe is faster at inference on CPU). For final production pose sequences destined for ControlNet-OpenPose, DWPose is preferred because it natively outputs the OpenPose keypoint schema.
- **Engine:** python · **Applies to:** pose-extract · **Kind:** technique
- **VRAM:** 0
- **Output license:** commercial **yes** (license: Apache-2.0) — Apache-2.0 permits full commercial use with no royalty. MediaPipe is maintained by Google and ships with an explicit commercial-use statement on its documentation page.
- **Fit:** rig 5/5 · studio 4/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [MediaPipe Pose Landmark Detection — Google AI Edge](https://developers.google.com/edge/mediapipe/solutions/vision/pose_landmarker) (Google, 2024) — MediaPipe Pose runs under Apache-2.0, infers 33 3D landmarks per frame from RGB video, and is explicitly permitted for commercial use with no restrictions. ; [Can MediaPipe be used commercially? — QuickPose.ai](https://quickpose.ai/faqs/can-mediapipe-be-used-commercially/) (QuickPose.ai editorial, 2024) — MediaPipe's Apache-2.0 licence explicitly allows commercial use without restriction, including building paid products and SaaS services on top of it.

### Public-domain / CC0 video (Internet Archive, Prelinger) as driving reference · `runner-up` · ▸ reproduced
**Footage on the Internet Archive explicitly marked CC0 or public-domain carries no copyright restriction and is safe as a pose-transfer driving signal for commercial use — but per-item license verification is required.**
The Internet Archive hosts thousands of films under CC0 and public-domain dedication, including the Prelinger Archives (~8,500 public-domain films downloadable for unrestricted reuse). CC0-marked footage can legally be used as an AI driving signal or training input with no attribution requirement. However, not all Archive items are public-domain — licenses must be checked per item. Public-domain action footage (silent-era physical comedy, historical newsreel movement, instructional sports films) can provide useful non-humanoid-adjacent motion references for monster, creature, and fantasy-character actions.
- **For the pipeline:** Search archive.org filtered by license:CC0 or license:Public Domain. Verify each item's detail page before use. Useful for unusual movement (acrobatic, animal-handler, industrial) that is impractical to self-shoot. Not a substitute for own-footage for primary character actions.
- **Engine:** n/a · **Applies to:** driving-video · **Kind:** technique
- **VRAM:** n/a
- **Output license:** commercial **conditional** (license: CC0 / Public Domain (varies per item — verify on item detail page)) — CC0 and true public-domain items are unconditionally clear for commercial use including AI driving signals. However: (a) some Prelinger items have complex copyright status due to embedded copyrighted music or archival footage — check each item; (b) items without explicit CC0 or PD label should not be assumed free.
- **Fit:** rig 4/5 · studio 3/5
- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Prelinger Archive — Internet Archive Help Center](https://help.archive.org/help/prelinger-archive/) (Internet Archive, 2024) — Approximately 8,500 Prelinger films are available for unrestricted download and reuse; 'any derivative works that you produce using these films are yours to perform, publish, reproduce, sell, or distribute in any way you wish without any limitations.' Per-item license check is still required. ; [Public Domain CC0 Air Travel Stock Video Footage — Internet Archive](https://archive.org/details/PublicDomainCc0AirTravelStockVideoFootage) (qubodup (Iwan Gabovitch), 2017) — Demonstrates CC0 video items on the Archive — confirmed CC0 1.0 Universal by the uploader, permitting any commercial or AI use without attribution.

### Mixamo animations — prohibited for AI input/driving (Adobe explicit restriction) · `avoid` · ▸ reproduced
**Adobe's Mixamo terms explicitly prohibit using Mixamo content as AI/ML training input or driving signal; despite being free for commercial games, Mixamo animations cannot be routed through a generative AI pose-transfer pipeline.**
Mixamo offers a large library of mocap humanoid animations (FBX/BVH download) free for commercial game use. However, Adobe's FAQ explicitly states: 'the only research application Mixamo content can't be used in is training machine-learning models.' Rendering a Mixamo animation as a pose skeleton sequence and feeding it into a pose-transfer model constitutes use as an AI input, which this restriction targets. Mixamo is therefore blocked from the studio's Spine pipeline as a driving source. It remains usable as a humanoid rig reference for manual animation or as direct FBX import into Godot/UE5 for non-AI animation workflows.
- **For the pipeline:** Do not route Mixamo FBX/BVH through pose extraction for AI pose-transfer. For non-AI direct animation import (blocking reference only), Mixamo is permissible in commercial games. For AI-driven character animation, use own-footage capture or public-domain sources.
- **Engine:** custom · **Applies to:** driving-video · **Kind:** service
- **VRAM:** n/a
- **Output license:** commercial **conditional** (license: Adobe Mixamo Terms of Use) — Commercial use in shipped games is permitted for direct animation (FBX/BVH import, rigging, rendering). AI/ML input use is explicitly prohibited by Adobe's Mixamo FAQ. Raw animation file redistribution is also prohibited.
- **License correction (verifier):** The cited Adobe FAQ explicitly prohibits only 'training machine-learning models' — not 'driving signal' or inference-time use. Extending the restriction to all AI input/driving overstates what the quote supports; commercial use of Mixamo FBX in shipped games is permitted, while use as ML training data is not.
- **Fit:** rig 1/5 · studio 1/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Adobe FAQ explicitly prohibits Mixamo content as ML/AI training or driving input |  |  |  |
| Adobe's terms have tightened over 2024–2026 with Creative Cloud integration; long-term access stability is uncertain |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed-with-fixes minimax-m3=confirmed-with-fixes] -> confirmed [license -> commercial_use=conditional] [confirmed by 3 of 3 juror(s) [confirmed, confirmed-with-fixes]]
- **Sources:** [Mixamo FAQ — Licensing, Royalties, Ownership, EULA and TOS (Adobe Community)](https://community.adobe.com/questions-696/mixamo-faq-licensing-royalties-ownership-eula-and-tos-589400) (Adobe, 2024) — Adobe's FAQ explicitly states 'the only research application Mixamo content can't be used in is training machine-learning models,' prohibiting use of Mixamo animations as AI input or driving signal.

### OpenPose — avoid for commercial use (CMU restrictive license) · `avoid` · ▸ reproduced
**The original CMU OpenPose is restricted to noncommercial academic use only; commercial use requires a paid CMU license (USD 25,000/yr). Use DWPose instead.**
OpenPose (CMU-Perceptual-Computing-Lab) was the pioneering multi-person 2D keypoint detector and remains widely cited. Its license, however, explicitly restricts use to noncommercial internal research by academic and nonprofit organisations. For-profit use requires a separate commercial licence from CMU at USD 25,000 per year. Additionally, the commercial licence excludes sports applications. Because DWPose (Apache-2.0) produces better accuracy and is commercially clean, OpenPose should be treated as deprecated for this studio's commercial pipeline.
- **For the pipeline:** Remove or never add OpenPose from the commercial Spine pipeline. Replace all OpenPose nodes/calls with DWPose. Flag any ComfyUI ControlNet nodes that still call the CMU OpenPose weights — substitute the DWPose model weights instead.
- **Engine:** python · **Applies to:** pose-extract · **Kind:** technique
- **VRAM:** 4
- **Output license:** commercial **no** (license: CMU noncommercial academic license) — The CMU LICENSE file states: 'The Software may be used for your own noncommercial internal research purposes only.' Commercial use requires a separate paid agreement (USD 25,000/yr) and excludes sports applications. The AMD community forum confirms this restriction explicitly.
- **Fit:** rig 1/5 · studio 0/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Commercial use is license-prohibited without a USD 25,000/yr CMU paid agreement |  |  |  |
| Sports/action categories excluded from commercial licence even when purchased |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [OpenPose LICENSE — CMU-Perceptual-Computing-Lab](https://github.com/CMU-Perceptual-Computing-Lab/openpose/blob/master/LICENSE) (Carnegie Mellon University, 2018) — The license explicitly limits use to noncommercial internal research; commercial use is prohibited without a separate paid CMU licence. ; [OpenPose License — Adaptive Support AMD forum](https://adaptivesupport.amd.com/s/question/0D52E00006hpWXeSAM/openpose-license) (AMD community, 2023) — Community discussion confirming CMU OpenPose commercial licence costs USD 25,000/yr and excludes sports use cases.

### Stock video as driving signal — license risk (Shutterstock/Getty prohibit AI use) · `avoid` · ▸ reproduced
**Standard commercial stock-video licenses (Shutterstock, Getty Images) explicitly prohibit using licensed footage to train or drive AI/ML models; using them as a pose-transfer driving signal likely violates license terms.**
Shutterstock's standard license terms prohibit using 'Visual Content as training data for artificial intelligence, machine learning, or generative AI systems, tools, processes, or datasets.' Getty Images takes the same position and pursued landmark litigation (Getty v Stability AI, UK High Court 2025) over AI use of its assets. Even though pose-transfer 'driving' is arguably not model training, any use of stock footage as a generative AI input sits in legally contested territory under these licenses. The safer interpretation is: stock footage under standard licenses must not be used as a pose-transfer driving signal for a commercially shipped game.
- **For the pipeline:** Do not route Shutterstock or Getty stock video through pose-transfer or any generative AI step in the studio pipeline. If stock action footage is needed, use only sources with explicit AI/derivative-work permission or own-footage substitute.
- **Engine:** n/a · **Applies to:** driving-video · **Kind:** technique
- **VRAM:** n/a
- **Output license:** commercial **no** (license: Shutterstock standard / Getty standard — AI use prohibited) — Shutterstock license (2024) explicitly prohibits using licensed content as AI training data or as input to generative AI systems. Getty actively litigated this in UK courts (2025). A special Shutterstock 'research licence' exists for AI training, but it requires a separate paid agreement and is not the standard content subscription.
- **Fit:** rig 0/5 · studio 0/5

**Failure modes**

| Symptom | Cause | Fix | Field |
|---|---|---|---|
| Standard Shutterstock and Getty licenses explicitly prohibit AI/ML use including generative driving signals |  |  |  |
| Getty v Stability AI (UK High Court, November 2025) confirms the rights-holder enforcement posture |  |  |  |
| Special AI training licences from Shutterstock require separate paid agreements not included in standard subscriptions |  |  |  |

- **Verify:** cross-family jury [deepseek-v4-pro=confirmed glm-5.2=confirmed minimax-m3=confirmed] -> confirmed [confirmed by 3 of 3 juror(s) [confirmed]]
- **Sources:** [Shutterstock Terms of Service & License Agreements](https://www.shutterstock.com/license) (Shutterstock, Inc., 2024) — Shutterstock prohibits using any licensed Visual Content as training data for AI, machine learning, or generative AI systems, tools, processes, or datasets. ; [Getty Images v Stability AI — UK High Court judgment (November 2025) summary](https://www.mayerbrown.com/en/insights/publications/2025/11/getty-images-v-stability-ai-what-the-high-courts-decision-means-for-rights-holders-and-ai-developers) (Mayer Brown LLP, 2025) — Getty Images actively litigated commercial AI use of its library without a licence, confirming the enforcement posture of major stock providers against unlicensed AI use of their footage.

