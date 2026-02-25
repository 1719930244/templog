# OpenClaw 与 Kimi 编码生态调研

> **日期**: 2026-02-25 | **定位**: OpenClaw 平台架构、Kimi 编码 Agent 系列、社区生态

---

## 一、OpenClaw

### 1.1 基本信息

| 项目 | 信息 |
|------|------|
| GitHub | https://github.com/openclaw/openclaw |
| Stars | 226,444 |
| 语言 | TypeScript |
| 许可证 | MIT |
| 创建时间 | 2025-11-24 |
| 创始人 | Peter Steinberger (@steipete)，知名 iOS/macOS 开发者 |
| 最新版本 | v2026.2.24（几乎日更） |

项目经历多次更名：Warelay → Clawdbot → Moltbot → OpenClaw。

### 1.2 定位与核心架构

OpenClaw 是一个开源的个人 AI 助手网关框架，口号是 "Your own personal AI assistant. Any OS. Any Platform. The lobster way."（龙虾之道）。它不是编码 Agent，而是一个通用 AI 助手平台，可连接多种消息渠道并执行各类任务。

```
WhatsApp / Telegram / Slack / Discord / Google Chat / Signal / iMessage / Teams / Matrix / WebChat
                              |
                              v
                    ┌─────────────────────┐
                    │      Gateway        │  (WebSocket 控制平面)
                    │  ws://127.0.0.1:18789│
                    └──────────┬──────────┘
                              |
                              ├─ Pi agent (RPC)
                              ├─ CLI (openclaw ...)
                              ├─ WebChat UI
                              ├─ macOS app
                              └─ iOS / Android nodes
```

Gateway 是核心控制平面，通过 WebSocket 协议连接所有客户端、工具和事件。

### 1.3 主要功能

- **多渠道消息集成**: WhatsApp、Telegram、Slack、Discord、Google Chat、Signal、iMessage、Teams、Matrix 等 14+ 渠道
- **多 Agent 路由**: 不同渠道/账户可路由到隔离的 agent 工作空间
- **语音交互**: Voice Wake + Talk Mode，支持 ElevenLabs 语音
- **Live Canvas**: agent 驱动的可视化工作空间（A2UI）
- **浏览器控制**: 内置 Chrome/Chromium CDP 控制
- **技能系统**: 支持 bundled/managed/workspace skills，有独立技能市场 ClawHub（clawhub.com）
- **跨平台**: macOS 菜单栏应用、iOS/Android 节点、Windows（WSL2）、Linux
- **安全模型**: DM 配对机制、Docker 沙箱、权限控制
- **MCP 支持**: 通过 mcporter 桥接 MCP 协议
- **自动化**: Cron / Webhook / Gmail Pub/Sub

模型方面，OpenClaw 支持任意 LLM，官方推荐 Anthropic Claude Opus 4.6。

### 1.4 生态子项目

| 子项目 | Stars | 说明 |
|--------|-------|------|
| clawhub | 2,804 | 技能目录市场 |
| skills | 1,417 | 所有技能存档 |
| lobster | 567 | OpenClaw 原生工作流 shell |
| openclaw-ansible | 398 | 自动化部署 |
| nix-openclaw | 448 | Nix 打包 |
| acpx | 70 | Agent Client Protocol 无头 CLI 客户端 |

### 1.5 Moltbook：Agent-Only 社交网络

OpenClaw 催生了一个名为 Moltbook 的 agent-only 社交网络，三周内增长到超过 280 万注册 agent，产生 23 万+ 非垃圾帖子，在 2026 年 1-2 月引发大量学术研究。

### 1.6 相关学术论文

1. "From Assistant to Double Agent: Formalizing and Benchmarking Attacks on OpenClaw for Personalized Local AI Agent" (arXiv:2602.08412) — 安全评估
2. "OpenClaw Agents on Moltbook: Risky Instruction Sharing and Norm Enforcement" (arXiv:2602.02625) — 社交网络分析
3. "OpenClaw, Moltbook, and ClawdLab: From Agent-Only Social Networks to Autonomous Scientific Research" (arXiv:2602.19810) — 综合研究
4. "OpenClaw AI Agents as Informal Learners at Moltbook" (arXiv:2602.18832) — 学习社区
5. "When OpenClaw AI Agents Teach Each Other" (arXiv:2602.14477) — 同伴学习
6. "Human Control Is the Anchor, Not the Answer" (arXiv:2602.09286) — 治理分析
7. "A Trajectory-Based Safety Audit of Clawdbot (OpenClaw)" (arXiv:2602.14364) — 安全审计

---

## 二、Moonshot AI 的 Kimi 编码系列

### 2.1 Kimi Code CLI

| 项目 | 信息 |
|------|------|
| GitHub | https://github.com/MoonshotAI/kimi-cli |
| Stars | 6,745 |
| 语言 | Python |
| 定位 | 终端 AI 编码 Agent（类似 Claude Code / Cursor CLI） |

主要特性：
- Shell 命令模式（Ctrl-X 切换）
- VS Code 扩展集成
- ACP（Agent Client Protocol）支持，可与 Zed、JetBrains 等 IDE 集成
- MCP 协议支持
- 多语言 Agent SDK（Go / Node.js / Python）

### 2.2 Kimi-Dev-72B

| 项目 | 信息 |
|------|------|
| GitHub | https://github.com/MoonshotAI/Kimi-Dev |
| Stars | 1,148 |
| 论文 | arXiv:2509.23045 |
| 定位 | 面向软件工程任务的开源编码 LLM |

技术要点：
- SWE-bench Verified 达 60.4%，开源模型 SOTA
- 通过大规模强化学习优化，在 Docker 中自主修补真实仓库
- 两阶段框架：文件定位 → 代码编辑
- 核心思想：Agentless 训练作为 SWE-Agent 的技能先验

### 2.3 Kimi K2

| 项目 | 信息 |
|------|------|
| GitHub | https://github.com/MoonshotAI/Kimi-K2 |
| Stars | 10,422 |
| 论文 | arXiv:2507.20534 |
| 参数 | 320 亿激活 / 1 万亿总参数（MoE 架构） |

Benchmark 表现：
- SWE-bench Verified: 65.8%
- SWE-bench Multilingual: 47.3%
- LiveCodeBench v6: 53.7
- AIME 2025: 49.5
- 使用 MuonClip 优化器，15.5 万亿 token 预训练
- 开源 base 和 post-trained 检查点

### 2.4 Kimi K2.5

| 论文 | arXiv:2602.02276 |
|------|-------------------|
| 定位 | 开源多模态 agentic 模型 |

在 K2 基础上引入：
- 联合文本-视觉预训练和强化学习
- **Agent Swarm**: 自主并行 agent 编排框架，可将复杂任务分解为异构子问题并发执行
- 延迟降低最高 4.5 倍
- 在编码、视觉、推理和 agentic 任务上达到 SOTA

---

## 三、"KimiClaw" 的真实含义

"KimiClaw" 并非独立项目。GitHub 上存在第三方集成插件 `FelipeOFF/openclaw-kimi-code-auth`（OAuth provider plugin for Kimi Code CLI integration with OpenClaw），说明社区在将 Kimi Code CLI 作为 OpenClaw 的后端 agent 使用。"KimiClaw" 是社区对这种组合的非正式称呼。

---

## 四、编码 Agent 横向对比

| 系统 | SWE-bench Verified | 类型 | 开源 |
|------|-------------------|------|------|
| Kimi K2.5 | — (多模态 agentic SOTA) | 多模态 MoE | 是 |
| Kimi K2 | 65.8% | 非思考模式 LLM | 是 |
| Kimi-Dev-72B | 60.4% | 工作流方法 | 是 |
| OpenClaw | N/A（平台，非模型） | AI 助手网关 | 是 |

OpenClaw 本身不参与 SWE-bench 评测，因为它是平台/框架而非模型。Kimi 系列在编码 benchmark 上表现突出，Kimi K2 在开源非思考模型中处于领先。

---

**调研日期**: 2026-02-25
