# logs

`outputs/logs/` 用来保存知识库的时间导航记录。

它和 `answers/`、`syntheses/` 的区别是：

- `answers/` 记录一次具体问题的结果
- `syntheses/` 记录一个阶段性的主题收束
- `logs/` 记录这轮实际做了什么、用了哪些证据、产出了哪些文件

当前建议记录的动作类型：

- `ingest`
- `query`
- `lint`
- `backfill`

推荐命名：

- `YYYY-MM-DD-主题-动作记录.md`

健康检查补充约定：

- 健康检查主报告固定在 `outputs/answers/知识库-健康检查-最新.md`
- 健康检查日志固定在 `outputs/logs/知识库-健康检查-日志.md`
- 检查动作与修复动作写入同一日志文件，采用增量更新
