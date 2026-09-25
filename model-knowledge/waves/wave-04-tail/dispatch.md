# Wave 4 — Narrow tail: SCNet separation, Wan Fun-Control-Camera, FLUX.2 klein quants

**Wave 4** · 2026-06-02 · 4 lanes · 8 agents · **11 models**. Run `wf_d965200a-b97`. The last optional candidates — the verifier-flagged queue is now **fully drained**. KB total: **119 models**. (First wave ingested directly in the `readouts` monorepo.)

## Added

- **Audio separation, completed:** **SCNet-large** (MIT — strongest for bass/drum stems, ~10M params, near-real-time) + **SCNet-XL** (MIT — highest SDR ~9.8–10.08, the quality pick) + **UVR5** (MIT GUI front-end for non-coders; *output* license depends on the model you run through it).
- **Video control, completed:** the alibaba-pai **VideoX-Fun** line — **Wan2.2-Fun-A14B-Control + Control-Camera** (camera-trajectory conditioning) + QuantStack GGUFs. Clean finding: these Fun fine-tunes carry **Apache-2.0** (not the base-Wan terms) → commercial-safe controllable camera moves on 32 GB (GGUF Q-quants fit easily).
- **Image-base formalized:** FLUX.2 **klein** as proper rows across **two axes** (distilled-vs-base AND 4B-vs-9B): **klein 4B base / FP8 / NVFP4 = Apache** (commercial-safe); **klein 9B base = FLUX Non-Commercial** (the trap, now explicit per-row).
- **Comfy:** **comfyui_controlnet_aux** (Fannovel16, Apache) — the preprocessor pack — + Inspire-Pack + separation/camera workflow links.

## Verdict

11/11 verified (8 confirmed, 3 confirmed-with-fixes; 9 commercial-safe). Details in [verification.md](verification.md). **No outstanding verifier queue** — the catalog is broad and deep across all 9 domains; further waves are optional/topic-driven.
