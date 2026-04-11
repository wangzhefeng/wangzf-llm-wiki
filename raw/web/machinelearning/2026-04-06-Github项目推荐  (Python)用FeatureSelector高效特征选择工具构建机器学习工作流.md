---
source_type: web
title: "Github项目推荐 | (Python)用FeatureSelector高效特征选择工具构建机器学习工作流"
author:
  - 
  - "[[Will Koehrsen]]"
created_at: 2026-04-06
topics:
  - 机器学习
status: inbox
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
source_url: "https://mp.weixin.qq.com/s?__biz=MzU1MjYzNjQwOQ==&mid=2247485147&idx=1&sn=0bba2ec9c8f43379ae599ad5f5c71464&chksm=fbfe5c4dcc89d55b5ab61a5782c5ea3594e2d2b73587ff3c1311b1b040379f42af6ca05dc779&mpshare=1&scene=1&srcid=&key=ff85e6c2ecb95825f1698b98daf49269a5112337140a746f63705e6f0d1e218a1f9bd0a2827715ec129b8a666d1e9d5edceeabe8c1e831a707cbabfab975957a6dddbe6da5356dc0599af5cd9a7e2776&ascene=1&uin=NzQ1MDMwNQ%3D%3D&devicetype=Windows+7&version=62060728&lang=zh_CN&pass_ticket=69eQVGs9alMeuD%2FjJMEbQvweQaVGUdwjJXObXjJbH%2FM%3D"
published_at: null
related_concepts: []
---

Will Koehrsen *2019年3月13日 11:44*

点击上方“ **AI派** ”，选择“ **设为星标** ”  

最新分享，第一时间送达！

> 来源：AI研习社
> 
> 链接：  
> https://mp.weixin.qq.com/s/6e\_FBqIDQiUzoydyi4vFtQ

*Feature Selector: Simple Feature Selection in Python*

by Will Koehrsen

FeatureSelector是用于降低机器学习数据集的维数的工具。

文章介绍：

https://towardsdatascience.com/a-feature-selection-tool-for-machine-learning-in-python-b64dd23710f0

项目地址：

https://github.com/WillKoehrsen/feature-selector

### 方法

有五种方法可用于识别要删除的特征：

1. 缺失值
2. 单一唯一值
3. 共线特征
4. 零重要性特征
5. 低重要性特征

### 使用

有关使用方法，请参阅 Feature Selector的使用指南

### 可视化

FeatureSelector还包括许多可视化方法，用于检查数据集的特征。

#### 相关热图

![图片](https://mp.weixin.qq.com/1551768343129489.png "1551768343129489.png")

#### 最重要的特征

![图片](https://mp.weixin.qq.com/1551768355541105.png "1551768355541105.png")

使用环境要求：

```
python==3.6+
lightgbm==2.1.1
matplotlib==2.1.2
seaborn==0.8.1
numpy==1.14.5
pandas==0.23.1
scikit-learn==0.19.1
```

历史推荐

[人人都是数据分析师，人人都能玩转Pandas](http://mp.weixin.qq.com/s?__biz=MzU1MjYzNjQwOQ==&mid=2247484289&idx=1&sn=a9175a7395c4b43471431c8a544de1c4&chksm=fbfe5917cc89d0017e323d1ae7e1c0632696f67c7f2c960b3d5bf5d3d7110cfdc01b3554415d&scene=21#wechat_redirect) | [Numpy 精品系列教程汇](http://mp.weixin.qq.com/s?__biz=MzU1MjYzNjQwOQ==&mid=2247483800&idx=1&sn=91e89daf490f150da31ddb3d5d9cfe0c&chksm=fbfe5b0ecc89d2189bbecdd9ccd67b622e79a8b1bff38a8e7002c3aad69505066324507143f4&scene=21#wechat_redirect) [总 |](http://mp.weixin.qq.com/s?__biz=MzU1MjYzNjQwOQ==&mid=2247483800&idx=1&sn=91e89daf490f150da31ddb3d5d9cfe0c&chksm=fbfe5b0ecc89d2189bbecdd9ccd67b622e79a8b1bff38a8e7002c3aad69505066324507143f4&scene=21#wechat_redirect) [我是如何入门机器学习的呢 |](http://mp.weixin.qq.com/s?__biz=MzU1MjYzNjQwOQ==&mid=2247484052&idx=1&sn=99b1b8f32f92c4d05e7add5c2a5c0747&chksm=fbfe5802cc89d114c6c36056658db7ab9e2d50b89e5b26994efbd7528726a1d6edec31ecb6c6&scene=21#wechat_redirect) [谷歌机器学习43条黄金法则](http://mp.weixin.qq.com/s?__biz=MzU1MjYzNjQwOQ==&mid=2247483970&idx=1&sn=c7ec8df87dc0261d37de61956da46078&chksm=fbfe58d4cc89d1c24339560d419541c08760f6a658fd28df40e8b733ce58fc14c3c7b71d60b5&scene=21#wechat_redirect)

  
![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

长按，识别二维码，加关注

继续滑动看下一个

AI派

向上滑动看下一个