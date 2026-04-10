---
source_type: web
title: "Google Colab"
author: 
created_at: 2026-04-06
topics:
  - 待分类
status: inbox
source: "https://colab.research.google.com/drive/1_X7O2BkFLvqyCdZzDZvV2MB0aAvYALLC#scrollTo=928tzaA2AA2g"
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
---

Gemini

## Informer Demo

---

Gemini

---

Gemini

\[ \]

```
Cloning into 'Informer2020'...
remote: Enumerating objects: 49, done.
remote: Counting objects: 100% (49/49), done.
remote: Compressing objects: 100% (39/39), done.
remote: Total 421 (delta 15), reused 26 (delta 10), pack-reused 372
Receiving objects: 100% (421/421), 6.44 MiB | 23.89 MiB/s, done.
Resolving deltas: 100% (229/229), done.
Cloning into 'ETDataset'...
remote: Enumerating objects: 175, done.
remote: Counting objects: 100% (175/175), done.
remote: Compressing objects: 100% (172/172), done.
remote: Total 175 (delta 59), reused 14 (delta 2), pack-reused 0
Receiving objects: 100% (175/175), 3.85 MiB | 13.55 MiB/s, done.
Resolving deltas: 100% (59/59), done.
ETDataset  Informer2020  sample_data
```

---

Gemini

\[ \]

---

Gemini

\[ \]

---

Gemini

---

Gemini

\[ \]

---

Gemini

\[ \]

---

Gemini

```
1
   2
   3
   4
   5
   6
   7
args.use_gpu = True if torch.cuda.is_available() and args.use_gpu else False

if args.use_gpu and args.use_multi_gpu:
    args.devices = args.devices.replace(' ','')
    device_ids = args.devices.split(',')
    args.device_ids = [int(id_) for id_ in device_ids]
    args.gpu = args.device_ids[0]
开始借助 AI 编写或生成代码。
```

---

Gemini

```
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
# Set augments by using data name
data_parser = {
    'ETTh1':{'data':'ETTh1.csv','T':'OT','M':[7,7,7],'S':[1,1,1],'MS':[7,7,1]},
    'ETTh2':{'data':'ETTh2.csv','T':'OT','M':[7,7,7],'S':[1,1,1],'MS':[7,7,1]},
    'ETTm1':{'data':'ETTm1.csv','T':'OT','M':[7,7,7],'S':[1,1,1],'MS':[7,7,1]},
    'ETTm2':{'data':'ETTm2.csv','T':'OT','M':[7,7,7],'S':[1,1,1],'MS':[7,7,1]},
}
if args.data in data_parser.keys():
    data_info = data_parser[args.data]
    args.data_path = data_info['data']
    args.target = data_info['T']
    args.enc_in, args.dec_in, args.c_out = data_info[args.features]
开始借助 AI 编写或生成代码。
```

---

Gemini

```
1
   2
args.detail_freq = args.freq
args.freq = args.freq[-1:]
开始借助 AI 编写或生成代码。
```

---

Gemini

```
1
   2
print('Args in experiment:')
print(args)
开始借助 AI 编写或生成代码。
```

```
Args in experiment:
{'model': 'informer', 'data': 'ETTh1', 'root_path': './ETDataset/ETT-small/', 'data_path': 'ETTh1.csv', 'features': 'M', 'target': 'OT', 'freq': 'h', 'checkpoints': './informer_checkpoints', 'seq_len': 96, 'label_len': 48, 'pred_len': 24, 'enc_in': 7, 'dec_in': 7, 'c_out': 7, 'factor': 5, 'd_model': 512, 'n_heads': 8, 'e_layers': 2, 'd_layers': 1, 'd_ff': 2048, 'dropout': 0.05, 'attn': 'prob', 'embed': 'timeF', 'activation': 'gelu', 'distil': True, 'output_attention': False, 'batch_size': 32, 'learning_rate': 0.0001, 'loss': 'mse', 'lradj': 'type1', 'use_amp': False, 'num_workers': 0, 'itr': 1, 'train_epochs': 6, 'patience': 3, 'des': 'exp', 'use_gpu': True, 'gpu': 0, 'use_multi_gpu': False, 'devices': '0,1,2,3', 'detail_freq': 'h'}
```

---

Gemini

<<<<<<< HEAD
```
1
Exp = Exp_Informer
开始借助 AI 编写或生成代码。
```

---

Gemini

\[ \]

```
Use GPU: cuda:0
>>>>>>>start training : informer_ETTh1_ftM_sl96_ll48_pl24_dm512_nh8_el2_dl1_df2048_atprob_fc5_ebtimeF_dtTrue_exp_0>>>>>>>>>>>>>>>>>>>>>>>>>>
train 8521
val 2857
test 2857
    iters: 100, epoch: 1 | loss: 0.3484939
    speed: 0.0800s/iter; left time: 119.7995s
    iters: 200, epoch: 1 | loss: 0.3274963
    speed: 0.0773s/iter; left time: 108.0117s
Epoch: 1 cost time: 20.9348361492157
Epoch: 1, Steps: 266 | Train Loss: 0.3885468 Vali Loss: 0.6522534 Test Loss: 0.6147651
Validation loss decreased (inf --> 0.652253).  Saving model ...
Updating learning rate to 0.0001
    iters: 100, epoch: 2 | loss: 0.2812596
    speed: 0.1925s/iter; left time: 236.9607s
    iters: 200, epoch: 2 | loss: 0.2148246
    speed: 0.0797s/iter; left time: 90.1093s
Epoch: 2 cost time: 21.145679235458374
Epoch: 2, Steps: 266 | Train Loss: 0.2568903 Vali Loss: 0.6256742 Test Loss: 0.5904896
Validation loss decreased (0.652253 --> 0.625674).  Saving model ...
Updating learning rate to 5e-05
    iters: 100, epoch: 3 | loss: 0.2377600
    speed: 0.1962s/iter; left time: 189.2880s
    iters: 200, epoch: 3 | loss: 0.1902070
    speed: 0.0812s/iter; left time: 70.2002s
Epoch: 3 cost time: 21.539507389068604
Epoch: 3, Steps: 266 | Train Loss: 0.2063076 Vali Loss: 0.6280525 Test Loss: 0.5942183
EarlyStopping counter: 1 out of 3
Updating learning rate to 2.5e-05
    iters: 100, epoch: 4 | loss: 0.1939584
    speed: 0.1975s/iter; left time: 138.0229s
    iters: 200, epoch: 4 | loss: 0.1632166
    speed: 0.0813s/iter; left time: 48.7252s
Epoch: 4 cost time: 21.655611753463745
Epoch: 4, Steps: 266 | Train Loss: 0.1804204 Vali Loss: 0.6678267 Test Loss: 0.6165376
EarlyStopping counter: 2 out of 3
Updating learning rate to 1.25e-05
    iters: 100, epoch: 5 | loss: 0.1675630
    speed: 0.1995s/iter; left time: 86.3623s
    iters: 200, epoch: 5 | loss: 0.1715067
    speed: 0.0826s/iter; left time: 27.5224s
Epoch: 5 cost time: 21.931761741638184
Epoch: 5, Steps: 266 | Train Loss: 0.1663280 Vali Loss: 0.6778610 Test Loss: 0.6354805
EarlyStopping counter: 3 out of 3
Early stopping
>>>>>>>testing : informer_ETTh1_ftM_sl96_ll48_pl24_dm512_nh8_el2_dl1_df2048_atprob_fc5_ebtimeF_dtTrue_exp_0<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
test 2857
test shape: (89, 32, 24, 7) (89, 32, 24, 7)
test shape: (2848, 24, 7) (2848, 24, 7)
mse:0.5913315415382385, mae:0.5571437478065491
```

---

Gemini

## Prediction

---

Gemini

```
1
   2
   3
   4
   5
import os

# set saved model path
setting = 'informer_ETTh1_ftM_sl96_ll48_pl24_dm512_nh8_el2_dl1_df2048_atprob_fc5_ebtimeF_dtTrue_mxTrue_exp_0'
# path = os.path.join(args.checkpoints,setting,'checkpoint.pth')
开始借助 AI 编写或生成代码。
```
=======
![[expected_input_output_1.png|The expected input and outputs during training]]

The expected input and outputs during training
>>>>>>> refs/remotes/origin/main

---

Gemini

```
1
   2
   3
   4
   5
   6
   7
# If you already have a trained model, you can set the arguments and model path, then initialize a Experiment and use it to predict
# Prediction is a sequence which is adjacent to the last date of the data, and does not exist in the data
# If you want to get more information about prediction, you can refer to code \`exp/exp_informer.py function predict()\` and \`data/data_loader.py class Dataset_Pred\`

exp = Exp(args)

exp.predict(setting, True)
开始借助 AI 编写或生成代码。
```

```
Use GPU: cuda:0
pred 1
```

---

Gemini

```
1
   2
   3
   4
   5
   6
# the prediction will be saved in ./results/{setting}/real_prediction.npy
import numpy as np

prediction = np.load('./results/'+setting+'/real_prediction.npy')

prediction.shape
开始借助 AI 编写或生成代码。
```

```
(1, 24, 7)
```

---

Gemini

---

Gemini

```
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
# here is the detailed code of function predict

def predict(exp, setting, load=False):
    pred_data, pred_loader = exp._get_data(flag='pred')
        
    if load:
        path = os.path.join(exp.args.checkpoints, setting)
        best_model_path = path+'/'+'checkpoint.pth'
        exp.model.load_state_dict(torch.load(best_model_path))

    exp.model.eval()
        
    preds = []
        
    for i, (batch_x,batch_y,batch_x_mark,batch_y_mark) in enumerate(pred_loader):
        batch_x = batch_x.float().to(exp.device)
        batch_y = batch_y.float()
        batch_x_mark = batch_x_mark.float().to(exp.device)
        batch_y_mark = batch_y_mark.float().to(exp.device)

        # decoder input
        if exp.args.padding==0:
            dec_inp = torch.zeros([batch_y.shape[0], exp.args.pred_len, batch_y.shape[-1]]).float()
        elif exp.args.padding==1:
            dec_inp = torch.ones([batch_y.shape[0], exp.args.pred_len, batch_y.shape[-1]]).float()
        else:
            dec_inp = torch.zeros([batch_y.shape[0], exp.args.pred_len, batch_y.shape[-1]]).float()
        dec_inp = torch.cat([batch_y[:,:exp.args.label_len,:], dec_inp], dim=1).float().to(exp.device)
        # encoder - decoder
        if exp.args.use_amp:
            with torch.cuda.amp.autocast():
                if exp.args.output_attention:
                    outputs = exp.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)[0]
                else:
                    outputs = exp.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
        else:
            if exp.args.output_attention:
                outputs = exp.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)[0]
            else:
                outputs = exp.model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
        f_dim = -1 if exp.args.features=='MS' else 0
        batch_y = batch_y[:,-exp.args.pred_len:,f_dim:].to(exp.device)
        
        pred = outputs.detach().cpu().numpy()#.squeeze()
        
        preds.append(pred)

    preds = np.array(preds)
    preds = preds.reshape(-1, preds.shape[-2], preds.shape[-1])
    
    # result save
    folder_path = './results/' + setting +'/'
    if not os.path.exists(folder_path):
        os.makedirs(folder_path)
    
    np.save(folder_path+'real_prediction.npy', preds)
    
    return preds

开始借助 AI 编写或生成代码。
```

---

Gemini

```
1
   2
# you can also use this prediction function to get result
prediction = predict(exp, setting, True)
开始借助 AI 编写或生成代码。
```

```
pred 1
```

---

Gemini

```
1
   2
   3
   4
   5
import matplotlib.pyplot as plt

plt.figure()
plt.plot(prediction[0,:,-1])
plt.show()
开始借助 AI 编写或生成代码。
```

---

Gemini

You can give a `root_path` and `data_path` of the data you want to forecast, and set `seq_len`, `label_len`, `pred_len` and other arguments as other Dataset. The difference is that you can set a more detailed freq such as `15min` or `3h` to generate the timestamp of prediction series.

`Dataset_Pred` only has one sample (including `encoder_input: [1, seq_len, dim]`, `decoder_token: [1, label_len, dim]`, `encoder_input_timestamp: [1, seq_len, date_dim]`, `decoder_input_timstamp: [1, label_len+pred_len, date_dim]`). It will intercept the last sequence of the given data (seq\_len data) to forecast the unseen future sequence (pred\_len data).

---

Gemini

```
1
   2
from data.data_loader import Dataset_Pred
from torch.utils.data import DataLoader
开始借助 AI 编写或生成代码。
```

---

Gemini

```
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
Data = Dataset_Pred
timeenc = 0 if args.embed!='timeF' else 1
flag = 'pred'; shuffle_flag = False; drop_last = False; batch_size = 1

freq = args.detail_freq

data_set = Data(
    root_path=args.root_path,
    data_path=args.data_path,
    flag=flag,
    size=[args.seq_len, args.label_len, args.pred_len],
    features=args.features,
    target=args.target,
    timeenc=timeenc,
    freq=freq
)
data_loader = DataLoader(
    data_set,
    batch_size=batch_size,
    shuffle=shuffle_flag,
    num_workers=args.num_workers,
    drop_last=drop_last)
开始借助 AI 编写或生成代码。
```

---

Gemini

```
1
len(data_set), len(data_loader)
开始借助 AI 编写或生成代码。
```

```
(1, 1)
```

---

Gemini

## Visualization

---

Gemini

```
1
   2
   3
   4
   5
   6
   7
   8
# When we finished exp.train(setting) and exp.test(setting), we will get a trained model and the results of test experiment
# The results of test experiment will be saved in ./results/{setting}/pred.npy (prediction of test dataset) and ./results/{setting}/true.npy (groundtruth of test dataset)

preds = np.load('./results/'+setting+'/pred.npy')
trues = np.load('./results/'+setting+'/true.npy')

# [samples, pred_len, dimensions]
preds.shape, trues.shape
开始借助 AI 编写或生成代码。
```

```
((2848, 24, 7), (2848, 24, 7))
```

---

Gemini

```
1
   2
import matplotlib.pyplot as plt
import seaborn as sns
开始借助 AI 编写或生成代码。
```

---

Gemini

```
1
   2
   3
   4
   5
   6
# draw OT prediction
plt.figure()
plt.plot(trues[0,:,-1], label='GroundTruth')
plt.plot(preds[0,:,-1], label='Prediction')
plt.legend()
plt.show()
开始借助 AI 编写或生成代码。
```

---

Gemini

```
1
   2
   3
   4
   5
   6
# draw HUFL prediction
plt.figure()
plt.plot(trues[0,:,0], label='GroundTruth')
plt.plot(preds[0,:,0], label='Prediction')
plt.legend()
plt.show()
开始借助 AI 编写或生成代码。
```

---

Gemini

```
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
from data.data_loader import Dataset_ETT_hour
from torch.utils.data import DataLoader

Data = Dataset_ETT_hour
timeenc = 0 if args.embed!='timeF' else 1
flag = 'test'; shuffle_flag = False; drop_last = True; batch_size = 1

data_set = Data(
    root_path=args.root_path,
    data_path=args.data_path,
    flag=flag,
    size=[args.seq_len, args.label_len, args.pred_len],
    features=args.features,
    timeenc=timeenc,
    freq=args.freq
)
data_loader = DataLoader(
    data_set,
    batch_size=batch_size,
    shuffle=shuffle_flag,
    num_workers=args.num_workers,
    drop_last=drop_last)
开始借助 AI 编写或生成代码。
```

---

Gemini

```
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
import os

args.output_attention = True

exp = Exp(args)

model = exp.model

setting = 'informer_ETTh1_ftM_sl96_ll48_pl24_dm512_nh8_el2_dl1_df2048_atprob_fc5_ebtimeF_dtTrue_mxTrue_exp_0'
path = os.path.join(args.checkpoints,setting,'checkpoint.pth')
model.load_state_dict(torch.load(path))
开始借助 AI 编写或生成代码。
```

```
Use GPU: cuda:0
```

```
<All keys matched successfully>
```

---

Gemini

```
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
# attention visualization
idx = 0
for i, (batch_x,batch_y,batch_x_mark,batch_y_mark) in enumerate(data_loader):
    if i!=idx:
        continue
    batch_x = batch_x.float().to(exp.device)
    batch_y = batch_y.float()

    batch_x_mark = batch_x_mark.float().to(exp.device)
    batch_y_mark = batch_y_mark.float().to(exp.device)
    
    dec_inp = torch.zeros_like(batch_y[:,-args.pred_len:,:]).float()
    dec_inp = torch.cat([batch_y[:,:args.label_len,:], dec_inp], dim=1).float().to(exp.device)
    
    outputs,attn = model(batch_x, batch_x_mark, dec_inp, batch_y_mark)
开始借助 AI 编写或生成代码。
```

---

Gemini

```
1
attn[0].shape, attn[1].shape #, attn[2].shape
开始借助 AI 编写或生成代码。
```

```
(torch.Size([1, 8, 96, 96]), torch.Size([1, 8, 49, 49]))
```

---

Gemini

```
1
   2
   3
   4
   5
   6
   7
   8
layer = 0
distil = 'Distil' if args.distil else 'NoDistil'
for h in range(0,8):
    plt.figure(figsize=[10,8])
    plt.title('Informer, {}, attn:{} layer:{} head:{}'.format(distil, args.attn, layer, h))
    A = attn[layer][0,h].detach().cpu().numpy()
    ax = sns.heatmap(A, vmin=0, vmax=A.max()+0.01)
    plt.show()
开始借助 AI 编写或生成代码。
```

---

Gemini

```
1
   2
   3
   4
   5
   6
   7
   8
layer = 1
distil = 'Distil' if args.distil else 'NoDistil'
for h in range(0,8):
    plt.figure(figsize=[10,8])
    plt.title('Informer, {}, attn:{} layer:{} head:{}'.format(distil, args.attn, layer, h))
    A = attn[layer][0,h].detach().cpu().numpy()
    ax = sns.heatmap(A, vmin=0, vmax=A.max()+0.01)
    plt.show()
开始借助 AI 编写或生成代码。
```

---

Gemini

## Custom Data

Custom data (xxx.csv) has to include at least 2 features: `date` (format: `YYYY-MM-DD hh:mm:ss`) and `target feature`.

---

Gemini

```
1
   2
   3
   4
from data.data_loader import Dataset_Custom
from torch.utils.data import DataLoader
import pandas as pd
import os
开始借助 AI 编写或生成代码。
```

---

Gemini

```
1
   2
   3
   4
   5
   6
   7
   8
# custom data: xxx.csv
# data features: ['date', ...(other features), target feature]

# we take ETTh2 as an example
args.root_path = './ETDataset/ETT-small/'
args.data_path = 'ETTh2.csv'

df = pd.read_csv(os.path.join(args.root_path, args.data_path))
开始借助 AI 编写或生成代码。
```

---

Gemini

```
1
df.head()
开始借助 AI 编写或生成代码。
```

---

Gemini

```
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
'''
We set 'HULL' as target instead of 'OT'

The following frequencies are supported:
        Y   - yearly
            alias: A
        M   - monthly
        W   - weekly
        D   - daily
        B   - business days
        H   - hourly
        T   - minutely
            alias: min
        S   - secondly
'''

args.target = 'HULL'
args.freq = 'h'

Data = Dataset_Custom
timeenc = 0 if args.embed!='timeF' else 1
flag = 'test'; shuffle_flag = False; drop_last = True; batch_size = 1

data_set = Data(
    root_path=args.root_path,
    data_path=args.data_path,
    flag=flag,
    size=[args.seq_len, args.label_len, args.pred_len],
    features=args.features,
    timeenc=timeenc,
    target=args.target, # HULL here
    freq=args.freq # 'h': hourly, 't':minutely
)
data_loader = DataLoader(
    data_set,
    batch_size=batch_size,
    shuffle=shuffle_flag,
    num_workers=args.num_workers,
    drop_last=drop_last)
开始借助 AI 编写或生成代码。
```

---

Gemini

```
1
batch_x,batch_y,batch_x_mark,batch_y_mark = data_set[0]
开始借助 AI 编写或生成代码。
```

---

Gemini

```
1

开始借助 AI 编写或生成代码。
```
