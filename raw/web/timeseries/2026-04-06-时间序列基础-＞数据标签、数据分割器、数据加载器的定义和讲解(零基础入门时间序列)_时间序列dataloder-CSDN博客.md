---
source_type: web
title: "时间序列基础-＞数据标签、数据分割器、数据加载器的定义和讲解(零基础入门时间序列)_时间序列dataloder-CSDN博客"
author:
  - 
  - "[[成就一亿技术人!]]"
  - "[[hope_wisdom 发出的红包]]"
created_at: 2026-04-06
topics:
  - 时间序列
status: inbox
source: "https://blog.csdn.net/java1314777/article/details/134407174"
published: 
created: 2026-04-06
description: "文章浏览阅读8.1k次，点赞75次，收藏103次。本文详细介绍了时间序列分析中标签的概念、窗口分割器的作用，以及如何构建数据加载器，包括数据预处理、窗口划分和使用PyTorchDataset与DataLoader。重点讲解了LSTM和GRU模型在时间序列预测中的应用。"
tags:
  - 
  - "clippings"
---

![[assets/attachments/timeseries/36bced8b7be43bce9369848b0c2bd472.gif]]

## 一、本文介绍

各位小伙伴好，最近在 **发时间序列的实战案例** 中总是有一些朋友问我时间序列中的部分对数据的操作是什么含义，我进行了挺多的介绍和讲解但是问的人越来越多，所以今天在这里单独发一篇文章来单独的讲一下时间序列中对数据的处理操作和如何定义 **时间序列特有的数据加载器和对数据打上标签的操作。** **(发现最近研究时间序列的人越来越多基本上都是为了发论文，感叹大家的论文压力都好大)**

**适用对象->** **本文适合那些零基础的时间序列的学习者**

**目录**

[一、本文介绍](#t1)

[二、 时间序列中的标签](#t2)

[三、时间序列中的窗口分割器](#t3)

[四、时间序列的数据加载器](#t4)

[五、测试流程代码](#t5)

[五、总结](#t6)

---

## 二、 时间序列中的标签

在开始讲解具体的操作含义之前，我们需要明白一个问题，时间序列中的标签是什么？如果你了解过图像领域，那么你应该知道在目标检测领域的数据集中的图像会有一个标签 **(标记一个物体是猫还是狗或者是其它的物体)** ，那么我们时间序列的领域标签是什么呢？咱们预测的时候，大家都会选择预测未来多少条数据，假设我们16条数据，选择其中的6条数据为窗口大小来预测未来的2条数据，那么我们的标签就是这2条数据 **(假设我们的特征数1即你是单元预测，那么我们这16条数据会送入到模型内部进行训练，模型会输出2条数据，输出的2条数据会和我们的标签求一个损失用于反向传播)**

## 三、时间序列中的窗口分割器

在时间序列中 **特有的就是窗口分割器** ，利用一个滑动的窗口(类似于卷积操作)沿着数据的方向进行滑动从而产生用于训练时间序列的数据和标签。大家看上面的图片，我们的 **蓝色** 和 **粉色** 就是滑动的窗口，一个用于滑动 训练数据 一个用于滑动标签，最后滑动到数据的结尾。我们可以计算我们能够得到的训练数据的多少，其中数据为16条滑动窗口为6标签为2那么我们最后能够得到的训练加载器中的数据大小就为16 - ( 6 + 2 - 1) = 9，所以最后我们就能得到9个数据。

![[assets/attachments/timeseries/dcdf89ef5dba02258b8feae8a98c0867.png]]

**每一个数据的内容如下面的图片所示->**

![[assets/attachments/timeseries/7889d374f3fc8718047923526211bdcc.png]]

```cobol
import numpy as np

 

# 定义参数

total_data_points = 16  # 总数据点数

window_size = 6         # 窗口大小

predict_length = 2      # 预测长度

 

# 随机生成一个数据集

data_set = np.random.rand(total_data_points)

 

# 分割数据集的函数

def create_inout_sequences(input_data, tw, pre_len):

    # 创建时间序列数据专用的数据分割器

    inout_seq = []

    L = len(input_data)

    for i in range(L - tw):

        train_seq = input_data[i:i + tw]

        if (i + tw + pre_len) > len(input_data):

            break

        train_label = input_data[i + tw:i + tw + pre_len]

        inout_seq.append((train_seq, train_label))

    return inout_seq

 

 

# 使用函数分割数据

X = create_inout_sequences(data_set, window_size, predict_length)

 

print("Input sequences (X):")

print(X)
```

大家可以复制上面的代码进行运行来实际了解这一个过程，其中的create\_inout\_sequences就是数据分割器我自己定义的一个，运行以上的结果输出如下->

![[assets/attachments/timeseries/2c3de2f44e81768201c236322dff1c2f.png]] 可以看上面的代码输出的X就正如我们设想的一样，输出了九条数据。

## 四、时间序列的数据加载器

经过上面的数据分割器处理之后，我们得到了一个样本数为9的数据集，一般用list在外侧内部为tuple 元组 保存训练数据和标签，这样list就包含九个数据点，每个 数据点内包含一个大的元组，大的元组内包含两个小的元组一个是储存训练集一个储存标签。

```clojure
[(('训练数据'),('标签')),(('训练数据'),('标签')),(('训练数据'),('标签')),....]
```

之后我们就要用这个list来生成数据加载器了，我们一般也用下面的加载器进行定义，

```typescript
from torch.utils.data import DataLoader
```

但是用它进行定义数据加载器之前需要输入的数据格式是dataset的格式，时间序列的dataset和其它领域的不太一样， **下面我们来讲解一下->**

> **一般的数据的dataset需要两个数据的输入但是我们的数据只有一个，所以我们需要自己定义一个定义dataset的类来实现这个功能。**

```python
class TimeSeriesDataset(Dataset):

    def __init__(self, sequences):

        self.sequences = sequences

 

    def __len__(self):

        return len(self.sequences)

 

    def __getitem__(self, index):

        sequence, label = self.sequences[index]

        return torch.Tensor(sequence), torch.Tensor(label)
python运行
```

上面这个就是一个基本的Dataset的定义， 通过这个类的定义我们将数据集输入到这个类里转化为Dataset格式，再将其输入到Dataloader里就形成了一个数据加载器。

```cobol
# 创建数据集

train_dataset = TimeSeriesDataset(X)

 

# 创建 DataLoader

batch_size = 2  # 你可以根据需要调整批量大小

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=True)
```

**上面的代码就是定义一个数据加载器的方法，** 其中我们设置了batch\_size=2就是我们的批次大小， shuffle代表的含义是从我们定义的九条数据里随机的取，drop\_last代表丢掉不满足条件的数据，类似于我们的数据大部分都是6条但是最后一条数据不足6，此时如果将其输入到模型里就会报错，所以这个参数就是将其丢弃掉。

```python
if Train:

    losss = []

    lstm_model.train()  # 训练模式

    for i in range(epochs):

        start_time = time.time()  # 计算起始时间

        for seq, labels in train_loader:

            lstm_model.train()

            optimizer.zero_grad()

 

            y_pred = lstm_model(seq)

 

            single_loss = loss_function(y_pred, labels)

 

            single_loss.backward()

            optimizer.step()

            print(f'epoch: {i:3} loss: {single_loss.item():10.8f}')

        losss.append(single_loss.detach().numpy())

    torch.save(lstm_model.state_dict(), 'save_model.pth')

    print(f"模型已保存,用时:{(time.time() - start_time) / 60:.4f} min")
python运行
```

这段代码之间省略了挺多代码包括模型的定义优化器定义什么的这和本文内容无关我就不讲了， **后面会放一个完整的代码给大家测试，** 可以看到代码调用了train\_loader这就是我们前面调用的数据加载器，它会调用我们前面定义的class TimeSeriesDataset(Dataset):这个方法，从数据中随机选取一个数据进行加载，分别将训练数据赋值给seq，标签赋值给labels，其中seq会输入到模型的内部进行训练，其中的seq的维度的维度定义应该如下->

![[assets/attachments/timeseries/ad883b4471b56d56d68278663e756297.png]]

可以看到其中的维度是(2,6,1)这其中的含义是\[batch\_size，window\_size，features\]，我在来描述一下第一个维度是批次大小，第二个维度是你定义的观测窗口大小，第三个维度是你数据的维度，(本次的讲解我们用的是一维的，如果你的特征数是三个那么这里就是三)。这就是一个标准的时间序列输入三个维度。

labels维度如下，和上面的含义是一致的我就不重复了。

我们将seq输入的模型内部， **得到如下输出->**

![[assets/attachments/timeseries/03c7eaab6ac168c11a0a12cffb69475c.png]]

其和labels的形状需要一致用于损失的计算， **并用于反向传播。**

## 五、测试流程代码

下面给大家一个测试的代码， **我建议大家还是自己debug一下看下其中的具体通道数的变化情况。**

```python
import time

import numpy as np

import pandas as pd

import torch

import torch.nn as nn

from matplotlib import pyplot as plt

from sklearn.preprocessing import MinMaxScaler

from torch.utils.data import DataLoader

import torch

from torch.utils.data import Dataset

 

# 随机数种子

np.random.seed(0)

 

 

class TimeSeriesDataset(Dataset):

    def __init__(self, sequences):

        self.sequences = sequences

 

    def __len__(self):

        return len(self.sequences)

 

    def __getitem__(self, index):

        sequence, label = self.sequences[index]

        return torch.Tensor(sequence), torch.Tensor(label)

 

 

def calculate_mae(y_true, y_pred):

    # 平均绝对误差

    mae = np.mean(np.abs(y_true - y_pred))

    return mae

 

"""

数据定义部分

"""

true_data = pd.read_csv('ETTh1.csv')  # 填你自己的数据地址,自动选取你最后一列数据为特征列

 

 

target = 'OT'  # 添加你想要预测的特征列

test_size = 0.15  # 训练集和测试集的尺寸划分

train_size = 0.85  # 训练集和测试集的尺寸划分

# 预测未来数据的长度

# 观测窗口

 

# 这里加一些数据的预处理, 最后需要的格式是pd.series

true_data = np.array(true_data[target])

 

# 定义标准化优化器

1

1

 

# 训练集和测试集划分

train_data = true_data[:int(train_size * len(true_data))]

test_data = true_data[-int(test_size * len(true_data)):]

print("训练集尺寸:", len(train_data))

print("测试集尺寸:", len(test_data))

 

# 进行标准化处理

1

1

 

# 转化为深度学习模型需要的类型Tensor

train_data_normalized = torch.FloatTensor(train_data_normalized)

test_data_normalized = torch.FloatTensor(test_data_normalized)

 

 

def create_inout_sequences(input_data, tw, pre_len):

    # 创建时间序列数据专用的数据分割器

    inout_seq = []

    L = len(input_data)

    for i in range(L - tw):

        train_seq = input_data[i:i + tw]

        if (i + tw + 4) > len(input_data):

            break

        train_label = input_data[i + tw:i + tw + pre_len]

        inout_seq.append((train_seq, train_label))

    return inout_seq

 

 

# 定义训练器的的输入

train_inout_seq = create_inout_sequences(train_data_normalized, train_window, pre_len)

test_inout_seq = create_inout_sequences(test_data_normalized, train_window, pre_len)

 

# 创建数据集

train_dataset = TimeSeriesDataset(train_inout_seq)

test_dataset = TimeSeriesDataset(test_inout_seq)

 

# 创建 DataLoader

# 你可以根据需要调整批量大小

train_loader = DataLoader(train_dataset, batch_size=batch_size, shuffle=True, drop_last=True)

test_loader = DataLoader(test_dataset, batch_size=batch_size, shuffle=False, drop_last=True)

 

 

class GRU(nn.Module):

    def __init__(self, input_dim=1, hidden_dim=32, num_layers=1, output_dim=1, pre_len= 4):

        super(GRU, self).__init__()

        self.pre_len = pre_len

        self.num_layers = num_layers

        self.hidden_dim = hidden_dim

        # 替换 LSTM 为 GRU

        self.gru = nn.GRU(input_dim, hidden_dim,num_layers=num_layers, batch_first=True)

        self.fc = nn.Linear(hidden_dim, output_dim)

        self.relu = nn.ReLU()

        self.dropout = nn.Dropout(0.1)

    def forward(self, x):

        h0_gru = torch.zeros(self.num_layers, x.size(0), self.hidden_dim).to(x.device)

 

        out, _ = self.gru(x, h0_gru)

 

        out = self.dropout(out)

 

        # 取最后 pre_len 时间步的输出

        out = out[:, -self.pre_len:, :]

 

        out = self.fc(out)

        out = self.relu(out)

        return out

 

 

lstm_model = GRU(input_dim=1, output_dim=1, num_layers=2, hidden_dim=train_window, pre_len=pre_len)

loss_function = nn.MSELoss()

optimizer = torch.optim.Adam(lstm_model.parameters(), lr=0.005)

epochs = 20

Train = True  # 训练还是预测

 

if Train:

    losss = []

    lstm_model.train()  # 训练模式

    for i in range(epochs):

        start_time = time.time()  # 计算起始时间

        for seq, labels in train_loader:

            lstm_model.train()

            optimizer.zero_grad()

 

            y_pred = lstm_model(seq)

 

            single_loss = loss_function(y_pred, labels)

 

            single_loss.backward()

            optimizer.step()

            print(f'epoch: {i:3} loss: {single_loss.item():10.8f}')

        losss.append(single_loss.detach().numpy())

    torch.save(lstm_model.state_dict(), 'save_model.pth')

    print(f"模型已保存,用时:{(time.time() - start_time) / 60:.4f} min")

 

 

else:

    # 加载模型进行预测

    lstm_model.load_state_dict(torch.load('save_model.pth'))

    lstm_model.eval()  # 评估模式

    results = []

    reals = []

    losss = []

 

    for seq, labels in test_loader:

        pred = lstm_model(seq)

        mae = calculate_mae(pred.detach().numpy(), np.array(labels))  # MAE误差计算绝对值(预测值  - 真实值)

        losss.append(mae)

        for j in range(batch_size):

            for i in range(pre_len):

                reals.append(labels[j][i][0].detach().numpy())

                results.append(pred[j][i][0].detach().numpy())

 

    reals = scaler_test.inverse_transform(np.array(reals).reshape(1, -1))[0]

    results = scaler_test.inverse_transform(np.array(results).reshape(1, -1))[0]

    print("模型预测结果：", results)

    print("预测误差MAE:", losss)

 

    plt.figure()

    plt.style.use('ggplot')

 

    # 创建折线图

    plt.plot(reals, label='real', color='blue')  # 实际值

    plt.plot(results, label='forecast', color='red', linestyle='--')  # 预测值

 

    # 增强视觉效果

    plt.grid(True)

    plt.title('real vs forecast')

    plt.xlabel('time')

    plt.ylabel('value')

    plt.legend()

    plt.savefig('test——results.png')
python运行
```

## 五、总结

到此本文就都讲解完成了， **本文的内容是针对于时间序列预测的新手** ，可能不太了解时间序列的数据处理流程，最近问的人有点多大家都说不理解，所以单独开了这么一篇文章给大家讲解，内容可能很简单，全文全手打，希望能够帮助到各位~

最后分享我的其他博客给大家，可以方便大家阅读完本文进行实战(**本专栏平均质量分98分，并且免费阅读**)~

**概念理解**

[15种时间序列预测方法总结(包含多种方法代码实现)](https://blog.csdn.net/java1314777/article/details/133272874 "15种时间序列预测方法总结(包含多种方法代码实现)")

**数据分析**

****[时间序列预测中的数据分析-＞周期性、相关性、滞后性、趋势性、离群值等特性的分析方法](https://blog.csdn.net/java1314777/article/details/134237225 "时间序列预测中的数据分析-＞周期性、相关性、滞后性、趋势性、离群值等特性的分析方法")****

**机器学习——难度等级(⭐⭐)**

[时间序列预测实战(四)(Xgboost)(Python)(机器学习)图解机制原理实现时间序列预测和分类(附一键运行代码资源下载和代码讲解)](https://blog.csdn.net/java1314777/article/details/133070494 "时间序列预测实战(四)(Xgboost)(Python)(机器学习)图解机制原理实现时间序列预测和分类(附一键运行代码资源下载和代码讲解)")

**深度学习——难度等级(⭐⭐⭐⭐)**

[时间序列预测实战(五)基于Bi-LSTM横向搭配LSTM进行回归问题解决](https://blog.csdn.net/java1314777/article/details/133272806 "时间序列预测实战(五)基于Bi-LSTM横向搭配LSTM进行回归问题解决")

[时间序列预测实战(七)(TPA-LSTM)结合TPA注意力机制的LSTM实现多元预测](https://blog.csdn.net/java1314777/article/details/134228977 "时间序列预测实战(七)(TPA-LSTM)结合TPA注意力机制的LSTM实现多元预测")

[时间序列预测实战(三)(LSTM)(Python)(深度学习)时间序列预测(包括运行代码以及代码讲解)](https://blog.csdn.net/java1314777/article/details/132974960 "时间序列预测实战(三)(LSTM)(Python)(深度学习)时间序列预测(包括运行代码以及代码讲解)")

[时间序列预测实战(十一)用SCINet实现滚动预测功能(附代码+数据集+原理介绍）](https://blog.csdn.net/java1314777/article/details/134341948?spm=1001.2014.3001.5501 "时间序列预测实战(十一)用SCINet实现滚动预测功能(附代码+数据集+原理介绍）")

[时间序列预测实战(十二)DLinear模型实现滚动长期预测并可视化预测结果](https://blog.csdn.net/java1314777/article/details/134348252 "时间序列预测实战(十二)DLinear模型实现滚动长期预测并可视化预测结果")

[时间序列预测实战(十五)PyTorch实现GRU模型长期预测并可视化结果](https://blog.csdn.net/java1314777/article/details/134384548 "时间序列预测实战(十五)PyTorch实现GRU模型长期预测并可视化结果")

**Transformer——难度等级(⭐⭐⭐⭐)**

[时间序列预测模型实战案例(八)(Informer)个人数据集、详细参数、代码实战讲解](https://blog.csdn.net/java1314777/article/details/134235548 "时间序列预测模型实战案例(八)(Informer)个人数据集、详细参数、代码实战讲解")

[时间序列预测模型实战案例(一)深度学习华为MTS-Mixers模型](https://blog.csdn.net/java1314777/article/details/132881996 "时间序列预测模型实战案例(一)深度学习华为MTS-Mixers模型")

[时间序列预测实战(十三)定制化数据集FNet模型实现滚动长期预测并可视化结果](https://blog.csdn.net/java1314777/article/details/134353171 "时间序列预测实战(十三)定制化数据集FNet模型实现滚动长期预测并可视化结果")

[时间序列预测实战(十四)Transformer模型实现长期预测并可视化结果（附代码+数据集+原理介绍）](https://blog.csdn.net/java1314777/article/details/134355884 "时间序列预测实战(十四)Transformer模型实现长期预测并可视化结果（附代码+数据集+原理介绍）")

**个人创新模型——难度等级(⭐⭐⭐⭐⭐)**

[时间序列预测实战(十)(CNN-GRU-LSTM)通过堆叠CNN、GRU、LSTM实现多元预测和单元预测](https://blog.csdn.net/java1314777/article/details/134272675 "时间序列预测实战(十)(CNN-GRU-LSTM)通过堆叠CNN、GRU、LSTM实现多元预测和单元预测")

**传统的时间序列预测模型(⭐⭐)**

****[时间序列预测实战(二)(Holt-Winter)(Python)结合K-折交叉验证进行时间序列预测实现企业级预测精度(包括运行代码以及代码讲解)](https://blog.csdn.net/java1314777/article/details/132906621 "时间序列预测实战(二)(Holt-Winter)(Python)结合K-折交叉验证进行时间序列预测实现企业级预测精度(包括运行代码以及代码讲解)")****

[时间序列预测实战(六)深入理解ARIMA包括差分和相关性分析](https://blog.csdn.net/java1314777/article/details/134033087 "时间序列预测实战(六)深入理解ARIMA包括差分和相关性分析")

**融合模型——难度等级(⭐⭐⭐)**

[时间序列预测实战(九)PyTorch实现融合移动平均和LSTM-ARIMA进行长期预测](https://blog.csdn.net/java1314777/article/details/134271888 "时间序列预测实战(九)PyTorch实现融合移动平均和LSTM-ARIMA进行长期预测")

[时间序列预测实战(十六)PyTorch实现GRU-FCN模型长期预测并可视化结果](https://blog.csdn.net/java1314777/article/details/134359127 "时间序列预测实战(十六)PyTorch实现GRU-FCN模型长期预测并可视化结果")

![[assets/attachments/timeseries/d3ba088d3e531db168b497d99ff695d1.gif]]

QQ名片