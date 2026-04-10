---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: 'About Code release for "Autoformer: Decomposition Transformers with
  Auto-Correlation for Long-Term Series Forecasting" (NeurIPS 2021), https://arxiv.org/abs/2106.13008
  - Autoformer/exp/exp_main.py at main · thuml/Autoformer'
published: null
source: https://github.com/thuml/Autoformer/blob/main/exp/exp_main.py#L241
source_type: web
status: inbox
tags:
- null
- clippings
title: Autoformer/exp/exp_main.py at main
topics:
- 深度学习
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

140

141

142

143

144

145

146

147

148

149

150

151

152

153

154

155

156

157

158

159

160

161

162

163

164

165

166

167

168

169

170

171

172

173

174

175

176

177

178

179

180

181

182

183

184

185

186

187

188

189

190

191

192

193

194

195

196

197

198

199

200

201

202

203

204

205

206

207

208

209

210

211

212

213

214

215

216

217

218

219

220

221

222

223

224

225

226

227

228

229

230

231

232

233

234

235

236

237

238

239

240

241

242

243

244

245

246

247

248

249

250

251

252

253

254

255

256

257

258

259

260

261

262

263

264

265

266

267

268

269

270

271

272

273

274

275

import logging

logging.basicConfig(format='%(asctime)s,%(msecs)03d %(levelname)-8s \[%(filename)s:%(lineno)d\] %(message)s',

datefmt='%Y-%m-%d:%H:%M:%S',

level=logging.INFO)

from data\_provider.data\_factory import data\_provider

from exp.exp\_basic import Exp\_Basic

from models import Informer, Autoformer, Transformer, Reformer

from utils.tools import EarlyStopping, adjust\_learning\_rate, visual

from utils.metrics import metric

import numpy as np

import torch

import torch.nn as nn

from torch import optim

import os

import time

import warnings

import numpy as np

warnings.filterwarnings('ignore')

class Exp\_Main(Exp\_Basic):

def \_\_init\_\_(self, args):

super(Exp\_Main, self).\_\_init\_\_(args)

def \_build\_model(self):

model\_dict = {

'Autoformer': Autoformer,

'Transformer': Transformer,

'Informer': Informer,

'Reformer': Reformer,

}

model = model\_dict\[self.args.model\].Model(self.args).float()

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

def \_predict(self, batch\_x, batch\_y, batch\_x\_mark, batch\_y\_mark):

\# decoder input

dec\_inp = torch.zeros\_like(batch\_y\[:, -self.args.pred\_len:,:\]).float()

dec\_inp = torch.cat(\[batch\_y\[:,:self.args.label\_len,:\], dec\_inp\], dim=1).float().to(self.device)

\# encoder - decoder

def \_run\_model():

outputs = self.model(batch\_x, batch\_x\_mark, dec\_inp, batch\_y\_mark)

if self.args.output\_attention:

outputs = outputs\[0\]

return outputs

if self.args.use\_amp:

with torch.cuda.amp.autocast():

outputs = \_run\_model()

else:

outputs = \_run\_model()

f\_dim = -1 if self.args.features == 'MS' else 0

outputs = outputs\[:, -self.args.pred\_len:, f\_dim:\]

batch\_y = batch\_y\[:, -self.args.pred\_len:, f\_dim:\].to(self.device)

return outputs, batch\_y

def vali(self, vali\_data, vali\_loader, criterion):

total\_loss = \[\]

self.model.eval()

with torch.no\_grad():

for i, (batch\_x, batch\_y, batch\_x\_mark, batch\_y\_mark) in enumerate(vali\_loader):

batch\_x = batch\_x.float().to(self.device)

batch\_y = batch\_y.float()

batch\_x\_mark = batch\_x\_mark.float().to(self.device)

batch\_y\_mark = batch\_y\_mark.float().to(self.device)

outputs, batch\_y = self.\_predict(batch\_x, batch\_y, batch\_x\_mark, batch\_y\_mark)

pred = outputs.detach().cpu()

true = batch\_y.detach().cpu()

loss = criterion(pred, true)

total\_loss.append(loss)

total\_loss = np.average(total\_loss)

self.model.train()

return total\_loss

def train(self, setting):

train\_data, train\_loader = self.\_get\_data(flag='train')

vali\_data, vali\_loader = self.\_get\_data(flag='val')

test\_data, test\_loader = self.\_get\_data(flag='test')

path = os.path.join(self.args.checkpoints, setting)

if not os.path.exists(path):

os.makedirs(path)

time\_now = time.time()

train\_steps = len(train\_loader)

early\_stopping = EarlyStopping(patience=self.args.patience, verbose=True)

model\_optim = self.\_select\_optimizer()

criterion = self.\_select\_criterion()

if self.args.use\_amp:

scaler = torch.cuda.amp.GradScaler()

for epoch in range(self.args.train\_epochs):

iter\_count = 0

train\_loss = \[\]

self.model.train()

epoch\_time = time.time()

for i, (batch\_x, batch\_y, batch\_x\_mark, batch\_y\_mark) in enumerate(train\_loader):

iter\_count += 1

model\_optim.zero\_grad()

batch\_x = batch\_x.float().to(self.device)

batch\_y = batch\_y.float().to(self.device)

batch\_x\_mark = batch\_x\_mark.float().to(self.device)

batch\_y\_mark = batch\_y\_mark.float().to(self.device)

outputs, batch\_y = self.\_predict(batch\_x, batch\_y, batch\_x\_mark, batch\_y\_mark)

loss = criterion(outputs, batch\_y)

train\_loss.append(loss.item())

if (i + 1) % 100 == 0:

print("\\titers: {0}, epoch: {1} | loss: {2:.7f}".format(i + 1, epoch + 1, loss.item()))

speed = (time.time() - time\_now) / iter\_count

left\_time = speed \* ((self.args.train\_epochs - epoch) \* train\_steps - i)

print('\\tspeed: {:.4f}s/iter; left time: {:.4f}s'.format(speed, left\_time))

iter\_count = 0

time\_now = time.time()

if self.args.use\_amp:

scaler.scale(loss).backward()

scaler.step(model\_optim)

scaler.update()

else:

loss.backward()

model\_optim.step()

print("Epoch: {} cost time: {}".format(epoch + 1, time.time() - epoch\_time))

train\_loss = np.average(train\_loss)

vali\_loss = self.vali(vali\_data, vali\_loader, criterion)

test\_loss = self.vali(test\_data, test\_loader, criterion)

print("Epoch: {0}, Steps: {1} | Train Loss: {2:.7f} Vali Loss: {3:.7f} Test Loss: {4:.7f}".format(

epoch + 1, train\_steps, train\_loss, vali\_loss, test\_loss))

early\_stopping(vali\_loss, self.model, path)

if early\_stopping.early\_stop:

print("Early stopping")

break

adjust\_learning\_rate(model\_optim, epoch + 1, self.args)

best\_model\_path = path + '/' + 'checkpoint.pth'

self.model.load\_state\_dict(torch.load(best\_model\_path))

return

def test(self, setting, test=0):

test\_data, test\_loader = self.\_get\_data(flag='test')

if test:

print('loading model')

self.model.load\_state\_dict(torch.load(os.path.join('./checkpoints/' + setting, 'checkpoint.pth')))

preds = \[\]

trues = \[\]

folder\_path = './test\_results/' + setting + '/'

if not os.path.exists(folder\_path):

os.makedirs(folder\_path)

self.model.eval()

with torch.no\_grad():

for i, (batch\_x, batch\_y, batch\_x\_mark, batch\_y\_mark) in enumerate(test\_loader):

batch\_x = batch\_x.float().to(self.device)

batch\_y = batch\_y.float().to(self.device)

batch\_x\_mark = batch\_x\_mark.float().to(self.device)

batch\_y\_mark = batch\_y\_mark.float().to(self.device)

outputs, batch\_y = self.\_predict(batch\_x, batch\_y, batch\_x\_mark, batch\_y\_mark)

outputs = outputs.detach().cpu().numpy()

batch\_y = batch\_y.detach().cpu().numpy()

pred = outputs # outputs.detach().cpu().numpy() #.squeeze()

true = batch\_y # batch\_y.detach().cpu().numpy() #.squeeze()

preds.append(pred)

trues.append(true)

if i % 20 == 0:

input = batch\_x.detach().cpu().numpy()

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

mae, mse, rmse, mape, mspe = metric(preds, trues)

print('mse:{}, mae:{}'.format(mse, mae))

f = open("result.txt", 'a')

f.write(setting + " \\n")

f.write('mse:{}, mae:{}'.format(mse, mae))

f.write('\\n')

f.write('\\n')

f.close()

np.save(folder\_path + 'metrics.npy', np.array(\[mae, mse, rmse, mape, mspe\]))

np.save(folder\_path + 'pred.npy', preds)

np.save(folder\_path + 'true.npy', trues)

return

def predict(self, setting, load=False):

pred\_data, pred\_loader = self.\_get\_data(flag='pred')

if load:

path = os.path.join(self.args.checkpoints, setting)

best\_model\_path = path + '/' + 'checkpoint.pth'

logging.info(best\_model\_path)

self.model.load\_state\_dict(torch.load(best\_model\_path))

preds = \[\]

self.model.eval()

with torch.no\_grad():

for i, (batch\_x, batch\_y, batch\_x\_mark, batch\_y\_mark) in enumerate(pred\_loader):

batch\_x = batch\_x.float().to(self.device)

batch\_y = batch\_y.float()

batch\_x\_mark = batch\_x\_mark.float().to(self.device)

batch\_y\_mark = batch\_y\_mark.float().to(self.device)

outputs, batch\_y = self.\_predict(batch\_x, batch\_y, batch\_x\_mark, batch\_y\_mark)

pred = outputs.detach().cpu().numpy() #.squeeze()

preds.append(pred)

preds = np.array(preds)

preds = preds.reshape(-1, preds.shape\[-2\], preds.shape\[-1\])

\# result save

folder\_path = './results/' + setting + '/'

if not os.path.exists(folder\_path):

os.makedirs(folder\_path)

np.save(folder\_path + 'real\_prediction.npy', preds)

return