---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: 'ChineseNMT: Translate English to Chinese with PyTorch Implementation
  of Transformer - ChineseNMT/data_loader.py at master · hemingkx/ChineseNMT'
source_type: web
status: inbox
tags:
- null
- clippings
title: ChineseNMT/data_loader.py at master
topics:
- 深度学习
source_url: https://github.com/hemingkx/ChineseNMT/blob/master/data_loader.py
published_at: null
related_concepts: []
---

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

88

89

90

91

92

93

94

95

96

97

98

99

100

101

102

103

104

105

import torch

import json

import numpy as np

from torch.autograd import Variable

from torch.utils.data import Dataset

from torch.nn.utils.rnn import pad\_sequence

from utils import english\_tokenizer\_load

from utils import chinese\_tokenizer\_load

import config

DEVICE = config.device

def subsequent\_mask(size):

"""Mask out subsequent positions."""

\# 设定subsequent\_mask矩阵的shape

attn\_shape = (1, size, size)

\# 生成一个右上角(不含主对角线)为全1，左下角(含主对角线)为全0的subsequent\_mask矩阵

subsequent\_mask = np.triu(np.ones(attn\_shape), k=1).astype('uint8')

\# 返回一个右上角(不含主对角线)为全False，左下角(含主对角线)为全True的subsequent\_mask矩阵

return torch.from\_numpy(subsequent\_mask) == 0

class Batch:

"""Object for holding a batch of data with mask during training."""

def \_\_init\_\_(self, src\_text, trg\_text, src, trg=None, pad=0):

self.src\_text = src\_text

self.trg\_text = trg\_text

src = src.to(DEVICE)

self.src = src

\# 对于当前输入的句子非空部分进行判断成bool序列

\# 并在seq length前面增加一维，形成维度为 1×seq length 的矩阵

self.src\_mask = (src!= pad).unsqueeze(-2)

\# 如果输出目标不为空，则需要对decoder要使用到的target句子进行mask

if trg is not None:

trg = trg.to(DEVICE)

\# decoder要用到的target输入部分

self.trg = trg\[:,:-1\]

\# decoder训练时应预测输出的target结果

self.trg\_y = trg\[:, 1:\]

\# 将target输入部分进行attention mask

self.trg\_mask = self.make\_std\_mask(self.trg, pad)

\# 将应输出的target结果中实际的词数进行统计

self.ntokens = (self.trg\_y!= pad).data.sum()

\# Mask掩码操作

@staticmethod

def make\_std\_mask(tgt, pad):

"""Create a mask to hide padding and future words."""

tgt\_mask = (tgt!= pad).unsqueeze(-2)

tgt\_mask = tgt\_mask & Variable(subsequent\_mask(tgt.size(-1)).type\_as(tgt\_mask.data))

return tgt\_mask

class MTDataset(Dataset):

def \_\_init\_\_(self, data\_path):

self.out\_en\_sent, self.out\_cn\_sent = self.get\_dataset(data\_path, sort=True)

self.sp\_eng = english\_tokenizer\_load()

self.sp\_chn = chinese\_tokenizer\_load()

self.PAD = self.sp\_eng.pad\_id() # 0

self.BOS = self.sp\_eng.bos\_id() # 2

self.EOS = self.sp\_eng.eos\_id() # 3

@staticmethod

def len\_argsort(seq):

"""传入一系列句子数据(分好词的列表形式)，按照句子长度排序后，返回排序后原来各句子在数据中的索引下标"""

return sorted(range(len(seq)), key=lambda x: len(seq\[x\]))

def get\_dataset(self, data\_path, sort=False):

"""把中文和英文按照同样的顺序排序, 以英文句子长度排序的(句子下标)顺序为基准"""

dataset = json.load(open(data\_path, 'r'))

out\_en\_sent = \[\]

out\_cn\_sent = \[\]

for idx, \_ in enumerate(dataset):

out\_en\_sent.append(dataset\[idx\]\[0\])

out\_cn\_sent.append(dataset\[idx\]\[1\])

if sort:

sorted\_index = self.len\_argsort(out\_en\_sent)

out\_en\_sent = \[out\_en\_sent\[i\] for i in sorted\_index\]

out\_cn\_sent = \[out\_cn\_sent\[i\] for i in sorted\_index\]

return out\_en\_sent, out\_cn\_sent

def \_\_getitem\_\_(self, idx):

eng\_text = self.out\_en\_sent\[idx\]

chn\_text = self.out\_cn\_sent\[idx\]

return \[eng\_text, chn\_text\]

def \_\_len\_\_(self):

return len(self.out\_en\_sent)

def collate\_fn(self, batch):

src\_text = \[x\[0\] for x in batch\]

tgt\_text = \[x\[1\] for x in batch\]

src\_tokens = \[\[self.BOS\] + self.sp\_eng.EncodeAsIds(sent) + \[self.EOS\] for sent in src\_text\]

tgt\_tokens = \[\[self.BOS\] + self.sp\_chn.EncodeAsIds(sent) + \[self.EOS\] for sent in tgt\_text\]

batch\_input = pad\_sequence(\[torch.LongTensor(np.array(l\_)) for l\_ in src\_tokens\],

batch\_first=True, padding\_value=self.PAD)

batch\_target = pad\_sequence(\[torch.LongTensor(np.array(l\_)) for l\_ in tgt\_tokens\],

batch\_first=True, padding\_value=self.PAD)

return Batch(src\_text, tgt\_text, batch\_input, batch\_target, self.PAD)