# Crate licences for a shipped MIT/Apache product — generator packet

Written by `google/gemini-3.1-pro-preview-20260219` through `scripts/openrouter_lane.py`; unverified until the wave's verification record says otherwise.

Q1: The shipped wasm law includes MIT, Apache-2.0, Unlicense, and Zlib; the native host adds BSD-1-Clause, while Unicode-3.0 remains build-time only. Q2: cargo-deny should allow MIT, Apache-2.0, Unlicense, Zlib, and BSD-1-Clause; MPL-2.0 requires file-level copyleft (safe for static linking if files are unmodified), and Apache-2.0 requires reproducing NOTICE files if present.

1. The wasm32 law ships with MIT, Apache-2.0, Unlicense, and Zlib.
2. The native host adds BSD-1-Clause and Apache-2.0-only.
3. Build-time licences (Unicode-3.0) do not reach the shipped binary.
4. cargo-deny enforces the allowed licence list.
5. Unlicense (midly) is public domain equivalent.
6. BSD-1-Clause (assert_no_alloc) requires copyright notice retention.
7. Apache-2.0-only (cpal) requires notice retention and NOTICE file reproduction.
8. MPL-2.0 allows static linking but requires modified files to be open.
9. Apache-2.0 NOTICE files must be reproduced in shipped products.
