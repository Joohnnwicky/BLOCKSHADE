# Phase 1: Core Framework - Research

**Researched:** 2026-04-23
**Domain:** Flask web application framework, TRON blockchain API, Tailwind CSS
**Confidence:** HIGH

## Summary

This phase establishes the foundation for a cryptocurrency investigation toolkit web application. The project converts existing Python training scripts into a unified Flask web interface with Tailwind CSS styling. The core challenge is adapting CLI-based Python analysis scripts to a web context while maintaining zero-config local startup.

**Primary recommendation:** Use Flask 3.1.3 with Blueprint-based modular architecture, Tailwind CSS v4 via CDN (no build step), and adapt existing `001-day1-TRON地址可疑特征分析工具.py` script logic into Flask route handlers returning JSON for frontend rendering.

## Architectural Responsibility Map

| Capability | Primary Tier | Secondary Tier | Rationale |
|------------|-------------|----------------|-----------|
| Address analysis logic | Backend (Flask/Python) | - | Complex scoring algorithm, API orchestration belongs in Python |
| Tronscan API calls | Backend | - | HTTP requests, data transformation, rate limiting handled server-side |
| Sidebar navigation | Frontend (HTML/Tailwind) | Frontend Server (Flask templates) | Static navigation rendered in base template |
| Template rendering | Frontend Server (Flask templates) | - | Jinja2 inheritance pattern for page composition |
| Risk score calculation | Backend | - | Algorithm from existing script, 0-100 scoring logic |
| JSON/CSV export | Backend | - | Python `json` module (built-in), `csv` module (built-in) for file generation |
| Sample data loading | Frontend Server | Backend | Button triggers backend to return sample address data |
| Legal disclaimer | Frontend Server | - | Static footer in base template, all pages inherit |

## Standard Stack

### Core
| Library | Version | Purpose | Why Standard |
|---------|---------|---------|--------------|
| Flask | 3.1.3 | Web framework | Python microframework, minimal setup, Jinja2 built-in [VERIFIED: pip index] |
| Tailwind CSS | 4.2 (CDN) | CSS styling | Zero-build styling via CDN, rapid prototyping [VERIFIED: tailwindcss.com] |
| requests | 2.32.5 | HTTP client | Already installed, used in existing scripts [VERIFIED: pip show] |

### Supporting
| Library | Version | Purpose | When to Use |
|---------|---------|---------|-------------|
| Jinja2 | (Flask bundled) | Template engine | All HTML rendering via template inheritance |
| Werkzeug | (Flask bundled) | WSGI utilities | Development server, routing |
| json | (built-in) | JSON export | EXPORT-01 requirement |
| csv | (built-in) | CSV export | EXPORT-02 requirement |
| datetime | (built-in) | Time handling | Address creation time analysis |

### Alternatives Considered
| Instead of | Could Use | Tradeoff |
|------------|-----------|----------|
| Tailwind CDN | Tailwind CLI build | CDN: faster setup, no customization; CLI: full config, requires build |
| Flask | Django | Flask: minimal, fits single-app need; Django: overkill for 11 tools |
| requests | httpx | requests: already installed, familiar; httpx: async, unnecessary here |

**Installation:**
```bash
pip install Flask==3.1.3
```

**Note:** requests, pandas already installed. Tailwind CSS requires no pip install (CDN only).

**Version verification:**
- Flask 3.1.3 - verified via `pip index versions Flask` [VERIFIED: 2026-04-23]
- requests 2.32.5 - verified via `pip show requests` [VERIFIED: 2026-04-23]
- pandas 3.0.1 - verified via `pip show pandas` [VERIFIED: 2026-04-23]

## Architecture Patterns

### System Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                         User Browser                                 │
│  ┌─────────────┐    ┌─────────────┐    ┌─────────────────────────┐  │
│  │ Homepage    │    │ Tool Pages  │    │ Analysis Results       │  │
│  │ (overview)  │───▶│ (sidebar)   │───▶│ (alerts + score)       │  │
│  └─────────────┘    └─────────────┘    └─────────────────────────┘  │
│         │                  │                      │                  │
│         ▼                  ▼                      ▼                  │
│  ┌──────────────────────────────────────────────────────────────┐   │
│  │                 Flask Application (app.py)                   │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────────────────┐  │   │
│  │  │ Routes     │  │ Templates  │  │ modules/tron/          │  │   │
│  │  │ (Blueprint)│  │ (Jinja2)   │  │ suspicious_analyzer.py │  │   │
│  │  └────────────┘  └────────────┘  └────────────────────────┘  │   │
│  │         │               │                    │               │   │
│  │         ▼               ▼                    ▼               │   │
│  │  ┌──────────────────────────────────────────────────────┐   │   │
│  │  │            modules/core/ (shared utilities)          │   │   │
│  │  │  api_client.py │ formatter.py │ exporter.py         │   │   │
│  │  └──────────────────────────────────────────────────────┘   │   │
│  └─────────────────────────────────────────────────────────────┘   │
│                              │                                      │
│                              ▼                                      │
│  ┌─────────────────────────────────────────────────────────────┐   │
│  │                    Tronscan API                              │   │
│  │  apilist.tronscanapi.com/api/accountv2                       │   │
│  │  apilist.tronscanapi.com/api/token_trc20/transfers          │   │
│  └─────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────┘
```

### Recommended Project Structure
```
J:/虚拟币犯罪调查工具集/docs/superpowers/
├── app.py                    # Flask entry point, Blueprint registration
├── run.bat                   # Windows startup script
├── run.sh                    # Linux/Mac startup script
├── templates/
│   ├── base.html             # Sidebar layout, legal disclaimer footer
│   ├── index.html            # Homepage with 4 tool groups
│   └── tron/
│       └── suspicious_analyzer.html  # TRON analysis tool page
├── static/
│   └── css/                  # Optional custom CSS (Tailwind handles most)
├── modules/
│   ├── core/
│   │   ├── __init__.py
│   │   ├── api_client.py     # Shared API request handler
│   │   ├── formatter.py      # Data formatting utilities
│   │   └── exporter.py       # JSON/CSV export functions
│   └── tron/
│       ├── __init__.py
│       └── suspicious_analyzer.py  # Adapted from 001-day1 script
└── requirements.txt          # Flask dependency
```

### Pattern 1: Flask Blueprint Modular Architecture
**What:** Organize tools into separate Blueprint modules for maintainability
**When to use:** Multi-tool application with distinct features per tool
**Example:**
```python
# modules/tron/routes.py
from flask import Blueprint, render_template, request, jsonify

tron_bp = Blueprint('tron', __name__, url_prefix='/tron')

@tron_bp.route('/suspicious-analyzer')
def suspicious_analyzer_page():
    return render_template('tron/suspicious_analyzer.html')

@tron_bp.route('/api/analyze', methods=['POST'])
def analyze_address():
    address = request.json.get('address')
    result = analyze_suspicious_features(address)
    return jsonify(result)
```
```python
# app.py
from flask import Flask
from modules.tron.routes import tron_bp

app = Flask(__name__)
app.register_blueprint(tron_bp)
```
**Source:** [CITED: Context7 /pallets/flask - Modular Applications with Blueprints]

### Pattern 2: Jinja2 Template Inheritance
**What:** Base template with blocks for sidebar, content, footer
**When to use:** All pages share sidebar navigation and legal disclaimer
**Example:**
```html+jinja
<!-- templates/base.html -->
<!doctype html>
<html>
<head>
  <script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
  <title>{% block title %}CIT{% endblock %}</title>
</head>
<body class="flex min-h-screen">
  <aside class="w-64 bg-gray-800 text-white">
    <!-- Sidebar navigation -->
    {% block sidebar %}
    <nav>
      <a href="/">首页</a>
      <a href="/tron/suspicious-analyzer">TRON可疑分析</a>
    </nav>
    {% endblock %}
  </aside>
  <main class="flex-1 p-6">
    {% block content %}{% endblock %}
  </main>
  <footer class="fixed bottom-0 w-full bg-yellow-100 p-2 text-center">
    {% block footer %}
    法律声明：本工具仅供合规调查使用，请确保遵守相关法律法规...
    {% endblock %}
  </footer>
</body>
</html>
```
```html+jinja
<!-- templates/tron/suspicious_analyzer.html -->
{% extends "base.html" %}
{% block title %}TRON可疑特征分析{% endblock %}
{% block content %}
  <h1>TRON地址可疑特征分析</h1>
  <input type="text" id="address-input" placeholder="输入TRON地址">
  <button onclick="analyze()">分析</button>
  <button onclick="loadSample()">加载样本</button>
  <div id="results"></div>
{% endblock %}
```
**Source:** [CITED: Context7 /pallets/flask - Template Inheritance]

### Pattern 3: TRON Address Analysis Logic Adaptation
**What:** Port CLI script logic to Flask route handlers
**When to use:** Converting existing Python scripts to web endpoints
**Example:**
```python
# modules/tron/suspicious_analyzer.py
# Adapted from 001-day1-TRON地址可疑特征分析工具.py

HEADERS = {
    "User-Agent": "Mozilla/5.0...",
    "Accept": "application/json"
}

def get_tron_address_info(address):
    """API call unchanged from original script"""
    url = "https://apilist.tronscanapi.com/api/accountv2"
    params = {"address": address}
    response = requests.get(url, params=params, headers=HEADERS, timeout=10)
    # ... same parsing logic

def detect_suspicious_features(address_info, trc20_transfers):
    """Scoring algorithm unchanged, returns dict for JSON response"""
    alerts = {'red': [], 'yellow': [], 'green': [], 'score': 0}
    # ... same detection logic (lines 170-351 of original)
    return alerts

def analyze_address_web(address):
    """Web-friendly wrapper returning JSON-serializable dict"""
    basic_info = get_tron_address_info(address)
    trc20_transfers = get_trc20_transfers(address)
    alerts = detect_suspicious_features(basic_info, trc20_transfers)
    return {
        'basic_info': basic_info,
        'alerts': alerts,
        'success': True
    }
```
**Source:** [VERIFIED: Code analysis of existing 001-day1-TRON地址可疑特征分析工具.py]

### Anti-Patterns to Avoid
- **Inline JavaScript in templates:** Use separate static JS files for AJAX calls
- **API keys hardcoded:** Never embed Tronscan API keys; users must input manually (ADDR-05 constraint)
- **Session state for analysis results:** Project constraint - no data persistence
- **Blocking API calls in main thread:** Use timeout parameter (already in original script)

## Don't Hand-Roll

| Problem | Don't Build | Use Instead | Why |
|---------|-------------|-------------|-----|
| Sidebar navigation state | Custom JS tracking | Tailwind CSS + Jinja2 blocks | Static HTML, simpler |
| JSON serialization | Manual string building | Python `json` module (built-in) | Handles escaping, unicode |
| CSV generation | Manual comma joining | Python `csv` module (built-in) | Handles quoting, special chars |
| HTTP requests | `urllib.request` | `requests` library (installed) | Simpler API, timeout support |
| Template rendering | Manual HTML string concat | Flask/Jinja2 | Inheritance, autoescaping |
| Risk score calculation | New algorithm | Existing script logic (lines 170-351) | Proven scoring rules |

**Key insight:** The existing Python scripts contain validated analysis logic. Do not rewrite scoring algorithms - adapt them for web response format.

## Common Pitfalls

### Pitfall 1: Flask Debug Mode in Production-like Context
**What goes wrong:** `app.run(debug=True)` exposes debugger, security risk
**Why it happens:** Default in tutorials, but local tool should still be safe
**How to avoid:** Use `debug=True` only in development, `debug=False` for run.bat/run.sh distribution
**Warning signs:** Werkzeug debugger page appearing on errors

### Pitfall 2: Tronscan API Rate Limiting
**What goes wrong:** Too many requests cause 429 errors, analysis fails
**Why it happens:** Multiple users or rapid analysis clicks
**How to avoid:** Add request timeout (already present), consider caching for repeated addresses within session
**Warning signs:** HTTP 429 responses, empty analysis results

### Pitfall 3: TRON Address Format Validation Missing
**What goes wrong:** Invalid addresses cause API errors, confusing UX
**Why it happens:** No validation before API call
**How to avoid:** Validate TRON address format (starts with 'T', 34 chars, Base58) before API request
```python
import re
def is_valid_tron_address(address):
    return bool(re.match(r'^T[A-Za-z1-9]{33}$', address))
```
**Warning signs:** API returning empty data for malformed addresses

### Pitfall 4: Missing Tailwind CSS CDN Script
**What goes wrong:** Unstyled pages, broken layout
**Why it happens:** Script tag omitted or wrong URL
**How to avoid:** Include exact CDN tag in base.html `<head>`:
```html
<script src="https://cdn.jsdelivr.net/npm/@tailwindcss/browser@4"></script>
```
**Warning signs:** Raw HTML without styling, sidebar not visible

### Pitfall 5: Export Not Including All Alert Data
**What goes wrong:** JSON/CSV exports missing alert details (meaning, feature)
**Why it happens:** Only exporting basic_info, not alerts dict
**How to avoid:** Export function must serialize full analysis result including all three alert levels
**Warning signs:** Exported files missing red/yellow/green categories

## Code Examples

### Flask Route Handler for TRON Analysis
```python
# modules/tron/routes.py
from flask import Blueprint, request, jsonify
from .suspicious_analyzer import analyze_address_web, is_valid_tron_address

tron_bp = Blueprint('tron', __name__, url_prefix='/tron')

@tron_bp.route('/api/analyze', methods=['POST'])
def analyze():
    address = request.json.get('address', '')
    if not is_valid_tron_address(address):
        return jsonify({'error': '无效的TRON地址格式'}), 400
    
    result = analyze_address_web(address)
    return jsonify(result)

@tron_bp.route('/api/sample')
def get_sample():
    """Return sample address for user to understand input format"""
    return jsonify({
        'address': 'TUtPdo7L45ey2KrpibdNcjNL3ujqXo1NNw',
        'description': '示例TRON地址，用于演示分析功能'
    })
```
**Source:** [VERIFIED: Adapted from existing 001-day1 script + Flask patterns]

### JSON/CSV Export Functions
```python
# modules/core/exporter.py
import json
import csv
from io import StringIO

def export_json(data):
    """Convert analysis result to JSON string"""
    return json.dumps(data, ensure_ascii=False, indent=2)

def export_csv(data):
    """Convert analysis alerts to CSV format"""
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['级别', '特征', '详情', '意义'])
    
    for alert in data.get('alerts', {}).get('red', []):
        if isinstance(alert, dict):
            writer.writerow(['红色', alert['feature'], alert['detail'], alert['meaning']])
    
    for alert in data.get('alerts', {}).get('yellow', []):
        if isinstance(alert, dict):
            writer.writerow(['黄色', alert['feature'], alert['detail'], alert['meaning']])
    
    for alert in data.get('alerts', {}).get('green', []):
        if isinstance(alert, dict):
            writer.writerow(['绿色', alert['feature'], alert['detail'], alert['meaning']])
    
    return output.getvalue()
```
**Source:** [ASSUMED: Standard Python csv/json module usage]

### Tronscan API Client (Adapted from Existing)
```python
# modules/core/api_client.py
import requests

TRONSCAN_BASE = "https://apilist.tronscanapi.com/api"
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Accept": "application/json"
}

def get_account_info(address):
    """Get TRON address basic info"""
    url = f"{TRONSCAN_BASE}/accountv2"
    params = {"address": address}
    response = requests.get(url, params=params, headers=HEADERS, timeout=10)
    if response.status_code == 200:
        return response.json()
    return None

def get_trc20_transfers(address, limit=50):
    """Get TRC20 token transfer history"""
    url = f"{TRONSCAN_BASE}/token_trc20/transfers"
    params = {"relatedAddress": address, "limit": limit, "sort": "-timestamp"}
    response = requests.get(url, params=params, headers=HEADERS, timeout=10)
    if response.status_code == 200:
        return response.json().get('token_transfers', [])
    return []
```
**Source:** [VERIFIED: Tronscan API docs + existing script]

## State of the Art

| Old Approach | Current Approach | When Changed | Impact |
|--------------|------------------|--------------|--------|
| Flask `app.run()` inline | Blueprint modular structure | Flask 2.0+ | Better organization for multi-tool apps |
| Tailwind CLI build | Tailwind CDN v4 | 2024 | Zero-config CSS, faster prototyping |
| Tronscan `apilist.tronscan.org` | `apilist.tronscanapi.com` | 2023+ | New API base URL, requires migration |

**Deprecated/outdated:**
- `apilist.tronscan.org` URL: Use `apilist.tronscanapi.com` instead [CITED: Tronscan docs]
- Tailwind v3 CDN: Use v4 `@tailwindcss/browser@4` instead [CITED: tailwindcss.com]

## Assumptions Log

| # | Claim | Section | Risk if Wrong |
|---|-------|---------|---------------|
| A1 | CSV export format includes all alert levels | Code Examples | Export incomplete data |
| A2 | Flask 3.1.3 compatible with Python 3.14.3 | Standard Stack | Installation fails |
| A3 | Sample address 'TUtPdo7L45ey2KrpibdNcjNL3ujqXo1NNw' is valid | Code Examples | Sample loading fails |

**Verification needed:** 
- Flask 3.1.3 compatibility with Python 3.14.3 (both current versions, likely compatible)
- Sample address validity (should test with API before implementation)

## Open Questions

1. **Should sample address use the existing script's default address?**
   - What we know: Script uses `TUtPdo7L45ey2KrpibdNcjNL3ujqXo1NNw` as sample
   - What's unclear: Whether this address returns interesting analysis data
   - Recommendation: Test address with Tronscan API during implementation, select address with meaningful alerts for demonstration

2. **Should Tronscan API key be required or optional?**
   - What we know: ADDR-05 says users input API key manually
   - What's unclear: Whether API works without key (public endpoints vs authenticated)
   - Recommendation: Test without key first; if rate-limited, add optional key input field

3. **Should export files download immediately or display in browser?**
   - What we know: EXPORT-01/02 require JSON/CSV export
   - What's unclear: UX preference - download vs in-browser display
   - Recommendation: Download files (standard evidence preservation workflow)

## Environment Availability

| Dependency | Required By | Available | Version | Fallback |
|------------|------------|-----------|---------|----------|
| Python | Flask runtime | ✓ | 3.14.3 | - |
| pip | Package install | ✓ | 26.0.1 | - |
| Flask | Web framework | ✗ | - | `pip install Flask==3.1.3` |
| requests | Tronscan API | ✓ | 2.32.5 | - |
| pandas | Data handling | ✓ | 3.0.1 | csv module (built-in) |
| Node.js/npm | (not required) | ✓ | 25.6.1/11.9.0 | - |

**Missing dependencies with no fallback:**
- Flask (must install before run.bat/run.sh execution)

**Missing dependencies with fallback:**
- None - pandas available but csv built-in sufficient for EXPORT-02

## Validation Architecture

> SKIPPED: `workflow.nyquist_validation: false` in config.json

## Security Domain

### Applicable ASVS Categories

| ASVS Category | Applies | Standard Control |
|---------------|---------|-----------------|
| V2 Authentication | no | Single-user local tool, no auth required |
| V3 Session Management | no | No session state per project constraint |
| V4 Access Control | no | Single-user, no access levels |
| V5 Input Validation | yes | TRON address format validation (regex) |
| V6 Cryptography | no | No encryption, local plaintext tool |

### Known Threat Patterns for Flask Web App

| Pattern | STRIDE | Standard Mitigation |
|---------|--------|---------------------|
| XSS (user input displayed) | Tampering | Jinja2 autoescaping (enabled by default) |
| SSRF (API URL manipulation) | Tampering | Fixed API endpoints, no user URL input |
| Path traversal (file export) | Tampering | Generated content, no file path input |
| API key leakage | Information Disclosure | User-provided keys, not stored |

### Input Validation Requirements
- **TRON address:** Must validate format (T prefix, 34 chars, Base58) before API call
- **No SQL injection risk:** No database, no SQL queries
- **No command injection:** No subprocess calls, no shell commands

## Sources

### Primary (HIGH confidence)
- Context7 `/pallets/flask` - Blueprint patterns, template inheritance, project structure
- Tronscan API docs - `apilist.tronscanapi.com` endpoints, parameters, response fields [VERIFIED]
- pip index - Flask 3.1.3 current version [VERIFIED: 2026-04-23]
- tailwindcss.com/docs/installation/play-cdn - Tailwind v4 CDN script tag [VERIFIED]

### Secondary (MEDIUM confidence)
- pip show requests - Version 2.32.5 installed [VERIFIED]
- pip show pandas - Version 3.0.1 installed [VERIFIED]
- Existing Python script `001-day1-TRON地址可疑特征分析工具.py` - Analysis logic to adapt [VERIFIED]

### Tertiary (LOW confidence)
- Flask 3.1.3 + Python 3.14.3 compatibility - Assumed compatible (both current) [ASSUMED]
- CSV export format design - Standard module usage pattern [ASSUMED]

## Metadata

**Confidence breakdown:**
- Standard stack: HIGH - Flask, Tailwind, requests versions verified via pip/npm
- Architecture: HIGH - Flask Blueprint and Jinja2 patterns from official docs (Context7)
- Pitfalls: MEDIUM - Common Flask issues from training knowledge, Tronscan API docs verified
- TRON API: HIGH - Official Tronscan documentation fetched, endpoints verified

**Research date:** 2026-04-23
**Valid until:** 2026-05-23 (30 days - Flask/Tailwind stable, Tronscan API endpoints may change)