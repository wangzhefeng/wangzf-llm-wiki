---
source_type: web
title: "Welcome to TorchMetrics — PyTorch-Metrics 1.9.0 documentation"
author: 
created_at: 2026-04-06
topics:
  - 深度学习
status: inbox
source: "https://lightning.ai/docs/torchmetrics/stable/"
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
---

## Welcome to TorchMetrics

TorchMetrics is a collection of 100+ PyTorch metrics implementations and an easy-to-use API to create custom metrics. It offers:

- A standardized interface to increase reproducibility
- Reduces Boilerplate
- Distributed-training compatible
- Rigorously tested
- Automatic accumulation over batches
- Automatic synchronization between multiple devices

You can use TorchMetrics in any PyTorch model, or within [PyTorch Lightning](https://lightning.ai/docs/pytorch/stable/) to enjoy the following additional benefits:

- Your data will always be placed on the same device as your metrics
- You can log [`Metric`](https://lightning.ai/docs/torchmetrics/stable/references/metric.html#torchmetrics.Metric "torchmetrics.Metric") objects directly in Lightning to reduce even more boilerplate

---

## Install TorchMetrics

For pip users

```bash
pip install torchmetrics
```

Or directly from conda

```bash
conda install -c conda-forge torchmetrics
```

---

### [New to TorchMetrics?](https://lightning.ai/docs/torchmetrics/stable/pages/quickstart.html)

Use this quickstart guide to learn key concepts.

### [TorchMetrics with PyTorch Lightning](https://lightning.ai/docs/torchmetrics/stable/pages/lightning.html)

Easily use TorchMetrics in your PyTorch Lightning code.

### [Metrics](https://lightning.ai/docs/torchmetrics/stable/all-metrics.html)

View the full list of metrics and filter by task and data type.

### [Overview](https://lightning.ai/docs/torchmetrics/stable/pages/overview.html)

A detailed overview of the TorchMetrics API and concepts.

### [Custom Metrics](https://lightning.ai/docs/torchmetrics/stable/pages/implement.html)

Learn how to implement a custom metric with TorchMetrics.

### [API Reference](https://lightning.ai/docs/torchmetrics/stable/references/metric.html)

Detailed descriptions of each API package.