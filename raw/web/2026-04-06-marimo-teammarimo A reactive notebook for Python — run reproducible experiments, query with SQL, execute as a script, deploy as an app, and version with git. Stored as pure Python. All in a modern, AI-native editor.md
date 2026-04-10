---
source_type: web
title: "marimo-team/marimo: A reactive notebook for Python — run reproducible experiments, query with SQL, execute as a script, deploy as an app, and version with git. Stored as pure Python. All in a modern, AI-native editor."
author: 
created_at: 2026-04-06
topics:
  - 待分类
status: inbox
source: "https://github.com/marimo-team/marimo?tab=readme-ov-file"
published: 
created: 2026-04-06
description: "A reactive notebook for Python — run reproducible experiments, query with SQL, execute as a script, deploy as an app, and version with git. Stored as pure Python. All in a modern, AI-native editor. - marimo-team/marimo"
tags:
  - 
  - "clippings"
---

[![[assets/attachments/uncategorized/marimo-logotype-thick.svg]]](https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/marimo-logotype-thick.svg)

*A reactive Python notebook that's reproducible, git-friendly, and deployable as scripts or apps.*

[**Docs**](https://docs.marimo.io/) · [**Discord**](https://marimo.io/discord?ref=readme) · [**Examples**](https://docs.marimo.io/examples/) · [**Gallery**](https://marimo.io/gallery/) · [**YouTube**](https://www.youtube.com/@marimo-team/)

**English** **|** [**繁體中文**](https://github.com/marimo-team/marimo/blob/main/README_Traditional_Chinese.md) **|** [**简体中文**](https://github.com/marimo-team/marimo/blob/main/README_Chinese.md) **|** [**日本語**](https://github.com/marimo-team/marimo/blob/main/README_Japanese.md) **|** [**Español**](https://github.com/marimo-team/marimo/blob/main/README_Spanish.md)

**marimo** is a reactive Python notebook: run a cell or interact with a UI element, and marimo automatically runs dependent cells (or [marks them as stale](#expensive-notebooks)), keeping code and outputs consistent. marimo notebooks are stored as pure Python (with first-class SQL support), executable as scripts, and deployable as apps.

**Highlights**.

- 🚀 **batteries-included:** replaces `jupyter`, `streamlit`, `jupytext`, `ipywidgets`, `papermill`, and more
- ⚡️ **reactive**: run a cell, and marimo reactively [runs all dependent cells](https://docs.marimo.io/guides/reactivity.html) or [marks them as stale](#expensive-notebooks)
- 🖐️ **interactive:** [bind sliders, tables, plots, and more](https://docs.marimo.io/guides/interactivity.html) to Python — no callbacks required
- 🐍 **git-friendly:** stored as `.py` files
- 🛢️ **designed for data**: query dataframes, databases, warehouses, or lakehouses [with SQL](https://docs.marimo.io/guides/working_with_data/sql.html), filter and search [dataframes](https://docs.marimo.io/guides/working_with_data/dataframes.html)
- 🤖 **AI-native**: [generate cells with AI](https://docs.marimo.io/guides/generate_with_ai/) tailored for data work
- 🔬 **reproducible:** [no hidden state](https://docs.marimo.io/guides/reactivity.html#no-hidden-state), deterministic execution, [built-in package management](https://docs.marimo.io/guides/package_management/)
- 🏃 **executable:** [execute as a Python script](https://docs.marimo.io/guides/scripts.html), parameterized by CLI args
- 🛜 **shareable**: [deploy as an interactive web app](https://docs.marimo.io/guides/apps.html) or [slides](https://docs.marimo.io/guides/apps.html#slides-layout), [run in the browser via WASM](https://docs.marimo.io/guides/wasm.html)
- 🧩 **reusable:** [import functions and classes](https://docs.marimo.io/guides/reusing_functions/) from one notebook to another
- 🧪 **testable:** [run pytest](https://docs.marimo.io/guides/testing/) on notebooks
- ⌨️ **a modern editor**: [GitHub Copilot](https://docs.marimo.io/guides/editor_features/ai_completion.html#github-copilot), [AI assistants](https://docs.marimo.io/guides/editor_features/ai_completion.html), vim keybindings, variable explorer, and [more](https://docs.marimo.io/guides/editor_features/index.html)
- 🧑💻 **use your favorite editor**: run in [VS Code or Cursor](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo), or edit in neovim, Zed, [or any other text editor](https://docs.marimo.io/guides/editor_features/watching/)
```
pip install marimo && marimo tutorial intro
```

*Get started instantly with [**mo** lab, our free online notebook](https://molab.marimo.io/notebooks). Or jump to the [quickstart](#quickstart) for a primer on our CLI.*

## A reactive programming environment

marimo guarantees your notebook code, outputs, and program state are consistent. This [solves many problems](https://docs.marimo.io/faq.html#faq-problems) associated with traditional notebooks like Jupyter.

**A reactive programming environment.** Run a cell and marimo *reacts* by automatically running the cells that reference its variables, eliminating the error-prone task of manually re-running cells. Delete a cell and marimo scrubs its variables from program memory, eliminating hidden state.

[![[reactive.gif]]](https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/reactive.gif)

**Compatible with expensive notebooks.** marimo lets you [configure the runtime to be lazy](https://docs.marimo.io/guides/configuration/runtime_configuration.html), marking affected cells as stale instead of automatically running them. This gives you guarantees on program state while preventing accidental execution of expensive cells.

**Synchronized UI elements.** Interact with [UI elements](https://docs.marimo.io/guides/interactivity.html) like [sliders](https://docs.marimo.io/api/inputs/slider.html#slider), [dropdowns](https://docs.marimo.io/api/inputs/dropdown.html), [dataframe transformers](https://docs.marimo.io/api/inputs/dataframe.html), and [chat interfaces](https://docs.marimo.io/api/inputs/chat.html), and the cells that use them are automatically re-run with their latest values.

[![[assets/attachments/uncategorized/readme-ui.gif]]](https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/readme-ui.gif)

**Interactive dataframes.** [Page through, search, filter, and sort](https://docs.marimo.io/guides/working_with_data/dataframes.html) millions of rows blazingly fast, no code required.

[![[assets/attachments/uncategorized/docs-df.gif]]](https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/docs-df.gif)

**Generate cells with data-aware AI.** [Generate code with an AI assistant](https://docs.marimo.io/guides/editor_features/ai_completion/) that is highly specialized for working with data, with context about your variables in memory; [zero-shot entire notebooks](https://docs.marimo.io/guides/generate_with_ai/text_to_notebook/). Customize the system prompt, bring your own API keys, or use local models.

[![[assets/attachments/uncategorized/readme-generate-with-ai.gif]]](https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/readme-generate-with-ai.gif)

**Query data with SQL.** Build [SQL](https://docs.marimo.io/guides/working_with_data/sql.html) queries that depend on Python values and execute them against dataframes, databases, lakehouses, CSVs, Google Sheets, or anything else using our built-in SQL engine, which returns the result as a Python dataframe.

[![[assets/attachments/uncategorized/readme-sql-cell.png]]](https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/readme-sql-cell.png)

Your notebooks are still pure Python, even if they use SQL.

**Dynamic markdown.** Use markdown parametrized by Python variables to tell dynamic stories that depend on Python data.

**Built-in package management.** marimo has built-in support for all major package managers, letting you [install packages on import](https://docs.marimo.io/guides/editor_features/package_management.html). marimo can even [serialize package requirements](https://docs.marimo.io/guides/package_management/inlining_dependencies/) in notebook files, and auto install them in isolated venv sandboxes.

**Deterministic execution order.** Notebooks are executed in a deterministic order, based on variable references instead of cells' positions on the page. Organize your notebooks to best fit the stories you'd like to tell.

**Performant runtime.** marimo runs only those cells that need to be run by statically analyzing your code.

**Batteries-included.** marimo comes with GitHub Copilot, AI assistants, Ruff code formatting, HTML export, fast code completion, a [VS Code extension](https://marketplace.visualstudio.com/items?itemName=marimo-team.vscode-marimo), an interactive dataframe viewer, and [many more](https://docs.marimo.io/guides/editor_features/index.html) quality-of-life features.

## Quickstart

*The [marimo concepts playlist](https://www.youtube.com/watch?v=3N6lInzq5MI&list=PLNJXGo8e1XT9jP7gPbRdm1XwloZVFvLEq) on our [YouTube channel](https://www.youtube.com/@marimo-team) gives an overview of many features.*

**Installation.** In a terminal, run

```
pip install marimo  # or conda install -c conda-forge marimo
marimo tutorial intro
```

To install with additional dependencies that unlock SQL cells, AI completion, and more, run

```
pip install "marimo[recommended]"
```

**Create notebooks.**

Create or edit notebooks with

```
marimo edit
```

**Run apps.** Run your notebook as a web app, with Python code hidden and uneditable:

```
marimo run your_notebook.py
```

[![[assets/attachments/uncategorized/docs-model-comparison.gif]]](https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/docs-model-comparison.gif)

**Execute as scripts.** Execute a notebook as a script at the command line:

```
python your_notebook.py
```

**Automatically convert Jupyter notebooks.** Automatically convert Jupyter notebooks to marimo notebooks with the CLI

```
marimo convert your_notebook.ipynb > your_notebook.py
```

or use our [web interface](https://marimo.io/convert).

**Tutorials.** List all tutorials:

```
marimo tutorial --help
```

**Share cloud-based notebooks.** Use [molab](https://molab.marimo.io/notebooks), a cloud-based marimo notebook service similar to Google Colab, to create and share notebook links.

## Questions?

See the [FAQ](https://docs.marimo.io/faq.html) at our docs.

## Learn more

marimo is easy to get started with, with lots of room for power users. For example, here's an embedding visualizer made in marimo ([try the notebook live on molab!](https://molab.marimo.io/notebooks/nb_jJiFFtznAy4BxkrrZA1o9b/app?show-code=true)):

[![[assets/attachments/uncategorized/embedding.gif]]](https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/embedding.gif)

Check out our [docs](https://docs.marimo.io/), [usage examples](https://docs.marimo.io/examples/), and our [gallery](https://marimo.io/gallery) to learn more.

| [![[assets/attachments/uncategorized/Image 7.gif]]](https://docs.marimo.io/getting_started/key_concepts.html) | [![[assets/attachments/uncategorized/readme-ui.gif]]](https://docs.marimo.io/api/inputs/index.html) | [![[assets/attachments/uncategorized/docs-intro.gif]]](https://docs.marimo.io/guides/working_with_data/plotting.html) | [![[assets/attachments/uncategorized/outputs.gif]]](https://docs.marimo.io/api/layouts/index.html) |
| --- | --- | --- | --- |
| [Tutorial](https://docs.marimo.io/getting_started/key_concepts.html) | [Inputs](https://docs.marimo.io/api/inputs/index.html) | [Plots](https://docs.marimo.io/guides/working_with_data/plotting.html) | [Layout](https://docs.marimo.io/api/layouts/index.html) |
|  |  |  |  |

## Contributing

We appreciate all contributions! You don't need to be an expert to help out. Please see [CONTRIBUTING.md](https://github.com/marimo-team/marimo/blob/main/CONTRIBUTING.md) for more details on how to get started.

> Questions? Reach out to us [on Discord](https://marimo.io/discord?ref=readme).

## Community

We're building a community. Come hang out with us!

- 🌟 [Star us on GitHub](https://github.com/marimo-team/marimo)
- 💬 [Chat with us on Discord](https://marimo.io/discord?ref=readme)
- 📧 [Subscribe to our Newsletter](https://marimo.io/newsletter)
- ☁️ [Join our Cloud Waitlist](https://marimo.io/cloud)
- ✏️ [Start a GitHub Discussion](https://github.com/marimo-team/marimo/discussions)
- 🦋 [Follow us on Bluesky](https://bsky.app/profile/marimo.io)
- 🐦 [Follow us on Twitter](https://twitter.com/marimo_io)
- 🎥 [Subscribe on YouTube](https://www.youtube.com/@marimo-team)
- 🤖 [Follow us on Reddit](https://www.reddit.com/r/marimo_notebook)
- 🕴️ [Follow us on LinkedIn](https://www.linkedin.com/company/marimo-io)

**A NumFOCUS affiliated project.** marimo is a core part of the broader Python ecosystem and is a member of the NumFOCUS community, which includes projects such as NumPy, SciPy, and Matplotlib.

[![[assets/attachments/uncategorized/numfocus_affiliated_project.png]]](https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/numfocus_affiliated_project.png)

## Inspiration ✨

marimo is a **reinvention** of the Python notebook as a reproducible, interactive, and shareable Python program, instead of an error-prone JSON scratchpad.

We believe that the tools we use shape the way we think — better tools, for better minds. With marimo, we hope to provide the Python community with a better programming environment to do research and communicate it; to experiment with code and share it; to learn computational science and teach it.

Our inspiration comes from many places and projects, especially [Pluto.jl](https://github.com/fonsp/Pluto.jl), [ObservableHQ](https://observablehq.com/tutorials), and [Bret Victor's essays](http://worrydream.com/). marimo is part of a greater movement toward reactive dataflow programming. From [IPyflow](https://github.com/ipyflow/ipyflow), [streamlit](https://github.com/streamlit/streamlit), [TensorFlow](https://github.com/tensorflow/tensorflow), [PyTorch](https://github.com/pytorch/pytorch/tree/main), [JAX](https://github.com/google/jax), and [React](https://github.com/facebook/react), the ideas of functional, declarative, and reactive programming are transforming a broad range of tools for the better.

[![[assets/attachments/uncategorized/marimo-logotype-horizontal.png]]](https://raw.githubusercontent.com/marimo-team/marimo/main/docs/_static/marimo-logotype-horizontal.png)