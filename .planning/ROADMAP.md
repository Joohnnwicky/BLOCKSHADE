# ROADMAP: Crypto Investigation Toolkit

**Project:** CIT
**Updated:** 2026-04-24
**Status:** Active

---

## Progress

| Milestone | Status | Phases | Progress |
|-----------|--------|--------|----------|
| v1 | ✅ Complete | 6/6 | 100% |

---

## Phases

### Phase 1: Core Framework
**Goal:** 构建Flask应用核心框架，包含基础模板、侧边栏导航、共享模块，以及第一个完整工具（TRON可疑特征分析）

**Status:** ✅ Complete
**Requirements:** CORE-01, CORE-02, CORE-03, CORE-04, CORE-05, ADDR-01, ADDR-02, EXPORT-01, EXPORT-02
**Plans:** 7 plans in 4 waves

**Success Criteria:**
- [x] run.bat双击可启动Flask应用
- [x] 首页显示工具概览和4个分组
- [x] 侧边栏导航正常切换
- [x] TRON可疑分析工具完整可用（样本填充、API调用、结果展示、导出）
- [x] 底部法律声明显示

**Key Files:**
- app.py (Flask入口)
- templates/base.html (侧边栏布局)
- modules/core/ (共享模块)
- modules/tron/suspicious_analyzer.py (TRON分析)

**Plan Details:**

| Wave | Plan | Objective | Requirements | Status |
|------|------|-----------|--------------|--------|
| 1 | [x] 01-01-PLAN.md | Base template with sidebar + footer | CORE-03, CORE-05 | DONE |
| 1 | [x] 01-02-PLAN.md | Core modules (API client, formatter, exporter) | EXPORT-01, EXPORT-02 | DONE |
| 2 | [x] 01-03-PLAN.md | Flask app + homepage with 4 categories | CORE-02 | DONE |
| 2 | [x] 01-04-PLAN.md | TRON analyzer backend (alerts + score) | ADDR-01, ADDR-02 | DONE |
| 3 | [x] 01-05-PLAN.md | TRON frontend page + sample loading | CORE-04 | DONE |
| 3 | [x] 01-06-PLAN.md | Startup scripts (run.bat/run.sh) | CORE-01 | DONE |
| 4 | [x] 01-07-PLAN.md | Final verification + integration | Verification only | DONE |

---

### Phase 2: Address Analysis Tools
**Goal:** 完成TRON地址行为分析和ETH交易查询工具（含跨链桥识别）

**Status:** ✅ Complete
**Requirements:** ADDR-03, ADDR-04, ADDR-05
**Plans:** 4 plans in 3 waves

**Success Criteria:**
- [x] TRON地址行为分析工具完整可用
- [x] ETH交易查询工具可查询全部交易
- [x] ETH工具可识别跨链桥（Stargate）事件
- [x] ETH工具支持API密钥输入

**Dependencies:** Phase 1 complete

**Plan Details:**

| Wave | Plan | Objective | Requirements | Status |
|------|------|-----------|--------------|--------|
| 1 | [x] 02-01-PLAN.md | TRON behavior analyzer backend + frontend | ADDR-03 | DONE |
| 1 | [x] 02-02-PLAN.md | ETH backend module (API + Stargate detector) | ADDR-04, ADDR-05 | DONE |
| 2 | [x] 02-03-PLAN.md | ETH frontend UI with API key input | ADDR-04, ADDR-05 | DONE |
| 3 | [x] 02-04-PLAN.md | Integration + end-to-end verification | ADDR-03, ADDR-04, ADDR-05 | DONE |

---

### Phase 3: Transaction Tracking Tools
**Goal:** 完成Uniswap追踪、混币器追踪、BTC交易分析工具

**Status:** ✅ Complete
**Requirements:** TRACE-01, TRACE-02, TRACE-03
**Plans:** 5 plans in 3 waves

**Success Criteria:**
- [x] Uniswap追踪可还原DEX交易路径
- [x] 混币器追踪可还原洗钱路径（集成到ETH页面）
- [x] BTC交易分析可查询比特币流向

**Dependencies:** Phase 2 complete

**Plan Details:**

| Wave | Plan | Objective | Requirements | Status |
|------|------|-----------|--------------|--------|
| 1 | [x] 03-01-PLAN.md | Backend: Uniswap tracker module with Web3 RPC client | TRACE-01 | DONE |
| 1 | [x] 03-02-PLAN.md | Backend: Tornado Cash mixer tracker with time window analysis | TRACE-02 | DONE |
| 2 | [x] 03-03-PLAN.md | Backend: BTC analyzer with Blockstream API | TRACE-03 | DONE |
| 2 | [x] 03-04-PLAN.md | Frontend: All three tool pages (uniswap.html, mixer.html, btc.html) | TRACE-01, TRACE-02, TRACE-03 | DONE |
| 3 | [x] 03-05-PLAN.md | Integration: Blueprint registration + mixer UX fix + session caching | TRACE-01, TRACE-02, TRACE-03 | DONE |

**Key Improvements (Session):**
- Mixer detection integrated into ETH page (always-visible card)
- Session caching for cross-module navigation (sessionStorage)
- Mixer entry removed from sidebar (access via ETH page only)

---

### Phase 4: Cross-Chain Analysis Tools
**Goal:** 完成地址聚类和跨境协查工具

**Status:** ✅ Complete
**Requirements:** CROSS-01, CROSS-02
**Plans:** 5 plans in 3 waves

**Success Criteria:**
- [x] 地址聚类可关联多个地址（4种聚类依据）
- [x] 跨境协查可生成国际协作模板（分步表单）

**Dependencies:** Phase 3 complete

**Plan Details:**

| Wave | Plan | Objective | Requirements | Status |
|------|------|-----------|--------------|--------|
| 1 | [x] 04-01-PLAN.md | Backend: Address clustering module (chain_detector, cluster_analyzer) | CROSS-01 | DONE |
| 1 | [x] 04-02-PLAN.md | Backend: Cross-border template generator module | CROSS-02 | DONE |
| 2 | [x] 04-03-PLAN.md | Frontend: Cluster page with multi-address input + API key handling | CROSS-01 | DONE |
| 2 | [x] 04-04-PLAN.md | Frontend: Cross-border page with step-by-step form | CROSS-02 | DONE |
| 3 | [x] 04-05-PLAN.md | Integration: Blueprint registration + export/import workflow | CROSS-01, CROSS-02 | DONE |

**Key Features:**
- 4 clustering heuristics: first funding source, mutual transfers, time window overlap, shared deposit
- Step-by-step template form (3 steps)
- Export from cluster -> import to cross-border workflow

---

### Phase 5: Case Handling Tools
**Goal:** 完成多链监控、混淆攻击对抗、资产追回冻结工具

**Status:** ✅ Complete
**Requirements:** CASE-01, CASE-02, CASE-03
**Plans:** 3 plans in 1 wave

**Success Criteria:**
- [x] 多链监控可手动刷新查看地址状态（余额、交易数、最后活跃）
- [x] 混淆对抗可识别4种攻击手法（三明治、闪电贷、粉尘、协议漏洞）
- [x] 资产追回可生成冻结申请模板（分步表单、文本复制）

**Dependencies:** Phase 4 complete

**Plan Details:**

| Wave | Plan | Objective | Requirements | Status |
|------|------|-----------|--------------|--------|
| 1 | [x] 05-01-PLAN.md | Multi-chain monitor tool (backend + frontend + exports) | CASE-01 | DONE |
| 1 | [x] 05-02-PLAN.md | Obfuscation attack detector tool (backend + frontend + exports) | CASE-02 | DONE |
| 1 | [x] 05-03-PLAN.md | Asset freeze template generator tool (backend + frontend + imports) | CASE-03 | DONE |

**Key Features:**
- Manual refresh trigger (no auto-polling) per D-01 to D-03
- TRON + ETH + BTC support for monitor
- ETH-only scope for attack detection per D-24
- 4 field categories for freeze template: case info, target info, reason info, terms info
- Tool interconnection via sessionStorage: monitor/cluster/obfuscation -> asset freeze

---

### Phase 6: Documentation & Export
**Goal:** 完善导出功能和用户手册

**Status:** ✅ Complete
**Requirements:** EXPORT-03, DOC-01, DOC-02
**Plans:** 6 plans in 4 waves

**Success Criteria:**
- [x] PDF导出功能完整可用
- [x] 11个工具有完整说明书
- [x] API获取指南（Tronscan、Etherscan、Blockchain）完整

**Dependencies:** Phase 5 complete

**Plan Details:**

| Wave | Plan | Objective | Requirements | Status |
|------|------|-----------|--------------|--------|
| 1 | [x] 06-01-PLAN.md | PDF export backend (WeasyPrint, exporter.py, docs Blueprint) | EXPORT-03 | DONE |
| 1 | [x] 06-02-PLAN.md | Manual homepage (manuals.html with 11 tool cards) | DOC-01 | DONE |
| 2 | [x] 06-03a-PLAN.md | PDF buttons on TRON/ETH tool templates | EXPORT-03 | DONE |
| 2 | [x] 06-03b-PLAN.md | PDF buttons on trace/cross/case tool templates | EXPORT-03 | DONE |
| 3 | [x] 06-04a-PLAN.md | Manual routes + API guide page + sidebar link | DOC-02 | DONE |
| 4 | [x] 06-04b-PLAN.md | 11 manual detail pages (4-section structure) | DOC-01 | DONE |

**Key Features:**
- WeasyPrint HTML-to-PDF export (per D-01)
- PDF button on all 11 tools (per D-02)
- 4-section manual structure (per D-04)
- API guide with 3 services (Tronscan free, Etherscan key required, Blockstream free)

---

## Coverage

- Total v1 Requirements: 22
- Mapped to Phases: 22
- Coverage: 100% ✓

## Requirements Traceability

| Phase 1 Plans | Requirements Covered |
|---------------|---------------------|
| 01-01-PLAN.md | CORE-03, CORE-05 |
| 01-02-PLAN.md | EXPORT-01, EXPORT-02 |
| 01-03-PLAN.md | CORE-02 |
| 01-04-PLAN.md | ADDR-01, ADDR-02 |
| 01-05-PLAN.md | CORE-04 |
| 01-06-PLAN.md | CORE-01 |

**Phase 1 Coverage:** 9/9 requirements ✓

| Phase 2 Plans | Requirements Covered |
|---------------|---------------------|
| 02-01-PLAN.md | ADDR-03 |
| 02-02-PLAN.md | ADDR-04, ADDR-05 |
| 02-03-PLAN.md | ADDR-04, ADDR-05 |
| 02-04-PLAN.md | ADDR-03, ADDR-04, ADDR-05 |

**Phase 2 Coverage:** 3/3 requirements ✓

| Phase 3 Plans | Requirements Covered |
|---------------|---------------------|
| 03-01-PLAN.md | TRACE-01 |
| 03-02-PLAN.md | TRACE-02 |
| 03-03-PLAN.md | TRACE-03 |
| 03-04-PLAN.md | TRACE-01, TRACE-02, TRACE-03 |
| 03-05-PLAN.md | TRACE-01, TRACE-02, TRACE-03 |

**Phase 3 Coverage:** 3/3 requirements ✓

| Phase 4 Plans | Requirements Covered |
|---------------|---------------------|
| 04-01-PLAN.md | CROSS-01 |
| 04-02-PLAN.md | CROSS-02 |
| 04-03-PLAN.md | CROSS-01 |
| 04-04-PLAN.md | CROSS-02 |
| 04-05-PLAN.md | CROSS-01, CROSS-02 |

**Phase 4 Coverage:** 2/2 requirements ✓

| Phase 5 Plans | Requirements Covered |
|---------------|---------------------|
| 05-01-PLAN.md | CASE-01 |
| 05-02-PLAN.md | CASE-02 |
| 05-03-PLAN.md | CASE-03 |

**Phase 5 Coverage:** 3/3 requirements ✓

| Phase 6 Plans | Requirements Covered |
|---------------|---------------------|
| 06-01-PLAN.md | EXPORT-03 |
| 06-02-PLAN.md | DOC-01 |
| 06-03a-PLAN.md | EXPORT-03 |
| 06-03b-PLAN.md | EXPORT-03 |
| 06-04a-PLAN.md | DOC-02 |
| 06-04b-PLAN.md | DOC-01 |

**Phase 6 Coverage:** 3/3 requirements ✓

---

*Updated: 2026-04-24 after Phase 6 plan revision (split 06-03/06-04 for scope sanity)*