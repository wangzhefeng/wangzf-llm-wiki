---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: A Next-Generation Training Engine Built for Ultra-Large MoE Models -
  xtuner/README_zh-CN.md at main · InternLM/xtuner
published: null
source: https://github.com/InternLM/xtuner/blob/main/README_zh-CN.md
source_type: web
status: inbox
tags:
- null
- clippings
title: xtuner/README_zh-CN.md at main
topics:
- 强化学习
---

## 🚀 Speed Benchmark

[![](https://private-user-images.githubusercontent.com/67539920/486694623-fa42d587-068d-427b-b88c-25a164b3511c.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzU0Njg2MDUsIm5iZiI6MTc3NTQ2ODMwNSwicGF0aCI6Ii82NzUzOTkyMC80ODY2OTQ2MjMtZmE0MmQ1ODctMDY4ZC00MjdiLWI4OGMtMjVhMTY0YjM1MTFjLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA0MDYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNDA2VDA5MzgyNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWI2MTBmYTg2NzMyOTFhZmU5OWQyYzhlODdiYzI1MmM3MzRlYmMzOWU5MmYzMzRlOTJiYWNjYzQzOWI2MDRkNWEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.xO4V2ZllAZ6Ur9gdlDsquLs8ikfA-fyPbQMkY7wtvCU)](https://private-user-images.githubusercontent.com/67539920/486694623-fa42d587-068d-427b-b88c-25a164b3511c.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzU0Njg2MDUsIm5iZiI6MTc3NTQ2ODMwNSwicGF0aCI6Ii82NzUzOTkyMC80ODY2OTQ2MjMtZmE0MmQ1ODctMDY4ZC00MjdiLWI4OGMtMjVhMTY0YjM1MTFjLnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA0MDYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNDA2VDA5MzgyNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPWI2MTBmYTg2NzMyOTFhZmU5OWQyYzhlODdiYzI1MmM3MzRlYmMzOWU5MmYzMzRlOTJiYWNjYzQzOWI2MDRkNWEmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.xO4V2ZllAZ6Ur9gdlDsquLs8ikfA-fyPbQMkY7wtvCU)

## 🎉 更新

- **\[2025/09\]** XTuner V1 正式发布！专为超大规模 MoE 模型打造的新一代训练引擎

## 📖 介绍

XTuner V1 是一个专为超大规模 MoE 模型打造的新一代大模型训练引擎。与传统 3D 并行训练架构相比，XTuner V1 针对当前学术界主流的 MoE 训练场景进行了深度优化。

### 核心特性

**📊 Dropless 训练**

- **灵活扩展，无需复杂配置：** 200B 量级 MoE 无需专家并行；600B MoE 仅需节点内专家并行
- **优化的并行策略：** 相比传统 3D 并行方案，专家并行维度更小，实现更高效的 Dropless 训练

**📝 长序列支持**

- **内存高效设计：** 通过先进的显存优化技术组合，200B MoE 模型无需序列并行即可训练 64k 序列长度
- **灵活扩展能力：** 全面支持 DeepSpeed Ulysses 序列并行，最大序列长度可线性扩展
- **稳定可靠：** 长序列训练时对专家负载不均衡不敏感，保持稳定性能

**⚡ 卓越效率**

- **超大规模支持：** 支持高达 1T 参数量的 MoE 模型训练
- **突破性能瓶颈：** 首次在 200B 以上规模的 MoE 模型上，实现 FSDP 训练吞吐超越传统 3D 并行方案
- **硬件优化：** 在 Ascend A3 NPU 超节点上，训练效率超越 NVIDIA H800

[![](https://private-user-images.githubusercontent.com/67539920/486606372-98519a93-1ce8-49f0-a7ab-d7968c9d67a6.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzU0Njg2MDUsIm5iZiI6MTc3NTQ2ODMwNSwicGF0aCI6Ii82NzUzOTkyMC80ODY2MDYzNzItOTg1MTlhOTMtMWNlOC00OWYwLWE3YWItZDc5NjhjOWQ2N2E2LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA0MDYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNDA2VDA5MzgyNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTlhMjgxMTQyOWU1ZjFlMzU0NDY0YTM4MTZjOTNiNjliM2QzOTU2ZTU4N2U0NWRlZWQyZmIzMmM3YWYxNGRkMjkmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.RQGy9bTrZ8zCru3qCtceBWCCzYlcA94csCQNcexCQsM)](https://private-user-images.githubusercontent.com/67539920/486606372-98519a93-1ce8-49f0-a7ab-d7968c9d67a6.png?jwt=eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJpc3MiOiJnaXRodWIuY29tIiwiYXVkIjoicmF3LmdpdGh1YnVzZXJjb250ZW50LmNvbSIsImtleSI6ImtleTUiLCJleHAiOjE3NzU0Njg2MDUsIm5iZiI6MTc3NTQ2ODMwNSwicGF0aCI6Ii82NzUzOTkyMC80ODY2MDYzNzItOTg1MTlhOTMtMWNlOC00OWYwLWE3YWItZDc5NjhjOWQ2N2E2LnBuZz9YLUFtei1BbGdvcml0aG09QVdTNC1ITUFDLVNIQTI1NiZYLUFtei1DcmVkZW50aWFsPUFLSUFWQ09EWUxTQTUzUFFLNFpBJTJGMjAyNjA0MDYlMkZ1cy1lYXN0LTElMkZzMyUyRmF3czRfcmVxdWVzdCZYLUFtei1EYXRlPTIwMjYwNDA2VDA5MzgyNVomWC1BbXotRXhwaXJlcz0zMDAmWC1BbXotU2lnbmF0dXJlPTlhMjgxMTQyOWU1ZjFlMzU0NDY0YTM4MTZjOTNiNjliM2QzOTU2ZTU4N2U0NWRlZWQyZmIzMmM3YWYxNGRkMjkmWC1BbXotU2lnbmVkSGVhZGVycz1ob3N0In0.RQGy9bTrZ8zCru3qCtceBWCCzYlcA94csCQNcexCQsM)

## 🔥 Roadmap

XTuner V1 致力于持续提升超大规模 MoE 模型的预训练、指令微调和强化学习训练效率，并重点优化昇腾 NPU 支持。

### 🚀 训练引擎

我们的愿景是将 XTuner V1 打造成通用训练后端，无缝集成到更广泛的开源生态系统中。

| Model | GPU(FP8) | GPU(BF16) | NPU(BF16) |
| --- | --- | --- | --- |
| Intern S1 | ✅ | ✅ | ✅ |
| Intern VL | ✅ | ✅ | ✅ |
| Qwen3 Dense | ✅ | ✅ | ✅ |
| Qwen3 MoE | ✅ | ✅ | ✅ |
| GPT OSS | ✅ | ✅ | ❌ |
| Deepseek V3 | ✅ | ✅ | ❌ |
| KIMI K2 | ✅ | ✅ | ❌ |

### 🧠 算法套件

算法组件正在快速迭代中。欢迎社区贡献 - 使用 XTuner V1，将您的算法扩展到前所未有的规模！

**已实现**

- ✅ **多模态预训练** - 全面支持视觉语言模型训练
- ✅ **多模态监督微调** - 针对指令跟随优化
- ✅ [GRPO](https://arxiv.org/pdf/2402.03300) - Group Relative Policy Optimization

**即将推出**

- 🔄 [MPO](https://arxiv.org/pdf/2411.10442) - Mixed Preference Optimization
- 🔄 [DAPO](https://arxiv.org/pdf/2503.14476) - Dynamic Sampling Policy Optimization
- 🔄 **多轮智能体强化学习** - 高级智能体训练能力

### ⚡ 推理引擎集成

与主流推理框架无缝对接

- LMDeploy
- vLLM
- SGLang

### 数据

- 推荐使用 [GraphGen](https://github.com/open-sciencelab/GraphGen) 合成 SFT 所需训练数据，目前已在多个垂域验证效果。

## 🤝 贡献指南

我们感谢所有的贡献者为改进和提升 XTuner 所作出的努力。请参考 [贡献指南](https://github.com/InternLM/xtuner/blob/main/.github/CONTRIBUTING.md) 来了解参与项目贡献的相关指引。

## 🙏 致谢

XTuner V1 的开发深受开源社区优秀项目的启发和支持。我们向以下开创性项目致以诚挚的谢意：

**训练引擎：**

- [Torchtitan](https://github.com/pytorch/torchtitan) - PyTorch 原生分布式训练框架
- [Deepspeed](https://github.com/deepspeedai/DeepSpeed) - 微软深度学习优化库
- [MindSpeed](https://gitee.com/ascend/MindSpeed) - 昇腾高性能训练加速库
- [Megatron](https://github.com/NVIDIA/Megatron-LM) - NVIDIA 大规模 Transformer 训练框架

**强化学习：**

XTuner V1 的强化学习能力借鉴了以下项目的优秀实践和经验

- [veRL](https://github.com/volcengine/verl) - Volcano Engine Reinforcement Learning for LLMs
- [SLIME](https://github.com/THUDM/slime) - THU's scalable RLHF implementation
- [AReal](https://github.com/inclusionAI/AReaL) - Ant Reasoning Reinforcement Learning for LLMs
- [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF) - An Easy-to-use, Scalable and High-performance RLHF Framework based on Ray

我们衷心感谢这些项目的所有贡献者和维护者，是他们推动了大规模模型训练领域的不断进步。

## 🖊️ 引用

```
@misc{2023xtuner,
    title={XTuner: A Toolkit for Efficiently Fine-tuning LLM},
    author={XTuner Contributors},
    howpublished = {\url{https://github.com/InternLM/xtuner}},
    year={2023}
}
```

## 开源许可证

该项目采用 [Apache License 2.0 开源许可证](https://github.com/InternLM/xtuner/blob/main/LICENSE) 。同时，请遵守所使用的模型与数据集的许可证。