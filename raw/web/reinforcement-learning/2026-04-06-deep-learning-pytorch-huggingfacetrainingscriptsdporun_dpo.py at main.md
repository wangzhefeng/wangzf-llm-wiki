---
source_type: web
title: "deep-learning-pytorch-huggingface/training/scripts/dpo/run_dpo.py at main"
author: 
created_at: 2026-04-06
topics:
  - 强化学习
status: inbox
source: "https://github.com/philschmid/deep-learning-pytorch-huggingface/blob/main/training/scripts/dpo/run_dpo.py"
published: 
created: 2026-04-06
description: "Contribute to philschmid/deep-learning-pytorch-huggingface development by creating an account on GitHub."
tags:
  - 
  - "clippings"
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

88

89

90

91

92

93

94

95

96

97

98

99

100

101

102

103

104

105

106

107

108

109

110

111

112

113

114

115

116

117

118

119

120

121

122

123

124

125

126

127

128

129

130

131

132

133

134

135

136

137

138

139

140

141

142

143

144

145

146

147

148

149

150

151

152

153

154

155

156

157

158

159

160

161

162

163

164

165

166

167

168

169

170

171

172

173

174

175

176

177

178

179

180

181

182

183

184

185

186

187

188

189

190

191

192

193

194

195

196

197

198

199

200

201

202

203

204

205

206

207

208

209

210

211

212

213

214

215

216

217

218

219

220

221

222

223

224

225

226

227

228

229

230

231

232

233

234

235

236

237

238

239

240

241

242

243

244

245

246

247

248

249

250

251

252

253

254

255

256

257

258

259

260

import logging

import os

import torch

from transformers import (

AutoModelForCausalLM,

set\_seed,

)

from dataclasses import dataclass

from datetime import datetime

from distutils.util import strtobool

import logging

import os

from typing import Optional

os.environ\["HF\_HUB\_ENABLE\_HF\_TRANSFER"\] = "1"

import torch

from transformers import (

AutoModelForCausalLM,

AutoTokenizer,

set\_seed,

BitsAndBytesConfig,

)

from transformers.trainer\_utils import get\_last\_checkpoint

from transformers.utils import is\_liger\_kernel\_available

from trl import TrlParser, ModelConfig, get\_peft\_config

from datasets import load\_dataset

from trl import (

DPOTrainer,

DPOConfig,

TrlParser,

get\_peft\_config,

ModelConfig,

)

from datasets import load\_dataset

########################

\# Custom dataclasses

########################

@dataclass

class ScriptArguments:

dataset\_id\_or\_path: str

dataset\_splits: str = "train"

tokenizer\_name\_or\_path: str = None

########################

\# Setup logging

########################

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(\_\_name\_\_)

logger.setLevel(logging.INFO)

handler = logging.StreamHandler()

handler.setFormatter(

logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")

)

logger.addHandler(handler)

########################

\# Helper functions

########################

def get\_checkpoint(training\_args: DPOConfig):

last\_checkpoint = None

if os.path.isdir(training\_args.output\_dir):

last\_checkpoint = get\_last\_checkpoint(training\_args.output\_dir)

return last\_checkpoint

def dpo\_function(

model\_args: ModelConfig, script\_args: ScriptArguments, training\_args: DPOConfig

):

#########################

\# Log parameters

#########################

logger.info(f"Model parameters {model\_args}")

logger.info(f"Training/evaluation parameters {training\_args}")

###############

\# Load datasets

###############

if script\_args.dataset\_id\_or\_path.endswith(".json"):

train\_dataset = load\_dataset(

"json", data\_files=script\_args.dataset\_id\_or\_path, split="train"

)

else:

train\_dataset = load\_dataset(

script\_args.dataset\_id\_or\_path, split=script\_args.dataset\_splits

)

logger.info(

f"Loaded dataset with {len(train\_dataset)} samples and the following features: {train\_dataset.features}"

)

################

\# Load tokenizer

################

tokenizer = AutoTokenizer.from\_pretrained(

(

script\_args.tokenizer\_name\_or\_path

if script\_args.tokenizer\_name\_or\_path

else model\_args.model\_name\_or\_path

),

revision=model\_args.model\_revision,

trust\_remote\_code=model\_args.trust\_remote\_code,

)

if tokenizer.pad\_token is None:

tokenizer.pad\_token = tokenizer.eos\_token

#####################

\# Prepare and format dataset

#####################

def format\_dpo\_sample(sample):

prompt = tokenizer.apply\_chat\_template(

\[

{"role": "system", "content": sample\["system\_prompt"\]},

{"role": "user", "content": sample\["prompt"\]},

\],

tokenize=False,

)

chosen = tokenizer.apply\_chat\_template(

\[{"role": "user", "content": sample\["chosen"\]}\], tokenize=False

)

rejected = tokenizer.apply\_chat\_template(

\[{"role": "user", "content": sample\["rejected"\]}\], tokenize=False

)

return {"prompt": prompt, "chosen": chosen, "rejected": rejected}

\# For DPO/ORPO, the inputs are triples of (prompt, chosen, rejected), where \`chosen\` and \`rejected\` are the final turn of a dialogue

train\_dataset = train\_dataset.map(

format\_dpo\_sample, remove\_columns=train\_dataset.column\_names

)

\# remove all columns except chosen, rejected

print(f"Columns: {train\_dataset.features.keys()}")

train\_dataset = train\_dataset.select\_columns(\["prompt", "chosen", "rejected"\])

#######################################

\# Load the model and/or reference model

#######################################

model\_kwargs = dict(

revision=model\_args.model\_revision, # What revision from Huggingface to use, defaults to main

trust\_remote\_code=model\_args.trust\_remote\_code, # Whether to trust the remote code, this also you to fine-tune custom architectures

attn\_implementation=model\_args.attn\_implementation, # What attention implementation to use, defaults to flash\_attention\_2

torch\_dtype=(

model\_args.torch\_dtype

if model\_args.torch\_dtype in \["auto", None\]

else getattr(torch, model\_args.torch\_dtype)

), # What torch dtype to use, defaults to auto

use\_cache=False if training\_args.gradient\_checkpointing else True, # Whether

low\_cpu\_mem\_usage=(

True

if not strtobool(os.environ.get("ACCELERATE\_USE\_DEEPSPEED", "false"))

else None

), # Reduces memory usage on CPU for loading the model

)

\# Check which training method to use and if 4-bit quantization is needed

if model\_args.load\_in\_4bit:

model\_kwargs\["quantization\_config"\] = BitsAndBytesConfig(

load\_in\_4bit=True,

bnb\_4bit\_use\_double\_quant=True,

bnb\_4bit\_quant\_type="nf4",

bnb\_4bit\_compute\_dtype=model\_kwargs\["torch\_dtype"\],

bnb\_4bit\_quant\_storage=model\_kwargs\["torch\_dtype"\],

)

if model\_args.use\_peft:

peft\_config = get\_peft\_config(model\_args)

else:

peft\_config = None

\# Policy Model

model = AutoModelForCausalLM.from\_pretrained(

model\_args.model\_name\_or\_path, \*\*model\_kwargs

)

\# Checks wether we use adapters for reference model or not

if peft\_config is None:

model\_ref = AutoModelForCausalLM.from\_pretrained(

model\_args.model\_name\_or\_path, \*\*model\_kwargs

)

else:

model\_ref = None

#########################

\# Instantiate DPO trainer

#########################

trainer = DPOTrainer(

model,

ref\_model=model\_ref,

args=training\_args,

train\_dataset=train\_dataset,

processing\_class=tokenizer,

peft\_config=peft\_config,

)

###############

\# Training loop

###############

\# Check for last checkpoint

last\_checkpoint = get\_checkpoint(training\_args)

if last\_checkpoint is not None and training\_args.resume\_from\_checkpoint is None:

logger.info(f"Checkpoint detected, resuming training at {last\_checkpoint}.")

\# Train the model

logger.info(

f'\*\*\* Starting training {datetime.now().strftime("%Y-%m-%d %H:%M:%S")} for {training\_args.num\_train\_epochs} epochs\*\*\*'

)

train\_result = trainer.train(resume\_from\_checkpoint=last\_checkpoint)

\# Log and save metrics

metrics = train\_result.metrics

metrics\["train\_samples"\] = len(train\_dataset)

trainer.log\_metrics("train", metrics)

trainer.save\_metrics("train", metrics)

trainer.save\_state()

logger.info("\*\*\* Training complete \*\*\*")

##################################

\# Save model and create model card

##################################

logger.info("\*\*\* Save model \*\*\*")

if trainer.is\_fsdp\_enabled and peft\_config:

trainer.accelerator.state.fsdp\_plugin.set\_state\_dict\_type("FULL\_STATE\_DICT")

\# Restore k,v cache for fast inference

trainer.model.config.use\_cache = True

trainer.save\_model(training\_args.output\_dir)

logger.info(f"Model saved to {training\_args.output\_dir}")

training\_args.distributed\_state.wait\_for\_everyone() # wait for all processes to load

tokenizer.save\_pretrained(training\_args.output\_dir)

logger.info(f"Tokenizer saved to {training\_args.output\_dir}")

\# Save everything else on main process

if trainer.accelerator.is\_main\_process:

trainer.create\_model\_card({"tags": \["sft", "tutorial", "philschmid"\]})

\# push to hub if needed

if training\_args.push\_to\_hub is True:

logger.info("Pushing to hub...")

trainer.push\_to\_hub()

logger.info("\*\*\* Training complete! \*\*\*")

def main():

parser = TrlParser((ModelConfig, ScriptArguments, DPOConfig))

model\_args, script\_args, training\_args = parser.parse\_args\_and\_config()

\# Set seed for reproducibility

set\_seed(training\_args.seed)

\# Run the main training loop

dpo\_function(model\_args, script\_args, training\_args)

if \_\_name\_\_ == "\_\_main\_\_":

main()