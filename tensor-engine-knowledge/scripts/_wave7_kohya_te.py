"""Wave-7 kohya text-encoder + trigger-token style-LoRA path (HANDS-ON, measured on the live RTX 5090).
Extends #150/#151 (unet-only) to the real TE+trigger path. Idempotent on wave_number=7 and recipe ids 165-166.
EXTERNAL_VERIFIER = the trigger-fires A/B in ComfyUI (SDXL generator, judged by direct visual inspection
of with-vs-without-trigger output against a base-only control; every image looked at). 3 runs cross-check.
"""
import sqlite3, os, hashlib
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()

def sha(p):
    if not os.path.exists(p): return "MISSING"
    h = hashlib.sha256()
    with open(p, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''): h.update(b)
    return h.hexdigest()[:16]

OUT = r"E:\AI\training\output"
h_v1 = sha(os.path.join(OUT, "stdstyl_te_lora.safetensors"))
h_v2 = sha(os.path.join(OUT, "stdstyl_te_lora_v2.safetensors"))
h_v3 = sha(os.path.join(OUT, "stdstyl_te_lora_v3.safetensors"))
print("LoRA sha256[:16]  v1", h_v1, " v2", h_v2, " v3", h_v3)

# --- Wave 7 (hands-on, no swarm) ---
c.execute("DELETE FROM waves WHERE wave_number=7")
c.execute("""INSERT INTO waves (wave_number,title,dispatched_date,domain_scope,agent_count,verifier_note,status,dispatch_path,notes)
VALUES (7,?,?,?,?,?,?,?,?)""", (
  "kohya text-encoder + trigger-token style-LoRA path (hands-on) - extends #150/#151 from unet-only",
  "2026-06-03",
  "training (kohya_ss SDXL LoRA: TE training + trigger token + regularization gating)",
  0,
  "HANDS-ON MEASURED on the live RTX 5090 (kohya train-log it/s; nvidia-smi clean peak VRAM). EXTERNAL_VERIFIER = "
  "the trigger-fires A/B test in ComfyUI: the SDXL generator's output is judged by direct visual inspection of "
  "with-trigger vs without-trigger images against a base-only control (a DIFFERENT signal from the generator; the "
  "LoRA cannot 'explain' itself, the image is the only evidence; every image looked at per the visual-pipeline "
  "look-at-images rule). A semantically-EMPTY trigger (stdstyl) rules out the token's CLIP prior as the cause. "
  "Three runs (v1 alpha8/300, v2 alpha16/600, v3 alpha16/700+reg) cross-checked every finding.",
  "synthesized",
  "KICKOFF-kohya-style-lora.md Path A (engine proof; canon-free neutral cyanotype style)",
  "Path B (real game canon) deferred: style-dataset-lab outputs/approved/ is empty post-2026-04-27 reformat and needs Mike's sign-off before generating for a game."
))
wave7 = c.execute("SELECT id FROM waves WHERE wave_number=7").fetchone()[0]
print("wave7 id =", wave7)

# --- #165 baseline (cat 5 training, engine 48 kohya_ss) ---
body165 = (
"kohya_ss SDXL LoRA :: TEXT-ENCODER + TRIGGER-TOKEN ENGINE PROOF (MEASURED hands-on 2026-06-03; RTX 5090 / sm_120 / 32 GB / "
"driver 610.47). Extends #150/#151 (which were dim16 UNET-ONLY on a throwaway subject set) to the REAL style-LoRA path: "
"text-encoder training ON + a trigger token + regularization gating. Same venv as #151 (E:\\AI\\training\\sd-scripts\\.venv, "
"py3.11, torch 2.12.0+cu130, sm_120 cap 12,0). Base = sd_xl_base_1.0.safetensors (Comfy-Org SDXL base). PINS per run below.\n\n"
"=== THE #151 CAPTION BUG (high-value, root-caused) ===\n"
"#151's train.log shows 'No caption file found for 10 images ... class token will be used' with caption_extension=.caption, "
"yet _dataset_gen.py wrote .txt captions. kohya's DEFAULT caption_extension is .caption, so #151 SILENTLY IGNORED its own "
".txt captions and trained on the folder class-token (frontiertraveler) -- the fronttrav trigger NEVER entered training. "
"FIX: pass --caption_extension .txt AND verify the log prints 'read caption: N/N' with NO 'No caption file found' warning. "
"This is load-bearing: the entire TE+trigger path depends on the trigger being in the READ captions. Confirmed fixed here "
"(log: 'read caption: 100%|##| 16/16', caption_extension: .txt).\n\n"
"=== MEASURED it/s (steady-state, train-log) ===\n"
"  v1  dim16 alpha8  unet_lr1e-4 te_lr5e-5  300 steps        : 1.66 it/s   (sha256[:16] " + h_v1 + ", 109.1 MB)\n"
"  v2  dim16 alpha16 unet_lr1e-4 te_lr1e-4  600 steps        : 1.46 it/s   (sha256[:16] " + h_v2 + ", 109.1 MB)\n"
"  v3  dim16 alpha16 unet_lr1e-4 te_lr1e-4  700 steps + REG  : 1.25 it/s   (sha256[:16] " + h_v3 + ", 109.1 MB)\n"
"  (ref #150/#151 unet-only: ~1.40 it/s, 81.5 MB)\n"
"=> TE training is ~FREE vs unet-only (the TE backward is cheap next to the latent-cached UNet path; v1 even edged 1.40). "
"REGULARIZATION (prior-preservation) costs ~20-25% throughput (1.66 -> 1.25) because half the batches are reg images. "
"TE-trained LoRA is 109.1 MB vs unet-only 81.5 MB (the trained 264 TE LoRA modules add ~28 MB; 722 UNet modules unchanged).\n\n"
"=== MEASURED VRAM (nvidia-smi 1 s) ===\n"
"CLEAN kohya-only peak (ComfyUI POST /free first): 19.42 GB at dim16/batch1/1024/bf16/AdamW/--sdpa -- ~12 GB headroom on 32 GB. "
"Co-resident-with-ComfyUI peak hit 31.27 GB (ComfyUI still held ~13.6 GB of Z-Image from dataset gen) = right at the ceiling. "
"=> POST {'unload_models':true,'free_memory':true} to ComfyUI /free (or close it) BEFORE training. Peak power 231 W, 51 C (light).\n\n"
"=== THE TRIGGER-FIRES A/B (the verifier) ===\n"
"Design: trigger = 'stdstyl' (deliberately a NON-WORD, so any style in the output proves TRAINING, not the token's pretrained "
"CLIP meaning). Dataset = 16 varied non-canon subjects (teapot/fox/bicycle/.../desk-lamp) in ONE consistent style (cyanotype "
"blueprint: white linework on deep prussian blue), generated by ComfyUI Z-Image-Turbo nvfp4. Captions 'stdstyl, <subject>' "
"(trigger carries the STYLE; NO style words in the caption -> style binds to the token). Held-out A/B subjects (ship, locomotive, "
"portrait) were NOT in training (also tests generalization). 3 cells per subject, same seed: A base+trigger(no LoRA) / "
"B LoRA+NO-trigger / C LoRA+trigger. Decisive = B vs C (LoRA loaded for both, only the token toggled). Proof images: "
"waves/wave-07-kohya-te/proof/03-06_*.png.\n\n"
"=== FINDINGS (the de-risking payload) ===\n"
"1. MECHANIC VALIDATED end-to-end: captions read, TE LoRA trains (264 modules, te_lr active), token learned, LoRA loads+applies "
"in ComfyUI, A/B measured. Closes the wave-5/6 'kohya TE+trigger' candidate.\n"
"2. GATING NEEDS CONTRAST. A single-style dataset with the trigger in EVERY caption and no counter-examples makes the style "
"learn LARGELY UNCONDITIONALLY -- the trigger CORRELATES with the style but cannot GATE it (it is perfectly correlated in "
"training, so there is no pressure to gate). v1 (light) showed weak gating (with-trigger slightly more styled than without); "
"v2 (heavier) LOST it (with ~= without -- the UNet absorbed the style fully unconditionally). Adding REGULARIZATION images "
"(same 16 subjects, NORMAL full color, captioned WITHOUT the trigger -> --reg_data_dir) RESTORES gating (v3: no-trigger => "
"normal color, trigger => the trained style) -- crisp on ship + portrait, weak on the strongly-colored locomotive (its black+red "
"resist conversion). Prior-preservation contrast is what teaches 'trigger => style, absent => base.'\n"
"3. THE BASE MODEL BOUNDS THE STYLE. SDXL base 1.0 RESISTS deep-blue monochrome; under heavier optimization (alpha16 / 600-700 "
"steps) the LoRA drifts to the base-EXPRESSIBLE subset (grayscale engraving / line-art) and LOSES the target cyanotype BLUE. "
"v1 (alpha8/300) retained more blue but had weak gating. REAL TENSION: gating (reg + steps) vs color fidelity (lighter training / "
"stronger base). For a sellable game style needing a specific palette, train on a stronger/more-flexible commercial-safe base, "
"NOT SDXL base 1.0.\n"
"4. For a GAME HOUSE-STYLE LoRA you usually WANT the style applied unconditionally (controlled by LoRA strength), so token-gating "
"is OPTIONAL; reg images become mandatory only for a token-gated MULTI-style LoRA.\n\n"
"Recipe + exact commands in #166. Proof artifacts + the 3 harness scripts: waves/wave-07-kohya-te/."
)
c.execute("DELETE FROM config_recipes WHERE id IN (165,166)")
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (165,?,?,?,?,?,?,?,?)""", (
  "training-kohya-sdxl-lora-te-trigger-reg-gating-baseline-5090",
  "BASELINE (MEASURED): kohya SDXL LoRA text-encoder + trigger-token + reg-gating on Blackwell -- it/s + VRAM + the caption bug + gating findings",
  5, 48, "baseline",
  "https://github.com/kohya-ss/sd-scripts",
  body165, wave7))

# --- #166 recipe (cat 5 training, engine 48) ---
body166 = (
"PROVEN (2026-06-03): kohya_ss SDXL style-LoRA with TEXT-ENCODER training + a trigger token, on the native-Windows RTX 5090. "
"Extends #151 (unet-only). Run from any cwd by full script path (Python puts the script dir on sys.path so networks.lora resolves).\n\n"
"GOTCHAS (inherited + new):\n"
"  - $env:PYTHONUTF8='1' (sd-scripts' Japanese log strings crash the cp1252 console at loop start) -- #151.\n"
"  - --sdpa, NEVER xformers on Blackwell -- #151.\n"
"  - **--caption_extension .txt** (NEW, load-bearing): kohya defaults to .caption; without this flag your .txt captions are "
"SILENTLY ignored and it trains on the folder class-token (this is exactly how #151's trigger never trained). VERIFY the log "
"says 'read caption: N/N', NOT 'No caption file found'.\n"
"  - POST {'unload_models':true,'free_memory':true} to ComfyUI 127.0.0.1:8188/free before training, or co-residence pushes VRAM "
"to the 32 GB ceiling (clean kohya peak is only 19.42 GB).\n\n"
"DATASET DISCIPLINE (style LoRA, not subject LoRA): consistent STYLE + varied SUBJECTS. Caption = '<TRIGGER>, <subject>' with the "
"trigger a NON-WORD (e.g. stdstyl) and NO style words -> the style binds to the token. Folder '10_<neutralclass>' (10 repeats); the "
"class name is NOT the trigger so the trigger's only source is the captions. Generate the set via ComfyUI (see harness scripts).\n\n"
"COMMAND A -- TE + trigger, NO gating (style learned largely unconditionally; fine for a house-style LoRA used at a strength):\n"
"  $env:PYTHONUTF8='1'; $env:PYTHONIOENCODING='utf-8'\n"
"  python sdxl_train_network.py --pretrained_model_name_or_path <sd_xl_base_1.0.safetensors> `\n"
"    --train_data_dir <dataset_parent> --output_dir <out> --output_name <name> `\n"
"    --network_module networks.lora --network_dim 16 --network_alpha 16 `\n"
"    --learning_rate 1e-4 --unet_lr 1e-4 --text_encoder_lr 1e-4 `   # (removing --network_train_unet_only is what turns TE training ON)\n"
"    --optimizer_type AdamW --lr_scheduler constant --max_train_steps 300-600 `\n"
"    --mixed_precision bf16 --save_precision bf16 --sdpa --cache_latents `\n"
"    --resolution 1024,1024 --train_batch_size 1 --caption_extension .txt `\n"
"    --save_model_as safetensors --seed 42 --max_data_loader_n_workers 0\n\n"
"COMMAND B -- TE + trigger WITH token gating (style ONLY when the trigger is present): add a regularization set -- the SAME "
"subjects in NORMAL style, captioned WITHOUT the trigger -- and pass --reg_data_dir <reg_parent> (reg folder '10_<class>'). "
"kohya then applies prior-preservation so 'no trigger => base/normal, trigger => style'. Costs ~20-25% it/s. Validated v3 (crisp on "
"ship/portrait, weak on strongly-colored subjects).\n\n"
"VALIDATE (the verifier): generate the SAME held-out subject 3 ways at one seed -- base+trigger (no LoRA, control), LoRA+no-trigger, "
"LoRA+trigger -- and LOOK at all three. Style in (LoRA+trigger) but not (LoRA+no-trigger) => the trigger fires/gates. Use a non-word "
"trigger so the control proves the style is trained, not prompted.\n\n"
"PIN per run: base sd_xl_base_1.0.safetensors; dim/alpha; unet_lr/text_encoder_lr; trigger token; seed; max_train_steps; "
"caption_extension. (P3: also capture the base-model sha256 -- filename-only today.) Measured v1/v2/v3 hashes in #165. "
"Harness scripts (idempotent, HTTP to ComfyUI): _dataset_gen_stdstyl.py, _reg_gen_stdstyl.py, _lora_validate_stdstyl.py in "
"waves/wave-07-kohya-te/proof/ (and live at E:\\AI\\training\\).\n\n"
"WHEN YOU NEED A SPECIFIC PALETTE (e.g. the cyanotype blue that SDXL base 1.0 dropped): use a stronger/more-flexible commercial-safe "
"base, or lighter training (alpha8 / ~300 steps holds more of a base-resisted color), or anchor the color in the caption. See #165 finding 3."
)
c.execute("""INSERT INTO config_recipes (id,slug,name,category_id,engine_id,kind,url,body,wave_id)
VALUES (166,?,?,?,?,?,?,?,?)""", (
  "training-kohya-sdxl-lora-te-trigger-reg-gating-recipe-5090",
  "RECIPE (PROVEN): kohya SDXL style-LoRA with text-encoder + trigger token (+ optional reg gating) -- exact commands + the caption_extension fix",
  5, 48, "recipe",
  "https://github.com/kohya-ss/sd-scripts",
  body166, wave7))

# --- update #151: note the TE+trigger extension ---
row = c.execute("SELECT body FROM config_recipes WHERE id=151").fetchone()
if row:
    b = row[0]
    marker = ("\n\n[UPDATE 2026-06-03 wave-7]: EXTENDED from unet-only to the real text-encoder + trigger-token path -- "
              "#165 (baseline, measured) + #166 (recipe). Earned here: #151's .txt captions were SILENTLY ignored "
              "(kohya default caption_extension=.caption) so its fronttrav trigger never trained -- pass --caption_extension .txt "
              "and verify 'read caption: N/N'. TE training is ~free on it/s; token GATING needs regularization images "
              "(contrast); SDXL base 1.0 resists deep-blue and drifts to grayscale line-art under heavy training.")
    if "[UPDATE 2026-06-03 wave-7]" not in b:
        c.execute("UPDATE config_recipes SET body=? WHERE id=151", (b + marker,))
        print("updated #151")

db.commit()
print("recipes now:", c.execute("SELECT count(*) FROM config_recipes").fetchone()[0])
for r in c.execute("SELECT id,kind,name FROM config_recipes WHERE id IN (151,165,166) ORDER BY id"):
    print(" ", r[0], r[1], "|", r[2][:74])
print("waves now:", c.execute("SELECT count(*) FROM waves").fetchone()[0])
db.close()
