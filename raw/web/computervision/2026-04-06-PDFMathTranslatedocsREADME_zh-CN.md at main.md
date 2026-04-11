---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: '[EMNLP 2025 Demo] PDF scientific paper translation with preserved formats
  - 基于 AI 完整保留排版的 PDF 文档全文双语翻译，支持 Google/DeepL/Ollama/OpenAI 等服务，提供 CLI/GUI/MCP/Docker/Zotero
  - PDFMathTranslate/docs/README_zh-CN.md at main · PDFMathTranslate/PDFMathTranslate'
source_type: web
status: inbox
tags:
- null
- clippings
title: PDFMathTranslate/docs/README_zh-CN.md at main
topics:
- 计算机视觉
source_url: https://github.com/PDFMathTranslate/PDFMathTranslate/blob/main/docs/README_zh-CN.md
published_at: null
related_concepts: []
---

科学 PDF 文档翻译及双语对照工具

- 📊 保留公式、图表、目录和注释 *([预览效果](#preview))*
- 🌐 支持 [多种语言](https://github.com/PDFMathTranslate/PDFMathTranslate/blob/main/docs/ADVANCED.md#language) 和 [诸多翻译服务](https://github.com/PDFMathTranslate/PDFMathTranslate/blob/main/docs/ADVANCED.md#services)
- 🤖 提供 [命令行工具](#usage) ， [图形交互界面](#gui) ，以及 [容器化部署](#docker)

欢迎在 [GitHub Issues](https://github.com/Byaidu/PDFMathTranslate/issues) 或 [Telegram 用户群](https://t.me/+Z9_SgnxmsmA5NzBl)

有关如何贡献的详细信息，请查阅 [贡献指南](https://github.com/Byaidu/PDFMathTranslate/wiki/Contribution-Guide---%E8%B4%A1%E7%8C%AE%E6%8C%87%E5%8D%97)

## 更新

- \[2026年3月23日\] 实验性支持 v2.0 翻译内核，使用隔离环境运行（ `--mode precise` ）。（由 [@reycn](https://github.com/reycn) 提交）
- \[2026年3月22日\] 支持 MiniMax（由 [@octo-patch](https://github.com/octo-patch) 提交的PR）
- \[2026年3月22日\] 修复与 OpenAI 相关的问题（由 [@samqin123](https://github.com/samqin123) 提交的PR）
- \[2026年3月22日\] 修复与 HTTP 相关的问题（由 [@soukouki](https://github.com/soukouki) 提交的PR）
- \[2026年3月22日\] 在 mac 和 OONX 平台上加快模型加载速度，GUI 启动，版本打印和持续集成。（由 [@reycn](https://github.com/reycn) 提交）
- \[2025 年 2 月 22 日\] 更好的发布 CI 和精心打包的 windows-amd64 exe (由 [@awwaawwa](https://github.com/awwaawwa) 提供)
- \[2024 年 12 月 24 日\] 翻译器现在支持在 [Xinference](https://github.com/xorbitsai/inference) 上使用本地模型 *(由 [@imClumsyPanda](https://github.com/imClumsyPanda) 提供)*

## 预览

![[raw/assets/attachments/computervision/preview.gif]]

## 在线演示 🌟

## 在线服务 🌟

您可以通过以下演示尝试我们的应用程序：

- [公共免费服务](https://pdf2zh.com/) 在线使用，无需安装 *(推荐)* 。
- [沉浸式翻译 - BabelDOC](https://app.immersivetranslate.com/babel-doc/) 每月免费 1000 页 *(推荐)*
- [在 HuggingFace 上托管的演示](https://huggingface.co/spaces/reycn/PDFMathTranslate-Docker)
- [在 ModelScope 上托管的演示](https://www.modelscope.cn/studios/AI-ModelScope/PDFMathTranslate) 无需安装。

请注意演示的计算资源有限，请避免滥用它们。

## 安装和使用

### 方法

针对不同的使用案例，我们提供不同的方法来使用我们的程序：

1\. UV 安装
1. 安装 Python (3.11 <= 版本 <= 3.12)
2. 安装我们的包：
	```
	pip install uv
	uv tool install --python 3.12 pdf2zh
	```
3. 执行翻译，文件生成在 [当前工作目录](https://chatgpt.com/share/6745ed36-9acc-800e-8a90-59204bd13444) ：
	```
	pdf2zh document.pdf
	```
2\. Windows exe
1. 从 [发布页面](https://github.com/Byaidu/PDFMathTranslate/releases) 下载 pdf2zh-version-win64.zip
2. 解压缩并双击 `pdf2zh.exe` 运行。
3\. 图形用户界面 1. 安装 Python (3.11 <= 版本 <= 3.12) 2. 安装我们的包：
```
pip install pdf2zh
```
1. 在浏览器中开始使用：
	```
	pdf2zh -i
	```
2. 如果您的浏览器没有自动启动，请访问
	```
	http://localhost:7860/
	```
	![[raw/assets/attachments/computervision/gui.gif]]

有关更多详细信息，请参阅 [GUI 文档](https://github.com/PDFMathTranslate/PDFMathTranslate/blob/main/docs/README_GUI.md) 。

4\. Docker
1. 拉取并运行：
	```
	docker pull byaidu/pdf2zh
	docker run -d -p 7860:7860 byaidu/pdf2zh
	```
2. 在浏览器中打开：
	```
	http://localhost:7860/
	```

对于云服务上的 docker 部署：

5\. Zotero 插件

有关更多细节，请参见 [Zotero PDF2zh](https://github.com/guaguastandup/zotero-pdf2zh) 。

6\. 命令行
1. 已安装 Python（3.11 <= 版本 <= 3.12）
2. 安装我们的包：
	```
	pip install pdf2zh
	```
3. 执行翻译，文件生成在 [当前工作目录](https://chatgpt.com/share/6745ed36-9acc-800e-8a90-59204bd13444):
	```
	pdf2zh document.pdf
	```

> [!tip] Tip
> - 如果你使用 Windows 并在下载后无法打开文件，请安装 [vc\_redist.x64.exe](https://aka.ms/vs/17/release/vc_redist.x64.exe) 并重试。
> - 如果你无法访问 Docker Hub，请尝试在 [GitHub 容器注册中心](https://github.com/Byaidu/PDFMathTranslate/pkgs/container/pdfmathtranslate) 上使用该镜像。
> ```
> docker pull ghcr.io/byaidu/pdfmathtranslate
> docker run -d -p 7860:7860 ghcr.io/byaidu/pdfmathtranslate
> ```

### 无法安装？

当前程序在工作前需要一个 AI 模型 (`wybxc/DocLayout-YOLO-DocStructBench-onnx`)，一些用户由于网络问题无法下载。如果你在下载此模型时遇到问题，我们提供以下环境变量的解决方法：

```
set HF_ENDPOINT=https://hf-mirror.com
```

对于 PowerShell 用户：

```
$env:HF_ENDPOINT = https://hf-mirror.com
```

如果此解决方案对您无效或您遇到其他问题，请参阅 [常见问题解答](https://github.com/Byaidu/PDFMathTranslate/wiki#-faq--%E5%B8%B8%E8%A7%81%E9%97%AE%E9%A2%98) 。

## 高级选项

在命令行中执行翻译命令，在当前工作目录下生成译文文档 `example-mono.pdf` 和双语对照文档 `example-dual.pdf` ，默认使用 Google 翻译服务，更多支持的服务在 [这里](https://github.com/Byaidu/PDFMathTranslate/blob/main/docs/ADVANCED.md#services))。

[![[cmd.explained.png|cmd]]](https://github.com/PDFMathTranslate/PDFMathTranslate/blob/main/docs/images/cmd.explained.png)

在下表中，我们列出了所有高级选项供参考：

| 选项 | 功能 | 示例 |
| --- | --- | --- |
| files | 本地文件 | `pdf2zh ~/local.pdf` |
| links | 在线文件 | `pdf2zh http://arxiv.org/paper.pdf` |
| `-i` | [进入 GUI](#gui) | `pdf2zh -i` |
| `-p` | [部分文档翻译](https://github.com/Byaidu/PDFMathTranslate/blob/main/docs/ADVANCED.md#partial) | `pdf2zh example.pdf -p 1` |
| `-li` | [源语言](https://github.com/Byaidu/PDFMathTranslate/blob/main/docs/ADVANCED.md#languages) | `pdf2zh example.pdf -li en` |
| `-lo` | [目标语言](https://github.com/Byaidu/PDFMathTranslate/blob/main/docs/ADVANCED.md#languages) | `pdf2zh example.pdf -lo zh` |
| `-s` | [翻译服务](https://github.com/Byaidu/PDFMathTranslate/blob/main/docs/ADVANCED.md#services) | `pdf2zh example.pdf -s deepl` |
| `-t` | [多线程](https://github.com/Byaidu/PDFMathTranslate/blob/main/docs/ADVANCED.md#threads) | `pdf2zh example.pdf -t 1` |
| `-o` | 输出目录 | `pdf2zh example.pdf -o output` |
| `-f`, `-c` | [异常](https://github.com/Byaidu/PDFMathTranslate/blob/main/docs/ADVANCED.md#exceptions) | `pdf2zh example.pdf -f "(MS.*)"` |
| `-cp` | 兼容模式 | `pdf2zh example.pdf --compatible` |
| `--share` | 公开链接 | `pdf2zh -i --share` |
| `--authorized` | [授权](https://github.com/Byaidu/PDFMathTranslate/blob/main/docs/ADVANCED.md#auth) | `pdf2zh -i --authorized users.txt [auth.html]` |
| `--prompt` | [自定义提示](https://github.com/Byaidu/PDFMathTranslate/blob/main/docs/ADVANCED.md#prompt) | `pdf2zh --prompt [prompt.txt]` |
| `--onnx` | \[使用自定义 DocLayout-YOLO ONNX 模型\] | `pdf2zh --onnx [onnx/model/path]` |
| `--serverport` | \[使用自定义 WebUI 端口\] | `pdf2zh --serverport 7860` |
| `--dir` | \[批量翻译\] | `pdf2zh --dir /path/to/translate/` |
| `--config` | [配置文件](https://github.com/Byaidu/PDFMathTranslate/blob/main/docs/ADVANCED.md#cofig) | `pdf2zh --config /path/to/config/config.json` |
| `--serverport` | \[自定义 gradio 服务器端口\] | `pdf2zh --serverport 7860` |
| `--mode` | 翻译模式： `fast` （默认，v1）或 `precise` （v2，实验性，需要 pdf2zh\_next 子模块） | `pdf2zh --mode precise example.pdf` |
| `--babeldoc` | 使用实验性后端 [BabelDOC](https://funstory-ai.github.io/BabelDOC/) 翻译 | `pdf2zh --babeldoc` -s openai example.pdf |

有关详细说明，请参阅我们的文档 [高级用法](https://github.com/PDFMathTranslate/PDFMathTranslate/blob/main/docs/ADVANCED.md) ，以获取每个选项的完整列表。

## 二次开发 (API)

当前的 pdf2zh API 暂时已弃用。API 将在 [pdf2zh 2.0](https://github.com/Byaidu/PDFMathTranslate/issues/586) 发布后重新提供。对于需要程序化访问的用户，请使用 [BabelDOC](https://github.com/funstory-ai/BabelDOC) 的 `babeldoc.high_level.async_translate` 函数。

API 暂时弃用意味着：相关代码暂时不会被移除，但不会提供技术支持，也不会修复 bug。

## 待办事项

- 使用基于 DocLayNet 的模型解析布局， [PaddleX](https://github.com/PaddlePaddle/PaddleX/blob/17cc27ac3842e7880ca4aad92358d3ef8555429a/paddlex/repo_apis/PaddleDetection_api/object_det/official_categories.py#L81) ， [PaperMage](https://github.com/allenai/papermage/blob/9cd4bb48cbedab45d0f7a455711438f1632abebe/README.md?plain=1#L102) ， [SAM2](https://github.com/facebookresearch/sam2)
- 修复页面旋转、目录、列表格式
- 修复旧论文中的像素公式
- 异步重试，除了 KeyboardInterrupt
- 针对西方语言的 Knuth–Plass 算法
- 支持非 PDF/A 文件
- [Zotero](https://github.com/zotero/zotero) 和 [Obsidian](https://github.com/obsidianmd/obsidian-releases) 的插件

## 致谢

- [Immersive Translation](https://immersivetranslate.com/) 为此项目的活跃贡献者提供每月的专业会员兑换码，详细信息请查看： [CONTRIBUTOR\_REWARD.md](https://github.com/funstory-ai/BabelDOC/blob/main/docs/CONTRIBUTOR_REWARD.md)
- 文档合并： [PyMuPDF](https://github.com/pymupdf/PyMuPDF)
- 文档解析： [Pdfminer.six](https://github.com/pdfminer/pdfminer.six)
- 文档提取： [MinerU](https://github.com/opendatalab/MinerU)
- 文档预览： [Gradio PDF](https://github.com/freddyaboulton/gradio-pdf)
- 多线程翻译： [MathTranslate](https://github.com/SUSYUSTC/MathTranslate)
- 布局解析： [DocLayout-YOLO](https://github.com/opendatalab/DocLayout-YOLO)
- 文档标准： [PDF Explained](https://zxyle.github.io/PDF-Explained/) ， [PDF Cheat Sheets](https://pdfa.org/resource/pdf-cheat-sheets/)
- 多语言字体： [Go Noto Universal](https://github.com/satbyy/go-noto-universal)
[![[raw/assets/attachments/computervision/Image 50.svg]]](https://github.com/Byaidu/PDFMathTranslate/graphs/contributors)

[![[Image 51.svg|Alt]]](https://camo.githubusercontent.com/cd596cb53913066324ad0661794e767242a44dbebea34a582f6fa29abe39d8de/68747470733a2f2f7265706f62656174732e6178696f6d2e636f2f6170692f656d6265642f646661373538336461353333326131313436386436383666626432396239323332306136613836392e737667)

[![[Image 52.svg|星标历史图表]]](https://star-history.com/#Byaidu/PDFMathTranslate&Date)