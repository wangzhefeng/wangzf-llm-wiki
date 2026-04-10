---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: CaffeNet fine-tuned on the Oxford 102 category flower dataset - readme.md
published: null
source: https://gist.github.com/jimgoo/0179e52305ca768a601f
source_type: web
status: inbox
tags:
- null
- clippings
title: CaffeNet fine-tuned on the Oxford 102 category flower dataset
topics:
- 运筹优化
---

name: CaffeNet fine-tuned on the Oxford 102 category flower dataset

caffemodel: oxford102.caffemodel

caffemodel\_url: [https://s3.amazonaws.com/jgoode/oxford102.caffemodel](https://s3.amazonaws.com/jgoode/oxford102.caffemodel)

gist\_id: 0179e52305ca768a601f

license: BSD-3

See [https://github.com/jimgoo/caffe-oxford102](https://github.com/jimgoo/caffe-oxford102) for full code.

The CNN is a BVLC reference CaffeNet fine-tuned for the [Oxford 102 category flower dataset](http://www.robots.ox.ac.uk/~vgg/data/flowers/102/index.html). The number of outputs in the inner product layer has been set to 102 to reflect the number of flower categories. Hyperparameter choices reflect those in [Fine-tuning CaffeNet for Style Recognition on “Flickr Style” Data](http://caffe.berkeleyvision.org/gathered/examples/finetune_flickr_style.html). The global learning rate is reduced while the learning rate for the final fully connected is increased relative to the other layers.

The split file (setid.mat) lists 6,149 images in the test set and 1,020 images in the training set. We have instead trained this model on the larger set of 6,149 images and tested against the smaller set of 1,020 images.

After 50,000 iterations, the top-1 error is 7% on the test set of 1,020 images:

```
I0215 15:28:06.417726  6585 solver.cpp:246] Iteration 50000, loss = 0.000120038
I0215 15:28:06.417789  6585 solver.cpp:264] Iteration 50000, Testing net (#0)
I0215 15:28:30.834987  6585 solver.cpp:315]     Test net output #0: accuracy = 0.9326
I0215 15:28:30.835072  6585 solver.cpp:251] Optimization Done.
I0215 15:28:30.835083  6585 caffe.cpp:121] Optimization Done.
```

Note that this uses the mean file for ILSVRC 2012 instead of the mean for the actual Oxford dataset.