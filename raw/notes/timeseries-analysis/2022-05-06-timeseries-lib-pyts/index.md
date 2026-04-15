---
title: pyts
subtitle: 时间序列分类
author: wangzf
date: '2022-05-06'
slug: timeseries-lib-pyts
categories:
  - timeseries
tags:
  - tool
source_type: notes
created_at: 2022-05-06
status: summarized
related_concepts:
  - 时间序列预测
  - 时间序列工具库
topics:
  - timeseries-analysis
  - 时间序列分析
---



<details><summary>目录</summary><p>

- [pyts Demo](#pyts-demo)
- [pyts 安装](#pyts-安装)
- [特征提取](#特征提取)
  - [Shapelet Transform](#shapelet-transform)
- [参考](#参考)
</p></details><p></p>

## pyts Demo

```python
from pyts.classification import BOSSVS
from pyts.datasets import load_gunpoint

X_train, X_test, y_train, y_test = load_gunpoint(return_X_y = True)
clf = BOSSVS(window_size = 28)
clf.fit(X_train, y_train)
clf.score(X_test, y_test)
```

## pyts 安装

```bash
$ pip install pyts
```

## 特征提取

### Shapelet Transform




## 参考

* Time Series Classifification from Scratch with Deep Neural Networks: A Strong Baseline
* [DTW & KNN](https://nbviewer.jupyter.org/github/markdregan/K-Nearest-Neighbors-with-Dynamic-Time-Warping/blob/master/K_Nearest_Neighbor_Dynamic_Time_Warping.ipynb)
* [BiGRU CNN](http://www.doc88.com/p-0334856528441.html)
* LSTM Fully Convolutional Networks for Time Series Classification
* [PyTS GitHub](https://github.com/johannfaouzi/pyts)
* [PyTS Doc](https://pyts.readthedocs.io/en/latest/)
