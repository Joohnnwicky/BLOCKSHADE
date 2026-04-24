# Phase 6: Documentation & Export - Discussion Log

> **Audit trail only.** Do not use as input to planning, research, or execution agents.
> Decisions are captured in 06-CONTEXT.md — this log preserves the alternatives considered.

**Date:** 2026-04-24
**Phase:** 06-documentation-export
**Areas discussed:** PDF导出方案, PDF按钮位置, 手册组织方式, 手册内容深度, API指南位置, API指南内容

---

## PDF导出方案

| Option | Description | Selected |
|--------|-------------|----------|
| WeasyPrint | HTML直接转PDF，风格与现有页面一致。需安装GTK | ✓ |
| ReportLab | 纯Python，无外部依赖，Windows兼容好。需手动布局代码 | |
| wkhtmltopdf | 渲染效果好，需系统安装wkhtmltopdf二进制 | |
| 浏览器打印 | window.print()触发打印对话框，最简单无代码改动 | |

**User's choice:** WeasyPrint
**Notes:** 考虑本地运行工具特性（Windows为主、无服务器），WeasyPrint提供最佳风格一致性

---

## PDF按钮位置

| Option | Description | Selected |
|--------|-------------|----------|
| 所有工具统一 | 所有11个工具结果页面都有PDF导出按钮，与JSON/CSV并列 | ✓ |
| 分析类工具 | 仅TRON可疑/行为、ETH交易、BTC提供PDF，模板类用文本复制 | |
| 核心工具 | 仅TRON可疑分析和ETH交易查询提供PDF | |

**User's choice:** 所有工具统一
**Notes:** 保持用户体验一致性，所有工具都提供完整导出选项

---

## 手册组织方式

| Option | Description | Selected |
|--------|-------------|----------|
| 首页卡片+详情页 | 手册首页展示11个工具卡片，点击卡片进入详细说明书页面 | ✓ |
| 单页滚动 | 一个长页面包含所有工具说明，滚动浏览 | |
| 首页卡片+弹窗 | 首页展示工具卡片，点击弹出模态窗口显示说明 | |

**User's choice:** 首页卡片+详情页
**Notes:** 需12个页面（首页+11详情），适合深度内容展示和复制

---

## 手册内容深度

| Option | Description | Selected |
|--------|-------------|----------|
| 操作步骤 | 从打开页面到导出结果的完整流程，分步骤配截图 | ✓ |
| 结果解释 | 每个结果字段含义、红/黄/绿级别解释、置信度含义 | ✓ |
| API密钥说明 | 如何获取Tronscan/Etherscan/Blockchain API密钥 | ✓ |
| 案例演示 | 真实调查场景示例、输入样例、输出解读 | ✓ |

**User's choice:** 全选（操作步骤、结果解释、API密钥说明、案例演示）
**Notes:** 针对初学者用户群（金融机构合规调查人员），提供完整友好说明

---

## API指南位置

| Option | Description | Selected |
|--------|-------------|----------|
| 独立页面 | 独立 `/docs/api-guide` 页面，包含三个API获取步骤 | ✓ |
| 嵌入工具页 | 嵌入各工具页面，输入密钥时显示"如何获取密钥？"链接 | |
| 嵌入手册首页 | 嵌入手册首页，作为"API获取指南"卡片入口 | |

**User's choice:** 独立页面
**Notes:** 独立页面便于集中维护和查找

---

## API指南内容

| Option | Description | Selected |
|--------|-------------|----------|
| 注册流程 | 官网注册链接、注册流程截图、密钥生成位置 | ✓ |
| 使用限制 | 密钥调用示例、API限制说明（免费额度、速率限制） | ✓ |
| 安全说明 | 密钥安全提醒、不存储密钥的设计说明 | ✓ |
| 问题排查 | 密钥丢失找回、常见错误排查 | ✓ |

**User's choice:** 全选（注册流程、使用限制、安全说明、问题排查）
**Notes:** 完整的API获取指南内容，帮助初学者理解密钥使用

---

## Claude's Discretion

- WeasyPrint安装脚本（Windows GTK依赖处理）
- PDF导出按钮具体样式设计
- 手册首页卡片布局细节
- 说明书页面模板设计
- API指南页面具体内容编写
- 侧边栏导航新增入口（手册、API指南）

## Deferred Ideas

None — discussion stayed within phase scope.