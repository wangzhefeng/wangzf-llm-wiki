# CLAUDE.md

本文件为 Claude Code 兼容入口。

## 主规范

本仓库唯一主规范为 [AGENTS.md](AGENTS.md)。

- Claude Code 在本仓库执行任务时，默认完整遵循 `AGENTS.md`。
- 若本文件与 `AGENTS.md` 冲突，以 `AGENTS.md` 为准。
- 新增或调整仓库级规则时，只在 `AGENTS.md` 维护；本文件不再维护并行规则。

## Claude 特有补充（最小）

- 默认使用简体中文（除非用户明确要求英文）。
- 默认直接执行任务并给出简洁进度更新。
- 无用户明确要求时，不主动提交、推送、开 PR。
