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

このスタイルは、テクスチャ空間内の**アセットに適用**されます。各視点ごとに描画されるのではなく、後でそれらを組み合わせて一つのものにします。形状を強調した粘土のコンセプトをルートに入力すると、その入力に基づいてスタイライズされた参照画像から色を取得したテクスチャ付きのメッシュが生成され、参照画像では見えなかった部分は、マスク処理されたインペイントブラシとサーフェス情報を考慮した拡大処理によって補完されます。

この名前は、問題の二つの要素、すなわち多角形と、それらが構成する面を表しています。

## その現状は

**4つの分野にわたる、合計4つの承認された資料。単位は0点とする。** 各資料の評価は、ディレクターがそれぞれの資料に合わせて（GLB形式の場合や、全ページ表示の場合など）個別に行い、一律の基準で合否を判断することはなかった。

| 件名、主題、対象 | クラス | 承認された、受け入れられた。 | 参照／ブラシ／拡張 |
|---|---|---|---|
| **Character (W3)** | 人型ロボット、人間のような姿 | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | 車両、細いロープやワイヤーなど。 | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | 獣、翼膜 | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | 小道具、ほぼ2次元の表現、グレーを基調とした配色。 | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

テクセルは有効な範囲を持ち、**被験者間で比較することはできません**。例えば、船の大部分は視線から隠れて見えませんし、動物は体の半分を隠します。それぞれの値を、事前に登録された上限と比較して評価すると、**86～93%**という結果が得られます。行間の差は回帰によるものではなく、あくまで形状の違いです。[詳細な数値と分母については、こちらをご覧ください](docs/handbook/subjects.md)。

**これは、単一のキャラクターを生成するものではなく、パイプラインです。** 8つの特定の要素に関する仕様と矛盾することで、プロンプトは**8回中8回勝利し**、5つのコントロール画像と比較して中央値ΔEが46.3となり、それに対してコントロール画像のΔEは6.2にとどまります。一方、生成される人物の姿は変わりません。構造はメッシュと制御によって維持され、特定の属性はプロンプトに沿って変化します。

## ルート

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

各段階ごとに、その理由を説明します：**[ハンドブック](docs/handbook/index.md)**。

## 何がうまく機能させるのでしょうか

6つの発見があり、それぞれに実験が必要であり、また、それらの発見は、その発見を生み出した対象を超えて一般化できるものである。[詳細な説明と測定値については、こちらを参照：docs/findings.md]

- **まずは形状を整え、その後にスタイルを加える。** リコンストラクターは表面のノイズをジオメトリとして解釈する。意図的に誇張された面を持つ、滑らかで彫刻のようなクレイモデルの方が、スタイライズされたスプライトよりも優れたトポロジーを持つ結果になる。そして、そのスタイライズされたモデルが同時に生成され、カラー参照として使用される。
- **顔の輪郭を明確にし、表情を豊かにする。** バストアップのクロップを行うと、頭部のポリゴン数が3.1～4.5倍に増加し、その差は構造的なものとなる。具体的には、まぶたが分離され、眉間の皺や鼻腔がモデリングされるなど、単なるぼかしの強さの問題ではない。
- **ツインモデルはキャラクターではなく、メッシュの一部である。** ツインモデルを複数のメッシュで再利用することで、カバレッジが62%から22.7%に減少する。これは、腕がモデルの横にある空中に投影されるためである。テクスチャを適用する予定のメッシュから毎回ツインモデルを生成する。
- **アイデンティティはプロンプトによって定義される。** プロンプトで指定されていないカノンの要素が偶然現れても、同じように消える。例えば、金色のニープレートが、壊れたControlNetによるノイズを通してのみ画像に表示された場合などである。
- **閾値ではなく、ジオメトリを考慮する。** キーフレームマスクを正確なレイキャストシルエットで置き換えると、有効なテクセルにおける参照カバレッジが28.4%から39.1%に増加する。これは、単純な加算であり、拡散やGPUは使用しない。コーナー・メディアンキーイングはここで3回失敗しており、廃止された。
- **カメラで見えないものは、アトラスから削除し、決してメッシュからは削除しない。** アトラスのテクセル全体の49%が外部からは見えないため、これらの面を削除することで補間処理が68%削減される。削除するのではなく、除外することで、単に検出可能にするだけでなく、失敗そのものを不可能にする。

## まだ解決されていないのは何ですか

ページ冒頭に名前と詳細を記載し、脚注には入れません。すべての情報は、次の場所にあります（コード内）。[docs/known-defects.md]

- **ブレードバンドは、すべての8つのカメラにおいて、ステージ1の参照値の0.00%を占める**。グレーの背景に置かれた金属製の帯が、キーの色と正確に一致する。この処理によって、55.72%の改善が見られる。
- **ストロークの継ぎ目は均一化されていない**。起源を示す境界線は、通常のテクスチャの変化よりも5.5倍大きく変化し、ディレクターが指定した領域では9.5倍の大きさで変化する。
- **関連性のないアトラスアイランド間で膨張が起こり、色が混ざる**。74.9%の膨張したテクセルは、別の島の色を借用しており、その距離は平均0.177（高さ1.0の図で）。
- **このルートにおけるすべての再構成は、中空の二重壁構造である**。壁の厚さは約2ボクセル。単一の構造に対しては、体積に関する述語は有効ではない。

## このリポジトリはどのように運用されているか

この分野における知識や技術は、パイプラインと同様に、ある目的のために存在し、その過程で生み出されるものでもある。以前の段階では、10回のセッションを通じて各自が自分の成果を評価し、次のセッションでそれを事実として共有するというプロセスを踏んでいた。しかし、その一連の流れの中で検証可能な点は何もなかった。

- **作業前に仕様を定め、作業後に報告し、最後に結論を出す** — そして、実験を設計するセッションは、決してその結果自体を評価することはありません。20件の実験が[記録](docs/experiments/)にあります。
- **修正は、それを覆した測定値の横に配置され、静かに削除されることはありません。** 最初のセッションだけで6つの既存の主張が誤りであることが判明し、そのすべては現在も、それらに取って代わるものと一緒に閲覧できます。
- **失敗事例とその理由とともに、リポジトリに残ります。** [`tools/superseded/`](docs/tools.md) はアーカイブではありません。誰でもこれらのツールを実行して、同じように失敗する様子を観察できます。
- **否定的な結果は完全な成功であり、特定の数値に調整するのではなく、報告され、完了として扱われます。**
- **テストは、コードを変更したコミットと連動します。** 2つの異なる担当者によって213件のテストが合格し、そのうち205件についてはパス制限付きのCI（継続的インテグレーション）が行われています。
- **記録は検索可能です。** 全ての履歴に対してSQLite + FTS5インデックスが作成され、4つの異なる環境で検証されています。これにより、3つの場所で文章に誤りがあったことが判明し、記録自体を数えることで結論の件数が確認されました。

## すべてが揃う場所

| | |
|---|---|
| **[ハンドブック](docs/handbook/index.md)** | ガイドの内容：各区間のルート、取り上げるテーマ、プロファイルシステム。 |
| **[記録](docs/experiments/)** | 20回の実験：仕様、レポート、判断、および測定前に述べられたすべての予測 |
| **[ルートが学習したこと](docs/findings.md)** | 永続的な発見と苦労して得られたルールをすべて記載 |
| **[各ツールのステータス](docs/tools.md)** | 動作するもの、廃止されたもの、およびそれぞれの証拠 |
| **[既知の欠陥](docs/known-defects.md)** | 解決されていないすべての問題。コード内で測定され、特定されているもの |
| **[実際に起こったこと](docs/arc-history.md)** | 時系列の履歴、修正はそのまま |
| **[CLAUDE.md](CLAUDE.md)** | ここで働く方法：役割、ルール、およびそれぞれのコスト |

## ライセンスに関する状況

すべての段階はローカルで実行され、商用利用においても問題ありません。SDXL（OpenRAIL++）、MV-Adapter（オープンソース）、open3d（Apache-2.0）、spandrel（MIT）、RealESRGAN anime6B（BSD-3）、Blender、numpy、scipy、trimesh。

意図的に除外され、その理由は以下のとおり：**nvdiffrast**（非商用利用 - ここでは構造的なトリップワイヤーによって強制され、認証によるものではありません）、**Hunyuan3D-Paint**（EU、英国、および韓国でのライセンスが無効）、**MVPaint**および**TEXGen**（ライセンスが全くない）、および**UltraSharp / SUPIR / StableSR**（非商用アップスケーラー）。

## 信頼と脅威モデル

facetは完全にローカルマシン上で実行されます。すべてのツールは、コマンドラインで入力したパスに対して呼び出すスクリプトです。したがって、重要な質問は、「このアプリはどのような権限を要求するか」ではなく、「これらのスクリプトがあなたのマシンに何をするか」ということです。測定によって回答され、すべてのスイープは再実行可能です。完全なポリシーは[SECURITY.md](SECURITY.md)に記載されています。

- **アクセスされるデータ：**ローカルディスク上のメッシュ、テクスチャ、画像、およびJSONファイル。コマンドラインで渡すパスにあります。さらに`docs/index/facet.db`があり、これは*派生したもの*です。これには、このリポジトリ内の既存のファイル以外のものは含まれておらず、`facet_index.py build`によって最初から再生成されます。
- **アクセスされないデータ：**認証情報は一切使用しません。ここに資格情報（トークン、キー、パスワード）を読み取ったり、保存したり、送信したりするものはなく、ツリーにも存在しません。プロバイダーのプレフィックスが付いたキー、GitHub PAT、Slackトークン、AWSキーID、秘密鍵ブロック、ベアラートークン、およびインラインの`api_key`/`password`割り当てについてスキャンしましたが、**一致するものはありません**。資格情報のようなファイルも追跡されていません。
- **テレメトリーは行いません。**収集も送信もしません。オプトアウトする必要がないのは、オプトアウトするものが何もないからです。
- **ネットワークからのデータ送信：**34個のツールのうち2つがソケットを開きます。それは`restylize_views.py`と`texpass_brush.py`であり、どちらも`--host`にあるComfyUI HTTP APIを呼び出します。デフォルトは`127.0.0.1:8188`です。その他のツール（`tools/`）はネットワーク接続を行いません。
- **権限：**通常ユーザー。昇格、サービスインストール、システム設定またはレジストリへの書き込みはありません。

Three sharp edges are disclosed rather than claimed away, because a security note that
only lists reassurances is not a threat model: **file operations are not sandboxed**
(a tool writes wherever its arguments say); **absolute local paths are baked into many
tools and docs** — 114 occurrences across 26 files, not secrets but a disclosure of one
machine's layout, and the reason most tools will not run unmodified elsewhere; and
**unexpected failures surface as Python tracebacks**, with no `--debug` gate and no
structured error shape. Deliberate halts are `ANDON:` messages carrying the measurement
that fired them. That is the research-instrument contract, and
[SHIP_GATE.md](SHIP_GATE.md) records exactly when it stops being good enough.

**サポート状況：**このリポジトリはオープンに開発されており、1つの環境で、1人のディレクターと、交代するアドバイザーと実行者のセッションによって行われます。`main`のみがサポートされている状態です。リリースチャンネルはなく、バックポートポリシーもSLAもありません。代わりに存在するものは記録であり、すべての主張はそのコードの隣にあり、[docs/experiments](docs/experiments/)には、各実験の仕様、レポート、および判断が含まれています。

## 要件

Blender 5.x、Python 3.11+と`numpy`、`scipy`、`trimesh`、`open3d`、`Pillow`、`spandrel`、`torch`が必要です。インペイントブラシを使用するには、ローカルのComfyUIインストールが必要です。RTX 5090で開発されました。生の速度よりもVRAMの余裕が重要です。

CIは、**ubuntu-latest / Python 3.12**上で、スイートの隔離されたサブセットを実行し、インストールを固定します（`.github/workflows/ci.yml`）。アーティファクト層には、記録されたツリーが必要であり、それは`E:\AI\training`にあります。これはgitには含まれていないため、CIはそれらを意図的に選択しません。ローカルでは、`python -m pytest`が**213個の**テストすべてを実行し、`python -m pytest -m "not artifacts"`が**205個の**CIで再現されるテストを実行します。

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
