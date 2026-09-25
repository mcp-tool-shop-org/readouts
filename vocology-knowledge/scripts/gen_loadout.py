#!/usr/bin/env python3
"""Generate .claude/loadout/index.json from the DB + catalog."""
import glob as _glob
import json
import os
import sqlite3

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
DB = os.path.join(ROOT, "findings.db")
OUTDIR = os.path.join(ROOT, ".claude", "loadout")
DATE_FALLBACK = "2026-09-04"

KW = {
    "vocology-source-filter": [
        "vocology", "source-filter", "formant", "glottal", "register", "vibrato",
        "breathiness", "singer", "phonation", "larynx",
    ],
    "musical-vs-speech-prosody": [
        "prosody", "speech", "singing", "duration", "f0", "pitch", "tts", "nhss",
    ],
    "lyric-to-note-alignment": [
        "alignment", "lyric", "lyrics", "phoneme", "midi", "vowel", "onset", "melisma",
    ],
    "svs-vs-song-generator": [
        "svs", "diffsinger", "ace-step", "diffrhythm", "midi-lock", "score", "generator",
        "singing-synthesis", "rvc", "svc",
    ],
    "eval-and-teaching-hci": [
        "eval", "mos", "mushra", "hci", "teaching", "practice", "admission", "singmos",
    ],
    # wave 2 — music as code; Comfy owns timbre
    "music-as-seconds-grid": [
        "seconds", "startsec", "pretty_midi", "music21", "abc", "musicxml", "smf", "ticks", "grid",
    ],
    "one-identity-retune-f0": [
        "identity", "retune", "f0", "world", "psola", "wsola", "timbre", "voice-conversion", "kokoro",
    ],
    "timing-as-contract": [
        "timing", "stamps", "warp", "place", "onset", "seed-audio", "duration", "clock",
    ],
    "comfy-cloud-audio-to-audio": [
        "comfy", "comfy-cloud", "sts", "speech-to-speech", "loadaudio", "elevenlabs", "chatterbox", "wav",
    ],
    # wave 7 — the spectrogram surface
    "vlm-spectrogram-reading": [
        "spectrogram", "vlm", "vision", "image", "gpt-4o", "few-shot", "audio-llm", "pitchbench", "blind",
    ],
    "time-frequency-representation": [
        "mel", "cqt", "hcqt", "stft", "log-mel", "whisper", "bins", "hop", "slaney", "htk", "transform",
    ],
    "spectrogram-rendering": [
        "render", "colormap", "magma", "viridis", "png", "overlay", "keyboard", "axis", "top_db", "1568", "riffusion",
    ],
    "audio-evaluation-metrics": [
        "fad", "clap", "mcd", "superflux", "onset", "swiftf0", "crepe", "rmvpe", "mir_eval", "metric", "compare_audio",
    ],
    "js-dsp-implementation": [
        "typescript", "javascript", "fft.js", "meyda", "essentia", "agpl", "librosa", "torchaudio", "pngjs", "analysernode", "license",
    ],
    # wave 8 — expansion: conversion, expression, articulation, datasets, assessment
    "breath-articulation": [
        "breath", "inhale", "consonant", "articulation", "plosive", "sibilant", "legato", "phrase", "diction",
    ],
    "expressive-control": [
        "vibrato", "dynamics", "expression", "portamento", "crescendo", "transition", "energy", "tension", "belt",
    ],
    "singing-assessment": [
        "assessment", "grading", "feedback", "practice", "rubric", "intonation", "register-classification", "avra", "tsfel",
    ],
    "singing-datasets": [
        "dataset", "corpus", "licence", "license", "provenance", "opensinger", "m4singer", "nhss", "kiritan",
    ],
    "singing-voice-conversion": [
        "svc", "conversion", "identity", "rvc", "so-vits", "timbre", "speaker", "cloning",
    ],
}
PAT = {
    "vocology-source-filter": ["formant", "phonation", "vibrato"],
    "musical-vs-speech-prosody": ["prosody", "duration", "f0"],
    "lyric-to-note-alignment": ["alignment", "midi", "phoneme"],
    "svs-vs-song-generator": ["svs", "midi", "generator"],
    "eval-and-teaching-hci": ["eval", "mos", "hci"],
    "music-as-seconds-grid": ["seconds", "midi", "grid"],
    "one-identity-retune-f0": ["identity", "f0", "timbre"],
    "timing-as-contract": ["timing", "onset", "stamps"],
    "comfy-cloud-audio-to-audio": ["comfy", "sts", "wav"],
    "vlm-spectrogram-reading": ["spectrogram", "vlm", "vision"],
    "time-frequency-representation": ["mel", "cqt", "stft"],
    "spectrogram-rendering": ["render", "colormap", "overlay"],
    "audio-evaluation-metrics": ["onset", "metric", "fad"],
    "js-dsp-implementation": ["typescript", "license", "librosa"],
    "breath-articulation": ["breath", "consonant", "articulation"],
    "expressive-control": ["vibrato", "dynamics", "expression"],
    "singing-assessment": ["assessment", "feedback", "practice"],
    "singing-datasets": ["dataset", "corpus", "licence"],
    "singing-voice-conversion": ["svc", "conversion", "identity"],
}


def est(path):
    if not os.path.exists(path):
        return 0, 0
    txt = open(path, encoding="utf-8").read()
    return max(0, len(txt) // 4), txt.count("\n") + 1


def main():
    con = sqlite3.connect(DB)
    con.row_factory = sqlite3.Row
    c = con.cursor()
    dr = c.execute("SELECT value FROM meta WHERE key='updated'").fetchone()
    date = dr[0] if dr else DATE_FALLBACK
    wr = c.execute("SELECT MAX(wave_number) FROM waves").fetchone()
    wave = wr[0] if wr and wr[0] is not None else 1
    cats = c.execute("SELECT * FROM categories ORDER BY sort").fetchall()
    os.makedirs(OUTDIR, exist_ok=True)
    entries = []

    t, l = est(os.path.join(ROOT, "catalog", "README.md"))
    entries.append({
        "id": "catalog-index", "path": "catalog/README.md",
        "keywords": ["vocology", "singing", "svs", "score-lock", "loadout", "catalog"],
        "patterns": [], "priority": "core",
        "summary": "vocology-knowledge catalog index + verified shortlist; drill into per-lane entries.",
        "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l,
    })

    for cat in cats:
        full = os.path.join(ROOT, "catalog", cat["slug"] + ".md")
        if not os.path.exists(full):
            continue
        nfind = c.execute(
            "SELECT COUNT(*) FROM findings WHERE category_id=?", (cat["id"],)).fetchone()[0]
        t, l = est(full)
        summ = f"{cat['name']}: {nfind} findings. {cat['description']}"[:120]
        entries.append({
            "id": cat["slug"], "path": f"catalog/{cat['slug']}.md",
            "keywords": list(KW.get(cat["slug"], [])),
            "patterns": PAT.get(cat["slug"], []), "priority": "domain", "summary": summ,
            "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l,
        })

    DISP_KW = ["vocology", "singing", "svs", "prosody", "midi", "score-lock", "jam"]
    VER_KW = ["verify", "verification", "citation", "prism", "roleos", "accept"]
    for wdir in sorted(_glob.glob(os.path.join(ROOT, "waves", "wave-*"))):
        if not os.path.isdir(wdir):
            continue
        wname = os.path.basename(wdir)
        disp = os.path.join(wdir, "dispatch.md")
        if os.path.exists(disp):
            t, l = est(disp)
            entries.append({
                "id": f"{wname}-dispatch", "path": f"waves/{wname}/dispatch.md",
                "keywords": DISP_KW, "patterns": ["vocology", "singing"], "priority": "domain",
                "summary": f"{wname} narrative: findings -> design implications."[:120],
                "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l,
            })
        ver = os.path.join(wdir, "verification.md")
        if os.path.exists(ver):
            t, l = est(ver)
            entries.append({
                "id": f"{wname}-verification", "path": f"waves/{wname}/verification.md",
                "keywords": VER_KW, "patterns": ["verification"], "priority": "domain",
                "summary": f"{wname} verifier receipt."[:120],
                "triggers": {"task": True, "plan": True, "edit": False}, "tokens_est": t, "lines": l,
            })
        rawj = os.path.join(wdir, "research-raw.json")
        if os.path.exists(rawj):
            t, l = est(rawj)
            entries.append({
                "id": f"{wname}-raw", "path": f"waves/{wname}/research-raw.json",
                "keywords": ["raw", "json"], "patterns": [], "priority": "manual",
                "summary": f"Raw {wname} swarm output — manual lookup only.",
                "triggers": {"task": False, "plan": False, "edit": False},
                "tokens_est": t, "lines": l,
            })

    index = {
        "version": "1.0.0",
        "schema": "ai-loadout/v1",
        "project": "vocology-knowledge",
        "generated": date,
        "wave": wave,
        "entries": entries,
    }
    out = os.path.join(OUTDIR, "index.json")
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(index, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    core = sum(e["tokens_est"] for e in entries if e["priority"] == "core")
    ondemand = sum(e["tokens_est"] for e in entries if e["priority"] != "core")
    print(f"loadout index: {len(entries)} entries — core {core} tok always-on, "
          f"{ondemand} tok on-demand. -> {out}")
    con.close()


if __name__ == "__main__":
    main()
