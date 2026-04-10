---
source_type: web
title: "基于Transform的机器翻译系统"
author:
  - 
  - "[[Dong]]"
created_at: 2026-04-06
topics:
  - 待分类
status: inbox
source: "https://zhuanlan.zhihu.com/p/144825330"
published: 
created: 2026-04-06
description: "大纲一. 建立Transformer模型的直观认识二. 编码器部分（Encoder）0. 先准备好输入的数据1. positional encoding（即位置嵌入或位置编码）2. self attention（自注意力机制）3. Attention Mask4. Layer Normalizat…"
tags:
  - 
  - "clippings"
---

## 大纲

- [一. 建立Transformer模型的直观认识](https://link.zhihu.com/?target=http%3A//localhost%3A8888/notebooks/transformer_nmt_student.ipynb%23%25E4%25B8%2580.-%25E5%25BB%25BA%25E7%25AB%258BTransformer%25E6%25A8%25A1%25E5%259E%258B%25E7%259A%2584%25E7%259B%25B4%25E8%25A7%2582%25E8%25AE%25A4%25E8%25AF%2586)
- [二. 编码器部分（Encoder）](https://link.zhihu.com/?target=http%3A//localhost%3A8888/notebooks/transformer_nmt_student.ipynb%23%25E4%25BA%258C.-%25E7%25BC%2596%25E7%25A0%2581%25E5%2599%25A8%25E9%2583%25A8%25E5%2588%2586%25EF%25BC%2588Encoder%25EF%25BC%2589)
- [0\. 先准备好输入的数据](https://link.zhihu.com/?target=http%3A//localhost%3A8888/notebooks/transformer_nmt_student.ipynb%230.-%25E5%2585%2588%25E5%2587%2586%25E5%25A4%2587%25E5%25A5%25BD%25E8%25BE%2593%25E5%2585%25A5%25E7%259A%2584%25E6%2595%25B0%25E6%258D%25AE)
	- [1\. positional encoding（即位置嵌入或位置编码）](https://link.zhihu.com/?target=http%3A//localhost%3A8888/notebooks/transformer_nmt_student.ipynb%231.-positional-encoding%25EF%25BC%2588%25E5%258D%25B3%25E4%25BD%258D%25E7%25BD%25AE%25E5%25B5%258C%25E5%2585%25A5%25E6%2588%2596%25E4%25BD%258D%25E7%25BD%25AE%25E7%25BC%2596%25E7%25A0%2581%25EF%25BC%2589)
	- [2\. self attention（自注意力机制）](https://link.zhihu.com/?target=http%3A//localhost%3A8888/notebooks/transformer_nmt_student.ipynb%232.-self-attention%25EF%25BC%2588%25E8%2587%25AA%25E6%25B3%25A8%25E6%2584%258F%25E5%258A%259B%25E6%259C%25BA%25E5%2588%25B6%25EF%25BC%2589)
	- [3\. Attention Mask](https://link.zhihu.com/?target=http%3A//localhost%3A8888/notebooks/transformer_nmt_student.ipynb%233.-Attention-Mask)
	- [4\. Layer Normalization 和残差连接](https://link.zhihu.com/?target=http%3A//localhost%3A8888/notebooks/transformer_nmt_student.ipynb%234.-Layer-Normalization-%25E5%2592%258C%25E6%25AE%258B%25E5%25B7%25AE%25E8%25BF%259E%25E6%258E%25A5)
	- [5\. Transformer Encoder 整体结构](https://link.zhihu.com/?target=http%3A//localhost%3A8888/notebooks/transformer_nmt_student.ipynb%235.-Transformer-Encoder-%25E6%2595%25B4%25E4%25BD%2593%25E7%25BB%2593%25E6%259E%2584)
- [三. 解码器部分（Decoder）](https://link.zhihu.com/?target=http%3A//localhost%3A8888/notebooks/transformer_nmt_student.ipynb%23%25E4%25B8%2589.-%25E8%25A7%25A3%25E7%25A0%2581%25E5%2599%25A8%25E9%2583%25A8%25E5%2588%2586%25EF%25BC%2588Decoder%25EF%25BC%2589)
- [四. Transformer模型](https://link.zhihu.com/?target=http%3A//localhost%3A8888/notebooks/transformer_nmt_student.ipynb%23%25E5%259B%259B.-Transformer%25E6%25A8%25A1%25E5%259E%258B)
- [五. 模型训练](https://link.zhihu.com/?target=http%3A//localhost%3A8888/notebooks/transformer_nmt_student.ipynb%23%25E4%25BA%2594.-%25E6%25A8%25A1%25E5%259E%258B%25E8%25AE%25AD%25E7%25BB%2583)
- [六. 模型预测](https://link.zhihu.com/?target=http%3A//localhost%3A8888/notebooks/transformer_nmt_student.ipynb%23%25E5%2585%25AD.-%25E6%25A8%25A1%25E5%259E%258B%25E9%25A2%2584%25E6%25B5%258B)

## 一. 建立Transformer模型的直观认识

首先来说一下 **Transformer** 和 **[LSTM](https://zhida.zhihu.com/search?content_id=120315155&content_type=Article&match_order=1&q=LSTM&zhida_source=entity)** 的最大区别，就是LSTM的训练是迭代（自回归）的，是一个接一个字的来，当前这个字过完LSTM单元，才可以进下一个字，而 Transformer 的训练是并行了，就是所有字是全部同时训练的，这样就大大加快了计算效率，Transformer 使用了位置嵌入positional encoding来理解语言的顺序，使用自注意力机制和全连接层来进行计算，这些后面都会详细讲解。

Transformer 模型主要分为两大部分，分别是编码器Encoder和解码器Decoder：

\- 编码器（Encoder）负责把自然语言序列映射成为隐藏层(下图中第2步用九宫格比喻的部分)，含有自然语言序列的数学表达

\- 解码器（Decoder）\*\*再把隐藏层映射为自然语言序列，从而使我们可以解决各种问题，如情感分类、命名实体识别、语义关系抽取、摘要生成、机器翻译等等。

## 二. 编码器部分（Encoder）

我们会重点介绍编码器的结构，因为理解了编码器中的结构, 理解解码器就非常简单了。而且我们用编码器就能够完成一些自然语言处理中比较主流的任务, 如情感分类, 语义关系分析, 命名实体识别等。

编码器（Encoder）部分, 即把自然语言序列映射为隐藏层的数学表达的过程。

**以下为一个Transformer Encoder Block结构示意图**

![[assets/attachments/uncategorized/v2-f7fe1892bbef2f1b6c4d1a605fce7456_1440w.jpg]]

注意: 为方便查看, 下面各部分的内容分别对应着图中第1, 2, 3, 4个方框的序号：

**0\. 先准备好输入的数据**

```python
import os
import math
import copy
import time
import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

from nltk import word_tokenize
from collections import Counter
from torch.autograd import Variable

# 初始化参数设置
UNK = 0  # 未登录词的标识符对应的词典id
PAD = 1  # padding占位符对应的词典id
BATCH_SIZE = 64  # 每批次训练数据数量
EPOCHS = 20  # 训练轮数
LAYERS = 6  # transformer中堆叠的encoder和decoder block层数
H_NUM = 8  # multihead attention hidden个数
D_MODEL = 256  # embedding维数
D_FF = 1024  # feed forward第一个全连接层维数
DROPOUT = 0.1  # dropout比例
MAX_LENGTH = 60  # 最大句子长度

TRAIN_FILE = 'nmt/en-cn/train.txt'  # 训练集数据文件
DEV_FILE = "nmt/en-cn/dev.txt"  # 验证(开发)集数据文件
SAVE_FILE = 'save/model.pt'  # 模型保存路径(注意如当前目录无save文件夹需要自己创建)
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def seq_padding(X, padding=0):
    """
    对一个batch批次(以单词id表示)的数据进行padding填充对齐长度
    """
    # 计算该批次数据各条数据句子长度
    L = [len(x) for x in X]
    # 获取该批次数据最大句子长度
    ML = max(L)
    # 对X中各条数据x进行遍历，如果长度短于该批次数据最大长度ML，则以padding id填充缺失长度ML-len(x)
    return np.array([
        np.concatenate([x, [padding] * (ML - len(x))]) if len(x) < ML else x for x in X
    ])

class PrepareData:
    def __init__(self, train_file, dev_file):
        # 读取数据 并分词
        self.train_en, self.train_cn = self.load_data(train_file)
        self.dev_en, self.dev_cn = self.load_data(dev_file)

        # 构建单词表
        self.en_word_dict, self.en_total_words, self.en_index_dict = self.build_dict(self.train_en)
        self.cn_word_dict, self.cn_total_words, self.cn_index_dict = self.build_dict(self.train_cn)

        # id化
        self.train_en, self.train_cn = self.wordToID(self.train_en, self.train_cn, self.en_word_dict, self.cn_word_dict)
        self.dev_en, self.dev_cn = self.wordToID(self.dev_en, self.dev_cn, self.en_word_dict, self.cn_word_dict)

        # 划分batch + padding + mask
        self.train_data = self.splitBatch(self.train_en, self.train_cn, BATCH_SIZE)
        self.dev_data = self.splitBatch(self.dev_en, self.dev_cn, BATCH_SIZE)

    def load_data(self, path):
        """
        读取翻译前(英文)和翻译后(中文)的数据文件
        每条数据都进行分词，然后构建成包含起始符(BOS)和终止符(EOS)的单词(中文为字符)列表
        形式如：en = [['BOS', 'i', 'love', 'you', 'EOS'], ['BOS', 'me', 'too', 'EOS'], ...]
                cn = [['BOS', '我', '爱', '你', 'EOS'], ['BOS', '我', '也', '是', 'EOS'], ...]
        """
        en = []
        cn = []
        # TODO ...
        with open(path, 'r', encoding='utf-8') as fin:
            for line in fin:
                list_content = line.split('\t')
                # print(list_content)
                en.append(['BOS'] + word_tokenize(list_content[0]) + ['EOS'])
                cn.append(['BOS'] + word_tokenize(" ".join(list_content[1])) + ['EOS'])

        return en, cn
    
    def build_dict(self, sentences, max_words = 50000):
        """
        传入load_data构造的分词后的列表数据
        构建词典(key为单词，value为id值)
        """
        # 对数据中所有单词进行计数
        word_count = Counter()

        for sentence in sentences:
            for s in sentence:
                word_count[s] += 1
        # 只保留最高频的前max_words数的单词构建词典
        # 并添加上UNK和PAD两个单词，对应id已经初始化设置过
        ls = word_count.most_common(max_words)
        # 统计词典的总词数
        total_words = len(ls) + 2

        word_dict = {w[0]: index + 2 for index, w in enumerate(ls)}
        word_dict['UNK'] = UNK
        word_dict['PAD'] = PAD
        # 再构建一个反向的词典，供id转单词使用
        index_dict = {v: k for k, v in word_dict.items()}

        return word_dict, total_words, index_dict

    def wordToID(self, en, cn, en_dict, cn_dict, sort=True):
        """
        该方法可以将翻译前(英文)数据和翻译后(中文)数据的单词列表表示的数据
        均转为id列表表示的数据
        如果sort参数设置为True，则会以翻译前(英文)的句子(单词数)长度排序
        以便后续分batch做padding时，同批次各句子需要padding的长度相近减少padding量
        """
        # 计算英文数据条数
        length = len(en)
        
        # TODO: 将翻译前(英文)数据和翻译后(中文)数据都转换为id表示的形式
        out_en_ids = [[en_dict.get(w, 0) for w in sent] for sent in en]
        out_cn_ids = [[cn_dict.get(w, 0) for w in sent] for sent in cn]

        # 构建一个按照句子长度排序的函数
        def len_argsort(seq):
            """
            传入一系列句子数据(分好词的列表形式)，
            按照句子长度排序后，返回排序后原来各句子在数据中的索引下标
            """
            return sorted(range(len(seq)), key=lambda x: len(seq[x]))

        # 把中文和英文按照同样的顺序排序
        if sort:
            # 以英文句子长度排序的(句子下标)顺序为基准
            sorted_index = len_argsort(out_en_ids)
            
            # TODO: 对翻译前(英文)数据和翻译后(中文)数据都按此基准进行排序
            out_en_ids = [out_en_ids[i] for i in sorted_index]
            out_cn_ids = [out_cn_ids[i] for i in sorted_index]
            
        return out_en_ids, out_cn_ids

    def splitBatch(self, en, cn, batch_size, shuffle=True):
        """
        将以单词id列表表示的翻译前(英文)数据和翻译后(中文)数据
        按照指定的batch_size进行划分
        如果shuffle参数为True，则会对这些batch数据顺序进行随机打乱
        """
        # 在按数据长度生成的各条数据下标列表[0, 1, ..., len(en)-1]中
        # 每隔指定长度(batch_size)取一个下标作为后续生成batch的起始下标
        idx_list = np.arange(0, len(en), batch_size)
        # 如果shuffle参数为True，则将这些各batch起始下标打乱
        if shuffle:
            np.random.shuffle(idx_list)
        # 存放各个batch批次的句子数据索引下标
        batch_indexs = []
        for idx in idx_list:
            # 注意，起始下标最大的那个batch可能会超出数据大小
            # 因此要限定其终止下标不能超过数据大小

            batch_indexs.append(np.arange(idx, min(idx + batch_size, len(en))))
        
        # 按各batch批次的句子数据索引下标，构建实际的单词id列表表示的各batch句子数据
        batches = []
        for batch_index in batch_indexs:
            # 按当前batch的各句子下标(数组批量索引)提取对应的单词id列表句子表示数据
            batch_en = [en[index] for index in batch_index]  
            batch_cn = [cn[index] for index in batch_index]
            # 对当前batch的各个句子都进行padding对齐长度
            # 维度为：batch数量×batch_size×每个batch最大句子长度
            batch_cn = seq_padding(batch_cn)
            batch_en = seq_padding(batch_en)
            # 将当前batch的英文和中文数据添加到存放所有batch数据的列表中
            batches.append(Batch(batch_en, batch_cn))

        return batches
```

注意，上述预处理中使用的 BatchBatch 类在后面的 EncoderEncoder 内容的 Attention MaskAttention Mask 部分定义

**Embedding**

与其他序列传导模型类似，我们使用learned embeddings将输入标记和输出标记转换为维度 的向量。我们还使用通常学习的线性变换和softmax函数将 Decoder（解码器）的输出转换为预测的下一个标签的概率。

在我们的模型中，我们在两个embedding层和pre-softmax线性变换层之间共享相同的权重矩阵。在其中的embedding层，我们会将这些权重乘以 。

```python
class Embeddings(nn.Module):
    def __init__(self, d_model, vocab):
        super(Embeddings, self).__init__()
        # Embedding层
        self.lut = nn.Embedding(vocab, d_model)
        # Embedding维数
        self.d_model = d_model

    def forward(self, x):
        # 返回x对应的embedding矩阵（需要乘以math.sqrt(d_model)）
        return self.lut(x) * math.sqrt(self.d_model)
```

数据全部处理完成，现在我们开始理解和构建 Transformer 模型

**1\. positional encoding（即位置嵌入或位置编码）**

由于 Transformer 模型没有循环神经网络的迭代操作，所以我们必须提供每个字的位置信息给 Transformer，才能识别出语言中的顺序关系。

因此，我们定义一个位置嵌入的概念，也就是positional encoding，位置嵌入的维度为\[max sequence length，embedding dimension\]，嵌入的维度同词向量的维度，max sequence length属于超参数，指的是限定的最大单个句长。

注意，我们一般以字为单位训练transformer模型，也就是说我们不用分词了，首先我们要初始化字向量为\[vocabsize，embedding dimension\], vocab size为总共的字库数量，embedding dimension为字向量的维度，也是每个字的数学表达。

在论文 **attention is all you need** （ [arxiv.org/pdf/1706.0376](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/1706.03762.pdf) ）中使用了sine和cosine函数的线性变换来提供给模型位置信息：

上式中pos指的是句中字的位置，取值范围是\[0,maxsequencelength)，i指的是词向量的维度，取值范围是\[0,embeddingdimension)，上面有sin和cos一组公式，也就是对应着embeddingdimension维度的一组奇数和偶数的序号的维度，例如0,1一组，2,3一组，分别用上面的sin和cos函数做处理，从而产生不同的周期性变化，而位置嵌入在embeddingdimension维度上随着维度序号增大，周期变化会越来越慢，而产生一种包含位置信息的纹理，就像论文原文中第六页讲的，位置嵌入函数的周期从2π到10000∗2π变化，而每一个位置在embedding dimension维度上都会得到不同周期的sin和cos函数的取值组合，从而产生独一的纹理位置信息，模型从而学到位置之间的依赖关系和自然语言的时序特性。

```python
# 导入依赖库
import matplotlib.pyplot as plt
import seaborn as sns

class PositionalEncoding(nn.Module):
    def __init__(self, d_model, dropout, max_len=5000):
        super(PositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(p=dropout)
        
        # 初始化一个size为 max_len(设定的最大长度)×embedding维度 的全零矩阵
        # 来存放所有小于这个长度位置对应的porisional embedding
        pe = torch.zeros(max_len, d_model, device=DEVICE)
        # 生成一个位置下标的tensor矩阵(每一行都是一个位置下标)
        """
        形式如：
        tensor([[0.],
                [1.],
                [2.],
                [3.],
                [4.],
                ...])
        """
        position = torch.arange(0., max_len, device=DEVICE).unsqueeze(1)
        # 这里幂运算太多，我们使用exp和log来转换实现公式中pos下面要除以的分母（由于是分母，要注意带负号）
        div_term = torch.exp(torch.arange(0., d_model, 2, device=DEVICE) * -(math.log(10000.0) / d_model))
        
        # TODO: 根据公式，计算各个位置在各embedding维度上的位置纹理值，存放到pe矩阵中
        pe[:, 0::2] =  torch.sin(position * div_term)
        pe[:, 1::2] =  torch.cos(position * div_term)
        
        # 加1个维度，使得pe维度变为：1×max_len×embedding维度
        # (方便后续与一个batch的句子所有词的embedding批量相加)
        pe = pe.unsqueeze(0) 
        # 将pe矩阵以持久的buffer状态存下(不会作为要训练的参数)
        self.register_buffer('pe', pe)

    def forward(self, x):
        # 将一个batch的句子所有词的embedding与已构建好的positional embeding相加
        # (这里按照该批次数据的最大句子长度来取对应需要的那些positional embedding值)
        x = x + Variable(self.pe[:, :x.size(1)], requires_grad=False)
        return self.dropout(x)
```

可见，这里首先是按照最大长度max\_len生成一个位置，而后根据公式计算出所有的向量，在forward函数中根据长度取用即可，非常方便。注意要设置requires\_grad=False，因其不参与训练。

**2\. self attention（自注意力机制）**

![[assets/attachments/uncategorized/v2-d6ef7986e3e8d903c927763869b92bf9_1440w.jpg]]

![[assets/attachments/uncategorized/v2-527bf28c7ad117710939334aa7d03fc3_1440w.jpg]]

**除以 的解释**

假设 q 和 k 是独立的随机变量，平均值为 0，方差 1，这样他们的点积后形成的注意力矩阵为 ，均值为 0 但方差放大为 。为了抵消这种影响，我们用 来缩放点积，可以使得Softmax归一化时结果更稳定（不至于点积后得到注意力矩阵的值差别太大），以便反向传播时获取平衡的梯度

```python
def attention(query, key, value, mask=None, dropout=None):
    # 将query矩阵的最后一个维度值作为d_k
    d_k = query.size(-1)
    
    # TODO: 将key的最后两个维度互换(转置)，才能与query矩阵相乘，乘完了还要除以d_k开根号
    scores = torch.matmul(query, key.transpose(-2, -1)) / math.sqrt(d_k)
    
    # 如果存在要进行mask的内容，则将那些为0的部分替换成一个很大的负数
    if mask is not None:
        scores = scores.masked_fill(mask == 0, -1e9)
        
    # TODO: 将mask后的attention矩阵按照最后一个维度进行softmax
    p_attn = F.softmax(scores, dim = -1)
    
    # 如果dropout参数设置为非空，则进行dropout操作
    if dropout is not None:
        p_attn = dropout(p_attn)
    # 最后返回注意力矩阵跟value的乘积，以及注意力矩阵
    return torch.matmul(p_attn, value), p_attn

class MultiHeadedAttention(nn.Module):
    def __init__(self, h, d_model, dropout=0.1):
        super(MultiHeadedAttention, self).__init__()
        # 保证可以整除
        assert d_model % h == 0
        # 得到一个head的attention表示维度
        self.d_k = d_model // h
        # head数量
        self.h = h
        # 定义4个全连接函数，供后续作为WQ，WK，WV矩阵和最后h个多头注意力矩阵concat之后进行变换的矩阵
        self.linears = clones(nn.Linear(d_model, d_model), 4)
        self.attn = None
        self.dropout = nn.Dropout(p=dropout)

    def forward(self, query, key, value, mask=None):
        if mask is not None:
            mask = mask.unsqueeze(1)
        # query的第一个维度值为batch size
        nbatches = query.size(0)
        # 将embedding层乘以WQ，WK，WV矩阵(均为全连接)
        # 并将结果拆成h块，然后将第二个和第三个维度值互换(具体过程见上述解析)
        query, key, value = [l(x).view(nbatches, -1, self.h, self.d_k).transpose(1, 2) 
                             for l, x in zip(self.linears, (query, key, value))]
        # 调用上述定义的attention函数计算得到h个注意力矩阵跟value的乘积，以及注意力矩阵
        x, self.attn = attention(query, key, value, mask=mask, dropout=self.dropout)
        # 将h个多头注意力矩阵concat起来（注意要先把h变回到第三维的位置）
        x = x.transpose(1, 2).contiguous().view(nbatches, -1, self.h * self.d_k)
        # 使用self.linears中构造的最后一个全连接函数来存放变换后的矩阵进行返回
        return self.linears[-1](x)
```

参数里面的 h 和 dmodel 分别表示注意力头的个数，以及模型的隐层单元数。

另外在 \_init\_\_ 函数中，我们定义了 self.linears=clones(nn.Linear(dmodel,dmodel),4),clone(x,N) 即为深拷贝N份，这里定义了4个全连接函数，实际上是3+1，其中的3个分别是Q、K和V的变换矩阵，最后一个是用于最后将 h 个多头注意力矩阵concat之后进行变换的矩阵。

在 forward 函数中，是首先将 query、key 和 value 进行相应的变换，然后需要经过 attention 这个函数的计算，这个函数实际上就是论文中“Scaled Dot-Product Attention”这个模块的计算

**3\. Attention Mask**

![[assets/attachments/uncategorized/v2-ee0a2281275c1bf9ce16f0f310392f0f_1440w.jpg]]

注意, 在上面self attention的计算过程中, 我们通常使用mini batch来计算, 也就是一次计算多句话, 也就是X的维度是\[batch size, sequence length\], sequence length是句长, 而一个mini batch是由多个不等长的句子组成的, 我们就需要按照这个mini batch中最大的句长对剩余的句子进行补齐长度, 我们一般用00来进行填充, 这个过程叫做padding.

但这时在进行softmax的时候就会产生问题, 回顾softmax函数 , 是1, 是有值的, padding的部分就参与了运算, 就等于是让无效的部分参与了运算, 会产生很大隐患, 这时就需要做一个mask让这些无效区域不参与运算, 我们一般给无效区域加一个很大的负数的偏置, 也就是:

经过上式的masking我们使无效区域经过softmax计算之后几乎为0, 这样就避免了无效区域参与计算.

在 Transformer 里面，Encoder 和 Decoder的 Attention 计算都需要相应的 Mask 处理，但功能却不同。

在 Encoder 中，就如上述介绍的，Mask 就是为了让那些在一个 batch 中长度较短的序列的 padding 部分不参与 Attention 的计算。因此我们定义一个 Batch 批处理对象，src（翻译前）和 trg（翻译后）句子，以及构造其中的 Mask 掩码。

**加了 Mask 的 Attention 原理如图（另附 Multi-HeadAttention ）：**

注意：这里的AttentionMask 是加在 Scale 和 Softmax 之间

![[assets/attachments/uncategorized/v2-dec95c5f3605c47ed1990e0ba6e5faca_1440w.jpg]]

```python
class Batch:
    "Object for holding a batch of data with mask during training."
    def __init__(self, src, trg=None, pad=0):
        # 将输入与输出的单词id表示的数据规范成整数类型
        src = torch.from_numpy(src).to(DEVICE).long()
        trg = torch.from_numpy(trg).to(DEVICE).long()
        self.src = src
        # 对于当前输入的句子非空部分进行判断成bool序列
        # 并在seq length前面增加一维，形成维度为 1×seq length 的矩阵
        self.src_mask = (src != pad).unsqueeze(-2)
        # 如果输出目标不为空，则需要对decoder要使用到的target句子进行mask
        if trg is not None:
            # decoder要用到的target输入部分
            self.trg = trg[:, :-1]
            # decoder训练时应预测输出的target结果
            self.trg_y = trg[:, 1:]
            # 将target输入部分进行attention mask
            self.trg_mask = self.make_std_mask(self.trg, pad)
            # 将应输出的target结果中实际的词数进行统计
            self.ntokens = (self.trg_y != pad).data.sum()
    
    # Mask掩码操作
    @staticmethod
    def make_std_mask(tgt, pad):
        "Create a mask to hide padding and future words."
        tgt_mask = (tgt != pad).unsqueeze(-2)
        tgt_mask = tgt_mask & Variable(subsequent_mask(tgt.size(-1)).type_as(tgt_mask.data))
        return tgt_mask
```

**4\. Layer Normalization 和残差连接**

1). LayerNorm:

LayerNormalization的作用是把神经网络中隐藏层归一为标准正态分布, 也就是 i.i.d（独立同分布）, 以起到加快训练速度, 加速收敛的作用:

上式中以矩阵的row为单位求均值

上式中以矩阵的行 row 为单位求方差

然后用每一行的每一个元素减去这行的均值, 再除以这行的标准差, 从而得到归一化后的数值, 是为了防止除0

之后引入两个可训练参数 , 来弥补归一化的过程中损失掉的信息, 注意 表示元素相乘而不是点积, 我们一般初始化 为全1, 而 为全0

2). 残差连接:

我们在上一步得到了经过注意力矩阵加权之后的V, 也就是Attention(Q,K,V), 我们对它进行一下转置, 使其和Xembedding的维度一致, 也就是\[batch size, sequence length, embedding dimension\],然后把他们加起来做残差连接, 直接进行元素相加, 因为他们的维度一致:

在之后的运算里, 每经过一个模块的运算, 都要把运算之前的值和运算之后的值相加, 从而得到残差连接, 训练的时候可以使梯度直接走捷径反传到最初始层

注意：这里我们对SubLayer(X)一般会进行dropout后再与X连接，即　X + Dropout(SubLayer(X))

```python
class LayerNorm(nn.Module):
    def __init__(self, features, eps=1e-6):
        super(LayerNorm, self).__init__()
        # 初始化α为全1, 而β为全0
        self.a_2 = nn.Parameter(torch.ones(features))
        self.b_2 = nn.Parameter(torch.zeros(features))
        # 平滑项
        self.eps = eps

    def forward(self, x):
        # TODO: 请利用init中的成员变量实现LayerNorm层的功能
        # 按最后一个维度计算均值和方差
        mean = x.mean(-1, keepdim = True)
        std = x.std(-1, keepdim = True)
        
        # TODO: 返回Layer Norm的结果
        return  self.a_2 * ( x - mean) / torch.sqrt(std ** 2 + self.eps) + self.b_2
```

以上是 LayerNormalization 的实现，其实PyTorch里面已经集成好了nn.LayerNorm，这里实现出来是为了学习其中的原理。而实际中，为了代码简洁，可以直接使用PyTorch里面实现好的函数。

```python
class SublayerConnection(nn.Module):
    """
    SublayerConnection的作用就是把Multi-Head Attention和Feed Forward层连在一起
    只不过每一层输出之后都要先做Layer Norm再残差连接
    sublayer是lamda函数
    """
    def __init__(self, size, dropout):
        super(SublayerConnection, self).__init__()
        self.norm = LayerNorm(size)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, sublayer):
        # TODO: 请利用init中的成员变量实现LayerNorm和残差连接的功能
        # 返回Layer Norm和残差连接后结果
        return x + self.dropout(sublayer(self.norm(x)))
```

**5\. Transformer Encoder 整体结构**

经过上面4个步骤, 我们已经基本了解到来transformer编码器的主要构成部分, 我们下面用公式把一个transformer block的计算过程整理一下:

1). 字向量与位置编码:

2). 自注意力机制:

  
3). 残差连接与Layer Normalization

4). FeedForward，其实就是两层线性映射并用激活函数（比如说ReLU）激活：

5). 重复3

```python
def clones(module, N):
    """
    克隆模型块，克隆的模型块参数不共享
    """
    return nn.ModuleList([copy.deepcopy(module) for _ in range(N)])
```

FeedForward（前馈网络）层其实就是两层线性映射并用激活函数激活

```python
class PositionwiseFeedForward(nn.Module):
    def __init__(self, d_model, d_ff, dropout=0.1):
        super(PositionwiseFeedForward, self).__init__()
        self.w_1 = nn.Linear(d_model, d_ff)
        self.w_2 = nn.Linear(d_ff, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x):
        # TODO: 请利用init中的成员变量实现Feed Forward层的功能
        return self.w_2(self.dropout(F.relu(self.w_1(x))))
```

Encoder 由 N=6 个相同的层组成。

```python
class Encoder(nn.Module):
    # layer = EncoderLayer
    # N = 6
    def __init__(self, layer, N):
        super(Encoder, self).__init__()
        # 复制N个encoder layer
        self.layers = clones(layer, N)
        # Layer Norm
        self.norm = LayerNorm(layer.size)

    def forward(self, x, mask):
        """
        使用循环连续eecode N次(这里为6次)
        这里的Eecoderlayer会接收一个对于输入的attention mask处理
        """
        for layer in self.layers:
            x = layer(x, mask)
        return self.norm(x)
```

每层 EncoderBlock 都有两个子层组成。第一个子层实现了“多头”的 elf-attention，第二个子层则是一个简单的 Position-wise 的全连接前馈网络。

```python
class EncoderLayer(nn.Module):
    def __init__(self, size, self_attn, feed_forward, dropout):
        super(EncoderLayer, self).__init__()
        self.self_attn = self_attn
        self.feed_forward = feed_forward
        # SublayerConnection的作用就是把multi和ffn连在一起
        # 只不过每一层输出之后都要先做Layer Norm再残差连接
        self.sublayer = clones(SublayerConnection(size, dropout), 2)
        # d_model
        self.size = size

    def forward(self, x, mask):
        # 将embedding层进行Multi head Attention
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, mask))
        # 注意到attn得到的结果x直接作为了下一层的输入
        return self.sublayer[1](x, self.feed_forward)
```

**三. 解码器部分（Decoder）**

![[assets/attachments/uncategorized/v2-e5a37aaafa4316ca04bbe8531034399d_1440w.jpg]]

接着来看 Decoder 部分（右半部分），它同样也是由 N 层（在论文中，仍取 N=6 ）堆叠起来。

对于其中的每一层，除了与 Encoder 中相同的 self-attention 及 FeedForward 两层之外，还在中间插入了一个传统的Encoder-Decoder 框架中的 context-attention 层（上图中的sub-layer2），即将 Decoder 的输出作为 query 去查询 Encoder 的输出，同样用的是 Multi-HeadAttention ，使得在Decode 的时候能看到 Encoder 的所有输出。

这里明确一下 Decoder **的输入输出和解码过程：**

- 输入：Encoder 的输出 & 对应 i−1 位置 Decoder 的输出。所以中间的 Attention 不是 Self-Attention ，它的 K，V 来自 Encoder ，Q来自上一位置 Decoder 的输出
- 输出：对应 i 位置的输出词的概率分布
- 解码：这里要特别注意一下，编码可以并行计算，一次性全部encoding出来，但解码不是一次把所有序列解出来的，而是像rnn一样一个一个解出来的，因为要用上一个位置的输入当作 Attention 的 query
```python
class Decoder(nn.Module):
    def __init__(self, layer, N):
        super(Decoder, self).__init__()
        # TODO: 参照EncoderLayer完成成员变量定义
        # 复制N个encoder layer
        self.layers = clones(layer, N)
        # Layer Norm
        self.norm = LayerNorm(layer.size)
        
    def forward(self, x, memory, src_mask, tgt_mask):
        """
        使用循环连续decode N次(这里为6次)
        这里的Decoderlayer会接收一个对于输入的attention mask处理
        和一个对输出的attention mask + subsequent mask处理
        """
        for layer in self.layers:
            x = layer(x, memory, src_mask, tgt_mask)
        return self.norm(x)

class DecoderLayer(nn.Module):
    def __init__(self, size, self_attn, src_attn, feed_forward, dropout):
        super(DecoderLayer, self).__init__()
        self.size = size
        # Self-Attention
        self.self_attn = self_attn
        # 与Encoder传入的Context进行Attention
        self.src_attn = src_attn
        self.feed_forward = feed_forward
        self.sublayer = clones(SublayerConnection(size, dropout), 3)

    def forward(self, x, memory, src_mask, tgt_mask):
        # 用m来存放encoder的最终hidden表示结果
        m = memory
        
        # TODO: 参照EncoderLayer完成DecoderLayer的forwark函数
        # Self-Attention：注意self-attention的q，k和v均为decoder hidden
        x = self.sublayer[0](x, lambda x: self.self_attn(x, x, x, tgt_mask))
        # Context-Attention：注意context-attention的q为decoder hidden，而k和v为encoder hidden
        x = self.sublayer[1](x, lambda x: self.src_attn(x, m, m, src_mask))
        return self.sublayer[2](x, self.feed_forward)
```

明确了解码过程之后最上面的图就很好懂了，这里主要的不同就是新加的另外要说一下新加的attention多加了一个subsequent\_mask ，因为训练时的output都是ground truth，这样可以确保预测第 i 个位置时不会接触到未来的信息，具体解释如下。  
对于 Encoder 中src 的 mask 方式就比较简单，直接把 pad 部分给 mask 掉即可。  
但对于 Decoder 中 trg 的 mask 计算略微复杂一些，不仅需要把 pad 部分 mask 掉，还需要进行一个 subsequent\_mask 的操作。  
即作为 decoder，在预测当前步的时候，是不能知道后面的内容的，即 attention 需要加上 mask，将当前步之后的分数全部置为−∞−∞，然后再计算 softmax，以防止发生数据泄露。这种 Masked 的 Attention 是考虑到输出 Embedding 会偏移一个位置，确保了生成位置 i 的预测时，仅依赖小于 i 的位置处的已知输出，相当于把后面不该看到的信息屏蔽掉。

```python
def subsequent_mask(size):
    "Mask out subsequent positions."
    # 设定subsequent_mask矩阵的shape
    attn_shape = (1, size, size)
    
    # TODO: 生成一个右上角(不含主对角线)为全1，左下角(含主对角线)为全0的subsequent_mask矩阵
    subsequent_mask = np.triu(np.ones(attn_shape), k=1).astype('uint8')
    
    # TODO: 返回一个右上角(不含主对角线)为全False，左下角(含主对角线)为全True的subsequent_mask矩阵
    return torch.from_numpy(subsequent_mask) == 0
```

我们可视化一下 subsequent\_mask 矩阵的形式，直观进行理解。  
这里的 Attentionmask 图显示了允许每个目标词（行）查看的位置（列）。在训练期间，当前解码位置的词不能 Attend 到后续位置的词。

这里是给定一个序列长度size，生成一个下三角矩阵，在主对角线右上的都是 False，其示意图如下：

![[assets/attachments/uncategorized/v2-484b64d3579a733340dff351d5af902f_1440w.jpg]]

就是在decoder层的self-Attention中，由于生成 时， 并没有产生，所以不能有 和 的关联系数，即只有下三角矩阵有系数，即下图中 **`黄色部分`**

```python
plt.figure(figsize=(5,5))
plt.imshow(subsequent_mask(20)[0])
```
![[assets/attachments/uncategorized/v2-c63829521ea1183596c8f9f879bfe44a_1440w.jpg]]

**四. Transformer模型**

最后，我们把 Encoder 和 Decoder 组成 Transformer 模型

```python
class Transformer(nn.Module):
    def __init__(self, encoder, decoder, src_embed, tgt_embed, generator):
        super(Transformer, self).__init__()
        self.encoder = encoder
        self.decoder = decoder
        self.src_embed = src_embed
        self.tgt_embed = tgt_embed
        self.generator = generator 

    def encode(self, src, src_mask):
        return self.encoder(self.src_embed(src), src_mask)

    def decode(self, memory, src_mask, tgt, tgt_mask):
        return self.decoder(self.tgt_embed(tgt), memory, src_mask, tgt_mask)

    def forward(self, src, tgt, src_mask, tgt_mask):
        # encoder的结果作为decoder的memory参数传入，进行decode
        return self.decode(self.encode(src, src_mask), src_mask, tgt, tgt_mask)

class Generator(nn.Module):
    # vocab: tgt_vocab
    def __init__(self, d_model, vocab):
        super(Generator, self).__init__()
        # decode后的结果，先进入一个全连接层变为词典大小的向量
        self.proj = nn.Linear(d_model, vocab)

    def forward(self, x):
        # 然后再进行log_softmax操作(在softmax结果上再做多一次log运算)
        return F.log_softmax(self.proj(x), dim=-1)
```

定义设置超参并连接完整模型的函数

```python
def make_model(src_vocab, tgt_vocab, N=6, d_model=512, d_ff=2048, h = 8, dropout=0.1):
    c = copy.deepcopy
    # 实例化Attention对象
    attn = MultiHeadedAttention(h, d_model).to(DEVICE)
    # 实例化FeedForward对象
    ff = PositionwiseFeedForward(d_model, d_ff, dropout).to(DEVICE)
    # 实例化PositionalEncoding对象
    position = PositionalEncoding(d_model, dropout).to(DEVICE)
    # 实例化Transformer模型对象
    model = Transformer(
        Encoder(EncoderLayer(d_model, c(attn), c(ff), dropout).to(DEVICE), N).to(DEVICE),
        Decoder(DecoderLayer(d_model, c(attn), c(attn), c(ff), dropout).to(DEVICE), N).to(DEVICE),
        nn.Sequential(Embeddings(d_model, src_vocab).to(DEVICE), c(position)),
        nn.Sequential(Embeddings(d_model, tgt_vocab).to(DEVICE), c(position)),
        Generator(d_model, tgt_vocab)).to(DEVICE)
    
    # This was important from their code. 
    # Initialize parameters with Glorot / fan_avg.
    for p in model.parameters():
        if p.dim() > 1:
            # 这里初始化采用的是nn.init.xavier_uniform
            nn.init.xavier_uniform_(p)
    return model.to(DEVICE)
```

**五. 模型训练**

标签平滑

在训练期间，我们采用了值 ϵls=0.1的标签平滑（参见： [arxiv.org/pdf/1512.0056](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/1512.00567.pdf) ），其实还是从ComputerVision上搬过来的，具体操作可以看下面的代码实现， **在这里不作为重点** 。  
这种做法提高了困惑度，因为模型变得更加不确定，但提高了准确性和BLEU分数。 我们使用 KLdivloss（KL散度损失）实现标签平滑。  
对于输出的分布，从原始的 one-hot 分布转为在groundtruth上使用一个confidence值，而后其他的所有非groudtruth标签上采用 作为概率值进行平滑。

```python
class LabelSmoothing(nn.Module):
    """标签平滑处理"""
    def __init__(self, size, padding_idx, smoothing=0.0):
        super(LabelSmoothing, self).__init__()
        self.criterion = nn.KLDivLoss(reduction='sum')
        self.padding_idx = padding_idx
        self.confidence = 1.0 - smoothing
        self.smoothing = smoothing
        self.size = size
        self.true_dist = None
        
    def forward(self, x, target):
        assert x.size(1) == self.size
        true_dist = x.data.clone()
        true_dist.fill_(self.smoothing / (self.size - 2))
        true_dist.scatter_(1, target.data.unsqueeze(1), self.confidence)
        true_dist[:, self.padding_idx] = 0
        mask = torch.nonzero(target.data == self.padding_idx)
        if mask.dim() > 0:
            true_dist.index_fill_(0, mask.squeeze(), 0.0)
        self.true_dist = true_dist
        return self.criterion(x, Variable(true_dist, requires_grad=False))
```

这里的size是输出词表的大小，smoothing是用于分摊在非groundtruth上面的概率值

**计算损失**

```python
class SimpleLossCompute:
    """
    简单的计算损失和进行参数反向传播更新训练的函数
    """
    def __init__(self, generator, criterion, opt=None):
        self.generator = generator
        self.criterion = criterion
        self.opt = opt
        
    def __call__(self, x, y, norm):
        x = self.generator(x)
        loss = self.criterion(x.contiguous().view(-1, x.size(-1)), 
                              y.contiguous().view(-1)) / norm
        loss.backward()
        if self.opt is not None:
            self.opt.step()
            self.opt.optimizer.zero_grad()
        return loss.data.item() * norm.float()
```

**optimizer优化器**

论文里面提到了他们用的优化器，是以 、 和 的 Adam$ 为基础，而后使用一种warmup的学习率调整方式来进行调节。

具体公式如下：

基本上就是用一个固定的 warmup\_steps 先进行学习率的线性增长（热身），而后到达 warmup\_steps 之后会随着 step\_num 的增长，以 step\_num（步数）的反平方根成比例地逐渐减小它，他们用的 warmup\_steps = 4000 ，这个可以针对不同的问题自己尝试。

```python
class NoamOpt:
    "Optim wrapper that implements rate."
    def __init__(self, model_size, factor, warmup, optimizer):
        self.optimizer = optimizer
        self._step = 0
        self.warmup = warmup
        self.factor = factor
        self.model_size = model_size
        self._rate = 0
        
    def step(self):
        "Update parameters and rate"
        self._step += 1
        rate = self.rate()
        for p in self.optimizer.param_groups:
            p['lr'] = rate
        self._rate = rate
        self.optimizer.step()
        
    def rate(self, step = None):
        "Implement \`lrate\` above"
        if step is None:
            step = self._step
        return self.factor * (self.model_size ** (-0.5) * min(step ** (-0.5), step * self.warmup ** (-1.5)))
        
def get_std_opt(model):
    return NoamOpt(model.src_embed[0].d_model, 2, 4000,
            torch.optim.Adam(model.parameters(), lr=0, betas=(0.9, 0.98), eps=1e-9))
```

主要调节是在 *rate* rate 这个函数中，其中

- model\_size 即为 dmodel
- warmup 即为 warmup\_steps
- factor 可以理解为初始的学习率

**训练迭代**

接下来，我们创建一个通用的训练和评分功能来跟踪损失。 我们传入一个上面定义的损失计算函数，它也处理参数更新。

```python
def run_epoch(data, model, loss_compute, epoch):
    start = time.time()
    total_tokens = 0.
    total_loss = 0.
    tokens = 0.

    for i , batch in enumerate(data):
        out = model(batch.src, batch.trg, batch.src_mask, batch.trg_mask)
        loss = loss_compute(out, batch.trg_y, batch.ntokens)

        total_loss += loss
        total_tokens += batch.ntokens
        tokens += batch.ntokens

        if i % 50 == 1:
            elapsed = time.time() - start
            print("Epoch %d Batch: %d Loss: %f Tokens per Sec: %fs" % (epoch, i - 1, loss / batch.ntokens, (tokens.float() / elapsed / 1000.)))
            start = time.time()
            tokens = 0

    return total_loss / total_tokens

def train(data, model, criterion, optimizer):
    """
    训练并保存模型
    """
    # 初始化模型在dev集上的最优Loss为一个较大值
    best_dev_loss = 1e5
    
    for epoch in range(EPOCHS):
        # 模型训练
        model.train()
        run_epoch(data.train_data, model, SimpleLossCompute(model.generator, criterion, optimizer), epoch)
        model.eval()

        # 在dev集上进行loss评估
        print('>>>>> Evaluate')
        dev_loss = run_epoch(data.dev_data, model, SimpleLossCompute(model.generator, criterion, None), epoch)
        print('<<<<< Evaluate loss: %f' % dev_loss)
        
        # TODO: 如果当前epoch的模型在dev集上的loss优于之前记录的最优loss则保存当前模型，并更新最优loss值
        if dev_loss < best_dev_loss:
            torch.save(model.state_dict(), SAVE_FILE)
            best_dev_loss = dev_loss
        
        
        print()

# 数据预处理
data = PrepareData(TRAIN_FILE, DEV_FILE)
src_vocab = len(data.en_word_dict)
tgt_vocab = len(data.cn_word_dict)
print("src_vocab %d" % src_vocab)
print("tgt_vocab %d" % tgt_vocab)

# 初始化模型
model = make_model(
                    src_vocab, 
                    tgt_vocab, 
                    LAYERS, 
                    D_MODEL, 
                    D_FF,
                    H_NUM,
                    DROPOUT
                )

# 训练
print(">>>>>>> start train")
train_start = time.time()
criterion = LabelSmoothing(tgt_vocab, padding_idx = 0, smoothing= 0.0)
optimizer = NoamOpt(D_MODEL, 1, 2000, torch.optim.Adam(model.parameters(), lr=0, betas=(0.9,0.98), eps=1e-9))

train(data, model, criterion, optimizer)
print(f"<<<<<<< finished train, cost {time.time()-train_start:.4f} seconds")
```

**六. 模型预测**

```python
def greedy_decode(model, src, src_mask, max_len, start_symbol):
    """
    传入一个训练好的模型，对指定数据进行预测
    """
    # 先用encoder进行encode
    memory = model.encode(src, src_mask)
    # 初始化预测内容为1×1的tensor，填入开始符('BOS')的id，并将type设置为输入数据类型(LongTensor)
    ys = torch.ones(1, 1).fill_(start_symbol).type_as(src.data)
    # 遍历输出的长度下标
    for i in range(max_len-1):
        # decode得到隐层表示
        out = model.decode(memory, 
                           src_mask, 
                           Variable(ys), 
                           Variable(subsequent_mask(ys.size(1)).type_as(src.data)))
        # 将隐藏表示转为对词典各词的log_softmax概率分布表示
        prob = model.generator(out[:, -1])
        # 获取当前位置最大概率的预测词id
        _, next_word = torch.max(prob, dim = 1)
        next_word = next_word.data[0]
        # 将当前位置预测的字符id与之前的预测内容拼接起来
        ys = torch.cat([ys, 
                        torch.ones(1, 1).type_as(src.data).fill_(next_word)], dim=1)
    return ys

def evaluate(data, model):
    """
    在data上用训练好的模型进行预测，打印模型翻译结果
    """
    # 梯度清零
    with torch.no_grad():
        # 在data的英文数据长度上遍历下标
        for i in range(len(data.dev_en)):
            # TODO: 打印待翻译的英文句子
            en_sent = " ".join([data.en_index_dict[w] for w in  data.dev_en[i]])
            print("\n" + en_sent)
            
            # TODO: 打印对应的中文句子答案
            cn_sent = " ".join([data.cn_index_dict[w] for w in  data.dev_cn[i]])
            print("".join(cn_sent))
            
            # 将当前以单词id表示的英文句子数据转为tensor，并放如DEVICE中
            src = torch.from_numpy(np.array(data.dev_en[i])).long().to(DEVICE)
            # 增加一维
            src = src.unsqueeze(0)
            # 设置attention mask
            src_mask = (src != 0).unsqueeze(-2)
            # 用训练好的模型进行decode预测
            out = greedy_decode(model, src, src_mask, max_len=MAX_LENGTH, start_symbol=data.cn_word_dict["BOS"])
            # 初始化一个用于存放模型翻译结果句子单词的列表
            translation = []
            # 遍历翻译输出字符的下标（注意：开始符"BOS"的索引0不遍历）
            for j in range(1, out.size(1)):
                # 获取当前下标的输出字符
                sym = data.cn_index_dict[out[0, j].item()]
                # 如果输出字符不为'EOS'终止符，则添加到当前句子的翻译结果列表
                if sym != 'EOS':
                    translation.append(sym)
                # 否则终止遍历
                else:
                    break
            # 打印模型翻译输出的中文句子结果
            print("translation: %s" % " ".join(translation))

# 预测
# 加载模型
model.load_state_dict(torch.load(SAVE_FILE))
# 开始预测
print(">>>>>>> start evaluate")
evaluate_start  = time.time()
evaluate(data, model)         
print(f"<<<<<<< finished evaluate, cost {time.time()-evaluate_start:.4f} seconds")

<-------------------截取了一些测试结果------------------------>
He is my youngest brother . EOS
BOS 他 是 我 最 年 轻 的 兄 弟 。 EOS
translation: 他 是 我 最 年 轻 的 兄 弟 。

BOS Most boys like computer games . EOS
BOS 大 多 数 男 生 喜 欢 电 脑 游 戏 。 EOS
translation: 大 部 分 男 生 喜 欢 电 脑 游 戏 。

BOS Can I have a bite ? EOS
BOS 我 可 以 吃 一 口 嗎 ？ EOS
translation: 我 有 咬 吗 ？

BOS This is not very UNK . EOS
BOS 這 不 是 很 流 行 。 EOS
translation: 這 不 是 很 匆 忙 的 。

BOS There is a fork missing . EOS
BOS 少 一 把 叉 子 。 EOS
translation: 少 一 把 叉 子 。

BOS I love my yellow sweater . EOS
BOS 我 很 喜 欢 我 的 黄 色 套 衫 。 EOS
translation: 我 愛 頭 髮 師 為 我 的 毛 筆 。

BOS We UNK tea from India . EOS
BOS 我 們 從 印 度 進 口 茶 葉 。 EOS
translation: 我 們 從 印 度 進 口 茶 。

BOS He seldom goes to church . EOS
BOS 他 很 少 去 教 堂 。 EOS
translation: 他 很 少 去 教 堂 。

BOS It seemed to be cheap . EOS
BOS 似 乎 很 便 宜 。 EOS
translation: 似 乎 很 便 宜 。

BOS Tom can keep a secret . EOS
BOS 汤 姆 会 保 密 。 EOS
translation: 汤 姆 可 能 是 一 个 秘 密 。

BOS Tennis is my favorite sport . EOS
BOS 网 球 是 我 最 喜 欢 的 运 动 。 EOS
translation: 网 球 是 我 最 喜 欢 的 运 动 。

BOS When is your bed time ? EOS
BOS 你 什 么 时 候 睡 觉 ？ EOS
translation: 你 什 麼 時 候 睡 覺 ?

BOS Give me something to do . EOS
BOS 给 我 点 事 做 。 EOS
translation: 給 我 些 什 麼 事 做 。

BOS Nobody gave us a chance . EOS
BOS 没 人 给 我 们 机 会 。 EOS
translation: 没 人 给 我 们 机 会 。

BOS I am six feet tall . EOS
BOS 我 六 英 尺 高 。 EOS
translation: 我 六 點 高 。

BOS Where can you get tickets ? EOS
BOS 在 哪 里 可 以 买 到 车 票 ？ EOS
translation: 你 在 哪 里 可 以 搭 到 火 車 ？

BOS These pants fit me well . EOS
BOS 我 穿 這 條 褲 子 很 合 身 。 EOS
translation: 這 些 裤 子 我 穿 起 來 很 合 身 。

BOS He showed me her picture . EOS
BOS 他 給 我 看 了 她 的 照 片 。 EOS
translation: 他 給 我 看 了 她 的 照 片 。

BOS Are you afraid of UNK ? EOS
BOS 你 怕 虫 子 吗 ？ EOS
translation: 你 怕 虫 子 吗 ？

BOS How about taking a rest ? EOS
BOS 休 息 一 下 怎 麼 樣 ? EOS
translation: 休 息 一 下 怎 麼 樣 ?

BOS I need a UNK dictionary . EOS
BOS 我 需 要 一 本 日 英 字 典 。 EOS
translation: 我 需 要 一 本 的 字 典 。

BOS He 's a bit UNK . EOS
BOS 他 有 点 活 泼 。 EOS
translation: 他 有 点 活 泼 。

BOS He 's bound to forget . EOS
BOS 他 准 会 忘 。 EOS
translation: 他 會 忘 。

BOS The well has run dry . EOS
BOS 這 口 井 乾 涸 了 。 EOS
translation: 這 口 井 乾 涸 了 。
```

**参考资料**

[arxiv.org/pdf/1706.0376](https://link.zhihu.com/?target=https%3A//arxiv.org/pdf/1706.03762.pdf)

[jianshu.com/p/579a0f4cb](https://link.zhihu.com/?target=https%3A//www.jianshu.com/p/579a0f4cbf24)

[blog.csdn.net/york1996/](https://link.zhihu.com/?target=https%3A//blog.csdn.net/york1996/article/details/102955270)

发布于 2020-05-31 17:40[机器翻译](https://www.zhihu.com/topic/19616892)[自然语言处理](https://www.zhihu.com/topic/19560026)[Transformer](https://www.zhihu.com/topic/20746363)[数字孪生不用游戏引擎可以吗？](https://www.shanhaibi.com/?utm=v2_ad_zhihu&spu=biz%3D0%26ci%3D3673767%26si%3De5752f4d-691a-4dc4-a419-5243ed72aa58%26ts%3D1775468103%26zid%3D1629)

[

推荐一款纯自研的数字孪生引擎，是我目前能找到的产品化做的相当好的一款产品，不仅视觉效果可以媲美游戏引擎的...

](https://www.shanhaibi.com/?utm=v2_ad_zhihu&spu=biz%3D0%26ci%3D3673767%26si%3De5752f4d-691a-4dc4-a419-5243ed72aa58%26ts%3D1775468103%26zid%3D1629)