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

该风格应用于**资源上**，在纹理空间中——而不是针对每个视角进行绘制，然后将它们拼接在一起。向流水线输入一个具有夸张形式的粘土概念模型，它会返回一个带有纹理的网格，其颜色来自对*该*网格的样式化参考，所有参考无法看到的部分都通过蒙版涂抹笔刷和感知表面的膨胀来填充。

名称既指问题的一半：多边形，也指它们需要呈现的面。

## 安装

该流水线本身是一组本地脚本，您可以在键入的路径上调用这些脚本——克隆仓库并阅读[入门指南](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/)。

**两个服务器以软件包的形式提供**——记录索引，因此助手可以查询证据链，而不是读取它；以及**从 v0.4.0 版本开始，测量服务器**，因此间隔几个月测量的两个资源将通过一个代码路径进行处理。

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` 是针对记录的 stdio MCP 服务器（六个工具，其中四足验证作为拒绝健康表面的工具），而 `facet-index` 本身是索引（`build` / `verify` / `q` / `claims`）。从检出目录内部运行任何一个；`--db` 指的是不同的索引。

### 测量服务器——v0.4.0 版本的新功能

`facet-measure` 回答了比较的**数值部分**，并且不会说明输出是否良好。每个有效负载都包含服务器版本、仪器的文件哈希值和配置哈希值，并且 `measure_report` **拒绝**跨不匹配进行比较——这是整个系统存在的目的。

通过运行一个**动词**而不是 `--help` 来验证——控制网格返回 786,432 个面，并在没有检出目录的机器上具有完整的身份包围。

**您获得的结果取决于一件事，那就是您的 Python 版本：**

| 您的 Python | `[measure-full]` 提供了 |
|---|---|
| **3.11 / 3.12** | **所有八个工具**——`open3d` 从 PyPI 安装 |
| **3.13** | 四个工具；`mesh_stats`、`mesh_topology`、`measure_report`、`anchor_check` |

`open3d` 0.19.0 是最新的*发布版*，并发布了 cp38–cp312 wheels，**没有 sdist**，因此在 3.13 上，PyPI 上没有任何内容可以安装。额外的组件将其置于 `python_version < "3.13"` 之后，因此安装在那里**成功**，并且四个几何工具会输出 **`4` REFUSED**，表明它们需要什么——而不是整个安装失败。

**要在 Python 3.13 上获得所有八个工具**，Open3D 在其持续的开发通道上发布了当前的 cp313 wheels。在命令行中可以使用直接 URL；它只是禁止在已发布的软件包元数据中使用：

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **在 Windows 和 macOS 上，开发 wheels 的后缀为 `+<sha>`**（撰写本文时为 `open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl`），并且名称会随着 `main` 的变化而变化——列出 [`main-devel` 发布版](https://github.com/isl-org/Open3D/releases/tag/main-devel) 中的资源，并选择当前版本。**此构建是本流水线中所有依赖于 open3d 的数字所依据的测量标准**，并且它是一个真正的可比性边界：身份包围记录仪器的哈希值，而不是其依赖项——[E31](docs/experiments/E31-ruling.md)。

*在 v0.3.1 之前，wheel 包含两个 `.py` 文件，并且不包含任何测量仪器，因此安装的测量服务器没有任何内容可以调用。没有人注意到这一点，因为这个仓库本身就是检出目录：该工具在其构建的位置工作，并且从未位于其他位置。*

⚠ **在所有已发布版本中，直到 v0.3.0，`pip install facet-mcp` 都有问题，并在 v0.3.1 中修复。** wheel 将 `facet_index` 作为顶级模块进行安装，因此，到包括 v0.3.0 在内的所有版本，它都会根据 `<venv>/Lib` 解析记录的位置——该位置既不包含语料库也不包含索引——并且 `build`、`claims` 和 `q` 在没有 `--db` 的情况下都失败。**在 v0.3.0 或更早的版本中，请使用上面的 `npx` 二进制文件。**

从 v0.3.1 开始，根目录通过**测试记录**来解析，而不是假设它：从检出目录内部运行任何一个命令，它会找到该目录；如果从其他位置运行，它将输出 **`4` REFUSED**，并显示它尝试的两个目录和它查找的两个标记。现在这两个命令都读取 `$FACET_INDEX_DB`，并且它选择哪个*索引*，而不是哪个*语料库*。在从 `main` 构建并在干净的 venv 中安装的 wheel 上进行测量——[E24](docs/experiments/E24-ruling.md)。

*此代码块已更正两次。它首先读取 `pipx install facet-mcp # 或直接安装 Python 包 `, until v0.3.0's read-back ran a **verb** instead of `--help`。然后，它说 wheel“仅适用于 `q` 和 `claims`”——**`claims` 也无法工作**，E24 通过运行它发现了这一点。这两个更正都包含在 [known-defects.md](docs/known-defects.md) 中，并附带了它们的测量结果。*

## 当前状态

**四个已接受的资源，跨越四个主题类别，无需任何积分。**每个资源都由导演在其自己的缩放级别上进行评估——在 GLB 上或在全尺寸工作表中——而不是通过指标来确定是否超过阈值。

| 主题 | 类别 | 已接受 | 参考/笔刷/膨胀 |
|---|---|---|---|
| **Character (W3)** | 人形生物 | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | 车辆，细长的骨架 | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | 野兽，翅膀膜 | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | 道具，近乎二维，灰度 | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

共享的是有效的纹素，并且**它们不能跨主题进行比较**——一艘船从视平线隐藏了大部分自身，而动物则隐藏了一半。将每个资源与其自己预先注册的范围上限进行比较，结果显示它们达到了 **86–93%**：行之间的差异在于几何形状，而不是回归。 [完整数字及其分母](docs/handbook/subjects.md)。

**这是一个流水线，而不是一个单字符生成器。**如果与八个命名元素指定的规范相矛盾，则提示将赢得 **8 次中的 8 次**——中位 ΔE 为 46.3，而五个保留的对照组为 6.2——同时人物保持不变。结构由网格和控制来维持；命名的属性取决于提示。

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

**虚线轮廓是新的，并且有意不是实心的。** 该流水线的第一个环节一直显示“粘土概念”，到目前为止，这里没有任何东西能够实现这一点——所有的粘土都是手工制作的，并在运送过程中进行处理。现在存在一个“概念→粘土”工具，它的第一个版本已经完成了完整尺寸的测试：姿势、腕部绑带、腰带饰片和撕裂的下摆都已呈现；鬃毛则没有呈现；颜色泄漏在整个画面中测量得出 **C\* p99.9 = 13.15**，背景为无缝的非彩色。**该版本无法展示的是网格是否会得到改进**，这是唯一能够证明其价值的问题，因此它仍然是一个候选方案，并且记录了相关证据：**[概念准备](docs/concept-prep.md)**。

## 是什么让它起作用

六个发现，每个发现都需要一次实验，并且每个发现都适用于超出其产生对象的范围。[完整版本，包含测量数据](docs/findings.md)。

- **先是形状，后才是风格。** 重建器将表面噪声解读为几何体。一个干净、雕塑感十足的粘土模型，并且故意夸大了平面，其拓扑结构会比程式化的精灵更好；程式化的孪生版本会在旁边生成，并成为颜色参考。
- **突出面部轮廓，获得面部特征。** 头部裁剪会将 **3.1–4.5×** 更多的多边形放置在头部上，并且这种差异是结构性的——分离的眼睑、眉毛皱纹、建模的鼻腔——而不是更清晰的模糊效果。
- **孪生模型属于一个网格，而不是一个角色。** 在多个网格中重复使用孪生模型会导致覆盖率下降 **62% → 22.7%**，因为手臂会投射到模型旁边的空白空间中。每次都从你即将进行纹理处理的网格中生成孪生模型。
- **身份属于提示词。** 如果提示词中没有提及某个规范元素，它就会意外出现，并且也会以同样的方式消失——当金色膝盖护甲最终仅通过损坏的 ControlNet 中的噪声出现在图像中时，会对其进行测量。
- **询问几何体，而不是阈值。** 将键控蒙版替换为精确的光线投射轮廓，会将参考覆盖率从 **28.4% 提高到 39.1%** 的有效纹素——完全是累加的，没有扩散，也没有 GPU。角中值键控在这里已经失败了三次，并且已被淘汰。
- **剔除任何相机都无法看到的物体，从图集中剔除，而不是从网格中删除。** 49% 的图集纹素从外部不可见；排除这些面会使插值减少 **68%**。与其删除，不如排除，这样可以使失败变得不可能，而不仅仅是可检测。

## 尚未解决的问题

已命名并测量，在首页而不是脚注中。[所有问题都位于代码中](docs/known-defects.md)。

- **刀刃带占所有八个相机的第一阶段参考的 0.00%**——钢材放置在灰色背景上，正好落在键值的阈值上。联合处理可以挽救 55.72%。
- **笔触接缝没有对齐。** 一个来源边界会使纹理变化增加 **5.5×**；导演所指的区域会增加 **9.5×**。
- **膨胀会在不相关的图集岛屿之间渗漏**——74.9% 的膨胀纹素会从另一个岛屿获取颜色，与平均距离为 1.0 个单位的身高上的 0.177 相差甚远。
- **此流水线中的每次重建都是一个空心双层外壳**，壁厚约为两个体素。没有体积谓词适用于其中任何一个。

## 如何运行这个仓库

这种方法与流水线本身一样重要，并且它存在于这里是有原因的：之前的流程进行了十次会话，每次都会对自己的输出进行评估，并在下一次会话中将结论作为既定事实。该循环中的任何内容都无法验证。

- **先制定规范，后进行工作，最后进行裁决**——并且设计实验的会话绝不会对其自身的结果进行评分。三十一个实验都在 [记录](docs/experiments/) 中。
- **更正会就地进行，与推翻它们的测量结果并列显示**，而不是作为静默删除。仅在最初的会话中，就有六个继承的声明被证明是错误的，并且这六个声明仍然可以与替代它们的内容一起查看。
- **失败会在仓库中保留其原因。** [`tools/superseded/`](docs/tools.md) 不是一个存档——任何人都可以运行这些工具并观察它们以相同的方式失败。
- **负面结果就是完全的成功**，报告并关闭，而不是调整到某个数字。
- **测试会与触及代码的提交一起进行**——在两个人的手中，有 1072 个通过测试，并且对 1027 个封闭的测试进行了路径门控 CI。
- **记录是可查询的。** 一个 SQLite + FTS5 索引覆盖了整个流程，并在四个方面进行了验证。它通过统计记录本身，发现了散文中错误的三处裁决计数。

## 所有内容的位置

| | |
|---|---|
| **[手册](docs/handbook/index.md)** | 指南——流水线的各个阶段、主题和配置文件系统 |
| **[概念准备](docs/concept-prep.md)** | 候选粘土轮廓：其 Gate 0 测试、放置以及它解锁的许可项目 |
| **[记录](docs/experiments/)** | 三十一个实验：规范、报告、裁决和所有在测量之前声明的预测 |
| **[流水线所学到的内容](docs/findings.md)** | 持久的发现和来之不易的规则，完整呈现 |
| **[每个工具的状态](docs/tools.md)** | 哪些有效，哪些已被取代，以及每种工具的证据 |
| **[已知缺陷](docs/known-defects.md)** | 所有未解决的问题，已测量并位于代码中 |
| **[流程的历史](docs/arc-history.md)** | 按时间顺序排列的历史记录，更正内容保留 |
| **[CLAUDE.md](CLAUDE.md)** | 如何在这里工作——角色、规则以及每个角色所付出的代价 |

## 许可声明

每个阶段都在本地运行，并且在商业上是安全的：SDXL (OpenRAIL++)、MV-Adapter（开源）、open3d（Apache-2.0）、spandrel（MIT）、RealESRGAN anime6B（BSD-3）、Blender、numpy、scipy、trimesh。

有意识地排除了一些内容，原因如下：**nvdiffrast**（非商业用途——此处通过结构性安全机制强制执行，而非通过认证），**Hunyuan3D-Paint**（在欧盟、英国和韩国的许可无效），**MVPaint** 和 **TEXGen**（完全没有许可证），以及 **UltraSharp / SUPIR / StableSR**（非商业用途的图像增强工具）。

**声明的范围，是明确说明的，而不是留待发现。** 它描述了**记录的流程**——即上述图中的各个阶段，从图像到 3D 开始。目前，在其上游运行的候选 clay-prep 步骤是在一个封闭的云 API 上运行的，该 API 的条款本仓库**尚未验证**，因此，此处没有任何许可声明涵盖了由其 clay 生成的资产。这是一个开放的问题，并且有一个明确的路径可以解决它：符合许可要求的本地模型是 **Qwen-Image-Edit (Apache-2.0)**，并且 **FLUX.1-Kontext [dev] 因与 nvdiffrast 相同的理由而被排除**——非商业用途的权重。两者都经过了与工作室的模型目录进行对比验证，而不是简单地回忆；其推理过程在 [概念准备](docs/concept-prep.md) 中。

## 信任和威胁模型

facet 完全在您自己的机器上运行——每个工具都是一个脚本，您可以针对您输入的路径来调用它，因此，有意义的问题不是*此应用程序请求了哪些权限*，而是*这些脚本对您的机器做了什么*。通过测量来回答这个问题，并且每次扫描都可以重新运行；完整的策略在 [SECURITY.md](SECURITY.md) 中：

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
- **Network egress:** two tools of thirty-four open a socket — `restylize_views.py`
  and `texpass_brush.py` — and both call a ComfyUI HTTP API at `--host`, **default
  `127.0.0.1:8188`**. Nothing else in `tools/` makes a network call.
- **Permissions:** ordinary user. No elevation, no service install, no system-settings
  or registry writes.

与其声称某些内容不存在，不如明确披露三个关键点，因为仅列出保证的安全说明并不是一个威胁模型：**文件操作没有进行沙箱隔离**（工具会在其参数指示的位置进行写入）；**许多工具和文档中都嵌入了绝对本地路径**——在 26 个文件中总共出现 114 次，这并非秘密，而是对一台机器的布局的披露，也是大多数工具无法在其他地方未经修改运行的原因；并且 **意外故障会以 Python 回溯的形式出现在 34 个未发布的实验脚本中**，没有 `--debug` 网关。有意的停止操作是 `ANDON:` 消息，其中包含触发它们的测量结果。这就是研究工具的约定，[SHIP_GATE.md](SHIP_GATE.md) 记录了何时不再满足要求——对于 facet *安装*的两个命令，在 0.2.0 版本时：`facet-index` 和 `facet-mcp` 返回 `0`（正常）/ `1`（用户错误）/ `2`（运行时错误），并且自从 [E22](docs/experiments/E22-ruling.md) 之后，**对于触发的网关或失败的 `verify` 步骤，返回 `4` (拒绝)**，这意味着工具正在工作并告诉您不要继续操作，而不是出现运行时错误。所有这些都会以结构化的方式失败，并命名下一个步骤，而不是显示回溯 ([E21](docs/experiments/E21-cli-contract-report.md))。

**并且这两个命令中的网关不再可以删除。** facet 安装的每个 ANDON 都会包含 `raise`；一个简单的 `assert` 表示 `python -O` 会静默地删除，并且在 E22 将它们转换为之前，本仓库中有 87 个网关可以通过环境变量来删除。在相同的网关上，以四种解释器模式进行了测量，分别在转换前后进行。
**并且自从 [E23](docs/experiments/E23-route-gates-report.md) 之后，生成四个已接受资产的流程中的网关也不再可以删除**——其 **跨越十二个工具的 57 个站点**，以纯粹的文件移动方式进行转换，现在每个站点都会在 `-O` 和 `PYTHONOPTIMIZE=1` 以及在正常解释器下拒绝。
**并且自从 [E25](docs/experiments/E25-ruling.md) 之后，该类别已经关闭。** 其 **跨越 43 个文件的 133 个站点**——用于生成上述四个已接受资产的证据的研究工具——以相同的方式进行转换，从而使总数达到 `raise`，即 **278**。
确切地只有一个 ANDON `assert` 存在于 `tools/` 下：
`superseded/texpass_thin_mask.py`，它**永远不会**被转换，因为这些工具会保留下来，以便任何人都可以运行它们并观察它们以相同的方式失败。剩余的部分通过名称固定在测试套件中，因此未来的扫描无法在不故意编辑测试的情况下将其删除。

**支持状态：** 本仓库在一个平台上进行开放式开发，由一位主管和一对轮换的顾问/执行者组成。`main` 是唯一受支持的状态。没有发布渠道、回溯策略或 SLA——取而代之的是记录：每个声明都与其生成它的代码并置，并且 [docs/experiments](docs/experiments/) 包含每个声明的规范、报告和裁决。

## 要求

Blender 5.x、Python 3.11+ 以及 `numpy`、`scipy`、`trimesh`、`open3d`、`Pillow`、`spandrel` 和 `torch`。仅对绘画笔刷需要一个本地的 ComfyUI 安装。
在 RTX 5090 上进行开发；VRAM 的可用空间比原始速度更重要。

持续集成（CI）在 **ubuntu-latest / Python 3.12** 环境下运行该测试套件的精简版本，并使用固定版本的安装包（`.github/workflows/ci.yml`）；工件层需要记录在 `E:\AI\training` 中的代码库，这些代码库不在 Git 中，因此 CI 会有意地将其排除。
在本地环境中，`python -m pytest` 将运行所有 **1072** 个测试用例，而 `python -m pytest -m "not artifacts"` 则会运行 **1027** 个 CI 重现的测试用例。

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
