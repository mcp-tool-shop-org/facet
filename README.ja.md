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

スタイルは**アセットに適用**され、テクスチャ空間で行われます。ビューごとに描画されたものを後でつなぎ合わせることはありません。形状を強調した粘土モデルをパイプラインに入力すると、そのメッシュのスタイライズされた参照から色を取得したテクスチャ付きメッシュが出力されます。参照では見えない部分は、マスク処理されたインペイントブラシとサーフェスを認識する拡張を使用して塗りつぶされます。

この問題の両側面を表す名前です：ポリゴンと、それらが表現する必要がある面。

## インストール

パイプライン自体は、入力したパスに対して実行する一連のローカルスクリプトです。リポジトリをクローンし、[開始方法](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/) を参照してください。

**レコードインデックスはパッケージとして提供**されるため、アシスタントは証拠の追跡を読み取る代わりに、それを照会できます。

```bash
npx @mcptoolshop/facet          # zero-prerequisite; verified binary, no Python needed
pipx install facet-mcp          # or the Python package directly
```

これには2つのコマンドが含まれています：`facet-mcp`（stdio MCPサーバー、6つのツール、4つの脚を持つ検証が健全性の基準を満たさない場合に使用）、および`facet-index`（`build` / `verify` / `q` / `claims`）。どちらかを、`--db`または`$FACET_INDEX_DB`を使用してインデックスに指定します。

## 現状

**4つのアセットが、4つの異なるカテゴリで、クレジット0で使用可能**です。それぞれは、ディレクターによって独自のズームレベルで評価されました（GLBまたはフルサイズのシートを使用）。特定の基準を満たすかどうかではなく、個別に判断されました。

| 対象 | カテゴリ | 承認済み | 参照/ブラシ/拡張 |
|---|---|---|---|
| **Character (W3)** | ヒューマノイド | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | 乗り物、シンプルなリギング | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | 獣、翼膜 | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | 小道具、ほぼ2D、グレーのオブジェクト | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

有効なテクセルは共有され、**異なる対象間で比較することはできません**。船はほとんど自身を視点から隠し、動物は半分を隠します。それぞれを事前に登録された範囲と比較して評価すると、**86〜93％**のカバー率になります。行間の違いはジオメトリであり、回帰ではありません。[完全な数値と分母](docs/handbook/subjects.md)。

**これはパイプラインであり、単一のキャラクタージェネレーターではありません。** 8つの名前付き要素で仕様に矛盾させると、プロンプトが**8回中8回勝利**します。中央値ΔEは46.3となり、5つの制御されたパラメータでは6.2でした。ただし、出力される人物は同じです。構造はメッシュと制御によって維持され、名前付き属性はプロンプトに依存します。

## パイプライン

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

段階ごとに、その理由とともに：**[ハンドブック](docs/handbook/index.md)**。

## どのように機能するか

6つの発見があり、それぞれに実験が必要であり、それぞれが生成された対象を超えて一般化されます。[詳細な説明と測定値](docs/findings.md)。

- **最初に形状を定義し、次にスタイルを適用します。** 再構築ツールは、サーフェスのノイズをジオメトリとして解釈します。意図的に誇張された平面を持つ、クリーンで彫刻のような粘土モデルの方が、より優れたトポロジーになります。スタイライズされたバージョンは並行して生成され、色の参照として使用されます。
- **顔のフレームを作成し、顔を取得します。** バストクロップを行うと、**3.1〜4.5倍**多くのポリゴンが頭部に配置され、その違いは構造的です。分離されたまぶた、眉間の溝、モデル化された鼻腔などです。シャープなぼかしではありません。
- **ツインはキャラクターではなく、メッシュに属します。** ツインを複数のメッシュで使用すると、カバー率が**62％から22.7％**に低下します。これは、腕がモデルの横の空中に投影されるためです。テクスチャを適用する予定のメッシュから、毎回ツインを生成してください。
- **アイデンティティはプロンプトに依存します。** プロンプトで名前が指定されていないカノンの要素は、偶然に現れ、同じように消えます。これは、金色の膝当てが、壊れたControlNetのノイズを通してのみ画像に表示されることがわかったときに測定されました。
- **ジオメトリを尋ね、閾値を使用しないでください。** キーでマスクされたものを、正確なレイキャストシルエットに置き換えると、有効なテクセルの参照カバー率が**28.4％から39.1％**に向上します。これは厳密に追加であり、拡散やGPUは使用しません。コーナーの中央値キーイングはここで3回失敗しており、廃止されました。
- **カメラで見ることができないものをアトラスから削除し、メッシュからは削除しないでください。** アトラスのテクセルの49％が外部からは見えません。これらの面を除外すると、補間が68％削減されます。削除するのではなく、除外することで、検出できるだけでなく、失敗を不可能にします。

## 解決されていない問題

名前と測定値は、脚注ではなく表紙に記載されています。[すべてコードにあります](docs/known-defects.md)。

- **ブレードバンドは、すべての8つのカメラでステージ1の参照の0.00％を占めます。** 灰色を背景にした鋼鉄が、キー自体の閾値に正確に一致します。ユニオンによって55.72％が救われます。
- **ストロークの継ぎ目は平滑化されていません。** プロベナンス境界は、通常のテクスチャバリエーションの5.5倍になります。ディレクターが指定した領域は9.5倍になります。
- **拡張によって、関連性のないアトラスアイランド間で出血が発生します。** 拡張されたテクセルの74.9％が、高さ1.0の図で平均0.177離れた別の島から色を取得します。
- **このパイプラインでのすべての再構築は、中空の二重壁シェルであり、壁は約2ボクセルです。** ボリュームに関する述語は、これには適用できません。

## このリポジトリの実行方法

この規律は、パイプラインと同じくらい重要であり、それには理由があります。以前のサイクルでは、10回のセッションがそれぞれ独自の出力を評価し、次のセッションで確立された事実として読まれる結論を記述しました。そのループ内のものは何も確認できませんでした。

- **作業前の仕様、作業後の報告、最終的な判断** — そして実験を設計するセッションは、決して自身の結果を評価することはありません。21件の実験が[記録](docs/experiments/)にあります。
- **修正は、それを覆した測定の横に配置されます**。静かな削除としてではなく。最初のセッションだけで6つの既存の主張が否定され、そのすべてが現在も、それらに取って代わるものと一緒に閲覧可能です。
- **失敗は、その理由とともにリポジトリに残ります**。[`tools/superseded/`](docs/tools.md) はアーカイブではありません。誰でもこれらのツールを実行し、同じように失敗する様子を観察できます。
- **否定的な結果は完全な成功です**。数値に調整するのではなく、報告され、完了します。
- **テストは、コードに触れるコミットと連携します** — 2つの環境で248件が合格し、240件の隔離されたものに対してパスベースのCIが実行されます。
- **記録は検索可能です**。全体の履歴に対するSQLite + FTS5インデックスがあり、4つの側面で検証されています。これにより、3つの場所で文章が間違っていた判断回数を、記録自体を数えることで特定しました。

## すべてがここにある

| | |
|---|---|
| **[ハンドブック](docs/handbook/index.md)** | ガイド — 各段階のルート、対象、プロファイルシステム |
| **[記録](docs/experiments/)** | 21件の実験：仕様、報告、判断、および測定前に述べられたすべての予測 |
| **[ルートで得られた知見](docs/findings.md)** | 永続的な知見と苦労して得られたルール（すべて） |
| **[各ツールのステータス](docs/tools.md)** | 動作するもの、廃止されたもの、およびそれぞれの証拠 |
| **[既知の欠陥](docs/known-defects.md)** | 解決されていないものすべて。コード内で測定され、特定されています。 |
| **[実際に起こった経緯](docs/arc-history.md)** | 時系列の履歴、修正はそのまま |
| **[CLAUDE.md](CLAUDE.md)** | ここで働く方法 — 役割、ルール、およびそれぞれのコスト |

## ライセンスに関する状況

すべての段階はローカルで実行され、商用利用も可能です：SDXL（OpenRAIL++）、MV-Adapter（オープンソース）、open3d（Apache-2.0）、spandrel（MIT）、RealESRGAN anime6B（BSD-3）、Blender、numpy、scipy、trimesh。

意図的に除外され、その理由も明記されています：**nvdiffrast**（非商用 — ここでは構造的なトリップワイヤーによって強制されており、アテステーションによるものではありません）、**Hunyuan3D-Paint**（EU、英国、および韓国ではライセンスが無効）、**MVPaint**と**TEXGen**（ライセンスが全くない）、および**UltraSharp / SUPIR / StableSR**（非商用のアップスケーラー）。

## 信頼性と脅威モデル

facetは完全に自分のマシン上で実行されます。すべてのツールは、コマンドラインで指定するパスに対して呼び出すスクリプトであるため、重要な質問は「このアプリはどのような権限を要求するか」ではなく、「これらのスクリプトはどのようにあなたのマシンに影響を与えるか」です。測定によって回答され、すべてのスイープは再実行可能です。完全なポリシーは[SECURITY.md](SECURITY.md)に記載されています：

- **アクセスされるデータ:** コマンドラインで指定するパスにあるローカルディスク上のメッシュ、テクスチャ、画像、およびJSON。さらに`docs/index/facet.db`も含まれますが、これは*派生したもの*です。これには、このリポジトリ内のファイルとしてすでに存在していたもの以外のものは含まれておらず、`facet_index.py build`によって最初から再生成されます。
- **アクセスされないデータ:** 認証情報は一切使用しません。ここでは、トークン、キー、またはパスワードを読み取ったり、保存したり、送信したりするものはなく、ツリーにも存在しません。プロバイダーのプレフィックスが付いたキー、GitHub PAT、Slackトークン、AWSキーID、秘密鍵ブロック、ベアラートークン、およびインラインの`api_key`/`password`割り当てについてスキャンしましたが、**一致するものはありません**。認証情報のようなファイルも追跡されていません。
- **テレメトリは行いません**。収集も送信もしません。オプトアウトするものが何もないため、オプトアウト機能もありません。
- **ネットワークへのデータ送信:** 34個のツールのうち2つがソケットを開きます — `restylize_views.py`と`texpass_brush.py` — そしてどちらもComfyUI HTTP API（`--host`）を呼び出します。**デフォルトは`127.0.0.1:8188`です**。その他のツール（`tools/`）はネットワーク接続を行いません。
- **権限:** 通常のユーザー。昇格、サービスインストール、システム設定またはレジストリへの書き込みはありません。

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
`0` ok / `1` user error / `2` runtime error, and refuse with a structured failure naming
the next step rather than a traceback ([E21](docs/experiments/E21-cli-contract-report.md)).

**サポート状況:** このリポジトリはオープンな環境で開発されており、1つのマシン上で、1人のディレクターとローテーションするアドバイザーと実行者のセッションによって行われます。`main`のみがサポートされている状態です。リリースチャンネルはなく、バックポートポリシーもSLAもありません。代わりに記録があります。すべての主張は、それを生成するコードの横に配置され、[docs/experiments](docs/experiments/)には、それぞれの仕様、報告書、および判断が含まれています。

## 要件

Blender 5.x、Python 3.11+と`numpy`、`scipy`、`trimesh`、`open3d`、`Pillow`、`spandrel`、`torch`が必要です。インペイントブラシを使用するには、ローカルのComfyUIインストールが必要です。RTX 5090で開発されました。VRAMの空き容量は、生の速度よりも重要です。

CIは、**ubuntu-latest / Python 3.12**上で、固定バージョンでインストールされたテストスイートの特定のサブセット（`.github/workflows/ci.yml`）を実行します。成果物として必要なのは、`E:\AI\training`に記録されているツリーですが、これらはGitに含まれていないため、CIは意図的にそれらをテスト対象から除外します。ローカル環境では、`python -m pytest`がすべての**248**個のテストを実行し、`python -m pytest -m "not artifacts"`がCIで再現される**240**個のテストを実行します。

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
