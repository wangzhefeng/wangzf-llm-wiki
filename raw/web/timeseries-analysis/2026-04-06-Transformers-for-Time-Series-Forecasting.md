---
author:
- null
- '[[Serana AI]]'
created: 2026-04-06
created_at: 2026-04-06
description: Transformers for Time Series Forecasting Time series forecasting has
  progressed from classical models like ARIMA, which perform well on short-term, linear
  patterns, to machine learning methods that …
source_type: web
status: inbox
tags:
- null
- clippings
title: Transformers for Time Series Forecasting
source_url: https://medium.com/@serana.ai/transformers-for-time-series-forecasting-e5e0327e78be
published_at: 2025-06-02
related_concepts: []
topics:
  - timeseries-analysis
  - 时间序列分析
---

[Sitemap](https://medium.com/sitemap/sitemap.xml)

Get unlimited access to the best of Medium for less than $1/week.[Become a member](https://medium.com/plans?source=upgrade_membership---post_top_nav_upsell-----------------------------------------)

[

Become a member

](https://medium.com/plans?source=upgrade_membership---post_top_nav_upsell-----------------------------------------)

<!-- missing attachment -->

Time series forecasting has progressed from [classical models](https://medium.com/@serana.ai/time-series-modelling-arima-and-ets-cafc904b9183) like ARIMA, which perform well on short-term, linear patterns, to machine learning methods that offer greater flexibility but often require extensive manual feature engineering. [Deep learning based models](https://medium.com/@serana.ai/deep-learning-for-time-series-forecasting-a71104aa5e19), such as recurrent neural networks, can learn temporal patterns directly from raw data, but these architectures frequently struggle with long-term dependencies and suffer from sequential processing bottlenecks. Transformers marked a major turning point by replacing recurrence with attention mechanisms, enabling models to efficiently capture both short and long-range dependencies. This shift has led to more scalable and robust forecasting across a wide range of time series applications, addressing several limitations of classical and earlier deep learning approaches. In this post, we explore recent developments in Time Series Forecasting (TSF) through the lens of Transformer-based models.

## Transformers

Transformers are redefining time series forecasting. Originally designed for natural language processing, these models, built around attention mechanisms, have become powerful tools for capturing complex temporal patterns. Unlike older models that process data sequentially, Transformers can examine the entire sequence at once and selectively focus on the most relevant parts. This ability makes them faster, more flexible, and particularly effective at modeling long-term dependencies.

At the core of this architecture is the self-attention mechanism, which enables the model to dynamically assign importance to different time steps, as shown in Fig. 1. This approach has allowed Transformers to outperform many traditional and deep learning methods, especially in tasks involving long-range forecasting or noisy data.

![[Image 108.webp|Image5]]

Figure 1. Transformer attention in time series: The model selectively highlights certain past time steps (shown in blue) that are most important for making the current prediction (in red). The attention weights control how much each past point contributes to the forecast.

Among the growing list of Transformer models for time series forecasting, this post will dive into six key architectures that represent distinct directions in the field: Informer, Autoformer, FEDformer, iTransformer, Temporal Fusion Transformer (TFT), and PatchTST.

### Informer

Informer \[1\] is a time series forecasting model based on Transformers, the same architecture used in powerful language models. But while standard Transformers are useful for many tasks, it’s an ordeal for them with very long time series because they slow down dramatically as the input gets longer. This is due to what’s called quadratic complexity, which simply means the work the model has to do increases with the square of the input length.

One of Informer’s key features is the ProbSparse attention mechanism, which speeds up the model by reducing the computation needed. Instead of comparing every part of the input to every other part (which takes time that grows quadratically as the input gets longer), it focuses only on the most important parts. This brings the time down to log-linear growth, making it much faster at handling long sequences.

Another key feature is self-attention distillation, where the sequence length is halved at each layer. This helps the model retain only the most salient temporal information while easing the memory load. Informer also outputs the entire forecast in a single forward pass rather than predicting step-by-step, making it particularly well-suited for real-time forecasting.

Owing to these innovations, Informer works well in tasks like predicting electricity usage hours, forecasting traffic trends throughout the day, or modeling financial signals across hundreds of time steps. It works especially well when there are repeating patterns and large volumes of historical data. However, it may still face challenges when the data is extremely noisy or behaves unpredictably over long periods of the historical data.

### Autoformer

While Informer made major strides in handling long time series efficiently, it still treated time as just a sequence of numbers, every time step weighed the same, regardless of whether it was a peak, a seasonal dip, or a long-term trend. But real-world time series aren’t flat, they have structure. For example, sales rise during holidays, electricity demand peaks in the evenings, and Mondays don’t behave like Sundays. That’s where Autoformer steps in \[2\].

The fundamental idea is series decomposition. Instead of processing the raw signal directly, Autoformer separates it into trend and seasonal components. This helps the model learn each part more effectively, rather than trying to capture everything at once. A second aspect is Auto-Correlation attention, which compares similar sub-sequences instead of every time step with each other. For example, it learns to compare Mondays with other Mondays. This not only reduces computation but also matches the periodic nature of many real-world time series. The architecture of Autoformers has been shown in Fig. 2. Unlike models that decompose data as a pre-processing step, Autoformers perform decomposition inside the model during both training and inference. This allows it to adaptively learn patterns as part of the forecasting task.

Autoformer stands strong in long-horizon forecasting, where trends and seasonality unfold over extended periods. It is a deterministic model, meaning it outputs a single forecast rather than a distribution. While this simplifies the model, it limits its ability to estimate uncertainty.

![[Image 109.webp|Image1]]

Figure 2. Architecture of Autoformer. This figure has been adapted from \[3\].

### Temporal Fusion Transformer

In the previous sections, we saw that Informer focused on scalability and Autoformer introduced modeling with trend and seasonality decomposition. However, they both still assume relatively clean, consistent data. But real-world forecasting problems are rarely that tidy. Inputs are often a mix of static features (like product type), known future events (like holidays or price changes), and observed variables (like past sales or weather), all of which may matter differently at different times. Hence, Temporal Fusion Transformer (TFT) was introduced \[4\].

TFT \[4\] is a transformer-based model designed for multi-horizon time-series forecasting, with a focus on interpretability and handling complex, real-world data. Traditional models often fall short when dealing with mixed inputs like static features, known future events, and dynamic variables. TFT addresses these challenges using a combination of gating mechanisms, attention layers, and variable selection networks to model both short and long-term dependencies.

A significant innovation in TFT is its use of variable selection networks, which dynamically identify the most relevant features at each time step. This improves model focus, accuracy, and transparency by showing which inputs contribute most to the forecast. Gated residual networks (GRNs) further enhance control over information flow. A GRN is a smart filter that helps the model decide which information to pass forward and which to ignore. It helps the network stay focused during training.

TFT combines recurrent layers (for short-term patterns) and self-attention (for long-term dependencies), allowing it to adapt to a range of temporal dynamics. It also supports quantile forecasting, providing prediction intervals rather than single-point estimates, which is useful for applications where uncertainty matters.

These design choices make TFT well-suited for forecasting tasks with rich and complex data, such as demand prediction, energy usage, or financial signals. However, TFT has many components that need to work together smoothly. Choosing the right settings (like learning rate, layer size, and input length) is key to getting good performance, and often requires trial and error.

### FEDformer

While the previously developed Transformer-based models focused on efficiency, brought structure-awareness through trend and seasonality, and tackled real-world complexity with interpretability, there remained a deeper challenge: how do we model the hidden rhythms of time series more directly? FEDformer introduces a novel take on this problem, one that treats time series not just as sequences of numbers, but as compositions with rhythm \[5\].Think of a time series like a piece of music. Just as a song contains repeating choruses, subtle background harmonies, and steady rhythms, a time series contains trends, seasonality, and fluctuations. FEDformer uses this insight to “listen” to the time series rather than analyzing each time step. The crux of this architecture is that FEDformer converts parts of the time series into the frequency domain using Fourier transforms, much like breaking music into bass and treble, to detect the dominant patterns. By focusing on the strongest frequencies and ignoring the rest, it filters out noise and highlights the signals that matter most.

Before this transformation happens, FEDformer first decomposes the time series input into a trend and a seasonal component. The trend captures long-term growth or decline, while the seasonal component captures recurring patterns. Only the seasonal part is processed in the frequency space, where attention mechanisms identify the most meaningful signals. After the model has worked its way through these components, it reconstructs the forecast by combining the refined trend and seasonal outputs.

Still, FEDformer has limitations. It assumes the time series has a frequency structure (rhythm) to exploit, so it may not be as effective on highly irregular data. It also focuses on point forecasts, which may not be ideal for applications that need uncertainty estimation. Also, while the model is powerful, its use of frequency-domain operations may be harder to interpret for practitioners unfamiliar with spectral analysis.

### ITransformer

One key challenge still remains, i.e., how do we model the relationships between variables in multivariate time series? As time series forecasting moves into more complex, multivariate domains, traditional approaches, even earlier Transformer-based ones, often struggle to model the intricate relationships between variables. Inverted Transformer (iTransformer) offers a new perspective: instead of focusing on how a series changes over time, it shifts the focus to how the variables within that series interact \[6\].

Think of a multivariate time series like a conversation at a dinner table. Traditional models listen to just one person at a time, tracing what they say minute by minute. But iTransformer listens to how people influence each other, how one speaker responds to another, or how a question from one side of the table affects answers on the other. In the same way, iTransformer treats each variable (like temperature, pressure, or demand) as a separate voice and learns the relationships between them, not just how they evolve over time.

To do this, iTransformer flips the usual Transformer setup. Instead of combining variables at each time step and applying attention across time, it treats each variable’s full time history as a separate input token and applies attention across variables. This inversion allows the model to directly capture interactions between features. After modeling these relationships, it processes each variable’s internal time dynamics independently, learning patterns like trends and fluctuations. The result is a model that excels at multivariate forecasting, especially when the variables influence one another, like in energy systems, financial markets, or sensor networks.

![[Image 110.webp|Image3]]

Figure 3. Comparison of transformer and inverse transformer \[6\].

However, iTransformer has its trade-offs. Its focus on variable interactions means it may be less suited for simple univariate tasks. And while it’s effective for point forecasting, it doesn’t natively model uncertainty. Still, by rethinking how one structures time series input and where we apply attention, iTransformer introduces a flexible and scalable way to forecast not just time, but interactions across time.

### PatchTST

PatchTST is a type of forecasting model that borrows smart ideas from Vision Transformers (Fig. 4) and adapts them for time series \[7\]. Traditional Transformers slow down on long time series because they compare every time step with every other, making computation more expensive as sequences keep growing. They also treat time as just another input, which makes it harder for them to naturally recognize trends, cycles, and the order of events, unless enhanced with specialized tricks. PatchTST fixes this by breaking the time series into small chunks, or “patches,” instead of feeding it one step at a time. This helps the model spot both short-term trends and long-term patterns, while also making it run faster.

![[Image 21.jpg|Image2]]

Figure 4. How Vision Transformers work: An image is divided into patches, each turned into a vector with positional information. These are processed by a Transformer encoder using self-attention to learn global relationships. A classification token summarizes the result for the final prediction. The graphics have been adapted from Wikipedia.

Unlike earlier models like Vanilla Transformers or Informer, which use both an encoder and a decoder, PatchTST keeps things simpler by using only an encoder. In those older models, the decoder is responsible for generating future values one step at a time, which can be slow. PatchTST skips the decoder entirely and predicts all future time points at once, in a single forward pass through the model.

The key idea behind PatchTST is to break up the input time series, which could be many days, weeks, or even months of data, into small chunks called “patches.” Each patch contains a short, consecutive window of past values (for example, 16 or 32 time steps). These patches are then flattened and converted into vectors called tokens. Just like how Vision Transformers treat patches of an image as tokens, PatchTST treats these time patches as the basic units it processes. In the case of multivariate time series (where multiple variables like temperature, pressure, and humidity are recorded), PatchTST applies a channel-independent approach. This means it models each variable separately, creating patches and tokens for each one independently. This allows the model to learn clean, variable-specific patterns, avoid interference between unrelated signals, and scale efficiently across datasets with multiple channels.

Despite the advantages, PatchTST does come with its drawbacks, too. It provides only point forecasts and may miss fine-grained patterns if patches are too large or overlapping, making it less suited for uncertainty estimation or capturing short-term anomalies.

### Comparison

Among the first breakthroughs was Informer, which outperformed vanilla Transformers by 15–20% on datasets like ETT and Weather, while also speeding up training and inference. Building on this, Autoformer incorporated a series decomposition block and autocorrelation attention, allowing the model to separately learn trend and seasonal components during training. This architecture led to another 10–12% improvement over Informer, particularly on structured, periodic data.

While not always the most accurate in benchmarks, TFT is known for its practical strengths. It supports exogenous inputs, provides uncertainty estimates, and offers interpretability through attention visualization, traits that make it valuable in real-world deployment.

FEDformer moves into the frequency domain, using Fourier transforms to isolate dominant patterns in the data, and it improves accuracy by over 22% on univariate tasks compared to Autoformer. iTransformer flips the usual time-step-first approach and treats each variable as a token, making it highly effective for multivariate forecasting where variable interactions are key. On benchmarks like Traffic and ETTm1, it outperforms previous models by 5–8% in RMSE.

PatchTST then shifted the paradigm by adapting ideas from Vision Transformers. It has become a popular choice when it comes to long-horizon forecasting tasks, reducing errors by up to 50% compared to deep learning models like DeepAR and TCN. In contrast, DeepAR and TCN still have roles to play in smaller or probabilistic forecasting tasks, but they generally suffer when dealing with long-sequence and high-dimensional settings. Across most public datasets, Transformer-based models are now used extensively, offering the best balance of performance, flexibility, and scalability.

### Conclusion

Transformer-based models have fundamentally changed how we approach time series forecasting. By replacing sequential processing with attention mechanisms and incorporating architectural innovations like patching, decomposition, frequency analysis, and variable-wise attention, these models have set new benchmarks in both accuracy and scalability. Whether it’s handling multivariate complexity with iTransformer, balancing performance and interpretability with TFT, or long-horizon forecasting with PatchTST, Transformers now offer a powerful toolkit tailored to the diverse demands of real-world forecasting tasks. As time series data grows in volume and complexity, Transformers are no longer just an alternative anymore.

### References

\[1\] Zhou et al. Informer: Beyond Efficient Transformer for Long Sequence Time-Series Forecasting (2021).  
\[2\] Wu et al. Autoformer: Decomposition Transformers with Auto-Correlation for Long-Term Series Forecasting, (2022).  
\[3\] Liu et al. DMEformer: A newly designed dynamic model ensemble transformer for crude oil futures prediction, (2023).  
\[4\] Lim et al. Temporal Fusion Transformers for Interpretable Multi-horizon Time Series Forecasting, (2020).  
\[5\] Zhou et al. FEDformer: Frequency Enhanced Decomposed Transformer for Long-term Series Forecasting, (2022).  
\[6\] Liu et al. Itransformer: Inverted Transformers are Effective for Time Series Forecasting, (2024).  
\[7\] Nie et al. A Time Series is Worth 64 Words: Long-Term Forecasting With Transformers, (2023).

*Contributed by Arnab Majumdar, Research Scientist at Serana AI.*

Serana AI is a pre-seed stage startup focused on building high-performance, scalable solutions for spatio-temporal forecasting. Our models are designed to handle real-world complexity and deliver actionable insights for decision-making. To learn more about our work or explore collaboration opportunities, visit [serana.ai](https://serana.ai/).

[![[1*72e0BK8ffP4w_TxTEnYdTA.png|Serana AI]]](https://medium.com/@serana.ai?source=post_page---post_author_info--e5e0327e78be---------------------------------------)

[![[1*72e0BK8ffP4w_TxTEnYdTA 1.png|Serana AI]]](https://medium.com/@serana.ai?source=post_page---post_author_info--e5e0327e78be---------------------------------------)

[1 following](https://medium.com/@serana.ai/following?source=post_page---post_author_info--e5e0327e78be---------------------------------------)

## Responses (1)

Wangzhefengr

What are your thoughts?  

```sh
Pushing transformers into time series feels like breaking old molds. Temporal attention shifts how we treat sequences—less brute force, more nuance in the signal.
```
