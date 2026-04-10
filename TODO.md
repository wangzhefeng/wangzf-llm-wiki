<details><summary>目录</summary><p>

- [assets](#assets)
- [outputs](#outputs)
    - [answers](#answers)
    - [figures](#figures)
    - [logs](#logs)
    - [logs](#logs-1)
    - [slides](#slides)
    - [syntheses](#syntheses)
    - [READMD.md](#readmdmd)
- [prompts](#prompts)
- [raw](#raw)
    - [images](#images)
- [tools](#tools)
- [wiki](#wiki)
    - [主题](#主题)
- [others](#others)
- [通用问题](#通用问题)
</p></details>

# assets

* [x] 对 assets/attachments 中的图片文件依据其引用的文件所属主题进行分类，为新的分类创建文件夹。
* [ ] 对 assets/attachments 中的图片文件进行命名规范。

# outputs

* [ ] 在该目录下的子目录中创建对应主题或任务（比如"知识库健康检查"）的目录，便于将生成的文件归类。

## answers

* [x] 知识库健康检查输出："知识库健康检查" 相关内容与 "outputs/logs" 中的 "知识库健康检查日志" 混乱和重复；

## figures



## logs

* [x] 知识库健康检查输出： "知识库健康检查" 相关内容与 "outputs/logs" 中的 "知识库健康检查日志" 混乱和重复；
* [x] 知识库健康检查输出：知识库健康检查报告内容，保持最后一次检查结果即可，报告中的待办事项，可在下一次检查时补充。

## logs

## slides

## syntheses

## READMD.md

# prompts

* [x] 在该目录下创建对应主题或任务（比如"知识库健康检查"）的目录，便于将生成的文件归类。
* [x] 知识库健康检查输入："knowledge-base-health-check" 内容与其他的“知识库健康检查” 功能重复，使用入口比较混乱；
* [x] 知识库健康检查输入："wiki-lint" 功能与 "knowledge-base-health-check" 重复，使用入口比较混乱。
* [ ] 更新 README.md 中关于目前 Prompt 的说明，以及下一步的建议。
* [ ] 考虑后续如何自动化，只作为工具或 skill

# raw

* [ ] codex_threads 中的线程总结模板：进行知识库构建的经验总结，skill制作
* [ ] datasets
    - [ ] 测试数据文档的解析和使用方法
* [ ] images
    - [ ] 处理图片文件的能力探索
* [ ] local-notes
    - [ ] post 中内容的主题提取
* [ ] papers
    - [ ] 处理 PDF 文档的能力探索
* [ ] repo
    - [ ] 完善相关主题的仓库，优化仓库解析
* [ ] web
    - [ ] 做清洗，人工监督

## images

* [ ] 图面重新加工
* [ ] 研究图片如何提取信息

# tools

* [ ] LLM 自动忽略，一个 Python 虚拟环境，及一些有用的任务处理脚本

# wiki

## 主题

* [x] 知识库构建
    - [x] 内容职责不清晰
* [x] 知识库维护
    - [x] 暂无
* [x] 知识库使用
    - [x] 暂无
* [ ] 时间序列分析
    - [x] 将电力市场交易抽取出来构建单独主题
* [ ] 运筹优化算法
* [ ] 机器学习
* [ ] 深度学习
* [ ] 强化学习
* [ ] 大语言模型
    - [x] 缺少来源清单
* [ ] 控制算法
    - [x] 缺少来源清单
* [ ] 计算机视觉
    - [ ] 没有构建完成
* [ ] 其他主体
    - [ ] 需要诊断
    - [x] vibe coding

# others

* [ ] AGENTS.md
    - [ ] 解释具体的工作原理
    - [ ] 优化的空间
* [ ] CLAUDE.md
    - [ ] 解释具体的工作原理
    - [ ] 优化的空间
* [ ] README.md
    - [ ] 解释具体的工作原理
    - [ ] 优化的空间

# 通用问题

* [x] 知识库健康检查任务比较混乱：
    - [x] 输入、触发
    - [x] 检查项更新
    - [x] 输出落地
