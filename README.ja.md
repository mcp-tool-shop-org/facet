<p align="center">
  <a href="README.md">English</a> | <a href="README.zh.md">中文</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
</p>

<p align="center">
  <img src="https://raw.githubusercontent.com/mcp-tool-shop-org/brand/main/logos/facet/readme.png" alt="facet" width="400">
</p>

<p align="center">
  <a href="https://github.com/mcp-tool-shop-org/facet/actions/workflows/ci.yml"><img src="https://github.com/mcp-tool-shop-org/facet/actions/workflows/ci.yml/badge.svg" alt="CI"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/license-MIT-blue" alt="MIT License"></a>
  <a href="docs/experiments/"><img src="https://img.shields.io/badge/record-spec%20%E2%86%92%20report%20%E2%86%92%20ruling-8a6f3f" alt="The record"></a>
  <a href="https://mcp-tool-shop-org.github.io/facet/"><img src="https://img.shields.io/badge/landing%20page-live-2ea043" alt="Landing page"></a>
</p>

<p align="center">
  <strong>A styled 2D concept goes in. A textured 3D asset comes out.</strong><br>
  Local hardware end to end · no non-commercial licence anywhere in the chain
</p>

---

スタイルは**アセットに適用**され、テクスチャ空間で行われます。ビューごとに描画されたものを後でつなぎ合わせることはありません。形状を強調した粘土モデルをパイプラインに入力すると、そのメッシュのスタイライズされた参照から色を取得したテクスチャ付きメッシュが出力されます。参照では見ることができなかった部分は、マスク処理されたインペイントブラシとサーフェスを認識する拡大によって補完されます。

この問題の2つの側面、つまりポリゴンと、それらが表現する必要がある表面にちなんで名付けられました。

## インストール

パイプライン自体は、入力するパスに対して実行する一連のローカルスクリプトです。リポジトリをクローンし、[Getting Started](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/) を参照してください。

**レコードインデックスはパッケージとして提供**されるため、アシスタントは証拠の追跡を読み込む代わりにクエリを実行できます。

```bash
npx @mcptoolshop/facet          # zero-prerequisite; verified binary, no Python needed
```

これには2つのコマンドが含まれています。1つは、標準入出力MCPサーバー（4つの脚を持つ検証が拒否的な健全な表面として機能する6つのツール）、もう1つは`facet-mcp`（`facet-index` / `build` / `verify` / `q` / `claims`）です。チェックアウト内から実行します。`--db`は別のインデックスを指定します。

⚠ **`pip install facet-mcp`は、v0.3.0までのすべてのリリースバージョンで問題があり、v0.3.1で修正されました。**ホイールは`facet_index`を最上位モジュールとしてインストールするため、v0.3.0まで、レコードの位置を`<venv>/Lib`（コーパスもインデックスも含まない）および`build`、`claims`、`q`に対して解決していました。また、`--db`がない場合、これらはすべて失敗しました。**v0.3.0以前のバージョンでは、上記の`npx`バイナリを使用してください。**

v0.3.1以降は、それを仮定するのではなく、**レコードをテストすることによってルートが解決されます。**チェックアウト内からいずれかのコマンドを実行すると、見つかります。それ以外の場所から実行すると、**`4` REFUSED**と表示され、試した両方のディレクトリと検索した両方のマーカーが表示されます。
`$FACET_INDEX_DB`は現在、両方のコマンドによって読み取られ、*コーパス*ではなく、どの*インデックス*を選択するかを決定します。`main`から構築され、クリーンな仮想環境にインストールされたホイールで測定しました。[E24](docs/experiments/E24-ruling.md)。

*このブロックは2回修正されました。最初に「pipx install facet-mcp #またはPythonパッケージを直接`, until v0.3.0's read-back ran a **verb** instead of `--help」と記述されていました。次に、ホイールは「`q`と`claims`でのみ機能する」と述べられていましたが、**`claims`も機能しませんでした**。これはE24が実行して確認したものです。両方の修正は[known-defects.md](docs/known-defects.md)に測定値とともに記載されています。*

## 現在の状況

**ゼロクレジットで、4つの被験者クラスにわたる4つのアセットが承認されました。**それぞれは、ディレクターによって独自のズームレベル（GLBまたはフルサイズのシート）で評価され、特定のメトリックが閾値を超えたわけではありませんでした。

| 被験者 | クラス | 承認済み | 参照/ブラシ/拡大 |
|---|---|---|---|
| **Character (W3)** | ヒューマノイド | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | 乗り物、細いリギング | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | 獣、翼膜 | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | 小道具、ほぼ2D、グレーのグラデーション | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

共有されるのは有効なテクセルであり、**それらは被験者間で比較できません。**船はほとんど自身を目の高さから隠し、動物は半分を隠します。それぞれを事前に登録された範囲と比較して評価すると、**86〜93％**になります。行間の違いはジオメトリであり、回帰ではありません。[完全な数値と分母](docs/handbook/subjects.md)。

**これはパイプラインであり、単一のキャラクタージェネレーターではありません。**8つの名前付き要素で仕様に矛盾させると、プロンプトが**8/8**で勝利します。中央値ΔEは46.3となり、5つの固定コントロールでは6.2でした。一方、図形は同じ人物です。構造はメッシュと制御によって保持され、名前付き属性はプロンプトに依存します。

## パイプライン

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

各段階とその理由を説明します。[ハンドブック](docs/handbook/index.md)。

## どのように機能するか

6つの発見があり、それぞれに実験のコストがかかり、それぞれがその生成元となった被験者を超えて一般化されます。[詳細な説明と測定値](docs/findings.md)。

- **最初に形状を、次にスタイルを。**再構築ツールは表面ノイズをジオメトリとして読み取ります。意図的に誇張された平面を持つクリーンで彫刻のような粘土モデルの方が、より優れたトポロジーになります。スタイライズされたツインは同時に生成され、カラー参照になります。
- **顔のフレームを作成し、顔を取得します。**バストクロップを行うと、**3.1〜4.5倍**多くのポリゴンが頭部に配置され、その違いは構造的です。分離されたまぶた、眉間の溝、モデル化された鼻腔などです。これは単なるぼかしの改善ではありません。
- **ツインはキャラクターではなくメッシュに属します。**ツインを複数のメッシュで使用すると、カバレッジが**62％から22.7％**に低下します。これは、腕がモデルの横の空中に投影されるためです。テクスチャを適用する予定のメッシュから、常にツインを生成してください。
- **アイデンティティはプロンプトに属します。**プロンプトで名前が指定されていないカノン要素は、偶然に現れ、同じように消えます。これは、壊れたControlNetのノイズによって金色の膝当てが画像に表示されるようになったときに測定されました。
- **ジオメトリを尋ね、閾値を使用しないでください。**キー処理されたマスクを正確なレイキャストシルエットに置き換えると、有効なテクセルの参照カバレッジが**28.4％から39.1％**に増加しました。これは厳密に追加であり、拡散もGPUも使用しません。コーナー中央のキー処理はここで3回失敗し、廃止されました。
- **カメラで見ることができないものをアトラスから削除し、メッシュからは決して削除しないでください。**アトラステクセルの49％が外部からは見えません。これらの面を除外すると、補間が68％削減されます。除外するのではなく削除することで、検出できるだけでなく、失敗を不可能にします。

## 解決されていない問題

名前と測定値は、脚注ではなく、最初のページに記載されています。[すべてコードにあります](docs/known-defects.md)。

- **ブレードバンドは、すべての8つのカメラでステージ1の参照に対して0.00%の影響を与えます。** スチールがグレーの背景に配置され、キー自体の閾値と正確に一致します。この組み合わせにより、55.72%の効果が得られます。
- **ストロークの継ぎ目は均一ではありません。** 起点の境界線は、通常のテクスチャの変化よりも5.5倍大きくなっています。ディレクターが指定した領域は、9.5倍大きくなっています。
- **関連性のないアトラスアイランド間で拡散が発生します。** 74.9%の拡大されたテクセルが、別の島から色を取得します。その距離の中央値は1.0の高さで0.177です。
- **このルート上のすべての再構成は、中空の二重壁構造です。** 壁は約2ボクセルです。単一のオブジェクトに対して有効な体積予測子は存在しません。

## このリポジトリの実行方法

このプロジェクトにおける規律は、パイプラインと同様に重要な要素であり、それには理由があります。以前の段階では、10回のセッションが実施され、各セッションで独自の出力を評価し、次のセッションで確立された事実として扱われる結論をまとめました。しかし、そのループの中で検証可能なものは何もありませんでした。

- **作業前に仕様を定め、作業後に報告を行い、最後に判断を下す。** 実験を設計するセッションは、自身の結果を評価することはありません。26件の実験が[記録](docs/experiments/)にあります。
- **修正は、それを覆した測定値の隣に配置されます。** 静かな削除として行われることはありません。最初のセッションだけで、6つの既存の主張が誤りであることが判明し、それらすべては、置き換えられたものと並んで今でも確認できます。
- **失敗は、その理由とともにリポジトリに残ります。** [`tools/superseded/`](docs/tools.md) はアーカイブではありません。誰でもこれらのツールを実行し、同じように失敗する様子を観察できます。
- **否定的な結果は完全な成功です。** 報告され、閉じられ、特定の数値に調整されることはありません。
- **テストは、コードに触れるコミットと関連付けられます。** 2つの異なる環境で684件のテストが合格し、675件の隔離されたテストに対してパスベースのCIが実行されます。
- **記録は検索可能です。** SQLite + FTS5インデックスを使用して、すべての履歴を検証します（4つの異なる環境で）。その結果、文章に誤りがあった3つの箇所を発見しました。これは、記録自体を数えることで行われました。

## すべてがどこにあるか

| | |
|---|---|
| **[ハンドブック](docs/handbook/index.md)** | ガイド — 各段階のルート、対象、プロファイルシステム |
| **[記録](docs/experiments/)** | 26件の実験：仕様、報告、判断、および測定前に述べられたすべての予測 |
| **[ルートで得られた知見](docs/findings.md)** | 永続的な知見と苦労して得られたルール（すべて） |
| **[各ツールのステータス](docs/tools.md)** | 動作するもの、廃止されたもの、およびそれぞれの証拠 |
| **[既知の欠陥](docs/known-defects.md)** | 解決されていないすべての問題。コード内で測定され、特定されています。 |
| **[実際に起こった一連の流れ](docs/arc-history.md)** | 時系列の履歴。修正はそのまま残っています。 |
| **[CLAUDE.md](CLAUDE.md)** | ここで働く方法 — 役割、ルール、およびそれぞれのコスト |

## ライセンスに関する事項

すべての段階はローカルで実行され、商用利用においても問題ありません。SDXL (OpenRAIL++)、MV-Adapter (オープン)、open3d (Apache-2.0)、spandrel (MIT)、RealESRGAN anime6B (BSD-3)、Blender、numpy、scipy、trimeshを使用しています。

意図的に除外されたもの（理由とともに）：**nvdiffrast**（非商用 — ここでは構造的なトリップワイヤーによって強制され、認証によるものではありません）、**Hunyuan3D-Paint**（EU、英国、および韓国でのライセンスが無効）、**MVPaint**および**TEXGen**（ライセンスが全く存在しない）、および**UltraSharp / SUPIR / StableSR**（非商用のアップスケーラー）。

## 信頼と脅威モデル

facetは完全にローカルマシン上で実行されます。すべてのツールは、コマンドラインで指定するパスに対して呼び出すスクリプトです。したがって、重要な質問は、「このアプリはどのような権限を要求するか」ではなく、「これらのスクリプトがあなたのマシンに何をするか」です。測定によって回答され、すべてのスイープは再実行可能です。完全なポリシーは[SECURITY.md](SECURITY.md)に記載されています。

- **アクセスされるデータ：** コマンドラインで指定するパスにあるローカルディスク上のメッシュ、テクスチャ、画像、およびJSONファイル。さらに、`docs/index/facet.db`も含まれます。これは*派生した*ものです。このリポジトリにすでに存在していたファイル以外のものは含まれておらず、`facet_index.py build`によって最初から再生成されます。
- **アクセスされないデータ：** 認証情報は一切使用しません。ここでは、トークン、キー、またはパスワードを読み取ったり、保存したり、送信したりするものがなく、ツリー内にそれらの要素も存在しません。プロバイダーのプレフィックスが付いたキー、GitHub PAT、Slackトークン、AWSキーID、秘密鍵ブロック、ベアラートークン、およびインラインの`api_key`/`password`割り当てについてスキャンしましたが、**一致するものはありませんでした**。また、認証情報のようなファイルも追跡されていません。
- **テレメトリーは行われません。** 収集も送信もしません。オプトアウトする必要がないのは、オプトアウトするものが何もないからです。
- **ネットワークからのデータ送信：** 34個のツールのうち2つがソケットを開きます。それは`restylize_views.py`と`texpass_brush.py`であり、どちらもComfyUI HTTP API（`--host`）を呼び出します。デフォルトは`127.0.0.1:8188`です。それ以外の`tools/`に含まれるものは、ネットワーク呼び出しを行いません。
- **権限：** 通常のユーザー。昇格やサービスインストール、システム設定またはレジストリへの書き込みはありません。

３つの鋭い点が明らかになる一方で、単に安心感だけを列挙したセキュリティに関する注意書きは脅威モデルではないため、それらは主張されることはありません。**ファイル操作はサンドボックス化されていません**（ツールは、その引数で指定された場所に書き込みます）。**多くのツールやドキュメントには絶対的なローカルパスが組み込まれています**—26個のファイルに114件の記述があります。これは秘密情報ではなく、単一のマシンの構成を明らかにするものであり、ほとんどのツールを変更せずに他の場所で実行できない理由でもあります。また、**予期しないエラーは、公開されていない34個の研究スクリプトにおいて、Pythonのトレースバックとして表示されます**。ゲートはありません（`--debug`）。意図的な停止は、それをトリガーした測定値を伝えるメッセージ（`ANDON:`）です。これが研究用機器の契約であり、[SHIP_GATE.md](SHIP_GATE.md)には、それが十分に機能しなくなる正確な時期が記録されています。これは、２つのコマンドにおいて、インストール時に0.2.0で発生しました：`facet-index`と`facet-mcp`はそれぞれ、`0`（正常）/ `1`（ユーザーエラー）/ `2`（実行時エラー）を返します。そして、[E22](docs/experiments/E22-ruling.md)以降、トリガーされたゲートまたは失敗したゲート（`verify`）に対しては、**`4`（拒否）**となります。これは、ツールが動作し、実行時エラーではなく、続行しないように指示していることを意味します。これらすべては、トレースバックの代わりに、次のステップを示す構造化されたエラーメッセージで拒否されます（[E21](docs/experiments/E21-cli-contract-report.md)）。

**And the gates in those two commands are no longer deletable.** Every ANDON in what
facet installs `raise`s; a bare `assert` is a statement `python -O` removes silently,
and 87 of this repo's gates were removable by an environment variable until E22
converted them. Measured before and after on the same gate, in four interpreter modes.
**And since [E23](docs/experiments/E23-route-gates-report.md), neither are the gates on
the route that produced the four accepted assets** — its **57 sites across twelve
tools**, converted as a pure move on files no test had ever executed, each one now
refusing under `-O` and `PYTHONOPTIMIZE=1` as well as under a normal interpreter.
**And since [E25](docs/experiments/E25-ruling.md) the class is closed.** Its **133 sites
across 43 files** — the measurement instruments that produced the evidence for the four
accepted assets above — convert the same way, bringing the total that `raise` to **278**.
Exactly **one** bare ANDON `assert` remains anywhere under `tools/`:
`superseded/texpass_thin_mask.py`, which is **never** converted, because those tools are
kept so anyone can run them and watch them fail the same way. That remainder is pinned
**by name** in the test suite, so a future sweep cannot tidy it away without editing the
test on purpose.

**サポート状況：** このリポジトリはオープンな環境で開発され、１つのハードウェア構成で、１人のディレクターと、交代するアドバイザーと実行者のセッションによって行われます。`main`のみがサポートされている状態です。リリースチャンネル、バックポートポリシー、SLAはありません。代わりに存在するものは記録であり、すべての主張はそれを生成するコードの隣に配置され、[docs/experiments](docs/experiments/)には、それぞれの仕様、レポート、および判断が含まれています。

## 要件

Blender 5.x、Python 3.11+（`numpy`、`scipy`、`trimesh`、`open3d`、`Pillow`、`spandrel`、`torch`を含む）。インペイントブラシを使用するには、ローカルのComfyUIインストールが必要です。RTX 5090で開発されました。生の速度よりもVRAMの余裕が重要です。

CIは、スイートの隔離されたサブセットを**ubuntu-latest / Python 3.12**で実行し、固定されたインストール（`.github/workflows/ci.yml`）を行います。アーティファクト層には、記録されたツリー（`E:\AI\training`）が必要ですが、これらはgitには含まれていないため、CIはそれらを意図的に選択しません。ローカルでは、`python -m pytest`がすべての**684個のテスト**を実行し、`python -m pytest -m "not artifacts"`がCIで再現される**675個のテスト**を実行します。

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
