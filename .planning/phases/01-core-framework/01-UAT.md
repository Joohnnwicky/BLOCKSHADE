---
status: testing
phase: 01-core-framework
source: [01-01-SUMMARY.md, 01-02-SUMMARY.md, 01-03-SUMMARY.md, 01-04-SUMMARY.md, 01-05-SUMMARY.md, 01-06-SUMMARY.md]
started: "2026-04-24T21:00:00.000Z"
updated: "2026-04-24T21:05:00.000Z"
---

## Current Test

number: 1
name: Cold Start Smoke Test (Retest after fix)
expected: |
  Double-click run.bat. Flask server starts without errors, browser opens to http://127.0.0.1:5000, homepage loads showing "虚拟币犯罪调查工具集" title.
awaiting: user response (retest)

## Tests

### 1. Cold Start Smoke Test
expected: Double-click run.bat → Flask server starts, browser opens to http://127.0.0.1:5000, homepage displays "虚拟币犯罪调查工具集" title
result: issue
reported: "jinja2.exceptions.TemplateNotFound: docs/manual_tron-suspicious.html - Server crashes. 使用手册部分全是乱码 (manuals section shows garbled text)"
severity: blocker
root_cause: "Slug-to-template naming mismatch: route used hyphen slug (tron-suspicious) but template filename used underscore (tron_suspicious). Also missing 404.html for invalid slug fallback."
fix_applied: "modules/docs/routes.py line 65: added tool.replace('-', '_') to convert slug hyphens to underscores before render_template"
fix_commit: c99986a

### 2. Homepage Categories
expected: Homepage shows 4 colored category badges: 地址分析, 交易追踪, 跨链分析, 案件处理
result: [pending]

### 3. Homepage Tool Count
expected: Homepage displays 11 tool links across all categories (3+3+2+3)
result: [pending]

### 4. Sidebar Navigation
expected: Sidebar shows 13 links (首页, 11 tools, 使用手册). Clicking any link navigates to correct page.
result: [pending]

### 5. Legal Disclaimer Footer
expected: Yellow footer at bottom of every page displays "法律声明：本工具仅供合规调查使用..."
result: [pending]

### 6. TRON Analyzer Sample Loading
expected: Navigate to TRON可疑分析 page. Click "加载样本" button. Address input fills with sample TRON address (TUtPdo7L45ey2KrpibdNcjNL3ujqXo1NNw).
result: [pending]

### 7. TRON Analyzer Analysis
expected: With sample address loaded, click "开始分析". After 5-10 seconds, results display: basic info (TRX balance, USDT balance, tx count), color-coded score circle, red/yellow/green alert sections.
result: [pending]

### 8. TRON Analyzer JSON Export
expected: After analysis completes, click "导出JSON". JSON file downloads with filename containing address and date.
result: [pending]

### 9. TRON Analyzer CSV Export
expected: After analysis completes, click "导出CSV". CSV file downloads with columns: 级别, 特征, 详情, 意义.
result: [pending]

## Summary

total: 9
passed: 0
issues: 1
pending: 8
skipped: 0
blocked: 0

## Gaps

- truth: "Flask server starts without errors when clicking manual links"
  status: fixed
  reason: "User reported: jinja2.exceptions.TemplateNotFound: docs/manual_tron-suspicious.html"
  severity: blocker
  test: 1
  root_cause: "Slug-to-template naming mismatch (hyphen vs underscore)"
  artifacts:
    - path: "modules/docs/routes.py"
      issue: "Used slug directly in template path without converting hyphens"
  fix_applied: c99986a