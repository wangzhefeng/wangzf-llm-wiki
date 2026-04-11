---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: 'Date: 2020/11/22 Coder: CW Foreword: CW 近日在自己的机子上发现，nvcc --version 和
  nvidia-smi 显示出来的CU...'
source_type: web
status: inbox
tags:
- null
- clippings
title: 【CUDA】nvcc和nvidia-smi显示的版本不一致？
topics:
- 运维工具
source_url: https://www.jianshu.com/p/eb5335708f2a
published_at: 2020-11-22
related_concepts: []
---

*Date: 2020/11/22*

*Coder: CW*

*Foreword:*

*CW 近日在自己的机子上发现， **nvcc --version** 和 **nvidia-smi** 显示出来的CUDA版本不一致，其中前者显示的版本是10.2，而后者是11.0，但是深度学习相关的程序是能正常跑的，期间GPU也确实有在使用（通过nvidia-smi可以看出）。*

*由于个人一贯以来的“居安思危”风格，担心这种情况会埋坑，于是查阅了相关资料进行了解，正好也弥补了这部分知识的空白。本文会先解释下 nvcc --version 和 nvidia-smi 各自显示出来的版本号的意义，然后分享下多版本CUDA切换的经验，最后再补充下如何正确选择与CUDA版本匹配的Pytorch。*

---

## nvcc & nvidia-smi

**nvcc** 属于CUDA的 **编译器** ，将程序编译成可执行的二进制文件， **nvidia-smi** 全称是 **NVIDIA System Management Interface** ，是一种 **命令行实用工具** ，旨在帮助 **管理和监控NVIDIA GPU设备。**

CUDA有 **runtime api** 和 **driver api** ，两者都有对应的CUDA版本， nvcc --version 显示的就是前者对应的CUDA版本，而 nvidia-smi显示的是后者对应的CUDA版本。

用于支持driver api的必要文件由 **GPU driver installer** 安装，nvidia-smi就属于这一类API；而用于支持runtime api的必要文件是由 **CUDA Toolkit installer** 安装的。nvcc是与CUDA Toolkit一起安装的CUDA compiler-driver tool， **它只知道它自身构建时的CUDA runtime版本，并不知道安装了什么版本的GPU driver，甚至不知道是否安装了GPU driver。**

CUDA Toolkit Installer通常会集成了GPU driver Installer，如果你的CUDA均通过CUDA Tooklkit Installer来安装，那么runtime api 和 driver api的版本应该是一致的，也就是说， nvcc --version 和 nvidia-smi 显示的版本应该一样。否则，你可能使用了单独的GPU driver installer来安装GPU dirver，这样就会导致 nvidia-smi 和 nvcc --version 显示的版本不一致了。

通常， **driver api的版本能向下兼容runtime api的版本** ，即 **nvidia-smi 显示的版本大于nvcc --version 的版本通常不会出现大问题。**

---

## 多版本CUDA切换

*[多版本CUDA下载地址](https://links.jianshu.com/go?to=https%3A%2F%2Fdeveloper.nvidia.com%2Fcuda-toolkit-archive)*

进入以上链接下载指定版本的CUDA，这里以 *CUDA Toolkit 11.0 Update 1* 为例：

选择自己的操作系统、架构以及对应的安装类型。

![[raw/assets/attachments/tools/20481399-9178f92dc7724a8f.png]]

CUDA安装(i)

**安装类型建议选择 runfile 安装，使用deb的方式可能会将已安装的较新的显卡驱动替换掉。**

选择完毕后根据提示的命令进行安装。

CUDA安装(ii)

接下来会出现窗口进行一些安装选项的选择，若你本地已经有了Driver并且你不想替换掉，那么可以不选择Driver进行安装。

安装完毕后，会在 **/usr/local/** 目录下出现相应版本的cuda文件夹，我这里是 /usr/local/cuda-11.0/。在前言中提到，我 nvcc --version 的版本是10.2，现在我要将其替换为刚下载的11.0，那么可以：

1\. 编辑 **~/.bashrc** 文件

2\. 更改 **PATH** 和 **LD\_LIBRARY\_PATH** 环境变量：

> *export PATH= **/usr/local/cuda-11.0:**$PATH*
> 
> *export LD\_LIBRARY\_PATH= **/usr/local/cuda-11.0/lib64:**$LD\_LIBRARY\_PATH*

3\. 保存内容退出，使其生效： **source ~/.bashrc**

现在，使用 nvcc --version 可以看到显示的版本已经是11.0了，与 nvidia-smi 的一致。

在这种方式下，每次我想使用其它CUDA版本的runtime api时，都需要更改~/.bashrc文件，这里再介绍另一种避免更改环境变量的方式：

i). 首先确保 PATH 和 LD\_LIBRARY\_PATH 中含有 **/usr/local/cuda** 路径， **注意是/cuda而不是/cuda-xxx**

ii). 删除之前创建的软链接：rm -rf /usr/local/cuda

iii). 建立新的软链接：sudo ln -s/usr/local/cuda-10.2/ /usr/local/cuda/ （此处代表我想使用10.2版本）

这样之后，通过 nvcc --version 可以看到CUDA runtime api的版本又切换回10.2了。

---

## 如何选择与CUDA版本匹配的Pytorch

那么 nvcc --version 与 nvidia-smi 的版本不一致的情况下，有些朋友可能就会懵了：我该如何选择与CUDA版本匹配的Pytorch呢？（炼个丹也太南了吧~！）

其实，只要上去Pytorch官网瞄瞄，细心的你应该能够发现在命令中指定CUDA版本时，用的是 **cudatoolkit** ，而 nvcc --version 显示的版本就是通过CUDA Toolkit Installer在安装时决定的，因此，我们 **应该选择与 nvcc --version 对应的CUDA版本匹配的Pytorch。**

Pytorch官网页面

相对而言，nvidia-smi 显示的是driver api对应的CUDA版本，若使用了单独的GPU driver Installer来安装驱动，那么nvidia-smi显示的版本与CUDA Toolkit所安装的版本就很可能不一致了。

---

## END

许多炼丹爱好者可能都只注重花里胡哨的深度学习知识， 选择性地无视了关于硬件、GPU、计算芯片等方面的知识，这样，自己的短板就未免过于明显了。虽然不要求洋洋精通，但只要是与你从业领域相关的知识都应或多或少有所涉猎，这样做起事来才能得心应手。

另外，关于GPU与CUDA的知识可参考这篇文章 *[GPU与CUDA知识揭秘](https://links.jianshu.com/go?to=https%3A%2F%2Fbaijiahao.baidu.com%2Fs%3Fid%3D1663920145053509733%26wfr%3Dspider%26for%3Dpc%26qq-pf-to%3Dpcqq.c2c)* ，内容全面同时也叙述简洁，非常棒，感恩乐于分享知识的朋友！