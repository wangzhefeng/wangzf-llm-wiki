---
source_type: web
title: "RLHF and alternatives: ORPO"
author:
  - 
  - "[[Argilla S.L.U.]]"
created_at: 2026-04-06
status: inbox
created: 2026-04-06
description: "open-source tool for data-centric NLP"
tags:
  - 
  - "clippings"
source_url: "https://argilla.io/blog/mantisnlp-rlhf-part-8/"
published_at: 2024-04-05
related_concepts: []
topics:
  - llm-post-training
  - 大语言模型后训练
---

## Introduction

This is a series of blog posts related to alternatives to Reinforcement Learning by Human Feedback, created as a joint effort between Argilla and [MantisNLP](https://mantisnlp.com/) teams. Please ensure you have gone through the previous entries in the series to fully understand the context and progression of the discussion before moving on to this segment. Scroll to the bottom of the page to go to the next blog post of the series.

In previous posts, we started by analyzing the efforts to carry out Supervised Fine-tuning (**SFT**) and Reinforcement Learning with Human Feedback (**RLHF**), and the importance of having high-quality data ([first](https://argilla.io/blog/mantisnlp-rlhf-part-1/) and [second](https://argilla.io/blog/mantisnlp-rlhf-part-2/) blog posts). Nevertheless, RLHF is complex and usually unstable, so we examined a promising alternative, Direct Preference Optimization (**DPO**), to align the LLM with human preferences without requiring RL ([third](https://argilla.io/blog/mantisnlp-rlhf-part-3/) blog post). Still, DPO does not solve all the shortcomings, for instance, a large amount of preference data is needed to fine-tune. To tackle this, researchers have come up with new methods. Some of them are Reinforcement Learning AI Feedback (**RLAIF**) or Self-Play Fine-Tuning (**SPIN**) ([fourth](https://argilla.io/blog/mantisnlp-rlhf-part-4/) and [fifth](https://argilla.io/blog/mantisnlp-rlhf-part-5/) blog posts). For better data alignment, we also explored the benefits of Identity Preference Optimization **(IPO)** and Kahneman-Tversky Optimization (**KTO**) ([sixth](https://argilla.io/blog/mantisnlp-rlhf-part-6/) and [seventh](https://argilla.io/blog/mantisnlp-rlhf-part-7/) blog posts).

To improve the process, several approaches have been developed from different perspectives. However, have you ever thought about implementing RL directly during the SFT? That’s exactly what **Odds Ratio Preference Optimization (ORPO)** suggests.

## SFT’s Role in Model Alignment Techniques

Currently, the number of models is continually increasing, and training each one demands significant resources and time. So when we want to tailor them to our needs, we apply **instruction tuning and preference alignment**. First, we fine-tune the model with instructions specific to the task we want it to perform. Then, through preference tuning, we improve its responses, ensuring they’re accurate and steer clear of any harmful or unethical content, and optimizing its performance across other NLP tasks.

However, this approach involves **several models and training stages** to achieve the expected results (think RLHF with its SFT, RM, and PPO steps, or DPO with its SFT and DPO stages). And, in the center of all of them, **SFT plays a crucial role** in achieving a successful convergence.

![[raw/assets/attachments/reinforcementlearning/part-8-alignments.png]] *Comparison of model alignment techniques. Source: [https://arxiv.org/html/2403.07691v2](https://arxiv.org/html/2403.07691v2).*

Although previous studies had already shed light on the relevance of **SFT** in alignment, the researchers analyzed it in deep and found a shortcoming. SFT **increased the likelihood of obtaining the desired tokens, but it also raised the probability of generating undesired outcomes**. This led to the search for a mechanism that would still adapt the models to the specific domain, but at the same time penalize undesired responses. This is how **ORPO** came about.

![[raw/assets/attachments/reinforcementlearning/part-8-sft.png]] *Log probabilities for chosen and rejected responses during OPT-350M model fine-tuning on HH-RLHF dataset. Source: [https://arxiv.org/html/2403.07691v2](https://arxiv.org/html/2403.07691v2).*

## Odds Ratio Preference Optimization (ORPO)

> You can check the official GitHub repository [here](https://github.com/xfactlab/orpo). If you're looking to dive into a practical aspect, the ORPO feature is already integrated into the [ORPO trainer](https://huggingface.co/docs/trl/main/en/orpo_trainer) within the TRL library by Hugging Face.

ORPO **combines instruction tuning and preference alignment in a single process**, making it reference model-free and computationally more efficient. It is not only more efficient in terms of resources but also saves memory and should perform fewer FLOPs.

ORPO creates a new objective by using an odds ratio-based loss to penalize undesirable responses along with conventional negative log-likelihood loss (NLL), allowing it to distinguish between favorable and unfavorable responses. Thus, it includes two main components:

- **SFT loss:** The NLL loss function for conventional language causal modeling, maximizes the probability of generating the reference tokens.
- **Relative ratio loss**: Maximizes the odds ratio between the generation of the favored and the disfavored response.

Together, these components guide the LLM to adapt to the desired generations for the specific domain and disfavor the generations in the set of rejected responses.

## Does ORPO really work?

To evaluate this method, researchers looked at how it performed across various model sizes, from the smaller 125-M parameter models to the large 1.3-B parameter ones, and used the Anthropic's HH-RLHF and Binarized UltraFeedback (and [Argilla’s cleaned version](https://huggingface.co/datasets/argilla/ultrafeedback-binarized-preferences-cleaned)) preference datasets. The findings showed that ORPO **outperformed other algorithms**. When using the AlpacaEval benchmark to follow instructions, ORPO got better results on models such as Phi-2, Llama-2, or Mistral, especially on the latter, where it achieved 12.20% on AlpacaEval2.0. In multi-turn instruction-following tasks, ORPO was also impressive, achieving scores comparable to those of other large language models with a 7.32 on MT-Bench, despite not being trained on multi-turn conversation data.

![[raw/assets/attachments/reinforcementlearning/part-8-mtbench.png]] *MT-Bench result of Mistral-ORPO-α (7B) and Mistral-ORPO-β (7B) by the category. Mistral-ORPO-α is fine-tuned exclusively on [HuggingFaceH4/ultrafeedback\_binarized](https://huggingface.co/datasets/HuggingFaceH4/ultrafeedback_binarized); while Mistral-ORPO-β is fine-tuned exclusively on the 61k instances of the cleaned version of UltraFeedback, [argilla/ultrafeedback-binarized-preferences-cleaned](https://huggingface.co/datasets/argilla/ultrafeedback-binarized-preferences-cleaned) by Argilla. Source: [https://arxiv.org/html/2403.07691v2](https://arxiv.org/html/2403.07691v2).*

When comparing the **win rate and reward distribution** of ORPO with those of SFT, PPO, and DPO, an increase was observed across all model sizes in both data sets. In the first case, ORPO was preferred over SFT and PPO, reaching a maximum win rate of 85%; while the win rate of DPO showed a proportional increase with model size. Moreover, upon examining **lexical diversity**, it became apparent that ORPO tended to assign higher probabilities to desirable tokens and to generate more specific responses.

![[raw/assets/attachments/reinforcementlearning/part-8-winrate.png]] *AlpacaEval 2.0 score for the models trained with different alignment methods. Source: [https://arxiv.org/html/2403.07691v2](https://arxiv.org/html/2403.07691v2).*

### Some limitations

While ORPO has demonstrated encouraging results, its **generalizability** across various tasks, and domains, or when scaled to larger language models, remains to be thoroughly examined. A broader **comparative analysis** with other preference alignment algorithms beyond the commonly referenced DPO and RLHF would be beneficial. Additionally, exploring the potential **integration** of ORPO with these algorithms could provide valuable insights.

## Conclusions

ORPO, with its novel approach based on likelihood ratios, offers a fresh perspective on model alignment that could lead to significant efficiency gains in resources. Its methodology is straightforward yet effective, enabling the fine-tuning of language models to not only specific domains but also to align their responses. In a context where LLMs are becoming more numerous and experimentation more frequent, ORPO presents itself as a valuable alternative. Although further research and experiments are needed, the results so far are promising.

## Want to know more?

This is the eighth entry of a series of blog posts dedicated to alternatives to RLHF. The [first](https://argilla.io/blog/mantisnlp-rlhf-part-1), [second](https://argilla.io/blog/mantisnlp-rlhf-part-2), [third](https://argilla.io/blog/mantisnlp-rlhf-part-3), [fourth](https://argilla.io/blog/mantisnlp-rlhf-part-4), [fifth](https://argilla.io/blog/mantisnlp-rlhf-part-5), [sixth](https://argilla.io/blog/mantisnlp-rlhf-part-6), and [seventh](https://argilla.io/blog/mantisnlp-rlhf-part-7) posts of the series can be found on our website too.

Argilla and Mantis NLP teams are happy to help with any question you may have about preparation steps for training a LLM using Supervised fine-tuning, Reinforcement Learning, or Direct Preference Optimization.

All the data curation steps are currently supported by Argilla’s Data Platform for LLM, and from Mantis NLP we offer end-to-end support for the whole process.