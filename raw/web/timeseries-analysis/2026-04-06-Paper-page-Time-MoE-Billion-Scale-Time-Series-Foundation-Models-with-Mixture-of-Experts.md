---
source_type: web
title: "Paper page - Time-MoE: Billion-Scale Time Series Foundation Models with Mixture of  Experts"
author: 
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
created: 2026-04-06
description: "Join the discussion on this paper page"
tags:
  - 
  - "clippings"
source_url: "https://huggingface.co/papers/2409.16040"
published_at: 2024-09-25
related_concepts: []
---

arxiv:2409.16040

## Time-MoE: Billion-Scale Time Series Foundation Models with Mixture of Experts

Authors:

## Abstract

Time-MoE, a scalable and efficient architecture using a sparse mixture-of-experts design, achieves state-of-the-art time series forecasting by pre-training large models on a massive dataset without increasing inference costs.

AI-generated summary

Deep learning for time series forecasting has seen significant advancements over the past decades. However, despite the success of large-scale pre-training in language and vision domains, pre-trained time series models remain limited in scale and operate at a high cost, hindering the development of larger capable forecasting models in real-world applications. In response, we introduce [Time-MoE](https://huggingface.co/papers?q=Time-MoE), a scalable and unified architecture designed to pre-train larger, more capable forecasting foundation models while reducing inference costs. By leveraging a sparse [mixture-of-experts](https://huggingface.co/papers?q=mixture-of-experts) ([MoE](https://huggingface.co/papers?q=MoE)) design, [Time-MoE](https://huggingface.co/papers?q=Time-MoE) enhances [computational efficiency](https://huggingface.co/papers?q=computational%20efficiency) by activating only a subset of networks for each prediction, reducing computational load while maintaining high model capacity. This allows [Time-MoE](https://huggingface.co/papers?q=Time-MoE) to scale effectively without a corresponding increase in inference costs. [Time-MoE](https://huggingface.co/papers?q=Time-MoE) comprises a family of decoder-only transformer models that operate in an [auto-regressive](https://huggingface.co/papers?q=auto-regressive) manner and support flexible [forecasting horizons](https://huggingface.co/papers?q=forecasting%20horizons) with varying [input context lengths](https://huggingface.co/papers?q=input%20context%20lengths). We pre-trained these models on our newly introduced large-scale data [Time-300B](https://huggingface.co/papers?q=Time-300B), which spans over 9 domains and encompassing over 300 billion time points. For the first time, we scaled a time series foundation model up to 2.4 billion parameters, achieving significantly improved [forecasting precision](https://huggingface.co/papers?q=forecasting%20precision). Our results validate the applicability of [scaling laws](https://huggingface.co/papers?q=scaling%20laws) for training tokens and model size in the context of time series forecasting. Compared to dense models with the same number of activated parameters or equivalent computation budgets, our models consistently outperform them by large margin. These advancements position [Time-MoE](https://huggingface.co/papers?q=Time-MoE) as a state-of-the-art solution for tackling real-world time series forecasting challenges with superior capability, efficiency, and flexibility.

### Community

[akhaliq](https://huggingface.co/akhaliq)

Paper submitter [Sep 25, 2024](#66f39a4ed1d8877758db1407)

[https://github.com/Time-MoE/Time-MoE](https://github.com/Time-MoE/Time-MoE)

[librarian-bot](https://huggingface.co/librarian-bot)

[Sep 26, 2024](#66f4b9face2502886ee1655e)

This is an automated message from the [Librarian Bot](https://huggingface.co/librarian-bots). I found the following papers similar to this paper.

The following papers were recommended by the Semantic Scholar API

- [Towards Long-Context Time Series Foundation Models](https://huggingface.co/papers/2409.13530) (2024)
- [LaDiMo: Layer-wise Distillation Inspired MoEfier](https://huggingface.co/papers/2408.04278) (2024)
- [Empowering Pre-Trained Language Models for Spatio-Temporal Forecasting via Decoupling Enhanced Discrete Reprogramming](https://huggingface.co/papers/2408.14505) (2024)
- [VisionTS: Visual Masked Autoencoders Are Free-Lunch Zero-Shot Time Series Forecasters](https://huggingface.co/papers/2408.17253) (2024)
- [GRIN: GRadient-INformed MoE](https://huggingface.co/papers/2409.12136) (2024)

Please give a thumbs up to this comment if you found it helpful!

If you want recommendations for any Paper on Hugging Face checkout [this](https://huggingface.co/spaces/librarian-bots/recommend_similar_papers) Space

You can directly ask Librarian Bot for paper recommendations by tagging it in a comment: `@librarian-bot  recommend`

Get this paper in your agent:

`hf papers read 2409.16040`

Don't have the latest CLI?

`curl -LsSf https://hf.co/cli/install.sh | bash`

## Models citing this paper 5

[Browse 5 models citing this paper](https://huggingface.co/models?other=arxiv:2409.16040)