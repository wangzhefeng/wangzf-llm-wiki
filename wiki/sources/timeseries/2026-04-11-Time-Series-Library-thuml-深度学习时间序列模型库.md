---
created_at: 2026-04-11
topics:
  - 时间序列预测
  - 深度学习
status: summarized
source_path: raw/repos/repo-thuml-Time-Series-Library.md
---

# 来源卡：Time-Series-Library (THUML)

## 这份材料讲了什么

- 原文：`raw/repos/repo-thuml-Time-Series-Library.md`
- 对应仓库：https://github.com/thuml/Time-Series-Library
- 内容：THUML (清华大学机器学习实验室) 维护的深度学习时间序列模型库，集中实现了 iTransformer、TimeMixer、Sundial、Timer、OpenLTM 等前沿时间序列预测模型，提供统一的训练、评估框架和实验脚本。

## 价值是什么

1. **代码实现参考**：提供最新时间序列模型的 PyTorch 实现，可作为算法复现和工程实现的参考模板。
2. **实验基准统一**：在同一代码框架下比较不同模型的性能，避免实现差异带来的评估偏差。
3. **工程实践范例**：展示时间序列预测任务的标准化工程结构，包括数据加载、模型定义、训练循环、评估指标等模块。
4. **研究生态入口**：通过该库可快速了解 THUML 团队在时间序列领域的研究脉络和模型演进。

## 连到哪些概念

- [[时序基础模型]] - 该库实现了多种时序基础模型 (Timer, Sundial, OpenLTM)
- [[深度学习时间序列预测]] - 库中所有模型均属于深度学习时间序列预测范畴
- [[预测工具生态]] - 作为开源工具库的一部分，丰富时间序列预测的工具选择
- [[Transformer时序预测]] - 包含 iTransformer 等基于 Transformer 的时序预测模型实现

## 关键模块

- **models/**：模型实现目录，按论文组织代码
- **exp/**：实验脚本，支持长期预测、零样本预测等任务
- **scripts/**：运行脚本，方便复现论文结果
- **data_provider/**：数据集加载与预处理工具
- **layers/**：基础神经网络层实现
- **utils/**：工具函数库
- **tutorial/**：教程与示例

## 使用建议

- 研究新模型时，可参考对应论文的实现代码
- 进行方法对比时，可使用该库的统一框架确保公平比较
- 工程实践中，可借鉴其模块化设计和配置管理方式