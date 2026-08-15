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
  Local-first — your own GPU, with a metered cloud step where it will not fit<br>
  No non-commercial licence anywhere in the chain
</p>

---

スタイルは**アセットに適用**され、テクスチャ空間で行われます。ビューごとに描画されて、後でつなぎ合わせることはありません。形状を強調した粘土のコンセプトをパイプラインに入力すると、スタイライズされた参照メッシュから色を取得したテクスチャ付きメッシュが出力されます。参照では見えない部分は、マスク処理されたインペイントブラシとサーフェスを認識する膨張によって補完されます。

この問題の2つの側面、つまりポリゴンと、それらが保持する必要がある面を表す名前が付けられています。

## インストール

パイプライン自体は、入力するパスに対して実行する一連のローカルスクリプトです。リポジトリをクローンし、[Getting Started](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/) を参照してください。

**2つのサーバーがパッケージとして提供されます**。1つはレコードインデックスで、アシスタントが証拠の追跡を読み込むのではなく、照会できるようにします。もう1つは、**v0.4.0から測定サーバー**です。これにより、数か月離れて測定された2つのアセットは、同じコードパスを経由します。

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` は、レコード上の stdio MCP サーバーであり（6つのツールがあり、そのうちの1つが拒否する健全性サーフェスとして機能する4脚検証）、`facet-index` はインデックス自体です（`build` / `verify` / `q` / `claims`）。どちらもチェックアウト内から実行します。`--db` は別のインデックスの名前です。

### 測定サーバー - v0.4.0で新規追加

`facet-measure` は、比較の**数値的な側面**を処理し、出力が良好かどうかは判断しません。すべてのペイロードには、サーバーバージョン、インストルメント自体のファイルハッシュ、および構成ハッシュが含まれており、`measure_report` は不一致がある場合の比較を**拒否します**。これは、このシステム全体の存在意義です。

**verb**（動詞）を実行することで検証され、`--help` を実行するのとは異なります。制御メッシュは、チェックアウトされていないマシン上で786,432個の面と完全なアイデンティティエンベロープを返します。

**結果は1つの要素に依存し、それはPythonのバージョンです:**

| お使いのPython | `[measure-full]` を使用すると |
|---|---|
| **3.11 / 3.12** | **8つのツールすべて**が利用可能になります。`open3d` はPyPIからインストールされます。 |
| **3.13** | 4つのツール：`mesh_stats`、`mesh_topology`、`measure_report`、`anchor_check` |

`open3d` 0.19.0 is the latest *release* and publishes cp38–cp312 wheels with **no sdist**,
so on 3.13 there is nothing on PyPI to install. The extra carries it behind
`python_version < "3.13"`, so the install **succeeds** there and the four geometry tools
exit **`4` REFUSED** naming what they need — rather than the whole install failing.

**Python 3.13で8つすべてを取得するには**、Open3Dは現在のcp313ホイールをローリング開発チャンネルに公開しています。コマンドラインでは直接URLを使用できます。これは、公開されたパッケージメタデータ内でのみ禁止されています。

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **WindowsとmacOSでは、開発用ホイールのファイル名は`+<sha>`で終わります**（執筆時点では`open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl`であり）、名前は`main`が変更されるにつれて変更されます。したがって、[`main-devel`リリース](https://github.com/isl-org/Open3D/releases/tag/main-devel)にあるアセットをリストし、現在のものを選択します。**このパイプライン自体のOpen3Dに依存する数値は、このビルドに対して測定されました**。これは、比較の境界線です。アイデンティティエンベロープには、インストルメントのハッシュが記録され、その依存関係は記録されません。[E31](docs/experiments/E31-ruling.md)。

*v0.3.1までのホイールには2つの`.py`ファイルが含まれており、測定インストルメントは含まれていません。そのため、インストールされた測定サーバーは実行するものがありませんでした。これは4回のリリースにわたって誰にも気づかれませんでした。なぜなら、このリポジトリ自体がチェックアウトだからです。ツールは、ビルドされた場所で機能し、他の場所に存在したことはありませんでした。*

⚠ **`pip install facet-mcp` は、v0.3.0までのすべてのリリースバージョンで壊れており、v0.3.1で修正されています**。ホイールは、トップレベルモジュールとして`facet_index`をインストールするため、v0.3.0までには、レコードの場所を`<venv>/Lib`に対して解決していました（これは、コーパスもインデックスも含まない）。また、`build`、`claims`、および`q`は、`--db`なしではすべて失敗します。
**v0.3.0以前を使用する場合は、上記の`npx`バイナリを使用してください。**

v0.3.1以降では、ルートはレコードを仮定するのではなく、**レコードの存在を確認することで解決されます**。どちらかのコマンドをチェックアウト内から実行すると、見つかります。他の場所から実行すると、**`4` REFUSED**と出力され、試した両方のディレクトリと検索した両方のマーカーの名前が表示されます。
`$FACET_INDEX_DB` は現在、両方のコマンドによって読み取られ、どの*インデックス*を使用するかを選択します（*コーパス*は選択しません）。ホイールを`main`からビルドし、クリーンなvenvにインストールした場合の測定結果。[E24](docs/experiments/E24-ruling.md)。

*このブロックは2回修正されました。最初に `pipx install facet-mcp # またはPythonパッケージを直接`, until v0.3.0's read-back ran a **verb** instead of `--help` と記述されていました。次に、ホイールは「`q`と`claims`でのみ機能する」と記述されていましたが、**`claims`も機能しませんでした**。これはE24によって実行された結果です。両方の修正は、[known-defects.md](docs/known-defects.md)に測定値とともに記録されています。*

## 現在の状況

**4つの承認済みアセットを、4つの被験者クラスに対して、クレジット0で使用できます**。それぞれは、ディレクターが独自のズームで（GLBまたはフルサイズのシート上で）判断しました。メトリックがしきい値を超えてクリアされたわけではありません。

| 被験者 | クラス | 承認済み | 参照/ブラシ/膨張 |
|---|---|---|---|
| **Character (W3)** | ヒューマノイド | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | 車両、細いリギング | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | 獣、翼膜 | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | 小道具、ほぼ2D、グレーのグラデーション | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

共有されるのは有効なテクセルであり、**それらは被験者間で比較できません**。船はほとんど自身を目の高さから隠し、動物は半分を隠します。それぞれを独自の事前に登録された範囲上限と比較して評価すると、**86〜93%**になります。行間の違いはジオメトリであり、回帰ではありません。[完全な数値と分母](docs/handbook/subjects.md)。

**これはパイプラインであり、1つのキャラクターを生成するものではありません**。8つの名前付き要素で仕様に矛盾させると、プロンプトが**8/8**で勝利します。中央値ΔEは46.3であり、5つの制御対象では6.2です。ただし、図は同じ人物のままです。構造はメッシュと制御によって保持され、名前付き属性はプロンプトに依存します。

## パイプライン

```
  styled 2D concept ╌╌► clay prep ╌╌╮   ← CANDIDATE hop, walked once. Not a route
                                    ╎     stage. Everything below it is the route.
                                    ▼
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

段階ごとに、各段階の理由を説明します：**[ハンドブック](docs/handbook/index.md)**。

**ダッシュ状のホップは新しく、意図的に完全に連続したものではありません。** ルートの最初のボックスには常に「粘土コンセプト」と表示されており、これまでここから何も生成されていませんでした。すべての粘土が手作業で到着し、処理中に調整されていました。現在、コンセプト→粘土ツールが存在し、その最初のペアがフルサイズでテストされました：ポーズ、リストラップ、ベルトのメダリオン、そして破れた裾がすべて再現されています。たてがみは再現されませんでした。色の滲みがフレーム全体で測定された結果、**C\* p99.9 = 13.15**となり、シームレスな非彩度背景になりました。**このペアでは、メッシュがより良い状態になるかどうかを示すことはできません。** これは、その価値を評価する唯一の基準であり、そのため、証拠とともに候補として残っています：**[コンセプト準備](docs/concept-prep.md)**。

## どのように機能するか

それぞれが実験の対象となり、それらの結果が対象を超えて一般化される6つの発見。[詳細な説明と測定値は](docs/findings.md)にあります。

- **まず形状を定義し、次にスタイルを適用します。** 再構築ツールは、表面のノイズをジオメトリとして解釈します。意図的に誇張された平面を持つ、滑らかで彫刻のような粘土は、様式化されたスプライトよりも優れたトポロジーで再現されます。様式化されたツインは並行して生成され、色の参照として使用されます。
- **顔の輪郭を捉え、顔を作成します。** バストクロップを使用すると、頭部のポリゴン数が**3.1〜4.5倍**増加し、その違いは構造的です。分離されたまぶた、眉間の溝、モデル化された鼻腔などであり、単なるぼかしの軽減ではありません。
- **ツインはキャラクターではなく、メッシュに属します。** ツインを複数のメッシュで使用すると、カバレッジが**62% → 22.7%**に低下します。これは、腕がモデルの横にある空中に投影されるためです。テクスチャを適用する予定のメッシュから毎回ツインを生成してください。
- **アイデンティティはプロンプトに依存します。** プロンプトで指定されていないカノンの要素が偶然生成され、同じ方法で消えます。これは、金色の膝当てが、壊れたControlNet内のノイズを通してのみ画像に表示されるようになったときに測定されました。
- **閾値ではなく、ジオメトリを要求します。** キー化されたマスクを正確なレイキャストシルエットに置き換えると、有効なテクセルに対する参照カバレッジが**28.4% → 39.1%**に増加しました。これは厳密に追加であり、拡散やGPUは使用しません。コーナーメディアンキーイングはここで3回失敗しており、廃止されました。
- **カメラで見ることができないものをアトラスから削除し、決してメッシュからは削除しないでください。** アトラスのテクセルの49%が外部からは見えません。これらの面を除外すると、補間が68%削減されます。削除するのではなく、除外することで、検出できるだけでなく、失敗を不可能にします。

## まだ解決されていない問題

脚注ではなく、表紙に記載されている名前と測定値。[すべてはコード内にあります](docs/known-defects.md)。

- **ブレードバンドはすべての8つのカメラでステージ1の参照の0.00%を占めます。** 鋼鉄が灰色の背景に配置されている場合、キー自体の閾値と完全に一致します。ユニオンによって55.72%が救済されます。
- **ストロークの継ぎ目は均一ではありません。** プロベナンス境界は、通常のテクスチャの変化の**5.5倍**を示し、ディレクターが指定した領域は**9.5倍**です。
- **拡散によって、関連性のないアトラスアイランド間で色が滲みます。** 74.9%の拡散されたテクセルは、高さ1.0の図で平均0.177離れた別の島から色を取得します。
- **このルート上のすべての再構築は、中空の二重壁シェルであり、壁は約2ボクセルです。** ボリューメトリックな述語は、これには適用できません。

## このリポジトリの運用方法

パイプラインと同様に、規律もまた重要な要素であり、それには理由があります：以前のサイクルでは、10回のセッションがそれぞれ独自の出力を評価し、次のセッションで確立された事実として読まれる結論を記述しました。そのループ内のものは何も検証できませんでした。

- **作業前に仕様を定め、報告後に判断を下します。** そして、実験を設計するセッションは、決して自身の結果を評価しません。31回の実験が[記録](docs/experiments/)にあります。
- **修正は測定によって覆された場所に配置され、静かに削除されることはありません。** 最初のセッションだけで、6つの継承された主張が否定されており、そのすべては、それを置き換えたものと一緒に今でも読むことができます。
- **失敗とその理由とともに、リポジトリに記録されます。[`tools/superseded/`](docs/tools.md)はアーカイブではありません。** 誰でもこれらのツールを実行し、同じように失敗するのを見ることができます。
- **否定的な結果は完全な成功であり、調整して数値に近づけるのではなく、報告され、閉じられます。**
- **テストはコードに触れるコミットとともに実行されます。** 2つの席で1053個が合格し、1008個の密閉されたものに対してパスゲート付きCIが実行されます。
- **記録はクエリ可能です。** SQLite + FTS5インデックスを使用して、すべての履歴を検証しました。これにより、プロットが3つの場所で間違っていたことが、記録自体を数えることで判明しました。

## すべてがどこにあるか

| | |
|---|---|
| **[ハンドブック](docs/handbook/index.md)** | ガイド - ルートの段階ごとの説明、対象、プロファイルシステム |
| **[コンセプト準備](docs/concept-prep.md)** | 候補となる粘土ホップ：ゲート0での実行、配置、およびそれが開くライセンス項目 |
| **[記録](docs/experiments/)** | 31回の実験：仕様、報告、判断、および測定前に述べられたすべての予測 |
| **[ルートが学んだこと](docs/findings.md)** | 永続的な発見と苦労して得られたルールをすべてまとめたもの |
| **[各ツールの状態](docs/tools.md)** | 何が機能し、何が廃止され、それぞれの証拠は何か |
| **[既知の欠陥](docs/known-defects.md)** | 解決されていないすべての問題。測定され、コード内に配置されています。 |
| **[アークの履歴](docs/arc-history.md)** | 時系列の履歴。修正はそのまま残っています。 |
| **[CLAUDE.md](CLAUDE.md)** | ここでどのように作業するか - 役割、ルール、およびそれぞれがどのようなコストを伴うか |

## ライセンスの位置

すべてのステージはローカルで実行され、商用利用可能な状態です：SDXL（OpenRAIL++）、MV-Adapter（オープンソース）、open3d（Apache-2.0）、spandrel（MIT）、RealESRGAN anime6B（BSD-3）、Blender、numpy、scipy、trimesh。

意図的に除外されており、その理由は次のとおりです：**nvdiffrast**（非商用利用 — ここでは構造的なトリップワイヤーによって強制され、アテステーションによるものではありません）、**Hunyuan3D-Paint**（EU、英国、および韓国でのライセンスが無効）、**MVPaint**および**TEXGen**（ライセンスが一切存在しない）、および**UltraSharp / SUPIR / StableSR**（非商用利用のアップスケーラー）。

**主張の範囲は、発見されるのを待つのではなく、明示的に述べられています。** これは、上記の図のステージから画像から3Dへの変換以降の**記録された経路**を記述します。それよりも上流にある候補となるクレイ準備ステップは、現在、このリポジトリが**検証していない**条件を持つクローズドクラウドAPIで実行されているため、ここにあるライセンスに関する主張は、そのクレイから作成されたアセットには適用されません。これは未解決の問題であり、解決への明確な経路があります：ライセンスに準拠したローカルモデルは**Qwen-Image-Edit（Apache-2.0）**であり、**FLUX.1-Kontext [dev] は、nvdiffrastと同じ理由で除外されています** — 非商用利用の重み。どちらもスタジオのモデルカタログに対してチェックされ、再利用されることはありません。その理由は[コンセプト準備](docs/concept-prep.md)にあります。

## 信頼と脅威モデル

facetは完全にローカルマシン上で実行されます — すべてのツールは、コマンドラインで入力するパスに対して呼び出すスクリプトです。したがって、重要な質問は、「このアプリはどのような権限を要求するか」ではなく、「これらのスクリプトがマシンに何をするか」です。測定によって回答され、すべてのスイープは再実行可能です。完全なポリシーは[SECURITY.md](SECURITY.md)にあります。

- **アクセスされるデータ：**ローカルディスク上のメッシュ、テクスチャ、画像、およびJSONファイル（コマンドラインで渡すパス）。さらに`docs/index/facet.db`があり、これは*派生したもの*です — これは、このリポジトリ内の既存のファイル以外のものを含んでいません。また、`facet_index.py build`は最初から再生成します。
- **アクセスされないデータ：**認証情報は一切使用しません。ここに認証情報（トークン、キー、パスワードなど）を読み取り、保存、または送信するものはなく、ツリーにも存在しません — プロバイダーのプレフィックスが付いたキー、GitHub PAT、Slackトークン、AWSキーID、秘密鍵ブロック、ベアラートークン、およびインラインの`api_key`/`password`割り当てについてスキャンされましたが、**一致するものはありません**。認証情報のようなファイルも追跡されていません。
- **テレメトリーは行いません。** 収集も送信もしません。オプトアウトするものが何もないため、オプトアウト機能もありません。
- **ネットワークからのデータ送信：**34個のツールのうち2つがソケットを開きます — `restylize_views.py`と`texpass_brush.py` — そしてどちらもComfyUI HTTP API（`--host`）を呼び出します。デフォルトは`127.0.0.1:8188`です。その他のツール（`tools/`）はネットワーク接続を行いません。
- **権限：**通常ユーザー。昇格、サービスインストール、システム設定またはレジストリへの書き込みはありません。

Three sharp edges are disclosed rather than claimed away, because a security note that
only lists reassurances is not a threat model: **file operations are not sandboxed**
(a tool writes wherever its arguments say); **absolute local paths are baked into many
tools and docs** — 114 occurrences across 26 files, not secrets but a disclosure of one
machine's layout, and the reason most tools will not run unmodified elsewhere; and
**unexpected failures surface as Python tracebacks in the 34 unpublished research
scripts**, with no `--debug` gate. Deliberate halts are `ANDON:` messages carrying the
measurement that fired them. That is the research-instrument contract, and
[SHIP_GATE.md](SHIP_GATE.md) records exactly when it stops being good enough — which for
the two commands facet *installs* it did, at 0.2.0: `facet-index` and `facet-mcp` return
`0` ok / `1` user error / `2` runtime error — and, since
[E22](docs/experiments/E22-ruling.md), **`4` REFUSED** for a fired gate or a failing
`verify` leg, which is the tool working and telling you not to proceed rather than a
runtime error. All of them refuse with a structured failure naming the next step rather
than a traceback ([E21](docs/experiments/E21-cli-contract-report.md)).

**そして、これらの2つのコマンドにあるゲートは、もはや削除できません。** facetがインストールするすべてのANDONは`raise`です。単なる`assert`は、環境変数によって静かに削除されるステートメント`python -O`であり、このリポジトリの87個のゲートはE22によって変換されるまで、環境変数で削除可能でした。同じゲートについて、4つのインタープリターモードで、前後に測定されました。
**そして、[E23](docs/experiments/E23-route-gates-report.md)以降、受け入れられた4つのアセットを生成した経路にあるゲートも同様です** — 12個のツールにまたがる57個のサイトで、テストが一度も実行されなかったファイルに対して純粋な移動として変換され、それぞれが`-O`と`PYTHONOPTIMIZE=1`だけでなく、通常のインタープリターでも拒否されるようになりました。
**そして、[E25](docs/experiments/E25-ruling.md)以降、クラスは閉じられました。** 43個のファイルにまたがる133個のサイト — 上記の4つの受け入れられたアセットのエビデンスを生成した測定ツール — は同じように変換され、合計で`raise`が278になりました。
正確には**1つだけ**のANDON`assert`が、`tools/`の下に存在します：
`superseded/texpass_thin_mask.py`であり、これは**決して**変換されません。なぜなら、これらのツールは誰でも実行して、同じように失敗する様子を見ることができるようにするためです。残りの部分はテストスイートで**名前によって固定**されており、将来のスイープでは、テストを意図的に編集しない限り、それを削除することはできません。

**サポート状況：**このリポジトリはオープンな環境で開発され、1つのマシンで、1人のディレクターと、ローテーションするアドバイザーと実行者のセッションによって行われます。`main`が唯一のサポート対象の状態です。リリースチャネル、バックポートポリシー、SLAはありません — 代わりに、すべての主張はそのコードの隣にあり、[docs/experiments](docs/experiments/)には、それぞれの仕様、レポート、および判決が含まれています。

## 要件

Blender 5.x、Python 3.11+と`numpy`、`scipy`、`trimesh`、`open3d`、`Pillow`、`spandrel`、`torch`が必要です。ローカルのComfyUIインストールは、インペイントブラシでのみ必要です。RTX 5090で開発されました。VRAMの余裕の方が、生の速度よりも重要です。

CIは、**ubuntu-latest / Python 3.12**上で、固定バージョンでインストールされた状態で（`.github/workflows/ci.yml`）、テストスイートの独立したサブセットを実行します。成果物として必要なのは、`E:\AI\training`に記録されているツリーですが、これらはGitに含まれていないため、CIは意図的にそれらを除外します。ローカル環境では、`python -m pytest`がすべての**1053**個のテストを実行し、`python -m pytest -m "not artifacts"`がCIで再現される**1008**個のテストを実行します。

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
