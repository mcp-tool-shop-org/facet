<p align="center">
  <a href="README.ja.md">日本語</a> | <a href="README.md">English</a> | <a href="README.es.md">Español</a> | <a href="README.fr.md">Français</a> | <a href="README.hi.md">हिन्दी</a> | <a href="README.it.md">Italiano</a> | <a href="README.pt-BR.md">Português (BR)</a>
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

该风格应用于**资源本身**，在纹理空间中——而不是针对每个视角进行绘制，然后将它们拼接在一起。向流水线输入一个具有夸张形式的粘土概念模型，它会返回一个带有纹理的网格，其颜色来自对*该*网格的样式化参考，所有参考无法看到的部分都通过蒙版涂抹画笔和感知表面的膨胀来填充。

名称既指问题的一半：多边形，也指它们需要呈现的面。

## 安装

该流水线本身是一组本地脚本，您可以在键入的路径上调用这些脚本——克隆仓库并阅读[入门指南](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/)。

**两个服务器以软件包的形式提供**——记录索引，因此助手可以查询证据链，而不是读取它；以及**从 v0.4.0 版本开始，测量服务器**，因此两个相隔几个月测量的资源将通过一个代码路径进行处理。

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` 是针对记录的 stdio MCP 服务器（六个工具，其中四足验证作为拒绝健康表面的工具），而 `facet-index` 本身是索引（`build` / `verify` / `q` / `claims`）。从检出目录内部运行任何一个；`--db` 指的是不同的索引。

### 测量服务器——v0.4.0 版本的新功能

`facet-measure` 回答了比较的**数值部分**，并且不会说明输出是否良好。每个有效负载都包含服务器版本、仪器的文件哈希和一个配置哈希，并且 `measure_report` **拒绝**跨不匹配进行比较——这是整个系统存在的目的。

通过运行一个**动词**而不是 `--help` 来验证——控制网格返回 786,432 个面，并在没有检出目录的机器上具有完整的身份包围。

**您获得的结果取决于一件事，那就是您的 Python 版本：**

| 您的 Python | `[measure-full]` 提供了 |
|---|---|
| **3.11 / 3.12** | **所有八个工具**——`open3d` 从 PyPI 安装 |
| **3.13** | 四个工具；`mesh_stats`、`mesh_topology`、`measure_report`、`anchor_check` |

`open3d` 0.19.0 是最新的*发布版*，并发布了 cp38–cp312 wheels，**没有 sdist**，因此在 3.13 上，PyPI 上没有任何内容可以安装。额外的组件将其置于 `python_version < "3.13"` 之后，因此安装在那里**成功**，并且四个几何工具会输出 **`4` REFUSED**，表明它们需要什么——而不是整个安装失败。

**要在 Python 3.13 上获得所有八个工具**，Open3D 在其滚动开发通道上发布了当前的 cp313 wheels。在命令行中使用直接 URL 即可；它只是禁止在已发布的软件包元数据中进行操作：

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **在 Windows 和 macOS 上，开发 wheels 的后缀为 `+<sha>`**（撰写本文时为 `open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl`），并且名称会随着 `main` 的变化而变化——列出 [`main-devel` 发布版](https://github.com/isl-org/Open3D/releases/tag/main-devel) 中的资源，并选择当前版本。**此构建是本流水线中所有依赖于 open3d 的数字所依据的测量标准**，并且它是一个真正的可比性边界：身份包围记录仪器的哈希值，而不是其依赖项——[E31](docs/experiments/E31-ruling.md)。

*在 v0.3.1 之前，wheel 包含两个 `.py` 文件，并且不包含任何测量仪器，因此安装的测量服务器没有任何内容可以调用。没有人注意到这一点，因为这个仓库就是检出目录：该工具在其构建的位置工作，并且从未位于其他位置。*

⚠ **在所有已发布版本中，直到 v0.3.0，`pip install facet-mcp` 都是损坏的，并在 v0.3.1 中修复。** wheel 将 `facet_index` 作为顶级模块进行安装，因此，到包括 v0.3.0 在内的所有版本，它都会根据 `<venv>/Lib` 解析记录的位置——其中既不包含语料库也不包含索引——并且 `build`、`claims` 和 `q` 在没有 `--db` 的情况下都失败。**在 v0.3.0 或更早的版本中，请使用上面的 `npx` 二进制文件。**

从 v0.3.1 开始，根目录是通过**测试记录**来解析的，而不是通过假设它：从检出目录内部运行任何一个命令，它会找到它；从其他任何位置运行它，它都会输出 **`4` REFUSED**，并显示它尝试过的两个目录和它查找的两个标记。现在，这两个命令都读取 `$FACET_INDEX_DB`，并且它选择哪个*索引*，而不是哪个*语料库*。在从 `main` 构建并在干净的 venv 中安装的 wheel 上进行测量——[E24](docs/experiments/E24-ruling.md)。

*此代码块已更正两次。它首先读取 `pipx install facet-mcp # 或直接安装 Python 包 `, until v0.3.0's read-back ran a **verb** instead of `--help`。然后，它说 wheel“仅适用于 `q` 和 `claims`”——**`claims` 也无法工作**，E24 通过运行它发现了这一点。这两个更正都包含在 [known-defects.md](docs/known-defects.md) 中，并附有其测量结果。*

## 当前状态

四个已接受的资源，跨越四个主题类别，无需任何积分。每个资源都由导演在其自己的缩放级别上进行评估——在 GLB 上或在全尺寸工作表中——而不是通过指标来确定是否达到阈值。

| 主题 | 类别 | 已接受 | 参考/画笔/膨胀 |
|---|---|---|---|
| **Character (W3)** | 人形生物 | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | 车辆，细长的骨架 | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | 野兽，翅膀膜 | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | 道具，近乎二维，灰度 | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

份额是有效的纹素，并且**它们不能跨主题进行比较**——一艘船在视线高度隐藏了大部分自身，而动物则隐藏了一半。将每个资源与其自身的预先注册的范围上限进行比较，结果显示它们达到 **86–93%**：行之间的差异在于几何形状，而不是回归。 [完整数字及其分母](docs/handbook/subjects.md)。

**这是一个流水线，而不是一个单字符生成器。** 如果与规范的八个命名元素相矛盾，则提示将赢得 **8 次中的 8 次**——中位 ΔE 为 46.3，而五个保留控件的中位数为 6.2——同时人物保持不变。结构由网格和控制来维持；命名的属性取决于提示。

## 该流水线

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

分阶段进行，并说明每个阶段的原因：**[手册](docs/handbook/index.md)**。

**虚线表示新的，并且故意不使用实线。** 该模型的第一个方框一直显示“粘土概念”，到目前为止，这里没有任何东西能够实现这一点——所有粘土都是手工制作的，并在过程中进行处理。现在存在一个“概念→粘土”工具，它的第一组模型已经以完整尺寸呈现：姿势、腕部绑带、腰带饰片和撕裂的下摆都已完成；鬃毛则未完成；颜色溢出测量结果为整个帧 **C\* p99.9 = 13.15**，背景为无缝的非彩色。**该模型无法展示的是网格是否会得到改进**，这是唯一能够证明其价值的问题，因此它仍然是一个候选对象，并且记录了相关证据：**[概念准备](docs/concept-prep.md)**。

## 是什么让它起作用

六个发现，每个发现都需要一次实验，并且都适用于产生它的主题之外的情况。[完整版本，包含测量结果](docs/findings.md)。

- **首先是形状，其次才是风格。** 重建器将表面噪声解读为几何体。一个干净、雕塑感十足的粘土模型，其平面经过故意夸张处理，最终呈现出比程式化的精灵更好的拓扑结构；程式化的孪生模型则与之同时生成，并成为颜色参考。
- **构建面部框架，获得面部效果。** 头部截取会使头部多出 **3.1–4.5×** 的多边形数量，并且这种差异是结构性的——分离的眼睑、眉毛皱纹、建模的鼻腔——而不是更清晰的模糊效果。
- **孪生模型属于一个网格，而不是一个角色。** 在多个网格中重复使用孪生模型会导致覆盖率下降 **62% → 22.7%**，因为手臂会投射到模型旁边的空白空间中。每次都从你即将进行纹理处理的网格中生成孪生模型。
- **身份属于提示词。** 如果提示词中没有提及某个规范元素，它就会意外出现，并且也会以同样的方式消失——当金色膝盖护甲最终仅通过损坏的 ControlNet 中的噪声出现在图像中时进行了测量。
- **询问几何体，而不是阈值。** 将键控蒙版替换为精确的光线投射轮廓，使参考覆盖率从 **28.4% 提高到 39.1%** 的有效纹素——完全是累加的，没有扩散，也没有 GPU。角中值键控在这里已经失败了三次，并且已被淘汰。
- **剔除任何相机都无法看到的区域，从图集中剔除，而不是从网格中剔除。** 49% 的图集纹素从外部不可见；排除这些面会使插值减少 **68%**。与其删除，不如排除，这样可以使失败变得不可能，而不仅仅是可检测。

## 尚未解决的问题

已命名并测量，放在首页而不是脚注中。[所有问题，位于代码中](docs/known-defects.md)。

- **一些可见的表面映射到图集空间，但没有任何烘焙操作会写入该区域**，并且呈现为图像未处理的默认黑色。Blender 的烘焙器使用纹素中心采样，因此没有与任何纹素中心重叠的三角形会被留空——它的开发者已经**命名了这种机制并合并了一个修复程序**（https://projects.blender.org/blender/blender/pulls/161752），时间是所有数据在此处测量完成后的两周。这是一种该模型的固有属性，而不是某个主题的属性：在一个资源上进行了测量，**但在其他四个资源上未进行测量**。
- **刀刃带在所有八个相机中占据 0.00% 的第一阶段参考**——钢材放置在灰色背景上，正好位于键值的阈值之上。联合操作可以恢复 55.72%。
- **笔触接缝没有对齐。** 一个来源边界会使纹理变化增加 **5.5×**；导演命名的区域则会使其增加 **9.5×**。
- **扩散会在不相关的图集岛屿之间渗漏**——74.9% 的扩散纹素从另一个岛屿获取颜色，与平均距离为 1.0 的图形上的 0.177 相差甚远。⚠ **该比例是在图集纹素中，而不是关于相机所见的内容：** 扩散占已写入图集的 26.95%，并且占渲染图形像素的 **4.95%**，比例为 0.18×。绘画存在于大型图表中，孔洞存在于小型图表中，因此在屏幕空间中，一个扩散的纹素是廉价的。
- **⚑ 决定接受的关键缺陷是由 PAINT 携带的，而不是由任何填充物携带**——区域呈现出另一种材料的颜色，而没有一种斑点统计方法能够检测到这一点。通过三种方式进行测量，在三个不同的空间中进行三次会话：**91.05% `reference`-携带，富集度为 0.99×**，与基准率完全一致；相同类别的绿色布料为 **68.46% `reference`**；并且在一个薄刀刃上，表面自身的绘制纹素的污染率为 **18.77%**，而其扩散填充物的污染率为 **5.55%**。该填充物正确地从最近的绘制邻居中获取信息——而该邻居本身已经存在问题。混合本身是一种未记录的双频带分割（`M + gaussian_blur_σ16(B − M)`），它在相同的点上测量了**四个替代方案中最差的结果**。
- **视图永远不会是独立的，这限制了所有混合修复。** 对于每个缺陷斑块，**100% 的面都具有两个或多个贡献相机，并且所有这些相机都在 90° 范围内（平均为 45°）**，并且有 21% 的缺陷面仅由一个相机看到。相邻的视图在几乎相同的控制下会同时失败，因此摄影测量学中发布的“多视角”优势不能在此处直接应用。
- **该模型中的每次重建都是一个空心双层外壳**，壁厚约为两个体素。没有体积谓词可以应用于其中任何一个。

## 如何运行此仓库

这种方法与流水线本身一样重要，并且它存在于这里是有原因的：之前的流程进行了十次会话，每次都会对自己的输出进行判断，并在下一次会话中将结论作为既定事实进行记录。该循环中的任何内容都无法进行验证。

- **先制定规范，再进行报告，最后做出裁决**——并且设计实验的环节绝不会评估其自身的结果。有四十个实验记录在[此处](docs/experiments/)。
- **更正会就地进行，与推翻它们的测量结果并列显示**，而不是以静默删除的方式呈现。仅在最初的环节中，就有六项既定主张被证明是错误的，并且这六项都仍然可以与其替代方案并排查看。
- **失败的结果将保留在代码仓库中，并附带其原因。**[`tools/superseded/`](docs/tools.md) 并非一个存档——任何人都可以运行这些工具，并观察它们以相同的方式失败。
- **负面结果就是一次完全的成功**，它会被报告和记录下来，而不是被调整到某个数值。
- **测试与修改代码相关的提交版本相关联**——在两次操作中，有 1182 个通过测试，并且对 1135 个经过严格隔离的版本进行了路径限制的 CI 测试。
- **可以查询记录。**整个过程都使用 SQLite + FTS5 索引进行验证，并在四个方面进行了验证。它发现裁决结果与文本中描述的不同，有三个地方存在差异，这是通过统计记录本身得出的。

## 所有内容都在这里

| | |
|---|---|
| **[手册](docs/handbook/index.md)** | 指南——分阶段的流程、主题和配置系统 |
| **[概念准备](docs/concept-prep.md)** | 候选粘土生成：其 Gate 0 流程、放置方式以及它所开启的许可项目 |
| **[记录](docs/experiments/)** | 四十个实验：规范、报告、裁决，以及在测量之前声明的所有预测 |
| **[流程中学到的内容](docs/findings.md)** | 持久的发现和来之不易的规则，完整呈现 |
| **[每个工具的状态](docs/tools.md)** | 哪些有效、哪些已被取代，以及每项内容的证据 |
| **[已知缺陷](docs/known-defects.md)** | 所有未解决的问题，已在代码中进行测量和定位 |
| **[事件的经过](docs/arc-history.md)** | 按时间顺序排列的历史记录，保留了更正内容 |
| **[CLAUDE.md](CLAUDE.md)** | 如何在此工作——角色、规则以及每个角色的成本 |

## 许可状态

每个阶段都在本地运行，并且在商业上是安全的：SDXL (OpenRAIL++)、MV-Adapter (开源)、open3d (Apache-2.0)、spandrel (MIT)、RealESRGAN anime6B (BSD-3)、Blender、numpy、scipy、trimesh。

有意排除，并说明原因：**nvdiffrast**（非商业用途——此处通过结构性触发器强制执行，而不是通过认证）、**Hunyuan3D-Paint**（在欧盟、英国和韩国的许可无效）、**MVPaint** 和 **TEXGen**（完全没有许可），以及 **UltraSharp / SUPIR / StableSR**（非商业放大器）。

**声明的主张范围，而不是让其自行发现。**它描述了**记录的流程**——上述图表中的各个阶段，从图像到 3D 开始。在其上游的候选粘土生成目前在一个封闭的云 API 上运行，该 API 的条款本代码仓库**尚未验证**，因此此处没有任何许可声明涵盖由其粘土制成的资产。这是一个开放项目，有明确的路径可以解决它：符合许可要求的本地模型是 **Qwen-Image-Edit (Apache-2.0)**，并且 **FLUX.1-Kontext [dev] 因与 nvdiffrast 相同的理由而被排除**——非商业权重。两者都经过了工作室的模型目录验证，而不是重新调用；其原因在[概念准备](docs/concept-prep.md)中。

## 信任和威胁模型

facet 完全在您自己的机器上运行——每个工具都是一个脚本，您可以针对您在命令行中输入的路径进行调用，因此有意义的问题不是*此应用程序请求了哪些权限*，而是*这些脚本对您的机器做了什么*。通过测量来回答，并且每次扫描都可以重新运行；完整的策略在 [SECURITY.md](SECURITY.md) 中：

- **Data touched:** meshes, textures, images and JSON on local disk, at paths you
  pass on the command line. Plus `docs/index/facet.db`, which is *derived* — it holds
  nothing that was not already a file in this repo, and `facet_index.py build`
  regenerates it from scratch.
- **Data NOT touched:** no credentials, ever. Nothing here reads, stores or transmits
  a token, key or password, and none is present in the tree — swept for
  provider-prefixed keys, GitHub PATs, Slack tokens, AWS key ids, private-key blocks,
  bearer tokens and inline `api_key`/`password` assignments, **zero matches**, no
  credential-shaped file tracked.
- **No telemetry.** None collected, none sent. There is no opt-out because there is
  nothing to opt out of.
- **Network egress:** two tools of thirty-six open a socket — `restylize_views.py`
  and `texpass_brush.py` — and both call a ComfyUI HTTP API at `--host`, **default
  `127.0.0.1:8188`**. Nothing else in `tools/` makes a network call.
- **Permissions:** ordinary user. No elevation, no service install, no system-settings
  or registry writes.

三个明显的漏洞被公开，而不是声称已被修复，因为一份仅列出保证的安全说明并不是一个威胁模型：**文件操作没有进行沙箱隔离**（工具会按照其参数指示写入任何位置）；**许多工具和文档中都嵌入了绝对本地路径**——在 26 个文件中总共出现 114 次，这并非秘密，而是对一台机器的布局的一种披露，也是大多数工具无法在其他地方未经修改运行的原因；并且，**未发布的 36 个研究脚本中的意外错误会显示为 Python 堆栈跟踪**，没有任何 `--debug` 网关。有意的停止操作是 `ANDON:` 消息，其中包含触发它们的测量结果。这就是研究工具的约定，[SHIP_GATE.md](SHIP_GATE.md) 准确地记录了何时不再满足要求——对于两个命令方面，在 0.2.0 版本中，它执行*安装*操作：`facet-index` 和 `facet-mcp` 返回 `0`（正常）/ `1`（用户错误）/ `2`（运行时错误）。并且，自从 [E22](docs/experiments/E22-ruling.md) 之后，对于触发的网关或失败的 `verify` 环节，会返回 **`4` REFUSED**，这意味着工具正在运行并告诉你不要继续，而不是出现运行时错误。所有这些都会以一种结构化的方式拒绝，并命名下一步操作，而不是显示堆栈跟踪 ([E21](docs/experiments/E21-cli-contract-report.md))。

**并且，这两个命令中的网关不再可以删除。** 在“安装”环节中，每个 ANDON 都会触发 `raise`；一个简单的 `assert` 是一个 `python -O` 会静默删除的语句，在 E22 将它们转换为当前形式之前，这个仓库中有 87 个网关可以通过环境变量来删除。在同一网关上，分别在四种解释器模式下进行测量。
**并且，自从 [E23](docs/experiments/E23-route-gates-report.md) 之后，生成四个已接受资产的路径上的网关也不再可以删除**——它有 **12 个工具中的 57 个站点**，转换为对文件进行纯粹的移动操作，而这些文件之前从未被测试过，现在每个文件都会在 `-O` 和 `PYTHONOPTIMIZE=1` 以及正常解释器下拒绝。
**并且，自从 [E25](docs/experiments/E25-ruling.md) 之后，该类别已关闭。** 它有 **43 个文件中的 133 个站点**——这些是生成上述四个已接受资产证据的测量工具，它们以相同的方式进行转换，从而使总数达到 `raise`，即 **278**。
在 `tools/` 下方，仅剩 **一个**简单的 ANDON `assert`：
`superseded/texpass_thin_mask.py`，它**永远不会**被转换，因为这些工具的目的是让任何人都可以运行它们并观察它们以相同的方式失败。这个剩余部分会通过名称固定在测试套件中，因此未来的扫描无法在不有意编辑测试的情况下将其删除。

**支持状态：** 此仓库在一个平台上由一位负责人和一个轮换的顾问和执行者团队进行开发。`main` 是唯一受支持的状态。没有发布渠道、回溯策略或 SLA——取而代之的是记录：每个声明都与其生成代码相邻，并且 [docs/experiments](docs/experiments/) 包含每个声明的规范、报告和裁决。

## 要求

Blender 5.x，Python 3.11+，以及 `numpy`、`scipy`、`trimesh`、`open3d`、`Pillow`、`spandrel` 和 `torch`。仅需要本地 ComfyUI 安装才能使用修复画笔。该项目是在 RTX 5090 上开发的；VRAM 的可用空间比原始速度更重要。

CI 在 **ubuntu-latest / Python 3.12** 上运行套件的封闭子集，并进行固定安装（`.github/workflows/ci.yml`）；工件层需要记录在 `E:\AI\training` 下的树，这些内容不在 git 中，因此 CI 会按设计选择不包含它们。本地，`python -m pytest` 运行所有 **1182** 个测试，而 `python -m pytest -m "not artifacts"` 运行 CI 重现的 **1135** 个测试。

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
