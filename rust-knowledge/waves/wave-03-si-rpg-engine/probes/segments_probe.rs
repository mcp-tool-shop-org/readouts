// The rest of a wasm instance's runtime state beyond globals, tables and memory:
// data and element segments by kind (a passive segment has a "dropped" bit that
// data.drop / elem.drop flip at run time and a memory image does not carry), the
// DataCount and start sections, imports, and every bulk-memory / table instruction.
use wasmparser::{DataKind, ElementKind, Operator, Parser, Payload};

fn scan(label: &str, path: &str) -> Result<(), Box<dyn std::error::Error>> {
    let bytes = std::fs::read(path)?;
    let (mut d_active, mut d_passive, mut e_active, mut e_passive, mut e_declared) = (0u32, 0u32, 0u32, 0u32, 0u32);
    let (mut imports, mut start, mut datacount) = (0u32, false, None::<u32>);
    let mut n: std::collections::BTreeMap<&'static str, u32> = Default::default();
    for p in Parser::new(0).parse_all(&bytes) {
        match p? {
            Payload::ImportSection(r) => imports += r.count(),
            Payload::StartSection { .. } => start = true,
            Payload::DataCountSection { count, .. } => datacount = Some(count),
            Payload::DataSection(r) => {
                for d in r {
                    match d?.kind {
                        DataKind::Active { .. } => d_active += 1,
                        DataKind::Passive => d_passive += 1,
                    }
                }
            }
            Payload::ElementSection(r) => {
                for e in r {
                    match e?.kind {
                        ElementKind::Active { .. } => e_active += 1,
                        ElementKind::Passive => e_passive += 1,
                        ElementKind::Declared => e_declared += 1,
                    }
                }
            }
            Payload::CodeSectionEntry(body) => {
                let mut ops = body.get_operators_reader()?;
                while !ops.eof() {
                    let k = match ops.read()? {
                        Operator::MemoryInit { .. } => "memory.init",
                        Operator::DataDrop { .. } => "data.drop",
                        Operator::TableInit { .. } => "table.init",
                        Operator::ElemDrop { .. } => "elem.drop",
                        Operator::TableCopy { .. } => "table.copy",
                        Operator::TableFill { .. } => "table.fill",
                        Operator::TableSet { .. } => "table.set",
                        Operator::TableGrow { .. } => "table.grow",
                        Operator::MemoryCopy { .. } => "memory.copy",
                        Operator::MemoryFill { .. } => "memory.fill",
                        Operator::MemoryGrow { .. } => "memory.grow",
                        _ => continue,
                    };
                    *n.entry(k).or_default() += 1;
                }
            }
            _ => {}
        }
    }
    println!("== {label}");
    println!("   imports={imports} start_section={start} datacount={datacount:?}");
    println!("   data segments: active={d_active} passive={d_passive}   element segments: active={e_active} passive={e_passive} declared={e_declared}");
    println!("   instructions: {n:?}");
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
