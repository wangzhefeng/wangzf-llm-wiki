---
source_type: web
title: "Your First API Call | DeepSeek API Docs"
author: 
created_at: 2026-04-06
topics:
  - 待分类
status: inbox
source: "https://api-docs.deepseek.com/"
published: 
created: 2026-04-06
description: "The DeepSeek API uses an API format compatible with OpenAI. By modifying the configuration, you can use the OpenAI SDK or softwares compatible with the OpenAI API to access the DeepSeek API."
tags:
  - 
  - "clippings"
---

## Your First API Call

The DeepSeek API uses an API format compatible with OpenAI. By modifying the configuration, you can use the OpenAI SDK or softwares compatible with the OpenAI API to access the DeepSeek API.

| PARAM | VALUE |
| --- | --- |
| base\_url <sup>*</sup> | `https://api.deepseek.com` |
| api\_key | apply for an [API key](https://platform.deepseek.com/api_keys) |

\* To be compatible with OpenAI, you can also use `https://api.deepseek.com/v1` as the `base_url`. But note that the `v1` here has NO relationship with the model's version.

\* **The `deepseek-chat` and `deepseek-reasoner` correspond to the model version DeepSeek-V3.2 (128K context limit), which differs from the APP/WEB version.** `deepseek-chat` is the **non-thinking mode** of DeepSeek-V3.2 and `deepseek-reasoner` is the **thinking mode** of DeepSeek-V3.2.

## Invoke The Chat API

Once you have obtained an API key, you can access the DeepSeek API using the following example scripts. This is a non-stream example, you can set the `stream` parameter to `true` to get stream response.

```bash
curl https://api.deepseek.com/chat/completions \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer ${DEEPSEEK_API_KEY}" \
  -d '{
        "model": "deepseek-chat",
        "messages": [
          {"role": "system", "content": "You are a helpful assistant."},
          {"role": "user", "content": "Hello!"}
        ],
        "stream": false
      }'
```