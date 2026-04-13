---
author:
- null
- '[[Asankhaya Sharma]]'
created: 2026-04-06
created_at: 2026-04-06
description: A Blog post by Asankhaya Sharma on Hugging Face
source_type: web
status: inbox
tags:
- null
- clippings
title: 'Adaptive Classifier: Dynamic Text Classification with Continuous Learning'
source_url: https://huggingface.co/blog/codelion/adaptive-classifier
published_at: 2025-06-20
related_concepts: []
topics:
  - llm-theory
  - 大语言模型理论
---

## Abstract

We introduce **Adaptive Classifier**, a novel text classification system that enables dynamic class addition and continuous learning without catastrophic forgetting. Our approach combines prototype-based memory systems with neural adaptation layers and introduces **strategic classification** - a game-theoretic framework for robust classification under adversarial manipulation. The system seamlessly integrates with the HuggingFace ecosystem and demonstrates strong empirical results across multiple applications including hallucination detection, LLM configuration optimization, and intelligent model routing. On the adversarial SST-2 dataset, our strategic classifier achieves 22.22% improvement over baseline methods when facing manipulated inputs while maintaining performance on clean data.

## Introduction

Traditional text classifiers suffer from a fundamental limitation: they require retraining from scratch when new classes emerge, leading to catastrophic forgetting of previously learned knowledge. This limitation becomes particularly problematic in production environments where new categories of text continuously emerge, and where adversarial users may attempt to manipulate classifications through strategic input modification.

Consider a customer support system that initially classifies tickets into "technical," "billing," and "general" categories. As the business evolves, new categories like "privacy," "compliance," and "integration" emerge. Traditional approaches would require collecting new training data for all classes and retraining the entire model, risking degradation on existing categories. Furthermore, if users discover they can game the system by modifying their language patterns, the classifier's reliability diminishes.

The Adaptive Classifier addresses these challenges through four key innovations:

1. **Dynamic Class Addition**: New classes can be added seamlessly without retraining existing knowledge
2. **Prototype-Based Memory**: Efficient similarity-based classification using learned class prototypes
3. **Neural Adaptation**: Continuous refinement of decision boundaries through lightweight neural layers
4. **Strategic Classification**: Game-theoretic robustness against adversarial manipulation

## Technical Architecture

### Core Design Principles

The Adaptive Classifier operates on the principle that effective classification can be decomposed into two complementary components: **memory-based retrieval** and **neural boundary refinement**. This dual approach enables both rapid adaptation to new examples and sophisticated decision boundary learning.

```python
from adaptive_classifier import AdaptiveClassifier

# Initialize with any transformer model
classifier = AdaptiveClassifier("bert-base-uncased")

# Add examples dynamically
texts = ["Great product!", "Terrible service", "API returning errors"]
labels = ["positive", "negative", "technical"]
classifier.add_examples(texts, labels)

# Immediate classification capability
predictions = classifier.predict("This is amazing!")
# Returns: [('positive', 0.87), ('negative', 0.08), ('technical', 0.05)]
```

[![[54qa0XHNxaf9puWvbTSab.png|image/png]]](https://cdn-uploads.huggingface.co/production/uploads/62f32eab52ad88c930bb3f3b/54qa0XHNxaf9puWvbTSab.png)

### Prototype Memory System

At the heart of our approach lies a sophisticated memory system that maintains **class prototypes** - learned representations that capture the essential characteristics of each class. Unlike traditional k-nearest neighbors approaches, our system uses FAISS-optimized similarity search with dynamic prototype updates.

**Mathematical Foundation**: For each class c, we maintain a prototype computed as the exponentially weighted moving average of class examples:

$$
p_{c}^{\left(\right. t + 1 \left.\right)} = \alpha \cdot p_{c}^{\left(\right. t \left.\right)} + \left(\right. 1 - \alpha \left.\right) \cdot \frac{1}{\mid S_{c} \mid} \underset{x \in S_{c}}{\sum} \phi \left(\right. x \left.\right)
$$

where φ(x) represents the transformer embedding of text x, and S\_c is the set of new examples for class c.

**Implementation Details**: The memory system employs several optimizations:

- **Selective Example Retention**: We maintain up to k representative examples per class, selected through k-means clustering to preserve diversity
- **Incremental Index Updates**: FAISS indices are rebuilt only when accumulated updates exceed a threshold, balancing accuracy with computational efficiency
- **Normalized Embeddings**: All embeddings are L2-normalized to enable meaningful cosine similarity comparisons

```python
class PrototypeMemory:
    def add_example(self, example: Example, label: str):
        # Add to examples and update prototype
        self.examples[label].append(example)
        self._update_prototype(label)
        
        # Conditional index rebuild for efficiency
        if self.updates_since_rebuild >= self.update_frequency:
            self._rebuild_index()
    
    def get_nearest_prototypes(self, query_embedding: torch.Tensor, k: int = 5):
        # FAISS-optimized similarity search
        distances, indices = self.index.search(query_embedding.numpy(), k)
        similarities = np.exp(-distances[0])  # Convert to similarities
        return [(self.index_to_label[idx], sim) for idx, sim in zip(indices[0], similarities)]
```

### Neural Adaptation Layer

While prototype-based classification provides excellent few-shot learning capabilities, complex decision boundaries often require more sophisticated modeling. Our neural adaptation layer addresses this need through a lightweight feedforward network that learns to refine classification decisions.

**Architecture**: The adaptation layer consists of:

- **Input Layer**: Transformer embeddings (typically 768 or 1024 dimensions)
- **Hidden Layer**: Reduced dimensionality with ReLU activation and dropout
- **Output Layer**: Softmax over current class set with dynamic resizing capability

**Catastrophic Forgetting Prevention**: When new classes are added, we employ Elastic Weight Consolidation (EWC) to preserve knowledge of existing classes:

$$
\mathcal{L}_{t o t a l} = \mathcal{L}_{t a s k} + \frac{\lambda}{2} \underset{i}{\sum} F_{i} \left(\right. \theta_{i} - \theta_{i}^{*} \left.\right)^{2}
$$

where F\_i represents the Fisher Information Matrix diagonal for parameter i, and θ\_i\* are the optimal parameters from previous tasks.

### Strategic Classification Framework

A critical innovation in our system is the introduction of **strategic classification** - a game-theoretic approach to robust classification under adversarial conditions. This addresses the reality that users may attempt to manipulate classifications by strategically modifying their inputs.

**Threat Model**: We model strategic users who can modify their inputs x to x' at cost c(x, x'), seeking to maximize their utility:

$$
\underset{x^{'}}{max ⁡} f \left(\right. x^{'} \left.\right) - c \left(\right. x , x^{'} \left.\right)
$$

where f(x') represents the classifier's confidence for the desired class.

**Cost Functions**: We implement several cost function families:

1. **Linear Costs**:

$$
c \left(\right. x , y \left.\right) = \langle \alpha , \left(\right. y - x \left.\right)_{+} \rangle
$$

where α represents per-feature modification costs

1. **Separable Costs**:

$$
c \left(\right. x , y \left.\right) = max ⁡ \left{\right. 0 , c_{2} \left(\right. y \left.\right) - c_{1} \left(\right. x \left.\right) \left.\right}
$$

enabling more complex strategic behaviors

**Dual Prediction System**: Our strategic classifier operates in multiple modes:

- **Regular Mode**: Standard classification using prototype and neural predictions
- **Strategic Mode**: Predicts where a strategic agent would move their input
- **Robust Mode**: Anti-manipulation prediction that accounts for potential gaming
- **Dual Mode**: Blends regular and strategic predictions for balanced performance

```python
# Enable strategic classification
config = {
    'enable_strategic_mode': True,
    'cost_function_type': 'linear',
    'cost_coefficients': {'sentiment_words': 0.5, 'length_change': 0.1},
    'strategic_blend_regular_weight': 0.6,
    'strategic_blend_strategic_weight': 0.4
}

classifier = AdaptiveClassifier("bert-base-uncased", config=config)

# Multiple prediction modes
dual_predictions = classifier.predict(text)           # Blended approach
strategic_predictions = classifier.predict_strategic(text)  # Assumes manipulation
robust_predictions = classifier.predict_robust(text)       # Anti-manipulation
```

## Empirical Evaluation

### Strategic Classification Performance

We evaluated our strategic classification framework on the AI-Secure/adv\_glue dataset's adversarial SST-2 subset, which contains sentiment classification examples specifically designed to test robustness against strategic manipulation.

**Experimental Setup**:

- **Dataset**: 148 adversarial examples split 70%/30% train/test
- **Model**: answerdotai/ModernBERT-base with linear cost function
- **Cost Strategy**: Balanced approach with 50% of embedding dimensions manipulable at cost 0.3

**Key Results**:

| Prediction Mode | Accuracy | F1-Score | Performance vs Baseline |
| --- | --- | --- | --- |
| Regular Classifier | 80.00% | 80.00% | Baseline |
| **Strategic (Dual)** | **82.22%** | **82.12%** | **+2.22% improvement** |
| Strategic (Pure) | 82.22% | 82.12% | +2.22% improvement |
| Robust Mode | 80.00% | 79.58% | Consistent performance |

**Robustness Under Attack**: Perhaps more importantly, we evaluated performance when inputs are strategically manipulated:

| Scenario | Regular Classifier | Strategic Classifier | Advantage |
| --- | --- | --- | --- |
| **Clean Data** | 80.00% | 82.22% | +2.22% |
| **Manipulated Data** | 60.00% | 82.22% | +22.22% |
| **Performance Drop** | \-20.00% | 0.00% | +20.00% robustness |

The strategic classifier demonstrates **perfect robustness** - maintaining identical performance regardless of input manipulation, while achieving improved performance on clean data.

### Application: Hallucination Detection

We developed a specialized hallucination detector for Retrieval-Augmented Generation (RAG) systems, addressing the critical problem of LLMs generating content not supported by provided context.

**Dataset**: RAGTruth benchmark across multiple task types **Classes**: `HALLUCINATED` vs `NOT_HALLUCINATED`

**Performance Results**:

| Task Type | Precision | Recall | F1 Score | Key Insights |
| --- | --- | --- | --- | --- |
| QA | 35.50% | 45.11% | 39.74% | Moderate precision, good recall |
| Summarization | 22.18% | 96.91% | 36.09% | Excellent at catching hallucinations |
| Data-to-Text | 65.00% | 100.0% | 78.79% | Strong performance on structured tasks |
| **Overall** | **40.89%** | **80.68%** | **51.54%** | High recall for safety-critical applications |

The high recall (80.68%) makes this system particularly valuable for safety-critical applications where false negatives (missed hallucinations) are more costly than false positives.

```python
from adaptive_classifier import AdaptiveClassifier

# Load pre-trained hallucination detector
detector = AdaptiveClassifier.from_pretrained("adaptive-classifier/llm-hallucination-detector")

# Evaluate RAG output
context = "France is in Western Europe. Capital: Paris. Population: 67 million."
query = "What is France's capital and population?"
response = "Paris is the capital. Population is 70 million."

input_text = f"Context: {context}\nQuestion: {query}\nAnswer: {response}"
prediction = detector.predict(input_text)

if prediction[0][0] == 'HALLUCINATED' and prediction[0][1] > 0.6:
    print("⚠️  Warning: Response may contain hallucinations")
```

### Application: LLM Configuration Optimization

Traditional LLM deployment requires manual tuning of hyperparameters like temperature for different query types. Our adaptive classifier automates this process by learning to predict optimal temperature ranges.

**Temperature Classes**:

- **DETERMINISTIC** (0.0-0.1): Factual queries requiring precision
- **FOCUSED** (0.2-0.5): Technical responses with slight flexibility
- **BALANCED** (0.6-1.0): Natural conversational responses
- **CREATIVE** (1.1-1.5): Varied and imaginative outputs
- **EXPERIMENTAL** (1.6-2.0): Maximum variability for brainstorming

**Evaluation on LLM Arena Dataset**:

- **Success Rate**: 69.8% in finding optimal configurations
- **Consistency**: Average similarity score of 0.64 across configurations
- **Distribution**: Balanced usage across temperature classes based on query characteristics

This automation eliminates the need for manual parameter tuning while ensuring optimal response quality for different query types.

[![[rdiSYxX1mtyu9q_2jM2De.png|image/png]]](https://cdn-uploads.huggingface.co/production/uploads/62f32eab52ad88c930bb3f3b/rdiSYxX1mtyu9q_2jM2De.png)

### Application: Intelligent LLM Routing

The adaptive classifier enables cost-efficient LLM deployment by intelligently routing queries between high-capability (expensive) and standard-capability (economical) models.

**Routing Classes**:

- **HIGH**: Complex queries requiring advanced reasoning, code generation, multi-step problems
- **LOW**: Straightforward queries, factual questions, basic formatting tasks

**Arena-Hard Evaluation Results**:

| Metric | Without Adaptation | With Adaptation | Impact |
| --- | --- | --- | --- |
| High Model Routes | 113 (22.6%) | 98 (19.6%) | 13% reduction |
| Low Model Routes | 387 (77.4%) | 402 (80.4%) | 4% increase |
| Cost Savings | 25.60% | 32.40% | **26.6% improvement** |
| Overall Success Rate | 22.00% | 22.00% | Maintained quality |

**Key Insights**:

- **Cost Efficiency**: 26.6% improvement in cost savings through better resource allocation
- **Quality Preservation**: No degradation in overall success rate
- **Learning Effectiveness**: Continuous adaptation improved low-model success rate from 16.54% to 20.15%

## Implementation and Integration

### HuggingFace Ecosystem Integration

The Adaptive Classifier seamlessly integrates with the HuggingFace ecosystem, supporting model sharing, versioning, and collaboration:

```python
# Train and save to Hub
classifier = AdaptiveClassifier("bert-base-uncased")
classifier.add_examples(texts, labels)
classifier.push_to_hub("adaptive-classifier/my-custom-classifier")

# Load from Hub
classifier = AdaptiveClassifier.from_pretrained("adaptive-classifier/my-custom-classifier")

# Continue training
classifier.add_examples(new_texts, new_labels)
```

### Production Deployment Considerations

**Memory Management**: The system implements intelligent memory management with configurable limits:

- Maximum examples per class (default: 1000)
- Prototype update frequency (default: every 100 examples)
- Representative example selection via k-means clustering

**Scalability**: FAISS-based similarity search enables efficient operation with large class sets:

- Logarithmic search complexity
- GPU acceleration support
- Distributed deployment compatibility

**Monitoring and Observability**:

```python
# Get comprehensive statistics
stats = classifier.get_memory_stats()
print(f"Classes: {stats['num_classes']}")
print(f"Total examples: {stats['total_examples']}")
print(f"Memory usage: {stats['memory_usage']}")

# Performance monitoring
evaluation_stats = classifier.get_example_statistics()
print(f"Training steps: {evaluation_stats['train_steps']}")
print(f"Model parameters: {evaluation_stats['model_params']}")
```

## Technical Innovations and Contributions

### 1\. Unified Memory-Neural Architecture

Our key insight is that effective adaptive classification requires both **fast similarity-based retrieval** and **sophisticated boundary learning**. The prototype memory system enables immediate classification of new examples, while the neural adaptation layer learns complex decision boundaries over time.

This dual approach outperforms pure memory-based systems (limited expressiveness) and pure neural approaches (catastrophic forgetting) by leveraging the strengths of both paradigms.

### 2\. Strategic Classification Framework

We introduce the first comprehensive framework for strategic-aware text classification, addressing a critical gap in robustness research. Our approach:

- **Models Strategic Behavior**: Uses game-theoretic cost functions to predict adversarial modifications
- **Provides Multiple Defense Modes**: Regular, strategic, robust, and dual prediction modes
- **Achieves Dual Benefits**: Improved performance on both clean and manipulated data

### 3\. Elastic Weight Consolidation for Text Classification

While EWC has been applied to computer vision, our adaptation to text classification with dynamic class sets represents a novel contribution. We demonstrate effective mitigation of catastrophic forgetting when classes are added incrementally.

### 4\. Production-Ready Continuous Learning

Unlike research prototypes, our system is designed for production deployment with:

- Efficient memory management and indexing
- Deterministic behavior with configurable randomness
- Comprehensive monitoring and observability
- Seamless HuggingFace integration

## Related Work and Positioning

**Continual Learning**: Our work builds on continual learning research but focuses specifically on the text classification setting with practical deployment constraints. Unlike approaches that require task boundaries, our system handles seamless class addition.

**Few-Shot Learning**: While few-shot learning methods exist, they typically require pre-defined class sets. Our approach enables true zero-shot addition of previously unseen classes.

**Adversarial Robustness**: Strategic classification extends beyond traditional adversarial robustness by modeling economically motivated attackers rather than worst-case perturbations.

**Prototype Networks**: We extend prototype networks with sophisticated memory management, neural refinement, and strategic considerations.

## Limitations and Future Work

**Current Limitations**:

1. **Computational Overhead**: Strategic prediction modes require additional computation
2. **Memory Growth**: Linear growth in memory usage with number of classes and examples
3. **Domain Shift**: Performance may degrade with significant domain changes

**Future Research Directions**:

1. **Hierarchical Class Organization**: Learning hierarchical relationships between classes
2. **Multi-Modal Extensions**: Extending to vision-language and other modalities
3. **Federated Learning**: Distributed adaptation across multiple clients
4. **Advanced Strategic Models**: More sophisticated game-theoretic frameworks

## Conclusion

The Adaptive Classifier represents a significant advancement in practical text classification, addressing real-world challenges of dynamic class addition, continuous learning, and adversarial robustness. Our comprehensive evaluation demonstrates substantial improvements across multiple applications:

- **22.22% robustness improvement** against adversarial manipulation
- **26.6% cost optimization** in LLM routing applications
- **80.68% recall** in safety-critical hallucination detection
- **69.8% success rate** in automated LLM configuration

The system's seamless integration with the HuggingFace ecosystem, combined with production-ready design considerations, makes it immediately applicable to real-world deployments. We hope this work inspires further research into adaptive, robust, and practical machine learning systems.

## Code Availability

The complete implementation is open source and available at:

- **GitHub**: [https://github.com/codelion/adaptive-classifier](https://github.com/codelion/adaptive-classifier)
- **PyPI**: `pip install adaptive-classifier`
- **HuggingFace Models**: [https://huggingface.co/adaptive-classifier](https://huggingface.co/adaptive-classifier)

## Citation

```
@software{adaptive_classifier_2025,
  title = {Adaptive Classifier: Dynamic Text Classification with Continuous Learning},
  author = {Sharma, Asankhaya},
  year = {2025},
  publisher = {GitHub},
  url = {https://github.com/codelion/adaptive-classifier},
  note = {Open source implementation with HuggingFace integration}
}
```

## Acknowledgments

We thank the HuggingFace team for their excellent transformer ecosystem, the creators of the AI-Secure/adv\_glue and RAGTruth datasets, and the open-source community for their valuable feedback and contributions.

More from this author

## [Scaling Pedagogical Pre-training: From Optimal Mixing to 10 Billion Tokens](https://huggingface.co/blog/codelion/scaling-pedagogical-pretraining-10-billion-tokens)

codelion

5

March 6, 2026

## [Reverse Engineering a $500M Mystery: From HashHop to Memory-Augmented Language Models](https://huggingface.co/blog/codelion/reverse-engineering-magic-hashhop)

codelion

10

January 23, 2026