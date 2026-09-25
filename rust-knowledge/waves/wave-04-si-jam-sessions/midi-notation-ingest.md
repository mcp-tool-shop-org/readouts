# Score ingest inside a wasm law: SMF, MusicXML, ABC — generator packet

Written by `google/gemini-3.1-pro-preview-20260219` through `scripts/openrouter_lane.py`; unverified until the wave's verification record says otherwise.

Parse SMF via midly (alloc, no std), MusicXML via quick-xml or musicxml, and ABC via abc-parser, mapping all timing to a fixed integer PPQ and rejecting unrepresentable events.
1. midly with alloc parses SMF in wasm32 without std or rayon.
2. SMF formats 0/1/2 are supported; timing is Metrical or SMPTE.
3. midly's strict feature toggles error tolerance.
4. MusicXML crates vary in std/alloc requirements; quick-xml is pull-based, roxmltree is DOM, musicxml is a typed SDK.
5. MusicXML <divisions> must map to the fixed PPQ using exact integer arithmetic.
6. MusicXML <backup> and <forward> adjust a running integer time cursor.
7. abc-parser 0.4.0 provides PEG-based ABC parsing but lacks some advanced features.
8. Admitted events must be canonically re-encoded (e.g., as SMF Format 0) for the deterministic state hash.
