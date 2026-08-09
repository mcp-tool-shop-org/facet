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

该风格应用于**资产上**，在纹理空间中——而不是针对每个视角进行绘制，然后将它们拼接在一起。向流水线输入一个具有夸张外形的粘土概念模型，它会返回一个带有纹理的网格，其颜色来自对*该*网格的样式化参考，所有参考无法看到的部分都通过蒙版修复画笔和基于表面的膨胀来填充。

它的命名既包含了问题的一半（多边形），也包含了它们需要呈现的面。

## 安装

该流水线本身是一组本地脚本，您可以在输入路径时调用它们——克隆仓库并阅读[入门指南](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/)。

**记录索引以软件包的形式提供**，因此助手可以查询证据链，而不是读取它：

```bash
npx @mcptoolshop/facet          # zero-prerequisite; verified binary, no Python needed
pipx install facet-mcp          # or the Python package directly
```

其中包含两个命令——`facet-mcp`，即 stdio MCP 服务器（六个工具，其中四面验证作为拒绝的健康表面），以及 `facet-index` (`build` / `verify` / `q` / `claims`)。将两者指向带有 `--db` 或 `$FACET_INDEX_DB` 的索引。

## 当前状态

**四个已接受的资产，跨越四个主题类别，无需任何积分。** 每个都由导演在自己的缩放级别上进行评估——在 GLB 上或在全尺寸图纸上——而不是通过一个阈值来衡量。

| 主题 | 类别 | 已接受 | 参考/画笔/膨胀 |
|---|---|---|---|
| **Character (W3)** | 人形 | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | 车辆，精简的骨骼结构 | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | 野兽，翼膜 | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | 道具，接近 2D，灰色调 | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

共享的是有效的纹素，并且**它们不能跨主题进行比较**——一艘船从视平线以上隐藏了大部分自身，而动物则隐藏了一半。将每个模型与其自身的预注册范围上限进行对比，由此得出其覆盖率达到 **86–93%**：行之间的差异在于几何结构，而不是回归。 [完整数据，及其分母](docs/handbook/subjects.md)。

**这是一个流水线，而不是一个单角色生成器。** 如果与规范中的八个命名元素相矛盾，提示将赢得 **8 次中的 8 次**——中位数 ΔE 为 46.3，而五个已设定的控制组为 6.2——同时人物形象保持不变。结构由网格和控制来维持；命名的属性则受提示的驱动。

## 该流水线

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

分阶段进行，并说明每个阶段的原因：**[手册](docs/handbook/index.md)**。

## 使其有效的原因

六个发现，每个发现都需要一次实验，并且每个发现都超出了产生它的主题的范围。[详细版本，包含测量数据](docs/findings.md)。

- **首先是形状，然后才是风格。** 重建器将表面噪声视为几何体。一个干净、雕塑般的粘土模型，其平面经过精心夸张处理，比一个程式化的精灵具有更好的拓扑结构；样式化后的孪生模型会同时生成，并成为颜色参考。
- **框定面部，获得面部。** 头部裁剪会将 **3.1–4.5 倍** 更多的多边形放置在头部上，并且这种差异是结构性的——分离的眼睑、眉毛皱纹、建模的鼻腔——而不是更清晰的模糊效果。
- **孪生模型属于网格，而不是角色。** 在不同的网格中重复使用孪生模型会导致覆盖率下降 **62% → 22.7%**，因为手臂会投射到模型旁边的空旷空间中。每次都从您即将对其进行纹理处理的网格中生成孪生模型。
- **身份属于提示。** 如果提示中没有提及规范元素，它将意外出现，并且也会以同样的方式消失——当金色膝盖护甲最终仅通过损坏的 ControlNet 中的噪声出现在图像中时，进行了测量。
- **询问几何体，而不是阈值。** 将键控蒙版替换为精确的光线投射轮廓，可以将参考覆盖率从 **28.4% 提高到 39.1%** 的有效纹素——完全是累加的，没有扩散，也没有 GPU。角落中值键控在此处已经失败了三次，并且已被淘汰。
- **剔除任何相机都无法看到的区域，从图集中剔除，而不是从网格中删除。** 49% 的图集纹素从外部不可见；排除这些面可以使插值减少 **68%**。与其删除，不如排除，这样可以将失败的可能性变为不可能，而不仅仅是可检测。

## 尚未解决的问题

已命名并测量，位于首页而不是脚注中。[所有问题，位于代码中](docs/known-defects.md)。

- **刀片带在所有八个相机上的第一阶段参考中所占比例为 0.00%**——钢材放置在灰色背景上，正好落在键的阈值上。联合处理可以挽救 55.72%。
- **笔触接缝没有平滑处理。** 一个来源边界会产生 **5.5 倍** 的普通纹理变化；导演命名的区域则会产生 **9.5 倍** 的变化。
- **膨胀会在不相关的图集岛屿之间泄漏**——74.9% 的膨胀纹素从另一个岛屿获取颜色，与一个高度为 1.0 的图形相比，中位距离为 0.177。
- **此流水线中的每次重建都是一个空心双层外壳**，壁厚约为两个体素。没有体积谓词对其中任何一个有效。

## 如何运行该仓库

这种方法与流水线本身一样重要，并且它存在于这里是有原因的：之前的流程进行了十次会话，每次会话都对其自身的输出进行评估，并在下一次会话中将结论作为既定事实进行记录。在那个循环中，没有任何东西可以被检查。

- **先制定规范，再进行报告，最后做出裁决**——并且设计实验的环节绝不会对自身的结果进行评估。目前有二十三项实验记录在[此处](docs/experiments/)。
- **修正会直接应用到相应位置，与导致其被修改的测量结果并列显示**，而不是以静默删除的方式进行。仅在最初的环节中，就有六个既定结论被证明是错误的，并且这六个结论仍然可以与替代它们的内容一起查看。
- **失败的结果会保留在代码仓库中，并附带其原因。**[`tools/superseded/`](docs/tools.md) 并非一个存档——任何人都可以运行这些工具，并观察它们以相同的方式失败。
- **负面结果也是一种完全的成功**，它会被报告和记录下来，而不是被调整到某个数值。
- **测试会与修改代码的提交版本相关联**——共有648个通过测试，由两个团队共同完成，并且在640个独立的测试中使用了路径限制的持续集成（CI）。
- **可以查询记录。**对整个过程进行 SQLite + FTS5 索引处理，并在四个方面进行了验证。它发现裁决结果与文本描述不符，具体体现在三个位置，这是通过统计记录本身得出的。

## 所有内容都位于

| | |
|---|---|
| **[手册](docs/handbook/index.md)** | 指南——分阶段的流程、主题和配置系统 |
| **[记录](docs/experiments/)** | 二十三项实验：规范、报告、裁决以及在测量之前声明的所有预测 |
| **[流程中学到的内容](docs/findings.md)** | 持久的发现和来之不易的规则，完整呈现 |
| **[每个工具的状态](docs/tools.md)** | 哪些有效、哪些已被取代以及各自的证据 |
| **[已知缺陷](docs/known-defects.md)** | 所有尚未解决的问题，已在代码中进行测量和定位 |
| **[事件经过](docs/arc-history.md)** | 按时间顺序排列的历史记录，保留了所有的修正 |
| **[CLAUDE.md](CLAUDE.md)** | 如何在此工作——角色、规则以及每个角色的成本 |

## 许可声明

所有阶段都在本地运行，并且在商业上是安全的：SDXL (OpenRAIL++)、MV-Adapter (开源)、open3d (Apache-2.0)、spandrel (MIT)、RealESRGAN anime6B (BSD-3)、Blender、numpy、scipy、trimesh。

故意排除，并说明原因：**nvdiffrast**（非商业用途——在此通过结构性触发器强制执行，而不是通过证明），**Hunyuan3D-Paint**（在欧盟、英国和韩国的许可无效）、**MVPaint** 和 **TEXGen**（完全没有许可）以及 **UltraSharp / SUPIR / StableSR**（非商业用途的图像增强工具）。

## 信任与威胁模型

facet 完全在您自己的机器上运行——每个工具都是一个脚本，您可以针对命令行中输入的路径进行调用，因此有意义的问题不是*此应用程序请求了哪些权限*，而是*这些脚本会对您的机器做什么*。通过测量来回答这个问题，并且每次测试都可以重新运行；完整的策略位于[SECURITY.md](SECURITY.md) 中：

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

**并且，这两个命令中的门不再可以删除。** 每个 ANDON 在其对应的模块中安装 `raise`；一个简单的 `assert` 是一个语句，它会静默地移除 `python -O`，而此仓库的 87 个门，在 E22 版本之前可以通过环境变量进行删除。在同一门上分别测量了转换前后的结果，使用了四种解释器模式。
**并且，自从 [E23](docs/experiments/E23-route-gates-report.md) 之后，生成这四个已接受的资源的路线上也不再可以删除这些门**——它包含 **十二个工具中的 57 个站点**，转换为对文件进行纯粹的移动操作，而这些文件之前从未被测试过，现在每个文件都会在 `-O` 和 `PYTHONOPTIMIZE=1` 以及正常解释器下拒绝执行。
**剩余研究工具中仍有 134 个门是断言**——在这里列出而不是省略，范围由 [E22 Ruling 4](docs/experiments/E22-ruling.md) 定义，并且它们都不在命令模块的安装过程中：其中 132 个是在 `diagnostics/` 下的测量工具，一个是渲染检查，而 `superseded/` 的一个**从不**进行转换，因为这些工具被保留下来，以便任何人都可以运行它们并观察它们以相同的方式失败。

**支持状态：** 此仓库在一个平台上由一位负责人和一个轮换的顾问和执行者团队共同开发。`main` 是唯一受支持的状态。没有发布渠道、回溯策略或 SLA——取而代之的是记录：每个声明都与其生成代码相邻，并且 [docs/experiments](docs/experiments/) 包含每个声明的规范、报告和裁决。

## 要求

Blender 5.x，Python 3.11+ 以及 `numpy`、`scipy`、`trimesh`、`open3d`、`Pillow`、`spandrel` 和 `torch`。仅需要本地安装 ComfyUI 来使用修复画笔。该项目基于 RTX 5090 进行开发；显存容量比原始速度更重要。

CI 在 **ubuntu-latest / Python 3.12** 上运行测试套件的封闭子集，并固定安装版本（`.github/workflows/ci.yml`）；工件层需要记录在 `E:\AI\training` 下的树，这些树不在 git 中，因此 CI 会按设计选择不包含它们。本地，`python -m pytest` 运行所有 **648 个** 测试，而 `python -m pytest -m "not artifacts"` 运行 **640 个** CI 重现的测试。

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
