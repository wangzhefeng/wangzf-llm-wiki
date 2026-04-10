---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: The simplest, fastest repository for training/finetuning small-sized
  VLMs. - nanoVLM/models/config.py at main · huggingface/nanoVLM
published: null
source: https://github.com/huggingface/nanoVLM/blob/main/models/config.py
source_type: web
status: inbox
tags:
- null
- clippings
title: nanoVLM/models/config.py at main
topics:
- 大语言模型
---

1

2

3

4

5

6

7

8

9

10

11

12

13

14

15

16

17

18

19

20

21

22

23

24

25

26

27

28

29

30

31

32

33

34

35

36

37

38

39

40

41

42

43

44

45

46

47

48

49

50

51

52

53

54

55

56

57

58

59

60

61

62

63

64

65

66

67

68

69

70

71

72

73

74

75

76

77

78

79

80

81

82

83

84

85

86

87

from dataclasses import dataclass, field

@dataclass

class VLMConfig:

vit\_hidden\_dim: int = 768

vit\_inter\_dim: int = 4 \* vit\_hidden\_dim

vit\_patch\_size: int = 16

vit\_img\_size: int = 512

vit\_n\_heads: int = 12

vit\_dropout: float = 0.0

vit\_n\_blocks: int = 12

vit\_ln\_eps: float = 1e-6

vit\_cls\_flag: bool = False

vit\_model\_type: str = 'google/siglip2-base-patch16-512'

lm\_hidden\_dim: int = 960

lm\_inter\_dim: int = 2560

lm\_rms\_eps: float = 1e-5

lm\_re\_base: int = 100000

lm\_max\_position\_embeddings: int = 8192

lm\_base\_vocab\_size: int = 49152

extra\_token\_amount: int = 66 # Number of extra tokens for the VLM (image start, image end, image token)

lm\_vocab\_size: int = lm\_base\_vocab\_size + extra\_token\_amount # Not a great way to do this, but it works for now (vlm\_extra\_tokens cannot be a dict, since this is mutable, and a Field has no len() function)

lm\_n\_heads: int = 15

lm\_n\_kv\_heads: int = 5

lm\_dropout: float = 0.0

lm\_n\_blocks: int = 32

lm\_attn\_scaling: float = 1.0

lm\_max\_length: int = 4096

lm\_use\_tokens: bool = False # Decide if the LM expects tokens or embeddings as input (if using as a backbone for the VLM, set to False)

lm\_tie\_weights: bool = True # Decide if you want to tie the LM Head weight to the token embedding weights

lm\_model\_type: str = 'HuggingFaceTB/SmolLM2-360M-Instruct' #'HuggingFaceTB/SmolLM2-135M' #

lm\_tokenizer: str = 'HuggingFaceTB/SmolLM2-360M-Instruct'

lm\_chat\_template: str = "{% for message in messages %}{{'<|im\_start|>' + message\['role'\] + '\\n' + message\['content'\] + '<|im\_end|>' + '\\n'}}{% endfor %}{% if add\_generation\_prompt %}{{ '<|im\_start|>assistant\\n' }}{% endif %}"

mp\_pixel\_shuffle\_factor: int = 4

mp\_image\_token\_length: int = 64

max\_img\_size: int = 2048

resize\_to\_max\_side\_len: bool = True

vlm\_extra\_tokens: dict\[str, str\] = field(default\_factory=lambda: {"image\_token": "<|image|>", "global\_image\_token": "<|global\_image|>",

"r1c1": "<row\_1\_col\_1>", "r1c2": "<row\_1\_col\_2>", "r1c3": "<row\_1\_col\_3>", "r1c4": "<row\_1\_col\_4>", "r1c5": "<row\_1\_col\_5>", "r1c6": "<row\_1\_col\_6>", "r1c7": "<row\_1\_col\_7>", "r1c8": "<row\_1\_col\_8>",

"r2c1": "<row\_2\_col\_1>", "r2c2": "<row\_2\_col\_2>", "r2c3": "<row\_2\_col\_3>", "r2c4": "<row\_2\_col\_4>", "r2c5": "<row\_2\_col\_5>", "r2c6": "<row\_2\_col\_6>", "r2c7": "<row\_2\_col\_7>", "r2c8": "<row\_2\_col\_8>",

"r3c1": "<row\_3\_col\_1>", "r3c2": "<row\_3\_col\_2>", "r3c3": "<row\_3\_col\_3>", "r3c4": "<row\_3\_col\_4>", "r3c5": "<row\_3\_col\_5>", "r3c6": "<row\_3\_col\_6>", "r3c7": "<row\_3\_col\_7>", "r3c8": "<row\_3\_col\_8>",

"r4c1": "<row\_4\_col\_1>", "r4c2": "<row\_4\_col\_2>", "r4c3": "<row\_4\_col\_3>", "r4c4": "<row\_4\_col\_4>", "r4c5": "<row\_4\_col\_5>", "r4c6": "<row\_4\_col\_6>", "r4c7": "<row\_4\_col\_7>", "r4c8": "<row\_4\_col\_8>",

"r5c1": "<row\_5\_col\_1>", "r5c2": "<row\_5\_col\_2>", "r5c3": "<row\_5\_col\_3>", "r5c4": "<row\_5\_col\_4>", "r5c5": "<row\_5\_col\_5>", "r5c6": "<row\_5\_col\_6>", "r5c7": "<row\_5\_col\_7>", "r5c8": "<row\_5\_col\_8>",

"r6c1": "<row\_6\_col\_1>", "r6c2": "<row\_6\_col\_2>", "r6c3": "<row\_6\_col\_3>", "r6c4": "<row\_6\_col\_4>", "r6c5": "<row\_6\_col\_5>", "r6c6": "<row\_6\_col\_6>", "r6c7": "<row\_6\_col\_7>", "r6c8": "<row\_6\_col\_8>",

"r7c1": "<row\_7\_col\_1>", "r7c2": "<row\_7\_col\_2>", "r7c3": "<row\_7\_col\_3>", "r7c4": "<row\_7\_col\_4>", "r7c5": "<row\_7\_col\_5>", "r7c6": "<row\_7\_col\_6>", "r7c7": "<row\_7\_col\_7>", "r7c8": "<row\_7\_col\_8>",

"r8c1": "<row\_8\_col\_1>", "r8c2": "<row\_8\_col\_2>", "r8c3": "<row\_8\_col\_3>", "r8c4": "<row\_8\_col\_4>", "r8c5": "<row\_8\_col\_5>", "r8c6": "<row\_8\_col\_6>", "r8c7": "<row\_8\_col\_7>", "r8c8": "<row\_8\_col\_8>"})

vlm\_load\_backbone\_weights: bool = True

vlm\_checkpoint\_path: str = 'checkpoints'

hf\_repo\_name: str = 'nanoVLM'

@dataclass

class TrainConfig:

lr\_mp: float = 0.00512

lr\_vision\_backbone: float = 5e-5 #0.0005 #

lr\_language\_backbone: float = 5e-5 #0

val\_size: int = 50000

batch\_size: int = 2

gradient\_accumulation\_steps: int = 8

max\_grad\_norm: float = 1.0

eval\_in\_epochs: bool = True

eval\_interval: int = 500

stats\_log\_interval: int = 100

max\_training\_steps: int = 40000

max\_images\_per\_example: int = 4

max\_images\_per\_knapsack: int = 18

max\_sample\_length: int = 4096

compile: bool = False

resume\_from\_vlm\_checkpoint: bool = False # Indicate if the training should be resumed from a checkpoint of the whole VLM or you want to start from scratch

train\_dataset\_path: str = 'HuggingFaceM4/FineVision\_concat\_shuffled\_2'

train\_dataset\_name: tuple\[str,...\] = ("default", ) #('allava\_laion', 'allava\_vflan', 'cambrian(filtered)\_processed', 'LLaVA\_Instruct\_150K', 'mmevol', 'sharegpt4o', 'sharegpt4v(coco)', 'sharegpt4v(knowledge)', 'sharegpt4v(llava)', 'sharegpt4v(sam)') # 'vision\_flan(filtered)', 'lvis\_instruct4v',

stream\_dataset: bool = True

relevance\_min\_rating: int = 1

image\_correspondence\_min\_rating: int = 1

visual\_dependency\_min\_rating: int = 1

formatting\_min\_rating: int = 1

wandb\_entity: str = "HuggingFace" # Indicate the entity to log to in wandb

log\_wandb: bool = True

use\_lmms\_eval: bool = True # Use lmms-eval for evaluation

lmms\_eval\_tasks: str = 'mmstar,mmmu\_val,ocrbench,textvqa\_val,docvqa\_val,scienceqa,mme,infovqa\_val,chartqa' # Pass additional task as one string, seperated by commas without spaces (e.g. 'mmstar,mmmu,ocrbench')

lmms\_eval\_limit: float = None

lmms\_eval\_batch\_size: int = 64