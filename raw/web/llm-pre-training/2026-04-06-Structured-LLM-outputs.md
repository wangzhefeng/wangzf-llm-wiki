---
source_type: web
title: "Structured LLM outputs"
author: 
created_at: 2026-04-06
topics:
  - 大语言模型
status: inbox
published: 
created: 2026-04-06
description: "A practical handbook for developers using LLMs to get structured outputs."
tags:
  - 
  - "clippings"
source_url: "https://nanonets.com/cookbooks/structured-llm-outputs"
published_at: null
related_concepts: []
---

LLMs mostly produce syntactically valid outputs when we try generating JSON, XML, code, etc., but they can occasionally fail due to their probabilistic nature. This is a problem for developers as we use LLMs programmatically, for tasks like data extraction, code generation, tool calling, etc.

![[pipedream-a9e6cafdfc5a2b271cc2ff623cc21e68.png|breaktasks]]

LLMs came with the promise of agents and automation. But without structured outputs, it’s just a pipe dream.

There are many deterministic ways to ensure structured LLM outputs. If you are a developer, this handbook covers everything you need.

- What happens under-the-hood?
- What are the best tools & techniques?
- How to pick the right tools & techniques?
- How to build, deploy, and scale systems?
- How to optimize for latency and cost?
- How to improve the quality of output?

## Motivation

Structured generation is moving too fast. Most resources you find today are already outdated. You have to dig through multiple academic papers, blogs, GitHub repos, and other resources.

This handbook brings it all together in a living document that updates regularly.

## How to use this

You can read it start-to-finish, or treat it like a lookup table.

## Who are we?

We're the maintainers of [Nanonets-OCR models](https://huggingface.co/nanonets/models) (VLMs to convert documents into clean, structured Markdown) and [docstrange](https://github.com/NanoNets/docstrange) (open-source document processing library).