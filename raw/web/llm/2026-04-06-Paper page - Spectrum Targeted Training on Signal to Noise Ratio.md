---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: Join the discussion on this paper page
source_type: web
status: inbox
tags:
- null
- clippings
title: 'Paper page - Spectrum: Targeted Training on Signal to Noise Ratio'
topics:
- 大语言模型
source_url: https://huggingface.co/papers/2406.06623
published_at: 2024-06-12
related_concepts: []
---

arxiv:2406.06623

## Spectrum: Targeted Training on Signal to Noise Ratio

Authors:

## Abstract

Spectrum accelerates LLM training by selectively targeting and freezing layer modules based on signal-to-noise ratio, reducing GPU memory usage while maintaining performance.

AI-generated summary

Efficiently post-training [large language models](https://huggingface.co/papers?q=large%20language%20models) remains a challenging task due to the vast computational resources required. We present Spectrum, a method that accelerates LLM training by selectively targeting layer modules based on their [signal-to-noise ratio](https://huggingface.co/papers?q=signal-to-noise%20ratio) ([SNR](https://huggingface.co/papers?q=SNR)), and freezing the remaining modules. Our approach, which utilizes an algorithm to compute module [SNR](https://huggingface.co/papers?q=SNR) s prior to training, has shown to effectively match the performance of full fine-tuning while reducing GPU memory usage. Experiments comparing Spectrum to existing methods such as [QLoRA](https://huggingface.co/papers?q=QLoRA) demonstrate its effectiveness in terms of [model quality](https://huggingface.co/papers?q=model%20quality) and VRAM efficiency in [distributed environments](https://huggingface.co/papers?q=distributed%20environments).

### Community

[sugatoray](https://huggingface.co/sugatoray)

[Jun 12, 2024](#66699ef9c9b2c795ba61b565)

GitHub: [https://github.com/cognitivecomputations/spectrum](https://github.com/cognitivecomputations/spectrum)

[Xa9aX](https://huggingface.co/Xa9aX)

[Sep 4, 2024](#66d7dc8ca5098dc7702a803d)

The same theory has been established for years now by [https://github.com/CalculatedContent/WeightWatcher](https://github.com/CalculatedContent/WeightWatcher)  
However there is no attribution to the same which is a let down

Get this paper in your agent:

`hf papers read 2406.06623`

Don't have the latest CLI?

`curl -LsSf https://hf.co/cli/install.sh | bash`

## Models citing this paper 36

[Browse 36 models citing this paper](https://huggingface.co/models?other=arxiv:2406.06623)

## Datasets citing this paper 0

No dataset linking this paper

Cite arxiv.org/abs/2406.06623 in a dataset README.md to link it from this page.