"""KB profiles for the shared readout generators (gen_readout.py / gen_index.py).

The two KBs share a parallel schema (categories / <item> / <item>_purposes / purposes / sources / waves;
views v_recommended, v_best_for). A profile maps the per-item columns to the generic readout view, so one
renderer serves both. detect() picks the profile by which DB sits in the current working directory.
"""
import os

PROFILES = {
    "engines.db": {
        "kb": "tensor-engine-knowledge", "table": "engines", "fk": "engine_id", "noun": "engines",
        "what": "Verified knowledge base of the ENGINES that run & train AI models locally on the RTX 5090 (Blackwell / sm_120 / Windows) rig.",
        "axis": "native-Windows Blackwell survivability + commercial license (a LoRA/app inherits its engine's license).",
        "columns": [
            {"key": "rank", "label": "#", "type": "rank"},
            {"key": "name", "label": "engine", "type": "name", "sub": "developer"},
            {"key": "engine_type", "label": "type", "type": "text", "cls": "hideS"},
            {"key": "commercial_use", "label": "license", "type": "license"},
            {"key": "blackwell_ready", "label": "blackwell", "type": "flag", "on_label": "sm_120 ✓", "cls": "hideS"},
            {"key": "rig_fit", "label": "rig fit", "type": "meter"},
            {"key": "status", "label": "status", "type": "status"},
            {"key": "verified", "label": "✓", "type": "tick"},
        ],
        "detail_spec": [["developer", "developer"], ["language", "language"], ["latest_version", "version"],
                        ["maturity_tier", "maturity"], ["platforms", "platforms"], ["accelerators", "accelerators"],
                        ["model_formats", "formats"], ["multi_gpu", "multi-gpu"]],
    },
    "models.db": {
        "kb": "model-knowledge", "table": "models", "fk": "model_id", "noun": "models",
        "what": "Verified knowledge base of the best local generative-AI MODELS per purpose (image / edit / control / video / 3D / audio / LLM / caption) for the RTX 5090 rig — commercial-license-first.",
        "axis": "commercial license (a LoRA/asset inherits its base model's license) + fits 32 GB VRAM.",
        "columns": [
            {"key": "rank", "label": "#", "type": "rank"},
            {"key": "name", "label": "model", "type": "name", "sub": "developer"},
            {"key": "base_arch", "label": "arch", "type": "text", "cls": "hideS"},
            {"key": "commercial_use", "label": "license", "type": "license"},
            {"key": "runs_on_32gb", "label": "32GB", "type": "flag", "on_label": "fits ✓", "cls": "hideS"},
            {"key": "game_asset_fit", "label": "asset fit", "type": "meter"},
            {"key": "status", "label": "status", "type": "status"},
            {"key": "verified", "label": "✓", "type": "tick"},
        ],
        "detail_spec": [["developer", "developer"], ["base_arch", "arch"], ["params", "params"],
                        ["disk_size_gb", "disk GB"], ["min_vram_gb", "min VRAM GB"], ["recommended_vram_gb", "rec VRAM GB"],
                        ["runs_on_32gb", "fits 32GB"], ["quality_tier", "quality"], ["marketing_fit", "marketing fit"]],
    },
    "training.db": {
        "kb": "training-knowledge", "table": "techniques", "fk": "technique_id", "noun": "techniques",
        "what": "Verified knowledge base of portable TRAINING CRAFT — methods, recipes, hyperparameter values, dataset & eval know-how — for training LoRAs / fine-tunes on the single RTX 5090 (Blackwell / Windows / WSL2) rig. The how-to-train layer between the weights (model-knowledge) and the software (tensor-engine-knowledge).",
        "axis": "single-RTX-5090 training viability + reproducibility (fits 32 GB, commercial-clean output, complete replay provenance) — which method/recipe/data/eval you feed the engine and why, not which weights or which software.",
        "columns": [
            {"key": "rank", "label": "#", "type": "rank"},
            {"key": "name", "label": "technique", "type": "name", "sub": "method_family"},
            {"key": "applicable_to", "label": "for", "type": "text", "cls": "hideS"},
            {"key": "commercial_use", "label": "license", "type": "license"},
            {"key": "evidence_strength", "label": "evidence", "type": "text", "cls": "hideS"},
            {"key": "rig_fit", "label": "rig fit", "type": "meter"},
            {"key": "status", "label": "status", "type": "status"},
            {"key": "verified", "label": "✓", "type": "tick"},
        ],
        "detail_spec": [["method_family", "method"], ["applicable_to", "applies to"], ["base_model_family", "base"],
                        ["kind", "kind"], ["evidence_strength", "evidence"], ["engine_recipe_ref", "measured receipt"],
                        ["seed", "seed"], ["num_runs", "runs"], ["tuning_budget", "tuning budget"],
                        ["measured_conditions", "validated under"]],
    },
    "xrpl.db": {
        "kb": "xrpl-knowledge", "table": "capabilities", "fk": "capability_id", "noun": "capabilities",
        "what": "Verified knowledge base of the XRP Ledger ECOSYSTEM for a builder — protocol features, transaction types, XLS standards, client libraries & tooling — each tagged with its current mainnet / amendment status. Whole-ecosystem: XRPL mainnet + Xahau/Hooks + the XRPL EVM sidechain + the institutional layer (RLUSD, compliance).",
        "axis": "network_status — is this feature ACTUALLY enabled on XRPL mainnet right now (vs amendment-pending / devnet-only / deprecated), and which standard/library is current — plus which of the four build-focus tracks (game economies / NFT assets / payments / identity-compliance) it serves.",
        "columns": [
            {"key": "rank", "label": "#", "type": "rank"},
            {"key": "name", "label": "capability", "type": "name", "sub": "kind"},
            {"key": "network_status", "label": "network", "type": "text"},
            {"key": "chain", "label": "chain", "type": "text", "cls": "hideS"},
            {"key": "xls_standard", "label": "XLS", "type": "text", "cls": "hideS"},
            {"key": "builder_fit", "label": "fit", "type": "meter"},
            {"key": "status", "label": "use", "type": "status"},
            {"key": "verified", "label": "✓", "type": "tick"},
        ],
        "detail_spec": [["kind", "kind"], ["chain", "chain"], ["network_status", "network"], ["xls_standard", "XLS"],
                        ["amendment_name", "amendment"], ["enabled_date", "enabled"], ["maturity_tier", "maturity"],
                        ["key_fields", "key fields"], ["gotchas", "gotchas"]],
    },
}

def detect(cwd=None):
    cwd = cwd or os.getcwd()
    for db, p in PROFILES.items():
        if os.path.exists(os.path.join(cwd, db)):
            return db, p
    raise SystemExit("no known KB DB (engines.db / models.db / training.db) in " + cwd)
