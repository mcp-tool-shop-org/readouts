<p align="center">
  <a href="README.md">English</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

readouts は、小規模なゲームスタジオの基盤となるツールに関する知識ベースの集合です。具体的には、Rust、Godot、Blender、スプライトとアニメーションの作成、ローカルAIモデル、およびそれらを実行およびトレーニングするためのエンジン、歌声、GPUコンテナ、XRP Ledgerなどです。

各知識ベース（KB）は、全文インデックスを持つSQLiteデータベース1つです。各エントリは、その情報源を明記し、そのエントリを作成した調査の段階を記録し、`verified`フラグを持ちます。このフラグは、別の検証者からの検証結果によってのみ設定できます。作成者自身の意見は考慮されません。

この名前は、特定のタスクに必要な知識を「ロード」する[loadout-os](https://github.com/mcp-tool-shop-org/loadout-os)に由来します。readoutsは、そこから読み取られる情報です。

## 知識ベース

| KB | 内容 | ステータス |
|----|------|--------|
| [blender-knowledge](blender-knowledge/) | 現在の、スタジオのヘッドレススプライトレンダリングパイプライン（TRELLISで生成されたGLBをインポート→Blenderで8方向のスプライトをレンダリング（--background --pythonオプションを使用）→2.5Dゲームに合成）および一般的なゲームアセットの準備に使用される、WebベースのBlender 4.xの実践的な内容。 | **219件のレシピ・10のドメイン・8つの段階・83/219件が検証済み** |
| [docker-knowledge](docker-knowledge/) | GPUコンテナ製品の基盤となる知識ベース。モデルをパッケージ化し、測定し、1つのGPUに配置する方法。 | **160件の調査結果・6つのドメイン・9つの段階・73/160件が検証済み** |
| [godot-knowledge](godot-knowledge/) | 現在の、2.5Dターン制タクティカルRPGを構築するための、敵対的に検証されたGodot 4の開発知識。 | **177件のレシピ・6つのドメイン・7つの段階・108/177件が検証済み** |
| [model-knowledge](model-knowledge/) | RTX 5090リグで使用する、目的別の最高のローカル生成AIモデル（画像/編集/制御/ビデオ/3D/オーディオ/LLM/キャプション）に関する、検証済みの知識ベース。商用ライセンスを優先。 | **129個のモデル・9つのドメイン・19の段階・126/129個が検証済み** |
| [rust-knowledge](rust-knowledge/) | si-rpg-engineを構築するための、検証済みのRust。必須要素、高度な機能、およびエンジンがそれを使用する方法（生のwasm ABI、浮動小数点数の決定性、Rapier 0.35の状態と復元、再現可能なバイト）と、si-jam-sessionsの音楽法に関する最初の段階。すべてのコードチェックは、固定バージョンのrustc 1.98.1によって実行されます。 | **267件のレシピ・27のドメイン・4つの段階・266/267件が検証済み** |
| [sprite-motion-knowledge](sprite-motion-knowledge/) | このリグで使用する、スプライトをアニメーション化するための移植可能な手法。 | **246件のレシピ・19のドメイン・8つの段階・170/246件が検証済み** |
| [sprites-knowledge](sprites-knowledge/) | このリグで使用する、コンセプトアートからゲームで使用できる2.5D JRPGスプライトを作成するための移植可能な手法。 | **215件のレシピ・8つのドメイン・6つの段階・182/215件が検証済み** |
| [tensor-engine-knowledge](tensor-engine-knowledge/) | RTX 5090（Blackwell / sm_120 / Windows）リグでローカルにAIモデルを実行およびトレーニングするためのエンジンに関する、検証済みの知識ベース。 | **193個のエンジン・10のドメイン・17の段階・134/193個が検証済み** |
| [training-knowledge](training-knowledge/) | 単一のRTX 5090（Blackwell / Windows / WSL2）リグでLoRA / ファインチューニングをトレーニングするための、移植可能なトレーニング手法（方法、レシピ、ハイパーパラメータ値、データセットと評価に関する知識）に関する、検証済みの知識ベース。重み（モデル知識）とソフトウェア（テンソルエンジン知識）の間の、トレーニング方法に関する知識。 | **204個の技術・13のドメイン・16の段階・101/204個が検証済み** |
| [vocology-knowledge](vocology-knowledge/) | 歌声に関する知識：音声学（音源-フィルター、レジスター、シンガーのフォルマント）、音楽的なプロソディと発話のプロソディ、歌詞と音符の対応、スコアで制御可能なSVSと歌詞から曲を生成するツールの比較、評価と指導。 | **317件の調査結果・19のドメイン・13の段階・214/317件が検証済み** |
| [xrpl-knowledge](xrpl-knowledge/) | XRP Ledgerエコシステムに関する、検証済みの知識ベース。プロトコル機能、トランザクションタイプ、XLS標準、クライアントライブラリとツールなど。それぞれに、現在のメインネット/修正ステータスがタグ付けされています。エコシステム全体：XRPLメインネット + Xahau/Hooks + XRPL EVMサイドチェーン + 機関レイヤー（RLUSD、コンプライアンス）。 | **457個の機能・12のドメイン・10の段階・362/457個が検証済み** |

このテーブルは、[`index.json`](index.json)から`shared/sync_readme_table.py`によって生成され、`python verify.py`が変更された場合、エラーが発生します。[`index.md`](index.md)は、エージェント向けに記述された同じマップであり、[`index.html`](index.html)はそれをレンダリングします。

各KBフォルダーには、データベース、生成されたマークダウンページのドメインごとの`catalog/`、各段階の調査と検証の記録を含む`waves/`フォルダー、および独自の`README.md`が含まれています。

## クイックスタート

```bash
git clone https://github.com/mcp-tool-shop-org/readouts
cd readouts
python verify.py
```

`verify.py`には、Python 3.10以降が必要であり、標準ライブラリ以外のものは必要ありません。データベースは通常のSQLiteファイルであるため、任意のSQLiteクライアントで開くことができます。

各KBの全文インデックスを使用して検索し、次にエントリに結合します。

```sql
-- sqlite3 rust-knowledge/rust.db
SELECT r.name, r.verified
FROM recipes_fts f
JOIN recipes r ON r.id = f.rowid
WHERE recipes_fts MATCH 'rapier'
LIMIT 5;
```

検証者が確認した情報のみを保持するために、`AND r.verified = 1`を追加します。同じパターンは、すべてのKBで機能します。エンティティテーブルの名前は、[`index.md`](index.md)に記載されています：`recipes`、`findings`、`models`、`engines`、`techniques`または`capabilities`。それぞれに、対応する`<table>_fts`インデックスがあります。ほとんどのKBには、`v_recommended`ビューもあります（docker-knowledgeとvocology-knowledgeには、`v_load_bearing`があります）。これらのビューは、各KBの独自の推奨フィールドに基づいて選択され、`verified`に基づいて選択されません。

## エントリが`verified`を獲得する方法

1. **調査の段階。** 各ドメインで1つの調査チームがエントリを作成し、各エントリは、その情報源を`{url, claim}`ペアとして引用します。
2. **別の検証者。** 調査者の推論を見たことがない2番目のエージェントが、各エントリを引用されたページと比較し、検証結果を返します。ほとんどの段階では、検証者は調査者と同じモデルファミリーに属します。一部の段階では、別のファミリーからのエージェントが追加されます。各段階の記録には、どの検証者が使用されたかが記載されています。
3. **`verified`の定義。** `verified = 1`は、外部の検証結果が肯定的な場合にのみ行われます（[`shared/verdicts.py`](shared/verdicts.py)）。検証結果がないエントリは、未検証のままになります。未検証のエントリは、事実ではなく、あくまで手がかりとして扱ってください。
4. **コードがある場合は、コンパイラ。** rust-knowledgeのすべてのコードチェックはコンパイルされ、コンパイルされた場合は実行されます（`rustc 1.98.1`）。独自の例がコンパイラでエラーになるレシピは、検証されません。

各ウェーブは、KBの`waves/`フォルダーにその記録を保持します：`dispatch.md`（質問された内容と返された内容）、`research-raw.json`（ロードされた内容）、そして、ウェーブに該当する場合、`verification.md`（検証者とコンパイラが見つけた内容）。永続的な検証記録を保持するKBは、それを`verification/verdicts.json`に保持します。

## エージェントを1つのスライスにルーティングします

2つのロードアウトインデックスは、エージェントがすべてのコーパスを読み込むのを防ぎます。

1. ルートの[`.claude/loadout/index.json`](.claude/loadout/index.json)は、タスクを適切なKBにルーティングします。
2. 各KB独自の`.claude/loadout/index.json`は、それをそのKB内の適切なドメインにルーティングします。

```bash
npx @mcptoolshop/loadout-os validate .claude/loadout/index.json
npx @mcptoolshop/loadout-os resolve --project .
```

`resolve`は、独自のグローバルロードアウトレイヤーがある場合、それもマージします。

## ご自身でコーパスを確認してください

`python verify.py`は、リポジトリの基盤です。生成されたファイルがデータベースに対して正しいかどうかをチェックします。具体的には、すべての全文行IDがそれぞれのエントリに結合されているか、検証済みのエントリにソースが欠けていないか、`verified`が外部の検証にトレースされるか、フロントドアとこのREADMEのテーブルがデータベースと一致するか、相対リンクが壊れていないかを確認します。

- `FAIL`は、契約に違反するか、誤ったデータを提供します。これにより、公開がブロックされます。
- `WARN`は、既知で、範囲が限定され、記録された実際の欠陥です。

すべてのFAILとWARNには、安定したコードと次のステップのヒントが含まれます。`python verify.py --json`は、各チェックごとに1つのJSONオブジェクトを出力します。正常終了の場合は終了コードは0、FAILの場合は1、チェック自体がクラッシュした場合は2です。CIは、コーパスを変更するたびにこれを実行します。

## セキュリティと脅威モデル

- **このリポジトリの内容:** データです。SQLiteデータベース、マークダウン、JSON、およびそれらを構築するPythonスクリプトが含まれています。インストール時に何も実行されず、インストールするものもありません。
- **読み取りパスはローカルです。** データベースへのクエリ、`verify.py`、およびジェネレーター（`regen.py`、`shared/gen_*.py`、各KBの`load_db.py`、`gen_catalog.py`、および`gen_loadout.py`）は、このチェックアウト内のファイルを読み取り、派生ファイルのみをその中に書き込みます。ネットワーク接続を開いたり、資格情報を読み取ったり、テレメトリを送信したりすることはありません。`verify.py`は何も書き込みません。
- **調査ツールはそうではありません。** ウェーブがどのように作成されたかの記録として保存されているスクリプト（たとえば、各`verify_cloud.py`、rust-knowledgeの`openrouter_lane.py`、およびtensor-engine-knowledgeの`verifier/`）は、モデルを呼び出します。ローカルのOllamaデーモン、または環境で設定した`OPENROUTER_API_KEY`を使用するOpenRouterです。一部は、引用したページもフェッチします。キーはリポジトリに保存されていません。`compile_oracle.py setup`は、cargoを通じて、ピン留めされたRustクレートを一度ダウンロードします。これらのうち、実際に実行しない限り、どれも実行されません。
- **権限:** チェックアウトへの読み取りアクセス。再生成する場合のみ、書き込みアクセス。
- **リポジトリ内のどこにもテレメトリはありません。**
- **コンテンツの内容:** 引用付きの研究ノートです。検証されていないエントリは、事実ではなく、手がかりです。モデル、データセット、およびクレートに関するライセンスノートは法的助言ではありません。何かを配布する前に、ライセンス自体を読んでください。

問題を報告するには、[SECURITY.md](SECURITY.md)を参照してください。

## 保守

[MAINTENANCE.md](MAINTENANCE.md)は、運用手順書です。ウェーブまたはKBの追加、検証スイープの実行、そして、すでに誰かの午後の時間を奪ったトラップについて説明しています。[CONVENTIONS.md](CONVENTIONS.md)は、すべてのKBが共有する構造について説明しています。[handbook](https://mcp-tool-shop-org.github.io/readouts/handbook/)では、クエリ、検証、およびルーティングについてより詳細に説明します。変更は[CHANGELOG.md](CHANGELOG.md)にリストされています。

## ライセンス

[MIT](LICENSE)

---

<a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>によって作成されました。
