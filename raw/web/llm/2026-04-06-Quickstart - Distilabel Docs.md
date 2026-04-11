---
author:
- null
- '[[Argilla]]'
- '[[Inc.]]'
created: 2026-04-06
created_at: 2026-04-06
description: Distilabel is an AI Feedback (AIF) framework for building datasets with
  and for LLMs.
source_type: web
status: inbox
tags:
- null
- clippings
title: Quickstart - Distilabel Docs
topics:
- 大语言模型
source_url: https://distilabel.argilla.io/latest/sections/getting_started/quickstart/
published_at: null
related_concepts: []
---

## Quickstart

Distilabel provides all the tools you need to your scalable and reliable pipelines for synthetic data generation and AI-feedback. Pipelines are used to generate data, evaluate models, manipulate data, or any other general task. They are made up of different components: Steps, Tasks and LLMs, which are chained together in a directed acyclic graph (DAG).

- **Steps**: These are the building blocks of your pipeline. Normal steps are used for basic executions like loading data, applying some transformations, or any other general task.
- **Tasks**: These are steps that rely on LLMs and prompts to perform generative tasks. For example, they can be used to generate data, evaluate models or manipulate data.
- **LLMs**: These are the models that will perform the task. They can be local or remote models, and open-source or commercial models.

Pipelines are designed to be scalable and reliable. They can be executed in a distributed manner, and they can be cached and recovered. This is useful when dealing with large datasets or when you want to ensure that your pipeline is reproducible.

Besides that, pipelines are designed to be modular and flexible. You can easily add new steps, tasks, or LLMs to your pipeline, and you can also easily modify or remove them. An example architecture of a pipeline to generate a dataset of preferences is the following:

## Installation

To install the latest release with `hf-inference-endpoints` extra of the package from PyPI you can use the following command:

```sh
pip install distilabel[hf-inference-endpoints] --upgrade
```

## Use a generic pipeline

To use a generic pipeline for an ML task, you can use the `InstructionResponsePipeline` class. This class is a generic pipeline that can be used to generate data for supervised fine-tuning tasks. It uses the `InferenceEndpointsLLM` class to generate data based on the input data and the model.

```python
from distilabel.pipeline import InstructionResponsePipeline

pipeline = InstructionResponsePipeline()
dataset = pipeline.run()
```

The `InstructionResponsePipeline` class will use the `InferenceEndpointsLLM` class with the model `meta-llama/Meta-Llama-3.1-8B-Instruct` to generate data based on the system prompt. The output data will be a dataset with the columns `instruction` and `response`. The class uses a generic system prompt, but you can customize it by passing the `system_prompt` parameter to the class.

Note

We're actively working on building more pipelines for different tasks. If you have any suggestions or requests, please let us know! We're currently working on pipelines for classification, Direct Preference Optimization, and Information Retrieval tasks.

## Define a Custom pipeline

In this guide we will walk you through the process of creating a simple pipeline that uses the [InferenceEndpointsLLM](https://distilabel.argilla.io/latest/api/models/llm/llm_gallery/#distilabel.models.llms.InferenceEndpointsLLM) class to generate text. The [Pipeline](https://distilabel.argilla.io/latest/api/pipeline/#distilabel.pipeline.local.Pipeline) will process a dataset loaded directly using the Hugging Face `datasets` library and use the [InferenceEndpointsLLM](https://distilabel.argilla.io/latest/api/models/llm/llm_gallery/#distilabel.models.llms.InferenceEndpointsLLM) class to generate text using the [TextGeneration](https://distilabel.argilla.io/latest/api/task/task_gallery/#distilabel.steps.tasks.TextGeneration) task.

> You can check the available models in the [Hugging Face Model Hub](https://huggingface.co/models?pipeline_tag=text-generation&sort=trending) and filter by `Inference status`.

```python
from datasets import load_dataset

from distilabel.models import InferenceEndpointsLLM
from distilabel.pipeline import Pipeline
from distilabel.steps.tasks import TextGeneration

with Pipeline() as pipeline: # 
    TextGeneration( # 
        llm=InferenceEndpointsLLM(
            model_id="meta-llama/Meta-Llama-3.1-8B-Instruct",
            generation_kwargs={"temperature": 0.7, "max_new_tokens": 512},
        ),
    )

if __name__ == "__main__":
    dataset = load_dataset("distilabel-internal-testing/instructions", split="test") # 
    distiset = pipeline.run(dataset=dataset)
    distiset.push_to_hub(repo_id="distilabel-example") #
```