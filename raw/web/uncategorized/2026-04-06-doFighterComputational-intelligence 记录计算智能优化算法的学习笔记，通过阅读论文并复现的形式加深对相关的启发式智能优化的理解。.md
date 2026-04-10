---
source_type: web
title: "doFighter/Computational-intelligence: 记录计算智能优化算法的学习笔记，通过阅读论文并复现的形式加深对相关的启发式智能优化的理解。"
author: 
created_at: 2026-04-06
topics:
  - 待分类
status: inbox
source: "https://github.com/doFighter/Computational-intelligence"
published: 
created: 2026-04-06
description: "记录计算智能优化算法的学习笔记，通过阅读论文并复现的形式加深对相关的启发式智能优化的理解。. Contribute to doFighter/Computational-intelligence development by creating an account on GitHub."
tags:
  - 
  - "clippings"
---

## Computational-intelligence

记录计算智能优化算法的学习笔记，通过阅读论文并复现的形式加深对相关的启发式智能优化的理解。

论文复现目前有 `matlab` 及 `python` 版，由于个人能力有限，因此难以避免论文代码复现中存在的错误，如有相关不妥之处，还望指正。

在每篇的笔记当中，存在部分个人的观点，该观点仅供参考！

## 内容目录

### 单目标优化

#### 粒子群优化

- [经典粒子群优化](https://github.com/doFighter/Computational-intelligence/blob/main/%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95/%E7%BB%8F%E5%85%B8%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96/%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96%E4%B8%80.md) (`OPSO/VPSO,1998`)
- [带收缩因子的粒子群优化](https://github.com/doFighter/Computational-intelligence/blob/main/%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95/%E5%B8%A6%E6%94%B6%E7%BC%A9%E5%9B%A0%E5%AD%90%E7%9A%84%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96/%E4%B8%80%E7%A7%8D%E4%BD%BF%E7%94%A8%E6%94%B6%E7%BC%A9%E5%9B%A0%E5%AD%90%E7%9A%84%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95.md) (`VPSO,2002`)
- [综合学习粒子群优化](https://github.com/doFighter/Computational-intelligence/blob/main/%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95/%E7%BB%BC%E5%90%88%E5%AD%A6%E4%B9%A0%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96/%E7%BB%BC%E5%90%88%E5%AD%A6%E4%B9%A0%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95.md) (`CLPSO,2006`)
- [自适应粒子群优化](https://github.com/doFighter/Computational-intelligence/blob/main/%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95/%E8%87%AA%E9%80%82%E5%BA%94%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96/%E8%87%AA%E9%80%82%E5%BA%94%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95.md) (`APSO,2009`)
- [双中心粒子群优化](https://github.com/doFighter/Computational-intelligence/blob/main/%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95/%E5%8F%8C%E4%B8%AD%E5%BF%83%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96/%E5%8F%8C%E4%B8%AD%E5%BF%83%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96.md) (`DCPSO,2012`)
- [完全受扰的混沌粒子群优化](https://github.com/doFighter/Computational-intelligence/blob/main/%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95/%E5%AE%8C%E5%85%A8%E5%8F%97%E6%89%B0%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96/%E5%AE%8C%E5%85%A8%E5%8F%97%E6%89%B0%E7%9A%84%E6%B7%B7%E6%B2%8C%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95.md) (`TDPSO,2015`)
- [一种基于Sigmoid函数的自适应加权粒子群优化器](https://github.com/doFighter/Computational-intelligence/blob/main/%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95/%E4%B8%80%E7%A7%8D%E6%96%B0%E7%9A%84%E5%9F%BA%E4%BA%8ESigmoid%E5%87%BD%E6%95%B0%E7%9A%84%E8%87%AA%E9%80%82%E5%BA%94%E5%8A%A0%E6%9D%83%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96%E5%99%A8/%E4%B8%80%E7%A7%8D%E5%9F%BA%E4%BA%8ESigmoid%E5%87%BD%E6%95%B0%E7%9A%84%E8%87%AA%E9%80%82%E5%BA%94%E5%8A%A0%E6%9D%83%E7%B2%92%E5%AD%90%E7%BE%A4%E4%BC%98%E5%8C%96%E5%99%A8.md) (`AWPSO,2021`)

#### 蚁群算法

- [蚂蚁系统](https://github.com/doFighter/Computational-intelligence/blob/main/%E8%9A%81%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95/%E8%9A%82%E8%9A%81%E7%B3%BB%E7%BB%9F/%E8%9A%82%E8%9A%81%E7%B3%BB%E7%BB%9F.md) (`AS,1996`)
- [蚁群系统](https://github.com/doFighter/Computational-intelligence/blob/main/%E8%9A%81%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95/%E8%9A%81%E7%BE%A4%E7%B3%BB%E7%BB%9F/%E8%9A%81%E7%BE%A4%E7%B3%BB%E7%BB%9F.md) (`ACS,1997`)
- [最大最小蚂蚁系统](https://github.com/doFighter/Computational-intelligence/blob/main/%E8%9A%81%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95/%E6%9C%80%E5%A4%A7%E6%9C%80%E5%B0%8F%E8%9A%82%E8%9A%81%E7%B3%BB%E7%BB%9F/%E6%9C%80%E5%A4%A7%E6%9C%80%E5%B0%8F%E8%9A%82%E8%9A%81%E7%B3%BB%E7%BB%9F.md) (`MMAS,2000`)
- [一种改进的自适应蚁群算法](https://github.com/doFighter/Computational-intelligence/blob/main/%E8%9A%81%E7%BE%A4%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95/%E4%B8%80%E7%A7%8D%E6%94%B9%E8%BF%9B%E7%9A%84%E8%87%AA%E9%80%82%E5%BA%94%E8%9A%81%E7%BE%A4%E7%AE%97%E6%B3%95/%E4%B8%80%E7%A7%8D%E6%94%B9%E8%BF%9B%E7%9A%84%E8%87%AA%E9%80%82%E5%BA%94%E8%9A%81%E7%BE%A4%E7%AE%97%E6%B3%95.md) (`IAACO,2021`)

#### 遗传算法

- [经典遗传算法](https://github.com/doFighter/Computational-intelligence/blob/main/%E9%81%97%E4%BC%A0%E7%AE%97%E6%B3%95/%E7%BB%8F%E5%85%B8%E9%81%97%E4%BC%A0%E7%AE%97%E6%B3%95-GA/%E7%BB%8F%E5%85%B8%E9%81%97%E4%BC%A0%E7%AE%97%E6%B3%95-GA.md) (`GA,1994`)

#### 狼群算法

#### 哈里斯鹰优化算法

- [哈里斯鹰优化算法](https://github.com/doFighter/Computational-intelligence/blob/main/%E5%93%88%E9%87%8C%E6%96%AF%E9%B9%B0%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95/%E5%93%88%E9%87%8C%E6%96%AF%E9%B9%B0%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95\(HHO\)/%E5%93%88%E9%87%8C%E6%96%AF%E9%B9%B0%E4%BC%98%E5%8C%96%E7%AE%97%E6%B3%95.md) (`HHO,2019`)

#### 麻雀算法

- [麻雀搜索算法](https://github.com/doFighter/Computational-intelligence/blob/main/%E9%BA%BB%E9%9B%80%E6%90%9C%E7%B4%A2%E7%AE%97%E6%B3%95/%E9%BA%BB%E9%9B%80%E6%90%9C%E7%B4%A2%E7%AE%97%E6%B3%95SSA/%E9%BA%BB%E9%9B%80%E6%90%9C%E7%B4%A2%E7%AE%97%E6%B3%95.md) (`SSA,2020`)

#### 萤火虫算法

- [萤火虫优化](https://github.com/doFighter/Computational-intelligence/blob/main/%E8%90%A4%E7%81%AB%E8%99%AB%E7%AE%97%E6%B3%95/%E8%90%A4%E7%81%AB%E8%99%AB%E4%BC%98%E5%8C%96FA/%E8%90%A4%E7%81%AB%E8%99%AB%E7%AE%97%E6%B3%95.md) (`FA,2009`)