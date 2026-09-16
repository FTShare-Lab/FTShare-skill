# Contributing to FTShare Skills

感谢你关注 `FTShare-skills`。

本仓库是 FTShare 面向 Agent 运行时提供的金融数据 Skill 接入项目。贡献内容围绕 `ftshare-market-data` 展开，包括金融数据子 Skill、接口适配、测试、文档和使用示例。

## 开发准备

克隆仓库：

```bash
git clone git@github.com:ftshare-lab/FTShare-skills.git
cd FTShare-skills
```

查看当前可用 Skill：

```bash
python3 ftshare-market-data/run.py
```

## 新增或修改 Skill

提交新 Skill 或修改现有 Skill 时，请保持：

- 每个 Skill 有独立 `SKILL.md`
- 每个 Skill 包有自己的 `README.md`
- 参数命名清晰
- 示例命令可执行
- 输出结构稳定，优先使用 JSON
- 下载类接口限制输出路径
- README 与实际能力保持同步
- 新增子 Skill 时同步更新父 Skill 的能力总览
- 涉及金融数据解释时写清时间、口径与返回字段
- 不在 Skill 中保存或输出用户密钥、令牌与其他敏感信息

## 提交流程

1. 从 `main` 拉取最新代码。
2. 新建功能分支。
3. 完成 Skill、文档和示例。
4. 本地运行相关命令，确认输出正常。
5. 提交 Pull Request，并说明修改内容和使用场景。

## 问题反馈

普通问题、功能建议和文档改进可以通过 GitHub Issue 或 Pull Request 提交。

安全相关问题请不要公开提交 Issue，请参考 [SECURITY.md](SECURITY.md)。
