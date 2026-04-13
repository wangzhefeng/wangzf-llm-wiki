---
source_type: web
title: "时间序列预测的层次分类辅助网络 --- Hierarchical Classification Auxiliary Network for Time Series Forecasting"
author: 
created_at: 2026-04-06
status: inbox
published: 
created: 2026-04-06
description: 
tags:
  - 
  - "clippings"
source_url: "https://arxiv.org/html/2405.18975v2?_immersive_translate_auto_translate=1"
published_at: null
related_concepts: []
topics:
  - timeseries-analysis
  - 时间序列分析
---

## 时间序列预测的层次分类辅助网络

Yanru Sun <sup>1</sup>, Zongxia Xie <sup>1</sup>, Dongyue Chen <sup>1</sup>, Emadeldeen Eldele <sup>2,</sup><sup>3</sup>, Qinghua Hu <sup>1</sup> Corresponding author.

###### 摘要

Deep learning has significantly advanced time series forecasting through its powerful capacity to capture sequence relationships. However, training these models with the Mean Square Error (MSE) loss often results in over-smooth predictions, making it challenging to handle the complexity and learn high-entropy features from time series data with high variability and unpredictability. In this work, we introduce a novel approach by tokenizing time series values to train forecasting models via cross-entropy loss, while considering the continuous nature of time series data. Specifically, we propose a Hierarchical Classification Auxiliary Network, HCAN, a general model-agnostic component that can be integrated with any forecasting model. HCAN is based on a Hierarchy-Aware Attention module that integrates multi-granularity high-entropy features at different hierarchy levels. At each level, we assign a class label for timesteps to train an Uncertainty-Aware Classifier. This classifier mitigates the over-confidence in softmax loss via evidence theory. We also implement a Hierarchical Consistency Loss to maintain prediction consistency across hierarchy levels. Extensive experiments integrating HCAN with state-of-the-art forecasting models demonstrate substantial improvements over baselines on several real-world datasets.

Code — https://github.com/syrGitHub/HCAN

## 引言

Time series forecasting has received significant attention due to its wide-ranging social impact. Among existing approaches for time series forecasting, deep learning methods have emerged as significant contributors to this field [^46] [^47] [^44] [^20]. These methods showed a powerful capacity to capture sequence continuity features [^35] [^34] and enhance forecasting performance in practical applications such as finance [^10], weather forecasting [^13], resource planning [^2], and other domains [^29] [^39].

Nevertheless, current time series forecasting methods relying on the Mean Square Error (MSE) loss for feature extraction can suffer inaccurate predictions. The main downside of the MSE loss is compressing the feature representation into a narrow space, limiting its ability to learn complexity and high-entropy feature representations, especially for those features that exhibit significant variability and unpredictability [^45] [^23]. Therefore, current methods often produce over-smooth predictions, leading to inaccuracies such as inflating wind speed estimates on sunny days when the actual wind speed is low, and underestimating wind speed on windy days when the actual wind speed is high. This weakness diminishes the utility of forecasting results for downstream applications, as shown in Figure 1a.

Recently, several studies have demonstrated the superiority of cross-entropy loss in capturing high-entropy feature representation from a mutual information perspective [^23] [^45]. Therefore, it has been successfully applied in various domains, such as depth estimation [^1] [^6], age estimation [^26] [^28], and crowd counting [^40] [^8].

![[fig-1-202405181011.png|Refer to caption]]

Figure 1: Comparison between Conventional and Discretized Settings for time series forecasting. (a) Conventional setting keeps features close together, producing over-smooth predictions; (b) Discretized setting spreads the features, resulting in a higher entropy feature space, but can misclassify inter-class boundary timesteps.

In this work, we reformulate time series forecasting as a classification problem. Specifically, we tokenize time series values into different categories based on their magnitude and leverage the cross-entropy loss to train a classifier on these tokenized values. For example, in Figure 1b, we employ quantization to convert the real values into four discrete intervals, where each interval is considered a separate class. In this way, we can generate predictions within the corresponding interval based on the output of the classifier.

However, the continuous nature of time series data makes it challenging to classify values near the inter-class boundaries accurately. This difficulty may result in sub-optimal relative improvements, as illustrated by the blue circle in Figure 1b, a phenomenon commonly referred to as the boundary effects [^16].

Therefore, we propose Hierarchical Classification Auxiliary Networks (HCAN), a novel model-agnostic component that can be integrated with any forecasting model. The architecture of HCAN is illustrated in Figure 2. In specific, we develop a Hierarchy-Aware Attention (HAA) module to incorporate multi-granular high-entropy features into the main features generated by the encoder network. For each hierarchy level, we propose an Uncertainty-Aware Classifier (UAC), combined with the evidence theory to mitigate the overconfident predictions and enhance the reliability of the features. Last, we propose a Hierarchical Consistency Loss (HCL) to ensure consistency of predicted values between hierarchies. In summary, our contributions are as follows:

- We reformulate forecasting as a hierarchical classification problem to introduce high-entropy feature representations, which helps to reduce over-smooth predictions.
- We propose HCAN, a hierarchy-aware attention module supported by uncertainty-aware classifiers and a consistency loss to alleviate issues caused by the boundary effects during the classification of timesteps.
- Extensive experiments conducted on real-world datasets show the effectiveness of integrating HCAN with various state-of-the-art methods.

## Related Work

### Time Series Forecasting

With the increased data availability and computational power, deep learning-based models have become an efficient solution to time series forecasting task [^24]. In overall, based on the underlying network architecture, they can be categorized into models based on Recurrent neural networks (RNNs), Convolutional neural networks (CNNs), Transformer, and multi-layer perceptron (MLP). RNNs are traditionally utilized to capture temporal dependencies, yet they suffer from gradient vanishing and exploding problems. In addition, besides the sequential data processing, RNNs have short-term memory and may not be efficient in learning long-term dependencies. To overcome the limitations of RNNs, Transformer-based models have excelled recently [^46] [^47] [^42] [^18]. Unlike RNNs, Transformers can process entire sequences simultaneously, benefiting from the parallel computations. In addition, Transformers handle long-range dependencies more effectively than RNNs [^21].

On the other hand, recent studies have leveraged the robust abilities of CNNs to capture short-term patterns while attempting to enhance their capabilities for recognizing long-range dependencies [^15] [^5]. Lastly, the recent development of MLP-based models has resulted in good performance with simple architectures [^44] [^41].

Despite these advancements, these methods still struggle with capturing high-entropy feature representations due to their reliance on the MSE loss, which often leads to over-smooth predictions [^45]. Differently, our proposed work aims to overcome this limitation and construct a complex and high-entropy feature space, thereby enhancing feature diversity and improving prediction accuracy.

![[fig-model-20240814-1339.png|Refer to caption]]

Figure 2: The structure of our proposed HCAN. From right to left, time series are first divided into fine-grained classes and coarse-grained classes to form category labels for Hierarchical Classification. According to these category labels, the Uncertainty-Aware Classifier (UAC) at each level obtains reliable multi-granularity high-entropy features using evidence theory. The Hierarchical Consistency Loss (HCL) ensures the consistency of values between hierarchies. Finally, the Hierarchy-Aware Attention (HAA) module integrated the multi-granularity features into the forecasting features obtained by the backbones.

### Classification for Continuous Targets

Our approach draws inspiration from successful applications of classification in other domains, such as computer vision and pose estimation, where discretizing continuous targets has led to significant improvements [^25] [^7]. For instance, in-depth estimation tasks, classifying depth ranges has proven more effective than precise value prediction [^1] [^6].

In the context of time series analysis, some recent works have explored limited categorization schemes. For example, DEMM [^36] and DEMMA [^32] propose frameworks that segment time series into three broad categories. Similarly, NEC+ [^14] employs binary classification to distinguish between extreme and normal events.

Our work significantly extends and refines these initial explorations by introducing a comprehensive, multi-level classification framework specifically designed for time series forecasting. This novel approach achieves a balance between the simplification benefits of discretization and the need for nuanced, continuous predictions. In addition, it addresses key limitations of previous methods, such as the loss of granularity in predictions and the occurrence of boundary effects near class thresholds.

## Methodology

### Preliminaries

Given the historical time series data $X=\{x^{i}\}_{i=1}^{N}$ with $N$ samples, where $x^{i}\in\mathbb{R}^{L\times D}$, the goal of time series forecasting is to predict horizon series $Y=\{y^{i}\}_{i=1}^{N}$, where $y^{i}\in\mathbb{R}^{T\times D}$. Here, $L$ is the look-back window, $T$ is the number of future timesteps, and $D$ refers to the number of channels in the multivariate time series.

HCAN reformulates the forecasting task as a hierarchical classification task with 3 levels: the original series, coarse, and fine-grained. The number of categories at each level is $K_{o}=1$, $K_{c}=2$, $K_{f}=4$. At each level, a discretizing mapping function converts the continuous target $y^{i}$ into a categorical target $k^{i}$ based on which interval $\mathcal{I}_{k}=(\rho_{k}^{\text{left}},\rho_{k}^{\text{right}})$ the value $y^{i}$ falls into. This interval $\mathcal{I}_{k}$ represents the range within which $y^{i}$ is categorized. The detailed mapping process can be found in the Appendix. Subsequently, the relative forecasting target $\Delta y^{i}=y^{i}-\rho_{k}^{\text{left}}$ is computed as the offset of $y^{i}$ from the lower bound $\rho_{k}^{\text{left}}$ of the interval $\mathcal{I}_{k}$, where $\Delta y^{i}\in\mathbb{R}^{T\times D}$. Therefore, the new structure of the dataset becomes $D=\{x^{i},y^{i},\Delta y^{i}_{c},k^{i}_{c},\Delta y^{i}_{f},k^{i}_{f}\}_{i=1}^%
{N}$ with $N$ samples.

### Hierarchical Classification Auxiliary Network

We propose a hierarchical structure that trains classifiers at the fine-grained and coarse-grained levels, each with a different number of classes, to obtain high-entropy features represented in multiple granularities. Specifically, the fine-grained feature is obtained from the hierarchy, which has a larger number of categories, providing the model with relatively precise quantification. Conversely, the coarse-grained feature, which corresponds to a hierarchy with fewer categories, aims to enhance classification accuracy, as shown in Figure 2.

To illustrate the workflow of our HCAN, we begin by extracting features $F\in\mathbb{R}^{D\times T}$ from the backbone model. Subsequently, we employ three distinct linear layers to generate three types of features: $\theta\in\mathbb{R}^{D\times M}$, $\phi\in\mathbb{R}^{D\times M}$, and $\eta\in\mathbb{R}^{D\times M}$, representing fine-grained, coarse-grained, and the original temporal features, respectively. Meanwhile, as depicted in the right-most part of Figure 2, we categorize the timesteps into fine-grained and coarse-grained classes based on their magnitude. Specifically, we define the boundary of each group by arranging the time series values in an ascending order and then dividing them based on the number of groups $K$ (see the Appendix). This categorization forms a hierarchical structure and establishes the category labels.

These hierarchical categories are used as labels to train the Uncertainty-Aware Classifiers (UAC) at the coarse-grained and fine-grained levels. Through backpropagation, the UAC refines the features $\theta$ and $\phi$, transforming them into high-entropy feature representations. The temporal feature $\eta$ is tailored to capture the temporal characteristics of time series forecasting. Furthermore, we implement the Hierarchical Consistency Loss (HCL) to maintain consistency between the coarse-grained and fine-grained levels and to mitigate boundary effects. Finally, we combine $\theta$, $\phi$, and $\eta$ with the initial forecasting features $F$ through the Hierarchy-Aware Attention (HAA) module. In the subsequent sections, we provide a detailed description of these components.

#### Uncertainty-Aware Classification

In our HCAN, we include a classifier at the coarse-grained and fine-grained levels to create the high entropy features. However, a key challenge is the high confidence often erroneously assigned to incorrect predictions by traditional softmax-based classifiers [^19] [^31]. This issue becomes more obvious given our objective of classifying timesteps-level values into distinct classes. To address this issue and improve the robustness of classification across various hierarchical levels, we implement an evidence-based uncertainty estimation technique, which is meant to enhance the precision of uncertainty assessments. Moreover, we consider the case of challenging samples that are usually estimated with high uncertainty by the Evidential Deep Learning (EDL) methods [^9]. To prioritize these samples, we propose a novel uncertainty-aware loss function. This loss increases the importance of these challenging samples in the learning process. Essentially, if the sample is hard to classify, it helps the model recognize its difficulty and pays more attention to it.

Our approach utilizes an evidence-based uncertainty estimation technique, leveraging the parameters of the Dirichlet distribution, which is the conjugate prior of the categorical distribution. This method allows us to compute belief masses ($b$) for different categories and the overall uncertainty mass ($u$), derived from the evidence ($e$) collected from the data.

For the $K$ -class classification problems, the softmax layer of a conventional neural network classifier is replaced with an activation function layer (i.e., Softplus) to ensure non-negative outputs, which are then treated as evidence vectors $e\in\mathbb{R}_{+}^{K}$. These vectors are obtained by the classifier network based on the fine-grained feature $\theta$ or coarse-grained feature $\phi$. Next, we use these evidence vectors to construct the parameters of the Dirichlet distribution, $i.e.$, $\alpha=e+1$, and calculate the belief mass $b_{k}$ and uncertainty $u$ as:

$$
b_{k}=\frac{e_{k}}{S}=\frac{\alpha_{k}-1}{S}\quad\text{and}\quad u=\frac{K}{S},
$$

where $S=\sum_{i=1}^{K}(e_{i}+1)=\sum_{i=1}^{K}\alpha_{i}$ represents the Dirichlet strength. In addition, the sum of uncertainty mass $u$ and belief mass $b$ equals 1, $u+\sum_{k=1}^{K}b_{k}=1$, where $u\geqslant 0$ and $b\geqslant 0$. Finally, the probability distribution $p$ is calculated as $p_{k}=\frac{\alpha_{k}}{S}$.

According to Eq. 1, the more evidence observed for the $k$ -th class, the greater the probability allocated to the $k$ -th class. Conversely, the less total evidence observed, the greater the overall uncertainty. Therefore, we use the belief mass to calculate the class uncertainty for each instance. Specifically, for the $i$ -th sample, we use $(1-b^{i})$ as class-level uncertainty, which is the uncertainty weight for categories during training. We define the uncertainty-aware (UA) coefficient as: $\omega^{i}=(1-b^{i})\bigodot o^{i}$, where $\bigodot$ means the Hadamard product.

Finally, the UAC loss is defined as:

$$
\displaystyle\begin{split}\mathcal{L}_{UAC}&=\lambda_{UA}\mathcal{L}^{i}_{UA}+%
\lambda_{KL}\mathcal{L}^{i}_{KL}\\
&=\lambda_{UA}\sum_{k=1}^{K}\omega_{k}^{i}(\psi(S^{i})-\psi(\alpha_{k}^{i}))\\
&+\lambda_{KL}KL[Dir(p^{i}|\widetilde{\alpha}^{i})||Dir(p^{i}|1)],\end{split}
$$

where $\psi(\cdot)$ is the digamma function, and $\lambda_{UA},\lambda_{KL}$ are balance factors, and $\text{Dir}(p^{i}|1)$ approximates the uniform distribution. Notably, we make adjustments to the Dirichlet parameters $\alpha^{i}$ by $\widetilde{\alpha}^{i}=o^{i}+(1-o^{i})\bigodot\alpha^{i}$ to remove the non-misleading evidence.

By formalizing forecasting as a classification task, we introduce high entropy features into the forecasting feature space. At the same time, to encourage the continuity of the extracted features, we propose a relative prediction strategy, making predictions within each classification bin [^43]. We optimize using the MSE loss against the ground truth forecasting interval:

$$
\mathcal{L}_{REG}=\sum_{k=1}^{K}\mathds{I}(c_{k}=1)(\Delta y_{k}-\Delta\hat{y}%
_{k})^{2},
$$

where $c_{k}$ and $\Delta y_{k}$ denote the classification and relative prediction labels, respectively, and $\Delta\hat{y}_{k}$ is the relative prediction value obtained by the model.

The hierarchy loss is formulated across two layers with varying granularity as:

$$
\mathcal{L}_{HIER}=\mathcal{L}_{UAC}^{f}+\alpha\mathcal{L}_{REG}^{f}+\mathcal{%
L}_{UAC}^{c}+\alpha\mathcal{L}_{REG}^{c},
$$

where $\alpha$ is the balance factor.

#### Hierarchical Consistency Loss

![[fig-HCL-20240804-1620.png|Refer to caption]]

Figure 3: The hierarchical consistency loss between fine-grained and coarse-grained hierarchies encourages consistent predictions among them, alleviating the boundary effects. The e f subscript 𝑒 𝑓 e\_{f} italic\_e start\_POSTSUBSCRIPT italic\_f end\_POSTSUBSCRIPT from the fine-grained classifier is converted to ^ c 𝑐 \\hat{e}\_{c} over^ start\_ARG italic\_e end\_ARG start\_POSTSUBSCRIPT italic\_c end\_POSTSUBSCRIPT, which aligns with the coarse-grained classifier e\_{c} italic\_e start\_POSTSUBSCRIPT italic\_c end\_POSTSUBSCRIPT. We minimize the KL divergence loss between their softmax outputs.

Due to the continuous nature of time series data, directly classifying timestep values may result in misclassified values near the inter-class boundaries, known as boundary effects. Therefore, we propose the Hierarchical Consistency Loss (HCL), which aims to keep the values near the boundary of a fine-grained class within the correct coarse-grained category.

To reinforce this alignment between the hierarchical classifiers, we propose an HCL to penalize discrepancies between them. As illustrated in Figure 3, we minimize a symmetric version of the Kullback-Leibler (KL) divergence between the class distributions of the fine-grained and coarse-grained classifiers.

For each fine-grained category, represented by evidence $e_{f}=[e_{f}^{A_{1}},...,e_{f}^{A_{|A|}},e_{f}^{B_{1}},...,e_{f}^{B_{|B|}},...]$, we first convert it to a coarse-grained category evidence $e_{c}=[e_{c}^{A},e_{c}^{B},...]$. To align $e_{f}$ and $e_{c}$, we average the $e_{f}$ values that belong to the same coarse-grained class to produce the converted coarse-grained evidence:

$$
\displaystyle\begin{split}\hat{e}_{c}&=[\hat{e}_{c}^{A},\hat{e}_{c}^{B},\dots]%
\\
&=[\frac{e_{f}^{A_{1}}+...+e_{f}^{A_{|A|}}}{|A|},\frac{e_{f}^{B_{1}}+...+e_{f}%
^{B_{|B|}}}{|B|},...].\end{split}
$$

The consistency loss for each coarse-grained class is then defined as a symmetric version of the KL divergence (equivalent to the Jensen-Shannon divergence) between $e$ and $\hat{e}$:

$$
\mathcal{L}_{HCL}=\frac{1}{2}D_{KL}(e_{c}||\hat{e}_{c})+\frac{1}{2}D_{KL}(\hat%
{e}_{c}||e_{c}).
$$

This approach ensures that our model’s predictions remain consistent across different hierarchical levels, effectively alleviating boundary effects.

| Model | Informer | +HCAN | Autoformer | +HCAN | PatchTST | +HCAN | SCINet | +HCAN | Dlinear | +HCAN | iTransformer | +HCAN | FITS | +HCAN |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Metric | MSE | MSE | MSE | MSE | MSE | MSE | MSE | MSE | MSE | MSE | MSE | MSE | MSE | MSE |
| ETTh1 | 1.077 | 0.897 | 0.530 | 0.462 | 0.421 | 0.396 | 0.591 | 0.536 | 0.453 | 0.428 | 0.457 | 0.451 | 0.439 | 0.436 |
| ETTh2 | 4.779 | 2.359 | 0.483 | 0.406 | 0.342 | 0.343 | 1.041 | 0.820 | 0.473 | 0.411 | 0.384 | 0.375 | 0.375 | 0.368 |
| ETTm1 | 0.951 | 0.717 | 0.606 | 0.540 | 0.353 | 0.350 | 0.417 | 0.390 | 0.359 | 0.344 | 0.408 | 0.403 | 0.414 | 0.405 |
| ETTm2 | 1.729 | 0.981 | 0.359 | 0.303 | 0.258 | 0.250 | 0.753 | 0.685 | 0.287 | 0.296 | 0.292 | 0.285 | 0.286 | 0.280 |
| Weather | 0.733 | 0.370 | 0.351 | 0.303 | 0.268 | 0.254 | 0.242 | 0.225 | 0.247 | 0.237 | 0.260 | 0.250 | 0.249 | 0.248 |
| Exchange | 1.726 | 0.845 | 0.525 | 0.410 | 0.516 | 0.344 | 0.844 | 0.549 | 0.369 | 0.338 | 0.364 | 0.395 | 0.360 | 0.426 |
| ILI | 2.889 | 2.738 | 5.012 | 4.166 | 1.516 | 1.428 | 3.277 | 3.265 | 2.347 | 2.276 | 2.767 | 2.741 | 3.680 | 2.095 |
| Electricity | 0.352 | 0.337 | 0.250 | 0.236 | 0.259 | 0.233 | 0.213 | 0.209 | 0.210 | 0.208 | 0.176 | 0.167 | 0.217 | 0.216 |
| Traffic | 0.853 | 0.818 | 0.651 | 0.552 | 0.490 | 0.460 | 0.612 | 0.527 | 0.625 | 0.597 | 0.422 | 0.416 | 0.642 | 0.624 |
| Solar Wind | 1.953 | 1.025 | 1.362 | 1.057 | 1.109 | 0.948 | 1.174 | 1.091 | 1.071 | 1.019 | 1.360 | 1.028 | 1.349 | 1.239 |

Table 1: Multivariate long sequence time-series forecasting results. We report the MSE of different prediction lengths. The look-up window is set to $L=336$ for PatchTST, DLinear, and SCINet, and $L=96$ for other models. The best results are highlighted in bold. Detailed results of all prediction lengths for MSE/MAE are provided in the Appendix.

#### Hierarchy-Aware Attention

To introduce the high-entropy feature into the forecasting features to alleviate the over-smooth predictions, and optimize the trade-off between forecasting features and high-entropy features at different granularities, we have developed the Hierarchy-Aware Attention (HAA) module.

Building on the feature architecture of Hierarchical Classification Auxiliary Network, we reshape $\phi\in\mathbb{R}^{H\times D}$ projections, allowing their dot-products to interact and generate the HAA map $A$ of size $\mathbb{R}^{D\times D}$. This is combined with $F$ through a residual connection to introduce high-entropy feature representations. The overall HAA process is defined as follows:

$$
\begin{split}&\hat{Y}=W_{f}(W\cdot\text{Attention}(\theta,\phi,\eta)+F)+b,\\
&\text{Attention}(\theta,\phi,\eta)=\eta\cdot\text{Softmax}(\theta\cdot\phi),%
\end{split}
$$

where $W$ and $W_{f}$ are linear layers, $F$ is the backbone feature map, and $\hat{Y}$ is the prediction output. The MSE loss is optimized according to $\hat{Y}$ and the ground truth labels $Y$ as:

$$
\mathcal{L}_{MSE}=\frac{1}{N}\sum_{i=1}^{N}(Y^{i}-\hat{Y}^{i})^{2},
$$

where $N$ represents the number of samples.

To sum up, the overall training loss is defined as:

$$
\begin{split}\mathcal{L}=\mathcal{L}_{HIER}+\beta\mathcal{L}_{HCL}+\gamma%
\mathcal{L}_{MSE},\end{split}
$$

where $\beta$ and $\gamma$ are hyper-parameter loss weights chosen through grid search.

## Experiments

In this section, we conduct extensive experiments to evaluate the performance of HCAN and further perform ablation studies to justify how each component contributes to the results. Further details about the experimental setup can be found in the Appendix.

### Experimental Settings

##### Datasets.

We ran our experiments on ten publicly available real-world multivariate time series datasets, namely: *ETT*, *Exchange-Rate*, *Weather*, *ILI*, *Electricity*, *Traffic*, and *Solar Wind*. We followed the standard protocol in the data preprocessing, where we split all datasets into training, validation, and testing in chronological order by a ratio of 6:2:2 for the ETT dataset and 7:1:2 for the other datasets [^44]. See the Appendix for more details.

##### Backbone models.

We experimented our HCAN on top of several state-of-the-art deep learning-based forecasting models. We selected these models with different architectures, where Informer [^46], Autoformer [^38], PatchTST [^21], and iTransformer [^18] are Transformer-based models, SCINet [^15] is a CNN-based model, while DLinear [^44] and FITS [^41] are MLP-based models. We evaluate their performance before and after including our HCAN in the multivariate and univariate settings. For the baselines, we re-run their codes in the same settings to ensure fairness and consistency.

##### Experiments details.

Following previous works [^21] [^44], we used ADAM [^11] as the default optimizer across all the experiments and reported the MSE and mean absolute error (MAE) as the evaluation metrics. A lower MSE/MAE value indicates a better performance. Detailed results for MSE/MAE are provided in the Appendix. We conducted the experiment for the same number of epochs as the baseline and the initial learning rate is chosen from {5e-3, 1e-3, 5e-4, 1e-4, 5e-5, 1e-5} through a grid search for different datasets. $\beta$ was chosen from {1, 0.1, 0.01} and $\gamma$ was chosen from {1, 0.1, 0.01} via grid search to obtain the best results. For HCAN parameters, we set $K_{c}=2$ and $K_{f}=4$. All the experiments were repeated five times with fixed random seeds, and we reported the average performance. HCAN was implemented by PyTorch [^22] and trained on a single NVIDIA RTX 3090 24GB GPU.

### Main Results

<table><thead><tr><th colspan="2">Model</th><th>Informer</th><th>+HCAN</th><th>Autoformer</th><th>+HCAN</th><th>PatchTST</th><th>+HCAN</th><th>SCINet</th><th>+HCAN</th><th>Dlinear</th><th>+HCAN</th><th>iTransformer</th><th>+HCAN</th><th>FITS</th><th>+HCAN</th></tr><tr><th colspan="2">Metric</th><th>MSE</th><th>MSE</th><th>MSE</th><th>MSE</th><th>MSE</th><th>MSE</th><th>MSE</th><th>MSE</th><th>MSE</th><th>MSE</th><th>MSE</th><th>MSE</th><th>MSE</th><th>MSE</th></tr></thead><tbody><tr><th rowspan="4">ETTh1</th><th>96</th><td>0.255</td><td>0.121</td><td>0.088</td><td>0.082</td><td>0.055</td><td>0.055</td><td>0.088</td><td>0.068</td><td>0.057</td><td>0.053</td><td>0.061</td><td>0.060</td><td>0.056</td><td>0.054</td></tr><tr><th>192</th><td>0.283</td><td>0.092</td><td>0.108</td><td>0.086</td><td>0.071</td><td>0.072</td><td>0.105</td><td>0.084</td><td>0.077</td><td>0.075</td><td>0.073</td><td>0.072</td><td>0.075</td><td>0.072</td></tr><tr><th>336</th><td>0.291</td><td>0.088</td><td>0.118</td><td>0.091</td><td>0.082</td><td>0.078</td><td>0.130</td><td>0.094</td><td>0.097</td><td>0.088</td><td>0.089</td><td>0.087</td><td>0.091</td><td>0.089</td></tr><tr><th>720</th><td>0.256</td><td>0.106</td><td>0.138</td><td>0.121</td><td>0.086</td><td>0.081</td><td>0.214</td><td>0.134</td><td>0.168</td><td>0.164</td><td>0.083</td><td>0.105</td><td>0.104</td><td>0.096</td></tr><tr><th rowspan="4">ETTh2</th><th>96</th><td>0.302</td><td>0.182</td><td>0.169</td><td>0.140</td><td>0.129</td><td>0.127</td><td>0.130</td><td>0.129</td><td>0.133</td><td>0.128</td><td>0.135</td><td>0.133</td><td>0.125</td><td>0.123</td></tr><tr><th>192</th><td>0.264</td><td>0.206</td><td>0.211</td><td>0.179</td><td>0.169</td><td>0.162</td><td>0.327</td><td>0.169</td><td>0.177</td><td>0.174</td><td>0.182</td><td>0.178</td><td>0.177</td><td>0.174</td></tr><tr><th>336</th><td>0.324</td><td>0.223</td><td>0.255</td><td>0.226</td><td>0.187</td><td>0.187</td><td>0.198</td><td>0.220</td><td>0.212</td><td>0.225</td><td>0.218</td><td>0.215</td><td>0.222</td><td>0.221</td></tr><tr><th>720</th><td>0.302</td><td>0.249</td><td>0.334</td><td>0.292</td><td>0.224</td><td>0.201</td><td>0.486</td><td>0.221</td><td>0.298</td><td>0.259</td><td>0.240</td><td>0.238</td><td>0.258</td><td>0.255</td></tr><tr><th rowspan="4">ETTm1</th><th>96</th><td>0.093</td><td>0.046</td><td>0.059</td><td>0.047</td><td>0.026</td><td>0.024</td><td>0.049</td><td>0.029</td><td>0.030</td><td>0.026</td><td>0.029</td><td>0.028</td><td>0.029</td><td>0.027</td></tr><tr><th>192</th><td>0.232</td><td>0.059</td><td>0.081</td><td>0.057</td><td>0.039</td><td>0.037</td><td>0.077</td><td>0.049</td><td>0.044</td><td>0.043</td><td>0.049</td><td>0.045</td><td>0.043</td><td>0.042</td></tr><tr><th>336</th><td>0.271</td><td>0.108</td><td>0.088</td><td>0.072</td><td>0.053</td><td>0.050</td><td>0.109</td><td>0.089</td><td>0.064</td><td>0.059</td><td>0.061</td><td>0.060</td><td>0.057</td><td>0.056</td></tr><tr><th>720</th><td>0.464</td><td>0.118</td><td>0.122</td><td>0.079</td><td>0.074</td><td>0.070</td><td>0.139</td><td>0.117</td><td>0.081</td><td>0.082</td><td>0.083</td><td>0.082</td><td>0.079</td><td>0.075</td></tr><tr><th rowspan="4">ETTm2</th><th>96</th><td>0.092</td><td>0.065</td><td>0.127</td><td>0.095</td><td>0.065</td><td>0.065</td><td>0.079</td><td>0.069</td><td>0.064</td><td>0.061</td><td>0.069</td><td>0.069</td><td>0.070</td><td>0.069</td></tr><tr><th>192</th><td>0.134</td><td>0.107</td><td>0.146</td><td>0.123</td><td>0.094</td><td>0.091</td><td>0.105</td><td>0.094</td><td>0.092</td><td>0.087</td><td>0.107</td><td>0.106</td><td>0.100</td><td>0.098</td></tr><tr><th>336</th><td>0.178</td><td>0.141</td><td>0.217</td><td>0.126</td><td>0.120</td><td>0.117</td><td>0.130</td><td>0.128</td><td>0.129</td><td>0.120</td><td>0.144</td><td>0.143</td><td>0.128</td><td>0.126</td></tr><tr><th>720</th><td>0.221</td><td>0.156</td><td>0.198</td><td>0.184</td><td>0.172</td><td>0.169</td><td>0.175</td><td>0.155</td><td>0.176</td><td>0.181</td><td>0.185</td><td>0.187</td><td>0.178</td><td>0.176</td></tr><tr><th rowspan="4">Solar Wind</th><th>96</th><td>1.443</td><td>1.268</td><td>2.316</td><td>1.289</td><td>1.021</td><td>0.851</td><td>1.518</td><td>1.366</td><td>1.316</td><td>1.223</td><td>1.727</td><td>1.266</td><td>1.669</td><td>1.658</td></tr><tr><th>192</th><td>1.765</td><td>1.581</td><td>2.765</td><td>1.590</td><td>1.130</td><td>1.030</td><td>1.836</td><td>1.723</td><td>1.568</td><td>1.549</td><td>2.273</td><td>1.568</td><td>2.308</td><td>2.280</td></tr><tr><th>336</th><td>1.849</td><td>1.740</td><td>2.783</td><td>1.715</td><td>1.137</td><td>1.098</td><td>1.853</td><td>1.746</td><td>1.686</td><td>1.671</td><td>2.370</td><td>1.714</td><td>2.355</td><td>2.327</td></tr><tr><th>720</th><td>1.826</td><td>1.694</td><td>2.606</td><td>1.701</td><td>1.125</td><td>1.041</td><td>1.672</td><td>1.547</td><td>1.660</td><td>1.654</td><td>2.228</td><td>1.679</td><td>2.220</td><td>2.189</td></tr></tbody></table>

Table 2: Univariate long sequence time-series forecasting results on ETT full benchmark and Solar Wind dataset. We report the MSE of different prediction lengths $T\in\{96,192,336,720\}$ for comparison. The look-up window is set to $L=336$ for PatchTST, DLinear, and SCINet, and $L=96$ for other models. The best results are highlighted in bold. Detailed results of all prediction lengths for MSE/MAE are provided in the Appendix.

<table><tbody><tr><td colspan="5">Component</td><td colspan="4">Weather</td><td colspan="4">Solar Wind</td></tr><tr><td colspan="2"><math><semantics><mrow><mi>U</mi> <mo>⁢</mo> <mi>A</mi> <mo>⁢</mo> <msub><mi>C</mi> <mrow><mi>f</mi> <mo>⁢</mo> <mi>i</mi> <mo>⁢</mo> <mi>n</mi> <mo>⁢</mo> <mi>e</mi></mrow></msub></mrow> <annotation-xml><apply><ci>𝑈</ci> <ci>𝐴</ci> <apply><csymbol>subscript</csymbol> <ci>𝐶</ci> <apply><ci>𝑓</ci> <ci>𝑖</ci> <ci>𝑛</ci> <ci>𝑒</ci></apply></apply></apply></annotation-xml> <annotation>UAC_{fine}</annotation> <annotation>italic_U italic_A italic_C start_POSTSUBSCRIPT italic_f italic_i italic_n italic_e end_POSTSUBSCRIPT</annotation></semantics></math></td><td rowspan="2">Hierarchy</td><td rowspan="2"><math><semantics><msub><mi>ℒ</mi> <mrow><mi>H</mi> <mo>⁢</mo> <mi>C</mi> <mo>⁢</mo> <mi>L</mi></mrow></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><ci>𝐻</ci> <ci>𝐶</ci> <ci>𝐿</ci></apply></apply></annotation-xml> <annotation>\mathcal{L}_{HCL}</annotation> <annotation>caligraphic_L start_POSTSUBSCRIPT italic_H italic_C italic_L end_POSTSUBSCRIPT</annotation></semantics></math></td><td rowspan="2">HAA</td><td rowspan="2">96</td><td rowspan="2">192</td><td rowspan="2">336</td><td rowspan="2">720</td><td rowspan="2">96</td><td rowspan="2">192</td><td rowspan="2">336</td><td rowspan="2">720</td></tr><tr><td><math><semantics><msub><mi>ℒ</mi> <mrow><mi>U</mi> <mo>⁢</mo> <mi>A</mi> <mo>⁢</mo> <mi>C</mi></mrow></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><ci>𝑈</ci> <ci>𝐴</ci> <ci>𝐶</ci></apply></apply></annotation-xml> <annotation>\mathcal{L}_{UAC}</annotation> <annotation>caligraphic_L start_POSTSUBSCRIPT italic_U italic_A italic_C end_POSTSUBSCRIPT</annotation></semantics></math></td><td><math><semantics><msub><mi>ℒ</mi> <mrow><mi>R</mi> <mo>⁢</mo> <mi>E</mi> <mo>⁢</mo> <mi>G</mi></mrow></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><ci>𝑅</ci> <ci>𝐸</ci> <ci>𝐺</ci></apply></apply></annotation-xml> <annotation>\mathcal{L}_{REG}</annotation> <annotation>caligraphic_L start_POSTSUBSCRIPT italic_R italic_E italic_G end_POSTSUBSCRIPT</annotation></semantics></math></td></tr><tr><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>0.352</td><td>0.636</td><td>0.680</td><td>1.265</td><td>1.710</td><td>1.991</td><td>1.958</td><td>2.154</td></tr><tr><td>✓</td><td>-</td><td>-</td><td>-</td><td>-</td><td>0.349</td><td>0.509</td><td>0.613</td><td>0.993</td><td>0.991</td><td>1.077</td><td>1.127</td><td>1.149</td></tr><tr><td>✓</td><td>✓</td><td>-</td><td>-</td><td>-</td><td>0.300</td><td>0.515</td><td>0.579</td><td>0.999</td><td>0.964</td><td>1.060</td><td>1.129</td><td>1.125</td></tr><tr><td>✓</td><td>✓</td><td>✓</td><td>-</td><td>-</td><td>0.322</td><td>0.406</td><td>0.580</td><td>0.961</td><td>0.948</td><td>1.048</td><td>1.099</td><td>1.109</td></tr><tr><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>-</td><td>0.295</td><td>0.345</td><td>0.395</td><td>0.614</td><td>0.935</td><td>1.038</td><td>1.097</td><td>1.083</td></tr><tr><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>0.291</td><td>0.306</td><td>0.369</td><td>0.513</td><td>0.920</td><td>1.027</td><td>1.087</td><td>1.065</td></tr></tbody></table>

Table 3: Ablation study of the components of HCAN on the Weather and Solar Wind datasets using Informer as a backbone: Uncertainty-Aware Classification (UAC), Hierarchical Structure (Hierarchy), Hierarchical Consistency Loss ($\mathcal{L}_{HCL}$), and Hierarchy-Aware Attention (HAA). The results are in terms of MSE for different prediction lengths. The best results are highlighted in bold.

Multivariate Forecasting Results. We present the multivariate forecasting results in Table 1. Notably, our proposed HCAN demonstrates a substantial impact on the performance of the baselines, as it boosts their forecasting results by a noticeable margin. This is evident in 66 out of 70 cases. For instance, HCAN achieves average performance gains of 9.1%, 35.5%, 10.2%, and 22.3% on the ETT dataset series. Similar improvements also observed on other datasets.

We attribute these performance enhancements to two primary aspects. First, HCAN incorporates a reliable hierarchical classification structure that captures high-entropy features, effectively alleviating the over-smooth predictions and reducing the boundary discontinuity typically associated with classification tasks. Second, the HAA mechanism enhances prediction accuracy by fusing features at different granular levels, thereby providing more reliable information for prediction. This attribute proves particularly advantageous in long-term forecasting scenarios, which inherently pose greater challenges as the forecast horizon extends. For example, as shown in the Appendix, when forecasting a length of 720 timesteps, the integration of HCAN with Autoformer leads to a significant reduction of 31.9% in MSE on the ETTh2 dataset and a reduction of 19.3% on the Exchange dataset. These results underscore the capability of HCAN to deliver stable and reliable predictions even in long-term forecasting scenarios.

Univariate Forecasting Results. We also report the univariate forecasting outcomes for the ETT and Solar Wind datasets in Table 2. Compared to the original performance of the baseline methods, incorporating our HCAN into these models yields an overall reduction of 23.0%, 35.8%, 7.5%, 12.6%, 2.5%, 22.8%, and 1.5% in the MSE results. These results validate the effectiveness of our proposed hierarchical structure in enhancing forecasting precision.

### Ablation Study

Table 3 presents an ablation study on the Weather and Solar Wind datasets to assess the effectiveness of each module in HCAN. Referring to Figure 2, we evaluate the following settings: (1) including the UAC with only the fine-grained classes ($\mathcal{L}_{UAC}$ alone) (2) with adding $\mathcal{L}_{REG}$ to the UAC module, i.e., $\mathcal{L}_{UAC}+\mathcal{L}_{REG}$ (3) with including the coarse-grained classes and directly concatenating the multi-level features (Hierarchy) (4) with using $\mathcal{L}_{HCL}$ to keep consistency among hierarchy levels (5) with using the attention module for feature fusion instead of direct concatenation (HAA).

Impact of UAC. Initially, applying the UAC on the fine-grained features alone with $\mathcal{L}_{UAC}$ significantly enhances performance by creating a high-entropy feature space that enriches forecasting representations. Adding $\mathcal{L}_{REG}$ further improves performance by imposing relative forecasting constraints, ensuring feature continuity and coherence.

Impact of Hierarchy Structure. Implementing a hierarchical structure with two layers of UAC layers (by including the coarse-grained features) demonstrates the value of incorporating multi-granularity features, as indicated by performance gains in the ablation study.

Impact of HCL. Performance is further enhanced by integrating $\mathcal{L}_{HCL}$, which imposes a consistency constraint between hierarchies and effectively addresses boundary effects.

Impact of HAA. The best performance is observed when replacing direct concatenation with the HAA mechanism. This change indicates that different features contribute variably to forecasting outcomes, and simple concatenation can lead to sub-optimal results.

![[fig-5-SCINet.png|Refer to caption]]

(a) SCINet

![[fig-4-a-PatchTST-ETTh1-M.png|Refer to caption]]

(a) PatchTST+HCAN

### Qualitative Evaluation

High-entropy Feature Representation. The t-SNE visualization of the features from SCINet on the ETTh1 dataset is displayed in Figure 4. As depicted in Figure 4(a), representations learned from the MSE loss exhibit lower diversity. Figures 4(b) and 4(c) illustrate that integrating classification indeed spreads features more broadly, yet it disrupts ordinality in feature space. Figure 4(d) shows how the HAA mechanism combines hierarchical features with the original features from the backbone model, effectively spreading the feature while maintaining ordinality. In conclusion, HCAN facilitates reliable high-entropy feature representations through hierarchical classification, significantly helping to alleviate over-smooth predictions.

Visualizations. To examine the quality of prediction results with and without our HCAN, Figure 5 presents this comparison on PatchTST, SCINe, DLinear, and FITS backbones on the ETTh1 dataset. Clearly, our HCAN yields more realistic predictions. This enhancement is largely regarded to the proposed hierarchical consistency loss (HCL), which notably improves performance at class boundaries. These results further validate the effectiveness of the high-entropy feature representations. Additionally, they demonstrate that HCL is effective in mitigating the boundary effects.

## Conclusion

In this study, we addressed the issue of over-smooth predictions in time series forecasting by introducing a novel hierarchical classification from an entropy perspective. We proposed HCAN, a model-agnostic component that enhances forecasting by tokenizing output and integrating muti-granularity high-entropy feature representations through a hierarchical-aware attention module. The HCL loss further aids in mitigating boundary effects, promoting overall accuracy. Extensive experiments on benchmarking datasets demonstrate that HCAN substantially improves the performance of baseline forecasting models. Our results suggest that HCAN can serve as a foundation component in time series forecasting, providing deeper insights into the interplay between classification tasks and forecasting.

## Acknowledgments

This work was supported in part by the National Natural Science Foundation of China under Grants 62376194, 61925602, U23B2049, 62406219, and 62436001 and in part by the China Postdoctoral Science Foundation - Tianjin Joint Support Program under Grant 2023T014TJ.

## References

## Appendix A Datasets and Implementation Details

This subsection provides a summary of the datasets utilized in this paper:

- ETT <sup>1</sup> [^46] (Electricity Transformer Temperature) dataset contains two electric transformers, ETT1 and ETT2, collected from two separate counties. Each of them has two versions of sampling resolutions (15min & 1h). Thus, there are four ETT datasets: ETTm1, ETTm2, ETTh1, and ETTh2. Oil temperature is the target series.
- Weather <sup>2</sup> [^38] dataset contains 21 meteorological indicators in Germany, such as humidity and air temperature. The $CO_{2}$ is chosen as the target series.
- Exchange-Rate <sup>3</sup> [^12] the exchange-rate dataset contains the daily exchange rates of eight foreign countries including Australia, British, Canada, Switzerland, China, Japan, New Zealand, and Singapore ranging from 1990 to 2016. We consider the time series of 30 days as a sample for this task. The Singapore exchange is taken as the target series, and we aim to predict the exchange rate of Singapore each day of a month.
- ILI <sup>4</sup> [^38] dataset collects the number of patients and influenza-like illness ratio in a weekly frequency. The "total patients" is chosen as the target series.
- Electricity <sup>5</sup> [^38] is a dataset that describes 321 customers’ hourly electricity consumption. The "320" is chosen as the target series.
- Traffic <sup>6</sup> [^38] is a dataset featuring hourly road occupancy rates from 862 sensors along the freeways in the San Francisco Bay area. The "861" is chosen as the target series.
- Solar Wind <sup>7</sup> [^30] dataset released by NASA is a collection of hourly solar wind properties from 2011 to 2017 collected by many spacecraft orbiting the L1 point between the Sun and Earth. The solar wind speed is the target series.

For data split, we follow [^46] and split data into train/validation/test set by the ratio 6:2:2 towards ETT datasets. We follow [^44] to preprocess data and split data by the ratio of 7:1:2 in other datasets. Details are shown in Table 4

| Dataset | Variates | Prediction Length | Timesteps | Granularity |
| --- | --- | --- | --- | --- |
| ETTh1 & ETTh2 | 7 | {96, 192, 336, 720} | 17420 | 1 hour |
| ETTm1 & ETTm2 | 7 | {96, 192, 336, 720} | 69680 | 5 min |
| Weather | 21 | {96, 192, 336, 720} | 52696 | 10 min |
| Exchange-Rate | 8 | {96, 192, 336, 720} | 7588 | 1 day |
| ILI | 7 | {24, 36, 48, 60} | 966 | 7 day |
| Electricity | 321 | {96, 192, 336, 720} | 26304 | 1 hour |
| Traffic | 862 | {96, 192, 336, 720} | 17544 | 1 hour |
| Solar-Wind | 4 | {96, 192, 336, 720} | 61369 | 1 hour |

Table 4: The statistics of the ten datasets.

## Appendix B Group Mapping Strategy

We describe our partition strategy to define the boundary of each group. First, for the list of time series $y=[y_{1},...,y_{Q}]$, where $Q$ is the length of the time series, we arrange them in ascending order to obtain $\hat{y}=[\hat{y}_{1},...,\hat{y}_{Q}]$. Given the number of groups $K$, the partitioning algorithm defines the boundary of each interval $\mathcal{I}_{k}=(\rho_{k}^{\text{left}},\rho_{k}^{\text{right}})$ as follows:

$$
\displaystyle\begin{split}&\rho_{k}^{\text{left}}=\hat{y}(\lfloor(Q-1)\times%
\frac{(k-1)}{K}\rfloor),\\
&\rho_{k}^{\text{right}}=\hat{y}(\lfloor(Q-1)\times\frac{k}{K}\rfloor),\quad%
\forall k=1,2,\dots,K,\end{split}
$$

where we use $\hat{y}(k)$ to represent the $k$ -th element of y. It is worth noting that the group strategy is non-trivial. If we simply divide the entire range uniformly into multiple groups, the time series within some of these groups in the training set may be unbalanced.

## Appendix C Related Work

### Multi-scale Modeling for Time series

Recently, multi-scale modeling has gained attention for its ability to capture temporal dependencies at different granularities, which is critical for time series forecasting. Pyraformer [^17] introduces a pyramid attention mechanism to extract features at various temporal resolutions, enabling models to capture patterns at different scales. Preformer [^4] proposes multi-scale segment-wise correlations as an extension to the self-attention mechanism, enhancing the model’s ability to understand complex temporal structures. Scaleformer [^27] proposes a multi-scale framework, and the need to allocate a predictive model at different temporal resolutions results in higher model complexity. Similarly, TimesNet [^37] ravels out the complex temporal variations into the multiple intraperiod- and intrerperiod-variations to adaptively discover the multi-periodicity within the data. Pathformer [^3] further advanced this concept by using a multi-scale Transformer with adaptive pathways to capture complex temporal relationships across scales. Timemixer [^33] proposed a multi-scale mixing architecture, emphasizing that combining patterns from different scales improves forecasting accuracy.

Our work aligns with and builds upon these developments by integrating multi-scale modeling in a way that not only addresses the complexities of temporal dependencies but also enhances model flexibility across different scales.

<table><thead><tr><th colspan="2">Model</th><th colspan="2">Informer</th><th colspan="2">+HCAN</th><th colspan="2">Autoformer</th><th colspan="2">+HCAN</th><th colspan="2">PatchTST</th><th colspan="2">+HCAN</th><th colspan="2">SCINet</th><th colspan="2">+HCAN</th><th colspan="2">Dlinear</th><th colspan="2">+HCAN</th><th colspan="2">iTransforrmer</th><th colspan="2">+HCAN</th><th colspan="2">FITS</th><th colspan="2">+HCAN</th></tr><tr><th colspan="2">Metric</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th></tr></thead><tbody><tr><th rowspan="5">ETTh1</th><th>96</th><td>0.950</td><td>0.773</td><td>0.703</td><td>0.617</td><td>0.465</td><td>0.459</td><td>0.412</td><td>0.405</td><td>0.382</td><td>0.405</td><td>0.358</td><td>0.398</td><td>0.445</td><td>0.460</td><td>0.415</td><td>0.422</td><td>0.384</td><td>0.405</td><td>0.371</td><td>0.382</td><td>0.387</td><td>0.405</td><td>0.379</td><td>0.402</td><td>0.385</td><td>0.393</td><td>0.377</td><td>0.388</td></tr><tr><th>192</th><td>1.011</td><td>0.787</td><td>0.848</td><td>0.704</td><td>0.484</td><td>0.471</td><td>0.441</td><td>0.444</td><td>0.414</td><td>0.421</td><td>0.382</td><td>0.412</td><td>0.457</td><td>0.459</td><td>0.421</td><td>0.420</td><td>0.443</td><td>0.450</td><td>0.420</td><td>0.392</td><td>0.441</td><td>0.436</td><td>0.432</td><td>0.427</td><td>0.435</td><td>0.422</td><td>0.429</td><td>0.417</td></tr><tr><th>336</th><td>1.141</td><td>0.844</td><td>0.979</td><td>0.767</td><td>0.517</td><td>0.495</td><td>0.490</td><td>0.459</td><td>0.437</td><td>0.443</td><td>0.421</td><td>0.432</td><td>0.573</td><td>0.541</td><td>0.556</td><td>0.532</td><td>0.451</td><td>0.451</td><td>0.439</td><td>0.414</td><td>0.491</td><td>0.462</td><td>0.489</td><td>0.454</td><td>0.475</td><td>0.443</td><td>0.481</td><td>0.436</td></tr><tr><th>720</th><td>1.207</td><td>0.864</td><td>1.058</td><td>0.800</td><td>0.655</td><td>0.573</td><td>0.505</td><td>0.504</td><td>0.450</td><td>0.466</td><td>0.425</td><td>0.451</td><td>0.888</td><td>0.705</td><td>0.754</td><td>0.674</td><td>0.535</td><td>0.536</td><td>0.482</td><td>0.491</td><td>0.509</td><td>0.494</td><td>0.504</td><td>0.474</td><td>0.462</td><td>0.460</td><td>0.456</td><td>0.475</td></tr><tr><th>Avg</th><td>1.077</td><td>0.817</td><td>0.897</td><td>0.722</td><td>0.530</td><td>0.500</td><td>0.462</td><td>0.453</td><td>0.421</td><td>0.434</td><td>0.396</td><td>0.423</td><td>0.591</td><td>0.541</td><td>0.536</td><td>0.512</td><td>0.453</td><td>0.460</td><td>0.428</td><td>0.420</td><td>0.457</td><td>0.449</td><td>0.451</td><td>0.439</td><td>0.439</td><td>0.430</td><td>0.436</td><td>0.429</td></tr><tr><th rowspan="5">ETTh2</th><th>96</th><td>2.896</td><td>1.342</td><td>1.563</td><td>1.011</td><td>0.383</td><td>0.412</td><td>0.341</td><td>0.364</td><td>0.275</td><td>0.337</td><td>0.265</td><td>0.334</td><td>0.746</td><td>0.637</td><td>0.648</td><td>0.600</td><td>0.300</td><td>0.363</td><td>0.287</td><td>0.358</td><td>0.301</td><td>0.350</td><td>0.282</td><td>0.343</td><td>0.290</td><td>0.339</td><td>0.284</td><td>0.322</td></tr><tr><th>192</th><td>6.580</td><td>2.117</td><td>2.757</td><td>1.463</td><td>0.463</td><td>0.463</td><td>0.408</td><td>0.404</td><td>0.339</td><td>0.379</td><td>0.323</td><td>0.363</td><td>0.860</td><td>0.689</td><td>0.716</td><td>0.642</td><td>0.394</td><td>0.426</td><td>0.359</td><td>0.400</td><td>0.380</td><td>0.399</td><td>0.373</td><td>0.381</td><td>0.377</td><td>0.391</td><td>0.372</td><td>0.382</td></tr><tr><th>336</th><td>5.608</td><td>1.994</td><td>2.734</td><td>1.435</td><td>0.473</td><td>0.474</td><td>0.460</td><td>0.468</td><td>0.331</td><td>0.380</td><td>0.368</td><td>0.401</td><td>1.000</td><td>0.744</td><td>0.764</td><td>0.688</td><td>0.465</td><td>0.471</td><td>0.439</td><td>0.444</td><td>0.424</td><td>0.432</td><td>0.420</td><td>0.426</td><td>0.416</td><td>0.425</td><td>0.408</td><td>0.419</td></tr><tr><th>720</th><td>4.034</td><td>1.673</td><td>2.384</td><td>1.332</td><td>0.614</td><td>0.527</td><td>0.418</td><td>0.450</td><td>0.421</td><td>0.494</td><td>0.416</td><td>0.440</td><td>1.557</td><td>0.954</td><td>1.153</td><td>0.863</td><td>0.733</td><td>0.606</td><td>0.557</td><td>0.534</td><td>0.430</td><td>0.447</td><td>0.423</td><td>0.435</td><td>0.418</td><td>0.437</td><td>0.409</td><td>0.421</td></tr><tr><th>Avg</th><td>4.779</td><td>1.782</td><td>2.359</td><td>1.310</td><td>0.483</td><td>0.469</td><td>0.406</td><td>0.422</td><td>0.342</td><td>0.397</td><td>0.343</td><td>0.384</td><td>1.041</td><td>0.756</td><td>0.820</td><td>0.698</td><td>0.473</td><td>0.467</td><td>0.411</td><td>0.434</td><td>0.384</td><td>0.407</td><td>0.375</td><td>0.396</td><td>0.375</td><td>0.398</td><td>0.368</td><td>0.386</td></tr><tr><th rowspan="5">ETTm1</th><th>96</th><td>0.670</td><td>0.595</td><td>0.592</td><td>0.544</td><td>0.534</td><td>0.490</td><td>0.489</td><td>0.491</td><td>0.289</td><td>0.343</td><td>0.281</td><td>0.329</td><td>0.394</td><td>0.414</td><td>0.345</td><td>0.390</td><td>0.301</td><td>0.345</td><td>0.284</td><td>0.321</td><td>0.342</td><td>0.377</td><td>0.339</td><td>0.360</td><td>0.354</td><td>0.375</td><td>0.336</td><td>0.370</td></tr><tr><th>192</th><td>0.855</td><td>0.702</td><td>0.620</td><td>0.573</td><td>0.595</td><td>0.511</td><td>0.515</td><td>0.497</td><td>0.336</td><td>0.371</td><td>0.318</td><td>0.342</td><td>0.385</td><td>0.422</td><td>0.362</td><td>0.404</td><td>0.336</td><td>0.366</td><td>0.328</td><td>0.349</td><td>0.383</td><td>0.396</td><td>0.379</td><td>0.388</td><td>0.392</td><td>0.393</td><td>0.383</td><td>0.395</td></tr><tr><th>336</th><td>1.149</td><td>0.827</td><td>0.721</td><td>0.621</td><td>0.683</td><td>0.552</td><td>0.563</td><td>0.536</td><td>0.367</td><td>0.392</td><td>0.349</td><td>0.351</td><td>0.408</td><td>0.430</td><td>0.402</td><td>0.422</td><td>0.372</td><td>0.389</td><td>0.351</td><td>0.372</td><td>0.418</td><td>0.418</td><td>0.414</td><td>0.403</td><td>0.425</td><td>0.415</td><td>0.408</td><td>0.410</td></tr><tr><th>720</th><td>1.129</td><td>0.786</td><td>0.935</td><td>0.716</td><td>0.614</td><td>0.527</td><td>0.590</td><td>0.471</td><td>0.419</td><td>0.425</td><td>0.452</td><td>0.432</td><td>0.479</td><td>0.471</td><td>0.451</td><td>0.458</td><td>0.427</td><td>0.423</td><td>0.413</td><td>0.421</td><td>0.487</td><td>0.457</td><td>0.482</td><td>0.440</td><td>0.486</td><td>0.449</td><td>0.492</td><td>0.454</td></tr><tr><th>Avg</th><td>0.951</td><td>0.728</td><td>0.717</td><td>0.613</td><td>0.606</td><td>0.520</td><td>0.540</td><td>0.499</td><td>0.353</td><td>0.382</td><td>0.350</td><td>0.364</td><td>0.417</td><td>0.434</td><td>0.390</td><td>0.418</td><td>0.359</td><td>0.381</td><td>0.344</td><td>0.366</td><td>0.408</td><td>0.412</td><td>0.403</td><td>0.398</td><td>0.414</td><td>0.408</td><td>0.405</td><td>0.407</td></tr><tr><th rowspan="5">ETTm2</th><th>96</th><td>0.447</td><td>0.523</td><td>0.419</td><td>0.505</td><td>0.243</td><td>0.324</td><td>0.248</td><td>0.291</td><td>0.164</td><td>0.254</td><td>0.161</td><td>0.242</td><td>0.208</td><td>0.304</td><td>0.225</td><td>0.325</td><td>0.172</td><td>0.267</td><td>0.169</td><td>0.264</td><td>0.186</td><td>0.272</td><td>0.183</td><td>0.264</td><td>0.183</td><td>0.266</td><td>0.181</td><td>0.260</td></tr><tr><th>192</th><td>0.814</td><td>0.706</td><td>0.592</td><td>0.621</td><td>0.284</td><td>0.341</td><td>0.253</td><td>0.327</td><td>0.224</td><td>0.294</td><td>0.218</td><td>0.293</td><td>0.351</td><td>0.410</td><td>0.307</td><td>0.387</td><td>0.237</td><td>0.314</td><td>0.279</td><td>0.395</td><td>0.254</td><td>0.314</td><td>0.242</td><td>0.312</td><td>0.247</td><td>0.305</td><td>0.231</td><td>0.290</td></tr><tr><th>336</th><td>1.426</td><td>0.916</td><td>0.927</td><td>0.735</td><td>0.366</td><td>0.390</td><td>0.295</td><td>0.353</td><td>0.278</td><td>0.330</td><td>0.276</td><td>0.330</td><td>0.608</td><td>0.548</td><td>0.601</td><td>0.511</td><td>0.307</td><td>0.358</td><td>0.306</td><td>0.350</td><td>0.316</td><td>0.351</td><td>0.306</td><td>0.355</td><td>0.307</td><td>0.342</td><td>0.306</td><td>0.335</td></tr><tr><th>720</th><td>4.229</td><td>1.609</td><td>1.986</td><td>1.191</td><td>0.544</td><td>0.481</td><td>0.415</td><td>0.416</td><td>0.367</td><td>0.385</td><td>0.345</td><td>0.382</td><td>1.842</td><td>0.996</td><td>1.606</td><td>1.025</td><td>0.431</td><td>0.449</td><td>0.431</td><td>0.441</td><td>0.414</td><td>0.407</td><td>0.410</td><td>0.401</td><td>0.407</td><td>0.397</td><td>0.403</td><td>0.330</td></tr><tr><th>Avg</th><td>1.729</td><td>0.939</td><td>0.981</td><td>0.763</td><td>0.359</td><td>0.384</td><td>0.303</td><td>0.347</td><td>0.258</td><td>0.316</td><td>0.250</td><td>0.312</td><td>0.753</td><td>0.565</td><td>0.685</td><td>0.562</td><td>0.287</td><td>0.347</td><td>0.296</td><td>0.363</td><td>0.292</td><td>0.336</td><td>0.285</td><td>0.333</td><td>0.286</td><td>0.327</td><td>0.280</td><td>0.304</td></tr><tr><th rowspan="5">Weather</th><th>96</th><td>0.352</td><td>0.419</td><td>0.291</td><td>0.371</td><td>0.291</td><td>0.359</td><td>0.255</td><td>0.344</td><td>0.304</td><td>0.309</td><td>0.287</td><td>0.289</td><td>0.156</td><td>0.212</td><td>0.149</td><td>0.204</td><td>0.175</td><td>0.236</td><td>0.164</td><td>0.219</td><td>0.176</td><td>0.216</td><td>0.161</td><td>0.242</td><td>0.167</td><td>0.214</td><td>0.165</td><td>0.208</td></tr><tr><th>192</th><td>0.636</td><td>0.562</td><td>0.306</td><td>0.382</td><td>0.315</td><td>0.374</td><td>0.283</td><td>0.363</td><td>0.197</td><td>0.243</td><td>0.183</td><td>0.238</td><td>0.216</td><td>0.263</td><td>0.197</td><td>0.249</td><td>0.218</td><td>0.278</td><td>0.205</td><td>0.264</td><td>0.225</td><td>0.257</td><td>0.218</td><td>0.298</td><td>0.215</td><td>0.257</td><td>0.211</td><td>0.254</td></tr><tr><th>336</th><td>0.680</td><td>0.584</td><td>0.369</td><td>0.438</td><td>0.378</td><td>0.408</td><td>0.318</td><td>0.383</td><td>0.250</td><td>0.284</td><td>0.239</td><td>0.280</td><td>0.268</td><td>0.308</td><td>0.241</td><td>0.280</td><td>0.263</td><td>0.314</td><td>0.258</td><td>0.309</td><td>0.281</td><td>0.299</td><td>0.276</td><td>0.347</td><td>0.267</td><td>0.293</td><td>0.270</td><td>0.295</td></tr><tr><th>720</th><td>1.265</td><td>0.815</td><td>0.513</td><td>0.545</td><td>0.423</td><td>0.431</td><td>0.356</td><td>0.396</td><td>0.320</td><td>0.334</td><td>0.305</td><td>0.320</td><td>0.329</td><td>0.351</td><td>0.312</td><td>0.344</td><td>0.332</td><td>0.374</td><td>0.319</td><td>0.357</td><td>0.358</td><td>0.350</td><td>0.345</td><td>0.392</td><td>0.347</td><td>0.345</td><td>0.345</td><td>0.344</td></tr><tr><th>Avg</th><td>0.733</td><td>0.595</td><td>0.370</td><td>0.434</td><td>0.351</td><td>0.393</td><td>0.303</td><td>0.371</td><td>0.268</td><td>0.293</td><td>0.254</td><td>0.282</td><td>0.242</td><td>0.283</td><td>0.225</td><td>0.269</td><td>0.247</td><td>0.300</td><td>0.237</td><td>0.287</td><td>0.260</td><td>0.280</td><td>0.250</td><td>0.320</td><td>0.249</td><td>0.277</td><td>0.248</td><td>0.275</td></tr><tr><th rowspan="5">Exchange</th><th>96</th><td>0.953</td><td>0.776</td><td>0.653</td><td>0.667</td><td>0.150</td><td>0.281</td><td>0.147</td><td>0.308</td><td>0.090</td><td>0.211</td><td>0.081</td><td>0.194</td><td>0.405</td><td>0.461</td><td>0.123</td><td>0.264</td><td>0.085</td><td>0.209</td><td>0.078</td><td>0.197</td><td>0.086</td><td>0.206</td><td>0.084</td><td>0.204</td><td>0.088</td><td>0.210</td><td>0.086</td><td>0.210</td></tr><tr><th>192</th><td>1.238</td><td>0.880</td><td>0.731</td><td>0.717</td><td>0.298</td><td>0.398</td><td>0.229</td><td>0.300</td><td>0.199</td><td>0.318</td><td>0.173</td><td>0.247</td><td>0.569</td><td>0.550</td><td>0.269</td><td>0.401</td><td>0.162</td><td>0.296</td><td>0.158</td><td>0.282</td><td>0.181</td><td>0.304</td><td>0.179</td><td>0.302</td><td>0.181</td><td>0.304</td><td>0.179</td><td>0.301</td></tr><tr><th>336</th><td>1.791</td><td>1.070</td><td>1.091</td><td>0.874</td><td>0.511</td><td>0.535</td><td>0.345</td><td>0.575</td><td>0.369</td><td>0.443</td><td>0.281</td><td>0.375</td><td>0.792</td><td>0.652</td><td>0.596</td><td>0.598</td><td>0.333</td><td>0.441</td><td>0.293</td><td>0.431</td><td>0.338</td><td>0.422</td><td>0.322</td><td>0.415</td><td>0.324</td><td>0.413</td><td>0.323</td><td>0.411</td></tr><tr><th>720</th><td>2.920</td><td>1.410</td><td>0.906</td><td>0.750</td><td>1.139</td><td>0.832</td><td>0.920</td><td>0.727</td><td>1.407</td><td>0.850</td><td>0.842</td><td>0.639</td><td>1.609</td><td>0.978</td><td>1.210</td><td>0.850</td><td>0.898</td><td>0.725</td><td>0.821</td><td>0.782</td><td>0.853</td><td>0.696</td><td>0.995</td><td>0.761</td><td>0.846</td><td>0.696</td><td>1.117</td><td>0.785</td></tr><tr><th>Avg</th><td>1.726</td><td>1.034</td><td>0.845</td><td>0.752</td><td>0.525</td><td>0.511</td><td>0.410</td><td>0.477</td><td>0.516</td><td>0.456</td><td>0.344</td><td>0.364</td><td>0.844</td><td>0.660</td><td>0.549</td><td>0.528</td><td>0.369</td><td>0.418</td><td>0.338</td><td>0.423</td><td>0.364</td><td>0.407</td><td>0.395</td><td>0.421</td><td>0.360</td><td>0.406</td><td>0.426</td><td>0.427</td></tr><tr><th rowspan="5">ILI</th><th>24</th><td>2.902</td><td>1.175</td><td>2.751</td><td>1.117</td><td>4.724</td><td>1.509</td><td>3.660</td><td>1.355</td><td>1.431</td><td>0.797</td><td>1.326</td><td>0.696</td><td>3.224</td><td>1.276</td><td>3.127</td><td>1.219</td><td>2.280</td><td>1.061</td><td>2.249</td><td>1.057</td><td>2.443</td><td>1.078</td><td>2.389</td><td>1.038</td><td>3.489</td><td>1.373</td><td>2.193</td><td>0.987</td></tr><tr><th>36</th><td>2.897</td><td>1.182</td><td>2.745</td><td>1.178</td><td>4.914</td><td>1.547</td><td>3.987</td><td>1.388</td><td>1.443</td><td>0.828</td><td>1.319</td><td>0.808</td><td>3.287</td><td>1.264</td><td>3.243</td><td>1.230</td><td>2.235</td><td>1.059</td><td>2.214</td><td>1.053</td><td>2.455</td><td>1.086</td><td>2.432</td><td>1.042</td><td>3.530</td><td>1.370</td><td>2.080</td><td>0.971</td></tr><tr><th>48</th><td>2.872</td><td>1.158</td><td>2.711</td><td>1.106</td><td>5.115</td><td>1.582</td><td>4.398</td><td>1.399</td><td>1.710</td><td>0.892</td><td>1.672</td><td>0.870</td><td>3.206</td><td>1.251</td><td>3.117</td><td>1.253</td><td>2.298</td><td>1.079</td><td>2.262</td><td>1.069</td><td>3.437</td><td>1.331</td><td>3.412</td><td>1.329</td><td>3.671</td><td>1.391</td><td>2.122</td><td>0.969</td></tr><tr><th>60</th><td>2.887</td><td>1.154</td><td>2.746</td><td>1.104</td><td>5.293</td><td>1.623</td><td>4.620</td><td>1.487</td><td>1.480</td><td>0.769</td><td>1.397</td><td>0.718</td><td>3.390</td><td>1.306</td><td>3.575</td><td>1.310</td><td>2.573</td><td>1.157</td><td>2.378</td><td>1.024</td><td>2.734</td><td>1.155</td><td>2.730</td><td>1.152</td><td>4.030</td><td>1.462</td><td>1.986</td><td>0.966</td></tr><tr><th>Avg</th><td>2.889</td><td>1.167</td><td>2.738</td><td>1.126</td><td>5.012</td><td>1.565</td><td>4.166</td><td>1.407</td><td>1.516</td><td>0.821</td><td>1.428</td><td>0.773</td><td>3.277</td><td>1.274</td><td>3.265</td><td>1.253</td><td>2.347</td><td>1.089</td><td>2.276</td><td>1.051</td><td>2.767</td><td>1.162</td><td>2.741</td><td>1.140</td><td>3.680</td><td>1.399</td><td>2.095</td><td>0.973</td></tr><tr><th rowspan="5">Electricity</th><th>96</th><td>0.322</td><td>0.409</td><td>0.319</td><td>0.405</td><td>0.204</td><td>0.319</td><td>0.201</td><td>0.372</td><td>0.278</td><td>0.353</td><td>0.249</td><td>0.325</td><td>0.183</td><td>0.285</td><td>0.177</td><td>0.279</td><td>0.195</td><td>0.277</td><td>0.189</td><td>0.268</td><td>0.148</td><td>0.239</td><td>0.130</td><td>0.229</td><td>0.200</td><td>0.278</td><td>0.197</td><td>0.285</td></tr><tr><th>192</th><td>0.346</td><td>0.430</td><td>0.307</td><td>0.415</td><td>0.223</td><td>0.330</td><td>0.209</td><td>0.313</td><td>0.257</td><td>0.335</td><td>0.213</td><td>0.304</td><td>0.207</td><td>0.306</td><td>0.201</td><td>0.302</td><td>0.194</td><td>0.280</td><td>0.199</td><td>0.279</td><td>0.167</td><td>0.258</td><td>0.164</td><td>0.234</td><td>0.200</td><td>0.281</td><td>0.198</td><td>0.280</td></tr><tr><th>336</th><td>0.355</td><td>0.436</td><td>0.348</td><td>0.408</td><td>0.237</td><td>0.342</td><td>0.216</td><td>0.313</td><td>0.273</td><td>0.350</td><td>0.259</td><td>0.312</td><td>0.213</td><td>0.315</td><td>0.208</td><td>0.309</td><td>0.207</td><td>0.296</td><td>0.204</td><td>0.289</td><td>0.178</td><td>0.271</td><td>0.169</td><td>0.269</td><td>0.214</td><td>0.295</td><td>0.213</td><td>0.295</td></tr><tr><th>720</th><td>0.388</td><td>0.452</td><td>0.373</td><td>0.421</td><td>0.337</td><td>0.405</td><td>0.317</td><td>0.402</td><td>0.230</td><td>0.311</td><td>0.210</td><td>0.301</td><td>0.251</td><td>0.338</td><td>0.248</td><td>0.319</td><td>0.243</td><td>0.328</td><td>0.239</td><td>0.323</td><td>0.209</td><td>0.298</td><td>0.205</td><td>0.284</td><td>0.256</td><td>0.328</td><td>0.255</td><td>0.328</td></tr><tr><th>Avg</th><td>0.352</td><td>0.432</td><td>0.337</td><td>0.412</td><td>0.250</td><td>0.349</td><td>0.236</td><td>0.350</td><td>0.259</td><td>0.337</td><td>0.233</td><td>0.311</td><td>0.213</td><td>0.311</td><td>0.209</td><td>0.302</td><td>0.210</td><td>0.296</td><td>0.208</td><td>0.290</td><td>0.176</td><td>0.267</td><td>0.167</td><td>0.254</td><td>0.217</td><td>0.295</td><td>0.216</td><td>0.297</td></tr><tr><th rowspan="5">Traffic</th><th>96</th><td>0.742</td><td>0.414</td><td>0.726</td><td>0.405</td><td>0.645</td><td>0.414</td><td>0.505</td><td>0.417</td><td>0.446</td><td>0.283</td><td>0.403</td><td>0.215</td><td>0.630</td><td>0.365</td><td>0.503</td><td>0.274</td><td>0.650</td><td>0.397</td><td>0.630</td><td>0.371</td><td>0.392</td><td>0.268</td><td>0.383</td><td>0.262</td><td>0.658</td><td>0.409</td><td>0.687</td><td>0.422</td></tr><tr><th>192</th><td>0.759</td><td>0.428</td><td>0.739</td><td>0.416</td><td>0.619</td><td>0.387</td><td>0.507</td><td>0.304</td><td>0.453</td><td>0.286</td><td>0.408</td><td>0.252</td><td>0.541</td><td>0.334</td><td>0.473</td><td>0.249</td><td>0.600</td><td>0.372</td><td>0.573</td><td>0.347</td><td>0.413</td><td>0.277</td><td>0.411</td><td>0.273</td><td>0.620</td><td>0.371</td><td>0.592</td><td>0.358</td></tr><tr><th>336</th><td>0.877</td><td>0.494</td><td>0.872</td><td>0.429</td><td>0.621</td><td>0.380</td><td>0.557</td><td>0.368</td><td>0.468</td><td>0.291</td><td>0.429</td><td>0.270</td><td>0.592</td><td>0.365</td><td>0.583</td><td>0.339</td><td>0.606</td><td>0.374</td><td>0.584</td><td>0.350</td><td>0.425</td><td>0.283</td><td>0.420</td><td>0.279</td><td>0.619</td><td>0.368</td><td>0.586</td><td>0.346</td></tr><tr><th>720</th><td>1.034</td><td>0.581</td><td>0.934</td><td>0.523</td><td>0.718</td><td>0.442</td><td>0.639</td><td>0.385</td><td>0.594</td><td>0.384</td><td>0.598</td><td>0.389</td><td>0.684</td><td>0.426</td><td>0.548</td><td>0.386</td><td>0.646</td><td>0.396</td><td>0.602</td><td>0.382</td><td>0.458</td><td>0.300</td><td>0.449</td><td>0.296</td><td>0.669</td><td>0.391</td><td>0.632</td><td>0.372</td></tr><tr><th>Avg</th><td>0.853</td><td>0.479</td><td>0.818</td><td>0.443</td><td>0.651</td><td>0.406</td><td>0.552</td><td>0.369</td><td>0.490</td><td>0.311</td><td>0.460</td><td>0.282</td><td>0.612</td><td>0.373</td><td>0.527</td><td>0.312</td><td>0.625</td><td>0.385</td><td>0.597</td><td>0.363</td><td>0.422</td><td>0.282</td><td>0.416</td><td>0.278</td><td>0.642</td><td>0.385</td><td>0.624</td><td>0.375</td></tr><tr><th rowspan="5">Solar Wind</th><th>96</th><td>1.710</td><td>0.759</td><td>0.920</td><td>0.633</td><td>1.193</td><td>0.765</td><td>0.950</td><td>0.643</td><td>1.121</td><td>0.687</td><td>0.914</td><td>0.629</td><td>1.113</td><td>0.676</td><td>0.980</td><td>0.612</td><td>1.008</td><td>0.657</td><td>0.906</td><td>0.614</td><td>1.210</td><td>0.739</td><td>0.912</td><td>0.623</td><td>1.234</td><td>0.762</td><td>1.089</td><td>0.690</td></tr><tr><th>192</th><td>1.991</td><td>0.801</td><td>1.027</td><td>0.687</td><td>1.530</td><td>0.890</td><td>1.068</td><td>0.689</td><td>1.130</td><td>0.737</td><td>1.017</td><td>0.674</td><td>1.205</td><td>0.714</td><td>1.142</td><td>0.679</td><td>1.076</td><td>0.691</td><td>1.021</td><td>0.667</td><td>1.433</td><td>0.828</td><td>1.029</td><td>0.675</td><td>1.410</td><td>0.833</td><td>1.291</td><td>0.779</td></tr><tr><th>336</th><td>1.958</td><td>0.826</td><td>1.087</td><td>0.714</td><td>1.437</td><td>0.852</td><td>1.108</td><td>0.706</td><td>1.137</td><td>0.741</td><td>1.039</td><td>0.688</td><td>1.221</td><td>0.724</td><td>1.157</td><td>0.685</td><td>1.100</td><td>0.702</td><td>1.079</td><td>0.689</td><td>1.415</td><td>0.820</td><td>1.088</td><td>0.699</td><td>1.394</td><td>0.825</td><td>1.304</td><td>0.781</td></tr><tr><th>720</th><td>2.154</td><td>0.823</td><td>1.065</td><td>0.702</td><td>1.286</td><td>0.799</td><td>1.103</td><td>0.702</td><td>1.046</td><td>0.701</td><td>0.821</td><td>0.673</td><td>1.155</td><td>0.699</td><td>1.086</td><td>0.661</td><td>1.097</td><td>0.700</td><td>1.072</td><td>0.688</td><td>1.381</td><td>0.804</td><td>1.083</td><td>0.703</td><td>1.358</td><td>0.814</td><td>1.275</td><td>0.773</td></tr><tr><th>Avg</th><td>1.953</td><td>0.803</td><td>1.025</td><td>0.684</td><td>1.362</td><td>0.826</td><td>1.057</td><td>0.685</td><td>1.109</td><td>0.717</td><td>0.948</td><td>0.666</td><td>1.174</td><td>0.703</td><td>1.091</td><td>0.659</td><td>1.071</td><td>0.687</td><td>1.019</td><td>0.665</td><td>1.360</td><td>0.798</td><td>1.028</td><td>0.675</td><td>1.349</td><td>0.809</td><td>1.239</td><td>0.756</td></tr></tbody></table>

Table 5: Multivariate long sequence time-series forecasting results. We report the MSE/MAE of different prediction lengths. The look-up window is set to $L=336$ for PatchTST, DLinear, and SCINet, and $L=96$ for other models. The best results are highlighted in bold.

<table><thead><tr><th colspan="2">Model</th><th colspan="2">Informer</th><th colspan="2">+HCAN</th><th colspan="2">Autoformer</th><th colspan="2">+HCAN</th><th colspan="2">PatchTST</th><th colspan="2">+HCAN</th><th colspan="2">SCINet</th><th colspan="2">+HCAN</th><th colspan="2">Dlinear</th><th colspan="2">+HCAN</th><th colspan="2">iTransforrmer</th><th colspan="2">+HCAN</th><th colspan="2">FITS</th><th colspan="2">+HCAN</th></tr><tr><th colspan="2">Metric</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th></tr></thead><tbody><tr><th rowspan="4">ETTh1</th><th>96</th><td>0.255</td><td>0.438</td><td>0.121</td><td>0.283</td><td>0.088</td><td>0.234</td><td>0.082</td><td>0.223</td><td>0.055</td><td>0.179</td><td>0.055</td><td>0.181</td><td>0.088</td><td>0.227</td><td>0.068</td><td>0.197</td><td>0.057</td><td>0.179</td><td>0.053</td><td>0.178</td><td>0.061</td><td>0.190</td><td>0.060</td><td>0.187</td><td>0.056</td><td>0.179</td><td>0.054</td><td>0.178</td></tr><tr><th>192</th><td>0.283</td><td>0.461</td><td>0.092</td><td>0.236</td><td>0.108</td><td>0.252</td><td>0.086</td><td>0.223</td><td>0.071</td><td>0.205</td><td>0.072</td><td>0.206</td><td>0.105</td><td>0.249</td><td>0.084</td><td>0.221</td><td>0.077</td><td>0.210</td><td>0.075</td><td>0.209</td><td>0.073</td><td>0.206</td><td>0.072</td><td>0.205</td><td>0.075</td><td>0.210</td><td>0.072</td><td>0.209</td></tr><tr><th>336</th><td>0.291</td><td>0.469</td><td>0.088</td><td>0.230</td><td>0.118</td><td>0.268</td><td>0.091</td><td>0.237</td><td>0.082</td><td>0.227</td><td>0.078</td><td>0.217</td><td>0.130</td><td>0.286</td><td>0.094</td><td>0.244</td><td>0.097</td><td>0.244</td><td>0.088</td><td>0.235</td><td>0.089</td><td>0.231</td><td>0.087</td><td>0.230</td><td>0.091</td><td>0.237</td><td>0.089</td><td>0.236</td></tr><tr><th>720</th><td>0.256</td><td>0.426</td><td>0.106</td><td>0.260</td><td>0.138</td><td>0.298</td><td>0.121</td><td>0.279</td><td>0.086</td><td>0.232</td><td>0.081</td><td>0.204</td><td>0.214</td><td>0.387</td><td>0.134</td><td>0.292</td><td>0.168</td><td>0.336</td><td>0.164</td><td>0.331</td><td>0.083</td><td>0.226</td><td>0.105</td><td>0.258</td><td>0.104</td><td>0.254</td><td>0.096</td><td>0.245</td></tr><tr><th rowspan="4">ETTh2</th><th>96</th><td>0.302</td><td>0.446</td><td>0.182</td><td>0.349</td><td>0.169</td><td>0.321</td><td>0.140</td><td>0.295</td><td>0.129</td><td>0.282</td><td>0.127</td><td>0.278</td><td>0.130</td><td>0.281</td><td>0.129</td><td>0.280</td><td>0.133</td><td>0.281</td><td>0.128</td><td>0.271</td><td>0.135</td><td>0.286</td><td>0.133</td><td>0.283</td><td>0.125</td><td>0.269</td><td>0.123</td><td>0.268</td></tr><tr><th>192</th><td>0.264</td><td>0.414</td><td>0.206</td><td>0.365</td><td>0.211</td><td>0.359</td><td>0.179</td><td>0.328</td><td>0.169</td><td>0.328</td><td>0.162</td><td>0.305</td><td>0.327</td><td>0.459</td><td>0.169</td><td>0.326</td><td>0.177</td><td>0.330</td><td>0.174</td><td>0.325</td><td>0.182</td><td>0.336</td><td>0.178</td><td>0.334</td><td>0.177</td><td>0.327</td><td>0.174</td><td>0.325</td></tr><tr><th>336</th><td>0.324</td><td>0.456</td><td>0.223</td><td>0.385</td><td>0.255</td><td>0.398</td><td>0.226</td><td>0.373</td><td>0.187</td><td>0.352</td><td>0.187</td><td>0.340</td><td>0.198</td><td>0.358</td><td>0.220</td><td>0.378</td><td>0.212</td><td>0.369</td><td>0.225</td><td>0.375</td><td>0.218</td><td>0.373</td><td>0.215</td><td>0.371</td><td>0.222</td><td>0.375</td><td>0.221</td><td>0.371</td></tr><tr><th>720</th><td>0.302</td><td>0.447</td><td>0.249</td><td>0.408</td><td>0.334</td><td>0.459</td><td>0.292</td><td>0.432</td><td>0.224</td><td>0.383</td><td>0.201</td><td>0.357</td><td>0.486</td><td>0.569</td><td>0.221</td><td>0.377</td><td>0.298</td><td>0.444</td><td>0.259</td><td>0.413</td><td>0.240</td><td>0.391</td><td>0.238</td><td>0.389</td><td>0.258</td><td>0.409</td><td>0.255</td><td>0.406</td></tr><tr><th rowspan="4">ETTm1</th><th>96</th><td>0.093</td><td>0.249</td><td>0.046</td><td>0.166</td><td>0.059</td><td>0.186</td><td>0.047</td><td>0.167</td><td>0.026</td><td>0.121</td><td>0.024</td><td>0.123</td><td>0.049</td><td>0.170</td><td>0.029</td><td>0.127</td><td>0.030</td><td>0.128</td><td>0.026</td><td>0.125</td><td>0.029</td><td>0.128</td><td>0.028</td><td>0.124</td><td>0.029</td><td>0.127</td><td>0.027</td><td>0.126</td></tr><tr><th>192</th><td>0.232</td><td>0.404</td><td>0.059</td><td>0.189</td><td>0.081</td><td>0.223</td><td>0.057</td><td>0.187</td><td>0.039</td><td>0.150</td><td>0.037</td><td>0.148</td><td>0.077</td><td>0.215</td><td>0.049</td><td>0.166</td><td>0.044</td><td>0.155</td><td>0.043</td><td>0.151</td><td>0.049</td><td>0.169</td><td>0.045</td><td>0.167</td><td>0.043</td><td>0.158</td><td>0.042</td><td>0.155</td></tr><tr><th>336</th><td>0.271</td><td>0.453</td><td>0.108</td><td>0.264</td><td>0.088</td><td>0.242</td><td>0.072</td><td>0.205</td><td>0.053</td><td>0.173</td><td>0.050</td><td>0.168</td><td>0.109</td><td>0.259</td><td>0.089</td><td>0.229</td><td>0.064</td><td>0.187</td><td>0.059</td><td>0.183</td><td>0.061</td><td>0.190</td><td>0.060</td><td>0.187</td><td>0.057</td><td>0.183</td><td>0.056</td><td>0.181</td></tr><tr><th>720</th><td>0.464</td><td>0.606</td><td>0.118</td><td>0.277</td><td>0.122</td><td>0.275</td><td>0.079</td><td>0.214</td><td>0.074</td><td>0.207</td><td>0.070</td><td>0.203</td><td>0.139</td><td>0.296</td><td>0.117</td><td>0.261</td><td>0.081</td><td>0.211</td><td>0.082</td><td>0.216</td><td>0.083</td><td>0.220</td><td>0.082</td><td>0.218</td><td>0.079</td><td>0.216</td><td>0.075</td><td>0.216</td></tr><tr><th rowspan="4">ETTm2</th><th>96</th><td>0.092</td><td>0.233</td><td>0.065</td><td>0.209</td><td>0.127</td><td>0.274</td><td>0.095</td><td>0.239</td><td>0.065</td><td>0.186</td><td>0.065</td><td>0.185</td><td>0.079</td><td>0.216</td><td>0.069</td><td>0.195</td><td>0.064</td><td>0.184</td><td>0.061</td><td>0.181</td><td>0.069</td><td>0.189</td><td>0.069</td><td>0.187</td><td>0.070</td><td>0.190</td><td>0.069</td><td>0.189</td></tr><tr><th>192</th><td>0.134</td><td>0.283</td><td>0.107</td><td>0.255</td><td>0.146</td><td>0.295</td><td>0.123</td><td>0.270</td><td>0.094</td><td>0.231</td><td>0.091</td><td>0.227</td><td>0.105</td><td>0.252</td><td>0.094</td><td>0.232</td><td>0.092</td><td>0.227</td><td>0.087</td><td>0.217</td><td>0.107</td><td>0.244</td><td>0.106</td><td>0.242</td><td>0.100</td><td>0.235</td><td>0.098</td><td>0.233</td></tr><tr><th>336</th><td>0.178</td><td>0.340</td><td>0.141</td><td>0.298</td><td>0.217</td><td>0.359</td><td>0.126</td><td>0.278</td><td>0.120</td><td>0.265</td><td>0.117</td><td>0.259</td><td>0.130</td><td>0.282</td><td>0.128</td><td>0.276</td><td>0.129</td><td>0.273</td><td>0.120</td><td>0.262</td><td>0.144</td><td>0.289</td><td>0.143</td><td>0.286</td><td>0.128</td><td>0.271</td><td>0.126</td><td>0.270</td></tr><tr><th>720</th><td>0.221</td><td>0.375</td><td>0.156</td><td>0.313</td><td>0.198</td><td>0.348</td><td>0.184</td><td>0.335</td><td>0.172</td><td>0.322</td><td>0.169</td><td>0.310</td><td>0.175</td><td>0.328</td><td>0.155</td><td>0.307</td><td>0.176</td><td>0.321</td><td>0.181</td><td>0.326</td><td>0.185</td><td>0.337</td><td>0.187</td><td>0.334</td><td>0.178</td><td>0.326</td><td>0.176</td><td>0.324</td></tr><tr><th rowspan="4">Solar Wind</th><th>96</th><td>1.443</td><td>0.892</td><td>1.268</td><td>0.823</td><td>2.316</td><td>1.220</td><td>1.289</td><td>0.870</td><td>1.021</td><td>0.687</td><td>0.851</td><td>0.663</td><td>1.518</td><td>0.885</td><td>1.366</td><td>0.815</td><td>1.316</td><td>0.849</td><td>1.223</td><td>0.812</td><td>1.727</td><td>0.977</td><td>1.266</td><td>0.823</td><td>1.669</td><td>0.969</td><td>1.658</td><td>0.954</td></tr><tr><th>192</th><td>1.765</td><td>1.003</td><td>1.581</td><td>0.963</td><td>2.765</td><td>1.364</td><td>1.590</td><td>0.965</td><td>1.130</td><td>0.757</td><td>1.030</td><td>0.738</td><td>1.836</td><td>1.003</td><td>1.723</td><td>0.952</td><td>1.568</td><td>0.941</td><td>1.549</td><td>0.934</td><td>2.273</td><td>1.179</td><td>1.568</td><td>0.948</td><td>2.308</td><td>1.198</td><td>2.280</td><td>1.174</td></tr><tr><th>336</th><td>1.849</td><td>1.047</td><td>1.740</td><td>1.023</td><td>2.783</td><td>1.351</td><td>1.715</td><td>1.013</td><td>1.137</td><td>0.791</td><td>1.098</td><td>0.747</td><td>1.853</td><td>1.020</td><td>1.746</td><td>0.979</td><td>1.686</td><td>0.998</td><td>1.671</td><td>0.995</td><td>2.370</td><td>1.218</td><td>1.714</td><td>1.010</td><td>2.355</td><td>1.220</td><td>2.327</td><td>1.200</td></tr><tr><th>720</th><td>1.826</td><td>1.052</td><td>1.694</td><td>1.019</td><td>2.606</td><td>1.300</td><td>1.701</td><td>1.022</td><td>1.125</td><td>0.792</td><td>1.041</td><td>0.703</td><td>1.672</td><td>0.976</td><td>1.547</td><td>0.933</td><td>1.660</td><td>0.997</td><td>1.654</td><td>0.990</td><td>2.228</td><td>1.183</td><td>1.679</td><td>1.001</td><td>2.220</td><td>1.185</td><td>2.189</td><td>1.163</td></tr></tbody></table>

Table 6: Univariate long sequence time-series forecasting results on ETT full benchmark and Solar Wind dataset. We report the MSE/MAE of different prediction lengths $T\in\{96,192,336,720\}$ for comparison. The look-up window is set to $L=336$ for PatchTST, DLinear, and SCINet, and $L=96$ for other models. The best results are highlighted in bold.

<table><tbody><tr><th colspan="2" rowspan="2">Model</th><td colspan="6">PatchTST</td><td colspan="6">FITS</td></tr><tr><td colspan="2">+ HCAN</td><td colspan="2">+ MAE</td><td colspan="2">+ Ordinal Entropy</td><td colspan="2">+ HCAN</td><td colspan="2">+ MAE</td><td colspan="2">+ Ordinal Entropy</td></tr><tr><th colspan="2">Metric</th><td>MSE</td><td>MAE</td><td>MSE</td><td>MAE</td><td>MSE</td><td>MAE</td><td>MSE</td><td>MAE</td><td>MSE</td><td>MAE</td><td>MSE</td><td>MAE</td></tr><tr><th rowspan="4">ETTh1</th><th>96</th><td>0.358</td><td>0.398</td><td>0.367</td><td>0.392</td><td>0.389</td><td>0.394</td><td>0.377</td><td>0.388</td><td>0.384</td><td>0.388</td><td>0.398</td><td>0.423</td></tr><tr><th>192</th><td>0.382</td><td>0.412</td><td>0.411</td><td>0.416</td><td>0.445</td><td>0.456</td><td>0.429</td><td>0.417</td><td>0.436</td><td>0.418</td><td>0.469</td><td>0.479</td></tr><tr><th>336</th><td>0.421</td><td>0.432</td><td>0.431</td><td>0.427</td><td>0.452</td><td>0.472</td><td>0.481</td><td>0.436</td><td>0.478</td><td>0.439</td><td>0.498</td><td>0.521</td></tr><tr><th>720</th><td>0.425</td><td>0.451</td><td>0.439</td><td>0.455</td><td>0.453</td><td>0.461</td><td>0.456</td><td>0.475</td><td>0.462</td><td>0.455</td><td>0.472</td><td>0.489</td></tr><tr><th rowspan="4">ETTh2</th><th>96</th><td>0.265</td><td>0.334</td><td>0.277</td><td>0.331</td><td>0.323</td><td>0.347</td><td>0.284</td><td>0.322</td><td>0.292</td><td>0.337</td><td>0.334</td><td>0.348</td></tr><tr><th>192</th><td>0.323</td><td>0.363</td><td>0.346</td><td>0.377</td><td>0.356</td><td>0.372</td><td>0.372</td><td>0.382</td><td>0.377</td><td>0.389</td><td>0.401</td><td>0.417</td></tr><tr><th>336</th><td>0.368</td><td>0.401</td><td>0.372</td><td>0.378</td><td>0.397</td><td>0.413</td><td>0.408</td><td>0.419</td><td>0.419</td><td>0.425</td><td>0.438</td><td>0.446</td></tr><tr><th>720</th><td>0.416</td><td>0.440</td><td>0.385</td><td>0.416</td><td>0.439</td><td>0.456</td><td>0.409</td><td>0.421</td><td>0.419</td><td>0.436</td><td>0.437</td><td>0.446</td></tr><tr><th rowspan="4">ETTm1</th><th>96</th><td>0.281</td><td>0.329</td><td>0.293</td><td>0.329</td><td>0.293</td><td>0.302</td><td>0.336</td><td>0.370</td><td>0.337</td><td>0.353</td><td>0.392</td><td>0.402</td></tr><tr><th>192</th><td>0.318</td><td>0.342</td><td>0.337</td><td>0.360</td><td>0.351</td><td>0.363</td><td>0.383</td><td>0.395</td><td>0.385</td><td>0.376</td><td>0.458</td><td>0.469</td></tr><tr><th>336</th><td>0.349</td><td>0.351</td><td>0.381</td><td>0.386</td><td>0.372</td><td>0.384</td><td>0.408</td><td>0.410</td><td>0.418</td><td>0.398</td><td>0.469</td><td>0.483</td></tr><tr><th>720</th><td>0.452</td><td>0.432</td><td>0.431</td><td>0.416</td><td>0.473</td><td>0.483</td><td>0.492</td><td>0.454</td><td>0.486</td><td>0.436</td><td>0.572</td><td>0.593</td></tr><tr><th rowspan="4">ETTm2</th><th>96</th><td>0.161</td><td>0.242</td><td>0.162</td><td>0.246</td><td>0.169</td><td>0.173</td><td>0.181</td><td>0.260</td><td>0.183</td><td>0.258</td><td>0.274</td><td>0.289</td></tr><tr><th>192</th><td>0.218</td><td>0.293</td><td>0.219</td><td>0.286</td><td>0.253</td><td>0.265</td><td>0.231</td><td>0.290</td><td>0.247</td><td>0.299</td><td>0.321</td><td>0.342</td></tr><tr><th>336</th><td>0.276</td><td>0.330</td><td>0.272</td><td>0.321</td><td>0.352</td><td>0.361</td><td>0.306</td><td>0.335</td><td>0.308</td><td>0.338</td><td>0.389</td><td>0.397</td></tr><tr><th>720</th><td>0.345</td><td>0.382</td><td>0.355</td><td>0.374</td><td>0.398</td><td>0.413</td><td>0.403</td><td>0.330</td><td>0.408</td><td>0.394</td><td>0.504</td><td>0.518</td></tr></tbody></table>

Table 7: Comparison with the regularization techniques.

## Appendix D Full Forecasting Results

The full multivariate forecasting results are provided in the following section due to the space limitation of the main text. Table 5 presents the detailed multivariate results of all prediction lengths in terms of MSE/MAE across ten well-acknowledged benchmarks. And Table 6 provides the univariate results for MSE/MAE. Our proposed model consistently achieves state-of-the-art performance in real-world forecasting applications.

## Appendix E Comparison with the regularization techniques

<table><tbody><tr><td colspan="5">Component</td><td colspan="4">iTransformer</td><td colspan="4">Dlinear</td></tr><tr><td colspan="2">UAC</td><td rowspan="2">Hierarchy</td><td rowspan="2"><math><semantics><msub><mi>ℒ</mi> <mrow><mi>H</mi> <mo>⁢</mo> <mi>C</mi> <mo>⁢</mo> <mi>L</mi></mrow></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><ci>𝐻</ci> <ci>𝐶</ci> <ci>𝐿</ci></apply></apply></annotation-xml> <annotation>\mathcal{L}_{HCL}</annotation> <annotation>caligraphic_L start_POSTSUBSCRIPT italic_H italic_C italic_L end_POSTSUBSCRIPT</annotation></semantics></math></td><td rowspan="2">HAA</td><td rowspan="2">96</td><td rowspan="2">192</td><td rowspan="2">336</td><td rowspan="2">720</td><td rowspan="2">96</td><td rowspan="2">192</td><td rowspan="2">336</td><td rowspan="2">720</td></tr><tr><td><math><semantics><msub><mi>ℒ</mi> <mrow><mi>U</mi> <mo>⁢</mo> <mi>A</mi> <mo>⁢</mo> <mi>C</mi></mrow></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><ci>𝑈</ci> <ci>𝐴</ci> <ci>𝐶</ci></apply></apply></annotation-xml> <annotation>\mathcal{L}_{UAC}</annotation> <annotation>caligraphic_L start_POSTSUBSCRIPT italic_U italic_A italic_C end_POSTSUBSCRIPT</annotation></semantics></math></td><td><math><semantics><msub><mi>ℒ</mi> <mrow><mi>R</mi> <mo>⁢</mo> <mi>E</mi> <mo>⁢</mo> <mi>G</mi></mrow></msub> <annotation-xml><apply><csymbol>subscript</csymbol> <ci>ℒ</ci> <apply><ci>𝑅</ci> <ci>𝐸</ci> <ci>𝐺</ci></apply></apply></annotation-xml> <annotation>\mathcal{L}_{REG}</annotation> <annotation>caligraphic_L start_POSTSUBSCRIPT italic_R italic_E italic_G end_POSTSUBSCRIPT</annotation></semantics></math></td></tr><tr><td>-</td><td>-</td><td>-</td><td>-</td><td>-</td><td>0.176</td><td>0.225</td><td>0.281</td><td>0.358</td><td>0.175</td><td>0.218</td><td>0.263</td><td>0.332</td></tr><tr><td>✓</td><td>-</td><td>-</td><td>-</td><td>-</td><td>0.173</td><td>0.225</td><td>0.285</td><td>0.354</td><td>0.171</td><td>0.215</td><td>0.261</td><td>0.337</td></tr><tr><td>✓</td><td>✓</td><td>-</td><td>-</td><td>-</td><td>0.174</td><td>0.223</td><td>0.278</td><td>0.350</td><td>0.173</td><td>0.211</td><td>0.262</td><td>0.334</td></tr><tr><td>✓</td><td>✓</td><td>✓</td><td>-</td><td>-</td><td>0.168</td><td>0.220</td><td>0.277</td><td>0.343</td><td>0.170</td><td>0.215</td><td>0.265</td><td>0.324</td></tr><tr><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>-</td><td>0.167</td><td>0.221</td><td>0.276</td><td>0.341</td><td>0.169</td><td>0.207</td><td>0.262</td><td>0.320</td></tr><tr><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>✓</td><td>0.161</td><td>0.218</td><td>0.276</td><td>0.345</td><td>0.164</td><td>0.205</td><td>0.258</td><td>0.319</td></tr></tbody></table>

Table 8: Ablation study of the components of HCAN on the Weather dataset using iTransformer and Dlinear as backbones.

### Mean Absolute Error Loss

Traditional regularization methods, such as L1 or L2 penalties, primarily constrain model complexity to prevent overfitting. However, they may not effectively address the specific issue of over-smoothing in time series forecasting, where models fail to capture high-entropy features due to the limitations of Mean Squared Error (MSE) loss. HCAN introduces a novel approach by reformulating the forecasting task as a classification problem, utilizing cross-entropy loss to better capture high-entropy features. This hierarchical structure enables the model to learn multi-granularity features, enhancing its ability to represent complex patterns in the data.

We replace the MSE with the MAE loss for PatchTST and iTransformer and report the results in Table 7. The key difference lies in how each loss function influences the model’s predictions. HCAN incorporates a cross-entropy term to promote diverse and informative features, enhancing model’s ability to capture complex patterns. In contrast, MAE loss mainly focuses on reducing error but does not encourage feature diversity.

### High-entropy Loss

In addition, we compared HCAN with Ordinal Entropy loss [^45] in Table 7, which discretizes the continuous labels and treats each bin as a class to encourage higher-entropy feature spaces. We discretized the time series and replaced the MSE loss with Ordinal Entropy loss, conducting experiments on PatchTST and FITS. Clearly, our proposed HCAN achieves better performance, which further demonstrates the effectiveness of our approach.

## Appendix F Ablation Study

We conduct more ablation studies on the Weather dataset with iTransformer and DLinear further demonstrate the necessity of each model component, as shown in Table 8.

Each component is essential to address specific challenges in time series forecasting:

- Multi-Resolution Analysis: Captures patterns at different scales, essential for understanding both short-term fluctuations and long-term trends.
- Regularized Classification Loss: Mitigates over-confidence in predictions and enhances the model’s generalization.
- Hierarchical Structure: Facilitates learning at various levels of abstraction, improving the model’s capacity to handle complex temporal dependencies.

## Appendix G Hyperparameter Sensitivity

As shown in Table 9, we conduct hyperparameter sensitivity experiments on $(K_{c},K_{f})$ based on Informer and achieve optimal performance with the configuration (2, 4), demonstrating that HCAN is robust to these hyperparameters and maintains consistent generalizability across diverse datasets.

<table><thead><tr><th rowspan="2">Informer</th><th colspan="2">(2, 4)</th><th colspan="2">(2, 8)</th><th colspan="2">(2, 16)</th><th colspan="2">(2, 32)</th></tr><tr><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th><th>MSE</th><th>MAE</th></tr></thead><tbody><tr><th>ETTh1</th><td>0.703</td><td>0.617</td><td>0.791</td><td>0.668</td><td>0.783</td><td>0.665</td><td>0.834</td><td>0.700</td></tr><tr><th>ETTh2</th><td>1.563</td><td>1.011</td><td>1.568</td><td>1.015</td><td>1.844</td><td>1.135</td><td>1.774</td><td>1.109</td></tr><tr><th>ETTm1</th><td>0.592</td><td>0.544</td><td>0.596</td><td>0.628</td><td>0.628</td><td>0.559</td><td>0.614</td><td>0.579</td></tr><tr><th>ETTm2</th><td>0.337</td><td>0.445</td><td>0.369</td><td>0.459</td><td>0.400</td><td>0.488</td><td>0.419</td><td>0.505</td></tr></tbody></table>

Table 9: Hyperparameter sensitively experiments on $(K_{c},K_{f})$.

## Appendix H Exploring Multiple Hierarchical Levels

The cited works employ multiple hierarchical levels to capture time-series patterns at various granularities. Incorporating more than three levels may enhance our model’s ability to represent complex temporal structures. To explore this, we have conducted some experiments based on DLinear using both ETTh1 and ETTh2:

- H=1 ($K_{1}=1$) (Backone)
- H=2 ($K_{1}=1$, $K_{2}=2$)
- H=3 ($K_{1}=1$, $K_{2}=2$, $K_{3}=4$) (HCAN)
- H=4 ($K_{1}=1$, $K_{2}=2$, $K_{3}=4$, $K_{4}=8$)
- H=5 ($K_{1}=1$, $K_{2}=2$, $K_{3}=4$, $K_{4}=8$, $K_{5}=16$)

where H denotes the number of hierarchy levels, and $K_{i}$ represents the number of classes. We report the results in Table 10. The best performance is achieved with H=3 in HCAN. While incorporating more levels of granularity could provide benefits compared to H=1, our experiments suggest that three levels are sufficient to capture the necessary temporal dependencies without introducing excessive complexity.

<table><thead><tr><th rowspan="2">Number of hierarchies</th><th colspan="4">ETTh1</th><th colspan="4">ETTh2</th></tr><tr><th>96</th><th>192</th><th>336</th><th>720</th><th>96</th><th>192</th><th>336</th><th>720</th></tr></thead><tbody><tr><th>H=1</th><td>0.384</td><td>0.443</td><td>0.451</td><td>0.535</td><td>0.300</td><td>0.394</td><td>0.465</td><td>0.733</td></tr><tr><th>H=2</th><td>0.396</td><td>0.405</td><td>0.457</td><td>0.524</td><td>0.294</td><td>0.369</td><td>0.452</td><td>0.583</td></tr><tr><th>H=3</th><td>0.371</td><td>0.420</td><td>0.439</td><td>0.482</td><td>0.287</td><td>0.359</td><td>0.439</td><td>0.557</td></tr><tr><th>H=4</th><td>0.397</td><td>0.430</td><td>0.451</td><td>0.559</td><td>0.291</td><td>0.379</td><td>0.458</td><td>0.589</td></tr><tr><th>H=5</th><td>0.370</td><td>0.421</td><td>0.475</td><td>0.530</td><td>0.303</td><td>0.384</td><td>0.461</td><td>0.593</td></tr></tbody></table>

Table 10: Experiments on the hierarchical levels.

![[ETTh1_M_o96_Informer_norm.png|Refer to caption]]

(a) Informer+HCAN

![[ETTh1_S_o96_Informer_norm.png|Refer to caption]]

(a) Informer+HCAN.

## Appendix I Visualizations of Main Results

Multivariate Forecasting Showcases and Boundary Effects. To evaluate the prediction of different models, Figures 6 shows the comparison on Informer and Autoformer backbones on ETTh1 dataset. Similar to Figures 5, the backbones tend to produce over-smooth predictions, and our HCAN gives realistic performance especially for values at the class boundaries. This is attributed to the high entropy features as well as HCL mitigating the boundary effects.

Univariate Forecasting Showcases and Boundary Effects. As shown in the Figure 7, adding HCAN to the baseline models gives more accurate predictions. Compared with the benchmark model, HCAN can precisely capture the periods of the future horizon by introducing hierarchical classification. In addition, our prediction series is closer to the ground truth, which can be attributed to the introduction of hierarchical attention mechanisms that enrich feature representations, along with the HCL alleviating boundary effects.

| Model | Number of Parameters (MB) $\downarrow$ | Inference Runtime (s) $\downarrow$ |
| --- | --- | --- |
| Informer | 43.227 | 0.0935 |
| +HCAN | 46.273 | 0.1103 |
| Autoformer | 40.211 | 0.0474 |
| +HCAN | 43.257 | 0.0373 |
| PatchTST | 0.134 | 0.0101 |
| +HCAN | 3.180 | 0.0176 |
| SCINet | 0.092 | 0.1560 |
| +HCAN | 3.138 | 0.1604 |
| Dlinear | 0.071 | 0.0006 |
| +HCAN | 3.117 | 0.0015 |
| iTransformer | 3.210 | 0.0026 |
| +HCAN | 15.466 | 0.0030 |
| FITS | 0.013 | 0.0012 |
| +HCAN | 3.059 | 0.0027 |

Table 11: Comparison of computation complexity and inference runtime.

## Appendix J Complexity and Runtime Analysis

We compare the computational complexity and runtimes of the baseline methods with and without including our HCAN. The details are outlined in Table 11. Given the multi-module architecture of HCAN, it naturally exhibits a modest increase in the number of parameters and inference runtime for each model. This can be viewed as a necessary trade-off for the potential gains in forecasting accuracy and complexity handling that HCAN provides. Specifically, models integrated with HCAN, such as the Informer and Autoformer, show only slight increases in parameter size and runtime, which are offset by the enhanced capability to manage high-entropy feature representations in time series data, potentially leading to more robust and precise predictions. Additionally, the increase in inference time remains minimal, suggesting that the enhanced functionality of HCAN can be utilized with a reasonable impact on performance efficiency.

## Appendix K Algorithm

We provide HCAN pseudo-code based on Informer in Algorithms 1.

Algorithm 1 Overall Hierarchical Classification Auxiliary Network (HCAN) Procedure

Input past time series $X$; Input Length $L$; Predict Length $T$; Data dimension $D$; Hidden dimension $M$. Technically, we set $M=512$.

$\hat{Y}$, $\Delta\hat{y}_{f}$, $\Delta\hat{y}_{c}$, $e_{f}$, $e_{c}$

F = Backbone (X)

$\psi$ = Linear (F)

$\theta$ = Linear (F)

$\eta$ = Linear (F)

$\Delta\hat{y}_{f}$ = Linear ($\psi$) $\triangleright$ This is $UAC_{fine}$

$e_{f}$ = Linear ($\psi$) $\triangleright$ This is $UAC_{fine}$

$\Delta\hat{y}_{c}$ = Linear ($\theta$) $\triangleright$ This is $UAC_{coarse}$

$e_{c}$ = Linear ($\theta$) $\triangleright$ This is $UAC_{coarse}$

$A=softmax(\psi\otimes\theta)$ $\triangleright$ This is HAA

$\hat{Y}=Linear(Linear(A\otimes\eta)\oplus F)$ $\triangleright$ This is HAA

return $\hat{Y}$, $\Delta\hat{y}_{f}$, $\Delta\hat{y}_{c}$, $e_{f}$, $e_{c}$

## Appendix L Broader Impact

Real-world applications. HCAN addresses the crucial challenge of time series forecasting, which is a valuable and urgent demand in extensive applications. Our method achieves consistent state-of-the-art performance in six real-world applications: electricity, weather, exchange rate, illness, traffic, and space weather. Researchers in these fields stand to benefit significantly from the enhanced forecasting capabilities of HCAN. We believe that improved time series forecasting holds the potential to empower decision-making and proactively manage risks in a wide array of societal domains.

Academic research. HCAN draws inspiration from classical time series analysis and stochastic process theory, contributing to the field by introducing a novel framework with the assistance of hierarchical classification. The innovative HCAN architecture and associated methodologies present valuable additions to the repertoire of time series forecasting models.

Model Robustness. Extensive experimentation with HCAN reveals robust performance without exceptional failure cases. Notably, HCAN exhibits impressive results and sustained robustness in datasets lacking obvious periodicity, such as the Exchange dataset. The hierarchical classification structure of HCAN divides the time series into intervals for further prediction, alleviating the prediction difficulty. However, it’s essential to note that, like any model, HCAN may face challenges when dealing with random or poorly temporally coherent data, where predictability is inherently limited. Understanding these nuances is crucial for appropriately applying and interpreting HCAN’s outcomes.

Our work only focuses on the scientific problem, so there is no potential ethical risk.

[^1]: Cao, Y.; Wu, Z.; and Shen, C. 2017. Estimating depth from monocular images as classification using deep fully convolutional residual networks. *IEEE Transactions on Circuits and Systems for Video Technology*, 28(11): 3174–3182.

[^2]: Chen, H.; Rossi, R. A.; Mahadik, K.; Kim, S.; and Eldardiry, H. 2021. Graph deep factors for forecasting with applications to cloud resource allocation. In *Proceedings of the 27th ACM SIGKDD Conference on Knowledge Discovery & Data Mining*, 106–116.

[^3]: Chen, P.; ZHANG, Y.; Cheng, Y.; Shu, Y.; Wang, Y.; Wen, Q.; Yang, B.; and Guo, C. 2024. Pathformer: Multi-scale Transformers with Adaptive Pathways for Time Series Forecasting. In *The Twelfth International Conference on Learning Representations*.

[^4]: Du, D.; Su, B.; and Wei, Z. 2023. Preformer: predictive transformer with multi-scale segment-wise correlations for long-term time series forecasting. In *ICASSP 2023-2023 IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)*, 1–5. IEEE.

[^5]: Eldele, E.; Ragab, M.; Chen, Z.; Wu, M.; and Li, X. 2024. TSLANet: Rethinking Transformers for Time Series Representation Learning. In *International Conference on Machine Learning*.

[^6]: Fu, H.; Gong, M.; Wang, C.; Batmanghelich, K.; and Tao, D. 2018. Deep ordinal regression network for monocular depth estimation. In *Proceedings of the IEEE conference on computer vision and pattern recognition*, 2002–2011.

[^7]: Gu, K.; Yang, L.; and Yao, A. 2021. Dive deeper into integral pose regression. In *International Conference on Learning Representations*.

[^8]: Guo, Q.; Yuan, P.; Huang, X.; and Ye, Y. 2024. Consistency-constrained RGB-T crowd counting via mutual information maximization. *Complex & Intelligent Systems*, 1–22.

[^9]: Han, Z.; Zhang, C.; Fu, H.; and Zhou, J. T. 2022. Trusted multi-view classification with dynamic evidential fusion. *IEEE transactions on pattern analysis and machine intelligence*, 45(2): 2551–2566.

[^10]: Hou, M.; Xu, C.; Li, Z.; Liu, Y.; Liu, W.; Chen, E.; and Bian, J. 2022. Multi-Granularity Residual Learning with Confidence Estimation for Time Series Prediction. In *Proceedings of the ACM Web Conference 2022*, 112–121.

[^11]: Kingma, D. P.; and Ba, J. 2014. Adam: A method for stochastic optimization. *arXiv preprint arXiv:1412.6980*.

[^12]: Lai, G.; Chang, W.-C.; Yang, Y.; and Liu, H. 2018. Modeling long-and short-term temporal patterns with deep neural networks. In *The 41st international ACM SIGIR conference on research & development in information retrieval*, 95–104.

[^13]: Lam, R.; Sanchez-Gonzalez, A.; Willson, M.; Wirnsberger, P.; Fortunato, M.; Pritzel, A.; Ravuri, S.; Ewalds, T.; Alet, F.; Eaton-Rosen, Z.; et al. 2022. GraphCast: Learning skillful medium-range global weather forecasting. *arXiv preprint arXiv:2212.12794*.

[^14]: Li, Y.; Xu, J.; and Anastasiu, D. C. 2023. An extreme-adaptive time series prediction model based on probability-enhanced lstm neural networks. In *Proceedings of the AAAI Conference on Artificial Intelligence*, volume 37, 8684–8691.

[^15]: Liu, M.; Zeng, A.; Chen, M.; Xu, Z.; Lai, Q.; Ma, L.; and Xu, Q. 2022a. Scinet: Time series modeling and forecasting with sample convolution and interaction. *Advances in Neural Information Processing Systems*, 35: 5816–5828.

[^16]: Liu, N.; Zhang, F.; and Duan, F. 2020. Facial age estimation using a multi-task network combining classification and regression. *IEEE Access*, 8: 92441–92451.

[^17]: Liu, S.; Yu, H.; Liao, C.; Li, J.; Lin, W.; Liu, A. X.; and Dustdar, S. 2022b. Pyraformer: Low-Complexity Pyramidal Attention for Long-Range Time Series Modeling and Forecasting. In *International Conference on Learning Representations*.

[^18]: Liu, Y.; Hu, T.; Zhang, H.; Wu, H.; Wang, S.; Ma, L.; and Long, M. 2023. iTransformer: Inverted Transformers Are Effective for Time Series Forecasting. In *The Twelfth International Conference on Learning Representations*.

[^19]: Moon, J.; Kim, J.; Shin, Y.; and Hwang, S. 2020. Confidence-aware learning for deep neural networks. In *international conference on machine learning*, 7034–7044. PMLR.

[^20]: Ni, Z.; Yu, H.; Liu, S.; Li, J.; and Lin, W. 2024. Basisformer: Attention-based time series forecasting with learnable and interpretable basis. *Advances in Neural Information Processing Systems*, 36.

[^21]: Nie, Y.; Nguyen, N. H.; Sinthong, P.; and Kalagnanam, J. 2022. A Time Series is Worth 64 Words: Long-term Forecasting with Transformers. In *The Eleventh International Conference on Learning Representations*.

[^22]: Paszke, A.; Gross, S.; Massa, F.; Lerer, A.; Bradbury, J.; Chanan, G.; Killeen, T.; Lin, Z.; Gimelshein, N.; Antiga, L.; et al. 2019. Pytorch: An imperative style, high-performance deep learning library. *Advances in neural information processing systems*, 32.

[^23]: Pintea, S. L.; Lin, Y.; Dijkstra, J.; and van Gemert, J. C. 2023. A step towards understanding why classification helps regression. In *Proceedings of the IEEE/CVF International Conference on Computer Vision*, 19972–19981.

[^24]: Qiu, X.; Hu, J.; Zhou, L.; Wu, X.; Du, J.; Zhang, B.; Guo, C.; Zhou, A.; Jensen, C. S.; Sheng, Z.; et al. 2024. Tfb: Towards comprehensive and fair benchmarking of time series forecasting methods. *arXiv preprint arXiv:2403.20150*.

[^25]: Rabanser, S.; Januschowski, T.; Flunkert, V.; Salinas, D.; and Gasthaus, J. 2020. The effectiveness of discretization in forecasting: An empirical study on neural time series models. *arXiv preprint arXiv:2005.10111*.

[^26]: Rothe, R.; Timofte, R.; and Van Gool, L. 2015. Dex: Deep expectation of apparent age from a single image. In *Proceedings of the IEEE international conference on computer vision workshops*, 10–15.

[^27]: Shabani, M. A.; Abdi, A. H.; Meng, L.; and Sylvain, T. 2023. Scaleformer: Iterative Multi-scale Refining Transformers for Time Series Forecasting. In *The Eleventh International Conference on Learning Representations*.

[^28]: Shah, J.; Siddiquee, M. M. R.; Su, Y.; Wu, T.; and Li, B. 2024. Ordinal Classification with Distance Regularization for Robust Brain Age Prediction. In *Proceedings of the IEEE/CVF Winter Conference on Applications of Computer Vision*, 7882–7891.

[^29]: Shao, Z.; Wang, F.; Xu, Y.; Wei, W.; Yu, C.; Zhang, Z.; Yao, D.; Sun, T.; Jin, G.; Cao, X.; et al. 2024. Exploring progress in multivariate time series forecasting: Comprehensive benchmarking and heterogeneity analysis. *IEEE Transactions on Knowledge and Data Engineering*.

[^30]: Sun, Y.; Xie, Z.; Chen, Y.; Huang, X.; and Hu, Q. 2021. Solar Wind Speed Prediction With Two-Dimensional Attention Mechanism. *Space Weather*, 19(7): e2020SW002707.

[^31]: Van Amersfoort, J.; Smith, L.; Teh, Y. W.; and Gal, Y. 2020. Uncertainty estimation using a single deep deterministic neural network. In *International conference on machine learning*, 9690–9700. PMLR.

[^32]: Wang, J.; and Gao, Y. 2023. Generalized Mixture Model for Extreme Events Forecasting in Time Series Data. *arXiv preprint arXiv:2310.07435*.

[^33]: Wang, S.; Wu, H.; Shi, X.; Hu, T.; Luo, H.; Ma, L.; Zhang, J. Y.; and ZHOU, J. 2024a. TimeMixer: Decomposable Multiscale Mixing for Time Series Forecasting. In *The Twelfth International Conference on Learning Representations*.

[^34]: Wang, X.; Zhou, T.; Wen, Q.; Gao, J.; Ding, B.; and Jin, R. 2024b. CARD: Channel aligned robust blend transformer for time series forecasting. In *The Twelfth International Conference on Learning Representations*.

[^35]: Wen, Q.; Zhou, T.; Zhang, C.; Chen, W.; Ma, Z.; Yan, J.; and Sun, L. 2023. Transformers in Time Series: A Survey. In *Proceedings of the Thirty-Second International Joint Conference on Artificial Intelligence, IJCAI 2023, 19th-25th August 2023, Macao, SAR, China*, 6778–6786. ijcai.org.

[^36]: Wilson, T.; McDonald, A.; Galib, A. H.; Tan, P.-N.; and Luo, L. 2022. Beyond Point Prediction: Capturing Zero-Inflated & Heavy-Tailed Spatiotemporal Data with Deep Extreme Mixture Models. In *Proceedings of the 28th ACM SIGKDD Conference on Knowledge Discovery and Data Mining*, 2020–2028.

[^37]: Wu, H.; Hu, T.; Liu, Y.; Zhou, H.; Wang, J.; and Long, M. 2023. TimesNet: Temporal 2D-Variation Modeling for General Time Series Analysis. In *The Eleventh International Conference on Learning Representations*.

[^38]: Wu, H.; Xu, J.; Wang, J.; and Long, M. 2021. Autoformer: Decomposition transformers with auto-correlation for long-term series forecasting. *Advances in Neural Information Processing Systems*, 34: 22419–22430.

[^39]: Wu, X.; Qiu, X.; Li, Z.; Wang, Y.; Hu, J.; Guo, C.; Xiong, H.; and Yang, B. 2024. CATCH: Channel-Aware multivariate Time Series Anomaly Detection via Frequency Patching. *arXiv preprint arXiv:2410.12261*.

[^40]: Xiong, H.; and Yao, A. 2022. Discrete-constrained regression for local counting models. In *European Conference on Computer Vision*, 621–636. Springer.

[^41]: Xu, Z.; Zeng, A.; and Xu, Q. 2024. FITS: Modeling Time Series with $10k$ Parameters. In *The Twelfth International Conference on Learning Representations*.

[^42]: Yu, C.; Wang, F.; Shao, Z.; Sun, T.; Wu, L.; and Xu, Y. 2023. Dsformer: A double sampling transformer for multivariate time series long-term prediction. In *Proceedings of the 32nd ACM international conference on information and knowledge management*, 3062–3072.

[^43]: Yu, X.; Rao, Y.; Zhao, W.; Lu, J.; and Zhou, J. 2021. Group-aware contrastive regression for action quality assessment. In *Proceedings of the IEEE/CVF international conference on computer vision*, 7919–7928.

[^44]: Zeng, A.; Chen, M.; Zhang, L.; and Xu, Q. 2023. Are transformers effective for time series forecasting? In *Proceedings of the AAAI conference on artificial intelligence*, volume 37, 11121–11128.

[^45]: Zhang, S.; Yang, L.; Mi, M. B.; Zheng, X.; and Yao, A. 2023. Improving Deep Regression with Ordinal Entropy. In *The Eleventh International Conference on Learning Representations*.

[^46]: Zhou, H.; Zhang, S.; Peng, J.; Zhang, S.; Li, J.; Xiong, H.; and Zhang, W. 2021. Informer: Beyond efficient transformer for long sequence time-series forecasting. In *Proceedings of the AAAI conference on artificial intelligence*, volume 35, 11106–11115.

[^47]: Zhou, T.; Ma, Z.; Wen, Q.; Wang, X.; Sun, L.; and Jin, R. 2022. Fedformer: Frequency enhanced decomposed transformer for long-term series forecasting. In *International Conference on Machine Learning*, 27268–27286. PMLR.