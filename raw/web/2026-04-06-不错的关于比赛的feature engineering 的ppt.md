---
source_type: web
title: "不错的关于比赛的feature engineering 的ppt"
author:
  - 
  - "[[马东什么算法工程师]]"
created_at: 2026-04-06
topics:
  - 待分类
status: inbox
source: "https://zhuanlan.zhihu.com/p/85242628"
published: 
created: 2026-04-06
description: "“More data beats clever algorithms, but better data beats more data.”——名人名言哈哈哈哈，更多的数据打败聪明的算法，更好的数据打败更多的数据。 特征工程 •数据科学最需要创意的方面。 •像对待其他任…"
tags:
  - 
  - "clippings"
---

![[assets/attachments/uncategorized/v2-c7aabf84f6f36752757367f82a71dd91_1440w.jpg]]

“More data beats clever algorithms, but better data beats more data.”——名人名言哈哈哈哈，更多的数据打败聪明的算法，更好的数据打败更多的数据。

![[assets/attachments/uncategorized/v2-608823133a7eed6afad9cace40bed2a7_1440w.jpg]]

特征工程

• [数据科学](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E7%A7%91%E5%AD%A6&zhida_source=entity) 最需要创意的方面。

•像对待其他任何创造性工作一样对待 [特征工程](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=2&q=%E7%89%B9%E5%BE%81%E5%B7%A5%E7%A8%8B&zhida_source=entity) ，例如喜剧表演：

•一起头脑风暴

•创建特征工程的模板/公式

•检查/重新检查以前的工作

![[assets/attachments/uncategorized/v2-b97cdd8dbb068051e388e0fdfd54cbc0_1440w.jpg]]

类别特征

•几乎总是需要一些处理

•高基数类别特征会导致非常稀疏的数据

•难以做 [缺失值插补](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E7%BC%BA%E5%A4%B1%E5%80%BC%E6%8F%92%E8%A1%A5&zhida_source=entity)

![[assets/attachments/uncategorized/v2-a88c1a805501a81c8fb56522406a98da_1440w.jpg]]

Onehot编码

•对长度为K的数组进行K编码。

•可以与大多数 [线性算法](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E7%BA%BF%E6%80%A7%E7%AE%97%E6%B3%95&zhida_source=entity) 一起使用

•删除第一列可避免 [共线性](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E5%85%B1%E7%BA%BF%E6%80%A7&zhida_source=entity) （pd.get\_dummies中有参数可以达到这个目的，其实就是用全0来表示一种类别其它都用1-0表示）

• [稀疏格式](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E7%A8%80%E7%96%8F%E6%A0%BC%E5%BC%8F&zhida_source=entity) 对于内存友好（csr\_matrix）

•大多数当前的处理方法都不能很好地对待缺失值，以及新数据中的新类别

![[assets/attachments/uncategorized/v2-27a08ebb86c35ee7351b5631bdf68e4b_1440w.jpg]]

一个简单的例子。

![[assets/attachments/uncategorized/v2-71c8bacfd939560294f537c858dc8f26_1440w.jpg]]

[哈希编码](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E5%93%88%E5%B8%8C%E7%BC%96%E7%A0%81&zhida_source=entity)

•对固定长度的数组执行“ OneHot编码”。（不同的 [hash编码](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=hash%E7%BC%96%E7%A0%81&zhida_source=entity) 通过不同的算法将类别映射为一个唯一的值，例如对于类别A通过hash编码可能映射为qwe456这种6维序列，然后我们再去做onehot展开）

•避免极为稀疏的数据

•可能会引起碰撞（例如10000个类别用2位的hash编码，很容易出现不同类别最终映射的 [hash值](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=hash%E5%80%BC&zhida_source=entity) 是相同的，此现象称为碰撞—collisions）

•可以重复使用不同的 [哈希函数](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E5%93%88%E5%B8%8C%E5%87%BD%E6%95%B0&zhida_source=entity) 和袋结果，以降低准确性（意思应该是用不同的 [hash算法](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=hash%E7%AE%97%E6%B3%95&zhida_source=entity) 得到不同的编码值然后concat到一起尽量避免碰撞的发生）

•碰撞collisions通常会降低结果，但可能会改善结果（增强泛化性能）。

•优雅地处理新变量（例如：新的用户代理）（新的类别重新hash然后合并即可）（关于hash编码可见facebook对于文本的处理的那篇论文，忘了叫啥了，回头补充在编码的文章里好了）

![[assets/attachments/uncategorized/v2-e0780437588a806f5a1bc2a478d5d7e2_1440w.jpg]]

一个简单的例子

![[assets/attachments/uncategorized/v2-e288d8fba1fc632958998cbefb378601_1440w.jpg]]

为每个类别变量赋予唯一的数字ID

•对于基于非线性树的算法很有用（仅限于lightgbm和catboost这类可以直接处理类别的 [算法](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=6&q=%E7%AE%97%E6%B3%95&zhida_source=entity) ，xgb还是要进行别的处理）

•不增加维度

•将cat\_var-> num\_id映射随机化，然后进行平均再训练，以降低准确性。（没看明白）

![[assets/attachments/uncategorized/v2-a8dc5aba6c09120c9765063eec6acd51_1440w.jpg]]

一个简单的例子

![[assets/attachments/uncategorized/v2-4e40f15e548b72d0cb4f54993b0bcf37_1440w.jpg]]

计数编码（ [频率编码](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E9%A2%91%E7%8E%87%E7%BC%96%E7%A0%81&zhida_source=entity) ）

•将类别特征替换为训练集中的计数（一般是根据训练集来进行计数，属于统计编码的一种， [统计编码](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=2&q=%E7%BB%9F%E8%AE%A1%E7%BC%96%E7%A0%81&zhida_source=entity) ，就是用类别的统计特征来代替原始类别，比如类别A在训练集中出现了100次则编码为100）

•对线性和 [非线性算法](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E9%9D%9E%E7%BA%BF%E6%80%A7%E7%AE%97%E6%B3%95&zhida_source=entity) 均有用

•可能对 [异常值](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E5%BC%82%E5%B8%B8%E5%80%BC&zhida_source=entity) 敏感

•可以添加对数转换，可以很好地处理计数（主要是针对count编码之后 [特征分布](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E7%89%B9%E5%BE%81%E5%88%86%E5%B8%83&zhida_source=entity) 不规则的问题和常规的处理 [不规则分布](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E4%B8%8D%E8%A7%84%E5%88%99%E5%88%86%E5%B8%83&zhida_source=entity) 的连续特征是一样的方式）

•用'1'替换新数据中没见过的类别（没见过的类别如果有n个则编码为n）

•可能会产生冲突：相同的编码，不同的变量（不同类别出现次数一样）

![[assets/attachments/uncategorized/v2-a20560cd413f69dd8aa257e7b57c5e7d_1440w.jpg]]

一个简单的例子

![[assets/attachments/uncategorized/v2-59f118bf4d5c72e36c0df78735d458e6_1440w.jpg]]

LabelCount编码（就是对count编码进行排名）

•通过训练集中的计数对分类变量进行排名

•对线性和非线性算法均有用

•对异常值不敏感

•不会对不同的变量使用相同的编码

• 两全其美

![[assets/attachments/uncategorized/v2-1188023b60e2d4efefb28b643f221f94_1440w.jpg]]

一个简单的例子

![[assets/attachments/uncategorized/v2-5a66f1dccdcca4a99e9e02d649cecf45_1440w.jpg]]

[目标编码](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E7%9B%AE%E6%A0%87%E7%BC%96%E7%A0%81&zhida_source=entity)

•按目标变量的比例对分类变量进行编码（二分类或回归）（如果是多分类其实也可以编码，例如类别A对应的标签1有100个，标签2有100个，标签3有100个，则可以编码为【1/3,1/3,1/3】）

•注意避免 [过拟合](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E8%BF%87%E6%8B%9F%E5%90%88&zhida_source=entity) ！（原始的target encoding直接对全部的训练集数据和标签进行编码，会导致得到的编码结果太过依赖与训练集）

•堆叠形式：输出平均的目标的 [单变量模型](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E5%8D%95%E5%8F%98%E9%87%8F%E6%A8%A1%E5%9E%8B&zhida_source=entity)

•以交叉验证的方式进行（一般会进行交叉验证，比如划分为10折，每次对9折进行 [标签编码](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E6%A0%87%E7%AD%BE%E7%BC%96%E7%A0%81&zhida_source=entity) 然后用得到的标签编码模型预测第10折的特征得到结果，其实就是常说的 [均值编码](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E5%9D%87%E5%80%BC%E7%BC%96%E7%A0%81&zhida_source=entity) ）

•添加平滑以避免将变量编码设置为0。（某些类别可能只包含部分的类别会出现0值，此时会进行 [拉普拉斯平滑](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E6%8B%89%E6%99%AE%E6%8B%89%E6%96%AF%E5%B9%B3%E6%BB%91&zhida_source=entity) ，不过对于回归则没有这种问题）

•添加 [随机噪声](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E9%9A%8F%E6%9C%BA%E5%99%AA%E5%A3%B0&zhida_source=entity) 以应对过拟合（我一般用 [交叉验证](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=3&q=%E4%BA%A4%E5%8F%89%E9%AA%8C%E8%AF%81&zhida_source=entity) 不怎么加噪声）

•正确应用时：线性和非线性的最佳编码

![[assets/attachments/uncategorized/v2-8ad967abcbffde43a3fc0e166cc5db88_1440w.jpg]]

一个简单的例子。

![[assets/attachments/uncategorized/v2-ebdf9ec5047ba4ec299a626ef848154d_1440w.jpg]]

类别的embedding

•使用神经网络根据 [分类变量](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=3&q=%E5%88%86%E7%B1%BB%E5%8F%98%E9%87%8F&zhida_source=entity) 创建密集的嵌入。

•将分类变量映射到 [欧几里得空间](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E6%AC%A7%E5%87%A0%E9%87%8C%E5%BE%97%E7%A9%BA%E9%97%B4&zhida_source=entity)

•更快的模型训练。

•更少的内存开销。

•可以提供比1 [热编码](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E7%83%AD%E7%BC%96%E7%A0%81&zhida_source=entity) 更好的精度。

• [Entity Embeddings of Categorical Variables](https://link.zhihu.com/?target=https%3A//arxiv.org/abs/1604.06737) （回头补充到类别编码的内容里）

![[assets/attachments/uncategorized/v2-eb4fc3ad783d52afcc7ec89112e8bd03_1440w.jpg]]

一个简单的例子

![[assets/attachments/uncategorized/v2-dcdc44d075d5cc3968ca4cbc55605367_1440w.jpg]]

NaN编码

•给NaN值一个明确的编码，而不是忽略它

•NaN值可以保存信息

•注意避免过度拟合！

•仅当nan值在训练集测试集中的NaN值是由相同的值引起的，或者当局部验证证明它可以保留信息时才使用（这里涉及到缺失值的缺失原因，比如客户处于某种不好的目的而故意不提供的情况下表示客户的某种不良的潜在行为则可以统一使用）

![[assets/attachments/uncategorized/v2-9635ba3da70efbc6f1462d17134119fe_1440w.jpg]]

一个简单的例子。

![[assets/attachments/uncategorized/v2-01e039a2ecbbaa2e9fecf41ee2ee5703_1440w.jpg]]

多项式编码

•编码分类变量之间的交互

•没有交互作用的线性算法无法解决XOR问题

•多项式编码可以解决XOR

•扩展功能空间：使用FS，哈希和/或VW

其实就是做了类别交叉然后再使用其它的 [编码方式](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E7%BC%96%E7%A0%81%E6%96%B9%E5%BC%8F&zhida_source=entity) 来处理

![[assets/attachments/uncategorized/v2-621df0d4629492d69918907a0cb33962_1440w.jpg]]

一个简单的例子。

![[assets/attachments/uncategorized/v2-7dbd2931c18330a6069eb6bc2ff8300d_1440w.jpg]]

[扩展编码](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E6%89%A9%E5%B1%95%E7%BC%96%E7%A0%81&zhida_source=entity)

•从单个变量创建多个 [类别变量](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=2&q=%E7%B1%BB%E5%88%AB%E5%8F%98%E9%87%8F&zhida_source=entity)

•一些高基数功能（例如 [用户代理](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=2&q=%E7%94%A8%E6%88%B7%E4%BB%A3%E7%90%86&zhida_source=entity) ）在其中包含更多信息：

•is\_mobile？

•is\_latest\_version？

•Operation\_system

•Browser\_build

•等等。

kaggle的常见magic feature的产生方式，这里需要人工思考和头脑风暴的结果

![[assets/attachments/uncategorized/v2-1641d2e481b3b804775fb920417e7b19_1440w.jpg]]

一个简单的例子

![[assets/attachments/uncategorized/v2-207fe2ff7119b1a47f5f6cfd2a872b7e_1440w.jpg]]

[合并编码](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E5%90%88%E5%B9%B6%E7%BC%96%E7%A0%81&zhida_source=entity)

•将不同的分类变量映射到同一变量

•拼写错误，职位描述略有不同，全名或缩写

•真实数据混乱，自由文本尤其如此

其实就是 [数据预处理](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E6%95%B0%E6%8D%AE%E9%A2%84%E5%A4%84%E7%90%86&zhida_source=entity) 中把相同含义的类别统一用一个类别表示

![[assets/attachments/uncategorized/v2-e81ea82a39f9ba6d13fbcefd23f627af_1440w.jpg]]

一个简单的例子

---

前面都是关于类别特征的常见处理，下面是关于连续特征的。

![[assets/attachments/uncategorized/v2-959d1f1a913b650dd1877562eacb792c_1440w.jpg]]

[数值特征](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E6%95%B0%E5%80%BC%E7%89%B9%E5%BE%81&zhida_source=entity)

•可以更轻松地输入算法

•可以构成浮点数，计数，数字

•更容易做缺失值插补

![[assets/attachments/uncategorized/v2-2c58730516363f0512efb8a0875b9c79_1440w.jpg]]

四舍五入

•舍入 [数值变量](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E6%95%B0%E5%80%BC%E5%8F%98%E9%87%8F&zhida_source=entity)

•保留数据的最重要特征。

•有时精度太高只是噪音

•舍入变量可以视为分类变量

•可以在四舍五入之前应用对数转换

当然要确保不损失信息的情况下使用，比如kaggle ieee的欺诈比赛，不同精度的交易金额代表了不同国家。。。这就不能直接四舍五入了。

![[assets/attachments/uncategorized/v2-87d44052ab0b1e05db8e0b3199086e23_1440w.jpg]]

![[assets/attachments/uncategorized/v2-8f252d4031120bfbfff9ad1c8c674dd3_1440w.jpg]]

分箱

•将数值变量放入bin并使用bin-ID进行编码

•可以通过 [分位数](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E5%88%86%E4%BD%8D%E6%95%B0&zhida_source=entity) ，均匀地务实地设置 [分箱](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=2&q=%E5%88%86%E7%AE%B1&zhida_source=entity) ，或使用模型找到最佳分箱

•可以与超出训练集的范围的变量正常配合

![[assets/attachments/uncategorized/v2-a17eec54d249331f477bd14a05b3edcc_1440w.jpg]]

![[assets/attachments/uncategorized/v2-b0daa172407ff45ad5e9771f83224cc5_1440w.jpg]]

![[assets/attachments/uncategorized/v2-8a1fd1f05c1d08805632620f73ba6f0a_1440w.jpg]]

标准化

•将 [数字变量](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E6%95%B0%E5%AD%97%E5%8F%98%E9%87%8F&zhida_source=entity) 缩放到一定范围

•标准（Z）缩放 standard scaler

•MinMax 标准化

•root scaling（这是啥。。。）

•log 变换（ [log变换](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=log%E5%8F%98%E6%8D%A2&zhida_source=entity) 是box cox变换的特例）

![[assets/attachments/uncategorized/v2-ca7aeed7ac7fe8ba778b823982a212a7_1440w.jpg]]

缺失值插补

•估算缺失变量

•硬编码可以与插补结合使用

•平均值：非常基础

• [中位数](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E4%B8%AD%E4%BD%8D%E6%95%B0&zhida_source=entity) ：对异常值更健壮

•忽略：只是忽略问题

•使用模型：会引入算法偏差

（缺失值的处理是一门大学问，这里写的太简单）

![[assets/attachments/uncategorized/v2-e49b99b37a94a0efab430ebd15a05d9d_1440w.jpg]]

![[assets/attachments/uncategorized/v2-f2010ddec1cc1a2ed2bd3916496b3fff_1440w.jpg]]

连续特征的交互

•编码数值变量之间的相互作用

•尝试：减法，加法，乘法，除法（还有更骚的，指数。。。）

• **使用：通过 [统计测试](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E7%BB%9F%E8%AE%A1%E6%B5%8B%E8%AF%95&zhida_source=entity) 选择特征，或训练模型特征的重要性，用于特征的筛选（这种方法很容易得到噪声，所以 [噪声特征](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E5%99%AA%E5%A3%B0%E7%89%B9%E5%BE%81&zhida_source=entity) 也要注意筛选掉）**

•忽略：有时候违背直觉的计算反而可以显着改善模型的训练效果！

![[assets/attachments/uncategorized/v2-af67e51a7771b4bdb27920de75159ca1_1440w.jpg]]

线性算法的 [非线性编码](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E9%9D%9E%E7%BA%BF%E6%80%A7%E7%BC%96%E7%A0%81&zhida_source=entity)

•硬编码非线性以改善线性算法（hash、各类embedding等）

•多项式编码

•Leafcoding（随机森林嵌入）（acebook的gbdt+lr这种思路）

• [遗传算法](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E9%81%97%E4%BC%A0%E7%AE%97%E6%B3%95&zhida_source=entity) （典型代表gplearn）

•局部线性嵌入，频谱嵌入，t SNE （降维提取重要特征）

![[assets/attachments/uncategorized/v2-807c6a076409b6ecfc4105393b4e54e1_1440w.jpg]]

按照行计算统计值

•在一行数据上创建统计信息

•NaN的数量，这个在 [拍拍贷](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E6%8B%8D%E6%8B%8D%E8%B4%B7&zhida_source=entity) 的top解决方案上看到过，不过实际效果不稳定

•0的数量

•负值数量

•平均值，最大值，最小值，偏度等。

![[assets/attachments/uncategorized/v2-7285ca1f6e22d8d1a222111671405570_1440w.jpg]]

时间特征

•时间特征，例如日期，需要更好的局部验证方案（如回测）

•容易在这里犯错误

•能够给模型效果带来很多好的提升

![[assets/attachments/uncategorized/v2-ca1e5107d15718a13a8b434282da6bb7_1440w.jpg]]

[投射](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E6%8A%95%E5%B0%84&zhida_source=entity) 到一个圆圈

•将单个要素（例如day\_of\_week）转换为圆上的两个坐标

•确保最大和最小之间的距离与最小和最小+1相同。

•用于day\_of\_week，day\_of\_month，hour\_of\_day等。

![[assets/attachments/uncategorized/v2-668981c6234e71c921526e01df35c0ec_1440w.jpg]]

趋势编码，简单说就是根据 [时间序列](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E6%97%B6%E9%97%B4%E5%BA%8F%E5%88%97&zhida_source=entity) 来计算某段时间的一些统计值，比如对总支出进行编码，例如：在上周支出，在上个月支出，在去年支出。这个也是比较常见的方法。

![[assets/attachments/uncategorized/v2-d08f2641a7f573167d8fc18051bf722a_1440w.jpg]]

事件编码

•硬编码分类功能，例如：date\_3\_days\_before\_holidays：1

•尝试：国定假日，重大体育赛事，周末，每月的第一个星期六等。

•这些因素可能对消费行为产生重大影响。

![[assets/attachments/uncategorized/v2-cd9c8de6ff9f674890eadf6f038f63dd_1440w.jpg]]

空间编码

• [空间变量](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E7%A9%BA%E9%97%B4%E5%8F%98%E9%87%8F&zhida_source=entity) 是对空间中的位置进行编码的变量

•示例包括：GPS坐标，城市，国家/地区，地址

![[assets/attachments/uncategorized/v2-4574cbaf690937dbf1eda36fa2ab620a_1440w.jpg]]

• [克里格](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E5%85%8B%E9%87%8C%E6%A0%BC&zhida_source=entity) （这是啥。。。）

•K- [均值聚类](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E5%9D%87%E5%80%BC%E8%81%9A%E7%B1%BB&zhida_source=entity)

•原始纬度

•将城市转换为 [经度](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E7%BB%8F%E5%BA%A6&zhida_source=entity)

•在街道名称中添加 [邮政编码](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E9%82%AE%E6%94%BF%E7%BC%96%E7%A0%81&zhida_source=entity)

![[assets/attachments/uncategorized/v2-946a2a2b4873bebee7e7e8c6279ce885_1440w.jpg]]

位置编码

•查找当前位置与重要地点之间的距离

•小城镇继承了附近大城市的某些文化/背景

•电话位置可以映射到附近的企业和超市

![[assets/attachments/uncategorized/v2-ee038355501bf031a6d7ddf9af0703d0_1440w.jpg]]

位置所反应出来的欺诈行为

•位置事件数据可以指示可疑行为

•不可能的旅行速度：在不同国家/地区同时进行多项交易

•花费在与住所或送货地址不同的城镇

•从未在同一地点消费

---

接下来是关于数据探索的一些资料：

![[assets/attachments/uncategorized/v2-ab74a35f7ae5ae7602070514038222f3_1440w.jpg]]

数据探索

•数据探索可以发现数据质量问题，异常值，噪声，要素工程构想，要素清理构想。

•可以使用： [spyder](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=spyder&zhida_source=entity) ，jupyter notebook，pandas

•尝试简单的统计信息：最小值，最大值

•合并目标，以便找到信息之间的相关性。

![[assets/attachments/uncategorized/v2-7bd250fb28724510a6cf5d3af24d00c3_1440w.jpg]]

迭代/调试

•特征工程是一个迭代过程：使您的管道适合于快速迭代。

•使用 [亚线性](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E4%BA%9A%E7%BA%BF%E6%80%A7&zhida_source=entity) 调试：输出有关过程的中间信息，进行伪记录。

•使用允许快速实验的工具与方法

•失败的想法多于行之有效的想法

---

关于标签的一些处理方法：

![[assets/attachments/uncategorized/v2-5e90810e2a9a0982eb1c0e26520f7abe_1440w.jpg]]

•可以将标签/ [目标变量](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=2&q=%E7%9B%AE%E6%A0%87%E5%8F%98%E9%87%8F&zhida_source=entity) /因变量视为数据的特征，反之亦然。

• [对数转换](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=3&q=%E5%AF%B9%E6%95%B0%E8%BD%AC%E6%8D%A2&zhida_source=entity) ：y-> log（y + 1）| exp（y\_pred）-1

• [平方变换](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E5%B9%B3%E6%96%B9%E5%8F%98%E6%8D%A2&zhida_source=entity)

•Box-Cox变换

•创建一个分数，把二分类问题转化为回归问题。

•训练回归器预测测试集中不可用的特征。

---

关于 [自然语言处理](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E8%87%AA%E7%84%B6%E8%AF%AD%E8%A8%80%E5%A4%84%E7%90%86&zhida_source=entity) 的一些方案，当然，很多方法类别特征也是很合适的。

![[assets/attachments/uncategorized/v2-4863eb063f6ac99fffa17fdd266e1dcc_1440w.jpg]]

•可以使用来自分类功能的相同想法。

•深度学习（ [自动特征工程](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E8%87%AA%E5%8A%A8%E7%89%B9%E5%BE%81%E5%B7%A5%E7%A8%8B&zhida_source=entity) ）正在逐渐占领这一领域，但是具有精心设计的特征的浅层学习仍然具有竞争力。

•数据的稀疏性使您进入“ [维数](https://zhida.zhihu.com/search?content_id=107072087&content_type=Article&match_order=1&q=%E7%BB%B4%E6%95%B0&zhida_source=entity) 的诅咒”

•很多挖掘出好特征的机会：

![[assets/attachments/uncategorized/v2-35e5f01a153c260fe83904c0860e0a59_1440w.jpg]]

算了，不写了，nlp没怎么涉及，用到再看吧。。。

---

篇末的一些好的资源：

Resources & Further Reading

• Kaggle forums & kernels: Far0n, KazAnova, Fchollet, Abhishek, Gilberto Titericz, Leustagos, Owen Zhang, Gert

Jacobusse …

• Introduction: [machinelearningmastery.com](https://link.zhihu.com/?target=http%3A//machinelearningmastery.com/discover-feature-engineering-how-to-engineer-features-and-how)

to-get-good-at-it/

• Books:

• Mastering Feature Engineering (Alice Zheng),

• Feature Extraction (Isabelle Guyon et al.)

• Blogs:

• [smerity.com/articles/20](https://link.zhihu.com/?target=https%3A//smerity.com/articles/2016/architectures_are_the_new_feature_engineering.html)

• [hunch.net/~jl/projects/](https://link.zhihu.com/?target=http%3A//hunch.net/~jl/projects/hash_reps/)

• [blogs.technet.microsoft.com](https://link.zhihu.com/?target=https%3A//blogs.technet.microsoft.com/machinelearning/2014/09/24/online-learning-and-sub-linear-debugging/)

• [blog.kaggle.com/2015/12](https://link.zhihu.com/?target=http%3A//blog.kaggle.com/2015/12/03/dato-winners-interview-1st-place-mad-professors/)

• [blog.kaggle.com/2016/08](https://link.zhihu.com/?target=http%3A//blog.kaggle.com/2016/08/24/avito-duplicate-ads-detection-winners-interview-1st-place-team-devil-team)

stanislav-dmitrii/

• [slideshare.net/DataRobo](https://link.zhihu.com/?target=http%3A//www.slideshare.net/DataRobot/featurizing-log-data-before-xgboost)

• Data: [data.quora.com/First-Qu](https://link.zhihu.com/?target=https%3A//data.quora.com/First-Quora-Dataset-Release-Question-Pairs)

• Software: [github.com/trevorstephe](https://link.zhihu.com/?target=https%3A//github.com/trevorstephens/gplearn)

---

重要的还是多实战，

## 多总结

**就像打策略游戏一样（比如魔兽争霸3），基本功要扎实，在实战中形成自己的一套处理问题的风格，不要抄kernel，不要窃取别人的特征，自己多思考和总结。**

发布于 2019-10-05 14:20[特征工程](https://www.zhihu.com/topic/20058170)[Kaggle](https://www.zhihu.com/topic/20003862)[机器学习](https://www.zhihu.com/topic/19559450)