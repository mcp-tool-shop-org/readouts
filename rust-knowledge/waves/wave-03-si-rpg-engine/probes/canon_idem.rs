// Is si-rpg-engine's canon_quat idempotent? canon and canon_quat are copied verbatim from
// solver/src/rapier_law.rs on main (5ec07f0) and PR #53 (bb462c6), lines 68-70 and 138-157.
fn canon(x: f64) -> f64 {
    if x == 0.0 { 0.0 } else { x }
}

fn canon_quat(x: f64, y: f64, z: f64, w: f64) -> Option<(f64, f64, f64, f64)> {
    if x.is_nan() || y.is_nan() || z.is_nan() || w.is_nan() {
        return None;
    }
    let n = (x * x + y * y + z * z + w * w).sqrt();
    if !(n > 0.0) {
        return None;
    }
    let mut x = canon(x / n);
    let mut y = canon(y / n);
    let mut z = canon(z / n);
    let mut w = canon(w / n);
    if w.is_sign_negative() {
        x = canon(-x);
        y = canon(-y);
        z = canon(-z);
        w = canon(-w);
    }
    Some((x, y, z, w))
}

fn main() {
    // Deterministic inputs: an xorshift64 stream mapped to [-1, 1), plus near-identity rotations
    // like a resting box's (small x, y, z; w near 1).
    let mut s: u64 = 0x9E37_79B9_7F4A_7C15;
    let mut next = || {
        s ^= s << 13;
        s ^= s >> 7;
        s ^= s << 17;
        (s >> 11) as f64 / (1u64 << 53) as f64 * 2.0 - 1.0
    };
    let (mut moved, mut total, mut second_moved) = (0u32, 0u32, 0u32);
    let mut first: Option<((f64, f64, f64, f64), (f64, f64, f64, f64))> = None;
    for i in 0..200_000u32 {
        let q = if i % 2 == 0 {
            (next(), next(), next(), next())
        } else {
            (next() * 1e-4, next() * 1e-4, next() * 1e-4, 1.0)
        };
        let Some(a) = canon_quat(q.0, q.1, q.2, q.3) else { continue };
        let b = canon_quat(a.0, a.1, a.2, a.3).unwrap();
        let c = canon_quat(b.0, b.1, b.2, b.3).unwrap();
        total += 1;
        let bits = |t: (f64, f64, f64, f64)| [t.0.to_bits(), t.1.to_bits(), t.2.to_bits(), t.3.to_bits()];
        if bits(a) != bits(b) {
            moved += 1;
            if first.is_none() {
                first = Some((a, b));
            }
        }
        if bits(b) != bits(c) {
            second_moved += 1;
        }
    }
    println!("canonical quaternions: {total}");
    println!("moved by a second canon_quat: {moved}");
    println!("moved again by a third: {second_moved}");
    if let Some((a, b)) = first {
        println!("first: {:?}", a);
        println!("   -> {:?}", b);
    }
}
