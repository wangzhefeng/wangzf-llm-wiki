---
source_type: web
title: "Debug your model (basic) — PyTorch Lightning 2.6.1 documentation"
author: 
created_at: 2026-04-06
topics:
  - 深度学习
status: inbox
source: "https://lightning.ai/docs/pytorch/stable/debug/debugging_basic.html"
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
---

## Debug your model (basic)

**Audience**: Users who want to learn the basics of debugging models.

---

## How does Lightning help me debug?

The Lightning Trainer has *a lot* of arguments devoted to maximizing your debugging productivity.

---

## Set a breakpoint

A breakpoint stops your code execution so you can inspect variables, etc… and allow your code to execute one line at a time.

```python
def function_to_debug():
    x = 2

    # set breakpoint
    breakpoint()
    y = x**2
```

In this example, the code will stop before executing the `y = x**2` line.

---

## Run all your model code once quickly

If you’ve ever trained a model for days only to crash during validation or testing then this trainer argument is about to become your best friend.

The [`fast_dev_run`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.params.fast_dev_run "lightning.pytorch.trainer.trainer.Trainer") argument in the trainer runs 5 batch of training, validation, test and prediction data through your trainer to see if there are any bugs:

```python
trainer = Trainer(fast_dev_run=True)
```

To change how many batches to use, change the argument to an integer. Here we run 7 batches of each:

```python
trainer = Trainer(fast_dev_run=7)
```

Note

This argument will disable tuner, checkpoint callbacks, early stopping callbacks, loggers and logger callbacks like [`LearningRateMonitor`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.LearningRateMonitor.html#lightning.pytorch.callbacks.LearningRateMonitor "lightning.pytorch.callbacks.lr_monitor.LearningRateMonitor") and [`DeviceStatsMonitor`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.DeviceStatsMonitor.html#lightning.pytorch.callbacks.DeviceStatsMonitor "lightning.pytorch.callbacks.device_stats_monitor.DeviceStatsMonitor").

---

## Shorten the epoch length

Sometimes it’s helpful to only use a fraction of your training, val, test, or predict data (or a set number of batches). For example, you can use 20% of the training set and 1% of the validation set.

On larger datasets like Imagenet, this can help you debug or test a few things faster than waiting for a full epoch.

```python
# use only 10% of training data and 1% of val data
trainer = Trainer(limit_train_batches=0.1, limit_val_batches=0.01)

# use 10 batches of train and 5 batches of val
trainer = Trainer(limit_train_batches=10, limit_val_batches=5)
```

---

## Run a Sanity Check

Lightning runs **2** steps of validation in the beginning of training. This avoids crashing in the validation loop sometime deep into a lengthy training loop.

(See: [`num_sanity_val_steps`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer.params.num_sanity_val_steps "lightning.pytorch.trainer.trainer.Trainer") argument of [`Trainer`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.trainer.trainer.Trainer.html#lightning.pytorch.trainer.trainer.Trainer "lightning.pytorch.trainer.trainer.Trainer"))

```python
trainer = Trainer(num_sanity_val_steps=2)
```

---

## Print LightningModule weights summary

Whenever the `.fit()` function gets called, the Trainer will print the weights summary for the LightningModule.

```python
trainer.fit(...)
```

this generate a table like:

```js
| Name  | Type        | Params | Mode
-------------------------------------------
0 | net   | Sequential  | 132 K  | train
1 | net.0 | Linear      | 131 K  | train
2 | net.1 | BatchNorm1d | 1.0 K  | train
```

To add the child modules to the summary add a [`ModelSummary`](https://lightning.ai/docs/pytorch/stable/api/lightning.pytorch.callbacks.ModelSummary.html#lightning.pytorch.callbacks.ModelSummary "lightning.pytorch.callbacks.model_summary.ModelSummary"):

```python
from lightning.pytorch.callbacks import ModelSummary

trainer = Trainer(callbacks=[ModelSummary(max_depth=-1)])
```

To print the model summary if `.fit()` is not called:

```python
from lightning.pytorch.utilities.model_summary import ModelSummary

model = LitModel()
summary = ModelSummary(model, max_depth=-1)
print(summary)
```

To turn off the autosummary use:

```python
trainer = Trainer(enable_model_summary=False)
```

---

## Print input output layer dimensions

Another debugging tool is to display the intermediate input- and output sizes of all your layers by setting the `example_input_array` attribute in your LightningModule.

```python
class LitModel(LightningModule):
    def __init__(self, *args, **kwargs):
        self.example_input_array = torch.Tensor(32, 1, 28, 28)
```

With the input array, the summary table will include the input and output layer dimensions:

```js
| Name  | Type        | Params | Mode  | In sizes  | Out sizes
----------------------------------------------------------------------
0 | net   | Sequential  | 132 K  | train | [10, 256] | [10, 512]
1 | net.0 | Linear      | 131 K  | train | [10, 256] | [10, 512]
2 | net.1 | BatchNorm1d | 1.0 K  | train | [10, 512] | [10, 512]
```

when you call `.fit()` on the Trainer. This can help you find bugs in the composition of your layers.