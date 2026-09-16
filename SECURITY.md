# Security Policy

## Reporting a vulnerability

如果你发现 `FTShare-skills` 中存在安全问题，请负责任地报告。

- 请不要在公开 GitHub Issue 中披露安全漏洞。
- 请发送邮件至 **liulei@ft.tech**，并说明问题描述、复现步骤和潜在影响。

我们会尽快确认并处理。

## Scope

本安全策略覆盖本仓库中的：

- Skill 描述文件
- 调度入口
- handler 实现
- 下载与文件写入逻辑
- 与 FTShare 数据服务交互的代码

第三方依赖或外部 Agent 运行时中的安全问题，请向对应项目维护者报告。

## Data service boundary

本仓库中的代码和 Skill 实现采用开源许可证，但 FTShare 数据服务的访问额度、权限和商业用途，可能受单独的数据服务条款约束。
