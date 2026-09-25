# workflows/

ComfyUI workflow graphs (`.json`), organized by domain. Drop a workflow's exported
JSON in the matching folder; record it in the KB (`workflows` table) so it's searchable
alongside the models it needs.

```
workflows/
  image/      text-to-image, img2img, inpaint, ControlNet, upscale, detail
  video/      text-to-video, image-to-video
  3d/         image/text-to-3D (mesh + texture)
  audio/      music, SFX, TTS/voice
  utility/    batch, format conversion, captioning, glue graphs
```

## Conventions

- **Filename:** `<base>-<purpose>.json` — e.g. `flux-dev-txt2img.json`, `wan22-i2v.json`.
- **Pair each workflow with a note** of which models it needs and where they go
  (see the storage-convention table in the parent README), so a fresh rig can be
  rebuilt from this folder + the model catalog.
- **Importing:** drag the `.json` onto the ComfyUI canvas, or load via the menu.
  Use **ComfyUI-Manager** to auto-install any missing custom nodes a workflow needs.

## Not the same as game style-profiles

Per-game generation profiles (the canon-bound prompt/checkpoint configs) live under
`style-dataset-lab/projects/<game>/workflows/profiles/*.json` and are authoritative for
that game's look. This folder is the **general, reusable** workflow library — starting
points and utilities, not canon-locked game pipelines.

## Vetted sources

Curated, verified workflow sources and canonical starter graphs are recorded in the KB
by the wave-1 `comfy` lane:

```powershell
python -c "import sqlite3;[print(r) for r in sqlite3.connect(r'model-knowledge/models.db').execute('SELECT kind,name,url FROM workflows ORDER BY kind,name')]"
```

(Populated when wave 1 finishes synthesizing.)
