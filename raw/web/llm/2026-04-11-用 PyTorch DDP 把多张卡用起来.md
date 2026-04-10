---
title: "用 PyTorch DDP 把多张卡用起来"
source: "https://mp.weixin.qq.com/s/aFj9R2N1cq1njUjtAXGPsg?clicktime=1774689238&enterid=1774689238&scene=90&subscene=236&xtrack=1"
author:
  - "[[小溪1005]]"
published:
created: 2026-04-11
description: "嗨，周末愉快！小编以前做过一个复杂度稍高的模型，数据量比较大单卡跑起来特别特别慢，那台小编独享的机器有8张卡，就想着优化成并行化训练，训练模型也很快。"
tags:
  - "clippings"
---
原创 小溪1005 *2026年3月28日 16:53*

嗨，周末愉快！

小编以前做过一个复杂度稍高的模型，数据量比较大单卡跑起来特别特别慢，那台小编独享的机器有8张卡，就想着优化成并行化训练，训练模型也很快。

并行化训练主要是因为：

1. 显存不够；
2. 跑得太慢。

数据并行化训练 其实就是把模型复制到不同的卡上，将数据拆分分发给每张卡去计算梯度，最后把梯度合并。

今天小编就和大家一起来详细讲讲并行化训练吧。

---

**一、背景**

假设你有 8 张卡，一个 batch 有 256 条数据。数据并行的做法是把这 256 条拆成 8 份，每张卡拿 32 条，各自做前向传播和反向传播，算出本地梯度。

然后把 8张卡的梯度加起来求平均，每张卡都拿到这个平均梯度，用它来更新参数。结果是所有卡的参数始终一致，训练效果等价于用 256 条数据在单卡上跑了一步。卡数越多，等效 batch size 越大，同样的 epoch 数跑完所需时间越短。

但有一点要说清楚：数据并行解决不了 **模型太大单卡放不下** 的问题，因为每张卡都要存一份完整模型。那是模型并行要干的事，小编不会，这里不展开了。

---

\*\*二、为什么用DDP

PyTorch 有两套多卡方案，老的叫 `DataParallel` （DP），新的叫 `DistributedDataParallel` （DDP）。

DP 的问题是有一张主卡，所有梯度先汇总到主卡再分发，主卡负担重，卡间负载不均衡，而且只能单机用。

DDP 每张卡地位对等，梯度通过 NCCL 的 AllReduce 直接在卡间同步。而且 DDP 的通信和计算可以重叠，不用等反向传播全部结束才同步，而是 每算完一层的梯度 就立刻触发通信，边算边传，非常省时间。

实际项目直接用 DDP，DP 基本可以忘掉。

---

**三、最简单的 DDP 代码**

DDP 要求每张卡跑一个独立进程，用 `torchrun` 启动：

```
# train.py
import torch
import torch.nn as nn
import torch.distributed as dist
from torch.nn.parallel import DistributedDataParallel as DDP
from torch.utils.data import DataLoader, DistributedSampler

def main():

    dist.init_process_group(backend='nccl')
    
    # 每个进程对应 一张卡
    local_rank = torch.distributed.get_rank()
    torch.cuda.set_device(local_rank)
    
    # 模型放到 对应卡上，再包一层 DDP
    model = YourModel().cuda()
    model = DDP(model, device_ids=[local_rank])
    
    dataset = YourDataset()
    sampler = DistributedSampler(dataset)
    loader = DataLoader(dataset, batch_size=32, sampler=sampler)
    
    optimizer = torch.optim.Adam(model.parameters(), lr=1e-3)
    
    for epoch in range(10):
        sampler.set_epoch(epoch)  

        for inputs, labels in loader:
            inputs, labels = inputs.cuda(), labels.cuda()
            outputs = model(inputs)
            loss = nn.CrossEntropyLoss()(outputs, labels)
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
    
    dist.destroy_process_group()

if __name__ == '__main__':
    main()
```

启动命令（8 张卡）：

```
torchrun --nproc_per_node = 8 train.py
```

两个细节必须注意： `DistributedSampler` 不能省，省了每张卡会拿到一样的数据，就白费功夫了。 `sampler.set_epoch(epoch)` 每轮要调，它控制数据打乱的随机种子，不调的话每个 epoch 数据顺序完全一样。

---

**四、混合精度训练**

混合精度几乎是标配，用 float16 做前向传播，省显存又快，精度损失也可以忽略：

```
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()

for inputs, labels in loader:
    inputs, labels = inputs.cuda(), labels.cuda()
    
    with autocast():  # 前向传播用 float16
        outputs = model(inputs)
        loss = nn.CrossEntropyLoss()(outputs, labels)
    
    optimizer.zero_grad()
    scaler.scale(loss).backward()   # 梯度缩放防止 float16 下溢
    scaler.step(optimizer)
    scaler.update()
```

`GradScaler` 的作用是把 loss 放大再缩小，防止 float16 精度不够导致梯度变成 0。

---

**五、梯度累积：变相放大 batch size**

通信是 DDP 的主要开销，每次 `loss.backward()` 都会触发一次 AllReduce。

```
accumulation_steps = 8  # 每 8 个 batch 更新一次

for i, (inputs, labels) in enumerate(loader):
    inputs, labels = inputs.cuda(), labels.cuda()
    
    with autocast():
        outputs = model(inputs)
        loss = nn.CrossEntropyLoss()(outputs, labels)
        loss = loss / accumulation_steps  # 梯度要除以累积步数
    
    scaler.scale(loss).backward()
    
    if (i + 1) % accumulation_steps == 0:
        scaler.step(optimizer)
        scaler.update()
        optimizer.zero_grad()
```

8 张卡、累积 8 步，等效 batch size 是单卡原始 batch 的 64 倍，但通信次数只有原来的 1/8。

---

**模型保存和加载**

DDP 包了一层，模型的真实权重在 `model.module` 里，保存时要注意：

```
if local_rank == 0:
    torch.save(model.module.state_dict(), 'model.pth')

# 加载时正常加载，不需要 .module
model = YourModel()
model.load_state_dict(torch.load('model.pth'))
```

---

**最后**

从单卡迁移到 DDP 的改动其实不多：初始化进程组、模型包 DDP、数据加上 DistributedSampler、用 torchrun 启动。加上 AMP 和梯度累积之后，多卡的效率基本能用起来。

**微信扫一扫赞赏作者**

继续滑动看下一个

风控建模

向上滑动看下一个