---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: Time Series Orchestra (TSorchestra) is a novel ensemble framework designed
  for zero-shot time series forecasting. It is built upon a curated collection of
  time series foundation models. The architecture is designed to leverage the specialized
  capabilities of its constituent models to deliver SOTA performance and generalization
  across datasets. - DC-research/TSorchestra
source_type: web
status: inbox
tags:
- null
- clippings
title: 'DC-research/TSorchestra: Time Series Orchestra (TSorchestra) is a novel ensemble
  framework designed for zero-shot time series forecasting. It is built upon a curated
  collection of time series foundation models. The architecture is designed to leverage
  the specialized capabilities of its constituent models to deliver SOTA performance
  and generalization across datasets.'
source_url: https://github.com/DC-research/TSorchestra
published_at: null
related_concepts: []
topics:
  - timeseries-analysis
  - 时间序列分析
---

## TSorchestra

\[Ongoing Project\]

Time Series Orchestra (TSorchestra) is a novel ensemble framework designed for zero-shot time series forecasting. It's a curated collection of time series foundation models (TSFMs) that leverages each TSFM's strengths to create something greater than the sum of its parts, yielding SOTA performance.

## Set Up

---

1. Create a new conda environment named `tso` from our.yml file:
```
conda env create -f environment.yml
```
1. Download the [GIFT-Eval benchmark](https://huggingface.co/spaces/Salesforce/GIFT-Eval) from Hugging Face:
```
mkdir data
huggingface-cli download Salesforce/GiftEval --repo-type=dataset --local-dir data
```
1. Set up the environment variable for loading the datasets: `bash  echo "GIFT_EVAL=data" >> .env `

## Usage

---

Run our evaluation script to reproduce our results:

```
chmod +x ./cli/eval.sh
./cli/eval.sh
```