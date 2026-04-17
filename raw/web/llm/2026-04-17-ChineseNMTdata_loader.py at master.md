---
source_type:
source: "https://github.com/hemingkx/ChineseNMT/tree/master"
title: "ChineseNMT/data_loader.py at master"
author:
published_at:
created_at: "2026-04-17T12:03:51+08:00"
topics: "ChineseNMT: Translate English to Chinese with PyTorch Implementation of Transformer - ChineseNMT/data_loader.py at master · hemingkx/ChineseNMT"
tags:
  - "clippings"
related_concepts:
status: "inbox"
---
Language: 简体中文 | [English](https://github.com/hemingkx/ChineseNMT/blob/master/README-en.md)

## ChineseNMT

基于transformer的英译中翻译模型🤗。

项目说明参考知乎文章： [教你用PyTorch玩转Transformer英译中翻译模型！](https://zhuanlan.zhihu.com/p/347061440)

## Data

The dataset is from [WMT 2018 Chinese-English track](http://statmt.org/wmt18/translation-task.html) (Only NEWS Area)

## Data Process

### 分词

- 工具： [sentencepiece](https://github.com/google/sentencepiece)
- 预处理：`./data/get_corpus.py` 抽取train、dev和test中双语语料，分别保存到 `corpus.en` 和 `corpus.ch` 中，每行一个句子。
- 训练分词模型：`./tokenizer/tokenize.py` 中调用了sentencepiece.SentencePieceTrainer.Train()方法，利用 `corpus.en` 和 `corpus.ch` 中的语料训练分词模型，训练完成后会在`./tokenizer` 文件夹下生成 `chn.model` ， `chn.vocab` ， `eng.model` 和 `eng.vocab` ，其中`.model` 和`.vocab` 分别为模型文件和对应的词表。

## Model

采用Harvard开源的 [transformer-pytorch](http://nlp.seas.harvard.edu/2018/04/03/attention.html) ，中文说明可参考 [传送门](https://zhuanlan.zhihu.com/p/144825330) 。

## Requirements

This repo was tested on Python 3.6+ and PyTorch 1.5.1. The main requirements are:

- tqdm
- pytorch >= 1.5.1
- sacrebleu >= 1.4.14
- sentencepiece >= 0.1.94

To get the environment settled quickly, run:

```
pip install -r requirements.txt
```

## Usage

模型参数在 `config.py` 中设置。

- 由于transformer显存要求，支持MultiGPU，需要设置 `config.py` 中的 `device_id` 列表以及 `main.py` 中的 `os.environ['CUDA_VISIBLE_DEVICES']` 。

如要运行模型，可在命令行输入：

```
python main.py
```

实验结果在`./experiment/train.log` 文件中，测试集翻译结果在`./experiment/output.txt` 中。

> 在两块GeForce GTX 1080 Ti上运行，每个epoch用时一小时左右。

## Results

| Model | NoamOpt | LabelSmoothing | Best Dev Bleu | Test Bleu |
| --- | --- | --- | --- | --- |
| 1 | No | No | 24.07 | 24.03 |
| 2 | Yes | No | **26.08** | **25.94** |
| 3 | No | Yes | 23.92 | 23.84 |

## Pretrained Model

训练好的 Model 2 模型（当前最优模型）可以在如下链接直接下载😊：

链接: [https://pan.baidu.com/s/1RKC-HV\_UmXHq-sy1-yZd2Q](https://pan.baidu.com/s/1RKC-HV_UmXHq-sy1-yZd2Q) 密码: g9wl

## Beam Search

当前最优模型（Model 2）使用beam search测试的结果

| Beam\_size | 2 | 3 | 4 | 5 |
| --- | --- | --- | --- | --- |
| Test Bleu | 26.59 | 26.80 | 26.84 | **26.86** |

## One Sentence Translation

将训练好的model或者上述Pretrained model以 `model.pth` 命名，保存在`./experiment` 路径下。在 `main.py` 中运行 `translate_example` ，即可实现单句翻译。

如英文输入单句为：

```
The near-term policy remedies are clear: raise the minimum wage to a level that will keep a fully employed worker and his or her family out of poverty, and extend the earned-income tax credit to childless workers.
```

ground truth为：

```
近期的政策对策很明确：把最低工资提升到足以一个全职工人及其家庭免于贫困的水平，扩大对无子女劳动者的工资所得税减免。
```

beam size = 3的翻译结果为：

```
短期政策方案很清楚:把最低工资提高到充分就业的水平,并扩大向无薪工人发放所得的税收信用。
```

## Mention

The codes released in this reposity are only tested successfully with **Linux**. If you wanna try it with **Windows**, steps below may be useful to you as mentioned in [issue 2](https://github.com/hemingkx/ChineseNMT/issues/2):

1. **adding utf-8 encoding declaration:**
	in lines 16 and 19 of get\_corpus.py:
	```
	with open(ch_path, "w", encoding="utf-8") as fch:
	with open(en_path, "w", encoding="utf-8") as fen:
	```
	in line 165 of train.py:
	```
	with open(config.output_path, "w", encoding="utf-8") as fp:
	```
2. **using conda command to install sacrebleu if Anoconda is used for building your virtual env:**
	```
	conda install -c conda-forge sacrebleu
	```

For any other problems you meet when doing your own project, welcome to issuing or sending emails to me 😊~