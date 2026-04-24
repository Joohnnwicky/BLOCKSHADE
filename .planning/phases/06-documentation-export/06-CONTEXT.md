# Phase 6: Documentation & Export - Context

**Gathered:** 2026-04-24
**Status:** Ready for planning

<domain>
## Phase Boundary

完善导出功能和用户手册。具体包括：PDF导出功能（补充现有JSON/CSV）、11个工具有完整说明书、API获取指南（Tronscan、Etherscan、Blockchain）。复用Phase 1-5的核心框架和导出模块。

**In scope:**
- PDF导出功能（WeasyPrint库，HTML转PDF）
- PDF导出按钮（所有11个工具统一提供）
- 用户手册首页（11个工具卡片展示）
- 11个工具详细说明书页面
- API密钥获取指南页面（Tronscan、Etherscan、Blockchain）
- 说明书内容：操作步骤、结果解释、API密钥说明、案例演示
- API指南内容：注册流程、使用限制、安全说明、问题排查

**Out of scope:**
- 多语言支持（仅中文）
- 视频教程
- 实时客服系统
- 用户反馈收集系统
- PDF模板定制功能

</domain>

<decisions>
## Implementation Decisions

### PDF导出功能
- **D-01:** PDF导出使用WeasyPrint库（HTML直接转PDF，风格与现有页面一致）
- **D-02:** PDF导出按钮在所有11个工具结果页面统一出现（与JSON/CSV并列）

### 用户手册组织
- **D-03:** 手册首页展示11个工具卡片，点击卡片进入详细说明书页面（需12个页面：首页+11详情）
- **D-04:** 每个工具说明书包含：操作步骤、结果解释、API密钥说明、案例演示

### API获取指南
- **D-05:** API密钥获取指南为独立页面（`/docs/api-guide`）
- **D-06:** API获取指南包含：注册流程、使用限制、安全说明、问题排查

### Claude's Discretion
- WeasyPrint安装脚本（Windows GTK依赖处理）
- PDF导出按钮具体样式设计
- 手册首页卡片布局细节
- 说明书页面模板设计
- API指南页面具体内容编写
- 侧边栏导航新增入口（手册、API指南）

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### Requirements
- `.planning/REQUIREMENTS.md` §EXPORT-03, DOC-01, DOC-02 — 导出和文档需求定义

### Existing Patterns (reference from Phase 1-5)
- `modules/core/exporter.py` — JSON/CSV导出功能（扩展PDF导出）
- `templates/base.html` — 基础模板（侧边栏、底部声明）
- `templates/index.html` — 首页卡片布局模式参考
- 各工具页面 `templates/tron/`, `templates/eth/`, `templates/trace/`, `templates/cross/`, `templates/case/` — 结果展示模式参考

### External Libraries
- WeasyPrint — https://weasyprint.org/ （HTML转PDF，需GTK）
- WeasyPrint Windows安装 — https://weasyprint.org/docs/install/#windows

### External APIs (for API Guide content)
- Tronscan API — https://api.tronscan.org/api（免费，无需密钥）
- Etherscan API V2 — https://api.etherscan.io/v2/api（需密钥，免费额度）
- Blockstream API — https://blockstream.info/api（免费，无需密钥）

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `modules/core/exporter.py` — JSON/CSV导出功能，可扩展PDF导出
- `templates/base.html` — 基础模板（侧边栏已有"使用手册"入口 `/docs/manuals`）
- `templates/index.html` — 首页卡片布局模式（4个分组），可复用于手册首页
- 各工具页面 — 结果展示模式，导出按钮位置参考

### Established Patterns
- Flask Blueprint modular architecture — 新增 `modules/docs/` 模块
- Card-based layout — 首页工具卡片，复用于手册首页
- Export button trio — JSON/CSV/按钮组合，扩展PDF按钮
- Sample filling button — 样本填充按钮，说明书需演示使用方法
- Tailwind CSS v4 CDN — 零构建样式，PDF导出需保持风格一致

### Integration Points
- `app.py` — 需注册新的docs blueprint
- `templates/docs/` — 新建文档页面目录（manuals.html, manual_*.html, api_guide.html）
- `modules/docs/` — 新建文档模块目录（routes.py, pdf_exporter.py）
- `templates/base.html` 侧边栏 — 已有 `/docs/manuals` 入口，需新增 `/docs/api-guide` 入口

</code_context>

<specifics>
## Specific Ideas

- PDF导出文件名格式：`{tool_name}_{address_short}_{date}.pdf`
- 手册首页每个卡片显示工具名称、简短描述、"查看详情"按钮
- 说明书页面使用统一模板（标题、工具图标、四部分内容）
- API指南页面分三个区块（Tronscan、Etherscan、Blockchain）
- Etherscan API指南需强调免费额度限制（5 calls/sec）
- 所有文档页面保持简洁风格，与现有工具页面一致

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 06-documentation-export*
*Context gathered: 2026-04-24*