---
title: XGBoost 安装
author: wangzf
date: '2024-09-18'
slug: ml-gbm-xgboost-install
categories:
  - machine-learning
tags:
  - model
source_type: local_note
created_at: 2024-09-18
topics:
  - machine-learning
status: inbox
---



<details><summary>目录</summary><p>

- [Linux](#linux)
- [Windows](#windows)
- [macOS](#macos)
</p></details><p></p>

## Linux

1. 下载源码

```bash
$ git clone --recursive https://github.com/dmlc/xgboost
```

2. 编译 `libxgboost.so`

```bash
$ cd xgboost
$ make -j4
```

3. 如果需要支持 GPU，则需要执行以下步骤

```bash
$ cd xgboost
$ mkdir build
$ cd build
$ cmake .. -DUSE_CUDA=ON
$ cd ..
make -j4
```

4. 安装 Python 支持

```bash
$ cd python-package
$ sudo python setup.py intall
```

## Windows

1. 下载源码

```bash
$ git clone --recursive https://github.com/dmlc/xgboost
$ git submodule init
$ git submodule update
```

2. 编译 `libxgboost.dll`

```bash
$ cd xgboost
$ make -j4
```

3. 如果需要支持 GPU，则需要执行以下步骤

```bash
$ cd xgboost
$ mkdir build
$ cd build
$ cmake .. -DUSE_CUDA=ON
$ cd ..
make -j4
```

4. 安装 Python 支持

```bash
$ cd python-package
$ python setup.py intall
```

## macOS

