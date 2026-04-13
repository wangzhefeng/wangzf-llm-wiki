---
author: null
created: 2026-04-06
created_at: 2026-04-06
description: A tool that connects everyday work into one space. It gives you and your
  teams AI tools—search, writing, note-taking—inside an all-in-one, flexible workspace.
source_type: web
status: inbox
tags:
- null
- clippings
title: Smth Smth GPU Related
source_url: https://sodakeyeatsmush.notion.site/Smth-Smth-GPU-Related-27bf1129214e804ba217e8d5d08fc8b5#27bf1129214e80928aeef2a9fa3c0e38
published_at: null
related_concepts: []
topics:
  - deep-learning-theory
  - 深度学习理论
---

For quite some time, I’ve been wanting to learn about GPUs. As someone in ML, I use them a lot, but I was really curious to understand how they actually work under the hood.

These are my notes on GPUs which I made while learning about GPUs from [Modal's GPU Glossary](https://modal.com/gpu-glossary).

The GPU Glossary is an excellent resource, but it can feel a bit overwhelming/dense for absolute beginners. So I made these notes to simplify things and put them in a more digestible format. At many points, I also used Gemini to help me better understand some concepts.

I’ve covered most of the topics from the glossary, though not all - only the ones I found most relevant for my use case.

## Device Hardware

### CUDA Device Architecture

CUDA ⇒ Compute Unified Device Architecture

Before CUDA, Early GPUs were essentially hardware-based assembly lines specifically for rendering 3D graphics. This pipeline had distinct, specialized hardware stages for each part of the process.

The GPU manufacturer had to guess the ratio of vertex processors to fragment processors. If a particular game or application had very complex geometry but simple coloring, the fragment processors would sit idle while the vertex processors were bottlenecked. The reverse was also true. This meant a portion of the chip's silicon was often underutilized.

Developers were forced to map their programs onto this fixed hardware structure. It was difficult to use the GPU for anything other than its intended graphics tasks, as the hardware itself was inflexible.

Starting with the G80 architecture (GeForce 8800), NVIDIA introduced a "unified" design. They replaced the separate, specialized processing blocks with a large array of identical, flexible processors called Streaming Multiprocessors (SMs). The main subcomponents of Streaming Multiprocessors are the CUDA Cores and (for recent GPUs) Tensor Cores.

### Streaming Multiprocessor

It can be thought of as the equivalent of a core on a CPU. It's the unit that actually executes instructions. But the difference is that a GPU SM can execute more threads in parallel.

For now think of a thread as an extremely lightweight worker that executes a sequence of instructions. We will take a look at it in one of the upcoming sections.

Now let’s try to understand about a streaming multiprocessor

An SM cares about high-throughput. It is designed to hide its latency by managing an enormous number of threads. Its silicon budget is spent not on complex control logic, but on a massive number of raw computational units.

Threads on a GPU are executed in groups of 32(usually), known as a warp. All 32 threads in a warp execute the same instruction on different data simultaneously.

An SM can handle many warps concurrently. When one warp must stall for a slow operation, like fetching data from memory, the Warp Scheduler doesn't wait.

It instantly and with zero overhead (within a single clock cycle) swaps out the stalled warp and begins executing instructions from another warp that is ready to run. (Because the SM has such a massive pool of threads to choose from, it can almost always find a warp that's ready to work. This ensures its computational units are constantly utilized, effectively hiding the time that would have been wasted waiting.)

For eg H100 SXM GPU has 132 SM’s each of which has four Warp Schedulers that can each issue instructions to 32 threads (aka a warp ) in parallel per clock cycle, for a total of 128 × 132 > 16,000 parallel threads running. These 16,000 threads are running truly in parallel ie each of these 16000 threads can make progress in each clock cycle.

A single SM on a H100 can concurrently execute up to 2048 threads split across 64 thread groups of 32 threads each. As we have 132 SMs so that gives a total of 250,000 concurrent threads. This is the much larger pool of active threads the GPU keeps loaded and ready to go.

If one group out of the 16,000 has to stop and wait for data. Instead of letting the hardware sit idle, the GPU's scheduler instantly swaps out the waiting threads and swaps in another group from the massive list of 250,000 threads.

### GPU Core

The cores are the primary compute units that make up the Streaming Multiprocessors (SMs).

Types of GPU cores include tensor cores and CUDA cores.

GPU cores should not be thought of as CPU cores.

A better way to think about GPU cores would be to think of them as pipes - some data enters it and transformed data comes out. Each pipe is associated with specific types of instructions. For eg floating point matrix multiplication arithmetic throughput in the case of the Tensor Cores.

SM is somewhat closer to being an equivalent of CPU core.

### Special Function Unit

The Special Function Units (SFUs) in SMs accelerate certain arithmetic operations. Handles special math operations that would otherwise be slow if done on normal cores.

### Load/Store Unit(LSU)

Moves data between registers inside the SM and memory (caches, global GPU memory, etc.). Load: Fetch data from memory → put into registers for computation. Store: Take results from registers → write back to memory.

Efficient use of LSUs + memory hierarchy = big performance boost in GPU programming.

### Warp Scheduler

Decides which group of threads to execute on each clock cycle.

These groups of threads, known as warps, are switched out on a per clock cycle basis

The ability of the Warp Schedulers to switch rapidly between a large number of concurrent tasks as soon as their instructions' operands are available is key to the latency hiding capabilities of GPUs.

A full CPU thread context switch can take hundreds to thousands of cycles (microseconds), as the system must save and restore thread states.

This also reduces locality, often leading to increased cache misses, which further degrades performance.

The new thread might be working on completely different data than the old one.

That means the data currently in the CPU caches (which belonged to the old thread) is not useful anymore.

GPUs avoid this cost because each thread already has its own private registers allocated from the SM’s register file. Thus, switching warps does not require saving or restoring state. The L1 caches on GPUs are often programmer-managed and shared among the warps scheduled onto an SM. This sharing, along with the lack of expensive state-saving, means that cache hit rates are less affected by context switching compared to CPUs.

### CUDA Core

Responsible for executing scalar arithmetic instructions. On the other hand tensor cores are responsible for handling matrix operations.

Unlike CPU cores, CUDA Cores are not independently scheduled. A Warp Scheduler issues the same instruction to a group(warp) of CUDA Cores simultaneously. Each core applies the instruction to different registers.

The term “CUDA Core” is not fixed.

In different GPU generations/architectures, CUDA Cores may represent different mixes of units:

32-bit integer units

32-bit floating-point units (FP32)

64-bit floating-point units (FP64)

### Tensor Core

Specialized GPU cores designed to operate on entire matrices with each instruction

Its fundamental operation is the Matrix Multiply-Accumulate (MMA), mathematically expressed as $D=AB+C$.

where A,B,C,D( C is often the same physical matrix as D) are matrices.

Lets take a look at the efficiency of Tensor Cores

On CUDA cores, if you want to do a matrix multiplication, you break it down into tons of scalar multiply-adds.

Tensor cores can do this in a single instruction

On modern CPUs/GPUs, a surprising amount of energy is spent not on math, but on:

Instruction fetch

Instruction decode

Instruction issue/scheduling

Operating on more data for a single instruction fetch dramatically reduces power requirements, which unlocks increased performance

Note: A single instruction in a single thread does not produce the entire matrix multiplication. The 32 threads of a warp cooperatively produce the result.

This means a Tensor Core instruction is not executed by a single thread in isolation. Instead, it's a collective command issued to a group of 32 threads (a warp), and the hardware is designed to orchestrate these 32 threads to perform one large, shared task. This follows the SIMT (Single Instruction, Multiple Thread) model. The key to understanding this is data fragmentation. No single thread holds the entire A, B, and C matrices. Instead, each of the 32 threads holds a small, unique fragment of these matrices in its own private registers.

Tensor Cores are much larger and less numerous than CUDA Cores.

### Tensor Memory Accelerators (TMAs)

A Tensor Memory Accelerator is special hardware inside newer NVIDIA GPUs (Hopper, Blackwell) that helps move big blocks of data (like arrays or matrices) from GPU memory into fast on-chip memory.

Advantages of TMAs are

Less overhead: Normally, copying arrays requires lots of little address calculations and temporary register storage. TMAs take over this job in hardware, so CUDA cores and registers are freed up for actual computation.

Asynchronous execution:

A thread tells the TMA hardware: “Go copy this big block of data from global memory into shared memory.”

Instead of waiting, the thread immediately goes back to doing other useful work (math, logic, etc.).

Meanwhile, the TMA hardware, in parallel, is performing the copy in the background.

Later, when the program actually needs the data, the threads can check: “Is the copy finished yet?”

If yes → use the data.

If not → do something else until it is.

### Texture Processing Cluster (TPC)

A Texture Processing Cluster is simply a pair of SMs grouped together. Earlier GPU generations didn’t expose this grouping in CUDA, but starting with the Blackwell architecture, it became relevant because some new Tensor Core instructions can operate at the TPC level instead of just a single SM. This means that instead of one SM running a tensor operation, two SMs can cooperate on it, effectively giving more parallel horsepower for larger matrix multiplications

### Graphics/GPU Processing Cluster (GPC)

A GPU Processing Cluster is a larger unit made up of multiple TPCs plus a raster engine (the graphics side of things). From an ML perspective, the raster engine isn’t relevant, but the grouping of TPCs is.

What’s relevant is that newer GPUs (like Hopper) added a concept called thread block clusters, which map to GPCs. This basically means:

Normally, all threads in a block run on one SM and share that SM’s memory.

Now, several blocks can be grouped into a cluster that spans multiple SMs inside the same GPC.

These blocks can share a new type of memory called distributed shared memory, which makes communication between them faster than going all the way to global memory.

### Register File

Registers are the fastest memory in an SM, and the register file is where threads store their working variables during computation.

Unlike L1 or shared memory, registers can keep pace with the compute cores themselves - they’re roughly an order of magnitude faster.

However, there’s a catch: each SM has a finite number of registers, and if each thread uses too many, the number of threads that can run simultaneously decreases. This is called register pressure, and it directly reduces occupancy, which is the number of active threads on the SM.

Low occupancy hurts performance because it reduces the GPU’s ability to hide memory latency.

### L1 Data Cache

The L1 cache is a small, very fast memory that sits inside each Streaming Multiprocessor (SM).

It’s much faster than global GPU memory, though slower than registers.

It’s typically programmer-managed in CUDA (unlike CPU caches, which are mostly automatic). This means you can control what goes into L1/shared memory to optimize performance.

In ML workloads, you use it to store small chunks of data (tiles) that many threads in the same block will reuse, e.g., during matrix multiplications or convolution kernels.

### Tensor Memory

This is special-purpose memory inside an SM designed specifically for Tensor Cores. It holds the inputs/outputs of Tensor Core operations (matrix multiplications). Access is tightly restricted: warps must coordinate in groups, and only certain usage patterns are allowed.

### GPU RAM (VRAM)

This is the large, slowest memory (relative to registers and cache), but it stores all your data - models, tensors, parameters, activations.

Every SM can access it, but going to GPU RAM has high latency (hundreds of cycles).

ML workloads constantly move data from GPU RAM → L2 cache → L1/shared memory → registers/Tensor Memory. Optimizing this data movement is crucial for performance.

Example: Training a transformer - the model weights live in VRAM, but for each matmul, the relevant tiles get loaded into L1/shared/Tensor Memory for fast compute.

## Device Software

### CUDA Programming Model

The CUDA Programming Model is a framework that allows programmers to write massively parallel programs by organizing work into scalable hierarchies of threads and memory.

The Three Core Abstractions

Hierarchy of Thread Groups

Grid: The entire collection of threads for a specific task

Block: A grid is divided into multiple thread blocks.

Hierarchy of Memories

Different levels of threads have access to different types of memory for communication:

Shared Memory: An extremely fast, on-chip memory that is private to a thread block.

Global Memory: A larger, slower memory accessible by all threads in the entire grid.

Barrier Synchronization: This is a mechanism that allows threads to coordinate. A programmer can place a barrier, which forces all threads within a thread block to pause at that point until every single thread in the block has reached it. This ensures that certain tasks are complete before the group moves on to the next step, preventing race conditions and ensuring correct data sharing.

### Streaming Assembler (SASS)

Streaming Assembler (SASS) is the native, hardware-specific assembly language for NVIDIA GPUs. It's the lowest level of human-readable code that directly maps to the machine instructions executed by the GPU's SMs.

Hardware-Specific: Each version of SASS is tied to a specific GPU architecture (e.g., Hopper, Ampere, Lovelace). Code written in SASS for a Hopper GPU will not run on a different generation of hardware. This is in contrast to PTX, which is a more general, intermediate assembly language that gets compiled down to architecture-specific SASS.

Poorly Documented: NVIDIA provides very limited official documentation on SASS.

Writing SASS by hand is exceptionally rare due to its complexity and lack of portability. Its primary and most valuable use is for performance engineering and debugging.

### Parallel Thread Execution(PTX)

Parallel Thread Execution (PTX) is a stable, intermediate assembly language that acts as a "virtual GPU" instruction set for NVIDIA hardware.

PTX defines a virtual machine with a consistent instruction set. When a compiler generates PTX code, it's targeting this abstract, idealized GPU rather than a specific physical chip. This allows developers to write parallel programs with the confidence that they will execute with the same semantics across many different generations of NVIDIA hardware.

PTX is not the final code that the GPU executes, it's an intermediate step. The compilation flow is:

CUDA C++ (High-Level Code): The programmer writes code in a language like CUDA C++.

PTX (Intermediate Code): The

nvcc

compiler translates the C++ into PTX assembly.

SASS (Machine Code): When you run the program, the NVIDIA driver on your machine performs a Just-In-Time (JIT) compilation, translating the portable PTX code into the native, hardware-specific SASS that your particular GPU understands.

The most important feature of PTX is forward compatibility. This means an application compiled to PTX today will automatically run on NVIDIA GPUs released years from now.

### Compute Capability

Compute Capability is a version number (e.g., 8.6, 9.0) that defines the set of features and instructions supported by an NVIDIA GPU's hardware

When you compile a CUDA application, you target a specific Compute Capability. This tells the compiler what features and instructions it's allowed to use. The primary purpose of this system is to enable forward compatibility. Thanks to the PTX intermediate language, code compiled for an older Compute Capability (e.g., 7.0 for Volta) is guaranteed to run on a newer GPU with a higher Compute Capability

### CUDA Thread

A CUDA thread is the most fundamental unit of execution in the CUDA programming model. It is an extremely lightweight worker that executes a sequence of instructions (a kernel) on a single CUDA Core.

Basic Unit of Work: A thread is the smallest, most granular component of a GPU program. It has its own private registers to perform calculations but possesses minimal other resources, which allows the GPU to create and manage hundreds of thousands of them with very low overhead.

The instructions from a single CUDA thread are executed by a single CUDA Core.

For performance reasons, threads do not run with complete independence. They are organized into groups of 32 called a warp. All 32 threads in a warp execute the same instruction at the exact same time on different data. This synchronized, parallel execution model is the foundation of the GPU's massive throughput.

### Warp

A warp is a group of 32 threads that are scheduled and executed together as a single unit on a Streaming Multiprocessor (SM). It's the fundamental unit of execution on NVIDIA GPUs.

A warp operates on the "Single Instruction, Multiple Thread" (SIMT) principle. At any given moment, all 32 threads in a warp execute the exact same instruction, but on their own private data. This lockstep execution is extremely efficient.

However, if a conditional statement (like an

if/else

block) causes threads within a warp to take different paths, it leads to warp divergence, where some threads are idle while others execute. This is a significant source of performance loss and should be avoided when possible.

The primary function of the warp scheduling system is latency hiding. An SM can manage multiple warps at once. When one warp stalls - meaning it has to wait for a slow operation like a memory fetch - the SM's Warp Scheduler doesn't wait with it. It instantly switches to another resident warp that is ready to execute.

It's important to understand that the warp is a hardware implementation detail, not a formal part of the CUDA programming model's hierarchy (like thread blocks or grids). For program correctness, you don't need to manage warps directly.

### Cooperative Thread Array

A Cooperative Thread Array (CTA) is the hardware-level implementation of a thread block in CUDA. It is a collection of threads that are always scheduled onto the same Streaming Multiprocessor (SM). Internally, a CTA is composed of one or more warps.

Threads within a CTA can efficiently coordinate and share data using shared memory. This makes intra-CTA communication fast. However, CTAs cannot synchronize directly with other CTAs, inter CTA communication has to go through global memory.

The number of CTAs that can run on a single SM at the same time depends on limited hardware resources such as registers, shared memory, and warp slots. This determines the occupancy of the GPU i.e., how many threads can be kept active to hide latency.

### CUDA Kernel

A kernel is the unit of CUDA code that programmers typically write and compose, it can be thought of as procedures/functions.

The fundamental difference between a kernel and a standard CPU function is its execution model: you "launch" a kernel once from the host (CPU), but it is executed in parallel by thousands or even millions of GPU threads. Each thread runs the same kernel code, but operates on different data by using its unique thread and block indices.

The entire collection of threads launched for a single kernel is called a grid, which is the highest level of the CUDA thread hierarchy.A kernel grid executes across multiple Streaming Multiprocessors (SMs) and so operates at the scale of the entire GPU. The matching level of the memory hierarchy is the global memory.

The main idea behind writing a CUDA kernel is to take a massive, repetitive computational problem and restructure it to run in parallel on thousands of GPU cores at once, with the primary goal of keeping those cores constantly fed with data.

Modern GPUs can perform calculations (FLOPs) much faster than they can fetch data from memory. This is the "memory wall." A naive kernel will have the GPU's powerful cores sitting idle, waiting for data.

The number one goal of a high-performance kernel writer is to maximize arithmetic intensity - the ratio of math operations to slow memory operations.

ML frameworks provide kernels for common ops (matmul, conv, ReLU, layernorm, etc.).

But if you invent a new operation (say, a new kind of attention, custom activation, or data transformation), the library won’t have it. You could write it in plain PyTorch (

for

loops, tensor ops), but that will be slow because it runs on the CPU or launches too many small GPU ops.

Writing a custom CUDA kernel lets you fuse that new op into one efficient GPU pass.

### CUDA Thread Block

It is a group of threads that are executed together on a single Streaming Multiprocessor (SM). It's the primary unit of cooperation and scheduling in the CUDA programming model.

”thread block” is the term you, the programmer, use in the CUDA programming model. When the high-level CUDA code is compiled, the abstract concept of a thread block is translated into a concrete Cooperative Thread Array (CTA).

So basically from what I can understand(this might be technically incorrect idk) the same group of threads is called thread block in CUDA whereas CTA in PTX/SASS assembly.

While threads within a block cooperate, different thread blocks are completely independent of each other. By enforcing that thread blocks are independent, the CUDA programming model provides no mechanism for direct communication or synchronization between them. This transforms the entire grid of blocks into an unordered "bag of work."

This is a deliberate constraint. It frees the GPU's hardware scheduler from any dependencies. The scheduler's only job is to pick an available thread block from the bag and assign it to any available Streaming Multiprocessor (SM) for execution. The order in which blocks are picked is non-deterministic and irrelevant to the final result.

When you run your code on a new GPU with more SMs, the hardware can simply execute more of these independent blocks simultaneously, making your program run faster without any code changes.

For example on an older GPU with 80 SMs, the scheduler can execute 80 blocks in parallel. On a newer GPU with 128 SMs, when you run the exact same compiled code, the new scheduler has more resources. It can execute 128 blocks in parallel.

### Thread Block Grid

A Thread Block Grid (or simply "grid") is the highest level of the thread hierarchy in the CUDA programming model. It represents the entire collection of threads launched for a single kernel, encompassing all the thread blocks that will execute the kernel's code.

When a programmer launches a CUDA kernel, they are defining the dimensions and size of a single grid. This grid is a one, two, or three-dimensional array of thread blocks.

The corresponding level of the memory hierarchy for a grid is global memory, which is accessible by all threads within that grid.

The most important characteristic of a grid is that it is composed of completely independent thread blocks.

### CUDA Thread Hierarchy

Thread: This is the lowest and most fundamental level. A thread is a single worker that executes the kernel's instructions. Each thread has its own private registers and is mapped to a single CUDA Core for execution. Each thread has a unique, built-in identifier that it can use to determine which part of the data to work on. These identifiers are variables like:

threadIdx

: An index that identifies a thread within its block (e.g., "I am worker #5 in my team").

blockIdx

: An index that identifies a thread block within the grid (e.g., "I am on team #12").

blockDim

: A variable that holds the dimensions (size) of the thread block.

Thread Block: This is the intermediate level. A thread block is a group of threads that are guaranteed to run on the same Streaming Multiprocessor (SM).

Grid: This is the highest level. A grid is the collection of all thread blocks for a single kernel launch. It represents the entire workload and is executed across the whole GPU.

Each level of the abstract corresponds directly to a specific physical component of the GPU hardware. An individual thread runs on a CUDA Core, a thread block runs on a Streaming Multiprocessor (SM), and the entire grid of blocks is distributed across the whole GPU.

### CUDA Memory Hierarchy

The CUDA Memory Hierarchy is a tiered system of memory spaces that corresponds directly to the CUDA Thread Hierarchy. Each level of the thread hierarchy has access to a different type of memory.

Registers (Thread Level): This is the fastest memory space on the GPU, located directly on the SM in the register file. Each individual thread has its own private registers to hold its working variables. Access is extremely fast, essentially on par with the speed of computation. While registers are private by default, certain advanced instructions for Tensor Cores can share data between the registers of threads within a warp.

Shared Memory (Block-Level): This is a fast, on-chip memory bank, physically located in each SM's L1 data cache. It is accessible to all threads within a single thread block (CTA). Because it is shared by a cooperative team, it is the primary mechanism for high-speed data exchange and coordination between threads in a block. The art of writing fast kernels often revolves around orchestrating the efficient use of shared memory to minimize slow trips to global memory.

Global Memory (Grid-Level): This is the largest memory space, but also the slowest. Physically, it is the GPU RAM. It is accessible by all threads across the entire grid. Because it is the only way for different thread blocks to communicate and is the primary storage for initial inputs and final outputs, all programs must use it. However, because it has high latency, performance-critical kernels aim to minimize the frequency of global memory accesses.

### Registers

Apart from the stuff which we discussed about registers in the previous section, here is some more stuff worth knowing

In high-level languages like CUDA C++, you don't manage registers directly, the compiler allocates them automatically. The number of registers a kernel uses per thread is a critical performance factor. An SM has a fixed-size register file that is shared among all its resident threads. A kernel that uses fewer registers per thread allows more threads (and thus more thread blocks) to be scheduled on the SM simultaneously. This increases occupancy, which is crucial for hiding memory latency and maximizing the GPU's throughput.

While registers are an abstraction in CUDA C++, they are explicitly visible and manipulated in the lower-level Parallel Thread Execution (PTX) language.

### Shared Memory

Shared Memory is physically located in the L1 data cache of each Streaming Multiprocessor (SM). Because it is on-chip and shared by a thread block, it is the key to writing high-performance kernels.

The typical workflow involves using shared memory to minimize slow access to global memory:

Threads in a block cooperatively load data from slow global memory into fast shared memory.

The threads then perform numerous computations, reading and writing to the fast shared memory.

Once the computation is complete, the final results are written back to global memory.

### Global Memory

Global Memory is the largest memory space on the GPU, physically located in the GPU’s RAM.

It is "global" in both scope and lifetime i.e. it is accessible by every thread in the entire grid and persists for the duration of the application.

Its primary roles are:

Storing initial input data and final output results for a kernel.

The only means of communication between different thread blocks, typically through slower atomic operations.

Because it is off-chip, global memory has much higher latency than shared memory. Therefore, a well-designed kernel will always aim to minimize the number of times it needs to be accessed.