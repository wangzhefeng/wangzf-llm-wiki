---
source_type: web
title: "What are embeddings?"
author: 
created_at: 2026-04-06
topics:
  - 大语言模型
status: inbox
source: "https://vickiboykis.com/what_are_embeddings/"
published: 
created: 2026-04-06
description: "A deep-dive into machine learning embeddings."
tags:
  - 
  - "clippings"
---

![[assets/attachments/llm/kandinsky 1.png]]

If you go to the [Museu Picasso in Barcelona](https://museupicassobcn.cat/en), you'll see many of the artist's early works. They're really interesting because they don't look like what we think of as Picasso's style. These paintings, completed during his early years, are displays of his technical genius - as a classical painter.

Some particularly amazing examples are " [Science and Charity](https://en.wikipedia.org/wiki/Science_and_Charity) " and " [First Communion](https://www.wikiart.org/en/pablo-picasso/first-communion-1896) ". One of my favorites is "Portrait of the Artist's Mother." These were all painted when he was fifteen.

![[assets/attachments/llm/portrait.png]]

You can see both the artist's innate ability to make art, and his immense potential future. But to get to the point where Picasso could reject traditional styles, he had to master them first.

![[assets/attachments/llm/yellow_hat.png]]

This is also true for machine learning. There's a whole universe of exciting developments at the forefront of large language models. But in the noise of the bleeding edge, a lot of important foundational concepts get lost. If we don't [understand the fundamentals](https://increment.com/software-architecture/architecture-for-generations/) of how we get from a single word to a BERT representation, and more importantly, why we do so, the models will remain black boxes to us. We won't be able to build on them and master them in the ways that we want.

Peter Norvig urges us to [teach ourselves programming in ten years](https://norvig.com/21-days.html). In this spirit, after several years of working with embeddings, foundational data structures in deep learning models, I realized it's not trivial to have a good conceptual model of them. Moreover, when I did want to learn more, there was no good, general text I could refer to as a starting point. Everything was either too deep and academic or too shallow and content from vendors in the space selling their solution. So I started a project to understand the fundamental building blocks of machine learning and natural language processing, particularly as they relate to recommendation systems today. The results of this project are the PDF on this site, which is aimed at a generalist audience and not trying to sell you anything except the idea that vectors are cool. I've also been working on [Viberary](http://viberary.pizza/) to implement these ideas in practice.

In addition to his art, Picasso also left us with the quote,

> When art critics get together they talk about Form and Structure and Meaning. When artists get together they talk about where you can buy cheap turpentine.

I wrote this text for my own learning process. But it's my hope that this document puts embeddings in a business and engineering context so that others including engineers, PMs, students, and anyone looking to learn more about fundamentals finds it useful.

Machine learning, like all good engineering and like good art, is ultimately, a way for us to express ourselves, a craft made up of fundamental building blocks and patterns that empower us and allow us to build something beautiful on strong foundations of those that came before us. and I hope you find as much joy in exploring embeddings and using them as I did.

---

---

## Audience

Anyone who needs to understand embeddings, from machine learning engineers, to SWE, product or project manager, student, or simply curious. That said, there are different levels of understanding in the document. Here are my recommendations on how to read:

| # | You want | Sections | Prereqs |
| --- | --- | --- | --- |
| 1 | a high-level intro | 1,2 | how apps work |
| 2 | to understand engineering concerns | 1,2,5 | Python, engineering, Big O Notation |
| 3 | an ML internal deep dive | 3,4 | Linear Algebra, ML, Python, engineering |

---

## License

"What are embeddings" is licensed under a Creative Commons, By Attribution, Non-Commercial, Share Alike 3.0 license. This means that you are welcome to use, download and share the text, provided that attribution is given to the author (Vicki Boykis) and that it is released under the same license and [not used for commercial purposes](https://creativecommons.org/licenses/by-nc-sa/3.0/us/).

---

## Feedback

Feedback on the clarity of concepts or just typos is welcome. Feel free to [submit a PR](https://github.com/veekaybee/what_are_embeddings).