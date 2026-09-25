<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.md">English</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/readouts/readme.png" alt="readouts" width="400" />
</p>

<h1 align="center">readouts</h1>

<p align="center">
  Verified, source-backed SQLite knowledge bases that an agent reads one slice at a time.
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/readouts/actions/workflows/verify.yml"><img src="https://github.com/mcp-tool-shop-org/readouts/actions/workflows/verify.yml/badge.svg" alt="verify" /></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License" /></a>
  <a href="https://mcp-tool-shop-org.github.io/readouts/"><img src="https://img.shields.io/badge/Landing_Page-live-34d399" alt="Landing Page" /></a>
</p>

---

readouts es un conjunto de bases de conocimiento sobre las herramientas que hay detrás de un pequeño estudio de juegos: Rust, Godot, Blender, diseño de sprites y animaciones, modelos de IA locales y los motores que los ejecutan y entrenan, la voz cantada, contenedores de GPU y el libro mayor XRP.

Cada base de conocimiento (KB) es una base de datos SQLite con un índice de texto completo. Cada entrada indica sus fuentes, registra la fase de investigación que la produjo y contiene una marca `verified`. Solo un veredicto de un verificador independiente puede establecer esa marca; la opinión del autor sobre su propio trabajo nunca se tiene en cuenta.

El nombre proviene de [loadout-os](https://github.com/mcp-tool-shop-org/loadout-os), que *carga* el conocimiento adecuado para una tarea. readouts es lo que lee.

## Las bases de conocimiento

| KB | Qué | Estado |
|----|------|--------|
| [blender-knowledge](blender-knowledge/) | Práctica actual, basada en la web, de Blender 4.x para el pipeline de renderizado de sprites sin cabeza del estudio (importar un GLB generado por TRELLIS → renderizar sprites en 8 direcciones mediante blender --background --python → componer en un juego 2.5D) más preparación general de activos para el juego. | **219 recetas · 10 dominios · 8 fases · 83/219 verificadas** |
| [docker-knowledge](docker-knowledge/) | La base de conocimiento detrás del producto gpu-container: cómo empaquetar, medir y colocar modelos de forma precisa en una GPU. | **160 hallazgos · 6 dominios · 9 fases · 73/160 verificadas** |
| [godot-knowledge](godot-knowledge/) | Conocimiento actual, verificado de forma adversaria, de Godot 4 para la creación de un RPG táctico por turnos en 2.5D. | **177 recetas · 6 dominios · 7 fases · 50/177 verificadas** |
| [model-knowledge](model-knowledge/) | Base de conocimiento verificada de los mejores MODELOS de IA generativa locales por propósito (imagen / edición / control / video / 3D / audio / LLM / subtítulos) para el equipo RTX 5090, con prioridad en las licencias comerciales. | **129 modelos · 9 dominios · 19 fases · 126/129 verificados** |
| [rust-knowledge](rust-knowledge/) | Rust verificado para la creación de si-rpg-engine (elementos esenciales, avanzados y cómo el motor lo utiliza: ABI wasm sin procesar, determinismo de punto flotante, estado y restauración de Rapier 0.35, bytes reproducibles) y una primera fase para la legislación musical de si-jam-sessions, con cada comprobación de código ejecutada por el compilador rustc 1.98.1. | **267 recetas · 27 dominios · 4 fases · 266/267 verificadas** |
| [sprite-motion-knowledge](sprite-motion-knowledge/) | El método portátil para animar sprites para este equipo | **246 recetas · 19 dominios · 8 fases · 170/246 verificadas** |
| [sprites-knowledge](sprites-knowledge/) | El método portátil para crear arte conceptual y convertirlo en sprites 2.5D listos para usar en un JRPG para este equipo | **215 recetas · 8 dominios · 6 fases · 92/215 verificadas** |
| [tensor-engine-knowledge](tensor-engine-knowledge/) | Base de conocimiento verificada de los MOTORES que ejecutan y entrenan modelos de IA localmente en el equipo RTX 5090 (Blackwell / sm_120 / Windows). | **193 motores · 10 dominios · 17 fases · 134/193 verificados** |
| [training-knowledge](training-knowledge/) | Base de conocimiento verificada de los métodos portátiles de ENTRENAMIENTO: métodos, recetas, valores de hiperparámetros, conocimientos sobre conjuntos de datos y evaluación, para el entrenamiento de LoRAs / ajustes finos en el equipo RTX 5090 (Blackwell / Windows / WSL2). La capa de "cómo entrenar" entre los pesos (conocimiento del modelo) y el software (conocimiento del motor de tensores). | **204 técnicas · 13 dominios · 16 fases · 101/204 verificadas** |
| [vocology-knowledge](vocology-knowledge/) | Técnicas de voz cantada: vocología (fuente-filtro, registros, formante del cantante), prosodia musical frente a la prosodia del habla, alineación de letras y notas, SVS controlable por partitura frente a generadores de canciones a partir de letras, evaluación de admisión/enseñanza. | **317 hallazgos · 19 dominios · 13 fases · 214/317 verificados** |
| [xrpl-knowledge](xrpl-knowledge/) | Base de conocimiento verificada del ECOSISTEMA XRP Ledger para un desarrollador: características del protocolo, tipos de transacciones, estándares XLS, bibliotecas de cliente y herramientas, cada una etiquetada con su estado actual en la red principal o en la enmienda. Ecosistema completo: XRPL mainnet + Xahau/Hooks + la cadena lateral XRPL EVM + la capa institucional (RLUSD, cumplimiento). | **457 capacidades · 12 dominios · 10 fases · 362/457 verificadas** |

La tabla se genera a partir de [`index.json`](index.json) mediante `shared/sync_readme_table.py`, y `python verify.py` falla si se desvía. [`index.md`](index.md) es el mismo mapa escrito para agentes, y [`index.html`](index.html) lo renderiza.

Cada carpeta de KB contiene su base de datos, un `catalog/` de páginas de Markdown generadas por dominio, una carpeta `waves/` con los registros de investigación y verificación de cada fase, y su propio `README.md`.

## Inicio rápido

```bash
git clone https://github.com/mcp-tool-shop-org/readouts
cd readouts
python verify.py
```

`verify.py` necesita Python 3.10 o superior y nada fuera de la biblioteca estándar. Las bases de datos son archivos SQLite comunes, por lo que cualquier cliente SQLite puede abrirlas.

Busque en una KB a través de su índice de texto completo y, a continuación, vuelva a unirlo a la entrada:

```sql
-- sqlite3 rust-knowledge/rust.db
SELECT r.name, r.verified
FROM recipes_fts f
JOIN recipes r ON r.id = f.rowid
WHERE recipes_fts MATCH 'rapier'
LIMIT 5;
```

Agregue `AND r.verified = 1` para mantener solo lo que el verificador confirmó. El mismo patrón funciona en cada KB. La tabla de entidades tiene el nombre que se indica en [`index.md`](index.md): `recipes`, `findings`, `models`, `engines`, `techniques` o `capabilities`, cada una con un índice `<table>_fts` correspondiente. La mayoría de las KB también tienen una vista `v_recommended` (docker-knowledge y vocology-knowledge tienen `v_load_bearing`). Estas vistas seleccionan según el campo de recomendación de cada KB, no según `verified`.

## Cómo una entrada obtiene `verified`

1. **Una fase de investigación.** Un canal de investigación por dominio escribe las entradas, y cada entrada cita sus fuentes como pares `{url, claim}`.
2. **Un verificador independiente.** Un segundo agente, que nunca ve el razonamiento del investigador, comprueba cada entrada con las páginas que cita y devuelve un veredicto. En la mayoría de las fases, el verificador proviene de la misma familia de modelos que el investigador; algunas fases añaden un miembro de una familia diferente. El registro de cada fase indica cuál.
3. **Una definición de `verified`.** `verified = 1` solo cuando el veredicto externo lo indica ([`shared/verdicts.py`](shared/verdicts.py)). Una entrada sin veredicto permanece sin verificar. Trátela como una pista, no como un hecho.
4. **Un compilador, cuando hay código.** Cada comprobación de código en rust-knowledge se compila y, cuando lo indica, se ejecuta mediante `rustc 1.98.1`. Una receta cuyo propio ejemplo falla al compilarse nunca se verifica.

Cada iteración guarda su registro en la carpeta `waves/` de la base de conocimiento: `dispatch.md` (lo que se solicitó y lo que se obtuvo), `research-raw.json` (lo que se cargó) y, cuando la iteración lo tenga, `verification.md` (lo que encontraron el verificador y el compilador). Las bases de conocimiento que mantienen un registro duradero de los resultados lo guardan en `verification/verdicts.json`.

## Asigne un agente a una sección

Dos índices de configuración evitan que un agente lea todo el corpus:

1. El archivo raíz [`.claude/loadout/index.json`](.claude/loadout/index.json) asigna una tarea a la base de conocimiento correcta.
2. El archivo `.claude/loadout/index.json` de cada base de conocimiento la asigna al dominio correcto dentro de esa base de conocimiento.

```bash
npx @mcptoolshop/loadout-os validate .claude/loadout/index.json
npx @mcptoolshop/loadout-os resolve --project .
```

`resolve` también fusiona su propia capa de configuración global si la tiene.

## Revise el corpus usted mismo

`python verify.py` es el nivel base del repositorio. Comprueba que los archivos generados sean precisos con respecto a las bases de datos: que cada ID de fila de texto completo se vincule a su entrada correspondiente, que ninguna entrada verificada carezca de una fuente, que `verified` haga referencia a un resultado externo, que la puerta de entrada y la tabla de este archivo README coincidan con las bases de datos, y que ningún enlace relativo esté roto.

- `FAIL` incumple un contrato o proporciona datos incorrectos. Bloquea la publicación.
- `WARN` es un defecto real que se conoce, está delimitado y se registra.

Cada resultado FAIL y WARN incluye un código estable y una pista para el siguiente paso. `python verify.py --json` imprime un objeto JSON por cada comprobación. El código de salida es 0 cuando todo está correcto, 1 en caso de un FAIL y 2 si la propia comprobación falló. CI lo ejecuta en cada confirmación que modifica el corpus.

## Seguridad y modelo de amenazas

- **De qué se trata este repositorio:** datos. Contiene bases de datos SQLite, archivos Markdown, JSON y los scripts de Python que los crearon. Nada se ejecuta durante la instalación y no hay nada que instalar.
- **La ruta de lectura es local.** Consultar una base de datos, `verify.py`, y los generadores (`regen.py`, `shared/gen_*.py`, el archivo `load_db.py` de cada base de conocimiento, `gen_catalog.py` y `gen_loadout.py`) leen archivos en esta copia y solo escriben archivos derivados dentro de ella. No establecen ninguna conexión de red, no leen credenciales y no envían telemetría. `verify.py` no escribe nada.
- **Las herramientas de investigación no lo hacen.** Los scripts que se guardan como registro de cómo se crearon las iteraciones (por ejemplo, cada archivo `verify_cloud.py`, el archivo `openrouter_lane.py` de rust-knowledge y el archivo `verifier/` de tensor-engine-knowledge) llaman a un modelo: un daemon Ollama local o OpenRouter con un archivo `OPENROUTER_API_KEY` que se define en el entorno. Algunos también recuperan las páginas que citan. No se guarda ninguna clave en el repositorio. `compile_oracle.py setup` descarga los paquetes Rust fijados a través de cargo, una sola vez. Ninguno de estos se ejecuta a menos que usted lo ejecute.
- **Permisos:** acceso de lectura a la copia; acceso de escritura solo si se vuelve a generar.
- **No hay telemetría**, en ninguna parte del repositorio.
- **De qué trata el contenido:** notas de investigación con citas. Una entrada no verificada es una pista, no un hecho. Las notas de licencia sobre los modelos, los conjuntos de datos y los paquetes no son asesoramiento legal; lea la licencia en sí antes de enviar cualquier cosa.

Para informar de un problema, consulte [SECURITY.md](SECURITY.md).

## Mantenimiento

[MAINTENANCE.md](MAINTENANCE.md) es el manual de procedimientos: agregar una iteración o una base de conocimiento, ejecutar una verificación exhaustiva y las trampas que ya le han costado una tarde a alguien. [CONVENTIONS.md](CONVENTIONS.md) describe la estructura que comparte cada base de conocimiento. El [manual](https://mcp-tool-shop-org.github.io/readouts/handbook/) explica en detalle cómo consultar, verificar y enrutar. Los cambios se enumeran en [CHANGELOG.md](CHANGELOG.md).

## Licencia

[MIT](LICENSE)

---

Creado por <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
