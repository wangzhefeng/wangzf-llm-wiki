---
source_type: web
title: "Long Short-Term Memory (LSTM)"
author: 
created_at: 2026-04-06
topics:
  - 待分类
status: inbox
source: "https://nn.labml.ai/lstm/index.html"
published: 
created: 2026-04-06
description: "A simple PyTorch implementation/tutorial of Long Short-Term Memory (LSTM) modules."
tags:
  - 
  - "clippings"
---

[#](#section-0)

This is a [PyTorch](https://pytorch.org/) implementation of Long Short-Term Memory.

```
12
from typing import Optional, Tuple
13

14
import torch
15
from torch import nn
```

[#](#section-1)

## Long Short-Term Memory Cell

LSTM Cell computes , and . is like the long-term memory, and is like the short term memory. We use the input and to update the long term memory. In the update, some features of are cleared with a forget gate , and some features are added through a gate .

The new short term memory is the of the long-term memory multiplied by the output gate .

Note that the cell doesn't look at long term memory when doing the update. It only modifies it. Also never goes through a linear transformation. This is what solves vanishing and exploding gradients.

Here's the update rule.

stands for element-wise multiplication.

Intermediate values and gates are computed as linear transformations of the hidden state and input.

```
19
class LSTMCell(nn.Module):
```

```
56
    def __init__(self, input_size: int, hidden_size: int, layer_norm: bool = False):
57
        super().__init__()
```

These are the linear layer to transform the

```
input
```
and
```
hidden
```
vectors. One of them doesn't need a bias since we add the transformations.

[#](#section-4)

This combines , , , and transformations.

```
63
        self.hidden_lin = nn.Linear(hidden_size, 4 * hidden_size)
```

[#](#section-5)

This combines , , , and transformations.

```
65
        self.input_lin = nn.Linear(input_size, 4 * hidden_size, bias=False)
```

[#](#section-6)

Whether to apply layer normalizations.

Applying layer normalization gives better results. , , and embeddings are normalized and is normalized in

```
72
        if layer_norm:
73
            self.layer_norm = nn.ModuleList([nn.LayerNorm(hidden_size) for _ in range(4)])
74
            self.layer_norm_c = nn.LayerNorm(hidden_size)
75
        else:
76
            self.layer_norm = nn.ModuleList([nn.Identity() for _ in range(4)])
77
            self.layer_norm_c = nn.Identity()
```

```
79
    def forward(self, x: torch.Tensor, h: torch.Tensor, c: torch.Tensor):
```

[#](#section-8)

We compute the linear transformations for , , and using the same linear layers.

```
82
        ifgo = self.hidden_lin(h) + self.input_lin(x)
```

Each layer produces an output of 4 times the

```
hidden_size
```
and we split them

```
84
        ifgo = ifgo.chunk(4, dim=-1)
```

[#](#section-10)

Apply layer normalization (not in original paper, but gives better results)

```
87
        ifgo = [self.layer_norm[i](ifgo[i]) for i in range(4)]
```

[#](#section-11)

```
90
        i, f, g, o = ifgo
```

[#](#section-12)

```
93
        c_next = torch.sigmoid(f) * c + torch.sigmoid(i) * torch.tanh(g)
```

[#](#section-13)

Optionally, apply layer norm to

```
97
        h_next = torch.sigmoid(o) * torch.tanh(self.layer_norm_c(c_next))
98

99
        return h_next, c_next
```

[#](#section-14)

## Multilayer LSTM

```
102
class LSTM(nn.Module):
```

Create a network of

```
n_layers
```
of LSTM.

```
107
    def __init__(self, input_size: int, hidden_size: int, n_layers: int):
```

```
112
        super().__init__()
113
        self.n_layers = n_layers
114
        self.hidden_size = hidden_size
```

[#](#section-17)

Create cells for each layer. Note that only the first layer gets the input directly. Rest of the layers get the input from the layer below

```
117
        self.cells = nn.ModuleList([LSTMCell(input_size, hidden_size)] +
118
                                   [LSTMCell(hidden_size, hidden_size) for _ in range(n_layers - 1)])
```

```
x
```
has shape
```
[n_steps, batch_size, input_size]
```
and
```
state
```
is a tuple of and, each with a shape of
```
[batch_size, hidden_size]
```
.

```
120
    def forward(self, x: torch.Tensor, state: Optional[Tuple[torch.Tensor, torch.Tensor]] = None):
```

```
125
        n_steps, batch_size = x.shape[:2]
```

Initialize the state if

```
None
```

```
128
        if state is None:
129
            h = [x.new_zeros(batch_size, self.hidden_size) for _ in range(self.n_layers)]
130
            c = [x.new_zeros(batch_size, self.hidden_size) for _ in range(self.n_layers)]
131
        else:
132
            (h, c) = state
```

[#](#section-21)

Reverse stack the tensors to get the states of each layer

📝 You can just work with the tensor itself but this is easier to debug

```
136
            h, c = list(torch.unbind(h)), list(torch.unbind(c))
```

[#](#section-22)

Array to collect the outputs of the final layer at each time step.

```
139
        out = []
140
        for t in range(n_steps):
```

[#](#section-23)

Input to the first layer is the input itself

```
142
            inp = x[t]
```

[#](#section-24)

Loop through the layers

```
144
            for layer in range(self.n_layers):
```

[#](#section-25)

Get the state of the layer

```
146
                h[layer], c[layer] = self.cells[layer](inp, h[layer], c[layer])
```

[#](#section-26)

Input to the next layer is the state of this layer

```
148
                inp = h[layer]
```

[#](#section-27)

Collect the output of the final layer

```
150
            out.append(h[-1])
```

[#](#section-28)

Stack the outputs and states

```
153
        out = torch.stack(out)
154
        h = torch.stack(h)
155
        c = torch.stack(c)
156

157
        return out, (h, c)
```