---
source_type: web
title: "kwuking/TimeMixer: [ICLR 2024] Official implementation of \"TimeMixer: Decomposable Multiscale Mixing for Time Series Forecasting\""
author: 
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
source: "https://github.com/kwuking/TimeMixer"
published: 
created: 2026-04-06
description: "[ICLR 2024] Official implementation of \"TimeMixer: Decomposable Multiscale Mixing for Time Series Forecasting\" - kwuking/TimeMixer"
tags:
  - 
  - "clippings"
---

## (ICLR'24) TimeMixer: Decomposable Multiscale Mixing for Time Series Forecasting

**\[[Paper Page](https://openreview.net/pdf?id=7oLshfEIC2)\]** **\[[ICLR Video](https://iclr.cc/virtual/2024/poster/19347)\]** **\[[Medium Blog](https://medium.com/towards-data-science/timemixer-exploring-the-latest-model-in-time-series-forecasting-056d9c883f46)\]**

**\[[中文解读1](https://mp.weixin.qq.com/s/d7fEnEpnyW5T8BN08XRi7g)\]** **\[[中文解读2](https://mp.weixin.qq.com/s/MsJmWfXuqh_pTYlwve6O3Q)\]** **\[[中文解读3](https://zhuanlan.zhihu.com/p/686772622)\]** **\[[中文解读4](https://mp.weixin.qq.com/s/YZ7L1hImIt-jbRT2tizyQw)\]**

---

> 🙋 Please let us know if you find out a mistake or have any suggestions!
> 
> 🌟 If you find this resource helpful, please consider to star this repository and cite our research:

```
@inproceedings{wang2023timemixer,
  title={TimeMixer: Decomposable Multiscale Mixing for Time Series Forecasting},
  author={Wang, Shiyu and Wu, Haixu and Shi, Xiaoming and Hu, Tengge and Luo, Huakun and Ma, Lintao and Zhang, James Y and ZHOU, JUN},
  booktitle={International Conference on Learning Representations (ICLR)},
  year={2024}
}

@article{wang2024timemixer++,
  title={TimeMixer++: A General Time Series Pattern Machine for Universal Predictive Analysis},
  author={Wang, Shiyu and Li, Jiawei and Shi, Xiaoming and Ye, Zhou and Mo, Baichuan and Lin, Wenze and Ju, Shengtong and Chu, Zhixuan and Jin, Ming},
  journal={arXiv preprint arXiv:2410.16032},
  year={2024}
}
```

## Updates

🚩 **News** (2024.10): TimeMixer series has been included in **[PyPOTS](https://pypots.com/)**. Many thanks to the PyPOTS team.

🚩 **News** (2024.10): We have newly released **[TimeMixer++](https://arxiv.org/abs/2410.16032)** as an upgraded version of TimeMixer. **TimeMixer++ is a time series pattern machine** that employs multi-scale and multi-resolution pattern extraction to **achieve 🏆state-of-the-art across 8 diverse analytical tasks!**

🚩 **News** (2024.07): TimeMixer has been included in **[NeuralForecast](https://github.com/Nixtla/neuralforecast)**. Special thanks to the contributor @ [marcopeix](https://github.com/marcopeix) and @ [JQGoh](https://github.com/JQGoh)!

🚩 **News** (2024.07) TimeMixer has evolved into a **large model supporting comprehensive time series analysis, including long-term forecasting, short-term forecasting, anomaly detection, imputation, and classification**. In the future, we will further explore additional types of time series analysis tasks and strive to break through the limitations of current long-term forecasting to achieve efficient extreme-long-term time series forecasting.

🚩 **News** (2024.06) **Introduction of TimeMixer** in **[Chinese](https://mp.weixin.qq.com/s/d7fEnEpnyW5T8BN08XRi7g)** is available.

🚩 **News** (2024.05) TimeMixer has now released a **28-page full paper version on [arXiv](https://arxiv.org/abs/2405.14616)**. Furthermore, we have provided a **brief [video](https://iclr.cc/virtual/2024/poster/19347)** to facilitate your understanding of our work.

🚩 **News** (2024.05) TimeMixer currently **supports using future temporal features for prediction**. This feature has been well-received by the community members. You can now decide whether to enable this feature by using the parameter use\_future\_temporal\_feature.

🚩 **News** (2024.03) TimeMixer has been included in [\[**Time-Series-Library**\]](https://github.com/thuml/Time-Series-Library) and achieve the consistent 🏆 **state-of-the-art** in **long-term time and short-term series forecasting**.

🚩 **News** (2024.03) TimeMixer has added a time-series decomposition method based on DFT, as well as downsampling operation based on 1D convolution.

🚩 **News** (2024.02) TimeMixer has been accepted as **ICLR 2024 Poster**.

## Introduction

🏆 **TimeMixer**, as a fully MLP-based architecture, taking full advantage of disentangled multiscale time series, is proposed to **achieve consistent SOTA performances in both long and short-term forecasting tasks with favorable run-time efficiency**.

🌟 **Observation 1: History Extraction**

Given that seasonal and trend components exhibit significantly different characteristics in time series, and different scales of the time series reflect different properties, with seasonal characteristics being more pronounced at a fine-grained micro-scale and trend characteristics being more pronounced at a coarse macro scale, it is, therefore, necessary to decouple seasonal and trend components at different scales.

[![[assets/attachments/timeseries/motivation1.png]]](https://github.com/kwuking/TimeMixer/blob/main/figures/motivation1.png)

🌟 **Observation 2: Future Prediction**

Different scales exhibit complementary predictive capabilities when integrating forecasts from different scales to obtain the final prediction results.

[![[assets/attachments/timeseries/motivation2.png]]](https://github.com/kwuking/TimeMixer/blob/main/figures/motivation2.png)

## Overall Architecture

TimeMixer as a fully MLP-based architecture with **Past-Decomposable-Mixing (PDM)** and **Future-Multipredictor-Mixing (FMM)** blocks to take full advantage of disentangled multiscale series in both past extraction and future prediction phases.

[![[assets/attachments/timeseries/overall.png]]](https://github.com/kwuking/TimeMixer/blob/main/figures/overall.png)

### Past Decomposable Mixing

we propose the **Past-Decomposable-Mixing (PDM)** block to mix the decomposed seasonal and trend components in multiple scales separately.

[![[assets/attachments/timeseries/past_mixing1.png]]](https://github.com/kwuking/TimeMixer/blob/main/figures/past_mixing1.png)

Empowered by seasonal and trend mixing, PDM progressively aggregates the detailed seasonal information from fine to coarse and dive into the macroscopic trend information with prior knowledge from coarser scales, eventually achieving the multiscale mixing in past information extraction.

[![[assets/attachments/timeseries/past_mixing2.png]]](https://github.com/kwuking/TimeMixer/blob/main/figures/past_mixing2.png)

### Future Multipredictor Mixing

Note that **Future Multipredictor Mixing (FMM)** is an ensemble of multiple predictors, where different predictors are based on past information from different scales, enabling FMM to integrate complementary forecasting capabilities of mixed multiscale series.

[![[assets/attachments/timeseries/future_mixing.png]]](https://github.com/kwuking/TimeMixer/blob/main/figures/future_mixing.png)

## Get Started

1. Install requirements. `pip install -r requirements.txt`
	> If you are using **Python 3.8**, please change the `sktime` version in `requirements.txt` to `0.29.1`
2. Download data. You can download all datasets from [Google Driver](https://drive.google.com/u/0/uc?id=1NF7VEefXCmXuWNbnNe858WvQAkJ_7wuP&export=download), [Baidu Driver](https://pan.baidu.com/share/init?surl=r3KhGd0Q9PJIUZdfEYoymg&pwd=i9iy) or [Kaggle Datasets](https://www.kaggle.com/datasets/wentixiaogege/time-series-dataset). **All the datasets are well pre-processed** and can be used easily.
3. Train the model. We provide the experiment scripts of all benchmarks under the folder `./scripts`. You can reproduce the experiment results by:
```
bash ./scripts/long_term_forecast/ETT_script/TimeMixer_ETTm1.sh
bash ./scripts/long_term_forecast/ECL_script/TimeMixer.sh
bash ./scripts/long_term_forecast/Traffic_script/TimeMixer.sh
bash ./scripts/long_term_forecast/Solar_script/TimeMixer.sh
bash ./scripts/long_term_forecast/Weather_script/TimeMixer.sh
bash ./scripts/short_term_forecast/M4/TimeMixer.sh
bash ./scripts/short_term_forecast/PEMS/TimeMixer.sh
```

## Main Results

We conduct extensive experiments to evaluate the performance and efficiency of TimeMixer, covering long-term and short-term forecasting, including 18 real-world benchmarks and 15 baselines. **🏆 TimeMixer achieves consistent state-of-the-art performance in all benchmarks**, covering a large variety of series with different frequencies, variate numbers and real-world scenarios.

### Long-term Forecasting

To ensure fairness in model comparison, experiments were performed with standardized parameters, including aligned input lengths, batch sizes, and training epochs. Additionally, given that results in various studies often stem from hyperparameter optimization, we include outcomes from comprehensive parameter searches.

[![[assets/attachments/timeseries/long_results.png]]](https://github.com/kwuking/TimeMixer/blob/main/figures/long_results.png)

### Short-term Forecasting: Multivariate data

[![[assets/attachments/timeseries/pems_results.png]]](https://github.com/kwuking/TimeMixer/blob/main/figures/pems_results.png)

### Short-term Forecasting: Univariate data

[![[assets/attachments/timeseries/m4_results.png]]](https://github.com/kwuking/TimeMixer/blob/main/figures/m4_results.png)

## Model Abalations

To verify the effectiveness of each component of TimeMixer, we provide the detailed ablation study on every possible design in both Past-Decomposable-Mixing and Future-Multipredictor-Mixing blocks on all 18 experiment benchmarks （see our paper for full results 😊）.

[![[assets/attachments/timeseries/ablation.png]]](https://github.com/kwuking/TimeMixer/blob/main/figures/ablation.png)

## Model Efficiency

We compare the running memory and time against the latest state-of-the-art models under the training phase, where TimeMixer consistently demonstrates favorable efficiency, in terms of both GPU memory and running time, for various series lengths (ranging from 192 to 3072), in addition to the consistent state-of-the-art performances for both long-term and short-term forecasting tasks. **It is noteworthy that TimeMixer, as a deep model, demonstrates results close to those of full-linear models in terms of efficiency. This makes TimeMixer promising in a wide range of scenarios that require high model efficiency.**

[![[assets/attachments/timeseries/efficiency.png]]](https://github.com/kwuking/TimeMixer/blob/main/figures/efficiency.png)