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

スタイルは**アセットに適用**され、テクスチャ空間で行われます。ビューごとに描画されたものを後でつなぎ合わせることはありません。形状を強調した粘土のコンセプトをパイプラインに入力すると、そのメッシュのスタイライズされた参照から色を取得したテクスチャ付きのメッシュが出力されます。参照では見えない部分は、マスク処理されたインペイントブラシとサーフェスを認識する拡張によって補完されます。

この問題の2つの側面、つまりポリゴンと、それらが表現する必要がある面を表す名前が付けられています。

## インストール

パイプライン自体は、入力するパスに対して実行する一連のローカルスクリプトです。リポジトリをクローンし、[開始方法](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/)を参照してください。

**レコードインデックスはパッケージとして提供**されるため、アシスタントは証拠の追跡を読み取る代わりに、それを照会できます。

```bash
npx @mcptoolshop/facet          # zero-prerequisite; verified binary, no Python needed
pipx install facet-mcp          # or the Python package directly
```

これには2つのコマンドが含まれています。1つは、標準入力/出力MCPサーバー（4脚検証が拒否的な健全なサーフェスとして機能する6つのツール）、もう1つは`facet-mcp`と`facet-index`（`build` / `verify` / `q` / `claims`）です。どちらかを、`--db`または`$FACET_INDEX_DB`を使用してインデックスにポイントします。

## 現状

**4つのアセットが、4つの異なる被写体クラスで、クレジット0で使用可能**です。それぞれは、ディレクターによって独自のズームレベルで評価されました（GLBまたはフルサイズのシートを使用）。特定の閾値を超えるという指標に基づいて評価されたわけではありません。

| 被写体 | クラス | 承認済み | 参照/ブラシ/拡張 |
|---|---|---|---|
| **Character (W3)** | ヒューマノイド | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | 乗り物、シンプルなリギング | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | 獣、翼膜 | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | 小道具、ほぼ2D、グレーのグラデーション | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

有効なテクセルは共有され、**被写体間で比較することはできません**。船はほとんど自身を目の高さから隠し、動物は半分を隠します。それぞれを事前に登録された範囲と比較して評価すると、**86〜93％**になります。行間の違いはジオメトリであり、回帰ではありません。[完全な数値と分母](docs/handbook/subjects.md)を参照してください。

**これはパイプラインであり、単一のキャラクタージェネレーターではありません。** 8つの名前付き要素で仕様に矛盾させると、プロンプトが**8回中8回勝利**します。中央値ΔEは46.3となり、5つの制御されたパラメータでは6.2でした。ただし、人物自体は同じままです。構造はメッシュと制御によって維持され、名前付きの属性はプロンプトに依存します。

## パイプライン

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

段階ごとに、その理由とともに説明します：**[ハンドブック](docs/handbook/index.md)**。

## どのように機能するか

6つの発見があり、それぞれに実験が必要であり、それぞれがそれを生成した被写体を越えて一般化されます。[詳細な説明と測定値](docs/findings.md)を参照してください。

- **まず形状を、次にスタイルを適用します。** 再構築ツールは、サーフェスのノイズをジオメトリとして解釈します。意図的に誇張された平面を持つ、クリーンで彫刻のような粘土を使用すると、スタイライズされたスプライトよりも優れたトポロジーが得られます。スタイライズされたバージョンは同時に生成され、色の参照になります。
- **面をフレームに収めると、顔が得られます。** バストクロップを行うと、頭部のポリゴン数が**3.1〜4.5倍**増加し、その違いは構造的です。分離されたまぶた、眉間の溝、モデル化された鼻腔などです。シャープなぼかしではありません。
- **ツインはキャラクターではなく、メッシュに属します。** ツインを複数のメッシュで再利用すると、カバレッジが**62％から22.7％**に低下します。これは、腕がモデルの横の空中に投影されるためです。テクスチャを適用する予定のメッシュから、毎回ツインを生成してください。
- **アイデンティティはプロンプトに属します。** プロンプトで名前が指定されていないカノン要素は、偶然に現れ、同じように消えます。これは、金色の膝当てが壊れたControlNetのノイズを通してのみ画像に表示されるようになったときに測定されました。
- **閾値ではなく、ジオメトリを要求します。** キー処理されたマスクを正確なレイキャストシルエットに置き換えると、有効なテクセルの参照カバレッジが**28.4％から39.1％**に増加しました。これは厳密に追加であり、拡散やGPUは使用しません。コーナーの中央値キーイングはここで3回失敗し、廃止されました。
- **カメラで見ることができないものをアトラスから削除し、メッシュからは決して削除しないでください。** アトラスのテクセルの49％が外側からは見えません。これらの面を除外すると、補間が68％削減されます。削除するのではなく、除外することで、検出できるだけでなく、失敗を不可能にします。

## 解決されていない問題

名前と測定値は、脚注ではなく表紙に記載されています。[すべてコードにあります](docs/known-defects.md)。

- **ブレードバンドは、すべての8つのカメラでステージ1の参照の0.00％を占めます。** 灰色を背景にした鋼鉄が、キー自体の閾値に正確に一致します。ユニオンによって55.72％が救われます。
- **ストロークの継ぎ目は平滑化されていません。** プロベナンス境界は、通常のテクスチャの変化の5.5倍になります。ディレクターが指定した領域は9.5倍になります。
- **拡張によって、関連性のないアトラスアイランド間で出血が発生します。** 拡張されたテクセルの74.9％が、高さ1.0の図で平均0.177離れた別の島から色を取得します。
- **このパイプラインでのすべての再構築は、中空の二重壁シェルであり、壁は約2ボクセルです。** ボリューメトリックな述語は、これには適用できません。

## このリポジトリの実行方法

この規律は、パイプラインと同じくらい重要であり、それには理由があります。以前の一連のセッションでは、各セッションで独自の出力を評価し、次のセッションで確立された事実として読まれる結論を記述しました。そのループ内のものは何も確認できませんでした。

- **作業前の仕様、作業後の報告、最終的な判断** — そして実験を設計するセッションは、決して自身の結果を評価することはありません。23件の実験が[記録](docs/experiments/)にあります。
- **修正は、それを覆した測定の横に配置されます**。静かな削除としてではなく。最初のセッションだけで6つの既存の主張が否定され、そのすべてが現在でも、それらに取って代わるものと一緒に読むことができます。
- **失敗は、その理由とともにリポジトリに残ります**。[`tools/superseded/`](docs/tools.md) はアーカイブではありません。誰でもこれらのツールを実行し、同じように失敗する様子を観察できます。
- **否定的な結果は完全な成功です**。数値に調整するのではなく、報告され、完了します。
- **テストは、コードに触れるコミットとともに実行されます** — 2つの担当者によって648件が合格し、640件の隔離されたものに対してパスベースのCIが適用されています。
- **記録は検索可能です**。4つの要素で検証された、すべてのデータに対するSQLite + FTS5インデックスです。これにより、文章に誤りがあった3つの場所で、記録自体を数えることで、判断の回数が特定されました。

## すべてがここにある

| | |
|---|---|
| **[ハンドブック](docs/handbook/index.md)** | ガイド — 各段階のルート、対象、プロファイルシステム |
| **[記録](docs/experiments/)** | 23件の実験：仕様、報告、判断、および測定前に述べられたすべての予測 |
| **[ルートが学んだこと](docs/findings.md)** | 永続的な発見と苦労して得られたルール（すべて） |
| **[各ツールのステータス](docs/tools.md)** | 動作するもの、廃止されたもの、およびそれぞれの証拠 |
| **[既知の欠陥](docs/known-defects.md)** | 解決されず、コードで測定および特定されたすべての問題 |
| **[実際に起こった経緯](docs/arc-history.md)** | 時系列の履歴、修正はそのまま |
| **[CLAUDE.md](CLAUDE.md)** | ここで働く方法 — 役割、ルール、およびそれぞれのコスト |

## ライセンスの位置

すべての段階はローカルで実行され、商用利用も可能です：SDXL（OpenRAIL++）、MV-Adapter（オープン）、open3d（Apache-2.0）、spandrel（MIT）、RealESRGAN anime6B（BSD-3）、Blender、numpy、scipy、trimesh。

意図的に除外され、その理由も記載されています：**nvdiffrast**（非商用 — ここでは構造的なトリップワイヤーによって強制されており、認証によるものではありません）、**Hunyuan3D-Paint**（EU、英国、および韓国でのライセンスが無効）、**MVPaint**と**TEXGen**（ライセンスが全くない）、および**UltraSharp / SUPIR / StableSR**（非商用のアップスケーラー）。

## 信頼と脅威モデル

facetは完全に自分のマシン上で実行されます。すべてのツールは、コマンドラインで渡すパスに対して呼び出すスクリプトです。したがって、重要な質問は、「このアプリはどのような権限を要求するか」ではなく、「これらのスクリプトはあなたのマシンに何をするか」です。測定によって回答され、すべてのスイープは再実行可能です。完全なポリシーは[SECURITY.md](SECURITY.md)に記載されています：

- **アクセスされるデータ:** ローカルディスク上のメッシュ、テクスチャ、画像、およびJSON。コマンドラインで渡すパスにあります。さらに`docs/index/facet.db`があり、これは*派生したもの*です。これには、このリポジトリのファイルとしてすでに存在していたもの以外のものは含まれておらず、`facet_index.py build`によって最初から再生成されます。
- **アクセスされないデータ:** 認証情報は一切ありません。ここでは、トークン、キー、またはパスワードを読み取ったり、保存したり、送信したりするものはなく、ツリーにも存在しません。プロバイダーのプレフィックスが付いたキー、GitHub PAT、Slackトークン、AWSキーID、秘密鍵ブロック、ベアラートークン、およびインラインの`api_key`/`password`割り当てについてスキャンされました。**一致するものはありません**。認証情報のようなファイルも追跡されていません。
- **テレメトリはありません**。収集も送信もしません。オプトアウトするものがないため、オプトアウトのオプションもありません。
- **ネットワークからのデータ送信:** 34個のツールのうち2つがソケットを開きます — `restylize_views.py`と`texpass_brush.py` — そしてどちらもComfyUI HTTP API（`--host`）を呼び出します。**デフォルトは`127.0.0.1:8188`です**。それ以外のもの（`tools/`）はネットワーク呼び出しを行いません。
- **権限:** 通常のユーザー。昇格、サービスインストール、システム設定またはレジストリへの書き込みはありません。

セキュリティに関する注意が安心感だけをリストアップするものではないため、3つの重要な点を開示します。それは脅威モデルではありません：「ファイル操作はサンドボックス化されていません」（ツールはその引数で指定された場所に書き込みます）、「絶対的なローカルパスは多くのツールとドキュメントに組み込まれています」 — 26個のファイルに114件の出現箇所があり、秘密情報ではなく、1つのマシンのレイアウトを開示するものであり、ほとんどのツールが変更せずに他の場所で実行されない理由です。そして、「予期しない失敗は、34個の未公開の研究スクリプトでPythonトレースバックとして表面化します」 — `--debug`ゲートはありません。意図的な停止は、それをトリガーした測定を含むメッセージである`ANDON:`です。それが研究ツールの契約であり、[SHIP_GATE.md](SHIP_GATE.md)には、それが十分に良い状態ではなくなる正確な時期が記録されています。facetが*インストールする*2つのコマンドの場合、0.2.0では次のようになります：`facet-index`と`facet-mcp`はそれぞれ、`0` OK / `1`ユーザーエラー / `2`ランタイムエラーを返します。そして、[E22](docs/experiments/E22-ruling.md)以降、トリガーされたゲートまたは失敗した`verify`要素の場合、**`4`拒否**されます。これは、ツールが動作し、実行時にエラーが発生するのではなく、続行しないように指示していることを意味します。それらすべては、トレースバックではなく、次のステップを記述した構造化されたエラーで拒否されます（[E21](docs/experiments/E21-cli-contract-report.md)）。

**And the gates in those two commands are no longer deletable.** Every ANDON in what
facet installs `raise`s; a bare `assert` is a statement `python -O` removes silently,
and 87 of this repo's gates were removable by an environment variable until E22
converted them. Measured before and after on the same gate, in four interpreter modes.
**And since [E23](docs/experiments/E23-route-gates-report.md), neither are the gates on
the route that produced the four accepted assets** — its **57 sites across twelve
tools**, converted as a pure move on files no test had ever executed, each one now
refusing under `-O` and `PYTHONOPTIMIZE=1` as well as under a normal interpreter.
**134 gates in the remaining research tools are still asserts** — named here rather than
omitted, scoped by [E22 Ruling 4](docs/experiments/E22-ruling.md), and none of them is
in a command facet installs: 132 are measurement instruments under `diagnostics/`, one
is a render check, and `superseded/`'s one is **never** converted, because those tools
are kept so anyone can run them and watch them fail the same way.

**サポート状況：** このリポジトリは、1つの環境で、1人のディレクターと交代制のアドバイザーおよび実行セッションによって、オープンに開発されています。`main`のみがサポートされている状態です。リリースチャンネル、バックポートポリシー、SLAはありません。代わりに、各主張はそれを生成するコードの隣に配置され、[docs/experiments](docs/experiments/)には、それぞれの仕様、レポート、および決定が含まれています。

## 要件

Blender 5.x、Python 3.11+（`numpy`、`scipy`、`trimesh`、`open3d`、`Pillow`、`spandrel`、`torch`を含む）。インペイントブラシを使用するには、ローカルにComfyUIをインストールする必要があります。RTX 5090で開発されており、生の速度よりもVRAMの余裕が重要です。

CIは、**ubuntu-latest / Python 3.12**上で、スイートの密閉されたサブセットを実行し、固定バージョンでインストールします（`.github/workflows/ci.yml`）。アーティファクト層には、記録されたツリーが必要です（`E:\AI\training`）。これらはgitに含まれていないため、CIは意図的にそれらを選択しません。ローカルでは、`python -m pytest`がすべての**648**個のテストを実行し、`python -m pytest -m "not artifacts"`がCIで再現される**640**個のテストを実行します。

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
