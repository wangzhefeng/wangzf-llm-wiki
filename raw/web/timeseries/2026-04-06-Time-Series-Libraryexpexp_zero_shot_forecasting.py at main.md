---
source_type: web
title: "Time-Series-Library/exp/exp_zero_shot_forecasting.py at main"
author: 
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
published: 
created: 2026-04-06
description: "A Library for Advanced Deep Time Series Models for General Time Series Analysis. - Time-Series-Library/exp/exp_zero_shot_forecasting.py at main · thuml/Time-Series-Library"
tags:
  - 
  - "clippings"
source_url: "https://github.com/thuml/Time-Series-Library/blob/main/exp/exp_zero_shot_forecasting.py"
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

106

107

108

109

110

111

112

113

114

115

116

117

118

119

120

121

122

123

124

125

126

127

128

129

130

131

132

133

134

135

136

137

138

139

from data\_provider.data\_factory import data\_provider

from exp.exp\_basic import Exp\_Basic

from utils.tools import EarlyStopping, adjust\_learning\_rate, visual

from utils.metrics import metric

import torch

import torch.nn as nn

from torch import optim

import os

import time

import warnings

import numpy as np

from utils.dtw\_metric import dtw, accelerated\_dtw

from utils.augmentation import run\_augmentation, run\_augmentation\_single

warnings.filterwarnings('ignore')

class Exp\_Zero\_Shot\_Forecast(Exp\_Basic):

def \_\_init\_\_(self, args):

super(Exp\_Zero\_Shot\_Forecast, self).\_\_init\_\_(args)

def \_build\_model(self):

model = self.model\_dict\[self.args.model\](self.args).float()

if self.args.use\_multi\_gpu and self.args.use\_gpu:

model = nn.DataParallel(model, device\_ids=self.args.device\_ids)

return model

def \_get\_data(self, flag):

data\_set, data\_loader = data\_provider(self.args, flag)

return data\_set, data\_loader

def \_select\_optimizer(self):

model\_optim = optim.Adam(self.model.parameters(), lr=self.args.learning\_rate)

return model\_optim

def \_select\_criterion(self):

criterion = nn.MSELoss()

return criterion

def test(self, setting, test=0):

test\_data, test\_loader = self.\_get\_data(flag='test')

preds = \[\]

trues = \[\]

folder\_path = './test\_results/' + setting + '/'

if not os.path.exists(folder\_path):

os.makedirs(folder\_path)

self.model.eval()

with torch.no\_grad():

for i, (batch\_x, batch\_y, batch\_x\_mark, batch\_y\_mark) in enumerate(test\_loader):

\# start\_time = time.time()

batch\_x = batch\_x.float().to(self.device)

batch\_y = batch\_y.float().to(self.device)

batch\_x\_mark = batch\_x\_mark.float().to(self.device)

batch\_y\_mark = batch\_y\_mark.float().to(self.device)

\# decoder input

dec\_inp = torch.zeros\_like(batch\_y\[:, -self.args.pred\_len:,:\]).float()

dec\_inp = torch.cat(\[batch\_y\[:,:self.args.label\_len,:\], dec\_inp\], dim=1).float().to(self.device)

\# encoder - decoder

if self.args.use\_amp:

with torch.cuda.amp.autocast():

outputs = self.model(batch\_x, batch\_x\_mark, dec\_inp, batch\_y\_mark)

else:

outputs = self.model(batch\_x, batch\_x\_mark, dec\_inp, batch\_y\_mark)

\# print("Test cost time: {}".format(time.time() - start\_time))

f\_dim = -1 if self.args.features == 'MS' else 0

outputs = outputs\[:, -self.args.pred\_len:,:\]

batch\_y = batch\_y\[:, -self.args.pred\_len:,:\].to(self.device)

outputs = outputs.detach().cpu().numpy()

batch\_y = batch\_y.detach().cpu().numpy()

if test\_data.scale and self.args.inverse:

shape = batch\_y.shape

if outputs.shape\[-1\]!= batch\_y.shape\[-1\]:

outputs = np.tile(outputs, \[1, 1, int(batch\_y.shape\[-1\] / outputs.shape\[-1\])\])

outputs = test\_data.inverse\_transform(outputs.reshape(shape\[0\] \* shape\[1\], -1)).reshape(shape)

batch\_y = test\_data.inverse\_transform(batch\_y.reshape(shape\[0\] \* shape\[1\], -1)).reshape(shape)

outputs = outputs\[:,:, f\_dim:\]

batch\_y = batch\_y\[:,:, f\_dim:\]

pred = outputs

true = batch\_y

preds.append(pred)

trues.append(true)

if i % 20 == 0:

input = batch\_x.detach().cpu().numpy()

if test\_data.scale and self.args.inverse:

shape = input.shape

input = test\_data.inverse\_transform(input.reshape(shape\[0\] \* shape\[1\], -1)).reshape(shape)

gt = np.concatenate((input\[0,:, -1\], true\[0,:, -1\]), axis=0)

pd = np.concatenate((input\[0,:, -1\], pred\[0,:, -1\]), axis=0)

visual(gt, pd, os.path.join(folder\_path, str(i) + '.pdf'))

preds = np.concatenate(preds, axis=0)

trues = np.concatenate(trues, axis=0)

print('test shape:', preds.shape, trues.shape)

preds = preds.reshape(-1, preds.shape\[-2\], preds.shape\[-1\])

trues = trues.reshape(-1, trues.shape\[-2\], trues.shape\[-1\])

print('test shape:', preds.shape, trues.shape)

\# result save

folder\_path = './results/' + setting + '/'

if not os.path.exists(folder\_path):

os.makedirs(folder\_path)

\# dtw calculation

if self.args.use\_dtw:

dtw\_list = \[\]

manhattan\_distance = lambda x, y: np.abs(x - y)

for i in range(preds.shape\[0\]):

x = preds\[i\].reshape(-1, 1)

y = trues\[i\].reshape(-1, 1)

if i % 100 == 0:

print("calculating dtw iter:", i)

d, \_, \_, \_ = accelerated\_dtw(x, y, dist=manhattan\_distance)

dtw\_list.append(d)

dtw = np.array(dtw\_list).mean()

else:

dtw = 'Not calculated'

mae, mse, rmse, mape, mspe = metric(preds, trues)

print('mse:{}, mae:{}, dtw:{}'.format(mse, mae, dtw))

f = open("result\_zero\_shot\_forecast\_search.txt", 'a')

f.write(setting + " \\n")

f.write('mse:{}, mae:{}, dtw:{}'.format(mse, mae, dtw))

f.write('\\n')

f.write('\\n')

f.close()

np.save(folder\_path + 'metrics.npy', np.array(\[mae, mse, rmse, mape, mspe\]))

np.save(folder\_path + 'pred.npy', preds)

np.save(folder\_path + 'true.npy', trues)

return