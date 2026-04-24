# Phase 2: Address Analysis Tools - Research

**Researched:** 2026-04-24
**Domain:** TRON behavior analysis, ETH transaction queries, Stargate bridge detection
**Confidence:** HIGH

## Summary

Phase 2 implements two new blockchain analysis tools: TRON behavior analyzer (4 behavior patterns) and ETH transaction query tool with Stargate cross-chain bridge detection. Both tools follow established patterns from Phase 1's TRON suspicious analyzer - Flask Blueprint architecture, card-based UI, JSON/CSV export.

**Primary recommendation:** Extend existing `modules/core/api_client.py` for ETH/Etherscan support, create new `modules/eth/` package mirroring TRON structure, reuse card-based UI pattern from `templates/tron/suspicious_analyzer.html`.

<user_constraints>
## User Constraints (from CONTEXT.md)

### Locked Decisions
- **D-01:** TRON behavior分析4种行为模式：首次资金来源、交易模式（入/出比例、频率）、地址关系（频繁交易对象）、活动时间线
- **D-02:** 结果展示采用Summary Cards格式，每个模式一个卡片，与suspicious analyzer保持一致风格
- **D-03:** 使用Etherscan API（免费版限制：5次/秒，100,000次/天）
- **D-04:** API密钥每次查询时输入，不存储（符合ADDR-05要求）
- **D-05:** Stargate检测采用Known Contract Scan方法 — 检查ETH交易是否与已知Stargate合约交互
- **D-06:** 检测结果以卡片形式展示，包含跨链详情（源链、目标链、金额）
- **D-07:** ETH工具界面与TRON suspicious analyzer保持一致布局（地址输入、分析按钮、结果展示）
- **D-08:** ETH交易结果采用Card-based alerts格式（与suspicious analyzer一致）
- **D-09:** TRON behavior analyzer结果采用Summary Cards格式

### Claude's Discretion
- Etherscan API具体endpoint选择
- Stargate已知合约地址列表（LayerZero官方文档）
- 错误处理和重试逻辑
- Loading状态展示细节

### Deferred Ideas (OUT OF SCOPE)
None — discussion stayed within phase scope.
</user_constraints>

<phase_requirements>
## Phase Requirements

| ID | Description | Research Support |
|----|-------------|------------------|
| ADDR-03 | User can analyze TRON address behavior patterns | Tronscan API endpoints documented; behavior analysis algorithms defined |
| ADDR-04 | User can query ETH address transactions with cross-chain bridge detection | Etherscan API endpoints documented; Stargate contract addresses verified |
| ADDR-05 | User inputs API key manually (not stored by application) | Per-query API key input pattern from locked decision D-04 |
</phase_requirements>

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| TRON API calls | Backend (Python) | — | Tronscan API requires server-side HTTP requests |
| TRON behavior analysis | Backend (Python) | — | Algorithmic processing of transfer history |
| ETH API calls | Backend (Python) | — | Etherscan API requires server-side HTTP requests with apikey |
| Stargate detection | Backend (Python) | — | Contract address matching requires transaction parsing |
| API key input | Frontend (HTML/JS) | Backend (validation) | User enters key in form, backend validates before API call |
| Results display | Frontend (HTML/JS) | — | Card-based UI pattern established in Phase 1 |
| JSON/CSV export | Backend (Python) | Frontend (download trigger) | Exporter module already handles formatting |

## Standard Stack

### Core (Reuse from Phase 1)

| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Flask | 3.0+ | Web framework | Established in Phase 1, Blueprint pattern working |
| requests | 2.31+ | HTTP client | Used in api_client.py, reliable for API calls |
| Tailwind CSS | 4.x CDN | Styling | Zero-build, consistent UI |

### New Dependencies

| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| — | — | No new Python packages required | Existing modules cover all needs |

**Version verification:**
```bash
# Existing packages confirmed working in Phase 1
pip show flask requests
```

## Architecture Patterns

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                      Browser / Client                           │
│  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐             │
│  │ TRON Behavior│  │ ETH Query   │  │ API Key     │             │
│  │ Input Form   │  │ Input Form  │  │ Input Field │             │
│  └──────┬──────┘  └──────┬──────┘  └──────┬──────┘             │
│         │                │                │                     │
│         ▼                ▼                ▼                     │
│  [AJAX POST /api/analyze]  [AJAX POST /api/query]              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    Flask Backend (app.py)                       │
│  ┌─────────────────────────┐  ┌─────────────────────────┐      │
│  │ tron_bp (Blueprint)     │  │ eth_bp (Blueprint)      │      │
│  │ - /api/behavior         │  │ - /api/query            │      │
│  │ - /api/export           │  │ - /api/export           │      │
│  └──────┬──────────────────┘  └──────┬──────────────────┘      │
│         │                           │                           │
│         ▼                           ▼                           │
┌─────────────────────────────────────────────────────────────────┐
│                    Core Modules                                 │
│  ┌──────────────────┐  ┌──────────────────┐  ┌───────────────┐ │
│  │ api_client.py    │  │ formatter.py     │  │ exporter.py   │ │
│  │ - Tronscan calls │  │ - Timestamp fmt  │  │ - JSON export │ │
│  │ - Etherscan calls│  │ - Amount fmt     │  │ - CSV export  │ │
│  └──────┬───────────┘  └──────────────────┘  └───────────────┘ │
│         │                                                       │
│         ▼                                                       │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │ tron/behavior_analyzer.py                                 │  │
│  │ eth/eth_analyzer.py                                       │  │
│  │ eth/stargate_detector.py                                  │  │
│  └──────────────────────────────────────────────────────────┘  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                    External APIs                                │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │ Tronscan API     │         │ Etherscan API    │             │
│  │ api.tronscan.org │         │ api.etherscan.io │             │
│  │ - /account       │         │ - module=account │             │
│  │ - /token_trc20   │         │ - action=txlist  │             │
│  │ - /transfers     │         │ - action=tokentx │             │
│  └──────┬───────────┘         └──────┬───────────┘             │
│         │                            │                         │
│         ▼                            ▼                         │
│  [Transfer History]          [Transaction List + Stargate]    │
│  [First Funding]             [Cross-chain Event Detection]    │
└─────────────────────────────────────────────────────────────────┘
```

### Recommended Project Structure

```
modules/
├── core/
│   ├── api_client.py      # Extend with Etherscan functions
│   ├── formatter.py       # Reuse (already has timestamp/amount formatting)
│   └── exporter.py        # Reuse (JSON/CSV export working)
├── tron/
│   ├── suspicious_analyzer.py  # Existing (Phase 1)
│   ├── behavior_analyzer.py    # NEW - 4 behavior patterns
│   └── routes.py              # Extend with behavior endpoint
├── eth/                    # NEW package
│   ├── __init__.py
│   ├── eth_analyzer.py     # Transaction query + analysis
│   ├── stargate_detector.py # Known contract scan logic
│   └── routes.py           # Blueprint for ETH endpoints
templates/
├── base.html               # Reuse
├── tron/
│   ├── suspicious_analyzer.html  # Existing
│   └── behavior_analyzer.html    # NEW - 4 card layout
├── eth/
│   └── transaction_query.html    # NEW - API key input + results
```

### Pattern 1: TRON Behavior Analysis Algorithm

**What:** Analyze 4 behavior patterns from transfer history
**When to use:** ADDR-03 requirement implementation

**Behavior Pattern Detection:**

```python
# Source: Adapted from existing suspicious_analyzer.py patterns
# VERIFIED: Tronscan API endpoint in modules/core/api_client.py

def analyze_first_funding_source(address: str, transfers: List[Dict]) -> Dict:
    """Find first address that sent funds to this address.
    
    Returns: {
        'funder_address': str,
        'first_transfer_time': timestamp,
        'first_amount': float,
        'funder_tx_count': int  # How many other transfers from this funder
    }
    """
    # Sort transfers by timestamp ascending
    # Find first incoming transfer (to_address == address)
    # Return funder details
    
def analyze_transfer_patterns(address: str, transfers: List[Dict]) -> Dict:
    """Calculate in/out ratio and frequency.
    
    Returns: {
        'total_in': float,
        'total_out': float,
        'in_out_ratio': float,
        'avg_transfer_interval_hours': float,
        'transfer_count_in': int,
        'transfer_count_out': int
    }
    """
    
def analyze_address_relationships(address: str, transfers: List[Dict]) -> Dict:
    """Identify frequently interacting addresses.
    
    Returns: {
        'top_counterparties': [
            {'address': str, 'interaction_count': int, 'total_amount': float}
        ],
        'unique_addresses_interacted': int
    }
    """
    
def analyze_activity_timeline(address: str, transfers: List[Dict]) -> Dict:
    """Build activity timeline.
    
    Returns: {
        'first_activity': timestamp,
        'last_activity': timestamp,
        'active_days': int,
        'peak_activity_period': {'start': date, 'end': date, 'count': int}
    }
    """
```

### Pattern 2: Etherscan API Integration

**What:** Query ETH transaction history with per-query API key
**When to use:** ADDR-04 requirement implementation

**API Endpoint Details [CITED: WebSearch results]:**

| Endpoint | URL | Parameters |
|----------|-----|------------|
| Normal Transactions | `api.etherscan.io/api` | `module=account&action=txlist&address={addr}&apikey={key}` |
| ERC20 Transfers | `api.etherscan.io/api` | `module=account&action=tokentx&address={addr}&apikey={key}` |

**Query Parameters:**
| Parameter | Required | Description |
|-----------|----------|-------------|
| module | yes | `account` |
| action | yes | `txlist` or `tokentx` |
| address | yes | ETH address (0x...) |
| apikey | yes | User-provided API key |
| startblock | optional | Starting block (default 0) |
| endblock | optional | Ending block (default 99999999) |
| page | optional | Page number (default 1) |
| offset | optional | Records per page (max 10000) |
| sort | optional | `asc` or `desc` |

**Response Fields [CITED: WebSearch results]:**
- `blockNumber`, `timeStamp`, `hash`, `from`, `to`, `value`
- `gas`, `gasUsed`, `gasPrice`, `isError`
- `contractAddress` (for contract creation)
- For tokentx: `tokenSymbol`, `tokenName`, `tokenDecimal`

**Rate Limits [CITED: Etherscan documentation]:**
- Free tier: 5 calls/second, 100,000 calls/day

**API Client Pattern:**

```python
# Source: Adapted from modules/core/api_client.py pattern
ETHERSCAN_BASE = "https://api.etherscan.io/api"

def get_eth_transactions(address: str, api_key: str, limit: int = 100) -> List[Dict]:
    """Get normal ETH transactions for address.
    
    Args:
        address: ETH address (0x prefix)
        api_key: User-provided Etherscan API key (per-query)
        limit: Max transactions to fetch
        
    Returns:
        List of transaction dicts with standard fields
    """
    params = {
        "module": "account",
        "action": "txlist",
        "address": address,
        "apikey": api_key,
        "page": 1,
        "offset": limit,
        "sort": "desc"
    }
    
    response = requests.get(ETHERSCAN_BASE, params=params, timeout=10)
    data = response.json()
    
    if data.get('status') != '1':
        return []  # API error or no transactions
    
    return data.get('result', [])
```

### Pattern 3: Stargate Bridge Detection

**What:** Known Contract Scan - check if transaction interacts with Stargate
**When to use:** ADDR-04 cross-chain detection requirement

**Stargate Contract Addresses [VERIFIED: GitBook documentation]:**

| Contract | Address | Purpose |
|----------|---------|---------|
| Router | `0x8731d54E9D02c286767d56ac03e8037C07e01e98` | Main routing interface |
| RouterETH | `0x150f94B44927F078737562f0fcF3C95c01Cc2376` | Native ETH swaps |
| Bridge | `0x296F55F8Fb28E498B858d0BcDA06D955B2Cb3f97` | LayerZero messaging |
| Factory | `0x06D538690AF257Da524f25D0CD52fD85b1c2173E` | Pool creation |
| Pool (ETH) | `0x101816545F6bd2b1076434B54383a1E633390A2E` | ETH liquidity |
| Pool (USDC) | `0xdf0770dF86a8034b3EFEf0A1Bb3c889B8332FF56` | USDC liquidity |
| Pool (USDT) | `0x38EA452219524Bb87e18dE1C24D3bB59510BD783` | USDT liquidity |

**Detection Algorithm:**

```python
# Source: Known contract scan pattern
STARGATE_CONTRACTS = {
    'router': '0x8731d54E9D02c286767d56ac03e8037C07e01e98',
    'router_eth': '0x150f94B44927F078737562f0fcF3C95c01Cc2376',
    'bridge': '0x296F55F8Fb28E498B858d0BcDA06D955B2Cb3f97',
    'pools': [
        '0x101816545F6bd2b1076434B54383a1E633390A2E',  # ETH
        '0xdf0770dF86a8034b3EFEf0A1Bb3c889B8332FF56',  # USDC
        '0x38EA452219524Bb87e18dE1C24D3bB59510BD783',  # USDT
    ]
}

def detect_stargate_bridge(transactions: List[Dict]) -> List[Dict]:
    """Scan transactions for Stargate bridge interactions.
    
    Returns: [
        {
            'tx_hash': str,
            'contract_type': str,  # 'router', 'pool', etc.
            'from_chain': str,     # Always 'ETH' for this tool
            'to_chain': str,       # Derived from destination chainId
            'amount': float,
            'timestamp': timestamp,
            'token': str           # USDC, USDT, ETH
        }
    ]
    """
    bridge_events = []
    
    for tx in transactions:
        to_address = tx.get('to', '').lower()
        
        # Check if transaction target is a known Stargate contract
        for name, addr in STARGATE_CONTRACTS.items():
            if isinstance(addr, list):
                if to_address in [a.lower() for a in addr]:
                    bridge_events.append({
                        'tx_hash': tx['hash'],
                        'contract_type': f'pool_{name}',
                        # ... extract details from tx input data
                    })
            elif to_address == addr.lower():
                bridge_events.append({
                    'tx_hash': tx['hash'],
                    'contract_type': name,
                    # ... parse cross-chain details
                })
    
    return bridge_events
```

### Anti-Patterns to Avoid

- **Storing API keys:** Never store API key in session, cookie, or local storage - pass per-request only
- **Hardcoded rate limits:** Free tier limits may change - add user-visible error for rate limit hits
- **Assuming all transfers are TRC20:** ETH has both normal tx and ERC20 - query both endpoints
- **Ignoring isError field:** Failed transactions should be filtered or flagged
- **Missing validation:** ETH address must match `0x[a-fA-F0-9]{40}` pattern

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Timestamp formatting | Custom datetime parsing | `formatter.py::format_timestamp()` | Already handles milliseconds |
| Amount formatting | Division by decimals | `formatter.py::format_amount()` | Handles USDT 6 decimals |
| JSON export | Custom JSON serialization | `exporter.py::export_json()` | Preserves Chinese characters |
| CSV export | Manual CSV writing | `exporter.py::export_csv()` | Standardized column format |
| API request errors | Custom error handling | Standard requests exceptions + Flask error handler | Consistent error display |
| Address validation | Regex from scratch | Copy from `suspicious_analyzer.py::is_valid_tron_address()` pattern | Add ETH version |

**Key insight:** All core utilities exist - extend api_client.py, reuse formatter/exporter, copy UI patterns.

## Common Pitfalls

### Pitfall 1: Etherscan API Key Not Provided
**What goes wrong:** User forgets API key, gets generic error
**Why it happens:** Free tier requires API key for all endpoints
**How to avoid:** Show helpful placeholder text: "从 etherscan.io 获取免费API密钥"
**Warning signs:** API returns status='0' with message='Invalid API Key'

### Pitfall 2: Rate Limit Exceeded
**What goes wrong:** 5 calls/second limit hit during testing
**Why it happens:** Free tier is strict, no burst allowance
**How to avoid:** Add 200ms delay between sequential calls, show error when hit
**Warning signs:** API returns status='0' with message='Max rate limit reached'

### Pitfall 3: ETH Address Format Validation
**What goes wrong:** User enters TRON address in ETH tool
**Why it happens:** Both tools on same sidebar, easy to confuse
**How to avoid:** Validate `0x` prefix + 40 hex chars, show clear error
**Warning signs:** Address doesn't match `^0x[a-fA-F0-9]{40}$`

### Pitfall 4: Stargate Detection False Negatives
**What goes wrong:** Misses bridge transfers through intermediary
**Why it happens:** Some users route through aggregators before Stargate
**How to avoid:** Known Contract Scan is simple but limited - document limitation
**Warning signs:** User expects bridge activity but tool shows none

### Pitfall 5: Missing First Funding Source
**What goes wrong:** TRON behavior analyzer shows "未知" for funding source
**Why it happens:** Address has no incoming transfers, or API returned empty list
**How to avoid:** Check for empty transfer list before processing, show "无转入记录"
**Warning signs:** Transfer count is 0 but address exists

## Code Examples

### TRON Behavior Analyzer Entry Point

```python
# Source: Adapted from modules/tron/suspicious_analyzer.py pattern
def analyze_behavior_web(address: str) -> Dict[str, Any]:
    """Web-friendly wrapper for TRON behavior analysis.
    
    Returns:
        dict with keys:
            - success: bool
            - address: str
            - behaviors: dict with 4 pattern results
            - error: str (if success=False)
    """
    if not is_valid_tron_address(address):
        return {
            'success': False,
            'address': address,
            'error': '无效的TRON地址格式',
            'behaviors': None
        }
    
    # Get transfer history (reuse existing function)
    transfers = get_trc20_transfers(address, limit=100)
    
    if not transfers:
        return {
            'success': True,
            'address': address,
            'behaviors': {
                'funding_source': {'status': '无转入记录'},
                'transfer_patterns': {'status': '无交易记录'},
                'relationships': {'status': '无交易对象'},
                'timeline': {'status': '无活动记录'}
            }
        }
    
    # Analyze 4 patterns
    behaviors = {
        'funding_source': analyze_first_funding_source(address, transfers),
        'transfer_patterns': analyze_transfer_patterns(address, transfers),
        'relationships': analyze_address_relationships(address, transfers),
        'timeline': analyze_activity_timeline(address, transfers)
    }
    
    return {
        'success': True,
        'address': address,
        'behaviors': behaviors
    }
```

### ETH Transaction Query with API Key

```python
# Source: New pattern based on api_client.py structure
def query_eth_transactions_web(address: str, api_key: str) -> Dict[str, Any]:
    """Query ETH transactions with user-provided API key.
    
    Args:
        address: ETH address (0x...)
        api_key: User's Etherscan API key (per-query input)
        
    Returns:
        dict with keys:
            - success: bool
            - address: str
            - transactions: list
            - stargate_events: list
            - error: str (if success=False)
    """
    if not is_valid_eth_address(address):
        return {
            'success': False,
            'address': address,
            'error': '无效的ETH地址格式（应以0x开头，42位字符）',
            'transactions': None,
            'stargate_events': None
        }
    
    if not api_key or len(api_key) < 20:
        return {
            'success': False,
            'address': address,
            'error': '请输入有效的Etherscan API密钥',
            'transactions': None,
            'stargate_events': None
        }
    
    # Query normal transactions
    transactions = get_eth_transactions(address, api_key, limit=50)
    
    # Query ERC20 token transfers
    erc20_transfers = get_erc20_transfers(address, api_key, limit=50)
    
    # Combine and detect Stargate
    all_txs = transactions + erc20_transfers
    stargate_events = detect_stargate_bridge(all_txs)
    
    return {
        'success': True,
        'address': address,
        'transactions': {
            'normal': transactions,
            'erc20': erc20_transfers,
            'total_count': len(all_txs)
        },
        'stargate_events': stargate_events
    }
```

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Manual API key config file | Per-query input field | Phase 2 D-04 | No key storage, better security |
| Single transaction list | Combined normal + ERC20 | Current | Complete history coverage |
| Simple address check | Known Contract Scan | Current | Basic bridge detection |

**Deprecated/outdated:**
- Hardcoded API keys: Replaced by per-query input per ADDR-05
- Separate pages for normal/ERC20: Combined in single tool

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | Stargate contract addresses stable | Pattern 3 | Addresses may change - verify before implementation |
| A2 | Etherscan free tier sufficient | Pattern 2 | User may exceed 100K/day limit - show rate limit error |
| A3 | 100 transfers sufficient for behavior analysis | Pattern 1 | May miss historical patterns - increase limit if needed |

## Open Questions

1. **Stargate destination chain extraction**
   - What we know: Router contract has swap() function with chainId parameter
   - What's unclear: How to decode chainId from transaction input data
   - Recommendation: Check Stargate ABI for swap() function signature, parse input data

2. **LayerZero event parsing**
   - What we know: PacketSent event emitted for cross-chain messages
   - What's unclear: Whether event appears in Etherscan transaction logs
   - Recommendation: Test with known Stargate transaction, check if event accessible via API

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Flask | Backend | ✓ | 3.0+ | — |
| requests | API calls | ✓ | 2.31+ | — |
| Etherscan API | ETH queries | External | Free tier | — |
| Tronscan API | TRON queries | External | Public | — |
| Internet access | API calls | Required | — | Tool unusable if blocked |

**Missing dependencies with no fallback:**
- None - all dependencies verified

**Missing dependencies with fallback:**
- None

## Security Domain

> Required per security_enforcement default (enabled).

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | Single-user local tool |
| V3 Session Management | no | No sessions, per-query API key |
| V4 Access Control | no | Local tool, no auth |
| V5 Input Validation | yes | Address format regex validation |
| V6 Cryptography | no | No encryption, API keys transient |

### Known Threat Patterns for Flask + External API

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| API key exposure in logs | Information Disclosure | Never log API key, pass directly to API |
| XSS via address input | Tampering | Escape HTML in address display (Jinja2 auto-escape) |
| SSRF via malformed address | Tampering | Validate address format before API call |
| Rate limit exhaustion | Denial of Service | Show error, don't retry automatically |

## Sources

### Primary (HIGH confidence)
- `modules/core/api_client.py` - Tronscan API pattern verified in codebase [VERIFIED]
- `modules/tron/suspicious_analyzer.py` - Analysis pattern verified in codebase [VERIFIED]
- `templates/tron/suspicious_analyzer.html` - UI pattern verified in codebase [VERIFIED]
- Stargate GitBook - Contract addresses extracted from `llms-full.txt` [CITED: https://stargateprotocol.gitbook.io/stargate]
- Etherscan documentation - API endpoint structure [CITED: WebSearch results]

### Secondary (MEDIUM confidence)
- LayerZero event signatures [CITED: WebSearch results]

### Tertiary (LOW confidence)
- Stargate swap() function parameter parsing - needs ABI verification [ASSUMED]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - All patterns exist in codebase
- Architecture: HIGH - Blueprint pattern established, modular extension clear
- Pitfalls: HIGH - Based on Phase 1 experience + API documentation

**Research date:** 2026-04-24
**Valid until:** 30 days (Stargate addresses may update)