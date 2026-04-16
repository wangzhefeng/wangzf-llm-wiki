---
author:
- null
- '[[Ckend]]'
created: 2026-04-06
created_at: 2026-04-06
description: 鼎鼎大名的 Bert 算法相信大部分同学都听说过，它是 Google 推出的 NLP 领域“王炸级”预训练模
source_type: web
status: inbox
tags:
- null
- clippings
title: Python 教你 3 分钟用 Bert 搭建问答搜索引擎
source_url: https://mp.weixin.qq.com/s/IhUhAOD8HmCXxhg7CpFhUw
published_at: null
related_concepts: []
topics:
  - llm-pre-training
  - 大语言模型预训练
---

*2024年5月23日 13:54*

![[Image.gif|图片]]

鼎鼎大名的 Bert 算法相信大部分同学都听说过，它是 Google 推出的 NLP 领域“王炸级”预训练模型，其在 NLP 任务中刷新了多项记录，并取得 state of the art 的成绩。

但是有很多深度学习的新手发现 BERT 模型并不好搭建，上手难度很高，普通人可能要研究几天才能勉强搭建出一个模型。

没关系，今天我们介绍的这个模块，能让你在 3 分钟内基于 BERT 算法搭建一个问答搜索引擎。它就是 **bert-as-service** 项目。这个开源项目，能够让你基于多 GPU 机器快速搭建 BERT 服务（支持微调模型），并且能够让多个客户端并发使用。

*****1.准备*****

**请选择以下任一种方式输入命令安装依赖** ：  
1\. Windows 环境 打开 Cmd (开始-运行-CMD)。  
2\. MacOS 环境 打开 Terminal (command+空格输入Terminal)。  
3\. 如果你用的是 VSCode编辑器 或 Pycharm，可以直接使用界面下方的Terminal.

```
pip install bert-serving-server # 服务端
pip install bert-serving-client # 客户端
```

请注意，服务端的版本要求：Python >= 3.5，Tensorflow >= 1.10 。

此外还要下载预训练好的BERT模型，在 https://github.com/hanxiao/bert-as-service#install 上可以下载，如果你无法访问该网站，也可以在 https://pythondict.com/download/bert-serving-model/ 此处下载。

也可在公众号后台回复 bert-as-service 下载这些预训练好的模型。

下载完成后，将 zip 文件解压到某个文件夹中，例如 `/tmp/uncased_L-24_H-1024_A-16/`.

***2.Bert-as-service 基本使用***

安装完成后，输入以下命令启动 BERT 服务：  

```
bert-serving-start -model_dir /tmp/uncased_L-24_H-1024_A-16/ -num_worker=4
```

\-num\_worker=4 代表这将启动一个有四个 worker 的服务，意味着它最多可以处理四个 **并发** 请求。超过 4 个其他并发请求将在负载均衡器中排队等待处理。

下面显示了正确启动时服务器的样子：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

#### 使用客户端获取语句的编码

现在你可以简单地对句子进行编码，如下所示：

```
from bert_serving.client import BertClient
bc = BertClient()
bc.encode(['First do it', 'then do it right', 'then do it better'])
```

作为 BERT 的一个特性，你可以通过将它们与 `|||` （前后有空格）连接来获得一对句子的编码，例如

```
bc.encode(['First do it ||| then do it right'])
```

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**远程使用 BERT 服务**

你还可以在一台 (GPU) 机器上启动服务并从另一台 (CPU) 机器上调用它，如下所示：

```
# on another CPU machine
from bert_serving.client import BertClient
bc = BertClient(ip='xx.xx.xx.xx') # ip address of the GPU machine
bc.encode(['First do it', 'then do it right', 'then do it better'])
```

***3.搭建问答搜索引擎***

我们将通过 bert-as-service 从 FAQ 列表中找到与用户输入的问题最相似的问题，并返回相应的答案。

FAQ 列表其实就是官方文档的 readme.md, 在我提供的下载链接里也附带了。

1\. 加载所有问题，并显示统计数据：

```
prefix_q = '##### **Q:** '
with open('README.md') as fp:
    questions = [v.replace(prefix_q, '').strip() for v in fp if v.strip() and v.startswith(prefix_q)]
    print('%d questions loaded, avg. len of %d' % (len(questions), np.mean([len(d.split()) for d in questions])))
    # 33 questions loaded, avg. len of 9
```

一共有 33 个问题被加载，平均长度是 9.

2\. 然后使用预训练好的模型： **uncased\_L-12\_H-768\_A-12** 启动一个 Bert 服务：

```
bert-serving-start -num_worker=1 -model_dir=/data/cips/data/lab/data/model/uncased_L-12_H-768_A-12
```

3\. 接下来，将我们的问题编码为向量：

```
bc = BertClient(port=4000, port_out=4001)
doc_vecs = bc.encode(questions)
```

4\. 最后，我们准备好接收用户的查询，并对现有问题执行简单的“模糊”搜索。

为此，每次有新查询到来时，我们将其编码为向量并计算其点积 **`doc_vecs`** 然后对结果进行降序排序，返回前 N 个类似的问题：

```
while True:
    query = input('your question: ')
    query_vec = bc.encode([query])[0]
    # compute normalized dot product as score
    score = np.sum(query_vec * doc_vecs, axis=1) / np.linalg.norm(doc_vecs, axis=1)
    topk_idx = np.argsort(score)[::-1][:topk]
    for idx in topk_idx:
        print('> %s\t%s' % (score[idx], questions[idx]))
```

**完成！** 现在运行代码并输入你的查询，看看这个搜索引擎如何处理模糊匹配：

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

完整代码如下，一共 23 行代码：

**上滑查看完整代码**

```
import numpy as np
from bert_serving.client import BertClient
from termcolor import colored

prefix_q = '##### **Q:** '
topk = 5

with open('README.md') as fp:
    questions = [v.replace(prefix_q, '').strip() for v in fp if v.strip() and v.startswith(prefix_q)]
    print('%d questions loaded, avg. len of %d' % (len(questions), np.mean([len(d.split()) for d in questions])))

with BertClient(port=4000, port_out=4001) as bc:
    doc_vecs = bc.encode(questions)

    while True:
        query = input(colored('your question: ', 'green'))
        query_vec = bc.encode([query])[0]
        # compute normalized dot product as score
        score = np.sum(query_vec * doc_vecs, axis=1) / np.linalg.norm(doc_vecs, axis=1)
        topk_idx = np.argsort(score)[::-1][:topk]
        print('top %d questions similar to "%s"' % (topk, colored(query, 'green')))
        for idx in topk_idx:
            print('> %s\t%s' % (colored('%.1f' % score[idx], 'cyan'), colored(questions[idx], 'yellow')))
```

  
够简单吧？当然，这是一个基于预训练的 Bert 模型制造的一个简单 QA 搜索模型。

你还可以微调模型，让这个模型整体表现地更完美，你可以将自己的数据放到某个目录下，然后执行 run\_classifier.py 对模型进行微调，比如这个例子：

https://github.com/google-research/bert#sentence-and-sentence-pair-classification-tasks

它还有许多别的用法，我们这里就不一一介绍了，大家可以前往官方文档学习：

https://github.com/hanxiao/bert-as-service

End

**「进击的Coder」** 专属学习群已正式成立，搜索 **「CQCcqc4」** 添加崔庆才的个人微信或者扫描下方二维码拉您入群交流学习。  

![图片](data:image/svg+xml,%3C%3Fxml version='1.0' encoding='UTF-8'%3F%3E%3Csvg width='1px' height='1px' viewBox='0 0 1 1' version='1.1' xmlns='http://www.w3.org/2000/svg' xmlns:xlink='http://www.w3.org/1999/xlink'%3E%3Ctitle%3E%3C/title%3E%3Cg stroke='none' stroke-width='1' fill='none' fill-rule='evenodd' fill-opacity='0'%3E%3Cg transform='translate(-249.000000, -126.000000)' fill='%23FFFFFF'%3E%3Crect x='249' y='126' width='1' height='1'%3E%3C/rect%3E%3C/g%3E%3C/g%3E%3C/svg%3E)

**看完记得关注@进击的Coder**  

**及时收看更多好文**  

**↓↓↓**

阅读原文

继续滑动看下一个

进击的Coder

向上滑动看下一个