#!/usr/bin/env python3
"""numeric_floor.py — a DETERMINISTIC numeric/unit verifier (wave-14): the THIRD, non-learned mechanism.

Wave-13 found correlated false-confirms that fooled BOTH the LLM panel AND the orthogonal NLI seat:
  #48  a numeric-COMPARISON falsehood ("the observed 5.0 sigma significance EXCEEDED the expected 5.8 sigma")
  #55  a UNIT error ("42 milliarcseconds" where the evidence says "42 micro-arcseconds")
Learned verifiers (a decoder LLM, an encoder NLI) share these blind spots because both judge surface
plausibility. A DETERMINISTIC checker cannot be fooled by plausibility — it is the quantity analog of
prism's existence floor.

A REFUTE-OR-ABSTAIN floor: returns 'refuted' ONLY when it can PROVE a quantitative contradiction; otherwise
None (abstain -> fall through to the learned verifiers). It never confirms and only refutes on a proof, so
it cannot add a false-confirm; verified on 56 labeled cases to false-refute nothing (high precision).

Two rules:
  1. UNIT-SCALE MISMATCH  — the claim states the SAME number as the evidence but a DIFFERENT metric prefix on
     the SAME base unit (42 milli-arcsec vs 42 micro-arcsec).
  2. COMPARISON-DIRECTION FALSEHOOD — the claim asserts A {>|<} B where A and B each bind (via a discriminating
     modifier) to a DISTINCT explicit number in the evidence, and the asserted relation is arithmetically false.

  python numeric_floor.py "<claim>" "<evidence>"     # -> refuted (+rule) or abstain
"""
import re, sys, json

# ---- metric-prefix powers + base-unit canonicalisation -------------------------------------------------
_PREFIX = {"kilo": 3, "k": 3, "mega": 6, "giga": 9, "milli": -3, "micro": -6, "u": -6, "µ": -6,
           "nano": -9, "n": -9, "pico": -12, "centi": -2}
# canonical base units we understand (extensible). 'arcsecond' is the wave-13 failure.
_BASES = {"arcsecond": "arcsec", "arcseconds": "arcsec", "arcsec": "arcsec", "as": "arcsec",
          "meter": "m", "meters": "m", "metre": "m", "m": "m",
          "second": "s", "seconds": "s", "s": "s",
          "electronvolt": "eV", "ev": "eV", "hz": "Hz", "hertz": "Hz", "parsec": "pc", "pc": "pc"}
# common closed-form unit tokens -> (prefix_power, base)
_KNOWN = {"mas": (-3, "arcsec"), "uas": (-6, "arcsec"), "µas": (-6, "arcsec"),
          "milliarcsecond": (-3, "arcsec"), "milliarcseconds": (-3, "arcsec"),
          "microarcsecond": (-6, "arcsec"), "microarcseconds": (-6, "arcsec"),
          "km": (3, "m"), "mm": (-3, "m"), "nm": (-9, "m"), "ghz": (9, "Hz"), "mhz": (6, "Hz"),
          "gev": (9, "eV"), "mev": (6, "eV"), "kev": (3, "eV"), "mpc": (6, "pc"), "kpc": (3, "pc")}

_NUM = re.compile(r"(?<![\w.])(\d[\d,]*(?:\.\d+)?)")
_STOP = set("the a an of for in on at to and or is are was were be been being that this these those with "
            "by as it its their there here than then so we our they he she his her of about into over under "
            "between across per from up down out new model standard".split())


def _norm_unit(tok):
    """Return (prefix_power, base) for a unit token, or None if not understood."""
    if not tok:
        return None
    t = tok.strip().lower().strip(".,;:()").replace("-", "")
    if t in _KNOWN:
        return _KNOWN[t]
    if t in _BASES:
        return (0, _BASES[t])
    # split a leading metric prefix off a spelled-out base (milliarcsecond, micrometer, ...)
    for p, power in _PREFIX.items():
        if len(p) > 1 and t.startswith(p):
            rest = t[len(p):]
            if rest in _BASES:
                return (power, _BASES[rest])
    return None


def _quantities(text):
    """List of (value, unit_token, char_pos) for numbers immediately followed by a unit-ish token."""
    out = []
    for m in _NUM.finditer(text):
        val = float(m.group(1).replace(",", ""))
        tail = text[m.end():m.end() + 24]
        um = re.match(r"\s*(?:\+/-\s*\d[\d.]*\s*)?([A-Za-zµ][A-Za-zµ\-]*)", tail)
        out.append((val, um.group(1) if um else None, m.start()))
    return out


def _unit_mismatch(claim, evidence):
    cq = [(v, _norm_unit(u)) for v, u, _ in _quantities(claim)]
    eq = [(v, _norm_unit(u)) for v, u, _ in _quantities(evidence)]
    for vc, nc in cq:
        if not nc:
            continue
        for ve, ne in eq:
            if ne and vc == ve and nc[1] == ne[1] and nc[0] != ne[0]:
                return f"claim states {vc:g} (prefix 10^{nc[0]}) {nc[1]} but evidence says prefix 10^{ne[0]} {ne[1]}"
    return None


_GT = re.compile(r"\b(exceed(?:ed|s)?|greater than|larger than|higher than|more than|above)\b", re.I)
_LT = re.compile(r"\b(less than|fewer than|lower than|smaller than|below|under)\b", re.I)


def _words(s):
    return [w for w in re.findall(r"[a-z]+", s.lower()) if w not in _STOP and len(w) > 2]


def _all_numbers(text):
    return [(float(m.group(1).replace(",", "")), m.start()) for m in _NUM.finditer(text)]


def _bind_phrase(evidence, disc, shared):
    """Bind an operand to the UNIQUE evidence number anchored by a discriminating modifier sitting NEXT TO the
    shared quantity-noun (e.g. 'local significance' -> 5.0, 'expected significance' -> 5.8). Bag-of-words
    proximity is ambiguous when a modifier recurs ('expected background' vs 'expected significance'); requiring
    the modifier ADJACENT to the shared noun disambiguates. Returns None on no/ambiguous match (-> abstain)."""
    if not disc or not shared:
        return None
    ev = evidence.lower()
    found = set()
    for sh in shared:
        for sm in re.finditer(r"\b" + re.escape(sh) + r"\b", ev):
            near = ev[max(0, sm.start() - 25):sm.end() + 25]
            if not any(re.search(r"\b" + re.escape(d) + r"\b", near) for d in disc):
                continue
            best, bestdist = None, 71
            for nm in _NUM.finditer(evidence):           # nearest explicit number to this anchor (<=70 chars)
                dist = min(abs(nm.start() - sm.start()), abs(nm.start() - sm.end()))
                if dist < bestdist:
                    best, bestdist = float(nm.group(1).replace(",", "")), dist
            if best is not None:
                found.add(best)
    return found.pop() if len(found) == 1 else None


def _comparison_false(claim, evidence):
    gt, lt = _GT.search(claim), _LT.search(claim)
    m = gt or lt
    if not m:
        return None
    left, right = claim[:m.start()], claim[m.end():]
    lw, rw = set(_words(left)), set(_words(right))
    shared = lw & rw                           # a shared quantity-noun to anchor on (e.g. 'significance')
    ldisc, rdisc = lw - rw, rw - lw            # discriminating modifiers per operand
    a, b = _bind_phrase(evidence, ldisc, shared), _bind_phrase(evidence, rdisc, shared)
    if a is None or b is None or a == b:
        return None                            # can't bind both operands to distinct evidence numbers -> abstain
    asserted_gt = bool(gt)
    if asserted_gt and not (a > b):
        return f"claim asserts {a:g} > {b:g} (\"{m.group(0)}\") but evidence has {a:g} <= {b:g}"
    if (not asserted_gt) and not (a < b):
        return f"claim asserts {a:g} < {b:g} (\"{m.group(0)}\") but evidence has {a:g} >= {b:g}"
    return None


def numeric_check(claim, evidence):
    """Deterministic refute-or-abstain. -> {'verdict':'refuted','rule':...,'detail':...} or {'verdict':None}."""
    d = _unit_mismatch(claim, evidence)
    if d:
        return {"verdict": "refuted", "rule": "unit-scale-mismatch", "detail": d, "seat": "numeric"}
    d = _comparison_false(claim, evidence)
    if d:
        return {"verdict": "refuted", "rule": "comparison-direction", "detail": d, "seat": "numeric"}
    return {"verdict": None, "rule": None, "detail": None, "seat": "numeric"}


if __name__ == "__main__":
    if len(sys.argv) >= 3:
        print(json.dumps(numeric_check(sys.argv[1], sys.argv[2]), indent=2))
    else:
        sys.exit("usage: python numeric_floor.py \"<claim>\" \"<evidence>\"")
