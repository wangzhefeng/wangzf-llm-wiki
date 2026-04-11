---
source_type: web
title: "教你用PyTorch玩转Transformer英译中翻译模型！"
author:
  - 
  - "[[hemingkx​北京大学 软件工程硕士]]"
created_at: 2026-04-06
topics:
  - 大语言模型
status: inbox
published: 
created: 2026-04-06
description: "本文分享一个基于Harvard开源的 transformer-pytorch的机器翻译模型（英译中）。在编写项目的过程中，从数据处理、模型编写、BLEU值计算到解决GPU的显存分配问题，我们都踩了不少坑，因此将心得分享给大家～Github…"
tags:
  - 
  - "clippings"
source_url: "https://zhuanlan.zhihu.com/p/347061440"
published_at: null
related_concepts: []
---

本文分享一个基于Harvard开源的 [transformer-pytorch](https://link.zhihu.com/?target=http%3A//nlp.seas.harvard.edu/2018/04/03/attention.html) 的机器翻译模型（英译中）。在编写项目的过程中，从数据处理、模型编写、 [BLEU值](https://zhida.zhihu.com/search?content_id=165254750&content_type=Article&match_order=1&q=BLEU%E5%80%BC&zhida_source=entity) 计算到解决GPU的显存分配问题，我们都踩了不少坑，因此将心得分享给大家～

Github地址： [github.com/hemingkx/Chi](https://link.zhihu.com/?target=https%3A//github.com/hemingkx/ChineseNMT)

---

## 1、机器翻译

机器翻译（Machine Translation），又称为自动翻译，是利用计算机把一种自然源语言转变为另一种自然目标语言的过程，一般指自然语言之间句子和全文的翻译。而 **英译中的机器翻译，即指把英文句子翻译为中文句子** 。

![[raw/assets/attachments/llm/v2-3e066b920658e54710e539bd6b77455f_1440w.jpg]]

（手动狗头

机器翻译方法主要有基于实例的机器翻译方法、基于统计的机器翻译方法以及神经机器翻译（Neural Machine Translation，NMT）。NMT通常采用 **Encoder-Decoder** 结构，实现对变长输入句子的建模。编码器实现对源语言句子的"理解"，形成一个特定维度的浮点数向量，之后解码器根据此向量逐字生成目标语言的翻译结果。

在NMT发展初期， [RNN](https://zhida.zhihu.com/search?content_id=165254750&content_type=Article&match_order=1&q=RNN&zhida_source=entity) 、 [LSTM](https://zhida.zhihu.com/search?content_id=165254750&content_type=Article&match_order=1&q=LSTM&zhida_source=entity) 、 [GRU](https://zhida.zhihu.com/search?content_id=165254750&content_type=Article&match_order=1&q=GRU&zhida_source=entity) 等被广泛用作编码器和解码器的网络结构。2017年， **Transformer** [^1] 横空出世。它不但在翻译效果上大幅超越了基于RNN的神经网络，还通过训练的并行化实现了训练效率的提升。目前，业界机器翻译主流框架广泛采用Transformer。因此， **我们在本文中也具体分享Transformer在翻译任务中的使用，教你从零开始玩转Transformer机器翻译模型** ！

## 2、数据处理

数据集来自 [WMT 2018 Chinese-English track](https://link.zhihu.com/?target=http%3A//statmt.org/wmt18/translation-task.html) (Only NEWS Area)。

**2.1 原始数据格式**

如下所示，原始的数据集是en-cn的sentence pair。

```
[
  ['Some analysts argue that the negative effects of such an outcome would only last for “months.”', 
   '某些分析家认为军事行动的负面效果只会持续短短“几个月”。'],
  ['The Fed apparently could not stomach the sell-off in global financial markets in January and February, which was driven largely by concerns about further tightening.', 
  '美联储显然无法消化1月和2月的全球金融市场抛售，而这一抛售潮主要是因为对美联储进一步紧缩的担忧导致的。']
]
```

**2.2 BPE分词**

BPE(Byte Pair Encoding)最早是一种压缩算法， **基本思路是将使用最频繁的字节用一个新的字节组合代替** ，比如用字符的n-gram替换各个字符。例如，假设('A', 'B') 经常顺序出现，则用一个新的标志'AB'来代替它们。2016年，Sennrich [^2] 提出采用分词算法（word segmentation）构建BPE，并将其应用于机器翻译任务中。论文提出的基本思想是，给定语料库，初始词汇库仅包含所有的单个字符。然后，模型不断地将出现频率最高的n-gram pair作为新的n-gram加入到词汇库中，直到词汇库的大小达到我们所设定的某个目标为止。

![[raw/assets/attachments/llm/v2-ca72c65768150425966bf5adadca45ed_1440w.jpg]]

论文中给出的算法例子如上图所示。 **算法从所有的字符开始，首先将出现频率最高的 (e, s) 作为新的词汇加入表中，然后是(es, t)。** 以此类推，直到词汇库大小达到我们设定的值。更清晰的过程如下图所示。其中，Dictionary左列表示单词出现的频率。

![[raw/assets/attachments/llm/v2-e22f345e20ec52372c065e66dc1e5c59_1440w.jpg]]

![[raw/assets/attachments/llm/v2-e15a00ed73d4fe9b6474f47ac6148529_1440w.jpg]]

![[raw/assets/attachments/llm/v2-4fdb512b61ec7a0e2945f6eb7973a217_1440w.jpg]]

cs224n-2019 Lecture 12

这个例子中词汇量较小，对于词汇量很大的实际情况，我们就可以通过BPE算法逐步建造一个基于subword unit的词汇库来表示所有的词汇，该词汇库由频率出现最多的 subword 组成，对未知词 (Out Of Vocabulary) 的预测有较大帮助。

本项目使用 [sentencepiece](https://link.zhihu.com/?target=https%3A//github.com/google/sentencepiece) [^3] 实现BPE分词。sentencepiece是一个google开源的自然语言处理工具包，支持bpe、unigram等多种分词方法。其优势在于：bpe、unigram等方法均假设输入文本是已经切分好的，只有这样bpe才能统计词频（通常直接通过空格切分）。但问题是，汉语、日语等语言的字与字之间并没有空格分隔。 **sentencepiece提出，可以将所有字符编码成Unicode码（包括空格），通过训练直接将原始文本（未切分）变为分词后的文本，从而避免了跨语言的问题。**

我们简要探究了英文和中文应选择的词表大小，发现英文的词表大小设定为32000时，可以覆盖数据集中词频为10以上的bpe组合；中文词表大小设定为32000时，覆盖了数据集中词频为21以上的bpe组合。进一步扩大词表，会导致词表过大，含有的非常用词增多，模型的训练参数也会增多。因此，我们设定中英文词表大小均为32000。根据 [sentencepiece](https://link.zhihu.com/?target=https%3A//github.com/google/sentencepiece) 代码说明， 这一参数在字符集较大的中文分词中设置为0.995，在字符集较小的英文分词中设置为1。

我们在tokenizer/tokenize.py文件中利用数据集中的中英语料训练分词模型，训练完成后会在指定路径下保存分词模型和词表。分词后的例子如下所示

如上所述，sentencepiece将每句文本的开头和空格均用 表示。

**2.3 数据预处理**

训练好分词模型之后，我们基于torch.utils.data.Dataset进行数据的预处理，主要包括：

- 把原始语料中的中英文句对按照英文句子的长度排序，使得每个batch中的句子长度相近。
- 利用训练好的分词模型分别对中英文句子进行分词，利用词表将其转换为id。
- 在每个 id sequence 的首尾加上起始符和终止符，并将其转换为Tensor。

将上述Tensor输入到 [transformer-pytorch](https://link.zhihu.com/?target=http%3A//nlp.seas.harvard.edu/2018/04/03/attention.html) 定义的Batch类中，转换为transformer支持的输入格式（构造decoder的输入输出、attention mask等）。上述代码在data\_loader.py文件中～。

## 3、Transformer

Transformer是Google在Attention is All You Need [^1] 论文中提出的模型。它并没有使用以往的CNN/RNN model，是一个仅基于 [Attention机制](https://zhida.zhihu.com/search?content_id=165254750&content_type=Article&match_order=1&q=Attention%E6%9C%BA%E5%88%B6&zhida_source=entity) 的模型。这使得它摆脱了RNN模型顺序读取序列的缺点，可以实现高度的并行化。

同时，CNN model的卷积操作使得获取相距较远的token之间的dependency的operation和距离成正比，即难以获取相距较远的token之间的依存关系，而Attention机制使得获取dependency的operation为常数，与距离无关。由于以上特点，导致Attention模型在各个方面超过了以往的SOTA模型，并且在多个任务上达到了SOTA结果。

![[raw/assets/attachments/llm/v2-e09a169399782babea626d87282bf14e_1440w.jpg]]

和大多数seq2seq模型一样，Transformer的结构也是一个编码器-解码器模型，模型结构如上图所示。本文使用Harvard开源的 [transformer-pytorch](https://link.zhihu.com/?target=http%3A//nlp.seas.harvard.edu/2018/04/03/attention.html) 代码构建transformer模型。不得不说Harvard贡献的轮子很好用！代码结构清晰，且由于之前在 [The Annotated Transformer](https://link.zhihu.com/?target=https%3A//nlp.seas.harvard.edu/2018/04/03/attention.html) 已经具体学习过一遍，使用起来压力小很多！我们做出的修改如下：

- 为加速解码过程，我们将greedy decode基于batch重新实现。
- transformer-pytorch使用的pytorch版本较早，我们修改了其与pytorch 1.5.1版本不兼容的地方。

代码文件位于model.py文件中～。

## 4、Warm Up

Warm up是在ResNet [^4] 中提到的一种针对包括Adam和RMSProp在内的一些自适应优化器的学习率预热方法。由于刚开始训练时，模型的权重通常是随机初始化的，此时选择一个较大的学习率，可能会引入一定的不稳定性。warm up就是在刚开始训练的时候先使用一个较小的学习率，训练一些epoches或iterations，等模型稳定时再修改为预先设置的学习率进行训练。ResNet [^4] 中使用一个110层的ResNet在cifar10上训练时，先用0.01的学习率训练直到训练误差低于80%，然后使用0.1的学习率进行训练。

18年，Facebook又针对上述的constant warmup方法进行了改进 [^5] ，因为从一个很小的学习率一下变为比较大的学习率可能会导致训练误差突然增大。Facebook [^5] 提出了gradual warmup来解决这个问题，即从最开始的小学习率开始，每个iteration增大一点，直到最初设置的比较大的学习率。

我们采用了和transformer [^1] 一致的warmup策略，具体如下式所示。其中， 是模型的特征维度， 是训练模型所需的总步数， 是人为设置的Warm Up阶段所占用的步数。

在模型中，我们采用的参数为 ， ，对应的warm-up学习率曲线如下图所示。

![[raw/assets/attachments/llm/v2-f16163e57fbcb7afe345509acc2a05b8_1440w.jpg]]

可以看到，transformer [^1] 在Warm Up阶段采用的策略与Facebook [^5] 近似。在Warm Up阶段之后，transformer [^1] 采用了指数的学习率递减策略。这一整体的学习率更新策略在下文中称为 [NoamOpt](https://zhida.zhihu.com/search?content_id=165254750&content_type=Article&match_order=1&q=NoamOpt&zhida_source=entity) （这是The Annotated Transformer中的称法）。

## 5、Label Smoothing

在分类问题中，我们的最后一层一般是全连接层，然后对应标签的one-hot编码，即把对应类别的值编码为1，其他为0。这种编码方式和通过降低交叉熵损失来调整参数的方式结合起来，会有一些问题。这种方式会鼓励模型对不同类别的输出分数差异非常大，或者说，模型过分相信它的判断。但是，对于一个由多人标注的数据集，不同人标注的准则可能不同，每个人的标注也可能会有一些错误。模型对标签的过分信任，可能会造成过拟合。

标签平滑(Label-smoothing)是应对该问题的有效方法之一，它的具体思想是降低我们对于标签的信任，例如我们可以将损失的目标值从1稍微降到0.9，或者将从0稍微升到0.1。标签平滑最早在inception-v2 [^6] 中被提出，它将真实的概率改造为：

其中， 是一个小的常数， 是类别的数目， 是图片的真正的标签， 代表第 个类别， 是图片为第 类的概率。

总的来说，LSR是一种通过在标签 中加入噪声，实现对模型约束，降低模型过拟合程度的一种正则化方法。transformer [^1] 通过实验发现，这种做法提高了困惑度，因为模型变得更加不确定，但提高了准确性和BLEU分数。

## 6、Beam Search

**相比于分类任务，生成任务通常是一个时间步一个时间步依次获得，且之前时间步的结果影响下一个时间步，也即模型的输出都是基于历史生成结果的条件概率。** 在生成序列时，最暴力的方法当然是穷举所有可能的序列，选取其中连乘概率最大的候选序列，但该方法很明显计算复杂度过高。

一个自然的改进想法是，每一个时间步都取条件概率最大的输出，即所谓的贪心搜索（Greedy Search），但这种方法会丢弃绝大部分的可能解，仅关注当前时间步，无法保证最终得到的序列是最优解。集束搜索（Beam Search）实际是这两者的折中，简言之，在每一个时间步，不再仅保留当前概率最高的1个输出，而是每次都保留 个输出。

![[raw/assets/attachments/llm/v2-646811f5b40d380f6201b97128f582a3_1440w.jpg]]

如图所示，图中的 ，也就是说每个时间步都会保留到当前步为止，条件概率最优的2个序列。

## 7、BLEU

BLEU即Bilingual Evaluation Understudy，在机器翻译任务中，BLEU非常常见，它主要用于评估模型生成句子（candidate）和实际句子（reference）之间的差异。其具体的计算公式见下式：

其中 是n-gram修正准确率， 为1/n， 是机器译文长度， 是参考译文长度， 通常取为4（和人工评价相关度最高）。

我们的BLEU值计算采用 [sacrebleu](https://link.zhihu.com/?target=https%3A//github.com/mjpost/sacrebleu) [^7] 。sacrebleu指出，现有的BLEU计算工具(nltk等)均需要提前进行分词，采取的分词方案不同会导致BLEU计算的结果有较大差异。因此，sacrebleu接收原文本输入，将分词和bleu计算统一进行，提供了更加具有可比性的BLEU分数参考。

## 8、模型训练

考虑到 [transformer-pytorch](https://link.zhihu.com/?target=http%3A//nlp.seas.harvard.edu/2018/04/03/attention.html) 运行时占用的服务器显存超过单一服务器显存上限，我们在模型中加入了多GPU训练支持。 **我们对比了Pytorch提供的nn.DataParallel，发现该方法在各GPU上存在严重的显存使用不均衡的问题。** 主要原因是，nn.DataParallel中，主GPU汇集了所有GPU的运算结果，导致主GPU 汇集的梯度过大，从而造成了显存使用不平衡的问题。

我们最终参考 [transformer-pytorch](https://link.zhihu.com/?target=http%3A//nlp.seas.harvard.edu/2018/04/03/attention.html) 的做法，实现损失函数的分布化计算，让梯度在各个GPU上单独计算，反向传播。我们同样对比了nn.DistributedDataParallel，效果并未优于没有上述方法（这方面坑还挺多的，多GPU计算真难...）。

## 9、实验结果

**9.1 Model Study**

如上所述，我们具体探究了NoamOpt, Label Smoothing对英译中任务的提升效果。实验结果如表所示：

![[raw/assets/attachments/llm/v2-b263c2af8a9959530e41c55eeb07c19f_1440w.jpg]]

从表中可以看到，NoamOpt对实验效果的提升较大，在验证集上的最优Bleu分数提升了8.4%，测试集Bleu分数提升了7.9%。在本实验中，我们设置Label Smoothing的比例为0.1，其对实验效果的提升并不明显。但在之后基于fairseq的实验中，我们发现Label Smoothing确实对BLEU分数有一定的提升效果。

我们实现了Beam Search并在测试集上探究了不同beam size的bleu结果，如表所示。

![[raw/assets/attachments/llm/v2-7dcc04b58cd2c36da53453719ccf0fd2_1440w.jpg]]

可以看到，随着beam size增加，BLEU值也明显增加，且显著优于greedy decode的BLEU分数，提升3.5%。

**9.2 Case Study**

俗话说得好，是骡子是马拉出来溜溜！BLEU分数未免有些抽象，我们可以具体来看翻译结果。我们选取了比较有代表意义的三个例子，对greedy search和beam size为3的beam search的解码结果进行了对比分析。

> 注：以下三个case都是基于Pytorch model的最优训练模型（即Model 2）的翻译结果

![[raw/assets/attachments/llm/v2-15837feb683703d59a208d0ca585085f_1440w.jpg]]

case 1

![[raw/assets/attachments/llm/v2-974950b4a43391087799308465b959ca_1440w.jpg]]

case 2

![[raw/assets/attachments/llm/v2-51a6df0ea9c0724fcd099a6da62667c3_1440w.jpg]]

case 3

从case 1和case 3中可以明显看出， **地名、货币名这一类专有名词的翻译基本正确** ，说明这类词语的中英文能够形成非常好的对应，翻译难度较低。但对于一些 **较为抽象的词语** ，比如case 1中的“对于”，seq2seq的机器翻译由于没有语法知识作为支持，无法正确翻译出中国、美国和前苏联三者之间的关系。

case 2和case 3中都出现了 **重复翻译** 的情况，虽然出现的频率并不高，但其出现的原因还是非常值得探讨的，经查阅资料，发现这是基于神经网络翻译模型常有的错误，其原因是模型对某些已翻译过的词语过度关注，而且早在几年前就有研究提出过解决方法 [^8] [^9] 。

此外，我们发现 **无论Ground truth长短，模型输出的结果在不出现重复翻译的情况下基本比Ground truth要短** 。关于这一点，我们猜测可能是因为就词的粒度来看，较短词在语料中出现的频率一般是高于较长词，NMT由于模型自身的特点（统计因素）倾向于输出高频词，短词更容易被译出，因而模型输出的句子长度普遍偏短。

## 10、总结

这次项目给我们提供了一个非常好的熟悉Transformer的机会。在编写项目的过程中，即使之前对transformer已经有了较多的了解，还是遇到了很多坑（上面基本都提到了~）。因此，希望把我们的总结分享给大家，希望能对大家有所帮助～！

附上Github项目链接，欢迎star~!

> 另外附上一句提醒， [transformer-pytorch](https://link.zhihu.com/?target=http%3A//nlp.seas.harvard.edu/2018/04/03/attention.html) 可以让我们更熟悉transformer的细节，但是显然存在着占用显存过多和训练时间长的问题。如果想快速使用transformer解决任务，建议使用 [fairseq](https://link.zhihu.com/?target=https%3A//github.com/pytorch/fairseq) 。实际体验上，fairseq在本任务上的训练时间缩短了1/10，GPU显存占用也减至原先的1/3。需要快速做出成果的小伙伴可以考虑fairseq～

## 参考

编辑于 2021-04-15 23:53[神经机器翻译(NMT)](https://www.zhihu.com/topic/20096829)[Transformer](https://www.zhihu.com/topic/20746363)[PyTorch](https://www.zhihu.com/topic/20075993)[阿里云 ×OpenClaw 三步极速上手](https://click.aliyun.com/m/1000409721/?spu=biz%3D0%26ci%3D3693408%26si%3Df84923d4-533e-4e94-b81b-3bf464e0ed46%26ts%3D1775469261%26zid%3D1629)

[

无需技术背景！小白也能拥有

](https://click.aliyun.com/m/1000409721/?spu=biz%3D0%26ci%3D3693408%26si%3Df84923d4-533e-4e94-b81b-3bf464e0ed46%26ts%3D1775469261%26zid%3D1629)

[^1]: ^ <sup><a href="#ref_1_0">a</a></sup> <sup><a href="#ref_1_1">b</a></sup> <sup><a href="#ref_1_2">c</a></sup> <sup><a href="#ref_1_3">d</a></sup> <sup><a href="#ref_1_4">e</a></sup> <sup><a href="#ref_1_5">f</a></sup> Ashish Vaswani, Noam Shazeer, Niki Parmar, Jakob Uszkoreit, Llion Jones, Aidan N. Gomez, Lukasz Kaiser, and Illia Polosukhin. Attention is all you need, 2017.

[^2]: Rico Sennrich, Barry Haddow, and Alexandra Birch. Neural machine translation of rare words with subword units. In Proceedings of the 54th Annual Meeting of the Association for Computational Linguistics (Volume 1: Long Papers), pages 1715–1725, Berlin, Germany, August 2016. Association for Computational Linguistics.

[^3]: Taku Kudo and John Richardson. SentencePiece: A simple and language independent subword tokenizer and detokenizer for Neural Text Processing.

[^4]: ^ <sup><a href="#ref_4_0">a</a></sup> <sup><a href="#ref_4_1">b</a></sup> Kaiming He, Xiangyu Zhang, Shaoqing Ren, and Jian Sun. Deep residual learning for image recognition. CoRR, abs/1512.03385, 2015.

[^5]: ^ <sup><a href="#ref_5_0">a</a></sup> <sup><a href="#ref_5_1">b</a></sup> <sup><a href="#ref_5_2">c</a></sup> Priya Goyal, Piotr Dollár, Ross B. Girshick, Pieter Noordhuis, Lukasz Wesolowski, Aapo Kyrola, Andrew Tulloch, Yangqing Jia, and Kaiming He. Accurate, large minibatch SGD: training imagenet in 1 hour. CoRR, abs/1706.02677, 2017.

[^6]: Christian Szegedy, Vincent Vanhoucke, Sergey Ioffe, Jonathon Shlens, and Zbigniew Wojna. Rethinking the inception architecture for computer vision. CoRR, abs/1512.00567, 2015.

[^7]: Matt Post. A call for clarity in reporting BLEU scores. In Proceedings of the Third Conference on Machine Translation: Research Papers, pages 186–191, Brussels, Belgium, October 2018. Association for Computational Linguistics.

[^8]: Zhaopeng Tu, Zhengdong Lu, Yang Liu, Xiaohua Liu, and Hang Li. Modeling coverage for neural machine translation, 2016.

[^9]: Zhaopeng Tu, Yang Liu, Lifeng Shang, Xiaohua Liu, and Hang Li. Neural machine translation with reconstruction, 2016.