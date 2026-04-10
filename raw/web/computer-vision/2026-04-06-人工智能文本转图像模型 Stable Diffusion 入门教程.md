---
source_type: web
title: "人工智能文本转图像模型 Stable Diffusion 入门教程"
author:
  - 
  - "[[x1ao4交流 PLEX 可加群]]"
created_at: 2026-04-06
topics:
  - 计算机视觉
status: inbox
source: "https://zhuanlan.zhihu.com/p/561112515"
published: 
created: 2026-04-06
description: "Stable Diffusion 是由 CompVis、Stability AI 和 LAION 共同开发的一个文本转图像模型，它通过 LAION-5B 子集大量的 512x512 图文模型进行训练，我们只要简单的输入一段文本，Stable Diffusion 就可以迅速将其转…"
tags:
  - 
  - "clippings"
---

Stable Diffusion 是由 [CompVis](https://link.zhihu.com/?target=https%3A//github.com/CompVis) 、 [Stability AI](https://link.zhihu.com/?target=https%3A//stability.ai/) 和 [LAION](https://link.zhihu.com/?target=https%3A//laion.ai/) 共同开发的一个文本转图像模型，它通过 [LAION-5B](https://link.zhihu.com/?target=https%3A//laion.ai/blog/laion-5b/) 子集大量的 512x512 图文模型进行训练，我们只要简单的输入一段文本，Stable Diffusion 就可以迅速将其转换为图像，同样我们也可以置入图片或视频，配合文本对其进行处理。先来看几个示例吧。

![[assets/attachments/computer-vision/v2-84f2397c03234011f055b4ff2187f639_1440w.jpg]]

Prompt: In a cyberpunk city, a police car is on the street, raining, light effect, Simon Stalenhag, Ian McQue, Ghibli Studio, Beeple, Kaino University

![[assets/attachments/computer-vision/v2-5ee6c9ad6ef109f483dcf35b70d553d4_1440w.jpg]]

Prompt: Glowing crystals in the depths of the black valley, Simon Stalenhag, Ian McQue, Ghibli Studio, Beeple, Kaino University, high-definition picture, unreal engine

![[assets/attachments/computer-vision/v2-5d35bc24bf88d77395650096af660172_1440w.jpg]]

Prompt: A silver mech horse running in a dark valley, in the night, Beeple, Kaino University, high-definition picture, unreal engine, cyberpunk

![[assets/attachments/computer-vision/v2-d021eea2409e310f3a01f79d743629fd_1440w.jpg]]

Prompt: An astronaut floating in the universe

![[assets/attachments/computer-vision/v2-31cf044221a35faae8aba0dc95721595_1440w.jpg]]

Prompt: Grass and flowers by the sea, forest, clear sky, light effect, Beeple, Caspar David Friedrich, Alphonse Mucha

![[assets/attachments/computer-vision/v2-533d3adf3902905562e3f6e373a90777_1440w.jpg]]

Prompt: Two knife-wielding pirates dueling on a pirate ship, dusk, heavy rain, unreal engine, 8k, high-definition, by Alphonse Mucha and Wayne Barlowe

使用 Stable Diffusion 目前有几种不同的途径：

01\. **[Stable Diffusion Demo](https://link.zhihu.com/?target=https%3A//huggingface.co/spaces/stabilityai/stable-diffusion)** ，这是官方发布的一个简单的体验版，无需登录，只需要「 **输入描述文本** 」，然后 **点击** 「 **生成图像** 」即可，可进行简单的设置，需要排队，等待时长根据排队人数而定，通常需要几分钟，完成后图片会展示在文本下方，可右击保存，只可生成 512x512 像素的图片。

![[assets/attachments/computer-vision/v2-43d12e3b3bc9d19ce35a2c7b5d9459a7_1440w.jpg]]

02\. **[DreamStudio Beta](https://link.zhihu.com/?target=https%3A//beta.dreamstudio.ai/dream)** ，这是官方发布的公测版，可以对参数进行调整，需要注册登录，注册后会获得 **200** 积分（generations/credits）， **每次生成需要消耗相应的积分** ，积分用完后需要购买才可继续使用，价格 10 英镑（80 元左右）1000 积分。

![[assets/attachments/computer-vision/v2-8979286536038b4d3ca96feeeb26f1de_1440w.jpg]]

界面右侧是参数调整区，可调整图片的尺寸、文本描述与成图的贴近程度、步数、生成图片的张数、采样模式和种子， **一般按默认参数即可** ，其中图片尺寸和步数会影响消耗的积分数量，步数建议使用默认 **50** 步，高了也并没有太大区别，各种尺寸和步数需要的积分如下。

![[assets/attachments/computer-vision/v2-f3ffaf71f8ec1574e555594fe113d8ff_1440w.jpg]]

图片生成后可 **点击图片中心的下载按钮下载图片** ，若生成多张图片可 **点击** 图片下方的「 **Download All** 」按钮下载全部图片，注意目前生成多张图片时若点击某张图片进行放大预览后是无法返回多图预览界面，无法再下载其他图片的，因此 **如果生成了多张图片建议先全部下载下来** 。

**点击** 界面左侧的「 **History** 」可进入历史记录页面，可以 **查看** 之前 **生成图片的记录** ，这里主要记录了历次生成的 Prompt、尺寸和种子等信息，如果想对过去生成的图片进行优化或调整，可在此复制 **Seed** 值，并回到 Dream 页面打开界面右下角 **Random Seed** 后方的按钮，然后将种子值粘贴至此，在调整参数或描述，重新生成图片。

**点击** 界面右上角 **自己的头像** ，选择「 **Membership** 」进入个人中心，可 **查看个人积分余额** 及充值。

![[assets/attachments/computer-vision/v2-46d4f038ae9a21454cb75e04654320df_1440w.jpg]]

03\. **[Stable Diffusion](https://link.zhihu.com/?target=https%3A//colab.research.google.com/github/huggingface/notebooks/blob/main/diffusers/stable_diffusion.ipynb)** ，这是官方发布的 Google Colab 版本，无生成次数限制，需要注册 Hugging Face 账号，需要谷歌账号，需要科学上网，这个版本的流程有点繁琐， **不推荐** ，这边不做介绍了。

04\. **[Stable Diffusion WebUI 1.4](https://link.zhihu.com/?target=https%3A//colab.research.google.com/github/altryne/sd-webui-colab/blob/main/Stable_Diffusion_WebUi_Altryne.ipynb)** ，这是由 **@altryne** 制作的有 WebUI 的 Google Colab 版本，无生成次数限制，需要注册 Hugging Face 账号，需要谷歌账号，需要科学上网，这算是目前比较好用的一版，这边详细介绍一下。

**准备工作\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**

04.01. **注册谷歌** 账号并 **登录** 。

04.02. **注册** **[Hugging Face](https://link.zhihu.com/?target=https%3A//huggingface.co/)** 账号并 **登录** （注册后去邮箱验证一下）。

04.03. **打开** **[CompVis/stable-diffusion-v1-4](https://link.zhihu.com/?target=https%3A//huggingface.co/CompVis/stable-diffusion-v1-4)** 页面，找到下图部分， **勾选同意** 选项， **点击** 「 **Access repository** 」，开通模型访问权限。（这里列出了使用协议，可以自己看一下）

![[assets/attachments/computer-vision/v2-14353fa103e4c4d54868a49bda09e1bc_1440w.jpg]]

04.04. **打开 [CompVis/stable-diffusion](https://link.zhihu.com/?target=https%3A//huggingface.co/CompVis/stable-diffusion)** 页面，找到「 **stable-diffusion-v-1-4-original** 」并单击打开链接。（如果以后更新版本了，请打开对应版本的链接）

![[assets/attachments/computer-vision/v2-a5899a9ba5c4c0504656734f9988f55b_1440w.jpg]]

04.05. 找到下图部分， **勾选同意** 选项， **点击** 「 **Access repository** 」，开通模型下载权限。

![[assets/attachments/computer-vision/v2-14353fa103e4c4d54868a49bda09e1bc_1440w.jpg]]

04.06. **打开 [Access Tokens](https://link.zhihu.com/?target=https%3A//huggingface.co/settings/tokens)** 页面， **点击** 「 **New Token** 」按钮，起个名字，Role 选 read 或者 write 都可以， **点击** 「 **Generate a token** 」， **点击** Show 后面的 **复制** 按钮复制 Token。

![[assets/attachments/computer-vision/v2-c028a2b815b257b8355e9bd810345800_1440w.jpg]]

![[assets/attachments/computer-vision/v2-421f5c4807d2b0380561c630543809ec_1440w.jpg]]

**入门教程\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**

04.1. **打开** **[Stable Diffusion WebUI 1.4](https://link.zhihu.com/?target=https%3A//colab.research.google.com/github/altryne/sd-webui-colab/blob/main/Stable_Diffusion_WebUi_Altryne.ipynb)** ，若未自动登录谷歌账号请 **点击** 页面右上角「 **登录** 」按钮， **登入你的谷歌账号** 。

04.2. **点击** 「 **复制到云端硬盘** 」或点击「文件」选择「在云端硬盘中保存一份副本」。

![[assets/attachments/computer-vision/v2-4131cf1a01afb4d430503091f259c57b_1440w.jpg]]

04.3. 副本创建完成会出现「笔记本的副本已完成」弹窗， **点击** 「 **在新标签页中打开** 」。

04.4. 点击「“Stable Diffusion WebUi - Altryne”的副本」 **修改笔记本名称** （不改也可以，以后就能直接从自己的云端硬盘打开这个文件运行 Stable Diffusion 了）。

![[assets/attachments/computer-vision/v2-94e0744cc44c8ea12f6bcd7f91f55b21_1440w.jpg]]

04.5. **点击** 「1 - Setup stage」前面的 **小三角** ，找到「 **1.4 Connect to Google Drive** 」，将 **token** （第 04.06. 步复制的 token）粘贴在图中位置，并 **勾选** 「 **download\_if\_missing** 」选项。

![[assets/attachments/computer-vision/v2-324a1f4a8d4f2b17769732d19251e2bc_1440w.jpg]]

04.6. 点击「代码执行程序」选择「 **全部运行** 」。

![[assets/attachments/computer-vision/v2-d9149adc7f3d69ab7dd105dac4d579d3_1440w.jpg]]

04.7. 弹出「笔记本需要高 RAM」的窗口， **点击** 「 **确定** 」。（接下来需要等待一段时间，你看到 1 - Setup stage 下面的按钮在转圈圈就表示程序正在运行，需要下载一些文件，第一次运行等待时间会稍长一些）

04.8. 弹出「您还在设备面前吗？」的窗口， **点击** 「 **进行人机身份验证** 」，按指令进行验证。（如果没有弹出可忽略）

04.9. 弹出「允许此笔记本访问您的 Google 云端硬盘文件吗？」的窗口， **点击** 「 **连接到 Google 云端硬盘** 」。

04.10. 弹出「登录 - Google 账号」窗口， **选择你的谷歌账号** ， **点击** 「 **允许** 」。（如果等待过程中 Google Colab 图标变红，网络中断，可点击页面右上角的重新连接，重连后会继续运行）

04.11. **点击** 「3 - Launch WebUI for stable diffusion」前面的 **小三角** 展开单元，当这个单元最下方出现「 **Running on public URL: https://57651.gradio.app** 」就表示程序启动成功， **点击** 「 **https://57651.gradio.app** 」 **打开 WebUI** 。（每次会得到不同的地址）

![[assets/attachments/computer-vision/v2-3aaaac5ded9b533798fb3a6e947c8234_1440w.jpg]]

04.12. 在如图位置 **输入prompt** （描述文本）， **设置** 好图片 **尺寸** 和生成图片 **张数** ，其他建议按默认值， **点击** 「 **Generate** 」就开始生成了。

![[assets/attachments/computer-vision/v2-4e2060c6703126ca8f416cb24d0c78d2_1440w.jpg]]

04.13. 回到 Stable Diffusion WebUi - Altryne 的页面，你会在「3 - Launch WebUI for stable diffusion」的末尾看到 **实时进度** ，以下图为例，Iteration: 1/12 表示总数 12 张图的第 1 张图片，以此类推，前面的 100% 是完成进度，50/50 是当前完成步数/总步数，00:42<00:00 是已使用时间<剩余时间，1.17it/s 是每秒完成 1.17 步，当出现 **\[MemMon\] Stopped recording.** 就表示当前任务的所有图片已经生成完毕。（正常情况生成结束后 WebUI 页面也会展示生成的图片，但是如果有网络不稳定、延迟大等情况或者连续运行超过 90 分钟，生成完毕后 WebUI 页面可能不会显示图片，甚至还在继续计时，此时 WebUI 页面已经断开连接，需要刷新页面后恢复使用）

![[assets/attachments/computer-vision/v2-e6dd2b33b4e73ae0a1a7759d55f18992_1440w.jpg]]

04.14. 现在你就可以在 **[Google Drive](https://link.zhihu.com/?target=https%3A//drive.google.com/)** 直接 **查看保存的图片** 了，打开 **AI** - **StableDiffusion** 文件夹，这个文件夹里保存的是每次生成任务的汇总图，如果一次生成了多张图片它会自动把这些图片拼在一起。在「 **samples** 」文件夹内会以每次生成任务的 **prompt** 为名称分别建立子文件夹，生成的图片会保存在里面，并且每张图都会附带一个 yaml 格式的配置文件，可以查看这张图片的参数设置。

![[assets/attachments/computer-vision/v2-82bf605e509fe9a1b72c1bdbf80826f0_1440w.jpg]]

**进阶教程\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**

04.15. 打开 WebUI 第二个标签，这个是图像转图像，就是添加一张参考图，配合文本描述生成图片，注意 **参考图的尺寸要和输出尺寸一致** ，否则会报错，可以将图片调整好尺寸以后再添加进来，或者使用左图下方的「 **Advanced Editor** 」编辑图片后再操作，步数建议 50 步，图中两个有说明的值可以调整生成效果，建议在默认值左右小范围调整以观察效果，极端值效果不佳。

![[assets/attachments/computer-vision/v2-6b7cacb249379b7f7d00328b15452558_1440w.jpg]]

04.16. WebUI 第三个标签是人脸修复工具，我试验了效果并不理想，使用方式就是添加图片点生成就行了，这边重点推荐一下第四个标签， **RealESRGAN** 是一个智能放大图片的模型，效果十分惊人，我之前一直用的是 Topaz Gigapixel AI，RealESRGAN 的效果完爆 Topaz Gigapixel AI，操作也很简单，添加图片点击生成即可，这里有两个模型，有一个模型是动漫专用的。

05\. **[pharmapsychotic Stable Diffusion](https://link.zhihu.com/?target=https%3A//colab.research.google.com/github/pharmapsychotic/ai-notebooks/blob/main/pharmapsychotic_Stable_Diffusion.ipynb)** ，这是由 **@pharmapsychotic** 制作的 Google Colab 版本，无生成次数限制，需要注册 Hugging Face 账号，需要谷歌账号，需要科学上网，这个版本的操作比较接近 Disco Diffusion，DD 玩家用起来可能比较顺手，这边也介绍一下。

**准备工作\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**

05.01. **注册谷歌** 账号并 **登录** 。（如果之前使用过 **[Stable Diffusion WebUI 1.4](https://link.zhihu.com/?target=https%3A//colab.research.google.com/github/altryne/sd-webui-colab/blob/main/Stable_Diffusion_WebUi_Altryne.ipynb)** 或其他 Google Colab 版本的 Stable Diffusion 可跳过步骤 05.02.-05.06.）

05.02. **注册** **[Hugging Face](https://link.zhihu.com/?target=https%3A//huggingface.co/)** 账号并 **登录** （注册后去邮箱验证一下）。

05.03. **打开** **[CompVis](https://link.zhihu.com/?target=https%3A//huggingface.co/CompVis/stable-diffusion) / [stable-diffusion](https://link.zhihu.com/?target=https%3A//huggingface.co/CompVis/stable-diffusion)** 页面，找到「 **stable-diffusion-v-1-4-original** 」并单击打开链接。（目前最新的版本是 1.4，如果以后有更新也可以来这里下载更新的版本）

![[assets/attachments/computer-vision/v2-a5899a9ba5c4c0504656734f9988f55b_1440w.jpg]]

05.04. 找到下图部分， **勾选同意** 选项， **点击** 「 **Access repository** 」，开通模型访问权限。（这里列出了使用协议，可以自己看一下）

![[assets/attachments/computer-vision/v2-14353fa103e4c4d54868a49bda09e1bc_1440w.jpg]]

05.05. 在页面上找到下图位置，通过链接 **下载** 「 **sd-v1-4.ckpt** 」文件。

![[assets/attachments/computer-vision/v2-76941eec4575000874da4c97f9710404_1440w.jpg]]

05.06. 打开 **[Google Drive](https://link.zhihu.com/?target=https%3A//drive.google.com/)** 并登录你的账号，将下载的「 **sd-v1-4.ckpt** 」文件上传至 **AI** 文件夹内的 **models** 文件夹内，如果没有这个文件夹请手动新建文件夹。

**入门教程\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**

05.1. **打开** **[pharmapsychotic Stable Diffusion](https://link.zhihu.com/?target=https%3A//colab.research.google.com/github/pharmapsychotic/ai-notebooks/blob/main/pharmapsychotic_Stable_Diffusion.ipynb)** ，若未自动登录谷歌账号请 **点击** 页面右上角「 **登录** 」按钮， **登入你的谷歌账号** 。

05.2. **点击** 「 **复制到云端硬盘** 」或点击「文件」选择「在云端硬盘中保存一份副本」。

![[assets/attachments/computer-vision/v2-a8b4ae6753e47cf69df046a236ff3f43_1440w.jpg]]

05.3. 副本创建完成会出现「笔记本的副本已完成」弹窗， **点击** 「 **在新标签页中打开** 」。

05.4. 点击「“pharmapsychotic\_Stable\_Diffusion.ipynb”的副本」 **修改笔记本名称** （以下所有代码可视为源文件/源代码，此处是源文件的名称，可按创作主题或其他方式命名，方便后期修改和区分）。

![[assets/attachments/computer-vision/v2-f708c7555f3e7769cb17d40db0ac9b4c_1440w.jpg]]

05.5. **修改** 文件夹 **名称** 、 **步数** 、生成图片 **张数** 等参数， **输入描述文本** 。

![[assets/attachments/computer-vision/v2-6bcae853daed9766254f1356f12775ad_1440w.jpg]]

05.6. 点击「代码执行程序」选择「 **全部运行** 」。

05.7. 弹出「笔记本需要高 RAM」的窗口， **点击** 「 **确定** 」。（接下来需要等待一段时间，第一次运行等待时间会稍长一些）

05.8. 弹出「您还在设备面前吗？」的窗口， **点击** 「 **进行人机身份验证** 」，按指令进行验证。（如果没有弹出可忽略）

05.9. 弹出「允许此笔记本访问您的 Google 云端硬盘文件吗？」的窗口， **点击** 「 **连接到 Google 云端硬盘** 」。

05.10. 弹出「登录 - Google 账号」窗口， **选择你的谷歌账号** ， **点击** 「 **允许** 」。（如果等待过程中 Google Colab 图标变红，网络中断，可点击页面右上角的重新连接，重连后会继续运行）

05.11. 待 **prompt** 下方出现 **进度条** 就表示正在生成图片了，以下图为例，46% 是当前完成进度，23/50 是指总步数 50 步目前已完成 23 步，00:20<00:25 是指已用时 20 秒，预计还需 25 秒，1.07it/s 是指每秒生成 1.07 步，4046755246 是种子值。

![[assets/attachments/computer-vision/v2-68cf801f8b3bb264828c754b75cb642f_1440w.jpg]]

05.12. 任务完成后会在此处显示，若一次生成了多张图片会依次在此显示，全部完成后会显示最后一张图片。

![[assets/attachments/computer-vision/v2-535aa1cf0e755172ad8e90f1ef201473_1440w.jpg]]

05.13. 你可以直接在这里右击保存图片，也可以在 **[Google Drive](https://link.zhihu.com/?target=https%3A//drive.google.com/)** 相应的文件夹内查看和下载图片，文件夹在 **AI** - **StableDiffusion** 这个目录下。

**进阶教程\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**

05.14. **点击** 左侧的第四个「 **文件** 」 **图标** 展开文件窗口。

![[assets/attachments/computer-vision/v2-af3326b005cc5984f16249b3836c17f2_1440w.jpg]]

05.15. **点击** 文件窗口上方第一个「 **上传到会话存储空间** 」 **图标** ，选择你要上传的图片并点击「打开」，图片就会开始上传（你也可以把图片直接拖进文件窗口的空白处）。

![[assets/attachments/computer-vision/v2-5ae1590897a508596403ab9b4de65d4c_1440w.jpg]]

05.16. 上传完成后图片会显示在文件窗口的列表中，找到你要使用的图片并 **点击** 文件名后方的 **三个小圆点** ，选择「 **复制路径** 」。

![[assets/attachments/computer-vision/v2-624b2ad24709ad13cb57becd5f66f245_1440w.jpg]]

05.17. **将路径粘贴在如图位置，设置 init\_strength 等参数，** 点击「代码执行程序」选择「 **全部运行** 」，如果之前已经运行过程序，直接点击 **Image creation** 单元前面的圆形按钮即可。

![[assets/attachments/computer-vision/v2-8802efb9b519feec31919f214943d1b5_1440w.png]]

06\. **[Deforum Stable Diffusion v0.3](https://link.zhihu.com/?target=https%3A//colab.research.google.com/github/deforum/stable-diffusion/blob/main/Deforum_Stable_Diffusion.ipynb)** ，这是由 **[deforum](https://link.zhihu.com/?target=https%3A//discord.gg/upmXXsrwZc)** 制作的 Google Colab 版本，无生成次数限制，需要注册 Hugging Face 账号，需要谷歌账号，需要科学上网，这个版本 **支持制作动画视频** ，如果运行过其他 Google Colab 版本的 Stable Diffusion 可以直接运行这个版本，如果未运行过其他版本的 Stable Diffusion 需要按「 **05.01. -05.06.**」步骤进行操作，下载并上传「 **sd-v1-4.ckpt** 」文件至你的谷歌云盘，然后可以直接运行。这个版本我就不讲解了，如果有想做视频的朋友可以去研究一下。

07\. **[Stable Diffusion Interpolation V2.1](https://link.zhihu.com/?target=https%3A//colab.research.google.com/drive/1EHZtFjQoRr-bns1It5mTcOVyZzZD9bBc%3Fusp%3Dsharing)** ，这是由 @ygantigravity 和 @pharmapsychotic 制作的 Google Colab 版本，无生成次数限制，需要注册 Hugging Face 账号，需要谷歌账号，需要科学上网，这个版本有 **多文本多种子混合模式** ，似乎可以生成视频，感兴趣的朋友可以研究一下，同样需要下载并上传「 **sd-v1-4.ckpt** 」文件至谷歌云盘，然后再使用，若运行过其他 Google Colab 版本的 Stable Diffusion 可以直接运行。

08\. **[四行PaddleNLP代码体验Stable Diffusion](https://link.zhihu.com/?target=https%3A//aistudio.baidu.com/aistudio/projectdetail/4459390%3FchannelType%3D0%26channel%3D0)** ，这是由 **凉心半浅良心人** 发布在飞桨平台的版本，有点类似于国内版的 Google Colab，也可以免费使用（有时长限制），这个我自己没有测试，看起来获取免费时长还是有点麻烦，供大家参考吧。

因为 Stable Diffusion 是一个开源模型，所以向公众开放以后涌现出了很多的开发者对其进行修改和加工，创造出了很多不同的版本，他们各有特色，大家可以选择适合自己的版本进行使用，也可以都试一试，选一个自己最顺手的版本。

**本地运行\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**

以上是在线使用的教程，其实你也可以把 Stable Diffusion 部署到本地运行，但你需要一个至少有 10G 显存的 NVIDIA 显卡，已知官方 DreamStudio Beta 出一张 1024x512 的图需要大概 15秒，Google Colab 免费用户使用 TESLA T4 GPU 16G 显存出一张 1024x512 的图需要大概 42 秒，不过重点不是时间快慢，而是如果显存不够可能根本跑不起来，或者只能跑很小尺寸的图，所以大家依自己的情况而定，如果条件允许，也可以考虑部署到本地，但是会相对麻烦许多。这边也分享两个本地部署的教程给大家。

[Stable Diffusion AI 绘画 ｜2022.08.27｜本地部署 新手教程](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/BV12d4y1A7fR%3Fspm_id_from%3D333.999.0.0%26vd_source%3Dc4ce73eabed370236ad7d8ab6079980c) by @stillcreek

[【傻瓜教程】10分钟本地部署最新AI生成绘画(Stable Diffusion)，有GPU就能玩！](https://link.zhihu.com/?target=https%3A//www.bilibili.com/video/BV1rV4y1H7K3%3Fspm_id_from%3D333.999.0.0%26vd_source%3Dc4ce73eabed370236ad7d8ab6079980c) by @诡道荒行

更新一个本地版本， [NMKD Stable Diffusion GUI - AI Image Generator](https://link.zhihu.com/?target=https%3A//nmkd.itch.io/t2i-gui) ，这个版本是打包好的程序，没有繁琐的部署过程，下载以后安装即可使用，目前仅支持 Nvidia 6G 以上的显卡，4G 可能参数设置的低一些也勉强能用，后续版本可能会增强对低显存的支持，仅支持 Windows 系统，这个版本的作者是 [N00MKRAD](https://link.zhihu.com/?target=https%3A//nmkd.itch.io/) ，使用此版的朋友可以加入他们的 Discord，如果使用遇到问题可以去上面反馈。

**注意事项\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_\_**

教程中所有准备工作部分仅第一次使用需要操作，之后可以直接运行，Google Colab 平台的版本可能会由于网络不稳定而报错，如果参考教程设置参数后仍有报错情况，请先仔细查阅错误提示，如果看不懂建议直接点击「代码执行程序」选择「 **全部运行** 」，重新运行即可。Stable Diffusion WebUI 1.4 版本 WebUI 页若操作没反应，尝试刷新页面后再操作即可，如果还有问题，建议重新运行。宽和高必须设置为 64 的整数倍，也就是 64、128、192、256、320、384、448、512、576、640、704、768、832、896、960、1024、1088、1152、1216、1280 等等，建议 1024x512 左右，大了会爆显存，会崩，可以小一点，RealESRGAN 的放大效果很好，可以出小图再用 RealESRGAN 放大，可放大 4 倍，且保持画质清晰。

如果你是首次接触 Google Colab，提醒一下，免费账号每天有使用时长限制，超过限额会有弹窗提醒，超额后从当日首次连接服务器开始计算 24 小时后恢复使用，如果想继续使用可以付费升级账号或者更换谷歌账号登录使用。

教程中所有准备工作都是为了下载模型，首次使用正常运行后模型就自动下载到你的云盘了，以后可以直接从云盘副本运行程序，不需要再按准备工作部分操作。

Stable Diffusion 的操作比较简单，效率也比较高，赶快去试一试吧！感谢 CompVis、Stability AI 和 LAION，感谢开发者们。

还没有人送礼物，鼓励一下作者吧

编辑于 2023-02-16 16:11・四川[图像处理](https://www.zhihu.com/topic/19556376)[人工智能](https://www.zhihu.com/topic/19551275)[Stable Diffusion](https://www.zhihu.com/topic/26072993)