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

该风格应用于**资产上**，在纹理空间中——而不是针对每个视角进行绘制，然后将它们拼接在一起。向流水线输入一个具有夸张外形的粘土概念模型，它会返回一个带有纹理的网格，其颜色来自对*该*网格的样式化参考，所有参考无法看到的部分都通过蒙版绘画笔刷和感知表面的膨胀来填充。

名称既指问题的一半：多边形，也指它们需要呈现的面。

## 安装

该流水线本身是一组本地脚本，您可以在键入的路径上调用这些脚本——克隆仓库并阅读[入门指南](https://mcp-tool-shop-org.github.io/facet/handbook/getting-started/)。

**两个服务器以软件包的形式提供**——记录索引，因此助手可以查询证据链，而不是读取它；以及**从 v0.4.0 版本开始，测量服务器**，这样两个相隔几个月测量的资产将通过一个代码路径进行处理。

```bash
npx @mcptoolshop/facet               # the record index; zero-prerequisite, no Python needed
pip install facet-mcp[measure-full]  # + the measurement tools and their instruments
```

`facet-mcp` 是针对记录的 stdio MCP 服务器（六个工具，其中四足验证作为拒绝健康表面的工具），而 `facet-index` 本身就是索引（`build` / `verify` / `q` / `claims`）。从检出目录内部运行任何一个；`--db` 指的是不同的索引。

### 测量服务器——v0.4.0 版本的新功能

`facet-measure` 回答了比较的**数值部分**，并且不会说明输出是否良好。每个有效负载都包含服务器版本、仪器的文件哈希值和配置哈希值，并且 `measure_report` **拒绝**跨不匹配进行比较——这是整个系统存在的目的。

通过运行一个**动词**而不是 `--help` 来验证——控制网格返回 786,432 个面，并在没有检出目录的机器上具有完整的身份包围。

**您获得的结果取决于一件事，那就是您的 Python 版本：**

| 您的 Python | `[measure-full]` 提供了 |
|---|---|
| **3.11 / 3.12** | **所有八个工具**——`open3d` 从 PyPI 安装 |
| **3.13** | 四个工具；`mesh_stats`、`mesh_topology`、`measure_report`、`anchor_check` |

`open3d` 0.19.0 是最新的*发布版*，并发布了 cp38–cp312 wheels，**没有 sdist**，因此在 3.13 上，PyPI 上没有任何内容可以安装。额外的文件将其包含在 `python_version < "3.13"` 之后，因此安装在那里**成功**，并且这四个几何工具会输出 **`4` REFUSED**，表明它们需要什么——而不是整个安装失败。

**要在 Python 3.13 上获得所有八个工具**，Open3D 在其持续的开发通道上发布了当前的 cp313 wheels。在命令行中使用直接 URL 即可；它只是禁止在已发布的包元数据中进行操作：

```bash
# Linux — stable filename, no build hash
pip install https://github.com/isl-org/Open3D/releases/download/main-devel/open3d-0.19.0-cp313-cp313-manylinux_2_35_x86_64.whl
```

⚠ **在 Windows 和 macOS 上，开发 wheels 的后缀为 `+<sha>`**（撰写本文时为 `open3d-0.19.0+63e30be-cp313-cp313-win_amd64.whl`），并且名称会随着 `main` 的变化而变化——列出 [`main-devel` 发布版](https://github.com/isl-org/Open3D/releases/tag/main-devel) 中的资产，并选择当前版本。**此构建是本流水线中所有依赖于 open3d 的数字所依据的测量标准**，并且它是一个真正的可比性边界：身份包围记录仪器的哈希值，而不是其依赖项——[E31](docs/experiments/E31-ruling.md)。

*在 v0.3.1 之前，wheel 包含两个 `.py` 文件，并且不包含任何测量仪器，因此安装的测量服务器没有任何内容可以调用。没有人注意到这一点，因为这个仓库就是检出目录：该工具在其构建的位置工作，并且从未在其他地方使用过。*

⚠ **`pip install facet-mcp` 在所有已发布版本中都存在问题，直到 v0.3.0 为止，并在 v0.3.1 中修复。** wheel 将 `facet_index` 作为顶级模块进行安装，因此在 v0.3.0 及更早的版本中，它会根据 `<venv>/Lib` 解析记录的位置——该文件既不包含语料库也不包含索引——并且 `build`、`claims` 和 `q` 在没有 `--db` 的情况下都会失败。**在 v0.3.0 或更早版本上，请使用上面的 `npx` 二进制文件。**

从 v0.3.1 开始，根目录是通过**测试记录是否存在**而不是假设它来解析的：从检出目录内部运行任何一个命令，它会找到该目录；从其他任何位置运行它，它将输出 **`4` REFUSED**，并显示它尝试过的两个目录和它查找的两个标记。现在这两个命令都读取 `$FACET_INDEX_DB`，并且它选择哪个*索引*，而不是哪个*语料库*。在从 `main` 构建并在干净的 venv 中安装的 wheel 上进行测量——[E24](docs/experiments/E24-ruling.md)。

*此代码块已更正两次。它最初读取 `pipx install facet-mcp # 或直接安装 Python 包 `, until v0.3.0's read-back ran a **verb** instead of `--help`。然后，它说 wheel“仅适用于 `q` 和 `claims`”——**`claims` 也无法工作**，E24 通过运行它发现了这一点。这两个更正都包含在 [known-defects.md](docs/known-defects.md) 中，并附带了它们的测量结果。*

## 当前状态

**四个已接受的资产，跨越四个主题类别，无需任何积分。**每个资产都由导演在其自己的缩放级别上进行评估——在 GLB 上或在全尺寸工作表中——而不是通过指标来确定是否达到阈值。

| 主题 | 类别 | 已接受 | 参考/笔刷/膨胀 |
|---|---|---|---|
| **Character (W3)** | 人形生物 | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | 车辆，细长的骨架 | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | 野兽，翅膀膜 | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | 道具，近乎二维，灰度 | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

共享的是有效的纹素，并且**它们不能跨主题进行比较**——一艘船在视线高度隐藏了大部分自身，而动物则隐藏了一半。将每个资产与其自身的预先注册的范围上限进行比较，结果显示它们达到了 **86–93%**：行之间的差异在于几何形状，而不是回归。 [完整数字及其分母](docs/handbook/subjects.md)。

**这是一个流水线，而不是一个单字符生成器。**如果与八个命名的元素相矛盾，提示将赢得 **8 次中的 8 次**——中位 ΔE 为 46.3，而五个保留的控制组为 6.2——同时人物保持不变。结构由网格和控制来维持；命名的属性则取决于提示。

**投影仪问题已于2026年8月16日结束**（[E45](docs/experiments/E45-warp-and-aov-kickoff.md)–[E49](docs/experiments/E49-finish-and-cap-kickoff.md））。
这八个图块的**构成方式**是：从基于视角束调整后的数据中重建，并根据边缘×朝向×可见性权重进行渲染。在本次流程中，图块集首次通过了导演的验收标准——两次，跨越两个弧线——旁边是一个已发布的图块集，其流程曾导致图块出现问题。完成此操作的链条位于`tools/`（`emit_view_aovs`、`s3_composite`、`flow_estimate`、`s3_run`、`s3_sheet`、`atlas_from_aovs`、`twin_mesh_warp`），主要通过外部审查渠道进行构建，该渠道指定的校准声明已保持“十七比十七”，即每一个都经过验证，方法是在信任构建之前先运行它。

**规范是数据，它决定了支出（2026年8月17日）。** 身份规范包含十七个元素；生成双子的工作流程包含了十六个元素；默认配置文件中包含六个元素。没有任何内容将它们联系起来，因此四个弧线修复了下游的合成问题，这些问题源于源数据中的错误。现在，规范是一个数据库，其键是“表面”——一个元素列表无法显示缺少的内容，并且一个可为空的占位符会使孔成为一行——并且`canon_gate`在`restylize_views`和`texpass_brush`中运行，然后在输出目录存在之前进行。如果某个生成过程的提示信息没有涵盖经过批准的规范，则该过程将被拒绝，并且不会写入任何内容。

```
canon_gate 1.0.0  census  (occupancy is not ratification)
subject      named   occupancy   ratified   prof_hit surfaces
W3              19       24/24      24/24       5/19 canon/w3.surfaces.json
GALLEON         13           -          -      11/13 NONE
DRAGON          11           -          -      10/11 NONE
LONGSWORD        5         5/5        5/5        4/5 canon/longsword.surfaces.json
E10-LAYER        1           -          -          - NONE
LOGO             0           -          -          - NONE
```

`prof_hit 5/19`是一个**故意留下的、未修复的样本**：它是实际构建过程中将使用的实时默认设置，因此第一个`--profile character.json`应该停止。修复字符串会删除证据。

**边界已明确规定，而不是让其自行发现。** 它检查主题提示是否包含经过批准的规范短语。它**不**检查释义、基于视角的词干、未经批准的草稿、没有表面文件的对象，或者指定的材质是否着陆在正确的表面上。有四个对象具有IDENTITY.md文件，但没有表面JSON文件——这是故意留下的，而不是生成时未执行参考操作。

## 流程

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

**虚线跳跃是新的，并且故意不是实线的。** 流程中的第一个方框一直显示“粘土概念”，到目前为止，这里没有任何东西可以生成它——每个粘土都是手工制作的，并在输入时进行哈希处理。现在存在一个概念→粘土工具，并且它的第一对已以完整尺寸呈现：姿势、腕带、腰带吊坠和撕裂的下摆都已呈现；鬃毛则没有呈现；色彩泄漏在整个帧中测量为**C\* p99.9 = 13.15**，背景为无缝的非彩色。**这对无法显示的是网格是否会得到改进**，这是唯一能够使其获得认可的问题，因此它仍然是一个候选对象，并且其证据已记录：**[概念准备](docs/concept-prep.md)**。

## 是什么让它起作用

六个发现，每个发现都需要一次实验，并且每个发现都超出了产生它的对象的范围。[完整版本，包含测量结果](docs/findings.md)。

- **首先是形状，然后才是风格。** 重建器将表面噪声解释为几何体。一个干净的、类似雕塑的粘土，其平面经过故意夸张处理，可以生成比程式化的精灵具有更好拓扑结构的模型；程式化的双子模型会同时生成，并成为色彩参考。
- **构图脸部，获得脸部。** 头部裁剪会将**3.1–4.5倍**更多的多边形放置在头部上，并且这种差异是结构性的——分离的眼睑、眉毛皱纹、建模的鼻腔——而不是更清晰的模糊效果。
- **双子模型属于网格，而不是角色。** 在不同的网格中重复使用双子模型会导致覆盖率下降**62% → 22.7%**，因为手臂会投射到模型旁边的空旷空间中。每次都从您即将进行纹理处理的网格中生成双子模型。
- **身份属于提示信息。** 如果规范元素未在提示信息中命名，则该元素将意外出现，并且也会以相同的方式消失——当金色膝盖护甲最终仅通过损坏的ControlNet中的噪声出现在图像中时进行测量。
- **询问几何体，而不是阈值。** 将键控蒙版替换为精确的光线投射轮廓，可以将参考覆盖率从**28.4%提高到39.1%**——严格来说是累加的，没有扩散，也没有GPU。这里已经有三次角点中值键控失败，并且已停止使用。
- **剔除任何相机都无法看到的物体，从图块集中剔除，而不是从网格中剔除。** 49%的图块纹理从外部是不可见的；排除这些面可以减少68%的插值。与其删除，不如排除，这样可以将失败的可能性变为不可能，而不仅仅是可以检测到的。

## 尚未解决的问题

已命名并测量，位于首页而不是脚注中。[所有问题，位于代码中](docs/known-defects.md)。

- **一些可见的表面贴图映射到图集空间，但渲染引擎不会写入任何烘焙信息**，因此呈现出图像中未修改的默认黑色。Blender 的烘焙工具使用纹素中心采样，因此没有与任何纹素中心重叠的三角形区域将被留空——它的开发者
[已经命名了这种机制并合并了一个修复](https://projects.blender.org/blender/blender/pulls/161752)，时间是构建所有这些数值之后的两周。这是一种与特定对象无关的属性，而是与流程有关：在一个资源上进行测量，**而在其他四个资源上未进行测量**。
- **刀片带占据了所有八个摄像机中第一阶段参考图像的 0.00%**——在灰色背景上的钢制物体正好位于关键阈值之上。联合处理可以修复 55.72%。
- **笔触接缝没有对齐。**一种来源边界与普通纹理变化相比，差异为 **5.5 倍**；导演命名的区域的差异为 **9.5 倍**。
- **膨胀会导致不相关的图集岛屿之间出现混叠**——74.9% 的膨胀纹素从另一个岛屿获取颜色，与平均距离 1.0 高度的图形上的 0.177 相差甚远。⚠ **这个比例是在图集纹素中计算的，而不是关于摄像机所见的内容**：膨胀占渲染图集中 26.95%，占**渲染图像像素的 4.95%**，比例为 0.18 倍。贴图存在于大型图表中，孔洞存在于小型图表中，因此在屏幕空间中，膨胀纹素的成本较低。
- **⚑ 用于决定是否接受的标准缺陷是由 PAINT 携带的，而不是由任何填充物携带**——区域呈现出另一种材质的颜色，而没有任何斑点统计数据可以检测到这一点。通过三个会话、在三个不同的空间中进行了三次测量：**91.05% `reference` 携带了 0.99 倍的增强效果**，与基准率完全一致；相同类别的绿色布料为 **68.46% `reference`**；而在薄刀片上，表面自身的绘制纹素为 **18.77%**，而与其膨胀填充的 **5.55%** 相比。
填充物正确地从其最近的绘制邻居处获取信息——而该邻居本身已经存在问题。混合本身是一种未记录的双频带分割 (`M + gaussian_blur_σ16(B − M)`)，它在相同的点上测量了**四个替代方案中最差的结果**。
- **各个视图并非相互独立，这限制了所有混合修复。**对于每个缺陷斑块，**100% 的面片具有两个或多个贡献摄像机，并且所有这些摄像机都位于 90° 范围内**（平均值为 45°），21% 的缺陷面片仅由一个摄像机观察到。在近乎相同的控制下，相邻视图会同时失败，因此摄影测量学中发布的基于多视角的优势在这里不能直接应用。
- **此流程中的每次重建都是一个空心双层外壳**，壁厚约为两个体素。没有体积谓词可以应用于其中任何一个。
- **各个板在未命名的材质边界处存在差异，而规范是关键**（2026-08-16）。内部与网格对齐的扭曲测量结果显示，所有八个视图中，平均值为 **3.5–11.1 像素**，而轮廓线的平均值为 1.2–3.0；导演圈出的每个残余区域——袖口、手部、鞋面顶部——都是材质连接点，该生成提示从未提及过。⚠ **已于 2026-08-17 更正，并且更正结果更加明确。**
之前的表述是“记录的提示包含六个元素”——经过测量，它将两个不同的文件组合在一起。生成双胞胎的工作流程命名了 **17 个中的 16 个**，仅缺少一个抓握点；*笔刷配置文件默认值* 命名了六个。两者都是正确的，并且该句子在其中做出了一个错误的声明。重要的是，抓握点、护手和护胫以及手部在 16 短语的提示中出现了 **零次**——因为**规范中根本不存在这些元素**。即使是完整的提示也无法命名从未指定的“手”。✅ **已于 2026-08-17 关闭**——表面列表已被遍历、填充，并且**所有 24 个都得到了确认**，现在该网关会拒绝任何不包含它的提示。
- **5.65–5.57% 的有效纹素是没有任何平面环摄像机可以观察到的表面**——它们在每个视图中都未能通过深度门，没有投影路线可以绘制它们，并且已发布的流水线使用岛屿盲区填充来覆盖这些区域，从而产生了深色标记。它们需要一个策略（中性材质、笔刷或接受），而不是修复（[E49 报告](docs/experiments/E49-finish-and-cap-report.md)）。
- **在已接受等级的板上存在平坦的彩色多边形**——这是导演唯一公开承认的类别。⚠ **填充通道假设已被证伪（2026-08-17）。**孤立填充的测量值低于其自身的基准率，并且这些补丁位于 90–99% 的普通绘制纹素上，并且相同的缺陷存在于从被认为是导致该问题的图集中构建的渲染图像中。相反，它与来源有关：渲染视图的双胞胎在该处是干净的，并且**不同的**视图拥有 115 个缺陷像素中的 97 个，其朝向为 0.68，而另一个则为 0.60。角度补丁是一种**散射伪像**，颜色是一种真实的跨视图差异，该差异存在于已经命名的表面上——因此，“缺陷存在于双胞胎中”这一说法并不能证明需要进行双胞胎再生。一个更喜欢目标视图的合成器是范围内的修复方法，并且成本为零。*已过时的文本，但根据更正规则保留：“孤立岛屿的大小与单个三角形相当，从边界相邻的双胞胎样本中以未经侵蚀的轮廓线进行平铺填充。”*

## 如何运行此仓库

这种方法本身就是一种产品，并且它存在于流程中，原因如下：之前的流程进行了十次会话，每次会话都会判断自己的输出并撰写结论，而这些结论将在下一次会话中被视为既定事实。该循环中的任何内容都无法进行验证。

- **先制定规范，再进行报告，最后得出结论**——并且设计实验的环节绝不会对自己的结果进行评估。有 51 个实验记录在 [此处](docs/experiments/)。
- **修正会就地生效，与推翻它们的测量结果并列显示**，而不是以静默删除的方式呈现。仅在最初的环节中，就有六个既定结论被证明是错误的，并且这六个结论仍然可以与替代它们的内容一起查看。
- **失败的结果将保留在代码库中，并附带原因说明。**[`tools/superseded/`](docs/tools.md) 并非一个存档——任何人都可以运行这些工具，并观察它们以相同的方式失败。
- **负面结果也是一种完全的成功**，它会被报告和记录下来，而不是被调整到某个数值。
- **测试与修改代码相关的提交一起进行**——在两个人的操作下，有 1266 个测试通过，并且对 1212 个密封性测试进行了路径限制的 CI 测试。
- **可以查询记录。**对整个过程进行 SQLite + FTS5 索引验证，共四个环节。它发现结论与文本中描述的不同，在三个站点上，通过统计记录本身来得出结论。

## 所有内容都位于

| | |
|---|---|
| **[手册](docs/handbook/index.md)** | 指南——分阶段的流程、主题和配置系统 |
| **[概念准备](docs/concept-prep.md)** | 候选粘土生成：其 Gate 0 流程、放置方式以及它所开启的许可项目 |
| **[记录](docs/experiments/)** | 51 个实验：规范、报告、结论，以及在测量之前声明的所有预测 |
| **[流程中学到的内容](docs/findings.md)** | 持久的发现和来之不易的规则，完整呈现 |
| **[每个工具的状态](docs/tools.md)** | 哪些有效、哪些已被取代，以及每种情况下的证据 |
| **[已知缺陷](docs/known-defects.md)** | 所有未解决的问题，已在代码中进行测量和定位 |
| **[事件的经过](docs/arc-history.md)** | 按时间顺序排列的历史记录，保留了修正内容 |
| **[CLAUDE.md](CLAUDE.md)** | 如何在此工作——角色、规则以及每个角色的成本 |

## 许可状态

每个阶段都在本地运行，并且符合商业要求：SDXL (OpenRAIL++)、MV-Adapter (开源)、open3d (Apache-2.0)、spandrel (MIT)、RealESRGAN anime6B (BSD-3)、Blender、numpy、scipy、trimesh。

有意排除，并说明原因：**nvdiffrast**（非商业用途——在此通过结构性触发器强制执行，而不是通过证明），**Hunyuan3D-Paint**（在欧盟、英国和韩国的许可无效）、**MVPaint** 和 **TEXGen**（完全没有许可），以及 **UltraSharp / SUPIR / StableSR**（非商业放大器）。

**声明了范围，而不是让其自行发现。**它描述了 **记录的流程**——图表中显示的各个阶段，从图像到 3D 开始。在其上游的候选粘土生成环节目前在封闭云 API 上运行，该 API 的条款本代码库尚未验证，因此此处没有任何许可声明涵盖由其粘土制成的资产。这是一个开放项目，有明确的路径可以解决：符合许可要求的本地模型是 **Qwen-Image-Edit (Apache-2.0)**，并且 **FLUX.1-Kontext [dev] 因与 nvdiffrast 相同的理由而被排除**——非商业权重。两者都与工作室的模型目录进行了对比，而不是回忆；其原因在 [概念准备](docs/concept-prep.md) 中。

## 信任和威胁模型

facet 完全在您自己的机器上运行——每个工具都是一个脚本，您可以针对您在命令行中输入的路径进行调用，因此有意义的问题不是 *此应用程序请求了哪些权限*，而是 *这些脚本对您的机器做了什么*。通过测量来回答，并且可以重新运行每次扫描；完整的策略在 [SECURITY.md](SECURITY.md) 中：

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

三个明显的漏洞被公开，而不是声称已被修复，因为一份仅列出保证的安全说明并不是一个威胁模型：**文件操作没有进行沙箱隔离**（工具会按照其参数指示写入任何位置）；**许多工具和文档中都嵌入了绝对本地路径**——在 26 个文件中总共出现 114 次，这并非秘密，而是对一台机器的布局的一种披露，也是大多数工具无法在其他地方未经修改运行的原因；并且，**未发布的 36 个研究脚本中的意外错误会以 Python 追溯的形式呈现出来**，没有任何 `--debug` 门控。有意的停止操作是 `ANDON:` 消息，其中包含触发它们的测量结果。这就是研究工具的契约，[SHIP_GATE.md](SHIP_GATE.md) 准确地记录了何时不再满足要求——对于两个命令方面而言，在 0.2.0 版本中：`facet-index` 和 `facet-mcp` 返回 `0`（正常）/ `1`（用户错误）/ `2`（运行时错误）。并且，自从 [E22](docs/experiments/E22-ruling.md) 之后，对于触发的门控或失败的 `verify` 环节，会返回 **`4` REFUSED**，这意味着工具正在运行并告知您不要继续操作，而不是出现运行时错误。所有这些都会以结构化的方式拒绝，并命名下一步骤，而不是显示追溯信息 ([E21](docs/experiments/E21-cli-contract-report.md))。

**并且，这两个命令中的门控不再可删除。** 在“安装”方面，每个 ANDON 都会触发 `raise`；一个简单的 `assert` 是一个语句，它会静默地移除 `python -O`，在 E22 将它们转换为当前形式之前，这个仓库中有 87 个门控可以通过环境变量来删除。在同一门控上，分别在四种解释器模式下进行测量。
**并且，自从 [E23](docs/experiments/E23-route-gates-report.md) 之后，生成四个已接受资产的路径上的门控也不再可删除**——它有 **12 个工具中的 57 个站点**，转换为对文件进行纯粹的移动操作，而这些文件之前从未被测试过，现在每个文件都会在 `-O` 和 `PYTHONOPTIMIZE=1` 以及正常解释器下拒绝。
**并且，自从 [E25](docs/experiments/E25-ruling.md) 之后，该类别已关闭。** 它有 **43 个文件中的 133 个站点**——这些是生成上述四个已接受资产证据的测量工具，它们以相同的方式进行转换，从而使总数达到 `raise`，为 **278**。
在 `tools/` 下方，仅剩 **一个**简单的 ANDON `assert`：
`superseded/texpass_thin_mask.py`，它**永远不会**被转换为当前形式，因为这些工具的目的是让任何人都可以运行它们并以相同的方式观察它们的失败情况。这个剩余部分会通过名称固定在测试套件中，因此未来的扫描无法在不故意编辑测试的情况下将其删除。

**支持状态：** 该仓库在一个平台上进行开放式开发，由一位主管和一对轮换的顾问/执行者组成。`main` 是唯一受支持的状态。没有发布渠道、没有回溯策略，也没有 SLA——取而代之的是记录：每个声明都与其生成代码相邻，并且 [docs/experiments](docs/experiments/) 包含每个声明的规范、报告和裁决。

## 要求

Blender 5.x，Python 3.11+，以及 `numpy`、`scipy`、`trimesh`、`open3d`、`Pillow`、`spandrel` 和 `torch`。仅需要本地 ComfyUI 安装才能使用修复画笔。该项目是在 RTX 5090 上开发的；VRAM 的可用空间比原始速度更重要。

CI 在 **ubuntu-latest / Python 3.12** 上运行套件的隔离子集，并进行固定安装（`.github/workflows/ci.yml`）；工件层需要记录在 `E:\AI\training` 下的树，这些内容不在 git 中，因此 CI 会按设计选择不包含它们。本地，`python -m pytest` 运行所有 **1266** 个测试，而 `python -m pytest -m "not artifacts"` 运行 CI 重现的 **1212** 个测试。

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
