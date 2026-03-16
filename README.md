# MOSS - OpenClaw Workspace

> 🤖 MOSS - 我的 AI 助手工作区备份

这个仓库备份了 **MOSS** (MiniMax-M2.5-Opus-Ultimate-v12.0) 在 OpenClaw 平台上的完整工作区，包括所有记忆、配置、项目和技能。

## 📁 目录结构

```
.
├── 🧠 记忆文件
│   ├── MEMORY.md          # 长期记忆（重要决策、项目记录）
│   └── memory/            # 每日记忆文件
│
├── ⚙️ 配置文件
│   ├── AGENTS.md          # OpenClaw 工作区规则
│   ├── SOUL.md            # AI 个性设定
│   ├── IDENTITY.md        # AI 身份信息
│   ├── USER.md            # 用户信息
│   ├── TOOLS.md           # 本地工具笔记
│   └── HEARTBEAT.md       # 定时检查任务配置
│
├── 📊 项目
│   └── finance-dashboard-v2/  # 金融看板项目（Git 子模块）
│
├── 🧰 已安装技能
│   └── skills/            # 所有通过 ClawHub/SkillHub 安装的技能
│
├── 📚 研究文档
│   ├── itick-research.md          # iTick API 初始研究
│   ├── itick-implementation-guide.md  # 实现指南
│   └── itick-config-guide.md      # 配置指南
│
└── 📂 其他
    ├── .learnings/        # 学习记录（错误、经验）
    └── openclaw-memory-hub/  # 智能记忆工具（子模块）
```

## 🚀 正在运行的项目

### [finance-dashboard](https://github.com/Honii-vscode/finance-dashboard)
- **描述**: 24/7 实时金融看板，展示中美市场数据
- **状态**: 活跃运行中
- **部署**: `http://43.156.96.119:3000`
- **技术**: Node.js + Express + 多数据源混合策略

## ⚙️ 配置

- **自动更新**: 已配置每日自动更新（每天凌晨 4:00 北京时间）
- **更新源**: 优先使用 `skillhub`（中国优化镜像）
- **Git**: 使用 SSH 认证推送到 GitHub

## 📋 内容说明

- 这个仓库是 **完整工作区备份**，包含 AI 的所有记忆和配置
- `finance-dashboard-v2` 和 `openclaw-memory-hub` 是 Git 子模块，指向独立仓库
- 所有研究文档保留作为历史记录，记录了项目从 0 到 1 的探索过程

## 👥 Contributors

- **张弘毅** - 项目发起人，用户配置
- **MOSS** - AI 助手，代码开发、文档编写、仓库维护

## 📄 License

MIT
