<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.md">English</a>
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

readouts é um conjunto de bases de conhecimento sobre as ferramentas utilizadas por um pequeno estúdio de jogos: Rust, Godot, Blender, criação de sprites e animações, modelos de IA locais e os motores que os executam e treinam, voz cantada, contêineres GPU e o XRP Ledger.

Cada base de conhecimento (KB) é um banco de dados SQLite com um índice de texto completo. Cada entrada indica suas fontes, registra a fase de pesquisa que a produziu e contém uma flag `verified`. Apenas um veredicto de um verificador separado pode definir essa flag; a opinião do autor sobre seu próprio trabalho nunca é considerada.

O nome vem de [loadout-os](https://github.com/mcp-tool-shop-org/loadout-os), que *carrega* o conhecimento correto para uma tarefa. readouts é o que ele lê.

## As bases de conhecimento

| KB | O quê | Status |
|----|------|--------|
| [blender-knowledge](blender-knowledge/) | Prática atual, baseada na web, do Blender 4.x para o pipeline de renderização de sprites sem interface gráfica do estúdio (importar um GLB gerado pelo TRELLIS → renderizar sprites em 8 direções via blender --background --python → compor em um jogo 2.5D) mais preparação geral de recursos para o jogo. | **219 receitas · 10 domínios · 8 fases · 83/219 verificadas** |
| [docker-knowledge](docker-knowledge/) | A base de conhecimento por trás do produto gpu-container — como empacotar, medir e posicionar modelos de forma precisa em uma única GPU. | **160 descobertas · 6 domínios · 9 fases · 73/160 verificadas** |
| [godot-knowledge](godot-knowledge/) | Conhecimento atual e verificado de forma adversária do Godot 4 para a criação de um RPG tático 2.5D baseado em turnos. | **177 receitas · 6 domínios · 7 fases · 50/177 verificadas** |
| [model-knowledge](model-knowledge/) | Base de conhecimento verificada dos melhores MODELOS de IA generativa locais por finalidade (imagem / edição / controle / vídeo / 3D / áudio / LLM / legenda) para o equipamento RTX 5090 — com foco em licenças comerciais. | **129 modelos · 9 domínios · 19 fases · 126/129 verificados** |
| [rust-knowledge](rust-knowledge/) | Rust verificado para a criação do si-rpg-engine (essenciais, avançado e como o motor o utiliza: ABI WASM bruto, determinismo de ponto flutuante, estado e restauração do Rapier 0.35, bytes reproduzíveis) e uma primeira etapa para as sessões musicais do si-jam-sessions, com cada verificação de código executada pelo rustc 1.98.1 fixo. | **267 receitas · 27 domínios · 4 fases · 266/267 verificadas** |
| [sprite-motion-knowledge](sprite-motion-knowledge/) | A técnica portátil de animação de sprites para este equipamento | **246 receitas · 19 domínios · 8 fases · 170/246 verificadas** |
| [sprites-knowledge](sprites-knowledge/) | A técnica portátil de concept art → sprite 2.5D pronto para o jogo para este equipamento | **215 receitas · 8 domínios · 6 fases · 92/215 verificadas** |
| [tensor-engine-knowledge](tensor-engine-knowledge/) | Base de conhecimento verificada dos MOTORES que executam e treinam modelos de IA localmente no equipamento RTX 5090 (Blackwell / sm_120 / Windows). | **193 motores · 10 domínios · 17 fases · 134/193 verificados** |
| [training-knowledge](training-knowledge/) | Base de conhecimento verificada de técnicas de TREINAMENTO portáteis — métodos, receitas, valores de hiperparâmetros, conhecimento sobre conjuntos de dados e avaliação — para o treinamento de LoRAs / ajustes finos no equipamento único RTX 5090 (Blackwell / Windows / WSL2). A camada de "como treinar" entre os pesos (conhecimento do modelo) e o software (conhecimento do motor de tensor). | **204 técnicas · 13 domínios · 16 fases · 101/204 verificadas** |
| [vocology-knowledge](vocology-knowledge/) | Técnica de voz cantada: vocologia (fonte-filtro, registros, formante do cantor), prosódia musical vs. da fala, alinhamento de letras com notas, SVS controlável por partitura vs. geradores de músicas a partir de letras, avaliação de admissão/ensino. | **317 descobertas · 19 domínios · 13 fases · 214/317 verificadas** |
| [xrpl-knowledge](xrpl-knowledge/) | Base de conhecimento verificada do ECOSSISTEMA XRP Ledger para um desenvolvedor — recursos do protocolo, tipos de transação, padrões XLS, bibliotecas de cliente e ferramentas — cada um marcado com seu status atual na mainnet / emenda. Ecossistema completo: XRPL mainnet + Xahau/Hooks + a sidechain XRPL EVM + a camada institucional (RLUSD, conformidade). | **457 capacidades · 12 domínios · 10 fases · 362/457 verificadas** |

A tabela é gerada a partir de [`index.json`](index.json) por `shared/sync_readme_table.py`, e `python verify.py` falha se houver desvio. [`index.md`](index.md) é o mesmo mapa escrito para agentes, e [`index.html`](index.html) o renderiza.

Cada pasta KB contém seu banco de dados, um `catalog/` de páginas Markdown geradas por domínio, uma pasta `waves/` com o registro de pesquisa e verificação de cada fase e seu próprio `README.md`.

## Início rápido

```bash
git clone https://github.com/mcp-tool-shop-org/readouts
cd readouts
python verify.py
```

`verify.py` precisa do Python 3.10 ou mais recente e nada fora da biblioteca padrão. Os bancos de dados são arquivos SQLite comuns, portanto, qualquer cliente SQLite pode abri-los.

Pesquise em uma KB por meio de seu índice de texto completo e, em seguida, junte-o à entrada:

```sql
-- sqlite3 rust-knowledge/rust.db
SELECT r.name, r.verified
FROM recipes_fts f
JOIN recipes r ON r.id = f.rowid
WHERE recipes_fts MATCH 'rapier'
LIMIT 5;
```

Adicione `AND r.verified = 1` para manter apenas o que o verificador confirmou. O mesmo padrão funciona em todas as KBs. A tabela de entidades é nomeada em [`index.md`](index.md): `recipes`, `findings`, `models`, `engines`, `techniques` ou `capabilities`, cada uma com um índice `<table>_fts` correspondente. A maioria das KBs também tem uma visualização `v_recommended` (docker-knowledge e vocology-knowledge têm `v_load_bearing`). Essas visualizações selecionam com base no campo de recomendação de cada KB, e não com base em `verified`.

## Como uma entrada obtém `verified`

1. **Uma fase de pesquisa.** Uma linha de pesquisa por domínio escreve entradas, e cada entrada cita suas fontes como pares `{url, claim}`.
2. **Um verificador separado.** Um segundo agente, que nunca vê o raciocínio do pesquisador, verifica cada entrada em relação às páginas que ela cita e retorna um veredicto. Na maioria das fases, o verificador é da mesma família de modelos do pesquisador; algumas fases adicionam um membro de uma família diferente. O registro de cada fase indica qual.
3. **Uma definição de `verified`.** `verified = 1` somente quando esse veredicto externo assim o indicar ([`shared/verdicts.py`](shared/verdicts.py)). Uma entrada sem veredicto permanece não verificada. Trate-a como uma pista, não como um fato.
4. **Um compilador, quando houver código.** Cada verificação de código em rust-knowledge é compilada e, quando aplicável, executada por `rustc 1.98.1`. Uma receita cujo próprio exemplo falha na compilação nunca é verificada.

Cada iteração mantém seu registro na pasta `waves/` do KB: `dispatch.md` (o que foi solicitado e o que foi retornado), `research-raw.json` (o que foi carregado) e, quando a iteração tiver um, `verification.md` (o que o verificador e o compilador encontraram). KBs que mantêm um registro duradouro de verificação o mantêm em `verification/verdicts.json`.

## Direcione um agente para uma fatia

Dois índices de configuração evitam que um agente leia todo o corpus:

1. O arquivo raiz [`.claude/loadout/index.json`](.claude/loadout/index.json) direciona uma tarefa para o KB correto.
2. O arquivo `.claude/loadout/index.json` de cada KB o direciona para o domínio correto dentro desse KB.

```bash
npx @mcptoolshop/loadout-os validate .claude/loadout/index.json
npx @mcptoolshop/loadout-os resolve --project .
```

`resolve` também mescla sua própria camada global de configuração, se você tiver uma.

## Verifique o corpus você mesmo

`python verify.py` é a base do repositório. Ele verifica se os arquivos gerados são precisos em relação aos bancos de dados: se cada linha de texto completo corresponde à sua entrada, se nenhuma entrada verificada carece de uma fonte, se `verified` rastreia uma verificação externa, se a porta de entrada e a tabela deste arquivo README correspondem aos bancos de dados e se nenhum link relativo está quebrado.

- `FAIL` quebra um contrato ou fornece dados incorretos. Ele bloqueia a publicação.
- `WARN` é um defeito real que é conhecido, limitado e registrado.

Cada FAIL e WARN contém um código estável e uma dica para o próximo passo. `python verify.py --json` imprime um objeto JSON por verificação. O código de saída é 0 quando tudo está correto, 1 em caso de FAIL e 2 se a própria verificação falhar. O CI o executa em cada envio que altera o corpus.

## Segurança e modelo de ameaças

- **O que este repositório é:** dados. Ele contém bancos de dados SQLite, markdown, JSON e os scripts Python que os criaram. Nada é executado durante a instalação, e não há nada para instalar.
- **O caminho de leitura é local.** Consultar um banco de dados, `verify.py`, e os geradores (`regen.py`, `shared/gen_*.py`, o `load_db.py` de cada KB, `gen_catalog.py` e `gen_loadout.py`) leem arquivos neste diretório e gravam apenas arquivos derivados dentro dele. Eles não abrem nenhuma conexão de rede, não leem nenhuma credencial e não enviam nenhuma telemetria. `verify.py` não grava nada.
- **As ferramentas de pesquisa não são.** Os scripts mantidos como registro de como as iterações foram criadas (por exemplo, cada `verify_cloud.py`, o `openrouter_lane.py` do rust-knowledge e o `verifier/` do tensor-engine-knowledge) chamam um modelo: um daemon Ollama local ou OpenRouter com um `OPENROUTER_API_KEY` que você define no ambiente. Alguns também buscam as páginas que citam. Nenhuma chave é armazenada no repositório. `compile_oracle.py setup` baixa os pacotes Rust fixados por meio do cargo, uma vez. Nenhum deles é executado, a menos que você o execute.
- **Permissões:** acesso de leitura ao diretório; acesso de gravação apenas se você regenerar.
- **Nenhuma telemetria**, em nenhum lugar do repositório.
- **O que o conteúdo é:** notas de pesquisa com citações. Uma entrada não verificada é uma pista, não um fato. As notas de licença sobre modelos, conjuntos de dados e pacotes não são aconselhamento jurídico; leia a licença em si antes de enviar qualquer coisa.

Para relatar um problema, consulte [SECURITY.md](SECURITY.md).

## Mantenha-o

[MAINTENANCE.md](MAINTENANCE.md) é o manual de procedimentos: adicionar uma iteração ou um KB, executar uma verificação completa e as armadilhas que já custaram a alguém uma tarde. [CONVENTIONS.md](CONVENTIONS.md) descreve a estrutura que cada KB compartilha. O [manual](https://mcp-tool-shop-org.github.io/readouts/handbook/) explica em detalhes a consulta, a verificação e o direcionamento. As alterações são listadas em [CHANGELOG.md](CHANGELOG.md).

## Licença

[MIT](LICENSE)

---

Criado por <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
