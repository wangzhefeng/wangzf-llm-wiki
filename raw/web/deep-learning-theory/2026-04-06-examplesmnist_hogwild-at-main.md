---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: A set of examples around pytorch in Vision, Text, Reinforcement Learning,
  etc. - examples/mnist_hogwild at main · pytorch/examples
source_type: web
status: inbox
tags:
- null
- clippings
title: examples/mnist_hogwild at main
source_url: https://github.com/pytorch/examples/tree/main/mnist_hogwild
published_at: null
related_concepts: []
topics:
  - deep-learning-theory
  - 深度学习理论
---

## MNIST Hogwild Example

```
pip install -r requirements.txt
python main.py
```

The main.py script accepts the following arguments:

```
optional arguments:
  -h, --help            show this help message and exit
  --batch-size          input batch_size for training (default: 64)
  --test-batch-size     input batch size for testing (default: 1000)
  --epochs EPOCHS       number of epochs to train (default: 10)
  --lr LR               learning rate (default: 0.01)
  --momentum            SGD momentum (default: 0.5)
  --seed SEED           random seed (default: 1)
  --save_model          save the trained model to state_dict
  --log-interval        how many batches to wait before logging training status (default: 10)
  --num-processes       how many training processes to use (default: 2)
  --cuda                enables CUDA training
  --mps                 enables macos GPU training
  --dry-run             quickly check a single pass
```