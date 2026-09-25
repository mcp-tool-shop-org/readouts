"""Wave-7b: append the blue-fidelity investigation (runs v4-v5 + strength diagnostic) to #165/#166. Idempotent (marker-guarded)."""
import sqlite3, os
os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
db = sqlite3.connect('engines.db'); c = db.cursor()

MARK = "[UPDATE 2026-06-03 blue-fidelity fix, runs v4-v5]"
add165 = (
"\n\n" + MARK + ": Took a run at recovering the cyanotype BLUE that v2/v3 lost. "
"DIAGNOSTIC first -- v3 at LoRA strength 1.4 vs 1.0 brings out only slightly more blue (portrait shirt / ship hull) but stays "
"grayscale-engraving => blue is weakly-PRESENT, not strength-recoverable => a RECIPE issue, not inference. Then 2 training runs "
"spanning the recipe space (both dim32 = 217.9 MB):\n"
"  v4  dim32/alpha16 (=0.5 scaling, v1's blue-friendly) + reg --prior_loss_weight 0.5, 600 steps, 1.33 it/s (sha256[:16] 33eae5df15acf183): "
"softening BOTH scaling AND reg to protect color OVERCORRECTED -> color/blue-ish preserved but the STYLE barely imposes and GATING "
"collapses (B ~= C). Wrong end of the tradeoff.\n"
"  v5  dim32/alpha32 (=1.0 scaling, SAME as v3; capacity-isolation: ONLY the rank doubled vs v3's dim16) + reg pw1.0, 700 steps, 1.53 it/s "
"(sha256[:16] 5f7b70e0547ce7a4): ~= v3 -- strong engraving style, cleanly gated (B full color / C monochrome), STILL NO BLUE. => doubling "
"the LoRA RANK did NOT recover the blue.\n"
"DEFINITIVE CONCLUSION (5 configs v1-v5): on SDXL base 1.0 you CANNOT get strong-blue + strong-style + token-gating simultaneously. "
"Low effective scaling (alpha/dim = 0.5: v1, v4) keeps a blue TINT but weak style + weak gating; high scaling (1.0: v3, v5) gives strong "
"style + crisp gating but collapses into the base-EXPRESSIBLE grayscale engraving (no blue); RANK (dim16->32) is IRRELEVANT to the blue. "
"The binding constraint is SDXL base 1.0's COLOR PRIOR, not the kohya recipe -- it pulls any strongly-applied style into its natural "
"grayscale-engraving manifold and resists the saturated non-natural prussian blue. Proof grids: waves/wave-07-kohya-te/proof/07-09.\n"
"ACTIONABLE FIX: (a) a GAME house-style LoRA usually does NOT need token-gating (apply the style ALWAYS, dial it with LoRA strength) -> "
"train LIGHT like v1 (alpha8/dim16, ~300 steps, NO reg) and the blue survives; gating is only needed for a multi-style/toggle LoRA. "
"(b) If you need BOTH a saturated non-natural palette AND gating, SWAP THE BASE -- the best on-disk candidate is Z-Image-Turbo "
"(it GENERATED the flawless cyanotype training set, Apache-2.0 / commercial-safe), trained via kohya's lumina_train_network.py "
"(Lumina2 arch, NOT sdxl_train_network.py). That is a new trainer sub-path = a wave-8 candidate."
)
add166 = (
"\n\n" + MARK + ": blue-fidelity / palette note. SDXL base 1.0 RESISTS saturated non-natural palettes -- 5 configs proved no kohya knob "
"(rank, scaling, steps, reg weight) recovers a strong cyanotype blue while keeping strong style + gating (see #165). PRACTICAL: for a game "
"house-style LoRA drop the gating requirement and train LIGHT (alpha8/dim16, ~300 steps, no reg) to keep the palette, applying the style at a "
"chosen LoRA strength; for a saturated palette WITH gating, train on a more-flexible commercial-safe base (Z-Image-Turbo via "
"lumina_train_network.py, Apache-2.0) instead of SDXL base 1.0."
)

for rid, add in ((165, add165), (166, add166)):
    row = c.execute("SELECT body FROM config_recipes WHERE id=?", (rid,)).fetchone()
    if row and MARK not in row[0]:
        c.execute("UPDATE config_recipes SET body=? WHERE id=?", (row[0] + add, rid)); print("updated #%d" % rid)
    else:
        print("#%d already has the marker (skip)" % rid)

# sharpen the wave-7 note too
w = c.execute("SELECT notes FROM waves WHERE wave_number=7").fetchone()
if w and "blue-fidelity" not in (w[0] or ""):
    c.execute("UPDATE waves SET notes = notes || ? WHERE wave_number=7",
              (" Blue-fidelity follow-up (v4-v5): the cyanotype blue is NOT recoverable via kohya knobs on SDXL base 1.0 (proven across 5 configs) -- it is the base's color prior; fix = base swap (Z-Image/Lumina2) or drop gating for game styles.",))
    print("updated wave-7 notes")

db.commit()
print("done; #165 len", c.execute("SELECT length(body) FROM config_recipes WHERE id=165").fetchone()[0])
db.close()
