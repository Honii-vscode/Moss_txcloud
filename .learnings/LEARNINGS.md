# Learnings

Corrections, insights, and knowledge gaps captured during development.

**Categories**: correction | insight | knowledge_gap | best_practice
**Areas**: frontend | backend | infra | tests | docs | config
**Statuses**: pending | in_progress | resolved | wont_fix | promoted | promoted_to_skill

## Status Definitions

| Status | Meaning |
|--------|---------|
| `pending` | Not yet addressed |
| `in_progress` | Actively being worked on |
| `resolved` | Issue fixed or knowledge integrated |
| `wont_fix` | Decided not to address (reason in Resolution) |
| `promoted` | Elevated to CLAUDE.md, AGENTS.md, or copilot-instructions.md |
| `promoted_to_skill` | Extracted as a reusable skill |

## Skill Extraction Fields

When a learning is promoted to a skill, add these fields:

```markdown
**Status**: promoted_to_skill
**Skill-Path**: skills/skill-name
```

Example:
```markdown
## [LRN-20250115-001] best_practice

**Logged**: 2025-01-15T10:00:00Z
**Priority**: high
**Status**: promoted_to_skill
**Skill-Path**: skills/docker-m1-fixes
**Area**: infra

### Summary
Docker build fails on Apple Silicon due to platform mismatch
...
```

---


---

## [LRN-20260313-001] correction

**Logged**: 2026-03-13T05:30:00Z
**Priority**: low
**Status**: pending
**Area**: config

### Summary
用户想知道我是否使用了特定技能（如weather技能），而不仅仅是直接用命令行工具

### Details
用户问"你在输出这个结果时使用了你的weather技能吗？"
实际上我直接用 curl 查询了 wttr.in，没有走 weather 技能的流程

### Suggested Action
当用户问是否使用某个技能时，应该：
1. 诚实回答是否使用了该技能
2. 如果直接用了底层工具，可以解释技能本质上也是调用这些工具
3. 可以问用户是否希望我使用特定技能

### Metadata
- Source: user_feedback
- Tags: skill-usage, transparency


---

## [LRN-20260313-002] user_preference

**Logged**: 2026-03-13T06:17:00Z
**Priority**: high
**Status**: pending
**Area**: config

### Summary
用户要求：做任何事情之前都要先商量，经过同意后再执行

### Details
张弘毅明确要求：
- 写代码前要先商量
- 自主做任何事之前要征得同意
- 不要擅自行动

### Suggested Action
1. 严格遵守：任何操作前先询问
2. 即使是简单任务也要先确认
3. 可以在建议后加 "可以吗？" 或 "要继续吗？"
4. 重要操作可以给多个选项让用户选择

### Metadata
- Source: user_feedback
- Tags: workflow, consent, user-preference


---

## [LRN-20260313-003] best_practice

**Logged**: 2026-03-13T06:28:00Z
**Priority**: medium
**Status**: pending
**Area**: backend

### Summary
腾讯财经API需要符号格式映射，不同市场使用不同前缀

### Details
- 上证指数: sh000001
- A股600开头: sh600900
- 深证399开头: sz399006
- 港股5位数字: hkXXXXX
- 美股: 直接用代码如SPY

### Suggested Action
新增股票时需要：
1. 在 server-tencent-finance.js 添加符号配置
2. 在 tencent-finance-integration.js 的 symbolMapping 添加格式映射
3. 前端 display 格式和后端 API 格式可能不同，需要转换

### Metadata
- Source: error_recovery
- Tags: tencent-finance, api, symbol-mapping


---

## [LRN-20260313-004] user_preference

**Logged**: 2026-03-13T06:35:00Z
**Priority**: high
**Status**: pending
**Area**: config

### Summary
用户要求：任何行动之前必须先问，得到"执行"答复后才能行动

### Details
张弘毅明确要求：
1. 我提出建议/方案
2. 问用户"要执行吗？"
3. 等用户回复"执行"后
4. 才开始行动
- 没有"执行"两个字，绝不行动

### Suggested Action
严格遵守此准则，绝不绕过

### Metadata
- Source: user_feedback
- Tags: workflow, consent, execution-require


---

## [LRN-20260313-005] project_summary

**Logged**: 2026-03-13T07:36:00Z
**Priority**: medium
**Status**: pending
**Area**: project

### Summary
金融看板项目重大更新汇总

### Details
今天完成的主要工作：

1. **UI重新设计**
   - 采用高端财经杂志风格（黑白灰+金色点缀）
   - Playfair Display衬线体标题
   - Source Sans 3现代正文
   - 标题改为两行：Finance. + Dashboard

2. **新增股票/指数**
   - 中国市场：中证A500(000510)、长江电力(600900)、小米集团(01810.HK)
   - 美股市场：标普500(usINX)、纳斯达克综合(usIXIC)、英伟达(NVDA)、谷歌(GOOG)
   - 加密货币板块：比特币、以太坊（CoinGecko数据源）

3. **技术修复**
   - 腾讯财经符号映射修复（sh600900等）
   - 美元符号判断逻辑修复
   - 加密货币涨跌数据源从CryptoCompare改为CoinGecko

4. **系统优化**
   - 保持活跃脚本(keep-alive)已启动，24/7自动运维

### Metadata
- Source: daily_work
- Tags: finance-dashboard, project-update

