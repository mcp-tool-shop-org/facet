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
  Local hardware end to end · no non-commercial licence anywhere in the chain
</p>

---

该风格应用于**资产上**，在纹理空间中——而不是针对每个视角进行绘制，然后将它们拼接在一起。向流水线输入一个具有夸张造型的粘土概念模型，它会返回一个带有纹理的网格，其颜色来自对*该*网格的样式化参考，所有参考无法看到的区域都通过蒙版绘画笔刷和基于表面的膨胀来填充。

它的命名既包含了问题的一半：多边形，也包含了它们需要呈现的面。

## 安装

该流水线本身是一组本地脚本，您可以在输入路径时调用它们——克隆仓库并阅读[入门指南](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/)。

**记录索引以软件包的形式提供**，因此助手可以查询证据链，而不是读取它：

```bash
npx @mcptoolshop/facet          # zero-prerequisite; verified binary, no Python needed
```

有两个命令与其一起提供——`facet-mcp`，标准输入输出 MCP 服务器（六个工具，其中四面验证作为拒绝的健康表面），以及 `facet-index` (`build` / `verify` / `q` / `claims`)。从检出目录中运行它；`--db` 指的是不同的索引。

⚠ **`pip install facet-mcp` was broken in every released version through v0.3.0, and is
fixed in v0.3.1.** The wheel installs `facet_index` as a top-level module, so up to and
including v0.3.0 it resolved the record's location against `<venv>/Lib` — which holds
neither corpus nor index — and `build`, `claims`, and `q` without `--db` all failed.
**On v0.3.0 or earlier, use the `npx` binary above.**

从 v0.3.1 开始，根目录是通过**测试记录**来解析的，而不是通过假设它：从检出目录中运行任一命令，它会找到该记录；如果从其他任何位置运行，它将退出并显示 **`4` REFUSED**，同时列出它尝试过的两个目录和它查找的两个标记。
现在，这两个命令都读取 `$FACET_INDEX_DB`，并且它选择哪个*索引*，而不是哪个*语料库*。在从 `main` 构建并安装到干净虚拟环境中时进行测量——[E24](docs/experiments/E24-ruling.md)。

*此部分已更正两次。最初的文本为 `pipx install facet-mcp # 或直接安装 Python 包 `, until v0.3.0's read-back ran a **verb** instead of `--help`。
然后，它说该软件包“仅适用于 `q` 和 `claims`”——**`claims` 也无法正常工作**，E24 通过运行它发现了这一点。两次更正都包含在 [known-defects.md](docs/known-defects.md) 中，并附有相应的测量结果。*

## 当前状态

**四个已接受的资产，跨越四个主题类别，无需任何积分。** 每个资产都由导演在自己的缩放级别下进行评估——在 GLB 上或在全尺寸图纸上——而不是通过某个指标来确定是否超过阈值。

| 主题 | 类别 | 已接受 | 参考/笔刷/膨胀 |
|---|---|---|---|
| **Character (W3)** | 人形生物 | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | 车辆，细长的骨架 | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | 野兽，翅膀膜 | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | 道具，近乎二维，灰色调 | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

共享的是有效的纹素，并且**它们不能跨主题进行比较**——一艘船从视线高度隐藏了大部分自身，而动物则隐藏了一半。将每个资产与其自己预先注册的范围上限进行比较，结果显示它们达到了 **86–93%**：行之间的差异在于几何形状，而不是回归。 [完整数字及其分母](docs/handbook/subjects.md)。

**这是一个流水线，而不是一个单角色生成器。** 如果与规范的八个命名元素相矛盾，提示将赢得 **8 次中的 8 次**——中位数 ΔE 为 46.3，而五个控制组的中位数为 6.2——同时人物形象保持不变。结构由网格和控制来维持；命名的属性则取决于提示。

## 该流水线

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

分阶段进行，并附带每个阶段的理由：**[手册](docs/handbook/index.md)**。

## 使其有效的原因

六个发现，每个发现都需要一次实验，并且每个发现都适用于超出产生它的主题。 [详细版本，附带测量结果](docs/findings.md)。

- **首先是形状，然后才是风格。** 重建器会将表面噪声解读为几何形状。一个干净的、类似雕塑的粘土模型，其平面经过故意夸张处理，最终会产生比样式化的精灵更好的拓扑结构；样式化版本会在旁边生成，并成为颜色参考。
- **框定面部，获得面部。** 头部裁剪会将 **3.1–4.5 倍** 更多的多边形放置在头部上，并且这种差异是结构性的——分离的眼睑、眉毛皱纹、建模的鼻腔——而不是更清晰的模糊效果。
- **双胞胎属于网格，而不是角色。** 在不同的网格中重复使用双胞胎会导致覆盖率下降 **62% → 22.7%**，因为手臂会投射到模型旁边的空旷空间中。每次都从您即将对其进行纹理处理的网格中生成双胞胎。
- **身份属于提示。** 如果提示中没有命名某个规范元素，它将意外地出现，并且也会以同样的方式消失——当金色膝盖护板最终仅通过损坏的 ControlNet 中的噪声出现在图像中时进行了测量。
- **询问几何形状，而不是阈值。** 将键控蒙版替换为精确的光线投射轮廓，可以将参考覆盖率从 **28.4% 提高到 39.1%** 的有效纹素——完全是累加的，没有扩散，也没有 GPU。这里，角中值键控已经失败了三次，并且已被淘汰。
- **剔除任何相机都无法看到的区域，从图集中剔除，而不是从网格中删除。** 49% 的图集纹素从外部不可见；排除这些面可以减少插值 **68%**。与其删除，不如排除，这样可以将失败的可能性变为不可能，而不仅仅是可检测。

## 尚未解决的问题

已命名并测量，位于首页而不是脚注中。 [所有问题，代码位置](docs/known-defects.md)。

- **刀刃带在所有八个摄像头上占据了第一阶段参考的0.00%**——钢材置于灰色背景之上，与关键值的阈值完全一致。该组合拯救了55.72%。
- **笔触缝隙未进行平整处理。**一个来源边界呈现出**5.5倍**于普通纹理变化的程度；导演所指的区域则呈现出**9.5倍**的变化。
- **扩张导致不相关的图块岛屿之间出现渗漏**——74.9%的扩张像素从另一个图块岛屿获取颜色，与平均距离为1.0（在高度为1.0的图像上）的点相距0.177。
- **此路径上的每次重建都是一个空心双层外壳**，壁厚约为两个体素。没有体积谓词适用于其中任何一个。

## 如何运行这个仓库

这种方法既是产品，也是流程的一部分，并且它存在于某种原因：之前的流程进行了十次会话，每次都会对自己的输出进行评估并撰写结论，而这些结论会在下一次会话中被视为既定事实。该循环中的任何内容都无法进行验证。

- **先制定规范，后进行报告，最后做出裁决**——并且设计实验的会话绝不会对自己的结果进行评分。有二十三项实验记录在[此处](docs/experiments/)。
- **修正会在相应的位置进行，与推翻它们的测量结果并列显示**，而不是以静默删除的方式进行。仅在最初的会话中，就有六个继承的声明被证明是错误的，并且这六个声明仍然可以与替代它们的内容一起查看。
- **失败的结果将保留在仓库中，并附带其原因。**[`tools/superseded/`](docs/tools.md)不是一个存档——任何人都可以运行这些工具，并观察它们以相同的方式失败。
- **负面结果就是完全的成功**，它会被报告和关闭，而不是调整到某个数值。
- **测试与修改代码的代码提交相关联**——在两个人的操作下，有684个测试通过，并且对这675个经过严格测试的测试进行了路径限制的CI（持续集成）。
- **记录是可查询的。**一个SQLite + FTS5索引覆盖了整个流程，并在四个方面进行了验证。它发现了一种裁决计数，而散文在三个地点给出的数字是不正确的，这是通过对记录本身进行计数得出的。

## 所有内容的位置

| | |
|---|---|
| **[手册](docs/handbook/index.md)** | 指南——流程的各个阶段、主题和配置系统 |
| **[记录](docs/experiments/)** | 二十三项实验：规范、报告、裁决以及在进行测量之前声明的所有预测 |
| **[流程中学到的内容](docs/findings.md)** | 持久的发现和来之不易的规则，完整呈现 |
| **[每个工具的状态](docs/tools.md)** | 哪些有效，哪些已被取代，以及每种情况下的证据 |
| **[已知缺陷](docs/known-defects.md)** | 所有未解决的问题，已进行测量并在代码中定位 |
| **[流程的实际过程](docs/arc-history.md)** | 按时间顺序排列的历史记录，保留了修正内容 |
| **[CLAUDE.md](CLAUDE.md)** | 如何在此处工作——角色、规则以及每个角色的成本 |

## 许可情况

每个阶段都在本地运行，并且在商业上是安全的：SDXL (OpenRAIL++)、MV-Adapter (开源)、open3d (Apache-2.0)、spandrel (MIT)、RealESRGAN anime6B (BSD-3)、Blender、numpy、scipy、trimesh。

有意排除，并说明原因：**nvdiffrast**（非商业用途——此处通过结构性触发器强制执行，而不是通过证明），**Hunyuan3D-Paint**（在欧盟、英国和韩国的许可无效）、**MVPaint**和**TEXGen**（完全没有许可），以及**UltraSharp / SUPIR / StableSR**（非商业放大器）。

## 信任和威胁模型

facet 完全在您自己的机器上运行——每个工具都是一个脚本，您可以针对命令行中键入的路径对其进行调用，因此有意义的问题不是*此应用程序请求了哪些权限*，而是*这些脚本对您的机器做了什么*。通过测量来回答这个问题，并且每次扫描都可以重新运行；完整的策略在[SECURITY.md](SECURITY.md)中：

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

公开了三个明显的漏洞，而不是声称它们已被修复，因为仅列出保证的安全说明并不是一个威胁模型：**文件操作没有进行沙箱隔离**（工具会按照其参数指示写入任何位置）；**许多工具和文档中都使用了绝对本地路径**——在 26 个文件中总共出现了 114 次，这并非秘密，而是对一台机器的布局的一种披露，也是大多数工具无法在其他地方未经修改运行的原因；并且，**未发布的 34 个研究脚本中的意外错误会显示为 Python 堆栈跟踪**，没有任何 `--debug` 门控。有意的停止操作是 `ANDON:` 消息，其中包含触发它们的测量结果。这就是研究工具的契约，[SHIP_GATE.md](SHIP_GATE.md) 准确地记录了何时不再满足要求——对于两个命令方面而言，在版本 0.2.0 时：`facet-index` 和 `facet-mcp` 返回 `0`（正常）/ `1`（用户错误）/ `2`（运行时错误）。并且，自从 [E22](docs/experiments/E22-ruling.md) 之后，对于触发的门控或失败的 `verify` 环节，会返回 **`4` REFUSED**，这意味着工具正在运行并告知您不要继续操作，而不是出现运行时错误。所有这些都会以结构化的方式拒绝，并命名下一步骤，而不是显示堆栈跟踪 ([E21](docs/experiments/E21-cli-contract-report.md))。

**并且，这两个命令中的门控不再可以删除。** 在“安装”方面，每个 ANDON 都会触发 `raise`；一个简单的 `assert` 是一个语句，它会静默地移除 `python -O`，在 E22 将它们转换为当前形式之前，此仓库中有 87 个门控可以通过环境变量来删除。在同一门控上，分别在四种解释器模式下进行了测量。
**并且，自从 [E23](docs/experiments/E23-route-gates-report.md) 之后，生成四个已接受资产的路径上的门控也不再可以删除**——它有 **12 个工具中的 57 个站点**，转换为对文件的纯粹移动操作，而这些文件之前从未被测试过，现在每个文件都会在 `-O` 和 `PYTHONOPTIMIZE=1` 以及正常解释器下拒绝。
**剩余研究工具中仍有 134 个门控是断言**——在这里命名而不是省略，范围由 [E22 Ruling 4](docs/experiments/E22-ruling.md) 定义，并且它们都不在“安装”命令方面：其中 132 个是在 `diagnostics/` 下的测量工具，一个是一个渲染检查，而 `superseded/` 的那个**永远不会**被转换，因为这些工具是为所有人设计的，以便他们可以运行这些工具并以相同的方式观察它们的失败。

**支持状态：** 此仓库采用开放方式进行开发，在一个平台上由一位负责人和一个轮换的顾问和执行者团队共同完成。`main` 是唯一受支持的状态。没有发布渠道、回溯策略或 SLA——取而代之的是记录：每个声明都与其生成代码相邻，并且 [docs/experiments](docs/experiments/) 包含每个声明的规范、报告和裁决。

## 要求

Blender 5.x，Python 3.11+，以及 `numpy`、`scipy`、`trimesh`、`open3d`、`Pillow`、`spandrel` 和 `torch`。仅需要本地 ComfyUI 安装才能使用修复画笔。针对 RTX 5090 进行开发；VRAM 的可用空间比原始速度更重要。

CI 在 **ubuntu-latest / Python 3.12** 上运行该套件的封闭子集，并使用固定的安装（`.github/workflows/ci.yml`）；工件层需要记录在 `E:\AI\training` 下的树，这些树不在 git 中，因此 CI 会按设计选择不包含它们。
本地，`python -m pytest` 运行所有 **684 个** 测试，而 `python -m pytest -m "not artifacts"` 运行 CI 重现的 **675 个** 测试。

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
