---
created_at: 2026-04-05
topics:
- knowledge-base
- tools
related_concepts:
- 知识库建设方法
- 知识库工作台
status: linked
---
# Obsidian Web Clipper 配置与图片本地化

## 一句话说明

这是关于如何配置 Obsidian Web Clipper 浏览器扩展，以及在 Obsidian 中将网页剪藏后的远程图片批量下载到本地的操作指南。

## 为什么需要这一步

Karpathy 在 LLM Wiki 模式中强调：**网页随时可能挂掉或修改，图片外链也可能失效**。如果剪藏后的 Markdown 文件中图片仍然是远程 URL，当原网站消失时，你的 `raw/` 层就不再是"不可变原始资料"，知识库的完整性会被破坏。

把图片下载到本地后，即使原网站消失，知识库中的图片和内容仍然完整可用。这也与当前知识库 `raw/` 层"唯一摄取入口、只存原始原件"的定位一致。

## 第一部分：安装与基础配置 Obsidian Web Clipper

### 1. 安装浏览器扩展

- Chrome / Edge：在扩展商店搜索 **Obsidian Web Clipper**，安装
- Firefox：同样搜索安装
- 安装后在浏览器工具栏可见剪藏图标

### 2. 配置剪藏保存路径

打开浏览器扩展 → 点击 **齿轮图标（设置）**：

| 设置项 | 推荐值 | 说明 |
|--------|--------|------|
| **Default location** | `raw/web/` | 剪藏文件存放路径，与知识库目录约定对齐 |
| **File name format** | `{{date:YYYY-MM-DD}}-{{title}}` | 统一命名格式，便于后续自动化处理 |
| **Download images** | ✅ 开启 | 自动把网页图片下载到本地 |
| **Image download folder** | `raw/assets/attachments/` 或相对路径 | 图片存放位置，建议与知识库 `raw/assets/` 结构对齐 |
| **Template** | 自定义或留空 | 可在知识库仓库中维护一个统一模板文件 |

## 第二部分：在 Obsidian 中批量下载远程图片

即使 Web Clipper 设置了下载图片，有时剪藏后的文件中仍可能残留远程图片 URL。以下是检查和补漏的方法。

### 方法一：Obsidian 内置命令（推荐）

1. 打开一篇用 Web Clipper 剪藏的文章
2. 按 `Ctrl+P`（Mac 是 `Cmd+P`）打开命令面板
3. 搜索 **"Download all images in file"**（中文界面为 **"下载文件中的所有图片"**）
4. 执行后，文章中所有远程图片会被下载到 Obsidian 的附件目录

### 方法二：社区插件 Local Images Plus

适合批量处理整个 vault 中所有未本地化的图片。

安装方式：
1. **设置 → 第三方插件** → 关闭安全模式
2. 搜索 **Local Images Plus** → 安装 → 启用
3. 在插件设置中指定下载目录（建议对齐 `raw/assets/attachments/` 结构）

使用方式：
1. 打开文件或选择多个文件
2. 命令面板 → 执行 **"Download all remote images"** 或 **"下载所有远程图片"**
3. 插件会批量处理，并自动更新 Markdown 中的图片路径

### 方法三：设置快捷键

如果你经常做这个操作，建议绑定快捷键提升效率：
1. **设置 → 快捷键**
2. 搜索 **"Download"** 或 **"下载"**
3. 找到 **"Download all images in file"** → 设置快捷键（例如 `Ctrl+Shift+D`）

之后每打开一篇新剪藏的文章，按一下快捷键即可完成图片本地化。

## 第三部分：附件目录结构建议

在 Obsidian **设置 → 文件和链接** 中配置：

| 设置项 | 推荐值 | 说明 |
|--------|--------|------|
| **附件文件夹路径** | `raw/assets/attachments/` | 与当前知识库结构对齐 |
| **附件子文件夹** | "基于当前文件路径" 或按专题手动分子目录 | 建议按专题分子目录，如 `knowledge-base/`、`timeseries/`、`operations-research/` |
| **使用双括号链接** | ✅ 开启 | 保持 Obsidian 链接风格一致性 |

这样下载的图片会自动整理到知识库已有的附件结构中，而不是散落在 vault 根目录。

## 第四部分：与知识库工作流的衔接

完成图片本地化后，这份剪藏文件就是一个合格的 `raw/` 层来源：

1. 文件位于 `raw/web/YYYY-MM-DD-标题.md`
2. 图片已下载到 `raw/assets/attachments/` 下
3. Markdown 中的图片路径已指向本地文件
4. 后续可以交给 LLM 生成 `wiki/sources/` 来源卡

## 代表来源

- [[2026-04-05-LLM-Wiki-持久化知识库模式]]
- [[2026-04-05-Karpathy-第二大脑-LLM-Wiki新范式]]
- [[2026-04-04-知识库构建执行指引]]
