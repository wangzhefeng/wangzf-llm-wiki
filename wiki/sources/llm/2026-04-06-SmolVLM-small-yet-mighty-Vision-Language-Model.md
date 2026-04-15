---
title: "SmolVLM - small yet mighty Vision Language Model"
created: 2026-04-15
updated: 2026-04-15
type: source
tags:
  - llm-theory
sources:
  - raw/web/llm-theory/2026-04-06-SmolVLM-small-yet-mighty-Vision-Language-Model.md
status: summarized
---
## 内容摘要
This blog post introduces SmolVLM, a 2B VLM, SOTA for its memory footprint. SmolVLM is small, fast, memory-efficient, and fully open-source. All model checkpoints, VLM datasets, training recipes and t

## 关键要点
- We replaced Llama 3.1 8B with SmolLM2 1.7B as the language backbone.
- We more aggressively compress the patched visual information by reducing the information 9x using the pixel shuffle strategy, compared to 4x with idefics3.
- We use patches of 384\*384, instead of 364x364, because 384 is divisible by 3, which is necessary for our pixel shuffle strategy to work.

## 来源信息
- 原始文件：2026-04-06-SmolVLM-small-yet-mighty-Vision-Language-Model.md
- 来源类型：web
