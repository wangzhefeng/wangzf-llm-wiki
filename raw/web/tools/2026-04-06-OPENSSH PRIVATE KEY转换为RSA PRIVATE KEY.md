---
author:
- null
- '[[Author Pony]]'
created: 2026-04-06
created_at: 2026-04-06
description: OPENSSH PRIVATE KEY转换为RSA PRIVATE KEY使用命令 ssh-keygen -t rsa 生成ssh，默认是以新的格式生成，id_rsa的第一行变成了“BEGIN
  ...
published: null
source: https://www.mayanpeng.cn/archives/132.html
source_type: web
status: inbox
tags:
- null
- clippings
title: OPENSSH PRIVATE KEY转换为RSA PRIVATE KEY
topics:
- 运维工具
---

使用命令 `ssh-keygen -t rsa` 生成ssh，默认是以新的格式生成，id\_rsa的第一行变成了“BEGIN OPENSSH PRIVATE KEY” 而不再是“BEGIN RSA PRIVATE KEY”，这是一种新的密钥格式， 而且很多软件对这种格式的密钥都是不支持的。此时用来msyql、MongoDB，配置ssh登陆的话，可能会报 “Resource temporarily unavailable. Authentication by key (/Users/youname/.ssh/id\_rsa) failed (Error -16). (Error #35)” 提示资源不可用，这就是id\_rsa 格式不对造成的。这时候就不得不把私钥转换成RSA – PEM格式。然而 `ssh-keygen` 并不提供这种格式转换的功能。

## 解决方案

### 一、生成新的RSA-PEM格式公私密钥

使用 `ssh-keygen -m PEM -t rsa -b 4096` 来生成

- \-m 参数指定密钥的格式，PEM（也就是RSA格式）是之前使用的旧格式
- \-b：指定密钥长度；
- \-e：读取openssh的私钥或者公钥文件；
- \-C：添加注释；
- \-f：指定用来保存密钥的文件名；
- \-i：读取未加密的ssh-v2兼容的私钥/公钥文件，然后在标准输出设备上显示openssh兼容的私钥/公钥；
- \-l：显示公钥文件的指纹数据；
- \-N：提供一个新密语；
- \-P：提供（旧）密语；
- \-q：静默模式；
- \-t：指定要创建的密钥类型

### 二、转换格式

**Mac系统**

1.安装putty

```js
brew install putty
```

2.通过将密钥转换为PuTTy ppk格式然后再转换为RSA-PEM

```js
# 生成一个密钥，命名为demo做为演示示例
# 转换为ppk格式
puttygen demo -o demo.ppk
# 转换为ras-pem格式
puttygen demo.ppk -O private-openssh -o demo.pem
```

[![[raw/assets/attachments/tools/20200430-102305.png]]](https://cdn.static.ponycool.com/img/20200430-102305.png "点击放大图片")

##### 可以参考issues/3360

**Win系统**

安装putty，利用puttygen转换

1.导入OPENSSH格式密钥

[![[raw/assets/attachments/tools/20200430-105037.png]]](https://cdn.static.ponycool.com/img/20200430-105037.png "点击放大图片")

2.点击菜单->Conversions->Export OpenSSH key导出RSA格式密钥

[![[raw/assets/attachments/tools/20200430-105224.png]]](https://cdn.static.ponycool.com/img/20200430-105224.png "点击放大图片")