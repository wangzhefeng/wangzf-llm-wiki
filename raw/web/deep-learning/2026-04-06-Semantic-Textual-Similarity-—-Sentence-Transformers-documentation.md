---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: null
source_type: web
status: inbox
tags:
- null
- clippings
title: Semantic Textual Similarity — Sentence Transformers  documentation
source_url: https://www.sbert.net/examples/sentence_transformer/training/sts/README.html
published_at: null
related_concepts: []
topics:
  - deep-learning
  - 深度学习理论
---

## Semantic Textual Similarity

Semantic Textual Similarity (STS) assigns a score on the similarity of two texts. In this example, we use the [stsb](https://huggingface.co/datasets/sentence-transformers/stsb) dataset as training data to fine-tune our model. See the following example scripts how to tune SentenceTransformer on STS data:

- **[training\_stsbenchmark.py](https://github.com/huggingface/sentence-transformers/tree/main/examples/sentence_transformer/training/sts/training_stsbenchmark.py)** - This example shows how to create a SentenceTransformer model from scratch by using a pre-trained transformer model (e.g. [`distilbert-base-uncased`](https://huggingface.co/distilbert/distilbert-base-uncased)) together with a pooling layer.
- **[training\_stsbenchmark\_continue\_training.py](https://github.com/huggingface/sentence-transformers/tree/main/examples/sentence_transformer/training/sts/training_stsbenchmark_continue_training.py)** - This example shows how to continue training on STS data for a previously created & trained SentenceTransformer model (e.g. [`all-mpnet-base-v2`](https://huggingface.co/sentence-transformers/all-mpnet-base-v2)).

You can also train and use [`CrossEncoder`](https://www.sbert.net/docs/package_reference/cross_encoder/cross_encoder.html#sentence_transformers.cross_encoder.CrossEncoder "sentence_transformers.cross_encoder.CrossEncoder") models for this task. See [Cross Encoder > Training Examples > Semantic Textual Similarity](https://www.sbert.net/examples/cross_encoder/training/sts/README.html) for more details.

## Training data

In STS, we have sentence pairs annotated together with a score indicating the similarity. In the original STSbenchmark dataset, the scores range from 0 to 5. We have normalized these scores to range between 0 and 1 in [stsb](https://huggingface.co/datasets/sentence-transformers/stsb), as that is required for [`CosineSimilarityLoss`](https://www.sbert.net/docs/package_reference/sentence_transformer/losses.html#sentence_transformers.losses.CosineSimilarityLoss "sentence_transformers.losses.CosineSimilarityLoss") as you can see in the [Loss Overiew](https://www.sbert.net/docs/sentence_transformer/loss_overview.html).

Here is a simplified version of our training data:

```python
from datasets import Dataset

sentence1_list = ["My first sentence", "Another pair"]
sentence2_list = ["My second sentence", "Unrelated sentence"]
labels_list = [0.8, 0.3]
train_dataset = Dataset.from_dict({
    "sentence1": sentence1_list,
    "sentence2": sentence2_list,
    "label": labels_list,
})
# => Dataset({
#     features: ['sentence1', 'sentence2', 'label'],
#     num_rows: 2
# })
print(train_dataset[0])
# => {'sentence1': 'My first sentence', 'sentence2': 'My second sentence', 'label': 0.8}
print(train_dataset[1])
# => {'sentence1': 'Another pair', 'sentence2': 'Unrelated sentence', 'label': 0.3}
```

In the aforementioned scripts, we directly load the [stsb](https://huggingface.co/datasets/sentence-transformers/stsb) dataset:

```python
from datasets import load_dataset

train_dataset = load_dataset("sentence-transformers/stsb", split="train")
# => Dataset({
#     features: ['sentence1', 'sentence2', 'score'],
#     num_rows: 5749
# })
```

## Loss Function

We use [`CosineSimilarityLoss`](https://www.sbert.net/docs/package_reference/sentence_transformer/losses.html#sentence_transformers.losses.CosineSimilarityLoss "sentence_transformers.losses.CosineSimilarityLoss") as our loss function.

![[SBERT_Siamese_Network.png|SBERT Siamese Network Architecture]]

For each sentence pair, we pass sentence A and sentence B through the BERT-based model, which yields the embeddings *u* und *v*. The similarity of these embeddings is computed using cosine similarity and the result is compared to the gold similarity score. Note that the two sentences are fed through the same model rather than two separate models. In particular, the cosine similarity for similar texts is maximized and the cosine similarity for dissimilar texts is minimized. This allows our model to be fine-tuned and to recognize the similarity of sentences.

For more details, see [Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks](https://huggingface.co/papers/1908.10084).

[`CoSENTLoss`](https://www.sbert.net/docs/package_reference/sentence_transformer/losses.html#sentence_transformers.losses.CoSENTLoss "sentence_transformers.losses.CoSENTLoss") and [`AnglELoss`](https://www.sbert.net/docs/package_reference/sentence_transformer/losses.html#sentence_transformers.losses.AnglELoss "sentence_transformers.losses.AnglELoss") are more modern variants of [`CosineSimilarityLoss`](https://www.sbert.net/docs/package_reference/sentence_transformer/losses.html#sentence_transformers.losses.CosineSimilarityLoss "sentence_transformers.losses.CosineSimilarityLoss") that accept the same data format of a sentence pair with a similarity score ranging from 0.0 to 1.0. Informal experiments indicate that these two produce stronger models than [`CosineSimilarityLoss`](https://www.sbert.net/docs/package_reference/sentence_transformer/losses.html#sentence_transformers.losses.CosineSimilarityLoss "sentence_transformers.losses.CosineSimilarityLoss").