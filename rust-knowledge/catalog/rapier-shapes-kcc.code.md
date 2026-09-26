# Rapier shapes, meshes & the character controller — code checks
Every check below was run by the pinned compiler (rustc 1.98.1) through `scripts/compile_oracle.py`; its verdict is on the caption. Wave 5 · 2026-09-25 · [‹ lane page](rapier-shapes-kcc.md) · [catalog index](README.md)

## Bake glTF collision meshes offline with the gltf crate and refuse what the deterministic law cannot reproduce
**The glTF 2.0 spec fixes meters, radians, +Y up, float32 POSITION with min/max, unit quaternions and in-range indices, but files can still break it; the gltf crate (1.4.1) exposes f32 transforms, Mode, positions, indices and skins. Converting belongs in a host tool that writes baked f64 triangles, not in the wasm law.**

*Check 1: a mirrored node flips a triangle's normal; an f32 unit quaternion misses 1 by 3.4e-8* · `runs` · edition 2021 · host · bin · exit code 0 · **✔ oracle pass**
```rust
fn normal(p: [[f64; 3]; 3]) -> [f64; 3] {
    let u = [p[1][0] - p[0][0], p[1][1] - p[0][1], p[1][2] - p[0][2]];
    let v = [p[2][0] - p[0][0], p[2][1] - p[0][1], p[2][2] - p[0][2]];
    [u[1] * v[2] - u[2] * v[1], u[2] * v[0] - u[0] * v[2], u[0] * v[1] - u[1] * v[0]]
}

fn main() {
    // A floor triangle wound so its normal points up (+Y).
    let tri = [[0.0, 0.0, 0.0], [0.0, 0.0, 1.0], [1.0, 0.0, 0.0]];
    println!("normal={:?}", normal(tri));
    // A node scale of (-1, 1, 1) mirrors it: same floor, normal now points down.
    let s = [-1.0, 1.0, 1.0];
    let m = tri.map(|p| [p[0] * s[0], p[1] * s[1], p[2] * s[2]]);
    println!("mirrored normal={:?} det={}", normal(m), s[0] * s[1] * s[2]);
    // Swapping two indices restores the outward winding.
    println!("mirrored, indices swapped normal={:?}", normal([m[0], m[2], m[1]]));
    // A glTF rotation is float32: 90 degrees about Y is not exactly unit.
    let q: [f32; 4] = [0.0, core::f32::consts::FRAC_1_SQRT_2, 0.0, core::f32::consts::FRAC_1_SQRT_2];
    let n2: f64 = q.iter().map(|c| (*c as f64) * (*c as f64)).sum();
    println!("f32 quaternion |q|^2 in f64 = {:e}, off by {:e}", n2, n2 - 1.0);
}
```
Expected output: `normal=[0.0, 1.0, 0.0] mirrored normal=[0.0, -1.0, 0.0] det=-1 mirrored, indices swapped normal=[0.0, 1.0, -0.0] f32 quaternion /q/^2 in f64 = 9.999999657714582e-1, off by -3.422854177870249e-8`

## Call KinematicCharacterController::move_shape with Absolute lengths and self-exclusion, then apply the result
**move_shape sweeps the shape (at most 20 casts, each stopping offset short of obstacles), tries a stair step on every wall hit and otherwise slides, snaps down only if the call started grounded, and returns EffectiveCharacterMovement { translation, grounded, is_sliding_down_slope }; it moves nothing, the caller applies translation.**

*Check 1: Relative lengths grow with the shape; without the self filter the walker cannot move* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
use rapier3d_f64::control::{CharacterLength, KinematicCharacterController};
use rapier3d_f64::prelude::*;

const DT: f64 = 1.0 / 64.0;

// Drop a box character of half-height `hy` onto a floor (top y = 0) and let it settle.
fn rest_gap(ctl: KinematicCharacterController, hy: f64, exclude_self: bool) -> (f64, f64) {
    let mut world = PhysicsWorld::new();
    world.integration_parameters.dt = DT;
    world.insert(RigidBodyBuilder::fixed().translation(Vector::new(0.0, -0.5, 0.0)), ColliderBuilder::cuboid(20.0, 0.5, 20.0));
    let shape = SharedShape::cuboid(0.25, hy, 0.25);
    let (h, _) = world.insert(RigidBodyBuilder::kinematic_position_based().translation(Vector::new(0.0, hy + 0.3, 0.0)), ColliderBuilder::new(shape.clone()));
    world.step();
    let mut vy = 0.0;
    let mut moved_x = 0.0;
    for _ in 0..64 {
        vy += -8.0 * DT;
        let pos = *world.bodies[h].position();
        let filter = if exclude_self { QueryFilter::new().exclude_rigid_body(h) } else { QueryFilter::new() };
        let mv = {
            let q = world.query_pipeline_with_filter(filter);
            ctl.move_shape(DT, &q, &*shape, &pos, Vector::new(1.0 * DT, vy * DT, 0.0), |_| {})
        };
        if mv.grounded { vy = 0.0; }
        moved_x += mv.translation.x;
        world.bodies[h].set_next_kinematic_translation(pos.translation + mv.translation);
        world.step();
    }
    let p = world.bodies[h].translation();
    (p.y - hy, moved_x)
}

fn main() {
    let rel = KinematicCharacterController::default();
    let abs = KinematicCharacterController { offset: CharacterLength::Absolute(0.01), ..KinematicCharacterController::default() };
    println!("default offset {:?} snap {:?}", rel.offset, rel.snap_to_ground);
    for hy in [0.5, 1.0] {
        let (g_rel, _) = rest_gap(rel, hy, true);
        let (g_abs, _) = rest_gap(abs, hy, true);
        println!("height {}: gap Relative(0.01)={:.4} Absolute(0.01)={:.4}", 2.0 * hy, g_rel, g_abs);
    }
    let (_, with) = rest_gap(abs, 0.5, true);
    let (_, without) = rest_gap(abs, 0.5, false);
    println!("x travelled in 64 quanta at 1 u/s: own body excluded={:.3} not excluded={:.3}", with, without);
}
```
Expected output: `default offset Relative(0.01) snap Some(Relative(0.2)) height 1: gap Relative(0.01)=0.0101 Absolute(0.01)=0.0101 height 2: gap Relative(0.01)=0.0201 Absolute(0.01)=0.0101 x travelled in 64 quanta at 1`

*Check 2: with the engine's constants a box and a capsule climb steps below 0.3, feet one offset up* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// End to end with the engine's controller constants: a box and a capsule of the same height and
// width walk into steps below the 0.3 limit; both climb, and the feet rest one offset (0.01) above.
use rapier3d_f64::control::{CharacterAutostep, CharacterLength, KinematicCharacterController};
use rapier3d_f64::prelude::*;

const DT: f64 = 1.0 / 64.0;

fn controller() -> KinematicCharacterController {
    KinematicCharacterController {
        up: Vector::new(0.0, 1.0, 0.0),
        offset: CharacterLength::Absolute(0.01),
        slide: true,
        autostep: Some(CharacterAutostep { max_height: CharacterLength::Absolute(0.3), min_width: CharacterLength::Absolute(0.2), include_dynamic_bodies: false }),
        max_slope_climb_angle: core::f64::consts::FRAC_PI_4,
        min_slope_slide_angle: 50.0 * core::f64::consts::PI / 180.0,
        snap_to_ground: Some(CharacterLength::Absolute(0.2)),
        normal_nudge_factor: 1.0e-4,
    }
}

// Floor top at y = 0; a block from x = 1.0 on with its top at `step`. Walk +x at 2 u/s for 96 quanta.
fn walk(shape: SharedShape, step: f64) -> (f64, bool) {
    let mut world = PhysicsWorld::new();
    world.integration_parameters.dt = DT;
    world.insert(RigidBodyBuilder::fixed().translation(Vector::new(0.0, -0.5, 0.0)), ColliderBuilder::cuboid(20.0, 0.5, 20.0));
    world.insert(RigidBodyBuilder::fixed().translation(Vector::new(6.0, step * 0.5, 0.0)), ColliderBuilder::cuboid(5.0, step * 0.5, 5.0));
    let (h, _) = world.insert(RigidBodyBuilder::kinematic_position_based().translation(Vector::new(0.0, 0.51, 0.0)), ColliderBuilder::new(shape.clone()));
    world.step();
    let ctl = controller();
    let (mut vy, mut grounded) = (0.0, false);
    for _ in 0..96 {
        vy += -8.0 * DT;
        let pos = *world.bodies[h].position();
        let mv = {
            let q = world.query_pipeline_with_filter(QueryFilter::new().exclude_rigid_body(h));
            ctl.move_shape(DT, &q, &*shape, &pos, Vector::new(2.0 * DT, vy * DT, 0.0), |_| {})
        };
        if mv.grounded { vy = 0.0; }
        grounded = mv.grounded;
        world.bodies[h].set_next_kinematic_translation(pos.translation + mv.translation);
        world.step();
    }
    (world.bodies[h].translation().y - 0.5, grounded)
}

fn main() {
    for step in [0.1, 0.2, 0.25] {
        let (b, bg) = walk(SharedShape::cuboid(0.25, 0.5, 0.25), step);
        let (c, cg) = walk(SharedShape::capsule_y(0.25, 0.25), step);
        println!("step {step}: box feet={:.3} grounded={bg} | capsule feet={:.3} grounded={cg}", b, c);
    }
}
```
Expected output: `step 0.1: box feet=0.110 grounded=true / capsule feet=0.110 grounded=true step 0.2: box feet=0.210 grounded=true / capsule feet=0.210 grounded=true step 0.25: box feet=0.260 grounded=true / capsule fe`

*Check 3: is_sliding_down_slope is true on flat ground under gravity; autostep fires in the air* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// What the outputs mean at 0.35.3: is_sliding_down_slope is set on flat ground when the motion
// has a downward part, and autostep fires for a character with nothing under it.
use rapier3d_f64::control::{CharacterAutostep, CharacterLength, EffectiveCharacterMovement, KinematicCharacterController};
use rapier3d_f64::prelude::*;

const DT: f64 = 1.0 / 64.0;

fn controller() -> KinematicCharacterController {
    KinematicCharacterController {
        up: Vector::new(0.0, 1.0, 0.0),
        offset: CharacterLength::Absolute(0.01),
        slide: true,
        autostep: Some(CharacterAutostep { max_height: CharacterLength::Absolute(0.3), min_width: CharacterLength::Absolute(0.2), include_dynamic_bodies: false }),
        max_slope_climb_angle: core::f64::consts::FRAC_PI_4,
        min_slope_slide_angle: 50.0 * core::f64::consts::PI / 180.0,
        snap_to_ground: Some(CharacterLength::Absolute(0.2)),
        normal_nudge_factor: 1.0e-4,
    }
}

// One move_shape call for a box character at `at` in a world of fixed cuboids (centre, half extents).
fn one_move(blocks: &[(Vector, Vector)], at: Vector, desired: Vector) -> EffectiveCharacterMovement {
    let mut world = PhysicsWorld::new();
    world.integration_parameters.dt = DT;
    for (c, h) in blocks { world.insert(RigidBodyBuilder::fixed().translation(*c), ColliderBuilder::cuboid(h.x, h.y, h.z)); }
    let shape = SharedShape::cuboid(0.25, 0.5, 0.25);
    let (h, _) = world.insert(RigidBodyBuilder::kinematic_position_based().translation(at), ColliderBuilder::new(shape.clone()));
    world.step();
    let pos = *world.bodies[h].position();
    let q = world.query_pipeline_with_filter(QueryFilter::new().exclude_rigid_body(h));
    controller().move_shape(DT, &q, &*shape, &pos, desired, |_| {})
}

fn main() {
    let floor = [(Vector::new(0.0, -0.5, 0.0), Vector::new(20.0, 0.5, 20.0))];
    let stand = Vector::new(0.0, 0.51, 0.0);
    let m = one_move(&floor, stand, Vector::new(DT, -8.0 * DT * DT, 0.0));
    println!("flat floor, level walk plus gravity: grounded={} is_sliding_down_slope={}", m.grounded, m.is_sliding_down_slope);
    let m = one_move(&floor, stand, Vector::new(DT, 0.0, 0.0));
    println!("flat floor, level walk only:         grounded={} is_sliding_down_slope={}", m.grounded, m.is_sliding_down_slope);
    // Feet at y = 0.0, the floor 1.0 below, a block with its top at y = 0.2 from x = 0.5 on.
    let pit = [(Vector::new(0.0, -1.5, 0.0), Vector::new(20.0, 0.5, 20.0)), (Vector::new(3.0, -0.4, 0.0), Vector::new(2.5, 0.6, 2.0))];
    let m = one_move(&pit, Vector::new(0.0, 0.5, 0.0), Vector::new(0.5, 0.0, 0.0));
    println!("airborne, moving level into a 0.2 rise: dx={:.4} dy={:.4} grounded={}", m.translation.x, m.translation.y, m.grounded);
}
```
Expected output: `flat floor, level walk plus gravity: grounded=true is_sliding_down_slope=true flat floor, level walk only:         grounded=true is_sliding_down_slope=false airborne, moving level into a 0.2 rise: dx=`

## Canonicalise -0.0 and weld vertices offline: MERGE_DUPLICATE_VERTICES keys raw bits and renumbers the mesh
**MERGE_DUPLICATE_VERTICES (and FIX_INTERNAL_EDGES, whose bits 144 include it) keys vertices by raw bytes but compares with ==, so (-0.0, 0, 0) welds to (0, 0, 0) in a 4- or 16-vertex mesh and not in a 64-vertex one; merging also renumbers and drops unreferenced vertices, and DELETE_DEGENERATE_TRIANGLES only removes repeated-index triangles.**

*Check 1: a -0.0 duplicate welds in 4 and 16 vertex meshes but not in 64 or 1024; canon() fixes it* · `runs` · edition 2021 · host · bin · deps: parry3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// MERGE_DUPLICATE_VERTICES keys on raw bytes but compares with ==, so whether (-0.0, 0, 0)
// welds to (0, 0, 0) depends on the hash-table layout, i.e. on the mesh size.
use parry3d_f64::math::Vector;
use parry3d_f64::shape::{TriMesh, TriMeshFlags};

// The engine's canon(): -0.0 becomes 0.0, every other value is unchanged.
fn canon(x: f64) -> f64 { if x == 0.0 { 0.0 } else { x } }

// An n x n grid of distinct vertices plus one extra triangle whose first vertex is `zero`,
// value-equal to grid vertex 0 = (0, 0, 0). Returns the vertex count after merging.
fn welded(n: u32, zero: f64, canonicalise: bool) -> usize {
    let mut v = Vec::new();
    for i in 0..n { for j in 0..n { v.push(Vector::new(j as f64, 0.0, i as f64)); } }
    let mut idx = Vec::new();
    for i in 0..n - 1 { for j in 0..n - 1 {
        let a = i * n + j;
        idx.push([a, a + n, a + 1]);
        idx.push([a + 1, a + n, a + n + 1]);
    } }
    let extra = v.len() as u32;
    v.push(Vector::new(zero, 0.0, 0.0));
    idx.push([extra, n, 1]);
    if canonicalise { for p in v.iter_mut() { *p = Vector::new(canon(p.x), canon(p.y), canon(p.z)); } }
    TriMesh::with_flags(v, idx, TriMeshFlags::MERGE_DUPLICATE_VERTICES).unwrap().vertices().len()
}

fn main() {
    for n in [2u32, 4, 8, 32] {
        println!("{} grid vertices: +0.0 -> {}, -0.0 -> {}, -0.0 canonicalised -> {}", n * n, welded(n, 0.0, false), welded(n, -0.0, false), welded(n, -0.0, true));
    }
}
```
Expected output: `4 grid vertices: +0.0 -> 4, -0.0 -> 4, -0.0 canonicalised -> 4 16 grid vertices: +0.0 -> 16, -0.0 -> 16, -0.0 canonicalised -> 16 64 grid vertices: +0.0 -> 64, -0.0 -> 65, -0.0 canonicalised -> 64 102`

*Check 2: FIX_INTERNAL_EDGES implies a merge that renumbers; pre-welded buffers pass unchanged* · `runs` · edition 2021 · host · bin · deps: parry3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// What the preprocessing flags do to the buffers.
use parry3d_f64::math::Vector;
use parry3d_f64::shape::{TriMesh, TriMeshFlags};

fn v(x: f64, y: f64, z: f64) -> Vector { Vector::new(x, y, z) }

fn main() {
    let f = TriMeshFlags::FIX_INTERNAL_EDGES;
    println!("FIX_INTERNAL_EDGES bits={} includes MERGE_DUPLICATE_VERTICES={}", f.bits(), f.contains(TriMeshFlags::MERGE_DUPLICATE_VERTICES));
    // Vertex 0 is unreferenced; vertices 4 and 5 duplicate 2 and 3.
    let raw = vec![v(9., 9., 9.), v(0., 0., 0.), v(1., 0., 0.), v(0., 0., 1.), v(1., 0., 0.), v(0., 0., 1.), v(1., 0., 1.)];
    let m = TriMesh::with_flags(raw, vec![[1, 3, 2], [4, 5, 6]], f).unwrap();
    let p = m.vertices()[0];
    println!("raw buffers: 7 vertices in, {} out, first=({}, {}, {}), indices={:?}", m.vertices().len(), p.x, p.y, p.z, m.indices());
    // Buffers already welded, all referenced, in first-reference order: the merge changes nothing.
    let welded = vec![v(0., 0., 0.), v(0., 0., 1.), v(1., 0., 0.), v(1., 0., 1.)];
    let idx = vec![[0, 1, 2], [2, 1, 3]];
    let m = TriMesh::with_flags(welded.clone(), idx.clone(), f).unwrap();
    let same = m.vertices().iter().zip(&welded).all(|(a, b)| a.x.to_bits() == b.x.to_bits() && a.y.to_bits() == b.y.to_bits() && a.z.to_bits() == b.z.to_bits());
    println!("pre-welded buffers: vertices unchanged={} indices unchanged={}", same && m.vertices().len() == welded.len(), m.indices() == &idx[..]);
    let col = vec![v(0., 0., 0.), v(1., 0., 0.), v(2., 0., 0.)];
    let kept = TriMesh::with_flags(col.clone(), vec![[0, 1, 2]], TriMeshFlags::DELETE_DEGENERATE_TRIANGLES).unwrap();
    let emptied = TriMesh::with_flags(col, vec![[0, 0, 1]], TriMeshFlags::DELETE_DEGENERATE_TRIANGLES).unwrap();
    println!("DELETE_DEGENERATE_TRIANGLES: zero-area triangle kept={}, repeated-index mesh left {} triangles", kept.indices().len(), emptied.indices().len());
}
```
Expected output: `FIX_INTERNAL_EDGES bits=144 includes MERGE_DUPLICATE_VERTICES=true raw buffers: 7 vertices in, 4 out, first=(0, 0, 0), indices=[[0, 1, 2], [2, 1, 3]] pre-welded buffers: vertices unchanged=true indice`

## Compute convex hulls and VHACD parts offline with pinned parameters, then load stored buffers with convex_mesh
**SharedShape::convex_hull is None for fewer than 3 points, NaN, coincident or collinear points, but Some for coplanar points: a flat polyhedron of mass 0. VHACD output follows its parameters: a two-box mesh of volume 2 became 2 parts (mass 2.0000) at resolution 64 and 13 parts (summed mass 3.1227) at resolution 16.**

*Check 1: convex_hull: None for collinear, coincident, 2 points, NaN; Some(mass 0) for coplanar* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// convex_hull on degenerate input at parry3d-f64 0.30.2 (through rapier3d-f64 0.35.3's re-export):
// None in most cases, but Some(mass 0) for coplanar points, and Rapier's wrappers pass it on.
use rapier3d_f64::geometry::MeshConverter;
use rapier3d_f64::parry::transformation::try_convex_hull;
use rapier3d_f64::prelude::*;

fn v(x: f64, y: f64, z: f64) -> Vector { Vector::new(x, y, z) }

fn main() {
    let cases: [(&str, Vec<Vector>); 6] = [
        ("tetra", vec![v(0., 0., 0.), v(1., 0., 0.), v(0., 1., 0.), v(0., 0., 1.)]),
        ("coplanar", vec![v(0., 0., 0.), v(1., 0., 0.), v(0., 0., 1.), v(1., 0., 1.)]),
        ("collinear", vec![v(0., 0., 0.), v(1., 0., 0.), v(2., 0., 0.)]),
        ("coincident", vec![v(1., 1., 1.), v(1., 1., 1.), v(1., 1., 1.)]),
        ("two points", vec![v(0., 0., 0.), v(1., 0., 0.)]),
        ("nan", vec![v(0., 0., 0.), v(1., 0., 0.), v(0., 1., 0.), v(0., 0., f64::NAN)]),
    ];
    for (name, pts) in &cases {
        let raw = match try_convex_hull(pts) { Ok((vs, is)) => format!("Ok({} verts, {} tris)", vs.len(), is.len()), Err(e) => format!("Err({:?})", e) };
        let shape = match SharedShape::convex_hull(pts) { Some(s) => format!("Some(mass {})", s.mass_properties(1.0).mass()), None => "None".to_string() };
        println!("{name}: try_convex_hull={raw} convex_hull={shape}");
    }
    let flat = cases[1].1.clone();
    let builder = ColliderBuilder::convex_hull(&flat).map(|b| b.build().mass());
    let converted = MeshConverter::ConvexHull.convert(flat, vec![]).map(|(s, _)| s.mass_properties(1.0).mass());
    println!("coplanar through ColliderBuilder::convex_hull: {:?}; through MeshConverter::ConvexHull: {:?}", builder, converted.ok());
}
```
Expected output: `tetra: try_convex_hull=Ok(4 verts, 4 tris) convex_hull=Some(mass 0.16666666666666666) coplanar: try_convex_hull=Ok(4 verts, 4 tris) convex_hull=Some(mass 0) collinear: try_convex_hull=Ok(2 verts, 2 tr`

*Check 2: a stored hull reloaded with convex_mesh has the same mass bits; VHACD defaults* · `runs` · edition 2021 · host · bin · deps: parry3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// Offline: keep the hull's vertex and index buffers. At load: convex_mesh, no hull computation.
use parry3d_f64::math::Vector;
use parry3d_f64::shape::SharedShape;
use parry3d_f64::transformation::try_convex_hull;
use parry3d_f64::transformation::vhacd::VHACDParameters;

fn main() {
    let mut pts = Vec::new();
    for i in 0..3 { for j in 0..3 { for k in 0..3 {
        pts.push(Vector::new(i as f64 * 0.5, j as f64 * 0.5, k as f64 * 0.5));
    } } }
    let (verts, idx) = try_convex_hull(&pts).unwrap();
    let loaded = SharedShape::convex_mesh(verts.clone(), &idx).unwrap();
    let direct = SharedShape::convex_hull(&pts).unwrap();
    let (ml, md) = (loaded.mass_properties(1.0).mass(), direct.mass_properties(1.0).mass());
    println!("{} points -> hull of {} vertices, {} triangles; convex_mesh mass bits == convex_hull mass bits: {}", pts.len(), verts.len(), idx.len(), ml.to_bits() == md.to_bits());
    let p = VHACDParameters::default();
    println!("VHACDParameters::default(): resolution={} concavity={} alpha={} beta={} plane_downsampling={} convex_hull_downsampling={} convex_hull_approximation={} max_convex_hulls={}",
        p.resolution, p.concavity, p.alpha, p.beta, p.plane_downsampling, p.convex_hull_downsampling, p.convex_hull_approximation, p.max_convex_hulls);
}
```
Expected output: `27 points -> hull of 8 vertices, 12 triangles; convex_mesh mass bits == convex_hull mass bits: true VHACDParameters::default(): resolution=64 concavity=0.01 alpha=0.05 beta=0.05 plane_downsampling=4 c`

*Check 3: VHACD resolution 64 vs 16 on one mesh: 2 parts vs 13 parts* · `runs` · edition 2021 · host · bin · deps: parry3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// The same mesh, two VHACD resolutions: the decomposition is a function of its parameters.
use parry3d_f64::math::Vector;
use parry3d_f64::shape::SharedShape;
use parry3d_f64::transformation::vhacd::VHACDParameters;

// An axis-aligned box as 8 vertices and 12 outward-wound triangles.
fn cuboid_mesh(min: [f64; 3], max: [f64; 3], v: &mut Vec<Vector>, idx: &mut Vec<[u32; 3]>) {
    let b = v.len() as u32;
    for i in 0..8u32 {
        v.push(Vector::new(if i & 1 == 0 { min[0] } else { max[0] }, if i & 2 == 0 { min[1] } else { max[1] }, if i & 4 == 0 { min[2] } else { max[2] }));
    }
    for t in [[0, 2, 1], [1, 2, 3], [4, 5, 6], [5, 7, 6], [0, 1, 4], [1, 5, 4], [2, 6, 3], [3, 6, 7], [0, 4, 2], [2, 4, 6], [1, 3, 5], [3, 7, 5]] {
        idx.push([b + t[0], b + t[1], b + t[2]]);
    }
}

fn main() {
    // Two unit boxes with a gap between them: true volume 2.
    let (mut v, mut idx) = (Vec::new(), Vec::new());
    cuboid_mesh([0.0, 0.0, 0.0], [1.0, 1.0, 1.0], &mut v, &mut idx);
    cuboid_mesh([2.0, 0.0, 0.0], [3.0, 1.0, 1.0], &mut v, &mut idx);
    for resolution in [64u32, 16] {
        let d = SharedShape::convex_decomposition_with_params(&v, &idx, &VHACDParameters { resolution, ..Default::default() });
        println!("resolution {resolution}: {} convex parts, summed mass {:.4}", d.as_compound().unwrap().shapes().len(), d.mass_properties(1.0).mass());
    }
}
```
Expected output: `resolution 64: 2 convex parts, summed mass 2.0000 resolution 16: 13 convex parts, summed mass 3.1227`

## Fill a parry HeightField column-major with scale as the whole extent, and sample it as two triangles per cell
**In HeightField::new(Array2::new(nrows, ncols, data), scale) row i advances z and column j advances x, data is column-major (i + j * nrows), scale is the whole field (cell width = scale.x / (ncols - 1)), the field is centred on its collider, and each cell is two triangles split along (x0, z1)-(x1, z0), not a bilinear patch.**

*Check 1: column-major data, whole-extent scale, centred field; a (1,1,1) scale gives 0.25-wide cells* · `runs` · edition 2021 · host · bin · deps: parry3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// HeightField layout at parry3d-f64 0.30.2: rows advance z, columns advance x, data is
// column-major (data[row + col * rows]), scale is the whole field, centred on the collider.
use parry3d_f64::math::{Pose, Vector};
use parry3d_f64::query::{Ray, RayCast};
use parry3d_f64::shape::HeightField;
use parry3d_f64::utils::Array2;

fn height(hf: &HeightField, x: f64, z: f64) -> Option<f64> {
    let ray = Ray::new(Vector::new(x, 5.0, z), Vector::new(0.0, -1.0, 0.0));
    hf.cast_ray(&Pose::IDENTITY, &ray, 100.0, true).map(|t| 5.0 - t)
}

fn main() {
    let (rows, cols) = (3usize, 5usize);
    let scale = Vector::new(4.0, 1.0, 2.0);
    // One bump of 1.0 at row 1, col 3, written column-major.
    let mut data = vec![0.0; rows * cols];
    data[1 + 3 * rows] = 1.0;
    let hf = HeightField::new(Array2::new(rows, cols, data), scale);
    let a = hf.root_aabb();
    println!("cell_width={} cell_height={} x=[{}, {}] z=[{}, {}]", hf.cell_width(), hf.cell_height(), a.mins.x, a.maxs.x, a.mins.z, a.maxs.z);
    println!("column-major: h(1,0)={:?} h(-1,0)={:?} h(2.5,0)={:?}", height(&hf, 1.0, 0.0), height(&hf, -1.0, 0.0), height(&hf, 2.5, 0.0));
    // The same bump written row-major (data[row * cols + col]) is not where it was meant to be.
    let mut rm = vec![0.0; rows * cols];
    rm[1 * cols + 3] = 1.0;
    println!("row-major buffer: h(1,0)={:?}", height(&HeightField::new(Array2::new(rows, cols, rm), scale), 1.0, 0.0));
    // Array2::from_fn takes (row, col) and lays the data out itself.
    let ff = HeightField::new(Array2::from_fn(rows, cols, |r, c| if (r, c) == (1, 3) { 1.0 } else { 0.0 }), scale);
    println!("Array2::from_fn: h(1,0)={:?}", height(&ff, 1.0, 0.0));
    // A scale read as "the size of one cell" gives cells four times too small here.
    let unit = HeightField::new(Array2::new(rows, cols, vec![0.0; rows * cols]), Vector::new(1.0, 1.0, 1.0));
    println!("scale (1, 1, 1) with 5 columns: cell_width={}", unit.cell_width());
}
```
Expected output: `cell_width=1 cell_height=1 x=[-2, 2] z=[-1, 1] column-major: h(1,0)=Some(1.0) h(-1,0)=Some(0.0) h(2.5,0)=None row-major buffer: h(1,0)=Some(0.0) Array2::from_fn: h(1,0)=Some(1.0) scale (1, 1, 1) with `

*Check 2: two triangles per cell: 0 at a cell centre where bilinear says 0.25; the rule in 'how' matches* · `runs` · edition 2021 · host · bin · deps: parry3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// A heightfield cell is two triangles split along (x0, z1)-(x1, z0), not a bilinear patch.
use parry3d_f64::math::{Pose, Vector};
use parry3d_f64::query::{Ray, RayCast};
use parry3d_f64::shape::HeightField;
use parry3d_f64::utils::Array2;

fn surface(hf: &HeightField, x: f64, z: f64) -> f64 {
    let ray = Ray::new(Vector::new(x, 5.0, z), Vector::new(0.0, -1.0, 0.0));
    5.0 - hf.cast_ray(&Pose::IDENTITY, &ray, 100.0, true).unwrap()
}

// h[row][col]: row advances z, col advances x. One 1 x 1 cell centred on the origin.
fn bilinear(h: [[f64; 2]; 2], x: f64, z: f64) -> f64 {
    let (u, v) = (x + 0.5, z + 0.5);
    h[0][0] * (1.0 - u) * (1.0 - v) + h[0][1] * u * (1.0 - v) + h[1][0] * (1.0 - u) * v + h[1][1] * u * v
}

// The two-triangle rule: h10 is the +z neighbour (row 1, col 0), h01 the +x neighbour (row 0, col 1).
fn triangles(h: [[f64; 2]; 2], x: f64, z: f64) -> f64 {
    let (u, v) = (x + 0.5, z + 0.5);
    let (h00, h01, h10, h11) = (h[0][0], h[0][1], h[1][0], h[1][1]);
    if u + v <= 1.0 { h00 + u * (h01 - h00) + v * (h10 - h00) } else { h11 + (1.0 - u) * (h10 - h11) + (1.0 - v) * (h01 - h11) }
}

fn main() {
    // One raised corner: row 1 (z = +0.5), col 1 (x = +0.5).
    let h = [[0.0, 0.0], [0.0, 1.0]];
    let hf = HeightField::new(Array2::from_fn(2, 2, |r, c| h[r][c]), Vector::new(1.0, 1.0, 1.0));
    for (x, z) in [(0.0, 0.0), (0.25, 0.25), (-0.25, -0.25)] {
        println!("({x}, {z}): solver surface={} bilinear={}", surface(&hf, x, z), bilinear(h, x, z));
    }
    // The rule matches the solver on another non-planar cell; bilinear does not.
    let g = [[0.2, -0.7], [1.3, 0.9]]; // h00 + h11 != h01 + h10: not planar
    let gf = HeightField::new(Array2::from_fn(2, 2, |r, c| g[r][c]), Vector::new(1.0, 1.0, 1.0));
    let pts = [(0.3, -0.1), (-0.4, 0.45), (0.1, 0.2), (-0.2, -0.3), (0.45, 0.35)];
    let worst = pts.iter().map(|&(x, z)| (surface(&gf, x, z) - triangles(g, x, z)).abs()).fold(0.0, f64::max);
    let worst_bilinear = pts.iter().map(|&(x, z)| (surface(&gf, x, z) - bilinear(g, x, z)).abs()).fold(0.0, f64::max);
    println!("5 points: two-triangle rule within 1e-12 of the solver={} bilinear max error={:.4}", worst < 1e-12, worst_bilinear);
}
```
Expected output: `(0, 0): solver surface=0 bilinear=0.25 (0.25, 0.25): solver surface=0.5 bilinear=0.5625 (-0.25, -0.25): solver surface=0 bilinear=0.0625 5 points: two-triangle rule within 1e-12 of the solver=true bil`

*Check 3: a heightfield with one row of heights panics in HeightField::new (exit 101)* · `runs` · edition 2021 · host · bin · deps: parry3d_f64 · exit code 101 · **✔ oracle pass**
```rust
// HeightField::new asserts at least 2 rows and 2 columns: one row is a panic, not an error.
use parry3d_f64::math::Vector;
use parry3d_f64::shape::HeightField;
use parry3d_f64::utils::Array2;

fn main() {
    println!("building");
    let hf = HeightField::new(Array2::new(1, 3, vec![0.0; 3]), Vector::new(2.0, 1.0, 1.0));
    println!("built {} cells", hf.nrows() * hf.ncols());
}
```
Expected output: `building`

## Push dynamic bodies with solve_character_collision_impulses and plan all walkers against the last step's poses
**move_shape stops a walker one offset short of a dynamic body and never moves it; solve_character_collision_impulses applies approximate impulses to dynamic bodies only. Walkers meet each other as kinematic obstacles at the last step's poses and inherit a touching kinematic body's velocity, so two walkers planned together stayed apart at 1 and 2 u/s but overlapped at 8 u/s.**

*Check 1: without impulses the crate stays at 0.600; with them it is pushed to 2.188* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
use rapier3d_f64::control::{CharacterAutostep, CharacterLength, KinematicCharacterController};
use rapier3d_f64::prelude::*;

const DT: f64 = 1.0 / 64.0;

fn controller() -> KinematicCharacterController {
    KinematicCharacterController {
        up: Vector::new(0.0, 1.0, 0.0),
        offset: CharacterLength::Absolute(0.01),
        slide: true,
        autostep: Some(CharacterAutostep { max_height: CharacterLength::Absolute(0.3), min_width: CharacterLength::Absolute(0.2), include_dynamic_bodies: false }),
        max_slope_climb_angle: core::f64::consts::FRAC_PI_4,
        min_slope_slide_angle: 50.0 * core::f64::consts::PI / 180.0,
        snap_to_ground: Some(CharacterLength::Absolute(0.2)),
        normal_nudge_factor: 1.0e-4,
    }
}

// A box character walks +x at 1 u/s into a dynamic crate (half 0.25, density 1) resting on the floor.
fn push(impulses: bool) -> (f64, f64, usize) {
    let mut world = PhysicsWorld::new();
    world.gravity = Vector::new(0.0, -8.0, 0.0);
    world.integration_parameters.dt = DT;
    world.insert(RigidBodyBuilder::fixed().translation(Vector::new(0.0, -0.5, 0.0)), ColliderBuilder::cuboid(20.0, 0.5, 20.0).friction(0.8));
    let (crate_h, _) = world.insert(RigidBodyBuilder::dynamic().translation(Vector::new(0.6, 0.25, 0.0)), ColliderBuilder::cuboid(0.25, 0.25, 0.25).friction(0.8));
    let shape = SharedShape::cuboid(0.25, 0.5, 0.25);
    let (h, _) = world.insert(RigidBodyBuilder::kinematic_position_based().translation(Vector::new(0.0, 0.51, 0.0)).additional_mass(1.0), ColliderBuilder::new(shape.clone()));
    world.step();
    let ctl = controller();
    let mut hits = 0usize;
    for _ in 0..128 {
        let pos = *world.bodies[h].position();
        let mut collisions = Vec::new();
        let mv = {
            let q = world.query_pipeline_with_filter(QueryFilter::new().exclude_rigid_body(h));
            ctl.move_shape(DT, &q, &*shape, &pos, Vector::new(1.0 * DT, -8.0 * DT * DT, 0.0), |c| collisions.push(c))
        };
        hits += collisions.len();
        world.bodies[h].set_next_kinematic_translation(pos.translation + mv.translation);
        if impulses {
            let PhysicsWorld { broad_phase, narrow_phase, bodies, colliders, .. } = &mut world;
            let mut q = broad_phase.as_query_pipeline_mut(narrow_phase.query_dispatcher(), bodies, colliders, QueryFilter::new().exclude_rigid_body(h));
            ctl.solve_character_collision_impulses(DT, &mut q, &*shape, 1.0, &collisions);
        }
        world.step();
    }
    (world.bodies[h].translation().x, world.bodies[crate_h].translation().x, hits)
}

fn main() {
    let (cx, bx, n) = push(false);
    println!("no impulses:   character x={:.3} crate x={:.3} collisions={}", cx, bx, n);
    let (cx, bx, n) = push(true);
    println!("with impulses: character x={:.3} crate x={:.3} collisions={}", cx, bx, n);
}
```
Expected output: `no impulses:   character x=0.090 crate x=0.600 collisions=250 with impulses: character x=1.657 crate x=2.188 collisions=169`

*Check 2: two walkers planned together: apart at 1 and 2 u/s, overlapping at 8 u/s, order-independent* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// Two box walkers (half 0.25) driven at each other from x = -1 and x = +1, both planned against the
// last step's poses and then applied together, as rapier_law.rs integrate() does.
use rapier3d_f64::control::{CharacterAutostep, CharacterLength, KinematicCharacterController};
use rapier3d_f64::prelude::*;

const DT: f64 = 1.0 / 64.0;

fn controller() -> KinematicCharacterController {
    KinematicCharacterController {
        up: Vector::new(0.0, 1.0, 0.0),
        offset: CharacterLength::Absolute(0.01),
        slide: true,
        autostep: Some(CharacterAutostep { max_height: CharacterLength::Absolute(0.3), min_width: CharacterLength::Absolute(0.2), include_dynamic_bodies: false }),
        max_slope_climb_angle: core::f64::consts::FRAC_PI_4,
        min_slope_slide_angle: 50.0 * core::f64::consts::PI / 180.0,
        snap_to_ground: Some(CharacterLength::Absolute(0.2)),
        normal_nudge_factor: 1.0e-4,
    }
}

// Returns (final x of A, final x of B, smallest gap between their faces over the run).
fn run(speed: f64, reverse: bool) -> (f64, f64, f64) {
    let mut world = PhysicsWorld::new();
    world.integration_parameters.dt = DT;
    world.insert(RigidBodyBuilder::fixed().translation(Vector::new(0.0, -0.5, 0.0)), ColliderBuilder::cuboid(20.0, 0.5, 20.0));
    let shape = SharedShape::cuboid(0.25, 0.5, 0.25);
    let hs: Vec<RigidBodyHandle> = [-1.0, 1.0].iter().map(|x| world.insert(RigidBodyBuilder::kinematic_position_based().translation(Vector::new(*x, 0.51, 0.0)), ColliderBuilder::new(shape.clone())).0).collect();
    let vel = [speed, -speed];
    world.step();
    let ctl = controller();
    let mut min_gap = f64::MAX;
    for _ in 0..64 {
        let order: [usize; 2] = if reverse { [1, 0] } else { [0, 1] };
        let mut plans = [Vector::ZERO; 2];
        for i in order {
            let pos = *world.bodies[hs[i]].position();
            let q = world.query_pipeline_with_filter(QueryFilter::new().exclude_rigid_body(hs[i]));
            let mv = ctl.move_shape(DT, &q, &*shape, &pos, Vector::new(vel[i] * DT, -8.0 * DT * DT, 0.0), |_| {});
            plans[i] = pos.translation + mv.translation;
        }
        for i in 0..2 { world.bodies[hs[i]].set_next_kinematic_translation(plans[i]); }
        world.step();
        min_gap = min_gap.min(world.bodies[hs[1]].translation().x - world.bodies[hs[0]].translation().x - 0.5);
    }
    (world.bodies[hs[0]].translation().x, world.bodies[hs[1]].translation().x, min_gap)
}

fn main() {
    for speed in [1.0, 2.0, 8.0] {
        let (a, b, g) = run(speed, false);
        let (ra, rb, _) = run(speed, true);
        println!("{speed} u/s each: A.x={:.4} B.x={:.4} final gap={:.4} min gap={:.4} reversed planning order bit-identical={}", a, b, b - a - 0.5, g, a.to_bits() == ra.to_bits() && b.to_bits() == rb.to_bits());
    }
}
```
Expected output: `1 u/s each: A.x=-0.2741 B.x=0.2905 final gap=0.0646 min gap=0.0341 reversed planning order bit-identical=true 2 u/s each: A.x=-0.2870 B.x=0.2373 final gap=0.0243 min gap=0.0137 reversed planning order`

*Check 3: a kinematic body walking into a standing walker pushes it* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
use rapier3d_f64::control::{CharacterAutostep, CharacterLength, KinematicCharacterController};
use rapier3d_f64::prelude::*;

const DT: f64 = 1.0 / 64.0;

fn controller() -> KinematicCharacterController {
    KinematicCharacterController {
        up: Vector::new(0.0, 1.0, 0.0),
        offset: CharacterLength::Absolute(0.01),
        slide: true,
        autostep: Some(CharacterAutostep { max_height: CharacterLength::Absolute(0.3), min_width: CharacterLength::Absolute(0.2), include_dynamic_bodies: false }),
        max_slope_climb_angle: core::f64::consts::FRAC_PI_4,
        min_slope_slide_angle: 50.0 * core::f64::consts::PI / 180.0,
        snap_to_ground: Some(CharacterLength::Absolute(0.2)),
        normal_nudge_factor: 1.0e-4,
    }
}

// A kinematic wall B moves -x at 1 u/s into character A standing at x = 0. `desired` is A's own intent.
fn pushed(desired: Vector) -> (f64, f64) {
    let mut world = PhysicsWorld::new();
    world.integration_parameters.dt = DT;
    world.insert(RigidBodyBuilder::fixed().translation(Vector::new(0.0, -0.5, 0.0)), ColliderBuilder::cuboid(20.0, 0.5, 20.0));
    let shape = SharedShape::cuboid(0.25, 0.5, 0.25);
    let (a, _) = world.insert(RigidBodyBuilder::kinematic_position_based().translation(Vector::new(0.0, 0.51, 0.0)), ColliderBuilder::new(shape.clone()));
    let (b, _) = world.insert(RigidBodyBuilder::kinematic_position_based().translation(Vector::new(0.6, 0.51, 0.0)), ColliderBuilder::cuboid(0.1, 0.5, 1.0));
    world.step();
    let ctl = controller();
    for _ in 0..64 {
        let pos = *world.bodies[a].position();
        let mv = {
            let q = world.query_pipeline_with_filter(QueryFilter::new().exclude_rigid_body(a));
            ctl.move_shape(DT, &q, &*shape, &pos, desired, |_| {})
        };
        world.bodies[a].set_next_kinematic_translation(pos.translation + mv.translation);
        let bp = world.bodies[b].translation();
        world.bodies[b].set_next_kinematic_translation(bp + Vector::new(-1.0 * DT, 0.0, 0.0));
        world.step();
    }
    (world.bodies[a].translation().x, world.bodies[b].translation().x)
}

fn main() {
    let (ax, bx) = pushed(Vector::new(0.0, -8.0 * DT * DT, 0.0));
    println!("A with a gravity-only intent: A.x={:.3} wall.x={:.3} overlap={}", ax, bx, (bx - 0.1) < (ax + 0.25));
    let (ax, bx) = pushed(Vector::ZERO);
    println!("A with a zero intent:         A.x={:.3} wall.x={:.3} overlap={}", ax, bx, (bx - 0.1) < (ax + 0.25));
}
```
Expected output: `A with a gravity-only intent: A.x=-0.797 wall.x=-0.400 overlap=false A with a zero intent:         A.x=-0.744 wall.x=-0.400 overlap=true`

## Test line of sight with an eye-to-target ray at max_toi 1.0 on fixed colliders once the broad phase holds them
**QueryPipeline::cast_ray(&Ray, max_toi, solid) returns the first (ColliderHandle, toi) with hit point origin + dir * toi, so dir = target - eye with max_toi 1.0 is exactly the eye-to-target segment. Queries see only colliders already in the broad phase, intersect_ray yields hits in tree order, and solid = true answers toi 0 from inside a shape.**

*Check 1: eye-to-target ray: toi 0.225 vs 0.9 unit; None before a step; self-hit at 0; tree order* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
use rapier3d_f64::prelude::*;

fn main() {
    let mut world = PhysicsWorld::new();
    // Three static walls across the x axis, inserted far-to-near.
    for x in [3.0, 2.0, 1.0] {
        world.insert(RigidBodyBuilder::fixed().translation(Vector::new(x, 1.0, 0.0)), ColliderBuilder::cuboid(0.1, 1.0, 1.0));
    }
    // The looker and the target are dynamic bodies with their own colliders.
    let (eye_b, _) = world.insert(RigidBodyBuilder::dynamic().translation(Vector::new(0.0, 1.0, 0.0)), ColliderBuilder::ball(0.3));
    let (tgt_b, _) = world.insert(RigidBodyBuilder::dynamic().translation(Vector::new(4.0, 1.0, 0.0)), ColliderBuilder::ball(0.3));
    let eye = Vector::new(0.0, 1.0, 0.0);
    let target = Vector::new(4.0, 1.0, 0.0);
    let seg = Ray::new(eye, target - eye);
    let before = world.cast_ray(&seg, 1.0, true, QueryFilter::only_fixed());
    println!("before any step: {:?}", before.map(|h| h.1));
    world.step();
    let hit = world.cast_ray(&seg, 1.0, true, QueryFilter::only_fixed());
    println!("eye->target ray, max_toi 1: toi={:?}", hit.map(|h| h.1));
    let unit = Ray::new(eye, (target - eye).normalize());
    println!("unit-direction ray: toi={:?}", world.cast_ray(&unit, 4.0, true, QueryFilter::only_fixed()).map(|h| h.1));
    let everything = world.cast_ray(&seg, 1.0, true, QueryFilter::new());
    let own = world.cast_ray(&seg, 1.0, true, QueryFilter::new().exclude_rigid_body(eye_b));
    println!("no filter: toi={:?}  excluding the looker: toi={:?}", everything.map(|h| h.1), own.map(|h| h.1));
    let _ = tgt_b;
    // solid flag: a ray starting inside the first wall.
    let inside = Ray::new(Vector::new(1.0, 1.0, 0.0), Vector::new(1.0, 0.0, 0.0));
    let s = world.cast_ray(&inside, 10.0, true, QueryFilter::only_fixed()).map(|h| h.1);
    let h = world.cast_ray(&inside, 10.0, false, QueryFilter::only_fixed()).map(|h| h.1);
    println!("start inside a wall: solid=true toi={:?} solid=false toi={:?}", s, h);
    let order: Vec<f64> = world.intersect_ray(seg, 1.0, true, QueryFilter::only_fixed()).map(|(_, _, i)| i.time_of_impact).collect();
    println!("intersect_ray yields toi in order {:?}", order);
}
```
Expected output: `before any step: None eye->target ray, max_toi 1: toi=Some(0.225) unit-direction ray: toi=Some(0.9) no filter: toi=Some(0.0)  excluding the looker: toi=Some(0.225) start inside a wall: solid=true toi=`

## Validate mesh buffers before TriMesh::with_flags: parry 0.30.2 drops TopologyError and panics on bad indices
**TriMesh::new and with_flags return Err only for an empty index buffer (EmptyIndices); a TopologyError under HALF_EDGE_TOPOLOGY is discarded (Ok, topology() == None), NaN and infinite vertices are accepted, and an index past the vertex buffer panics.**

*Check 1: with_flags returns Ok with no topology on bad winding; set_flags returns the TopologyError* · `runs` · edition 2021 · host · bin · deps: parry3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// What a bad mesh returns at parry3d-f64 0.30.2.
use parry3d_f64::math::Vector;
use parry3d_f64::shape::{TriMesh, TriMeshFlags};

fn quad() -> Vec<Vector> {
    vec![Vector::new(0., 0., 0.), Vector::new(1., 0., 0.), Vector::new(0., 0., 1.), Vector::new(1., 0., 1.)]
}

fn main() {
    println!("empty indices: {:?}", TriMesh::new(quad(), vec![]).err());
    // Two triangles traverse the shared edge (0,1) in the same direction.
    let bad = vec![[0, 1, 2], [0, 1, 3]];
    let m = TriMesh::with_flags(quad(), bad.clone(), TriMeshFlags::HALF_EDGE_TOPOLOGY);
    let ok = m.is_ok();
    let m = m.unwrap();
    println!("with_flags(HALF_EDGE_TOPOLOGY) on bad winding: is_ok={} topology_is_some={} flags_claim_topology={}", ok, m.topology().is_some(), m.flags().contains(TriMeshFlags::HALF_EDGE_TOPOLOGY));
    let mut m = TriMesh::new(quad(), bad).unwrap();
    println!("set_flags(HALF_EDGE_TOPOLOGY): {:?}", m.set_flags(TriMeshFlags::HALF_EDGE_TOPOLOGY));
}
```
Expected output: `empty indices: Some(EmptyIndices) with_flags(HALF_EDGE_TOPOLOGY) on bad winding: is_ok=true topology_is_some=false flags_claim_topology=true set_flags(HALF_EDGE_TOPOLOGY): Err(BadAdjacentTrianglesOrie`

*Check 2: TriMesh::new accepts NaN and infinite vertices; the NaN is missing from the AABB* · `runs` · edition 2021 · host · bin · deps: parry3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// TriMesh::new accepts non-finite vertices; the NaN one is missing from the bounding box.
use parry3d_f64::math::Vector;
use parry3d_f64::shape::TriMesh;

fn main() {
    let nan = vec![Vector::new(0., 0., 0.), Vector::new(f64::NAN, 0., 0.), Vector::new(0., 0., 1.)];
    let m = TriMesh::new(nan, vec![[0, 2, 1]]).unwrap();
    let a = m.local_aabb();
    println!("NaN vertex accepted: aabb x=[{}, {}]", a.mins.x, a.maxs.x);
    let inf = vec![Vector::new(0., 0., 0.), Vector::new(f64::INFINITY, 0., 0.), Vector::new(0., 0., 1.)];
    let m = TriMesh::new(inf, vec![[0, 2, 1]]).unwrap();
    println!("infinite vertex accepted: aabb max x={}", m.local_aabb().maxs.x);
}
```
Expected output: `NaN vertex accepted: aabb x=[0, 0] infinite vertex accepted: aabb max x=inf`

*Check 3: an index past the vertex buffer panics inside TriMesh::new (exit 101)* · `runs` · edition 2021 · host · bin · deps: parry3d_f64 · exit code 101 · **✔ oracle pass**
```rust
// An index past the vertex buffer is not an Err: TriMesh::new panics (a trap under panic = "abort").
use parry3d_f64::math::Vector;
use parry3d_f64::shape::TriMesh;

fn main() {
    let tri = vec![Vector::new(0., 0., 0.), Vector::new(1., 0., 0.), Vector::new(0., 0., 1.)];
    println!("building");
    let r = TriMesh::new(tri, vec![[0, 2, 7]]);
    println!("returned ok={}", r.is_ok());
}
```
Expected output: `building`

*Check 4: a validating loader refuses NaN, bad indices, repeats and bad winding as data* · `runs` · edition 2021 · host · bin · deps: parry3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// The fix: refuse before parry, then take the topology verdict from set_flags, not with_flags.
use parry3d_f64::math::Vector;
use parry3d_f64::shape::{TopologyError, TriMesh, TriMeshFlags};

#[derive(Debug)]
enum Refusal {
    Empty,
    NonFinite { vertex: usize },
    IndexOutOfRange { triangle: usize, index: u32 },
    RepeatedIndex { triangle: usize },
    Topology(TopologyError),
}

fn load(vertices: &[[f64; 3]], indices: &[[u32; 3]]) -> Result<TriMesh, Refusal> {
    if indices.is_empty() { return Err(Refusal::Empty); }
    if let Some(vertex) = vertices.iter().position(|p| !p.iter().all(|c| c.is_finite())) {
        return Err(Refusal::NonFinite { vertex });
    }
    for (triangle, t) in indices.iter().enumerate() {
        if let Some(&index) = t.iter().find(|&&i| i as usize >= vertices.len()) {
            return Err(Refusal::IndexOutOfRange { triangle, index });
        }
        if t[0] == t[1] || t[1] == t[2] || t[0] == t[2] { return Err(Refusal::RepeatedIndex { triangle }); }
    }
    let v: Vec<Vector> = vertices.iter().map(|p| Vector::new(p[0], p[1], p[2])).collect();
    let mut mesh = TriMesh::new(v, indices.to_vec()).map_err(|_| Refusal::Empty)?;
    mesh.set_flags(TriMeshFlags::HALF_EDGE_TOPOLOGY).map_err(Refusal::Topology)?;
    Ok(mesh)
}

fn main() {
    let q = [[0., 0., 0.], [1., 0., 0.], [0., 0., 1.], [1., 0., 1.]];
    let nan = [[0., 0., 0.], [f64::NAN, 0., 0.], [0., 0., 1.], [1., 0., 1.]];
    let cases: [(&str, &[[f64; 3]], &[[u32; 3]]); 5] = [
        ("good", &q, &[[0, 2, 1], [1, 2, 3]]),
        ("nan", &nan, &[[0, 2, 1]]),
        ("index 7", &q, &[[0, 2, 7]]),
        ("repeated", &q, &[[0, 0, 1]]),
        ("bad winding", &q, &[[0, 1, 2], [0, 1, 3]]),
    ];
    for (name, v, i) in cases {
        match load(v, i) {
            Ok(m) => println!("{name}: loaded {} triangles", m.indices().len()),
            Err(r) => println!("{name}: refused {:?}", r),
        }
    }
}
```
Expected output: `good: loaded 2 triangles nan: refused NonFinite { vertex: 1 } index 7: refused IndexOutOfRange { triangle: 0, index: 7 } repeated: refused RepeatedIndex { triangle: 0 } bad winding: refused Topology(B`

## Pick parry 0.30.2 shapes by body role: primitives, convex or compound on moving bodies, trimeshes on fixed
**At parry3d-f64 0.30.2 SharedShape covers ball, cuboid, capsule, cylinder, cone, round variants, convex polyhedra, compounds, trimeshes, heightfields and voxels; a TriMesh has no interior, so it belongs on fixed bodies only.**

*Check 1: every shape family builds at parry3d-f64 0.30.2, voxels included* · `runs` · edition 2021 · host · bin · deps: parry3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// Every shape family a collider can use at parry3d-f64 0.30.2, including voxels.
use parry3d_f64::math::{IVector, Pose, Vector};
use parry3d_f64::shape::SharedShape;
use parry3d_f64::utils::Array2;

fn v(x: f64, y: f64, z: f64) -> Vector { Vector::new(x, y, z) }

fn main() {
    let tet = [v(0., 0., 0.), v(1., 0., 0.), v(0., 1., 0.), v(0., 0., 1.)];
    let shapes = vec![
        SharedShape::ball(0.5),
        SharedShape::cuboid(0.5, 0.5, 0.5),
        SharedShape::round_cuboid(0.4, 0.4, 0.4, 0.1),
        SharedShape::capsule_y(0.25, 0.25),
        SharedShape::cylinder(0.5, 0.25),
        SharedShape::cone(0.5, 0.25),
        SharedShape::convex_hull(&tet).unwrap(),
        SharedShape::compound(vec![(Pose::IDENTITY, SharedShape::ball(0.5)), (Pose::from_translation(v(1., 0., 0.)), SharedShape::cuboid(0.2, 0.2, 0.2))]),
        SharedShape::trimesh(tet.to_vec(), vec![[0, 2, 1], [0, 1, 3], [0, 3, 2], [1, 2, 3]]).unwrap(),
        SharedShape::heightfield(Array2::new(2, 2, vec![0.0; 4]), v(1., 1., 1.)),
        SharedShape::voxels(v(0.5, 0.5, 0.5), &[IVector::new(0, 0, 0), IVector::new(1, 0, 0)]),
    ];
    let names: Vec<String> = shapes.iter().map(|s| format!("{:?}", s.shape_type())).collect();
    println!("{}", names.join(" "));
}
```
Expected output: `Ball Cuboid RoundCuboid Capsule Cylinder Cone ConvexPolyhedron Compound TriMesh HeightField Voxels`

*Check 2: an open trimesh has mass 0 and ccd_thickness 0; a closed one matches its hull* · `runs` · edition 2021 · host · bin · deps: parry3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// A trimesh has no interior: an open surface has zero mass and zero CCD thickness.
use parry3d_f64::math::Vector;
use parry3d_f64::shape::{Shape, SharedShape, TriMesh};

fn v(x: f64, y: f64, z: f64) -> Vector { Vector::new(x, y, z) }

fn main() {
    let open = TriMesh::new(vec![v(0., 0., 0.), v(1., 0., 0.), v(0., 0., 1.), v(1., 0., 1.)], vec![[0, 2, 1], [1, 2, 3]]).unwrap();
    println!("open trimesh: mass={} ccd_thickness={}", open.mass_properties(1.0).mass(), open.ccd_thickness());
    let p = vec![v(0., 0., 0.), v(1., 0., 0.), v(0., 1., 0.), v(0., 0., 1.)];
    let closed = TriMesh::new(p.clone(), vec![[0, 2, 1], [0, 1, 3], [0, 3, 2], [1, 2, 3]]).unwrap();
    let hull = SharedShape::convex_hull(&p).unwrap();
    println!("closed tetra: trimesh mass={:.6} convex hull mass={:.6}", closed.mass_properties(1.0).mass(), hull.mass_properties(1.0).mass());
}
```
Expected output: `open trimesh: mass=0 ccd_thickness=0 closed tetra: trimesh mass=0.166667 convex hull mass=0.166667`

## Set FIX_INTERNAL_EDGES on ground dynamic bodies slide over; test heightfield row 0 moving +x on its own
**Without the flag, a frictionless box sliding flat at 2 u/s stopped dead at the first internal edge of a trimesh or heightfield (0.25 of 2.00 travelled in 64 quanta) because the edge adds a sideways contact normal. TriMeshFlags::FIX_INTERNAL_EDGES removed the snag; on a 9 x 9 heightfield, HeightFieldFlags::FIX_INTERNAL_EDGES removed it for every row and column in both directions except moving +x in row 0, the lowest-z row of cells.**

*Check 1: an internal edge adds a sideways normal; FIX_INTERNAL_EDGES removes it (trimesh, heightfield)* · `runs` · edition 2021 · host · bin · deps: parry3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// A box sunk 0.01 into a flat floor, its left face 0.004 past an internal edge: without
// FIX_INTERNAL_EDGES the contact manifolds include a sideways normal from that edge.
use parry3d_f64::math::{Pose, Vector};
use parry3d_f64::query::{ContactManifold, DefaultQueryDispatcher, PersistentQueryDispatcher};
use parry3d_f64::shape::{Cuboid, HeightField, HeightFieldFlags, Shape, TriMesh, TriMeshFlags};
use parry3d_f64::utils::Array2;

fn v(x: f64, y: f64, z: f64) -> Vector { Vector::new(x, y, z) }

fn normals(floor: &dyn Shape, z: f64) -> Vec<[f64; 3]> {
    let bx = Cuboid::new(v(0.25, 0.25, 0.25));
    let mut m: Vec<ContactManifold<(), ()>> = Vec::new();
    DefaultQueryDispatcher.contact_manifolds(&Pose::from_translation(v(0.246, 0.24, z)), floor, &bx, 0.0, &mut m, &mut None).unwrap();
    let r = |c: f64| (c * 1e3).round() / 1e3 + 0.0;
    let mut out: Vec<[f64; 3]> = m.iter().filter(|m| !m.points.is_empty())
        .map(|m| { let n = m.local_n1; [r(n.x), r(n.y), r(n.z)] }).collect();
    out.sort_by(|a, b| a.partial_cmp(b).unwrap());
    out.dedup();
    out
}

fn main() {
    // Flat trimesh strip: two quads meeting at the internal edge x = 0, +Y outward.
    let verts = vec![v(-1., 0., -1.), v(0., 0., -1.), v(1., 0., -1.), v(-1., 0., 1.), v(0., 0., 1.), v(1., 0., 1.)];
    let idx = vec![[0, 3, 1], [1, 3, 4], [1, 4, 2], [2, 4, 5]];
    println!("trimesh plain: {:?}", normals(&TriMesh::new(verts.clone(), idx.clone()).unwrap(), 0.0));
    println!("trimesh FIX_INTERNAL_EDGES: {:?}", normals(&TriMesh::with_flags(verts, idx, TriMeshFlags::FIX_INTERNAL_EDGES).unwrap(), 0.0));
    // Flat heightfield: 3 rows x 3 columns, scale (2, 1, 2): column seam at x = 0; the box sits mid-row (z = 0.5).
    let hf = |f| HeightField::with_flags(Array2::new(3, 3, vec![0.0; 9]), v(2.0, 1.0, 2.0), f);
    println!("heightfield plain: {:?}", normals(&hf(HeightFieldFlags::empty()), 0.5));
    println!("heightfield FIX_INTERNAL_EDGES: {:?}", normals(&hf(HeightFieldFlags::FIX_INTERNAL_EDGES), 0.5));
}
```
Expected output: `trimesh plain: [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]] trimesh FIX_INTERNAL_EDGES: [[0.0, 1.0, 0.0]] heightfield plain: [[0.0, 1.0, 0.0], [1.0, 0.0, 0.0]] heightfield FIX_INTERNAL_EDGES: [[0.0, 1.0, 0.0]]`

*Check 2: seams stop a sliding box, CCD or not; the flag fixes every 9x9 row and column but row 0 moving +x* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// Full rapier3d-f64 0.35.3 pipeline: a frictionless, rotation-locked box (half 0.25) sliding at
// 2 u/s over flat ground made of cells 1.0 wide. Distance travelled in 64 quanta (ideal 2.00).
use rapier3d_f64::prelude::*;

const DT: f64 = 1.0 / 64.0;

fn slide_with(ground: Collider, start: Vector, dir: Vector, ccd_substeps: Option<usize>) -> f64 {
    let mut world = PhysicsWorld::new();
    world.gravity = Vector::new(0.0, -8.0, 0.0);
    world.integration_parameters.dt = DT;
    world.integration_parameters.contact_clustering = false;
    if let Some(n) = ccd_substeps { world.integration_parameters.max_ccd_substeps = n; }
    world.insert(RigidBodyBuilder::fixed(), ground);
    let (b, _) = world.insert(RigidBodyBuilder::dynamic().translation(start).linvel(dir * 2.0).lock_rotations(), ColliderBuilder::cuboid(0.25, 0.25, 0.25).friction(0.0));
    for _ in 0..64 { world.step(); }
    (world.bodies[b].translation() - start).dot(dir)
}

fn slide(ground: Collider, start: Vector, dir: Vector) -> f64 { slide_with(ground, start, dir, None) }

// A flat 9 x 9 heightfield, scale 8 x 8: rows advance z (row 0 is the lowest z), columns advance x.
fn field(flags: HeightFieldFlags, start: Vector, dir: Vector) -> f64 {
    let hf = ColliderBuilder::heightfield_with_flags(Array2::new(9, 9, vec![0.0; 81]), Vector::new(8.0, 1.0, 8.0), flags).friction(0.0).build();
    slide(hf, start, dir)
}

fn strip(flags: TriMeshFlags) -> f64 {
    let mut v = Vec::new();
    for i in 0..9 { v.push(Vector::new(-4.0 + i as f64, 0.0, -2.0)); v.push(Vector::new(-4.0 + i as f64, 0.0, 2.0)); }
    let mut idx = Vec::new();
    for i in 0..8u32 { let a = 2 * i; idx.push([a, a + 1, a + 2]); idx.push([a + 2, a + 1, a + 3]); }
    let tm = ColliderBuilder::trimesh_with_flags(v, idx, flags).unwrap().friction(0.0).build();
    slide(tm, Vector::new(-3.5, 0.25, 0.0), Vector::X)
}

fn main() {
    let f = HeightFieldFlags::FIX_INTERNAL_EDGES;
    let plain = |ccd| {
        let hf = ColliderBuilder::heightfield(Array2::new(9, 9, vec![0.0; 81]), Vector::new(8.0, 1.0, 8.0)).friction(0.0).build();
        slide_with(hf, Vector::new(-2.5, 0.25, -2.5), Vector::X, ccd)
    };
    println!("heightfield plain, row 1, +x: {:.2} (CCD off: {:.2}); with FIX_INTERNAL_EDGES: {:.2}", plain(None), plain(Some(0)), field(f, Vector::new(-2.5, 0.25, -2.5), Vector::X));
    let mut s = String::new();
    for i in 0..8 {
        let z = -3.5 + i as f64;
        s += &format!(" r{i}:{:.2}/{:.2}", field(f, Vector::new(-2.5, 0.25, z), Vector::X), field(f, Vector::new(2.5, 0.25, z), -Vector::X));
    }
    println!("heightfield FIX, along x (+x/-x) per row:{s}");
    let mut s = String::new();
    for j in 0..8 {
        let x = -3.5 + j as f64;
        s += &format!(" c{j}:{:.2}/{:.2}", field(f, Vector::new(x, 0.25, -2.5), Vector::Z), field(f, Vector::new(x, 0.25, 2.5), -Vector::Z));
    }
    println!("heightfield FIX, along z (+z/-z) per col:{s}");
    println!("trimesh strip, +x: plain={:.2} FIX={:.2}", strip(TriMeshFlags::empty()), strip(TriMeshFlags::FIX_INTERNAL_EDGES));
}
```
Expected output: `heightfield plain, row 1, +x: 0.25 (CCD off: 0.25); with FIX_INTERNAL_EDGES: 2.00 heightfield FIX, along x (+x/-x) per row: r0:0.25/2.00 r1:2.00/2.00 r2:2.00/2.00 r3:2.00/2.00 r4:2.00/2.00 r5:2.00/2.0`

*Check 3: the kinematic walker crosses the same seams with or without the flag* · `runs` · edition 2021 · host · bin · deps: rapier3d_f64 · exit code 0 · **✔ oracle pass**
```rust
// The kinematic controller is not snagged by the seams that stop a sliding dynamic box.
use rapier3d_f64::control::{CharacterAutostep, CharacterLength, KinematicCharacterController};
use rapier3d_f64::prelude::*;

const DT: f64 = 1.0 / 64.0;

fn controller() -> KinematicCharacterController {
    KinematicCharacterController {
        up: Vector::new(0.0, 1.0, 0.0),
        offset: CharacterLength::Absolute(0.01),
        slide: true,
        autostep: Some(CharacterAutostep { max_height: CharacterLength::Absolute(0.3), min_width: CharacterLength::Absolute(0.2), include_dynamic_bodies: false }),
        max_slope_climb_angle: core::f64::consts::FRAC_PI_4,
        min_slope_slide_angle: 50.0 * core::f64::consts::PI / 180.0,
        snap_to_ground: Some(CharacterLength::Absolute(0.2)),
        normal_nudge_factor: 1.0e-4,
    }
}

// A box walker (half 0.25, 0.5, 0.25) walks +x at 1 u/s for 128 quanta over a flat field of 9 columns.
fn walk(rows: usize, flags: HeightFieldFlags) -> (f64, usize) {
    let mut world = PhysicsWorld::new();
    world.integration_parameters.dt = DT;
    let scale = Vector::new(8.0, 1.0, rows as f64 - 1.0);
    world.insert(RigidBodyBuilder::fixed(), ColliderBuilder::heightfield_with_flags(Array2::new(rows, 9, vec![0.0; rows * 9]), scale, flags));
    let shape = SharedShape::cuboid(0.25, 0.5, 0.25);
    let start = Vector::new(-3.5, 0.51, -scale.z * 0.5 + 0.5);
    let (h, _) = world.insert(RigidBodyBuilder::kinematic_position_based().translation(start), ColliderBuilder::new(shape.clone()));
    world.step();
    let ctl = controller();
    let mut airborne = 0;
    for _ in 0..128 {
        let pos = *world.bodies[h].position();
        let mv = {
            let q = world.query_pipeline_with_filter(QueryFilter::new().exclude_rigid_body(h));
            ctl.move_shape(DT, &q, &*shape, &pos, Vector::new(1.0 * DT, -8.0 * DT * DT, 0.0), |_| {})
        };
        if !mv.grounded { airborne += 1; }
        world.bodies[h].set_next_kinematic_translation(pos.translation + mv.translation);
        world.step();
    }
    (world.bodies[h].translation().x - start.x, airborne)
}

fn main() {
    for rows in [2usize, 3] {
        let (a, na) = walk(rows, HeightFieldFlags::empty());
        let (b, nb) = walk(rows, HeightFieldFlags::FIX_INTERNAL_EDGES);
        println!("{rows} rows: plain travelled {:.3} (airborne {na}), FIX travelled {:.3} (airborne {nb})", a, b);
    }
}
```
Expected output: `2 rows: plain travelled 1.985 (airborne 0), FIX travelled 1.985 (airborne 0) 3 rows: plain travelled 2.000 (airborne 0), FIX travelled 2.000 (airborne 0)`

