---
source_type: web
title: "PyTorch documentation"
author:
  - 
  - "[[PyTorch Contributors]]"
created_at: 2026-04-06
status: inbox
created: 2026-04-06
description: "PyTorch Documentation. Explore PyTorch, an open-source machine learning library that accelerates the path from research prototyping to production deployment."
tags:
  - 
  - "clippings"
source_url: "https://docs.pytorch.org/docs/stable/index.html"
published_at: 2023-01-01
related_concepts: []
topics:
  - deep-learning
  - 深度学习理论
---

## PyTorch documentation

PyTorch is an optimized tensor library for deep learning using GPUs and CPUs.

Features described in this documentation are classified by release status:

**Stable (API-Stable):** These features will be maintained long-term and there should generally be no major performance limitations or gaps in documentation. We also expect to maintain backwards compatibility (although breaking changes can happen and notice will be given one release ahead of time).

**Unstable (API-Unstable):** Encompasses all features that are under active development where APIs may change based on user feedback, requisite performance improvements or because coverage across operators is not yet complete. The APIs and performance characteristics of these features may change.

- [Install PyTorch](https://pytorch.org/get-started/locally/)
- [User Guide](https://docs.pytorch.org/docs/stable/user_guide/index.html)
	- [Pytorch Overview](https://docs.pytorch.org/tutorials/beginner/deep_learning_60min_blitz.html)
		- [Get Started](https://pytorch.org/get-started/locally/)
		- [Learn the Basics](https://docs.pytorch.org/tutorials/beginner/basics/intro.html)
		- [PyTorch Main Components](https://docs.pytorch.org/docs/stable/user_guide/pytorch_main_components.html)
		- [Torch.compile](https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/torch.compiler.html)
		- [Torch.export](https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/export.html)
		- [Developer Notes](https://docs.pytorch.org/docs/stable/notes.html)
		- [Accelerator Integration](https://docs.pytorch.org/docs/stable/accelerator/index.html)
- [Reference API](https://docs.pytorch.org/docs/stable/pytorch-api.html)
	- [C++](https://docs.pytorch.org/cppdocs/)
		- [torch](https://docs.pytorch.org/docs/stable/torch.html)
		- [torch.nn](https://docs.pytorch.org/docs/stable/nn.html)
		- [torch.nn.functional](https://docs.pytorch.org/docs/stable/nn.functional.html)
		- [torch.Tensor](https://docs.pytorch.org/docs/stable/tensors.html)
		- [Tensor Attributes](https://docs.pytorch.org/docs/stable/tensor_attributes.html)
		- [Tensor Views](https://docs.pytorch.org/docs/stable/tensor_view.html)
		- [torch.amp](https://docs.pytorch.org/docs/stable/amp.html)
		- [torch.autograd](https://docs.pytorch.org/docs/stable/autograd.html)
		- [torch.library](https://docs.pytorch.org/docs/stable/library.html)
		- [torch.accelerator](https://docs.pytorch.org/docs/stable/accelerator.html)
		- [torch.cpu](https://docs.pytorch.org/docs/stable/cpu.html)
		- [torch.cuda](https://docs.pytorch.org/docs/stable/cuda.html)
		- [torch.cuda.memory](https://docs.pytorch.org/docs/stable/torch_cuda_memory.html)
		- [torch.mps](https://docs.pytorch.org/docs/stable/mps.html)
		- [torch.xpu](https://docs.pytorch.org/docs/stable/xpu.html)
		- [torch.mtia](https://docs.pytorch.org/docs/stable/mtia.html)
		- [torch.mtia.memory](https://docs.pytorch.org/docs/stable/mtia.memory.html)
		- [torch.mtia.mtia\_graph](https://docs.pytorch.org/docs/stable/mtia.mtia_graph.html)
		- [Meta device](https://docs.pytorch.org/docs/stable/meta.html)
		- [torch.backends](https://docs.pytorch.org/docs/stable/backends.html)
		- [torch.export](https://docs.pytorch.org/docs/stable/user_guide/torch_compiler/export.html)
		- [torch.distributed](https://docs.pytorch.org/docs/stable/distributed.html)
		- [torch.distributed.tensor](https://docs.pytorch.org/docs/stable/distributed.tensor.html)
		- [torch.distributed.algorithms.join](https://docs.pytorch.org/docs/stable/distributed.algorithms.join.html)
		- [torch.distributed.elastic](https://docs.pytorch.org/docs/stable/distributed.elastic.html)
		- [torch.distributed.fsdp](https://docs.pytorch.org/docs/stable/fsdp.html)
		- [torch.distributed.fsdp.fully\_shard](https://docs.pytorch.org/docs/stable/distributed.fsdp.fully_shard.html)
		- [torch.distributed.tensor.parallel](https://docs.pytorch.org/docs/stable/distributed.tensor.parallel.html)
		- [torch.distributed.optim](https://docs.pytorch.org/docs/stable/distributed.optim.html)
		- [torch.distributed.pipelining](https://docs.pytorch.org/docs/stable/distributed.pipelining.html)
		- [torch.distributed.\_symmetric\_memory](https://docs.pytorch.org/docs/stable/symmetric_memory.html)
		- [torch.distributed.checkpoint](https://docs.pytorch.org/docs/stable/distributed.checkpoint.html)
		- [torch.distributions](https://docs.pytorch.org/docs/stable/distributions.html)
		- [torch.compiler](https://docs.pytorch.org/docs/stable/torch.compiler_api.html)
		- [torch.fft](https://docs.pytorch.org/docs/stable/fft.html)
		- [torch.func](https://docs.pytorch.org/docs/stable/func.html)
		- [torch.futures](https://docs.pytorch.org/docs/stable/futures.html)
		- [torch.fx](https://docs.pytorch.org/docs/stable/fx.html)
		- [torch.fx.experimental](https://docs.pytorch.org/docs/stable/fx.experimental.html)
		- [torch.hub](https://docs.pytorch.org/docs/stable/hub.html)
		- [torch.linalg](https://docs.pytorch.org/docs/stable/linalg.html)
		- [torch.monitor](https://docs.pytorch.org/docs/stable/monitor.html)
		- [torch.signal](https://docs.pytorch.org/docs/stable/signal.html)
		- [torch.special](https://docs.pytorch.org/docs/stable/special.html)
		- [torch.overrides](https://docs.pytorch.org/docs/stable/torch.overrides.html)
		- [torch.nativert](https://docs.pytorch.org/docs/stable/nativert.html)
		- [torch.package](https://docs.pytorch.org/docs/stable/package.html)
		- [torch.profiler](https://docs.pytorch.org/docs/stable/profiler.html)
		- [torch.nn.init](https://docs.pytorch.org/docs/stable/nn.init.html)
		- [torch.nn.attention](https://docs.pytorch.org/docs/stable/nn.attention.html)
		- [torch.onnx](https://docs.pytorch.org/docs/stable/onnx.html)
		- [torch.optim](https://docs.pytorch.org/docs/stable/optim.html)
		- [Complex Numbers](https://docs.pytorch.org/docs/stable/complex_numbers.html)
		- [DDP Communication Hooks](https://docs.pytorch.org/docs/stable/ddp_comm_hooks.html)
		- [Quantization](https://docs.pytorch.org/docs/stable/quantization.html)
		- [Distributed RPC Framework](https://docs.pytorch.org/docs/stable/rpc.html)
		- [torch.random](https://docs.pytorch.org/docs/stable/random.html)
		- [torch.masked](https://docs.pytorch.org/docs/stable/masked.html)
		- [torch.nested](https://docs.pytorch.org/docs/stable/nested.html)
		- [torch.Size](https://docs.pytorch.org/docs/stable/size.html)
		- [torch.sparse](https://docs.pytorch.org/docs/stable/sparse.html)
		- [torch.Storage](https://docs.pytorch.org/docs/stable/storage.html)
		- [torch.testing](https://docs.pytorch.org/docs/stable/testing.html)
		- [torch.utils](https://docs.pytorch.org/docs/stable/utils.html)
		- [torch.utils.collect\_env](https://docs.pytorch.org/docs/stable/utils.html#module-torch.utils.collect_env)
		- [torch.utils.flop\_counter](https://docs.pytorch.org/docs/stable/utils.html#module-torch.utils.flop_counter)
		- [torch.utils.hipify.hipify\_python](https://docs.pytorch.org/docs/stable/utils.html#module-torch.utils.hipify.hipify_python)
		- [torch.utils.benchmark](https://docs.pytorch.org/docs/stable/benchmark_utils.html)
		- [torch.utils.checkpoint](https://docs.pytorch.org/docs/stable/checkpoint.html)
		- [torch.utils.cpp\_extension](https://docs.pytorch.org/docs/stable/cpp_extension.html)
		- [torch.utils.data](https://docs.pytorch.org/docs/stable/data.html)
		- [torch.utils.deterministic](https://docs.pytorch.org/docs/stable/deterministic.html)
		- [torch.utils.jit](https://docs.pytorch.org/docs/stable/jit_utils.html)
		- [torch.utils.dlpack](https://docs.pytorch.org/docs/stable/dlpack.html)
		- [torch.utils.mobile\_optimizer](https://docs.pytorch.org/docs/stable/mobile_optimizer.html)
		- [torch.utils.model\_zoo](https://docs.pytorch.org/docs/stable/model_zoo.html)
		- [torch.utils.tensorboard](https://docs.pytorch.org/docs/stable/tensorboard.html)
		- [torch.utils.module\_tracker](https://docs.pytorch.org/docs/stable/module_tracker.html)
		- [Type Info](https://docs.pytorch.org/docs/stable/type_info.html)
		- [Named Tensors](https://docs.pytorch.org/docs/stable/named_tensor.html)
		- [Named Tensors operator coverage](https://docs.pytorch.org/docs/stable/name_inference.html)
		- [torch.\_\_config\_\_](https://docs.pytorch.org/docs/stable/config_mod.html)
		- [torch.\_\_future\_\_](https://docs.pytorch.org/docs/stable/future_mod.html)
		- [torch.\_logging](https://docs.pytorch.org/docs/stable/logging.html)
		- [Torch Environment Variables](https://docs.pytorch.org/docs/stable/torch_environment_variables.html)
- [Developer Notes](https://docs.pytorch.org/docs/stable/notes.html)
	- [Automatic Mixed Precision examples](https://docs.pytorch.org/docs/stable/notes/amp_examples.html)
		- [Autograd mechanics](https://docs.pytorch.org/docs/stable/notes/autograd.html)
		- [Broadcasting semantics](https://docs.pytorch.org/docs/stable/notes/broadcasting.html)
		- [CPU threading and TorchScript inference](https://docs.pytorch.org/docs/stable/notes/cpu_threading_torchscript_inference.html)
		- [CUDA semantics](https://docs.pytorch.org/docs/stable/notes/cuda.html)
		- [PyTorch Custom Operators Landing Page](https://docs.pytorch.org/docs/stable/notes/custom_operators.html)
		- [Distributed Data Parallel](https://docs.pytorch.org/docs/stable/notes/ddp.html)
		- [Extending PyTorch](https://docs.pytorch.org/docs/stable/notes/extending.html)
		- [Extending torch.func with autograd.Function](https://docs.pytorch.org/docs/stable/notes/extending.func.html)
		- [Frequently Asked Questions](https://docs.pytorch.org/docs/stable/notes/faq.html)
		- [Getting Started on Intel GPU](https://docs.pytorch.org/docs/stable/notes/get_start_xpu.html)
		- [Gradcheck mechanics](https://docs.pytorch.org/docs/stable/notes/gradcheck.html)
		- [HIP (ROCm) semantics](https://docs.pytorch.org/docs/stable/notes/hip.html)
		- [Features for large-scale deployments](https://docs.pytorch.org/docs/stable/notes/large_scale_deployments.html)
		- [LibTorch Stable ABI](https://docs.pytorch.org/docs/stable/notes/libtorch_stable_abi.html)
		- [LocalTensor Tutorial: Single-Process SPMD Debugging](https://docs.pytorch.org/docs/stable/notes/local_tensor_tutorial.html)
		- [MKLDNN backend](https://docs.pytorch.org/docs/stable/notes/mkldnn.html)
		- [Bfloat16 (BF16) on MKLDNN backend](https://docs.pytorch.org/docs/stable/notes/mkldnn.html#bfloat16-bf16-on-mkldnn-backend)
		- [Modules](https://docs.pytorch.org/docs/stable/notes/modules.html)
		- [MPS backend](https://docs.pytorch.org/docs/stable/notes/mps.html)
		- [Multiprocessing best practices](https://docs.pytorch.org/docs/stable/notes/multiprocessing.html)
		- [Numerical accuracy](https://docs.pytorch.org/docs/stable/notes/numerical_accuracy.html)
		- [Out Notes](https://docs.pytorch.org/docs/stable/notes/out.html)
		- [Reproducibility](https://docs.pytorch.org/docs/stable/notes/randomness.html)
		- [Serialization semantics](https://docs.pytorch.org/docs/stable/notes/serialization.html)
		- [Windows FAQ](https://docs.pytorch.org/docs/stable/notes/windows.html)
- [Community](https://docs.pytorch.org/docs/stable/community/index.html)