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

这种风格应用于**资源本身**，是在纹理空间中进行处理——而不是针对每个视角单独绘制，然后再将它们拼接在一起。只需向程序输入一个外形夸张的泥塑概念模型，它就会生成一个带有纹理的模型网格，该网格的颜色来自对原始模型的风格化参考，而参考模型无法看到的区域则会通过蒙版修复画笔和具有表面感知的膨胀功能进行填充。

这个名称既指出了问题的两个方面：多边形，以及它们所构成的表面。

## 目前的状况如何？

**四种被批准的资产，涵盖四个不同的类别，且学分均为零。** 主管对每一种资产都进行了评估——有时是在大型显示器上查看全球业务列表（GLB），有时是在全尺寸纸张上查看——而不是根据某个指标是否达到特定阈值来决定。

| 主题；学科；对象；使……屈从 | 类 | 接受；被接纳。 | 参考；刷子；扩张 |
|---|---|---|---|
| **Character (W3)** | 人形的；像人的。 | [2026-08-04](docs/experiments/E08-ruling-gate0.md) | 68.8 / 4.2 / 27.0 |
| **Galleon** | 车辆；细小的索具。 | [2026-08-05](docs/experiments/E04-ruling.md) | 36.89 / 6.87 / 56.24 |
| **Dragon** | 野兽，翼膜。 | [2026-08-07](docs/experiments/E12-ruling.md) | 44.15 / 3.07 / 52.78 |
| **Longsword** | 道具、近乎二维、灰色调。 | [2026-08-08](docs/experiments/E14-ruling.md) | 45.25 / 2.07 / 52.68 |

图像块是有效的，并且**不同主体之间的图像块不能进行比较**——一艘船大部分都隐藏在视线以下，而动物则只隐藏一半。将每个图像块与其预先设定的最大显示范围进行对比，它们会达到**86%–93%**的显示效果；行与行之间的差异在于几何形状，而不是回归分析。[完整的数值及其分母](docs/handbook/subjects.md)。

**这是一个流水线，而不是一个简单的生成器。** 它与八个指定元素的规范相悖，但生成的图像却获得了 **8/8** 的好评——中位 ΔE 值为 46.3，而五个对照组的平均值为 6.2——同时，图像中的人物保持不变。结构由网格和控制机制维持；指定的属性则受到提示词的影响。

## 路线

```
form-exaggerated clay concept ──► image-to-3D ──► weld ──► density allocation
                                                             │
                    cull what no camera can see ◄────────────┘
                                 │
                                 ▼
       twins, generated from THIS mesh ──► project ──► brush the holes ──► fill
```

分阶段进行，并对每个阶段进行说明：**[《手册》](docs/handbook/index.md)**。

## 是什么让它发挥作用？

有六项研究发现，每一项都需进行实验才能得出，并且其结论具有普遍适用性，超越了最初的研究对象。[详细报告，包括各项测量数据](docs/findings.md)。

- **先注重结构，再考虑风格。** 重建工具会将表面噪点解读为几何形状。一个干净、雕塑感十足的粘土模型，其平面经过有意的夸张处理后，最终呈现出比风格化的精灵图像更好的拓扑结构；而风格化的孪生模型则会同时生成，并作为色彩参考。
- **突出面部轮廓，塑造清晰的面容。** 将画面裁剪为半身像，可以使头部拥有多达 **3.1–4.5 倍** 的多边形数量，而且这种差异是结构性的——例如，分离的眼睑、眉毛纹路和建模过的鼻孔等，而不是仅仅提高模糊度。
- **孪生模型属于网格，而非角色。** 在不同的网格中重复使用孪生模型，可以使覆盖率从 **62% 降低到 22.7%**，因为手臂会投射到模型旁边的空白区域。每次都要根据即将进行纹理处理的网格生成孪生模型。
- **身份归属于提示词。** 如果提示词中没有提及某个正统元素，它就会意外地出现，并且也会以同样的方式消失——例如，当金色护膝最终仅通过损坏的 ControlNet 中的噪点出现在图像中时。
- **询问几何形状，而不是阈值。** 将关键遮罩替换为精确的光线投射轮廓，可以将参考覆盖率从 **28.4% 提高到 39.1%** 的有效像素——完全是累加式的，没有扩散，也不需要 GPU。角落中值抠图在这里已经失败了三次，现在已被弃用。
- **剔除任何相机都无法看到的区域，从贴图中剔除，而不是从网格中删除。** 49% 的贴图像素从外部不可见；排除这些面可以使插值减少 **68%**。与其删除，不如排除，这样不仅可以检测到错误，而且还可以使其完全不可能发生。

## 还有哪些问题没有得到解决？

这些问题都已明确列出并进行了说明，而且是在文档的首页上，而不是在脚注中。[所有问题都位于代码文件中](docs/known-defects.md)。

- 在所有八个摄像头中，**刀片带占据了第一阶段参考图像的 0.00%**——在灰色背景上的一块金属板正好位于关键点的阈值位置。这种组合方式使效果提升了 55.72%。
- **笔触边缘没有进行平滑处理。**一个来源边界呈现出**5.5倍**于普通纹理变化的程度；导演所指的区域则呈现出**9.5倍**的变化。
- **膨胀效应导致不相关的图块之间出现颜色溢出**——74.9%的膨胀像素从另一个图块获取颜色，平均距离为0.177（在高度为1.0的图像中）。
- **这条路径上的每一次重建都形成了一个空心的双层外壳**，壁厚约为两个体素。无法对单个外壳应用任何体积谓词。

## 这个代码仓库是如何运行的？

这种方法既是结果，也是过程的一部分，它之所以存在是有原因的：之前的流程包含十个环节，每个环节都对自己的成果进行评估，并在下一个环节中将这些评估结果作为既定事实进行阅读。在这个循环中，没有任何环节可以被验证。

- **先进行规划，后提交报告，最后做出结论**——而且设计实验的环节绝不会对自身的结果进行评估。目前有二十个实验记录在[此处](docs/experiments/)。
- **更正会直接显示在其所影响的测量结果旁边**，而不是以静默删除的方式呈现。仅在最初的环节中，就有六项既定结论被证明是错误的，而且这六项结论仍然可以与替代它们的内容并列显示。
- **失败的结果及其原因将保留在代码库中。**[`tools/superseded/`](docs/tools.md) 并非一个存档——任何人都可以运行这些工具，并观察它们以相同的方式失败。
- **负面结果也是一种完整的成功**，它会被报告和记录下来，而不是被调整到某个特定数值。
- **测试会与修改代码的提交版本相关联**——在两个人的操作下，有 202 个测试通过，并且对这 194 个独立的测试进行了路径限制的持续集成。
- **可以查询记录。**针对整个历史记录构建了一个 SQLite + FTS5 索引，并在四个方面进行了验证。它通过统计记录本身，发现了三个站点中，文本描述与实际结果不符的情况。

## 这里就是一切

| | |
|---|---|
| 《手册》（请参阅 docs/handbook/index.md） | 指南——分阶段介绍路线、主题和人物档案系统。 |
| **[记录](docs/experiments/)** | 二十个实验：规范、报告、裁决，以及在测量之前声明的每一个预测。 |
| **[路线所学习的内容](docs/findings.md)** | 持久性的发现和来之不易的规则，完整呈现。 |
| **[每个工具的状态](docs/tools.md)** | 哪些有效，哪些已过时，以及每种情况下的证据。 |
| **[已知缺陷](docs/known-defects.md)** | 所有未解决的问题，在代码中进行测量和定位。 |
| **[事件的经过](docs/arc-history.md)** | 按时间顺序排列的历史记录，包含完整的更正。 |
| **[CLAUDE.md](CLAUDE.md)** | 如何在此工作——角色、规则以及每个角色的成本。 |

## 许可条款

所有阶段都在本地运行，并且在商业上是安全的：SDXL (OpenRAIL++)、MV-Adapter (开源)、open3d (Apache-2.0)、spandrel (MIT)、RealESRGAN anime6B (BSD-3)、Blender、numpy、scipy、trimesh。

有意识地排除，并说明原因：**nvdiffrast**（非商业用途——通过结构性触发器强制执行，而不是通过认证），**Hunyuan3D-Paint**（在欧盟、英国和韩国的许可无效）、**MVPaint** 和 **TEXGen**（完全没有许可），以及 **UltraSharp / SUPIR / StableSR**（非商业用途的图像增强工具）。

## 信任与威胁模型

facet 完全在您自己的机器上运行——每个工具都是一个脚本，您可以针对您输入的路径来调用它，因此有意义的问题不是*此应用程序请求了哪些权限*，而是*这些脚本对您的机器做了什么*。通过测量来回答这个问题，并且每次扫描都可以重新运行；完整的策略位于 [SECURITY.md](SECURITY.md) 中：

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

公开了三个关键点，而不是声称已经解决了它们，因为仅列出保证的安全说明并不是一个威胁模型：**文件操作没有进行沙箱隔离**（工具会在其参数指示的位置进行写入）；**许多工具和文档中都嵌入了绝对本地路径**——在 26 个文件中共有 114 次出现，这并非秘密，而是对一台机器的布局的一种披露，也是大多数工具无法在其他地方未经修改运行的原因；并且 **意外故障会显示为 Python 堆栈跟踪**，没有 `--debug` 网关，也没有结构化的错误形式。有意的停止操作是 `ANDON:` 消息，其中包含触发它们的测量结果。这就是研究工具的约定，[SHIP_GATE.md](SHIP_GATE.md) 记录了何时不再满足要求。

**支持状态：**此仓库在一个环境中进行开发，由一位负责人和一个轮流出现的顾问和执行者团队负责。`main` 是唯一受支持的状态。没有发布渠道、回溯策略或 SLA——取而代之的是记录：每个声明都与其生成代码相邻，并且 [docs/experiments](docs/experiments/) 包含每个实验的规范、报告和裁决。

## 要求

Blender 5.x、Python 3.11+，以及 `numpy`、`scipy`、`trimesh`、`open3d`、`Pillow`、`spandrel` 和 `torch`。仅需要本地 ComfyUI 安装才能使用绘画笔刷。在 RTX 5090 上进行开发；VRAM 容量比原始速度更重要。

CI 在 **ubuntu-latest / Python 3.12** 上运行该套件的隔离子集，并固定安装（`.github/workflows/ci.yml`）；工件层需要记录的树，位于 `E:\AI\training` 中，这些内容不在 git 中，因此 CI 会按设计选择排除它们。在本地，`python -m pytest` 会运行所有 **202 个** 测试，并且 `python -m pytest -m "not artifacts"` 会运行 **194 个** CI 重现的测试。

---

<p align="center">
  Built by <a href="https://mcp-tool-shop.github.io/">MCP Tool Shop</a>
</p>
