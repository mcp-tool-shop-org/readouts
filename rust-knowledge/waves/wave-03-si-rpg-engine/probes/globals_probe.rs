// Lists every global of each solver build, its mutability and initializer, how many
// `global.set` instructions write it, and the module's other runtime-mutable state:
// memories (limits), tables (limits) and any table.set / table.grow / memory.grow.
use wasmparser::{ExternalKind, Operator, Parser, Payload};

fn scan(label: &str, path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let bytes = std::fs::read(path)?;
    let mut globals: Vec<(String, bool, String)> = Vec::new();
    let mut exported: Vec<(String, u32)> = Vec::new();
    let mut sets: std::collections::BTreeMap<u32, u32> = Default::default();
    let (mut table_set, mut table_grow, mut mem_grow, mut funcs) = (0u32, 0u32, 0u32, 0u32);
    let mut memories = Vec::new();
    let mut tables = Vec::new();
    for payload in Parser::new(0).parse_all(&bytes) {
        match payload? {
            Payload::GlobalSection(reader) => {
                for g in reader {
                    let g = g?;
                    let mut ops = g.init_expr.get_operators_reader();
                    let mut init = Vec::new();
                    while !ops.eof() {
                        let op = ops.read()?;
                        if !matches!(op, Operator::End) {
                            init.push(format!("{op:?}"));
                        }
                    }
                    globals.push((format!("{:?}", g.ty.content_type), g.ty.mutable, init.join(" ")));
                }
            }
            Payload::ExportSection(reader) => {
                for e in reader {
                    let e = e?;
                    if e.kind == ExternalKind::Global {
                        exported.push((e.name.to_string(), e.index));
                    }
                }
            }
            Payload::MemorySection(reader) => {
                for m in reader {
                    let m = m?;
                    memories.push(format!("initial={} maximum={:?}", m.initial, m.maximum));
                }
            }
            Payload::TableSection(reader) => {
                for t in reader {
                    let t = t?;
                    tables.push(format!("initial={} maximum={:?}", t.ty.initial, t.ty.maximum));
                }
            }
            Payload::CodeSectionEntry(body) => {
                funcs += 1;
                let mut ops = body.get_operators_reader()?;
                while !ops.eof() {
                    match ops.read()? {
                        Operator::GlobalSet { global_index } => *sets.entry(global_index).or_default() += 1,
                        Operator::TableSet { .. } => table_set += 1,
                        Operator::TableGrow { .. } => table_grow += 1,
                        Operator::MemoryGrow { .. } => mem_grow += 1,
                        _ => {}
                    }
                }
            }
            _ => {}
        }
    }
    println!("== {label}: {} bytes, {funcs} function bodies", bytes.len());
    println!("   memories: {memories:?}   tables: {tables:?}");
    println!("   memory.grow={mem_grow} table.set={table_set} table.grow={table_grow}");
    for (i, (ty, mutable, init)) in globals.iter().enumerate() {
        let name = exported.iter().find(|(_, idx)| *idx == i as u32).map(|(n, _)| n.as_str()).unwrap_or("-");
        let writes = sets.get(&(i as u32)).copied().unwrap_or(0);
        println!("   global {i}: {ty} mutable={mutable} init=[{init}] exported_as={name} global.set_sites={writes}");
    }
    Ok(())
}

fn main() {
    // SI_BUILDS: a directory holding the three builds, each a copy of si-rpg-engine's solver/
    // built with `cargo +1.98.1 build --release --target wasm32-unknown-unknown`:
    //   main/si_solver.wasm     main's persistent law (std dlmalloc)
    //   pr44/si_solver.wasm     PR #44 at b99a636 (arena, fixed 256 pages)
    //   dlarena/si_solver.wasm  dlmalloc 0.2.13 over one fixed arena (answer 5's fix)
    let Ok(base) = std::env::var("SI_BUILDS") else {
        println!("set SI_BUILDS to the directory holding main/, pr44/ and dlarena/");
        return;
    };
    for (label, rel) in [
        ("main (persistent law, std dlmalloc)", "main/si_solver.wasm"),
        ("PR #44 (arena, fixed 256 pages)", "pr44/si_solver.wasm"),
        ("dlmalloc over a fixed arena (Q5 fix)", "dlarena/si_solver.wasm"),
    ] {
        let path = std::path::Path::new(&base).join(rel);
        if let Err(e) = scan(label, &path.to_string_lossy()) {
            println!("== {label}: ERROR {e}");
        }
    }
}
