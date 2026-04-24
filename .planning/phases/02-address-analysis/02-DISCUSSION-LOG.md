# Phase 2: Address Analysis Tools - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-24
**Phase:** 02-address-analysis
**Areas discussed:** TRON behavior patterns, ETH API integration, Stargate bridge detection, UI layout

---

## TRON Behavior Patterns

| Option | Description | Selected |
|--------|-------------|----------|
| First funding source | Identify first funding source(s) — who sent initial TRX/USDT | ✓ |
| Transfer patterns | Calculate in/out ratio, average amounts, transfer frequency | ✓ |
| Address relationships | Build graph of connected addresses (frequent senders/receivers) | ✓ |
| Activity timeline | Address age vs first transaction, peak activity, dormancy | ✓ |

**User's choice:** All 4 patterns selected
**Notes:** Behavior analysis differs from suspicious analysis (fraud indicators) — focuses on usage patterns and relationships

---

## ETH Blockchain API

| Option | Description | Selected |
|--------|-------------|----------|
| Etherscan API | Free tier: 5 calls/sec, 100K/day. Industry standard | ✓ |
| Blockscout API | Ethereum Foundation's official explorer. No rate limits | |
| Dual fallback | Etherscan primary, Blockscout secondary on errors | |

**User's choice:** Etherscan API (Recommended)
**Notes:** Most reliable, well-documented, sufficient for project needs

---

## API Key Handling

| Option | Description | Selected |
|--------|-------------|----------|
| Per-query input | User enters API key each query. No persistence | ✓ |
| Session-level storage | Store in sessionStorage during session | |
| Page-level storage | Store in JS variable until page refresh | |

**User's choice:** Per-query input (Recommended)
**Notes:** Meets ADDR-05 requirement exactly — no storage

---

## Stargate Bridge Detection

| Option | Description | Selected |
|--------|-------------|----------|
| Known contract scan | Check transactions against known Stargate contracts | ✓ |
| Event log parsing | Parse LayerZero event signatures from logs | |
| Method signature matching | Match function selectors against Stargate patterns | |

**User's choice:** Known contract scan (Recommended)
**Notes:** Detects most bridge events, simpler implementation

---

## ETH Tool UI Layout

| Option | Description | Selected |
|--------|-------------|----------|
| Match TRON analyzer | Same layout — address input, button, results below | ✓ |
| Split-panel layout | Input on left, results on right | |
| Accordion sections | Collapsible sections for each analysis type | |

**User's choice:** Match TRON analyzer (Recommended)
**Notes:** Consistent UX across tools

---

## ETH Results Display

| Option | Description | Selected |
|--------|-------------|----------|
| Card-based alerts | Same as suspicious analyzer — cards for alerts | ✓ |
| Table + cards | Table for transaction list, cards for events | |
| Timeline visualization | Visual transaction flow | |

**User's choice:** Card-based alerts (Recommended)
**Notes:** Familiar to users from Phase 1

---

## TRON Behavior Results

| Option | Description | Selected |
|--------|-------------|----------|
| Summary cards | One card per pattern (funding, patterns, relationships, timeline) | ✓ |
| Table + cards | Table for transfer list, cards for patterns | |
| Visual relationship graph | HTML/CSS graph showing connected addresses | |

**User's choice:** Summary cards (Recommended)
**Notes:** Clean, consistent with existing tool

---

## Claude's Discretion

Areas where Claude has flexibility during planning/implementation:
- Etherscan API具体endpoint选择
- Stargate已知合约地址列表
- 错误处理和重试逻辑
- Loading状态展示细节

---

## Deferred Ideas

None — discussion stayed within phase scope.