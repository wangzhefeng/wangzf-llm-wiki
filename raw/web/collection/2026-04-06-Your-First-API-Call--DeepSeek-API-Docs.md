---
source_type: web
source_url: https://api-docs.deepseek.com
title: Your First API Call | DeepSeek API Docs
created_at: 2026-04-06
topics:
  - 资料收集
status: inbox
---


# Your First API Call | DeepSeek API Docs

> 来源: https://api-docs.deepseek.com
> 提取时间: 2026-04-06 16:06:53

---

- [Skip to main content]()
- [DeepSeek API Docs Logo DeepSeek API Docs]()
DeepSeek API Docs
`English`
English
`Switch between dark and light mode (currently light mode)`
- [Quick Start]()
- [Your First API Call]()
- [The Temperature Parameter]()
- [Token & Token Usage]()
- [Rate Limit]()
- [Error Codes]()
- [News]()
- [DeepSeek-V3.2 Release 2025/12/01]()
- [DeepSeek-V3.2-Exp Release 2025/09/29]()
- [DeepSeek V3.1 Update 2025/09/22]()
- [DeepSeek V3.1 Release 2025/08/21]()
- [DeepSeek-R1-0528 Release 2025/05/28]()
- [DeepSeek-V3-0324 Release 2025/03/25]()
- [DeepSeek-R1 Release 2025/01/20]()
- [DeepSeek APP 2025/01/15]()
- [Introducing DeepSeek-V3 2024/12/26]()
- [DeepSeek-V2.5-1210 Release 2024/12/10]()
- [DeepSeek-R1-Lite Release 2024/11/20]()
- [DeepSeek-V2.5 Release 2024/09/05]()
- [Context Caching is Available 2024/08/02]()
- [New API Features 2024/07/25]()
- [API Reference]()
- [API Guides]()
- [Thinking Mode]()
- [Multi-round Conversation]()
- [Chat Prefix Completion (Beta)]()
- [FIM Completion (Beta)]()
- [JSON Output]()
- [Tool Calls]()
- [Context Caching]()
- [Anthropic API]()
- [Integrations]()
- [API Status Page]()
- [Change Log]()
- [Home page]()
Quick Start
Your First API Call

# Your First API Call
The DeepSeek API uses an API format compatible with OpenAI. By modifying the configuration, you can use the OpenAI SDK or softwares compatible with the OpenAI API to access the DeepSeek API.
base_url
https://api.deepseek.com
apply for an
- [API key]()
* To be compatible with OpenAI, you can also use
https://api.deepseek.com/v1
as the
base_url
. But note that the
here has NO relationship with the model's version.
The
deepseek-chat
and
deepseek-reasoner
correspond to the model version DeepSeek-V3.2 (128K context limit), which differs from the APP/WEB version.
deepseek-chat
is the
non-thinking mode
of DeepSeek-V3.2 and
deepseek-reasoner
is the
thinking mode
of DeepSeek-V3.2.

## Invoke The Chat API Direct link to Invoke The Chat API
Invoke The Chat API
- [Direct link to Invoke The Chat API]()
Once you have obtained an API key, you can access the DeepSeek API using the following example scripts. This is a non-stream example, you can set the
stream
parameter to
true
to get stream response.
curl https://api.deepseek.com/chat/completions \\
-H \
-H \
-d '{
`Toggle word wrap`
`Copy code to clipboard`
Next
- [Invoke The Chat API]()
WeChat Official Account
Community
- [Email]()
- [Discord]()
- [Twitter]()
More
- [GitHub]()
Copyright © 2026 DeepSeek, Inc.

