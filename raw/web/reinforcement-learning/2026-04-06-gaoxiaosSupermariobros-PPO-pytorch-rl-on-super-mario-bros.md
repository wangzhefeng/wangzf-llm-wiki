---
source_type: web
title: "gaoxiaos/Supermariobros-PPO-pytorch: rl on super-mario-bros"
author: 
created_at: 2026-04-06
status: inbox
published: 
created: 2026-04-06
description: "rl on super-mario-bros. Contribute to gaoxiaos/Supermariobros-PPO-pytorch development by creating an account on GitHub."
tags:
  - 
  - "clippings"
source_url: "https://github.com/gaoxiaos/Supermariobros-PPO-pytorch"
published_at: null
related_concepts: []
topics:
  - reinforcement-learning
  - 强化学习
---

## Supermariobros-PPO-pytorch

基于超级玛丽游戏的pytorch版本强化学习实践教程

rl(ppo) course with super-mario-bros

你可以直接在jupyter notebook中开始学习（course.ipynb、course2.ipynb）

[![[raw/assets/attachments/reinforcementlearning/Image 6.gif]]](https://camo.githubusercontent.com/c78d53764db23c10f50ce2fa9b99ba9b88defa65e49bbc5580b0216141d19ceb/68747470733a2f2f696d672e616c6963646e2e636f6d2f7466732f5442316c4746476c4969656231386a535a467658586149334658612d3235342d3233362e676966)

## run the code with docker (推荐)

play with docker (ON your local computer with display),just run:

推荐使用docker直接运行，可以无需关注软件环境

```
docker run --gpus all -v /tmp/.X11-unix:/tmp/.X11-unix registry.cn-shanghai.aliyuncs.com/tcc-public/super-mario-ppo:localdisplay
```

if you want debuge the code and exec into container,command like this:

```
docker run --gpus all -it -v /tmp/.X11-unix:/tmp/.X11-unix registry.cn-shanghai.aliyuncs.com/tcc-public/super-mario-ppo:localdisplay  /bin/bash
```

train the model:

```
python ppo_lstm.py
```

test on super-mario-bros(see the video of agent):

```
python test_lstm.py
```

## run the code witch conda

```
conda create -n ppo python=3.7
conda activate ppo
```

python request:

```
torch torchvision
gym_super_mario_bros
spinup(要用源码安装：https://spinningup.openai.com/en/latest/user/installation.html)
opencv-python
```

train:

```
python ppo_lstm.py
```

test:

```
python test_lstm.py
```

## learn the course in jupyter notebook:

the notebook can be find at course.ipynb、course2.ipynb

## jion the rl Communication group,contact us:

remarks（添加请备注）：github rl

[![[raw/assets/attachments/reinforcementlearning/20201201160554.jpg]]](https://github.com/gaoxiaos/Supermariobros-PPO-pytorch/blob/master/doc/20201201160554.jpg)

## learn more in our DRL Training camp （aliyun tianchi）

you can find some ppo info on [https://tianchi.aliyun.com/specials/promotion/aicamprl](https://tianchi.aliyun.com/specials/promotion/aicamprl)