"""Wave-8: blue-fidelity BASE SWAP. Chroma1-HD (Flux-family) LoRA via kohya flux_train_network.py --model_type chroma.
Resolves the wave-7 finding that SDXL base 1.0 can't do strong cyanotype blue. HANDS-ON measured. Idempotent (wave 8, recipes 167-168)."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()
HASH = "b90176156eaa546b"

c.execute("DELETE FROM waves WHERE wave_number=8")
c.execute("""INSERT INTO waves (wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path,notes)
VALUES (8,?,?,?,?,?,?,?,?)""", (
  "Blue-fidelity base swap: Chroma1-HD (Flux-family) LoRA via kohya flux_train_network.py - resolves the wave-7 SDXL blue ceiling",
  "2026-06-03",
  "training (Chroma/Flux LoRA: flux_train_network.py --model_type chroma)",
  0,
  "HANDS-ON MEASURED on the live RTX 5090. EXTERNAL_VERIFIER = the trigger-fires A/B in ComfyUI (Chroma generator, judged by "
  "direct visual inspection vs a base-only control) PLUS a LoRA-strength sweep; every image looked at. The blue question is "
  "answered by measurement, not assertion: the ship reaches strong white-on-prussian-blue cyanotype at LoRA strength 1.5-2.0.",
  "synthesized",
  "KICKOFF-kohya-style-lora.md blue-fidelity follow-up (was the wave-7 'wave-8 candidate')",
  "Z-Image/Lumina2 (the originally-named base) is NOT trainable here: Z-Image-Turbo's TE is Qwen3-4B but kohya lumina_train_network.py is hardcoded for Gemma-2; no Z-Image trainer installed. Pivoted to Chroma1-HD (Apache-2.0, Flux-family, kohya-native, a neutral LoRA base)."
))
w8 = c.execute("SELECT id FROM waves WHERE wave_number=8").fetchone()[0]
print("wave8 id =", w8)

body167 = (
"CHROMA1-HD LoRA :: BLUE-FIDELITY BASE SWAP (MEASURED hands-on 2026-06-03; RTX 5090). Resolves the wave-7 #165 finding that SDXL "
"base 1.0 cannot render a strong saturated non-natural palette (the cyanotype blue). Same cyanotype dataset + reg set + `stdstyl` "
"trigger as wave-7, so it is apples-to-apples across bases.\n\n"
"=== WHY CHROMA, NOT Z-IMAGE ===\n"
"The originally-named Z-Image/Lumina2 path is NOT viable on this rig: Z-Image-Turbo's text encoder is Qwen3-4B, but kohya's "
"lumina_train_network.py is hardcoded for Lumina-Image-2.0's Gemma-2 TE (load_gemma2, 'Lumina uses a single text encoder (Gemma2)'). "
"Z-Image only shares ComfyUI's 'lumina2' loader type; it is not a Lumina-2 model and has no kohya trainer here. Chroma1-HD is the "
"better vehicle anyway: 8.9B FLUX.1-schnell-derived, Apache-2.0 (LoRA inherits it), explicitly a neutral base for finetuning/LoRA "
"across artistic styles, on-disk, and natively kohya-trainable (library/chroma_models.py).\n\n"
"=== ENGINE: kohya flux_train_network.py --model_type=chroma ===\n"
"network_module = networks.lora_flux (NOT networks.lora). Chroma is T5-ONLY: pass --t5xxl + --ae, OMIT --clip_l (kohya uses a "
"dummy_clip_l). REQUIRED for Chroma: --guidance_scale=0.0 and --apply_t5_attn_mask. Recommended: --timestep_sampling=sigmoid, "
"--model_prediction_type=raw. LoRA trains the DiT only (228 FLUX blocks; T5 frozen, 0 TE modules) -> gating comes from the reg "
"contrast on the DiT, not TE training. Files all on disk: Chroma1-HD.safetensors (bf16 17.8GB), t5xxl_fp8_e4m3fn, ae.safetensors.\n\n"
"=== TWO GOTCHAS EARNED (both load-bearing) ===\n"
"1. --cache_text_encoder_outputs is INCOMPATIBLE with --apply_t5_attn_mask: the cached path leaves batch['input_ids_list']=None and "
"process_batch crashes at STEP 0 (TypeError: 'NoneType' object is not iterable, train_network.py:432). Chroma REQUIRES the attn mask, "
"so you MUST drop --cache_text_encoder_outputs (T5 runs live each step). Keep --cache_latents.\n"
"2. bf16 Chroma + live T5 SPILLS the 32 GB card: VRAM pinned at 31974/32607 MiB and step time ballooned 5 -> 34 s/it (WDDM paging GPU "
"mem to system RAM). Fix = --fp8_base (Chroma to ~fp8): VRAM ~20 GB, 2.65-2.71 s/it. ~27 min for 600 steps.\n\n"
"=== PROVEN CONFIG ===\n"
"Chroma1-HD.safetensors + --fp8_base, t5xxl_fp8_e4m3fn, ae; networks.lora_flux dim16/alpha16; AdamW; --guidance_scale 0.0 "
"--timestep_sampling sigmoid --model_prediction_type raw --apply_t5_attn_mask; --sdpa --gradient_checkpointing --cache_latents "
"(NO --cache_text_encoder_outputs); reg gating via dataset TOML (is_reg subset); 600 steps; seed 42. LoRA sha256[:16] " + HASH + " (107.0 MB).\n\n"
"=== RESULT (the answer to 'can a flexible base have it all') ===\n"
"YES, substantially -- and far better than SDXL base 1.0:\n"
"- GATING is crisp and CLEANER than SDXL: B (no trigger) = photorealistic / normal color (matches the reg set), C (trigger) = the "
"trained style. Base quality is much higher (B portrait is photographic).\n"
"- STRONG CYANOTYPE BLUE is ACHIEVED -- the thing SDXL base 1.0 never did at any setting. Strength sweep: the ship saturates to white "
"linework on DEEP PRUSSIAN BLUE at LoRA strength 1.5-2.0. The blue IS in the LoRA; recommended inference strength ~1.3-1.5.\n"
"- SUBJECT-DEPENDENT residual: scenes (ship) get the full blue field; ISOLATED subjects (portrait) render white-line on a WHITE "
"background even at strength 2.0. Root-caused: the REG images were generated on 'plain white background', so the contrast taught WHITE "
"as the neutral bg, which bleeds into the trigger case for subjects without a natural sky/sea region. FIX for universal blue: regenerate "
"the reg set with varied/colored backgrounds (not white).\n\n"
"CONCLUSION: the base swap RESOLVES the wave-7 blue ceiling. On a flexible commercial-safe base (Chroma, Apache-2.0) the cyanotype "
"blue + the linework style + token gating + high base quality all land together (strength ~1.5), where SDXL base 1.0 could only ever "
"get two of the three. Recipe in #168; proof grids waves/wave-08-chroma-baseswap/proof/."
)
c.execute("DELETE FROM config_recipes WHERE id IN (167,168)")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (167,?,?,?,?,?,?,?,?)""", (
  "training-chroma-flux-lora-baseswap-cyanotype-baseline-5090",
  "BASELINE (MEASURED): Chroma1-HD LoRA via kohya flux_train_network.py --model_type chroma -- resolves the SDXL blue ceiling (strong cyanotype at strength ~1.5)",
  5, 48, "baseline",
  "https://github.com/kohya-ss/sd-scripts",
  body167, w8))

body168 = (
"PROVEN (2026-06-03): kohya Chroma LoRA on the native-Windows RTX 5090 -- a FLEXIBLE commercial-safe base (Apache-2.0) that DOES render "
"a saturated non-natural palette (cyanotype blue), unlike SDXL base 1.0 (#165). Run by full script path (no accelerate launch needed).\n\n"
"COMMAND (the working config):\n"
"  $env:PYTHONUTF8='1'\n"
"  python flux_train_network.py `\n"
"    --pretrained_model_name_or_path <Chroma1-HD.safetensors> --model_type chroma `\n"
"    --t5xxl <t5xxl_fp8_e4m3fn.safetensors> --ae <ae.safetensors>  # NO --clip_l (Chroma is T5-only) `\n"
"    --dataset_config <chroma_dataset.toml>   # train subset + is_reg subset for gating `\n"
"    --output_dir <out> --output_name stdstyl_chroma_lora `\n"
"    --network_module networks.lora_flux --network_dim 16 --network_alpha 16 `\n"
"    --learning_rate 1e-4 --optimizer_type AdamW --lr_scheduler constant --max_train_steps 600 `\n"
"    --mixed_precision bf16 --save_precision bf16 --fp8_base `   # fp8_base is REQUIRED: bf16+live-T5 spills 32GB (34 s/it) `\n"
"    --sdpa --gradient_checkpointing --cache_latents `          # do NOT add --cache_text_encoder_outputs (see gotcha) `\n"
"    --guidance_scale 0.0 --timestep_sampling sigmoid --model_prediction_type raw --apply_t5_attn_mask `\n"
"    --save_model_as safetensors --seed 42 --max_data_loader_n_workers 0\n\n"
"TWO MUST-KNOW GOTCHAS:\n"
"  (1) --cache_text_encoder_outputs + --apply_t5_attn_mask => crash at step 0 (input_ids_list=None). Chroma needs the attn mask, so "
"omit TE caching (T5 runs live).\n"
"  (2) bf16 Chroma + live T5 spills VRAM (32GB pinned, 34 s/it). --fp8_base => ~20GB, 2.65 s/it. ~27 min / 600 steps.\n\n"
"INFERENCE / VALIDATE (ComfyUI, Chroma graph): UNETLoader(Chroma fp8mixed) -> LoraLoaderModelOnly(strength ~1.3-1.5) -> "
"ModelSamplingAuraFlow(shift 1.0) -> CFGGuider(cfg ~4) -> SamplerCustomAdvanced(euler / beta / 26 steps); CLIPLoader type='chroma' "
"(T5 only); ae VAE. The LoRA is DiT-only so LoraLoaderModelOnly is correct. Run base / LoRA+no-trigger / LoRA+trigger at one seed and LOOK.\n\n"
"PALETTE TUNING (earned): the cyanotype BLUE strengthens with LoRA strength -- use ~1.5 for strong white-on-prussian-blue (scenes). "
"Isolated subjects render white-bg line-art because the REG images used white backgrounds; for universal blue, regenerate the reg set "
"with varied/colored backgrounds so 'blue field' isn't contrasted away. PIN per run: base + dim/alpha + lr + trigger + seed + steps."
)
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (168,?,?,?,?,?,?,?,?)""", (
  "training-chroma-flux-lora-baseswap-cyanotype-recipe-5090",
  "RECIPE (PROVEN): kohya Chroma LoRA (flux_train_network.py --model_type chroma) -- exact command + the 2 gotchas + strength/reg palette tuning",
  5, 48, "recipe",
  "https://github.com/kohya-ss/sd-scripts/blob/main/docs/flux_train_network.md",
  body168, w8))

# cross-link from wave-7 #165
row = c.execute("SELECT body FROM config_recipes WHERE id=165").fetchone()
if row and "[RESOLVED wave-8]" not in row[0]:
    c.execute("UPDATE config_recipes SET body=? WHERE id=165",
      (row[0] + "\n\n[RESOLVED wave-8]: the base-swap fix was executed -> #167/#168. Chroma1-HD (Apache, Flux-family) DOES render the "
       "strong cyanotype blue SDXL base 1.0 could not (ship saturates at LoRA strength ~1.5), with cleaner gating + higher base quality. "
       "Z-Image/Lumina2 was infeasible (Qwen TE vs kohya's Gemma-2 lumina trainer); Chroma via flux_train_network.py --model_type chroma is the path.",))
    print("cross-linked #165 -> wave-8")

db.commit()
print("recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0])
for r in c.execute("SELECT id,kind,name FROM config_recipes WHERE id IN (167,168) ORDER BY id"):
    print(" ", r[0], r[1], "|", r[2][:72])
print("waves now:", c.execute("SELECT count(*) FROM waves").fetchone()[0])
db.close()
