---
source_type: web
title: "Word Embeddings"
author: 
created_at: 2026-04-06
topics:
  - 大语言模型
status: inbox
source: "https://lena-voita.github.io/nlp_course/word_embeddings.html#main_content"
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
---

![[raw/assets/attachments/llm/word_repr_intro-min.png]]

The way machine learning models " see " data is different from how we (humans) do. For example, we can easily understand the text "I saw a cat", but our models can not - they need vectors of features. Such vectors, or word embeddings, are representations of words which can be fed into your model.

  
![[raw/assets/attachments/llm/lookup_table.gif]]

#### How it works: Look-up Table (Vocabulary)

In practice, you have a vocabulary of allowed words; you choose this vocabulary in advance. For each vocabulary word, a look-up table contains its embedding. This embedding can be found using the word index in the vocabulary (i.e., you to look up the embedding in the table using word index).

![[raw/assets/attachments/llm/unk_in_voc-min.png]]

To account for unknown words (the ones which are not in the vocabulary), usually a vocabulary contains a special token UNK. Alternatively, unknown tokens can be ignored or assigned a zero vector.

### The main question of this lecture is: how do we get these word vectors?

  

## Represent as Discrete Symbols: One-hot Vectors

![[raw/assets/attachments/llm/one_hot-min.png]]

The easiest you can do is to represent words as one-hot vectors: for the i-th word in the vocabulary, the vector has 1 on the i-th dimension and 0 on the rest. In Machine Learning, this is the most simple way to represent categorical features.

You probably can guess why one-hot vectors are not the best way to represent words. One of the problems is that for large vocabularies, these vectors will be very long: vector dimensionality is equal to the vocabulary size. This is undesirable in practice, but this problem is not the most crucial one.

What is really important, is that these vectors know nothing about the words they represent. For example, one-hot vectors "think" that cat is as close to dog as it is to table! We can say that one-hot vectors do not capture meaning.

But how do we know what is meaning?

  

## Distributional Semantics

To capture meaning of words in their vectors, we first need to define the notion of meaning that can be used in practice. For this, let us try to understand how we, humans, get to know which words have similar meaning.

How to: go over the slides at your pace. Try to notice how your brain works.

Lena: The example is from [Jacob Eisenstein's NLP notes;](https://github.com/jacobeisenstein/gt-nlp-class/blob/master/notes/eisenstein-nlp-notes.pdf) the tezgüino example originally appeared in [Lin, 1998](https://www.aclweb.org/anthology/C98-2122.pdf).

  
  

Once you saw how the unknown word used in different contexts, you were able to understand it's meaning. How did you do this?

The hypothesis is that your brain searched for other words that can be used in the same contexts, found some (e.g., wine), and made a conclusion that tezgüino has meaning similar to those other words. This is the distributional hypothesis:

Words which frequently appear in **similar contexts** have **similar meaning**.

Lena: Often you can find it formulated as "You shall know a word by the company it keeps" with the reference to J. R. Firth in 1957, but actually there were a lot more people responsible, and much earlier. For example, [Harris, 1954.](https://www.tandfonline.com/doi/pdf/10.1080/00437956.1954.11659520)

This is an extremely valuable idea: it can be used in practice to make word vectors capture their meaning. According to the distributional hypothesis, "to capture meaning" and "to capture contexts" are inherently the same. Therefore, all we need to do is to put information about word contexts into word representation.

Main idea: We need to put information about word contexts into word representation.

All we'll be doing at this lecture is looking at different ways to do this.

  

## Count-Based Methods

![[raw/assets/attachments/llm/idea-min.png]]

Let's remember our main idea:

Main idea: We have to put information about contexts into word vectors.

Count-based methods take this idea quite literally:

How: Put this information **manually** based on global corpus statistics.

The general procedure is illustrated above and consists of the two steps: (1) construct a word-context matrix, (2) reduce its dimensionality. There are two reasons to reduce dimensionality. First, a raw matrix is very large. Second, since a lot of words appear in only a few of possible contexts, this matrix potentially has a lot of uninformative elements (e.g., zeros).

To estimate similarity between words/contexts, usually you need to evaluate the dot-product of normalized word/context vectors (i.e., cosine similarity).

To define a count-based method, we need to define two things:

- possible contexts (including what does it mean that a word appears in a context),
- the notion of association, i.e., formulas for computing matrix elements.

Below we provide a couple of popular ways of doing this.

  

## Simple: Co-Occurence Counts

![[raw/assets/attachments/llm/window-min.png]]

The simplest approach is to define contexts as each word in an L-sized window. Matrix element for a word-context pair (w, c) is the number of times w appears in context c. This is the very basic (and very, very old) method for obtaining embeddings.

The (once) famous HAL model (1996) is also a modification of this approach. Learn more from [this exercise](#research_improve_count_based) in the [Research Thinking](#research_thinking) section.

## Positive Pointwise Mutual Information (PPMI)

![[raw/assets/attachments/llm/define_ppmi-min.png]]

Here contexts are defined as before, but the measure of the association between word and context is more clever: positive PMI (or PPMI for short). PPMI measure is widely regarded as state-of-the-art for pre-neural distributional-similarity models.

  
  

Important: relation to neural models!  
Turns out, some of the neural methods we will consider (Word2Vec) were shown to implicitly approximate the factorization of a (shifted) PMI matrix. Stay tuned!

  

## Latent Semantic Analysis (LSA): Understanding Documents

![[raw/assets/attachments/llm/lsa-min.png]]

[Latent Semantic Analysis (LSA)](http://lsa.colorado.edu/papers/JASIS.lsi.90.pdf) analyzes a collection of documents. While in the previous approaches contexts served only to get word vectors and were thrown away afterward, here we are also interested in context, or, in this case, document vectors. LSA is one of the simplest topic models: cosine similarity between document vectors can be used to measure similarity between documents.

The term "LSA" sometimes refers to a more general approach of applying SVD to a term-document matrix where the term-document elements can be computed in different ways (e.g., simple co-occurrence, tf-idf, or some other weighting).

Animation alert! [LSA wikipedia page](https://en.wikipedia.org/wiki/Latent_semantic_analysis) has a nice animation of the topic detection process in a document-word matrix - take a look!

  
  

## Word2Vec: a Prediction-Based Method

Let us remember our main idea again:

Main idea: We have to put information about contexts into word vectors.

While count-based methods took this idea quite literally, Word2Vec uses it in a different manner:

How: **Learn** word vectors by teaching them to **predict contexts**.

![[raw/assets/attachments/llm/intro-min.png]]

Word2Vec is a model whose parameters are word vectors. These parameters are optimized iteratively for a certain objective. The objective forces word vectors to "know" contexts a word can appear in: the vectors are trained to predict possible contexts of the corresponding words. As you remember from the distributional hypothesis, if vectors "know" about contexts, they "know" word meaning.

Word2Vec is an iterative method. Its main idea is as follows:

- take a huge text corpus;
- go over the text with a sliding window, moving one word at a time. At each step, there is a central word and context words (other words in this window);
- for the central word, compute probabilities of context words;
- adjust the vectors to increase these probabilities.
  

How to: go over the illustration to understand the main idea.

Lena: Visualization idea is from [the Stanford CS224n course.](http://web.stanford.edu/class/cs224n/index.html#schedule)

  
  

## Objective Function: Negative Log-Likelihood

For each position $t = 1 , \ldots , T$ in a text corpus, Word2Vec predicts context words within a m-sized window given the central word $w_{t}$: 
$$
\text{Likelihood} = L \left(\right. \theta \left.\right) = \prod_{t = 1}^{T} \underset{- m \leq j \leq m , j \neq 0}{\prod} P \left(\right. w_{t + j} \left|\right. w_{t} , \theta \left.\right) ,
$$
 where $\theta$ are all variables to be optimized. The objective function (aka loss function or cost function) $J \left(\right. \theta \left.\right)$ is the average negative log-likelihood:

![[raw/assets/attachments/llm/loss_with_the_plan-min.png]]

Note how well the loss agrees with our plan main above: go over text with a sliding window and compute probabilities. Now let's find out how to compute these probabilities.

![[raw/assets/attachments/llm/two_vocs_with_theta-min.png]]

### How to calculate P(wt+j|wt,θ)?

For each word $w$ we will have two vectors:

- $v_{w}$ when it is a central word;
- $u_{w}$ when it is a context word.

(Once the vectors are trained, usually we throw away context vectors and use only word vectors.)

Then for the central word $c$ (c - central) and the context word $o$ (o - outside word) probability of the context word is

![[raw/assets/attachments/llm/prob_o_c-min.png]]  

Note: this is the softmax function! (click for the details)

The function above is an example of the softmax function: 
$$
s o f t m a x \left(\right. x_{i} \left.\right) = \frac{exp ⁡ \left(\right. x_{i} \left.\right)}{\sum_{j = i}^{n} exp ⁡ \left(\right. x_{j} \left.\right)} .
$$
 Softmax maps arbitrary values $x_{i}$ to a probability distribution $p_{i}$:

- "max" because the largest $x_{i}$ will have the largest probability $p_{i}$;
- "soft" because all probabilities are non-zero.

You will deal with this function quite a lot over the NLP course (and in Deep Learning in general).

  

How to: go over the illustration. Note that for central words and context words, different vectors are used. For example, first the word **a** is central and we use $v_{a}$, but when it becomes context, we use $u_{a}$ instead.

  
  

## How to train: by Gradient Descent, One Word at a Time

Let us recall that our parameters $\theta$ are vectors $v_{w}$ and $u_{w}$ for all words in the vocabulary. These vectors are learned by optimizing the training objective via gradient descent (with some learning rate $\alpha$): 
$$
\theta^{n e w} = \theta^{o l d} - \alpha \nabla_{\theta} J \left(\right. \theta \left.\right) .
$$

### One word at a time

We make these updates one at a time: each update is for a single pair of a center word and one of its context words. Look again at the loss function: 
$$
\text{Loss} = J \left(\right. \theta \left.\right) = - \frac{1}{T} log ⁡ L \left(\right. \theta \left.\right) = - \frac{1}{T} \sum_{t = 1}^{T} \underset{- m \leq j \leq m , j \neq 0}{\sum} log ⁡ P \left(\right. w_{t + j} \left|\right. w_{t} , \theta \left.\right) = \frac{1}{T} \sum_{t = 1}^{T} \underset{- m \leq j \leq m , j \neq 0}{\sum} J_{t , j} \left(\right. \theta \left.\right) .
$$
 For the center word $w_{t}$, the loss contains a distinct term $J_{t , j} \left(\right. \theta \left.\right) = - log ⁡ P \left(\right. w_{t + j} \left|\right. w_{t} , \theta \left.\right)$ for each of its context words $w_{t + j}$. Let us look in more detail at just this one term and try to understand how to make an update for this step. For example, let's imagine we have a sentence

![[raw/assets/attachments/llm/sent_cat_central-min.png]]

with the central word cat, and four context words. Since we are going to look at just one step, we will pick only one of the context words; for example, let's take cute. Then the loss term for the central word cat and the context word cute is: 
$$
J_{t , j} \left(\right. \theta \left.\right) = - log ⁡ P \left(\right. c u t e \left|\right. c a t \left.\right) = - log ⁡ \frac{exp u_{c u t e}^{T} v_{c a t}}{\underset{w \in V o c}{\sum} exp ⁡ u_{w}^{T} v_{c a t}} = - u_{c u t e}^{T} v_{c a t} + log ⁡ \underset{w \in V o c}{\sum} exp ⁡ u_{w}^{T} v_{c a t} .
$$

Note which parameters are present at this step:

- from vectors for central words, only $v_{c a t}$;
- from vectors for context words, all $u_{w}$ (for all words in the vocabulary).

Only these parameters will be updated at the current step.

Below is the schematic illustration of the derivations for this step.

![[raw/assets/attachments/llm/one_step_alg-min.png]]

  
  
![[raw/assets/attachments/llm/loss_intuition-min.png]]

By making an update to minimize $J_{t , j} \left(\right. \theta \left.\right)$, we force the parameters to increase similarity (dot product) of $v_{c a t}$ and $u_{c u t e}$ and, at the same time, to decrease similarity between $v_{c a t}$ and $u_{w}$ for all other words $w$ in the vocabulary.

This may sound a bit strange: why do we want to decrease similarity between $v_{c a t}$ and all other words, if some of them are also valid context words (e.g., grey, playing, in on our example sentence)?  
But do not worry: since we make updates for each context word (and for all central words in your text), on average over all updates our vectors will learn the distribution of the possible contexts.

Try to derive the gradients at the final step of the illustration above.  
  
If you get lost, you can look at the paper [Word2Vec Parameter Learning Explained](https://arxiv.org/pdf/1411.2738.pdf).

  

## Faster Training: Negative Sampling

In the example above, for each pair of a central word and its context word, we had to update all vectors for context words. This is highly inefficient: for each step, the time needed to make an update is proportional to the vocabulary size.

But why do we have to consider all context vectors in the vocabulary at each step? For example, imagine that at the current step we consider context vectors not for all words, but only for the current target (cute) and several randomly chosen words. The figure shows the intuition.

![[raw/assets/attachments/llm/negative_sampling-min.png]]

  

As before, we are increasing similarity between $v_{c a t}$ and $u_{c u t e}$. What is different, is that now we decrease similarity between $v_{c a t}$ and context vectors not for all words, but only with a subset of K "negative" examples.

Since we have a large corpus, on average over all updates we will update each vector sufficient number of times, and the vectors will still be able to learn the relationships between words quite well.

Formally, the new loss function for this step is: 
$$
J_{t , j} \left(\right. \theta \left.\right) = - log ⁡ \sigma \left(\right. u_{c u t e}^{T} v_{c a t} \left.\right) - \underset{w \in \left{\right. w_{i_{1}} , \ldots , w_{i_{K}} \left.\right}}{\sum} log ⁡ \sigma \left(\right. - u_{w}^{T} v_{c a t} \left.\right) ,
$$
 where $w_{i_{1}} , \ldots , w_{i_{K}}$ are the K negative examples chosen at this step and $\sigma \left(\right. x \left.\right) = \frac{1}{1 + e^{- x}}$ is the sigmoid function.

Note that $\sigma \left(\right. - x \left.\right) = \frac{1}{1 + e^{x}} = \frac{1 \cdot e^{- x}}{\left(\right. 1 + e^{x} \left.\right) \cdot e^{- x}} = \frac{e^{- x}}{1 + e^{- x}} = 1 - \frac{1}{1 + e^{x}} = 1 - \sigma \left(\right. x \left.\right)$. Then the loss can also be written as: 
$$
J_{t , j} \left(\right. \theta \left.\right) = - log ⁡ \sigma \left(\right. u_{c u t e}^{T} v_{c a t} \left.\right) - \underset{w \in \left{\right. w_{i_{1}} , \ldots , w_{i_{K}} \left.\right}}{\sum} log ⁡ \left(\right. 1 - \sigma \left(\right. u_{w}^{T} v_{c a t} \left.\right) \left.\right) .
$$

How the gradients and updates change when using negative sampling?

  

### The Choice of Negative Examples

Each word has only a few "true" contexts. Therefore, randomly chosen words are very likely to be "negative", i.e. not true contexts. This simple idea is used not only to train Word2Vec efficiently but also in many other applications, some of which we will see later in the course.

Word2Vec randomly samples negative examples based on the empirical distribution of words. Let $U \left(\right. w \left.\right)$ be a unigram distribution of words, i.e. $U \left(\right. w \left.\right)$ is the frequency of the word $w$ in the text corpus. Word2Vec modifies this distribution to sample less frequent words more often: it samples proportionally to $U^{3 / 4} \left(\right. w \left.\right)$.

## Word2Vec variants: Skip-Gram and CBOW

There are two Word2Vec variants: Skip-Gram and CBOW.

Skip-Gram is the model we considered so far: it predicts context words given the central word. Skip-Gram with negative sampling is the most popular approach.

CBOW (Continuous Bag-of-Words) predicts the central word from the sum of context vectors. This simple sum of word vectors is called "bag of words", which gives the name for the model.

![[raw/assets/attachments/llm/cbow_skip-min.png]]

How the loss function and the gradients change for the CBOW model?  
  
If you get lost, you can again look at the paper [Word2Vec Parameter Learning Explained](https://arxiv.org/pdf/1411.2738.pdf).

## Additional Notes

The original Word2Vec papers are:

- [Efficient Estimation of Word Representations in Vector Space](https://arxiv.org/pdf/1301.3781.pdf)
- [Distributed Representations of Words and Phrases and their Compositionality](https://papers.nips.cc/paper/5021-distributed-representations-of-words-and-phrases-and-their-compositionality.pdf)

You can look into them for the details on the experiments, implementation and hyperparameters. Here we will provide some of the most important things you need to know.

### The Idea is Not New

The idea to learn word vectors (distributed representations) is not new. For example, there were attempts to learn word vectors as part of a larger network and then extract the embedding layer. (For the details on the previous methods, you can look, for example, at the summary in the original Word2Vec papers).

What was very unexpected in Word2Vec, is its ability to learn high-quality word vectors very fast on huge datasets and for large vocabularies. And of course, all the fun properties we will see in the [Analysis and Interpretability](#analysis_interpretability) section quickly made Word2Vec very famous.

### Why Two Vectors?

As you remember, in Word2Vec we train two vectors for each word: one when it is a central word and another when it is a context word. After training, context vectors are thrown away.

This is one of the tricks that made Word2Vec so simple. Look again at the loss function (for one step): 
$$
J_{t , j} \left(\right. \theta \left.\right) = - u_{c u t e}^{T} v_{c a t} - log ⁡ \underset{w \in V}{\sum} exp ⁡ u_{w}^{T} v_{c a t} .
$$
 When central and context words have different vectors, both the first term and dot products inside the exponents are linear with respect to the parameters (the same for the negative training objective). Therefore, the gradients are easy to compute.

Repeat the derivations (loss and the gradients) for the case with one vector for each word ($\forall w i n V , v_{w} = u_{w}$ ).

While the standard practice is to throw away context vectors, it was shown that averaging word and context vectors may be more beneficial. [More details are here.](#papers_good_old_classics)

### Better training

There's one more trick: learn more from [this exercise](#w2v_subsample_frequent) in the [Research Thinking](#research_thinking) section.

### Relation to PMI Matrix Factorization

Word2Vec SGNS (Skip-Gram with Negative Sampling) implicitly approximates the factorization of a (shifted) PMI matrix. [Learn more here.](#papers_good_old_classics)

### The Effect of Window Size

The size of the sliding window has a strong effect on the resulting vector similarities. For example, [this paper](https://arxiv.org/pdf/1510.00726.pdf) notes that larger windows tend to produce more topical similarities (i.e. **dog**, **bark** and **leash** will be grouped together, as well as **walked**, **run** and **walking**), while smaller windows tend to produce more functional and syntactic similarities (i.e. **Poodle**, **Pitbull**, **Rottweiler**, or **walking**, **running**, **approaching**).

### (Somewhat) Standard Hyperparameters

As always, the choice of hyperparameters usually depends on the task at hand; you can look at the original papers for more details.  
  
Somewhat standard setting is:
- Model: Skip-Gram with negative sampling;
- Number of negative examples: for smaller datasets, 15-20; for huge datasets (which are usually used) it can be 2-5.
- Embedding dimensionality: frequently used value is 300, but other variants (e.g., 100 or 50) are also possible. For theoretical explanation of the optimal dimensionality, take a look at the [Related Papers](#related_papers) section.
- Sliding window (context) size: 5-10.
  

## GloVe: Global Vectors for Word Representation

![[raw/assets/attachments/llm/idea-min 1.png]]

[The GloVe model](https://www.aclweb.org/anthology/D14-1162.pdf) is a combination of count-based methods and prediction methods (e.g., Word2Vec). Model name, GloVe, stands for "Global Vectors", which reflects its idea: the method uses global information from corpus to learn vectors.

[As we saw earlier](#simple_cooccurrence), the simplest count-based method uses co-occurrence counts to measure the association between word w and context c: N(w, c). GloVe also uses these counts to construct the loss function:

![[raw/assets/attachments/llm/glove_loss-min.png]]

Similar to Word2Vec, we also have different vectors for central and context words - these are our parameters. Additionally, the method has a scalar bias term for each word vector.

What is especially interesting, is the way GloVe controls the influence of rare and frequent words: loss for each pair (w, c) is weighted in a way that

- rare events are penalized,
- very frequent events are not over-weighted.

Lena: The loss function looks reasonable as it is, but [the original GloVe paper](https://www.aclweb.org/anthology/D14-1162.pdf) has very nice motivation leading to the above formula. I will not provide it here (I have to finish the lecture at some point, right?..), but you can read it yourself - it's really, really nice!

  

## Evaluation of Word Embeddings

How can we understand that one method for getting word embeddings is better than another? There are two types of evaluation (not only for word embeddings): intrinsic and extrinsic.

### Intrinsic Evaluation: Based on Internal Properties

![[raw/assets/attachments/llm/intrinsic_evaluation-min.png]]

This type of evaluation looks at the internal properties of embeddings, i.e. how well they capture meaning. Specifically, in the [Analysis and Interpretability](#analysis_interpretability) section, we will discuss in detail how we can evaluate embeddings on word similarity and word analogy tasks.

### Extrinsic Evaluation: On a Real Task

![[raw/assets/attachments/llm/extrinsic_evaluation-min.png]]

This type of evaluation tells which embeddings are better for the task you really care about (e.g., text classification, coreference resolution, etc.).  
  
In this setting, you have to train the model/algorithm for the real task several times: one model for each of the embeddings you want to evaluate. Then, look at the quality of these models to decide which embeddings are better.

### How to Choose?

![[raw/assets/attachments/llm/evaluation_tradeoff-min.png]]

One thing you have to get used to is that there is no perfect solution and no right answer for all situations: it always depends on many things.

Regarding evaluation, you usually care about quality of the task you want to solve. Therefore, you are likely to be more interested in extrinsic evaluation. However, real-task models usually require a lot of time and resources to train, and training several of them may be too expensive.

In the end, this is your call to make:)

  
  

## Analysis and Interpretability

Lena: For word embeddings, most of the content of this part is usually considered as evaluation (intrinsic evaluation). However, since looking at what a model learned (beyond task-specific metrics) is the kind of thing people usually do for analysis, I believe it can be presented here, in the analysis section.

## Take a Walk Through Space... Semantic Space!

Semantic spaces aim to create representations of natural language that capture meaning. We can say that (good) word embeddings form semantic space and will refer to a set of word vectors in a multi-dimensional space as "semantic space".

Below is shown semantic space formed by GloVe vectors trained on twitter data (taken from [gensim](https://github.com/RaRe-Technologies/gensim-data)). Vectors were projected to two-dimensional space using t-SNE; these are only the top-3k most frequent words.

How to: Walk through semantic space and try to find:

- language clusters: Spanish, Arabic, Russian, English. Can you find more languages?
- clusters for: food, family, names, geographical locations. What else can you find?

<iframe frameborder="0" width="510" height="510" src="https://lena-voita.github.io/resources/lectures/word_emb/analysis/glove100_twitter_top3k.html"></iframe>

  
  

## Nearest Neighbors

![[raw/assets/attachments/llm/frog-min.png]]  
The example is from the [GloVe project page](https://nlp.stanford.edu/projects/glove/).

During your walk through semantic space, you probably noticed that the points (vectors) which are nearby usually have close meaning. Sometimes, even rare words are understood very well. Look at the example: the model understood that words such as leptodactylidae or litoria are close to frog.

  

![[raw/assets/attachments/llm/rare_words-min.png]]  
Several pairs from the [Rare Words similarity benchmark](https://nlp.stanford.edu/~lmthang/data/papers/conll13_morpho.pdf).

### Word Similarity Benchmarks

"Looking" at nearest neighbors (by cosine similarity or Euclidean distance) is one of the methods to estimate the quality of the learned embeddings. There are several word similarity benchmarks (test sets). They consist of word pairs with a similarity score according to human judgments. The quality of embeddings is estimated as the correlation between the two similarity scores (from model and from humans).

  

## Linear Structure

While similarity results are encouraging, they are not surprising: all in all, the embeddings were trained specifically to reflect word similarity. What is surprising, is that many semantic and syntactic relationships between words are (almost) linear in word vector space.

![[raw/assets/attachments/llm/king_example-min.png]]

For example, the difference between king and queen is (almost) the same as between man and woman. Or a word that is similar to queen in the same sense that kings is similar to king turns out to be queens. The man-woman $\approx$ king-queen example is probably the most popular one, but there are also many other relations and funny examples.

Below are examples for the country-capital relation and a couple of syntactic relations.

![[raw/assets/attachments/llm/examples_both-min.png]]

At ICML 2019, it was shown that there's actually a theoretical explanation for analogies in Word2Vec. [More details are here.](#papers_theory)  
  
Lena: This paper, [Analogies Explained: Towards Understanding Word Embeddings](https://arxiv.org/pdf/1901.09813.pdf) by Carl Allen and Timothy Hospedales from the University of Edinburgh, received Best Paper Honourable Mention award at ICML 2019 - well deserved!

### Word Analogy Benchmarks

These near-linear relationships inspired a new type of evaluation: word analogy evaluation.

![[raw/assets/attachments/llm/analogy_task_v2-min.png]]

![[raw/assets/attachments/llm/analogy_testset-min.png]]  
Examples of relations and word pairs from [the Google analogy test set](https://arxiv.org/pdf/1301.3781.pdf).

Given two word pairs for the same relation, for example (man, woman) and (king, queen), the task is to check if we can identify one of the words based on the rest of them. Specifically, we have to check if the closest vector to king - man + woman corresponds to the word queen.

Now there are several analogy benchmarks; these include the standard benchmarks ([MSR](https://www.aclweb.org/anthology/N13-1090.pdf) + [Google analogy](https://arxiv.org/pdf/1301.3781.pdf) test sets) and [BATS (the Bigger Analogy Test Set)](https://www.aclweb.org/anthology/N16-2002.pdf).

  

## Similarities across Languages

We just saw that some relationships between words are (almost) linear in the embedding space. But what happens across languages? Turns out, relationships between semantic spaces are also (somewhat) linear: you can linearly map one semantic space to another so that corresponding words in the two languages match in the new, joint semantic space.

![[raw/assets/attachments/llm/cross_lingual_matching-min.png]]

The figure above illustrates [the approach proposed by Tomas Mikolov et al. in 2013](https://arxiv.org/pdf/1309.4168.pdf) not long after the original Word2Vec. Formally, we are given a set of word pairs and their vector representations $\left{\right. x_{i} , z_{i} \left.\right}_{i = 1}^{n}$, where $x_{i}$ and $z_{i}$ are vectors for i-th word in the source language and its translation in the target. We want to find a transformation matrix W such that $W z_{i}$ approximates $x_{i}$: "matches" words from the dictionary. We pick $W$ such that 
$$
W = arg ⁡ \underset{W}{min} \sum_{i = 1}^{n} \parallel W z_{i} - x_{i} \parallel^{2} ,
$$
 and learn this matrix by gradient descent.

In the original paper, the initial vocabulary consists of the 5k most frequent words with their translations, and the rest is learned.

Later it turned out, that we don't need a dictionary at all - we can build a mapping between semantic spaces even if we know nothing about languages! [More details are here.](#papers_cross_lingual)

Is the "true" mapping between languages indeed linear, or more complicated? We can look at geometry of the learned semantic spaces and check. [More details are here.](#papers_analyzing_geometry)

The idea to linearly map different embedding sets to (nearly) match them can also be used for a very different task! Learn more in the [Research Thinking](#research_thinking) section.

  
  

## Research Thinking

---

  
  

## Count-Based Methods

Improve Simple Co-Occurrence Counts

---

The simplest co-occurrence counts treat context words equally, although these words are at different relative positions from the central word. For example, from one sentence the central word cat will get a co-occurrence count of 1 for each of the words cute, grey, playing, in (look at the example to the right).

![[raw/assets/attachments/llm/counts_simple-min.png]]

---

? Are context words at different distances equally important? If not, how can we modify co-occurrence counts?  
Possible answers ![[raw/assets/attachments/llm/counts_modify_position-min.png]] Intuitively, words that are closer to the central are more important; for example, immediate neighbors are more informative than words at distance 3.  
  
We can use this to modify the model: when evaluating counts, let's give closer words more weight. This idea was used in the [HAL model (1996)](https://link.springer.com/content/pdf/10.3758/BF03204766.pdf), which once was very famous. They modified counts as shown in the example.  
? In language, word order is important; specifically, left and right contexts have different meanings. How can we distinguish between the left and right contexts? One of the existing approaches ![[raw/assets/attachments/llm/counts_left_right-min.png]] Here the weighting idea we saw above would not work: we can not say which contexts, left or right, are more important.  
  
What we have to do is to evaluate co-occurrences to the left and to the right separately. For each context word, we will have two different counts: one when it is a left context and another when it is the right context. This means that our co-occurrence matrix will have |V| rows and 2|V| columns. This idea was also used in the [HAL model (1996)](https://link.springer.com/content/pdf/10.3758/BF03204766.pdf).  
  
Look at the example; note that for cute, we have left co-occurrence count, for cat - right.

  
  

## Word2Vec

Are all context words equally important for training?

---

During Word2Vec training, we make an update for each of the context words. For example, for the central word cat we make an update for each of the words cute, grey, playing, in.

![[raw/assets/attachments/llm/cat_5windows-min.png]]

---

? Are all context words equally important?  
Which word types give more/less information than others? Think about some characteristics of words that can influence their importance. Do not forget the previous exercise! Possible answers
- word frequency  
	We can expect that frequent words usually give less information than rare ones. For example, the fact that cat appears in context of in does not tell us much about the meaning of cat: the word in serves as a context for many other words. In contrast, cute, grey and playing already give us some idea about cat.
- distance from the central word  
	As we discussed in [the previous exercise on count-based methods](#research_improve_count_based), words that are closer to the central may be more important.
  
? How can we use this to modify training? Tricks from the original Word2Vec

### 1\. Word Frequency

![[raw/assets/attachments/llm/freq_subsampling_idea-min.png]]

To account for different informativeness of rare and frequent words, Word2Vec uses a simple subsampling approach: each word $w_{i}$ in the training set is ignored with probability computed by the formula 
$$
P \left(\right. w_{i} \left.\right) = 1 - \sqrt{\frac{t h r}{f \left(\right. w_{i} \left.\right)}}
$$
 where $f \left(\right. w_{i} \left.\right)$ is the word frequency and $t h r$ is the chosen threshold (in the original paper, $t h r = 10^{- 5}$). This formula preserves the ranking of the frequencies, but aggressively subsamples words whose frequency is greater than $t h r$.  
  
Interestingly, this heuristic works well in practice: it accelerates learning and even significantly improves the accuracy of the learned vectors of the rare words.  
  

### 2\. Distance from the central word

![[raw/assets/attachments/llm/w2v_position-min.png]] As in [the previous exercise on count-based methods](#research_improve_count_based), we can assign higher weights to the words which are closer to the central.  
  
At the first glance, you won't see any weights in the original Word2Vec implementation. However, at each step it samples the size of the context window from 1 to L. Therefore, words which are closer to central are used more frequently than the distant ones. In the original work this was (probably) done for efficiency (fewer updates for each step), but this also has the effect similar to assigning weights.

Use Information About Subwords ("invent" FastText)

---

Usually, we have a look-up table where each word is assigned a distinct vector. By construction, these vectors do not have any idea about subwords they consist of: all information they have is what they learned from contexts.

![[raw/assets/attachments/llm/distinct_vectors-min.png]]

---

? Imagine that word embeddings have some understanding of subwords they consist of. Why can this be useful?  
Possible answers
- better understanding of morphology  
	By assigning a distinct vector to each word, we ignore morphology. Giving information about subwords can let the model know that different tokens can be forms of the same word.
- representations for unknown words  
	Usually, we can represent only those words, which are present in the vocabulary. Giving information about subwords can help to represent out-of-vocabulary words relying of their spelling.
- handling misspellings  
	Even if one character in a word is wrong, this is another token, and, therefore, a completely different embedding (or even unknown word). With information about subwords, misspelled word would still be similar to the original one.
  
? How can we incorporate information about subwords into embeddings? Let's assume that the training pipeline is fixed, e.g., Skip-Gram with Negative sampling. One of the existing approaches (FastText)

![[raw/assets/attachments/llm/fasttext-min.png]]

One of the possible approaches is to compose a word vector from vectors for its subwords. For example, popular [FastText embeddings](https://arxiv.org/pdf/1607.04606.pdf) operate as shown in the illustration. For each word, they add special start and end characters for each word. Then, in addition to the vector for this word, they also use vectors for character n-grams (which are also in the vocabulary). Representation of a word is a sum of vectors for the word and its subwords, as shown in the picture.  
  
Note that this changes only the way we form word vector; the whole training pipeline is the same as in the standard Word2Vec.

  
  

## Semantic Change

Detect Words that Changed Their Usage

---

Imagine you have text corpora from different sources: time periods, populations, geographic regions, etc. In digital humanities and computational social science, people often want to find words that used differently in these corpora.

![[raw/assets/attachments/llm/semantic_change-min.png]]

---

? Given two text corpora, how would you detect which words are used differently/have different meaning? Do not be shy to think about very simple ways! Some of the existing attempts

### ACL 2020: train embeddings, look at the neighbors

![[raw/assets/attachments/llm/intersect_neighbors-min.png]] A very simple approach is to train embeddings (e.g., Word2Vec) and look at the closest neighbors. If a word's closest neighbors are different for the two corpora, the word changed its meaning: remember that word embeddings reflect contexts they saw!  
  
This approach was proposed in [this ACL 2020 paper](https://www.aclweb.org/anthology/2020.acl-main.51.pdf). Formally, for each word the authors take k nearest neighbors in the two embeddings sets and count how many neighbors are the same. Large intersection means that the meaning is not different, small intersection - meaning is different.  
  

Lena: Note that while the approach is recent, it is extremely simple and works better than previous more complicated ideas. Never be afraid to try simple things - you'll be surprised how often they work!

### Previous popular approach: align two embedding sets

![[raw/assets/attachments/llm/emb_align-min.png]]

[The previous popular approach](https://www.aclweb.org/anthology/P16-1141.pdf) was to align two embeddings sets and to find word whose embeddings do not match well. Formally, let $W_{1} , W_{2} \in \mathbb{R}^{d \times \left|\right. V \left|\right.}$ be embedding sets trained on different corpora. To align the learned embeddings, the authors find the rotation $R = arg ⁡ \underset{Q^{T} Q = I}{min} \parallel W_{2} Q - W_{1} \parallel_{F}$ - this is called Orthogonal Procrustes. Using this rotation, we can align embedding sets and find words which do not match well: these are the words that change meaning with the corpora.  
  

Lena: You will implement Ortogonal Proctustes in your homework to align Russian and Ukranian embeddings. Find the notebook in [the course repo](https://github.com/yandexdataschool/nlp_course).

  
  

## Have Fun!

---

  
  

shampoo - hair + body =?

next

Choose your answer