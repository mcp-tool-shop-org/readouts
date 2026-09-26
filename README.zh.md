<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.md">English</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

readouts 是一系列知识库，内容是关于一家小型游戏工作室所使用的工具：Rust、Godot、Blender、精灵和动画制作、本地 AI 模型以及运行和训练这些模型的引擎、人声、GPU 容器和 XRP Ledger。

每个知识库（KB）都是一个 SQLite 数据库，包含一个全文索引。每个条目都会注明其来源，记录产生该条目的研究阶段，并带有 `verified` 标志。只有来自独立验证者的结论才能设置该标志；作者对其作品的个人意见不予考虑。

这个名称来源于 [loadout-os](https://github.com/mcp-tool-shop-org/loadout-os)，它会“加载”适用于特定任务的正确知识。readouts 则是它所读取的内容。

## 知识库

| KB | 内容 | 状态 |
|----|------|--------|
| [blender-knowledge](blender-knowledge/) | 当前，针对工作室的无头精灵渲染流水线，采用基于 Web 的 Blender 4.x 实践（导入 TRELLIS 生成的 GLB → 通过 blender --background --python 渲染 8 个方向的精灵 → 合成成 2.5D 游戏），以及通用的游戏资源准备。 | **219 条配方 · 10 个领域 · 8 个阶段 · 83/219 已验证** |
| [docker-knowledge](docker-knowledge/) | gpu-container 产品背后的知识库——如何以诚实的方式打包、衡量和放置模型到单个 GPU 上。 | **160 条发现 · 6 个领域 · 9 个阶段 · 73/160 已验证** |
| [godot-knowledge](godot-knowledge/) | 当前，用于构建 2.5D 回合制战术 RPG 的、经过对抗验证的 Godot 4 开发知识。 | **177 条配方 · 6 个领域 · 7 个阶段 · 108/177 已验证** |
| [model-knowledge](model-knowledge/) | 针对 RTX 5090 平台的、按用途划分的最佳本地生成式 AI 模型（图像/编辑/控制/视频/3D/音频/LLM/字幕）的已验证知识库——首先考虑商业许可。 | **129 个模型 · 9 个领域 · 19 个阶段 · 126/129 已验证** |
| [rust-knowledge](rust-knowledge/) | 用于构建 si-rpg-engine（基本、高级以及引擎如何使用它：原始 WASM ABI、浮点数确定性、Rapier 0.35 状态和恢复、可重现字节）的已验证 Rust 代码，以及 si-jam-sessions 音乐法律的第一层，所有代码检查均由固定的 rustc 1.98.1 运行。 | **280 条配方 · 27 个领域 · 5 个阶段 · 279/280 已验证** |
| [sprite-motion-knowledge](sprite-motion-knowledge/) | 适用于该平台的、可移植的精灵动画制作技术 | **246 条配方 · 19 个领域 · 8 个阶段 · 170/246 已验证** |
| [sprites-knowledge](sprites-knowledge/) | 适用于该平台的、可移植的概念艺术 → 游戏可用 2.5D JRPG 精灵制作技术 | **215 条配方 · 8 个领域 · 6 个阶段 · 182/215 已验证** |
| [tensor-engine-knowledge](tensor-engine-knowledge/) | 在 RTX 5090 平台上运行和训练 AI 模型的引擎的已验证知识库（Blackwell / sm_120 / Windows）。 | **193 个引擎 · 10 个领域 · 17 个阶段 · 134/193 已验证** |
| [training-knowledge](training-knowledge/) | 可移植的训练技术的已验证知识库——方法、配方、超参数值、数据集和评估知识——用于在单个 RTX 5090 平台上训练 LoRA/微调模型（Blackwell / Windows / WSL2）。这是连接权重（模型知识）和软件（张量引擎知识）的训练方法。 | **204 种技术 · 13 个领域 · 16 个阶段 · 101/204 已验证** |
| [vocology-knowledge](vocology-knowledge/) | 人声制作：声学（声源-滤波器、音域、歌手共振峰）、音乐与语音韵律、歌词与音符对齐、可控制乐谱的 SVS 与歌词到歌曲生成器、录取/教学评估。 | **317 条发现 · 19 个领域 · 13 个阶段 · 214/317 已验证** |
| [xrpl-knowledge](xrpl-knowledge/) | 针对构建者的、XRP Ledger 生态系统的已验证知识库——协议功能、交易类型、XLS 标准、客户端库和工具——每个条目都标记了其当前主网/修订状态。整个生态系统：XRPL 主网 + Xahau/Hooks + XRPL EVM 侧链 + 机构层（RLUSD、合规性）。 | **457 种能力 · 12 个领域 · 10 个阶段 · 362/457 已验证** |

该表由 [`index.json`](index.json) 生成，由 `shared/sync_readme_table.py` 处理，如果发生偏差，`python verify.py` 将会失败。[`index.md`](index.md) 是为代理编写的相同映射，[`index.html`](index.html) 用于渲染它。

每个 KB 文件夹都包含其数据库、一个包含每个领域生成的 Markdown 页面的 `catalog/` 文件、一个包含每个阶段的研究和验证记录的 `waves/` 文件夹，以及它自己的 `README.md`。

## 快速入门

```bash
git clone https://github.com/mcp-tool-shop-org/readouts
cd readouts
python verify.py
```

`verify.py` 需要 Python 3.10 或更高版本，并且不需要标准库之外的任何内容。数据库是普通的 SQLite 文件，因此任何 SQLite 客户端都可以打开它们。

通过其全文索引搜索一个 KB，然后将其与条目连接：

```sql
-- sqlite3 rust-knowledge/rust.db
SELECT r.name, r.verified
FROM recipes_fts f
JOIN recipes r ON r.id = f.rowid
WHERE recipes_fts MATCH 'rapier'
LIMIT 5;
```

将 `AND r.verified = 1` 添加到搜索条件中，以仅保留验证者确认的内容。相同的模式适用于每个 KB。实体表在 [`index.md`](index.md) 中命名：`recipes`、`findings`、`models`、`engines`、`techniques` 或 `capabilities`，每个表都有一个匹配的 `<table>_fts` 索引。大多数 KB 还有一个 `v_recommended` 视图（docker-knowledge 和 vocology-knowledge 具有 `v_load_bearing`）。这些视图根据每个 KB 自己的推荐字段进行选择，而不是根据 `verified`。

## 一个条目如何获得 `verified`

1. **一个研究阶段。** 每个研究方向都会编写一个领域的条目，并且每个条目都会引用其来源，格式为 `{url, claim}` 对。
2. **一个独立的验证者。** 第二个代理（它永远不会看到研究者的推理过程）会检查每个条目是否与它引用的页面一致，并返回一个结论。在大多数阶段，验证者与研究者来自相同的模型家族；有些阶段会增加来自不同家族的代理。每个阶段的记录都会说明这一点。
3. **一个 `verified` 的定义。** 只有当外部结论为真时，才会设置 `verified = 1` ([`shared/verdicts.py`](shared/verdicts.py))。没有结论的条目将保持未验证状态。将其视为一个线索，而不是一个事实。
4. **一个编译器，如果存在代码。** rust-knowledge 中的每个代码检查都会被编译，并且在适用时会运行，由 `rustc 1.98.1` 运行。如果一个配方的示例无法通过编译器，则该配方将永远不会被验证。

每个波次的记录都保存在知识库的 `waves/` 文件夹中：`dispatch.md`（提问的内容和返回的结果）、`research-raw.json`（加载的内容），以及波次拥有的 `verification.md`（验证器和编译器发现的内容）。保存持久性验证记录的知识库将其保存在 `verification/verdicts.json` 中。

## 将一个代理路由到一个切片

两个加载索引可以防止代理读取整个语料库：

1. 根目录 [`.claude/loadout/index.json`](.claude/loadout/index.json) 将任务路由到正确的知识库。
2. 每个知识库自己的 `.claude/loadout/index.json` 将其路由到该知识库内的正确领域。

```bash
npx @mcptoolshop/loadout-os validate .claude/loadout/index.json
npx @mcptoolshop/loadout-os resolve --project .
```

`resolve` 还会合并您自己的全局加载层（如果存在）。

## 自行检查语料库

`python verify.py` 是仓库的基础。它检查生成的文件是否准确地反映了数据库：每个全文 rowid 是否与其对应的条目关联，没有经过验证的条目是否缺少来源，`verified` 是否可追溯到外部验证，前置界面和此 README 文件中的表格是否与数据库匹配，以及是否存在失效的相对链接。

- `FAIL` 违反了协议或提供了错误的数据。它会阻止发布。
- `WARN` 是一个已知的、可控的和已记录的实际缺陷。

每个 FAIL 和 WARN 都包含一个稳定的代码和一个关于下一步操作的提示。`python verify.py --json` 为每个检查打印一个 JSON 对象。如果一切正常，退出代码为 0；如果出现 FAIL，则为 1；如果检查本身崩溃，则为 2。CI 会在每次更改语料库时运行它。

## 安全性和威胁模型

- **此仓库包含的内容：**数据。它包含 SQLite 数据库、Markdown、JSON 以及用于构建这些数据库的 Python 脚本。安装时没有任何程序运行，也没有任何需要安装的内容。
- **读取路径是本地的。** 查询数据库、`verify.py` 以及生成器（`regen.py`、`shared/gen_*.py`、每个知识库的 `load_db.py`、`gen_catalog.py` 和 `gen_loadout.py`）读取此检出目录中的文件，并仅写入派生的文件到其中。它们不打开任何网络连接，不读取任何凭据，也不发送任何遥测数据。`verify.py` 根本不写入任何内容。
- **研究工具不是。** 作为记录波次生成方式的脚本（例如，每个 `verify_cloud.py`、rust-knowledge 的 `openrouter_lane.py` 以及 tensor-engine-knowledge 的 `verifier/`）会调用一个模型：本地 Ollama 守护程序，或 OpenRouter，并使用您在环境中设置的 `OPENROUTER_API_KEY`。有些还会获取它们引用的页面。没有密钥存储在仓库中。`compile_oracle.py setup` 通过 cargo 下载已固定的 Rust 包，一次性完成。除非您运行它，否则这些都不会运行。
- **权限：**读取检出目录的权限；如果需要重新生成，则具有写入权限。
- **在仓库中的任何位置都没有遥测数据。**
- **内容：**带有引用的研究笔记。未经验证的条目是一个线索，而不是事实。关于模型、数据集和包的许可说明不是法律建议；在发布任何内容之前，请阅读许可本身。

如需报告问题，请参阅 [SECURITY.md](SECURITY.md)。

## 维护

[MAINTENANCE.md](MAINTENANCE.md) 是操作手册：添加一个波次或知识库、运行验证扫描，以及已经让某人浪费了一个下午的陷阱。[CONVENTIONS.md](CONVENTIONS.md) 描述了每个知识库都具有的结构。 [handbook](https://mcp-tool-shop-org.github.io/readouts/handbook/) 详细介绍了查询、验证和路由。更改记录在 [CHANGELOG.md](CHANGELOG.md) 中。

## 许可证

[MIT](LICENSE)

---

由 <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a> 构建
