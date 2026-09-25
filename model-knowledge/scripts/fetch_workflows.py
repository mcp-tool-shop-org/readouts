#!/usr/bin/env python3
"""Download a curated set of official Comfy-Org LOCAL-model starter workflows into
workflows/<domain>/ and register them in models.db (as a local 'wave 0' so model
waves never overwrite them). Re-run safe (idempotent by slug). Skips cloud api_* templates.
"""
import json
import os
import re
import sqlite3
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WF = os.path.join(ROOT, "workflows")
DB = os.path.join(ROOT, "models.db")
BASE = "https://raw.githubusercontent.com/Comfy-Org/workflow_templates/main/templates/"

# (folder, template filename, friendly description) — all LOCAL-model graphs
PICKS = [
    ("image", "image_z_image_turbo.json", "Z-Image-Turbo text-to-image — fast daily driver (Apache, commercial-safe)"),
    ("image", "image_qwen_Image_2512.json", "Qwen-Image-2512 text-to-image — quality + text rendering (Apache)"),
    ("image", "image_chroma_text_to_image.json", "Chroma text-to-image — FLUX-quality commercial-safe game-asset base"),
    ("image", "sdxl_simple_example.json", "SDXL base text-to-image — the LoRA-trainable workhorse"),
    ("image", "image_qwen_image_edit_2509.json", "Qwen-Image-Edit 2509 — instruction editing (Apache, commercial-safe)"),
    ("image", "flux_kontext_dev_basic.json", "FLUX.1-Kontext[dev] — instruction editing (NON-COMMERCIAL weights)"),
    ("image", "image_qwen_image_instantx_controlnet.json", "Qwen-Image + InstantX ControlNet — commercial-safe control"),
    ("image", "flux_fill_inpaint_example.json", "FLUX Fill — inpaint (NON-COMMERCIAL weights)"),
    ("video", "03_video_wan2_2_14B_i2v_subgraphed.json", "Wan 2.2 14B image-to-video — quality anchor"),
    ("video", "text_to_video_wan.json", "Wan text-to-video — starter"),
    ("video", "ltxv_image_to_video.json", "LTX-Video image-to-video — fast/marketing turnaround"),
    ("3d", "04_hunyuan_3d_2.1_subgraphed.json", "Hunyuan3D 2.1 image-to-3D — best PBR textures"),
    ("3d", "3d_hunyuan3d_image_to_model.json", "Hunyuan3D image-to-model — single-image mesh"),
    ("audio", "audio_ace_step1_5_xl_base.json", "ACE-Step 1.5 XL — music generation (MIT)"),
    ("audio", "audio-chatterbox_tts.json", "Chatterbox TTS — voice/VO (MIT)"),
    ("utility", "utility-frame_interpolation-film.json", "FILM frame interpolation — video helper"),
]
FOLDER_CAT = {"image": "image-base", "video": "video", "3d": "3d", "audio": "audio", "utility": "comfy"}


def slugify(s):
    s = re.sub(r"\.json$", "", s.lower())
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    return s or "wf"


def main():
    results = []
    for folder, fn, desc in PICKS:
        url = BASE + fn
        dest = os.path.join(WF, folder, fn)
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "model-knowledge-fetch"})
            data = urllib.request.urlopen(req, timeout=40).read()
            json.loads(data)  # validate JSON
            with open(dest, "wb") as f:
                f.write(data)
            results.append((folder, fn, desc, url, len(data), True))
        except Exception as e:  # noqa
            results.append((folder, fn, desc, url, 0, repr(e)))

    con = sqlite3.connect(DB)
    con.execute("PRAGMA foreign_keys=ON")
    c = con.cursor()
    r = c.execute("SELECT id FROM waves WHERE wave_number=0").fetchone()
    if r:
        wave0 = r[0]
    else:
        c.execute("""INSERT INTO waves(wave_number,title,dispatched_date,domain_scope,status,notes)
                     VALUES(0,'Local downloaded workflows','2026-06-02','workflows','local',
                     'Starter workflow .json files fetched from Comfy-Org/workflow_templates')""")
        wave0 = c.lastrowid
    cat = {s: i for s, i in c.execute("SELECT slug,id FROM categories")}
    n = 0
    for folder, fn, desc, url, size, ok in results:
        if ok is not True:
            continue
        slug = slugify(folder + "-" + fn)
        rel = f"workflows/{folder}/{fn}"
        cid = cat.get(FOLDER_CAT.get(folder))
        c.execute("DELETE FROM workflows WHERE slug=?", (slug,))
        c.execute("""INSERT INTO workflows(slug,name,category_id,kind,file_path,url,description,status,wave_id)
                     VALUES(?,?,?,?,?,?,?,?,?)""", (slug, fn, cid, "workflow", rel, url, desc, "downloaded", wave0))
        n += 1
    con.commit()
    con.close()

    for folder, fn, desc, url, size, ok in results:
        print(("OK   " if ok is True else "FAIL ") + f"{folder}/{fn}" + (f"  {size} B" if ok is True else f"  {ok}"))
    ok_n = sum(1 for r in results if r[5] is True)
    print(f"\ndownloaded {ok_n}/{len(PICKS)} workflows; registered {n} in DB (wave 0 = local).")


if __name__ == "__main__":
    main()
