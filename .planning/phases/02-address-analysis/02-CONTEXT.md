# Phase 2: Address Analysis Tools - Context

**Gathered:** 2026-04-24
**Status:** Ready for planning

<domain>
## Phase Boundary

完成TRON地址行为分析和ETH交易查询工具（含跨链桥识别）。构建两个新的链上分析工具，复用Phase 1的核心框架和模块。

**In scope:**
- TRON地址行为分析工具（资金来源、交易模式、地址关系、活动时间线）
- ETH交易查询工具（支持Stargate跨链桥检测）
- API密钥输入界面（不存储）
- JSON/CSV导出功能

**Out of scope:**
- 用户认证系统
- 数据持久化存储
- 云端部署
- 其他链（BTC、BSC等）支持

</domain>

<decisions>
## Implementation Decisions

### TRON Behavior Analysis
- **D-01:** 分析4种行为模式：首次资金来源、交易模式（入/出比例、频率）、地址关系（频繁交易对象）、活动时间线
- **D-02:** 结果展示采用Summary Cards格式，每个模式一个卡片，与suspicious analyzer保持一致风格

### ETH API Integration
- **D-03:** 使用Etherscan API（免费版限制：5次/秒，100,000次/天）
- **D-04:** API密钥每次查询时输入，不存储（符合ADDR-05要求）

### Stargate Bridge Detection
- **D-05:** 采用Known Contract Scan方法 — 检查ETH交易是否与已知Stargate合约交互
- **D-06:** 检测结果以卡片形式展示，包含跨链详情（源链、目标链、金额）

### UI Layout
- **D-07:** ETH工具界面与TRON suspicious analyzer保持一致布局（地址输入、分析按钮、结果展示）
- **D-08:** ETH交易结果采用Card-based alerts格式（与suspicious analyzer一致）
- **D-09:** TRON behavior analyzer结果采用Summary Cards格式

### Claude's Discretion
- Etherscan API具体endpoint选择
- Stargate已知合约地址列表（LayerZero官方文档）
- 错误处理和重试逻辑
- Loading状态展示细节

</decisions>

<canonical_refs>
## Canonical References

**Downstream agents MUST read these before planning or implementing.**

### TRON Behavior Analysis
- `.planning/REQUIREMENTS.md` §ADDR-03 — TRON地址行为分析需求定义
- `modules/tron/suspicious_analyzer.py` — 参考现有TRON分析模式（API调用、结果结构）
- `modules/core/api_client.py` — Tronscan API client可复用

### ETH API Integration
- `.planning/REQUIREMENTS.md` §ADDR-04, ADDR-05 — ETH交易查询和API密钥输入需求
- Etherscan API Documentation — https://docs.etherscan.io/（外部参考）

### Stargate Bridge Detection
- Stargate Official Docs — https://stargate.finance/（外部参考）
- LayerZero Protocol Docs — https://layerzero.network/（外部参考）

### UI Patterns
- `templates/base.html` — 基础模板复用（侧边栏、底部声明）
- `templates/tron/suspicious_analyzer.html` — 参考现有工具页面布局

</canonical_refs>

<code_context>
## Existing Code Insights

### Reusable Assets
- `modules/core/api_client.py` — Tronscan API client，可扩展为Etherscan client
- `modules/core/formatter.py` — 数据格式化工具
- `modules/core/exporter.py` — JSON/CSV导出功能
- `modules/tron/routes.py` — Flask Blueprint模式，可复用创建ETH blueprint
- `templates/base.html` — 基础模板（侧边栏、底部声明）

### Established Patterns
- Flask Blueprint modular architecture — 每个链一个模块
- Analysis pattern: structured result dict (success, address, basic_info, alerts)
- UI pattern: address input → analyze button → results cards

### Integration Points
- `app.py` — 需注册新的ETH blueprint
- `templates/tron/` — TRON behavior analyzer页面添加到此处
- `modules/eth/` — 新建ETH模块目录（routes.py, eth_analyzer.py）

</code_context>

<specifics>
## Specific Ideas

- TRON behavior analyzer应该显示"谁首次资助了这个地址"（追踪诈骗源头）
- ETH工具需要API密钥输入框，每次查询都要输入（不存储）
- Stargate检测应该显示：源链 → 目标链 → 金额 → 时间
- 界面保持简洁，与现有TRON suspicious analyzer风格一致

</specifics>

<deferred>
## Deferred Ideas

None — discussion stayed within phase scope.

</deferred>

---

*Phase: 02-address-analysis*
*Context gathered: 2026-04-24*