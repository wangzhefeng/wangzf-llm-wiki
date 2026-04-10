---
source_type: web
title: "lyhue1991/torchkeras: Pytorch❤️  Keras 😋😋"
author: 
created_at: 2026-04-06
topics:
  - 深度学习
status: inbox
source: "https://github.com/lyhue1991/torchkeras?tab=readme-ov-file"
published: 
created: 2026-04-06
description: "Pytorch❤️  Keras 😋😋. Contribute to lyhue1991/torchkeras development by creating an account on GitHub."
tags:
  - 
  - "clippings"
---

## 炼丹师，这是你的梦中情炉吗?🌹🌹

[English](https://github.com/lyhue1991/torchkeras/blob/master/README_en.md) | 简体中文

torchkeras 是一个通用的pytorch模型训练模版工具，按照如下目标进行设计和实现：

- **好看** (代码优雅，日志美丽，自带可视化)
- **好用** (使用方便，支持 进度条、评估指标、early-stopping等常用功能，支持tensorboard，wandb回调函数等扩展功能)
- **好改** (修改简单，核心代码模块化，仅约200行，并提供丰富的修改使用案例)

## 1，炼丹之痛 😭😭

无论是学术研究还是工业落地，pytorch几乎都是目前炼丹的首选框架。

pytorch的胜出不仅在于其简洁一致的api设计，更在于其生态中丰富和强大的模型库。

但是我们会发现不同的pytorch模型库提供的训练和验证代码非常不一样。

torchvision官方提供的范例代码主要是一个关联了非常多依赖函数的train\_one\_epoch和evaluate函数，针对检测和分割各有一套。

yolo系列的主要是支持ddp模式的各种风格迥异的Trainer，每个不同的yolo版本都会改动很多导致不同yolo版本之间都难以通用。

抱抱脸的transformers库在借鉴了pytorch\_lightning的基础上也搞了一个自己的Trainer，但与pytorch\_lightning并不兼容。

非常有名的facebook的目标检测库detectron2, 也是搞了一个它自己的Trainer，配合一个全局的cfg参数设置对象来训练模型。

还有我用的比较多的语义分割的segmentation\_models.pytorch这个库，设计了一个TrainEpoch和一个ValidEpoch来做训练和验证。

在学习和使用这些不同的pytorch模型库时，尝试阅读理解和改动这些训练和验证相关的代码让我受到了一万点伤害。

有些设计非常糟糕，嵌套了十几层，有些实现非常dirty，各种带下划线的私有变量满天飞。

让你每次想要改动一下加入一些自己想要的功能时就感到望而却步。

我不就想finetune一下模型嘛，何必拿这么多垃圾代码搞我？

## 2，梦中情炉 🤗🤗

这一切的苦不由得让我怀念起tensorflow中keras的美好了。

还记得keras那compile, fit, evalute三连击吗？一切都像行云流水般自然，真正的for humans。

而且你看任何用keras实现的模型库，训练和验证都几乎可以用这一套相同的接口，没有那么多莫名奇妙的野生Trainer。

我能否基于pytorch打造一个接口和keras一样简洁易用，功能强大，但是实现代码非常简短易懂，便于修改的模型训练工具呢？

从2020年7月左右发布1.0版本到最近发布的3.86版本，我陆陆续续在工作中一边使用一边打磨一个工具，总共提交修改了70多次。

现在我感觉我细心雕琢的这个作品终于长成了我心目中接近完美的样子。

**她有一个美丽的名字：torchkeras.**

**是的，她兼具torch的灵动，也有keras的优雅~**

**并且她的美丽，无与伦比~**

**她，就是我的梦中情炉~ 🤗🤗**

[![](https://github.com/lyhue1991/torchkeras/raw/master/data/torchkeras.png)](https://github.com/lyhue1991/torchkeras/blob/master/data/torchkeras.png)

## 3，使用方法 🍊🍊

安装torchkeras

```
pip install torchkeras
```

通过使用torchkeras，你不需要写自己的pytorch模型训练循环。你只要做这样两步就可以了。

(1) 创建你的模型结构net,然后把它和损失函数传入torchkeras.KerasModel构建一个model。

(2) 使用model的fit方法在你的训练数据和验证数据上进行训练，训练数据和验证数据需要封装成两个DataLoader.

核心使用代码就像下面这样：

```
import torch 
import torchkeras
import torchmetrics
model = torchkeras.KerasModel(net,
                              loss_fn = nn.BCEWithLogitsLoss(),
                              optimizer= torch.optim.Adam(net.parameters(),lr = 1e-4),
                              metrics_dict = {"acc":torchmetrics.Accuracy(task='binary')}
                             )
dfhistory=model.fit(train_data=dl_train, 
                    val_data=dl_val, 
                    epochs=20, 
                    patience=3, 
                    ckpt_path='checkpoint',
                    monitor="val_acc",
                    mode="max",
                    plot=True
                   )
```

在jupyter notebook中执行训练代码，你将看到类似下面的动态可视化图像和训练日志进度条。

[![](https://github.com/lyhue1991/torchkeras/raw/master/data/torchkeras_plot.gif)](https://github.com/lyhue1991/torchkeras/blob/master/data/torchkeras_plot.gif)

除此之外，torchkeras还提供了一个VLog类，方便你在任意的训练逻辑中使用动态可视化图像和日志进度条。

```
import time
import math,random
from torchkeras import VLog

epochs = 10
batchs = 30

#0, 指定监控北极星指标，以及指标优化方向
vlog = VLog(epochs, monitor_metric='val_loss', monitor_mode='min') 

#1, log_start 初始化动态图表
vlog.log_start() 

for epoch in range(epochs):
    
    #train
    for step in range(batchs):
        
        #2, log_step 更新step级别日志信息，打日志，并用小进度条显示进度
        vlog.log_step({'train_loss':100-2.5*epoch+math.sin(2*step/batchs)}) 
        time.sleep(0.05)
        
    #eval    
    for step in range(20):
        
        #3, log_step 更新step级别日志信息，指定training=False说明在验证模式，只打日志不更新小进度条
        vlog.log_step({'val_loss':100-2*epoch+math.sin(2*step/batchs)},training=False)
        time.sleep(0.05)
        
    #4, log_epoch 更新epoch级别日志信息，每个epoch刷新一次动态图表和大进度条进度
    vlog.log_epoch({'val_loss':100 - 2*epoch+2*random.random()-1,
                    'train_loss':100-2.5*epoch+2*random.random()-1})  

# 5, log_end 调整坐标轴范围，输出最终指标可视化图表
vlog.log_end()
```

## 4，主要特性 🍉🍉

torchkeras 支持以下这些功能特性，稳定支持这些功能的起始版本以及这些功能借鉴或者依赖的库的来源见下表。

| 功能 | 稳定支持起始版本 | 依赖或借鉴库 |
| --- | --- | --- |
| ✅ 训练进度条 | 3.0.0 | 依赖tqdm,借鉴keras |
| ✅ 训练评估指标 | 3.0.0 | 借鉴pytorch\_lightning |
| ✅ notebook中训练自带可视化 | 3.8.0 | 借鉴fastai |
| ✅ early stopping | 3.0.0 | 借鉴keras |
| ✅ gpu training | 3.0.0 | 依赖accelerate |
| ✅ multi-gpus training(ddp) | 3.6.0 | 依赖accelerate |
| ✅ fp16/bf16 training | 3.6.0 | 依赖accelerate |
| ✅ tensorboard callback | 3.7.0 | 依赖tensorboard |
| ✅ wandb callback | 3.7.0 | 依赖wandb |
| ✅ VLog | 3.9.5 | 依赖matplotlib |

## 5，基本范例 🌰🌰

以下范例是torchkeras的基础范例，演示了torchkeras的主要功能。

包括基础训练，使用wandb可视化，使用wandb调参，使用tensorboard可视化，使用多GPU的ddp模式训练，通用的VLog动态日志可视化等。

| example | notebook | kaggle链接 |
| --- | --- | --- |
| ①基础范例 🔥🔥 | [**basic example**](https://github.com/lyhue1991/torchkeras/blob/master/01%EF%BC%8Ckerasmodel_example.ipynb) |  |
| ②wandb可视化 🔥🔥🔥 | [**wandb demo**](https://github.com/lyhue1991/torchkeras/blob/master/02%EF%BC%8Ckerasmodel_wandb_demo.ipynb) |  |
| ③wandb自动化调参🔥🔥 | [**wandb sweep demo**](https://github.com/lyhue1991/torchkeras/blob/master/03%EF%BC%8Ckerasmodel_tuning_demo.ipynb) |  |
| ④tensorboard可视化 | [**tensorboard example**](https://github.com/lyhue1991/torchkeras/blob/master/04%EF%BC%8Ckerasmodel_tensorboard_demo.ipynb) |  |
| ⑤ddp/tpu训练范例 | [**ddp tpu examples**](https://www.kaggle.com/code/lyhue1991/torchkeras-ddp-tpu-examples) |  |
| ⑥VLog动态日志可视化范例🔥🔥🔥 | [**VLog example**](https://github.com/lyhue1991/torchkeras/blob/master/10%EF%BC%8Cvlog_example.ipynb) |  |

## 6，进阶范例 🔥🔥

在炼丹实践中，遇到的数据集结构或者训练推理逻辑往往会千差万别。

例如我们可能会遇到多输入多输出结构，或者希望在训练过程中计算并打印一些特定的指标等等。

这时候炼丹师可能会倾向于使用最纯粹的pytorch编写自己的训练循环。

实际上，torchkeras提供了极致的灵活性来让炼丹师掌控训练过程的每个细节。

从这个意义上说，torchkeras更像是一个训练代码模版。

这个模版由低到高由StepRunner，EpochRunner 和 KerasModel 三个类组成。

在绝大多数场景下，用户只需要在StepRunner上稍作修改并覆盖掉，就可以实现自己想要的训练推理逻辑。

就像下面这段代码范例，这是一个多输入的例子，并且嵌入了特定的accuracy计算逻辑。

这段代码的完整范例，见examples下的CRNN\_CTC验证码识别。

```
import torch.nn.functional as F 
from torchkeras import KerasModel
from accelerate import Accelerator

#我们覆盖KerasModel的StepRunner以实现自定义训练逻辑。
#注意这里把acc指标的结果写在了step_losses中以便和loss一样在Epoch上求平均，这是一个非常灵活而且有用的写法。

class StepRunner:
    def __init__(self, net, loss_fn, accelerator=None, stage = "train", metrics_dict = None, 
                 optimizer = None, lr_scheduler = None
                 ):
        self.net,self.loss_fn,self.metrics_dict,self.stage = net,loss_fn,metrics_dict,stage
        self.optimizer,self.lr_scheduler = optimizer,lr_scheduler
        self.accelerator = accelerator if accelerator is not None else Accelerator()
        if self.stage=='train':
            self.net.train() 
        else:
            self.net.eval()
    
    def __call__(self, batch):
        
        images, targets, input_lengths, target_lengths = batch
        
        #loss
        preds = self.net(images)
        preds_log_softmax = F.log_softmax(preds, dim=-1)
        loss = F.ctc_loss(preds_log_softmax, targets, input_lengths, target_lengths)
        acc = eval_acc(targets,preds)
            

        #backward()
        if self.optimizer is not None and self.stage=="train":
            self.accelerator.backward(loss)
            self.optimizer.step()
            if self.lr_scheduler is not None:
                self.lr_scheduler.step()
            self.optimizer.zero_grad()
            
            
        all_loss = self.accelerator.gather(loss).sum()
        
        #losses （or plain metric that can be averaged）
        step_losses = {self.stage+"_loss":all_loss.item(),
                       self.stage+'_acc':acc}
        
        #metrics (stateful metric)
        step_metrics = {}
        if self.stage=="train":
            if self.optimizer is not None:
                step_metrics['lr'] = self.optimizer.state_dict()['param_groups'][0]['lr']
            else:
                step_metrics['lr'] = 0.0
        return step_losses,step_metrics
    
#覆盖掉默认StepRunner 
KerasModel.StepRunner = StepRunner
```

可以看到，这种修改实际上是非常简单并且灵活的，保持每个模块的输出与原始实现格式一致就行，中间处理逻辑根据需要灵活调整。

同理，用户也可以修改并覆盖EpochRunner来实现自己的特定逻辑，但我一般很少遇到有这样需求的场景。

examples目录下的范例库包括了使用torchkeras对一些非常常用的库中的模型进行训练的例子。

例如：

- torchvision
- transformers
- segmentation\_models\_pytorch
- ultralytics
- timm

> 如果你想掌握一个东西，那么就去使用它，如果你想真正理解一个东西，那么尝试去改变它。 ———— 爱因斯坦

| example | 使用模型库 | notebook |
| --- | --- | --- |
|  |  |  |
| **RL** |  |  |
| 强化学习——Q-Learning 🔥🔥 | \- | [Q-learning](https://github.com/lyhue1991/torchkeras/blob/master/examples/Q-learning.ipynb) |
| 强化学习——DQN | \- | [DQN](https://github.com/lyhue1991/torchkeras/blob/master/examples/DQN.ipynb) |
|  |  |  |
| **Tabular** |  |  |
| 二分类——LightGBM | \- | [LightGBM](https://github.com/lyhue1991/torchkeras/blob/master/examples/LightGBM%E4%BA%8C%E5%88%86%E7%B1%BB.ipynb) |
| 多分类——Tabm🔥🔥🔥🔥🔥 | \- | [Tabm](https://github.com/lyhue1991/torchkeras/blob/master/examples/Tabm%E5%A4%9A%E5%88%86%E7%B1%BB.ipynb) |
| 多分类——FTTransformer🔥🔥 | \- | [FTTransformer](https://github.com/lyhue1991/torchkeras/blob/master/examples/FTTransformer%E5%A4%9A%E5%88%86%E7%B1%BB.ipynb) |
| 二分类——FM | \- | [FM](https://github.com/lyhue1991/torchkeras/blob/master/examples/FM%E4%BA%8C%E5%88%86%E7%B1%BB.ipynb) |
| 二分类——DeepFM | \- | [DeepFM](https://github.com/lyhue1991/torchkeras/blob/master/examples/DeepFM%E4%BA%8C%E5%88%86%E7%B1%BB.ipynb) |
| 二分类——DeepCross | \- | [DeepCross](https://github.com/lyhue1991/torchkeras/blob/master/examples/DeepCross%E4%BA%8C%E5%88%86%E7%B1%BB.ipynb) |
|  |  |  |
| **CV** |  |  |
| 图片分类——Resnet | \- | [Resnet](https://github.com/lyhue1991/torchkeras/blob/master/examples/ResNet.ipynb) |
| 语义分割——UNet | \- | [UNet](https://github.com/lyhue1991/torchkeras/blob/master/examples/UNet.ipynb) |
| 目标检测——SSD | \- | [SSD](https://github.com/lyhue1991/torchkeras/blob/master/examples/SSD.ipynb) |
| 文字识别——CRNN 🔥🔥 | \- | [CRNN-CTC](https://github.com/lyhue1991/torchkeras/blob/master/examples/CRNN_CTC.ipynb) |
| 目标检测——FasterRCNN | torchvision | [FasterRCNN](https://github.com/lyhue1991/torchkeras/blob/master/examples/FasterRCNN%E2%80%94%E2%80%94vision.ipynb) |
| 语义分割——DeepLabV3++ | segmentation\_models\_pytorch | [Deeplabv3++](https://github.com/lyhue1991/torchkeras/blob/master/examples/Deeplabv3plus%E2%80%94%E2%80%94smp.ipynb) |
| 实例分割——MaskRCNN | detectron2 | [MaskRCNN](https://github.com/lyhue1991/torchkeras/blob/master/examples/MaskRCNN%E2%80%94%E2%80%94detectron2.ipynb) |
| 图片分类——SwinTransformer | timm | [Swin](https://github.com/lyhue1991/torchkeras/blob/master/examples/SwinTransformer%E2%80%94%E2%80%94timm.ipynb) |
| 目标检测——YOLOv8 🔥🔥🔥 | ultralytics | [YOLOv8\_Detect](https://github.com/lyhue1991/torchkeras/blob/master/examples/YOLOV8_Detect%E2%80%94%E2%80%94ultralytics.ipynb) |
| 实例分割——YOLOv8 🔥🔥🔥 | ultralytics | [YOLOv8\_Segment](https://github.com/lyhue1991/torchkeras/blob/master/examples/YOLOV8_Segment%E2%80%94%E2%80%94ultralytics.ipynb) |
|  |  |  |
| **NLP** |  |  |
| 序列翻译——Transformer🔥🔥 | \- | [Transformer](https://github.com/lyhue1991/torchkeras/blob/master/examples/Dive_into_Transformer.ipynb) |
| 文本生成——Llama🔥 | \- | [Llama](https://github.com/lyhue1991/torchkeras/blob/master/examples/Dive_into_Llama.ipynb) |
| 文本分类——BERT | transformers | [BERT](https://github.com/lyhue1991/torchkeras/blob/master/examples/BERT%E2%80%94%E2%80%94transformers.ipynb) |
| 命名实体识别——BERT | transformers | [BERT\_NER](https://github.com/lyhue1991/torchkeras/blob/master/examples/BERT_NER%E2%80%94%E2%80%94transformers.ipynb) |
| LLM微调——ChatGLM2\_LoRA 🔥🔥🔥 | transformers | [ChatGLM2\_LoRA](https://github.com/lyhue1991/torchkeras/blob/master/examples/ChatGLM2_LoRA%E2%80%94%E2%80%94transformers.ipynb) |
| LLM微调——ChatGLM2\_AdaLoRA 🔥 | transformers | [ChatGLM2\_AdaLoRA](https://github.com/lyhue1991/torchkeras/blob/master/examples/ChatGLM2_AdaLoRA%E2%80%94%E2%80%94transformers.ipynb) |
| LLM微调——ChatGLM2\_QLoRA | transformers | [ChatGLM2\_QLoRA\_Kaggle](https://github.com/lyhue1991/torchkeras/blob/master/examples/ChatGLM2_QLoRA_Kaggle%E2%80%94%E2%80%94transformers.ipynb) |
| LLM微调——BaiChuan13B\_QLoRA | transformers | [BaiChuan13B\_QLoRA](https://github.com/lyhue1991/torchkeras/blob/master/examples/BaiChuan13B_QLoRA%E2%80%94%E2%80%94transformers.ipynb) |
| LLM微调——BaiChuan13B\_NER 🔥🔥🔥 | transformers | [BaiChuan13B\_NER](https://github.com/lyhue1991/torchkeras/blob/master/examples/BaiChuan13B_NER%E2%80%94%E2%80%94transformers.ipynb) |
| LLM微调——BaiChuan13B\_MultiRounds 🔥 | transformers | [BaiChuan13B\_MultiRounds](https://github.com/lyhue1991/torchkeras/blob/master/examples/BaiChuan13B_MultiRounds%E2%80%94%E2%80%94transformers.ipynb) |
| LLM微调——Qwen7B\_MultiRounds 🔥🔥🔥 | transformers | [Qwen7B\_MultiRounds](https://github.com/lyhue1991/torchkeras/blob/master/examples/Qwen7B_MultiRounds%E2%80%94%E2%80%94transformers.ipynb) |
| LLM微调——BaiChuan2\_13B 🔥 | transformers | [BaiChuan2\_13B](https://github.com/lyhue1991/torchkeras/blob/master/examples/BaiChuan2_13B%E2%80%94%E2%80%94transformers.ipynb) |

## 7，鼓励和联系作者 🎈🎈

**如果本项目对你有所帮助，想鼓励一下作者，记得给本项目加一颗星星star⭐️，并分享给你的朋友们喔😊!**

如果在torchkeras的使用中遇到问题，可以在项目中提交issue。

如果想要获得更快的反馈或者与其他torchkeras用户小伙伴进行交流，

可以在公众号算法美食屋后台回复关键字： **加群** 。

[![](https://camo.githubusercontent.com/8a1eddc026bbe8dde0eae725581ee97bfd9e9b20d3bce822f1a9d823f8856a71/68747470733a2f2f747661312e73696e61696d672e636e2f6c617267652f65366339643234656779316834316d327a756767756a32306b303062397134362e6a7067)](https://camo.githubusercontent.com/8a1eddc026bbe8dde0eae725581ee97bfd9e9b20d3bce822f1a9d823f8856a71/68747470733a2f2f747661312e73696e61696d672e636e2f6c617267652f65366339643234656779316834316d327a756767756a32306b303062397134362e6a7067)