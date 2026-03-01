# 深度网络调研 MCP 工具推荐清单

> 专为考研复试信息调研、学术资料收集等深度研究任务设计
> 更新日期：2026-03-01

---

## 一、推荐工具总览（按优先级）

### 🥇 第一梯队：必装工具（免费/低成本）

| 工具 | 类型 | 主要功能 | 免费额度 | 推荐指数 |
|------|------|----------|----------|----------|
| **Playwright** | 浏览器自动化 | 访问动态网页、截图、表单填写 | 无限制（本地） | ⭐⭐⭐⭐⭐ |
| **Brave Search** | 搜索引擎 | 实时网络搜索 | 2000次/月 | ⭐⭐⭐⭐⭐ |
| **Firecrawl** | 智能爬虫 | 网页内容提取、结构化数据 | 500次/月 | ⭐⭐⭐⭐⭐ |
| **Context7** | 文档查询 | 获取最新技术文档 | 免费 | ⭐⭐⭐⭐ |

### 🥈 第二梯队：增强工具（付费但强大）

| 工具 | 类型 | 主要功能 | 价格 | 推荐指数 |
|------|------|----------|------|----------|
| **Exa** | AI搜索 | 语义搜索、学术论文查找 | $10/月起 | ⭐⭐⭐⭐⭐ |
| **Tavily** | 研究助手 | 深度研究、多源聚合 | $20/月起 | ⭐⭐⭐⭐ |
| **Apify** | 云端爬虫 | 大规模数据采集 | $49/月起 | ⭐⭐⭐⭐ |
| **Perplexity** | AI搜索 | 带引用的AI搜索 | $20/月 | ⭐⭐⭐⭐ |

### 🥉 第三梯队：专业工具（特定场景）

| 工具 | 类型 | 主要功能 | 适用场景 |
|------|------|----------|----------|
| **SearXNG** | 元搜索 | 聚合多个搜索引擎 | 需要多源对比 |
| **Jina Reader** | 内容提取 | LLM友好的内容格式化 | 学术论文阅读 |
| **Crawl4AI** | 开源爬虫 | 免费的网页抓取 | 预算有限 |

---

## 二、针对考研调研的最佳配置方案

### 方案 A：免费方案（推荐新手）

**已启用：**
- ✅ Playwright（已配置）

**建议添加：**
```json
{
  "enabledPlugins": {
    "playwright@claude-plugins-official": true,
    "context7@claude-plugins-official": true
  }
}
```

**外部 MCP（需手动安装）：**
1. **Brave Search MCP**（免费 2000次/月）
2. **Firecrawl MCP**（免费 500次/月）

**能力：**
- ✅ 访问动态网页（考研论坛、小红书）
- ✅ 实时搜索（Brave Search）
- ✅ 智能内容提取（Firecrawl）
- ✅ 文档查询（Context7）

**预计成本：** $0/月

---

### 方案 B：专业方案（推荐深度调研）

**Claude Code 插件：**
```json
{
  "enabledPlugins": {
    "playwright@claude-plugins-official": true,
    "context7@claude-plugins-official": true,
    "github@claude-plugins-official": true
  }
}
```

**外部 MCP（需手动安装）：**
1. **Brave Search MCP**（免费）
2. **Firecrawl MCP**（付费 $20/月）
3. **Exa MCP**（付费 $10/月）
4. **Tavily MCP**（付费 $20/月）

**能力：**
- ✅ 所有免费方案功能
- ✅ 语义搜索（Exa）- 找相似经验分享
- ✅ 深度研究（Tavily）- 多源信息聚合
- ✅ 高级爬虫（Firecrawl付费版）- 无限制抓取
- ✅ GitHub搜索 - 查找考研资料仓库

**预计成本：** $50/月

---

### 方案 C：终极方案（适合长期使用）

**所有方案B的工具 +**
1. **Perplexity API**（$20/月）
2. **Apify**（$49/月）
3. **SearXNG**（自建，免费）

**能力：**
- ✅ 所有专业方案功能
- ✅ AI驱动的研究（Perplexity）
- ✅ 大规模数据采集（Apify）
- ✅ 多搜索引擎聚合（SearXNG）

**预计成本：** $119/月

---

## 三、详细工具介绍

### 1. Playwright（已启用）✅

**官方插件，已在你的配置中启用**

**功能：**
- 自动访问网页
- 处理 JavaScript 渲染的动态内容
- 截图保存
- 填写表单、点击按钮
- 模拟真实用户行为

**适用场景：**
- 访问需要登录的考研论坛
- 抓取小红书、知乎的经验分享
- 访问学校官网的动态内容
- 自动填写查询表单

**使用示例：**
```
使用 Playwright 访问 https://www.xiaohongshu.com/search_result?keyword=南大护理考研
并提取所有相关帖子的标题和链接
```

---

### 2. Brave Search MCP ⭐⭐⭐⭐⭐

**免费额度：2000次/月**

**GitHub：** https://github.com/brave/brave-search-mcp-server

**功能：**
- 实时网络搜索
- 独立搜索索引（不依赖 Google）
- 支持网页搜索和本地搜索
- 无需登录即可使用免费版

**安装方法：**
```bash
npm install -g @modelcontextprotocol/server-brave-search
```

**配置（需要创建 .mcp.json）：**
```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "可选，免费版不需要"
      }
    }
  }
}
```

**获取 API Key（可选）：** https://brave.com/search/api/

**适用场景：**
- 搜索考研经验分享
- 查找学校官网信息
- 搜索论坛帖子
- 实时信息查询

---

### 3. Firecrawl MCP ⭐⭐⭐⭐⭐

**免费额度：500次/月 | 付费：$20/月起**

**GitHub：** https://github.com/mendableai/firecrawl-mcp-server

**功能：**
- 智能网页内容提取
- 自动处理反爬虫机制
- 支持 JavaScript 渲染
- 结构化数据提取
- 批量抓取支持

**安装方法：**
```bash
npm install -g @mendable/firecrawl-mcp
```

**配置：**
```json
{
  "mcpServers": {
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "@mendable/firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "your-api-key"
      }
    }
  }
}
```

**获取 API Key：** https://firecrawl.dev/

**适用场景：**
- 抓取学校官网的招生信息
- 提取论坛帖子的结构化内容
- 批量抓取多个页面
- 处理复杂的动态网站

**使用示例：**
```
使用 Firecrawl 抓取 https://grawww.nju.edu.cn/
并提取所有关于护理学硕士的招生信息
```

---

### 4. Exa MCP ⭐⭐⭐⭐⭐

**价格：$10/月起（1000次搜索）**

**GitHub：** https://github.com/exa-labs/exa-mcp-server

**功能：**
- **语义搜索**：理解搜索意图，不只是关键词匹配
- **学术论文搜索**：专门优化的学术内容搜索
- **相似内容查找**：找到类似的经验分享
- **时间过滤**：只搜索最近的内容

**安装方法：**
```bash
npm install -g @exa/mcp-server
```

**配置：**
```json
{
  "mcpServers": {
    "exa": {
      "command": "npx",
      "args": ["-y", "@exa/mcp-server"],
      "env": {
        "EXA_API_KEY": "your-api-key"
      }
    }
  }
}
```

**获取 API Key：** https://exa.ai/

**适用场景：**
- 搜索"南京大学护理学硕士复试经验"的语义相关内容
- 查找类似的考研经验分享
- 搜索学术论文和研究报告
- 发现相关但关键词不同的内容

**为什么推荐 Exa：**
- 传统搜索：只能找到包含"南京大学"+"护理"+"复试"的页面
- Exa 语义搜索：能找到"南大医学院考研面试"、"护理专业研究生入学考试"等相关内容

---

### 5. Tavily MCP ⭐⭐⭐⭐

**价格：$20/月起（1000次搜索）**

**GitHub：** https://github.com/tavily-ai/tavily-mcp-server

**功能：**
- **深度研究模式**：自动进行多轮搜索和信息聚合
- **多源验证**：从多个来源交叉验证信息
- **自动摘要**：提取关键信息并生成摘要
- **引用追踪**：保留所有信息来源

**安装方法：**
```bash
npm install -g @tavily/mcp-server
```

**配置：**
```json
{
  "mcpServers": {
    "tavily": {
      "command": "npx",
      "args": ["-y", "@tavily/mcp-server"],
      "env": {
        "TAVILY_API_KEY": "your-api-key"
      }
    }
  }
}
```

**获取 API Key：** https://tavily.com/

**适用场景：**
- 深度调研复试流程和内容
- 收集多个来源的信息并对比
- 自动生成调研报告
- 验证信息的真实性

**使用示例：**
```
使用 Tavily 深度研究"南京大学护理学硕士复试"
包括：分数线、考试内容、面试形式、录取比例
```

---

### 6. Context7（官方插件）⭐⭐⭐⭐

**完全免费**

**功能：**
- 查询最新的技术文档
- 获取版本特定的代码示例
- 直接从源仓库拉取文档

**启用方法：**
```json
{
  "enabledPlugins": {
    "playwright@claude-plugins-official": true,
    "context7@claude-plugins-official": true
  }
}
```

**适用场景：**
- 查询护理学相关的学术标准
- 获取医学教育的最新指南
- 查找护理操作的标准流程

---

### 7. Apify MCP ⭐⭐⭐⭐

**价格：$49/月起**

**GitHub：** https://github.com/apify/apify-mcp-server

**功能：**
- **云端执行**：不占用本地资源
- **预构建爬虫**：针对常见网站的现成模板
- **大规模抓取**：同时抓取数百个页面
- **数据存储**：自动保存抓取结果

**安装方法：**
```bash
npm install -g @apify/mcp-server
```

**配置：**
```json
{
  "mcpServers": {
    "apify": {
      "command": "npx",
      "args": ["-y", "@apify/mcp-server"],
      "env": {
        "APIFY_API_TOKEN": "your-token"
      }
    }
  }
}
```

**获取 Token：** https://apify.com/

**适用场景：**
- 批量抓取多个学校的招生信息
- 大规模收集考研经验分享
- 定期监控官网更新
- 抓取需要复杂交互的网站

---

### 8. SearXNG MCP ⭐⭐⭐

**完全免费（需自建）**

**GitHub：** https://github.com/searxng/searxng

**功能：**
- 聚合多个搜索引擎（Google、Bing、DuckDuckGo等）
- 隐私保护
- 无广告
- 可自定义搜索源

**安装方法：**
需要自己搭建 SearXNG 服务器，然后配置 MCP 连接

**适用场景：**
- 需要对比多个搜索引擎的结果
- 注重隐私保护
- 预算有限但需要强大搜索能力

---

## 四、针对你的需求的推荐配置

### 目标：调研南京大学护理学硕士复试信息

**推荐配置（性价比最高）：**

```json
{
  "enabledPlugins": {
    "playwright@claude-plugins-official": true,
    "context7@claude-plugins-official": true
  }
}
```

**外部 MCP（在项目目录创建 .mcp.json）：**
```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"]
    },
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "@mendable/firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "fc-your-key"
      }
    },
    "exa": {
      "command": "npx",
      "args": ["-y", "@exa/mcp-server"],
      "env": {
        "EXA_API_KEY": "your-exa-key"
      }
    }
  }
}
```

**总成本：**
- Playwright：免费
- Context7：免费
- Brave Search：免费（2000次/月）
- Firecrawl：$20/月（或免费500次）
- Exa：$10/月

**总计：$30/月（或 $0/月 使用免费额度）**

---

## 五、安装步骤

### 步骤 1：启用官方插件（已完成）

你已经启用了 Playwright，现在添加 Context7：

```json
{
  "enabledPlugins": {
    "playwright@claude-plugins-official": true,
    "context7@claude-plugins-official": true
  }
}
```

### 步骤 2：在项目目录创建 .mcp.json

```bash
cd /d/OneDrive/Projects/templog/nju-nursing-postgrad-research
```

创建 `.mcp.json` 文件：
```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"]
    },
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "@mendable/firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "your-key-here"
      }
    }
  }
}
```

### 步骤 3：获取 API Keys

1. **Firecrawl**：访问 https://firecrawl.dev/ 注册
2. **Exa**（可选）：访问 https://exa.ai/ 注册
3. **Brave Search**（可选）：访问 https://brave.com/search/api/ 注册

### 步骤 4：重启 Claude Code

重启后，MCP 服务器会自动加载。

### 步骤 5：测试

```
使用 Brave Search 搜索"南京大学护理学硕士复试经验"
```

---

## 六、使用技巧

### 1. 组合使用多个工具

**示例工作流：**
```
1. 用 Brave Search 搜索关键词
2. 用 Exa 进行语义搜索找相关内容
3. 用 Playwright 访问找到的页面
4. 用 Firecrawl 提取结构化内容
5. 用 Tavily 验证信息并生成报告
```

### 2. 针对不同平台使用不同工具

| 平台 | 推荐工具 | 原因 |
|------|---------|------|
| 学校官网 | Firecrawl | 处理复杂结构 |
| 小红书 | Playwright | 需要模拟浏览器 |
| 知乎 | Exa | 语义搜索相关问答 |
| 考研论坛 | Brave Search | 快速搜索 |
| 学术论文 | Exa | 专门优化 |

### 3. 设置代理（如需要）

在 `.mcp.json` 中添加代理：
```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "HTTP_PROXY": "http://127.0.0.1:7890",
        "HTTPS_PROXY": "http://127.0.0.1:7890"
      }
    }
  }
}
```

---

## 七、对比表格

### 搜索工具对比

| 工具 | 类型 | 优势 | 劣势 | 价格 |
|------|------|------|------|------|
| Brave Search | 传统搜索 | 快速、免费额度高 | 关键词匹配 | 免费2000次 |
| Exa | AI搜索 | 语义理解、学术优化 | 需付费 | $10/月 |
| Tavily | 研究助手 | 深度研究、多源验证 | 较贵 | $20/月 |
| Perplexity | AI搜索 | 带引用、易用 | 需订阅 | $20/月 |

### 爬虫工具对比

| 工具 | 类型 | 优势 | 劣势 | 价格 |
|------|------|------|------|------|
| Playwright | 浏览器自动化 | 本地运行、无限制 | 需要编程 | 免费 |
| Firecrawl | 智能爬虫 | 自动处理反爬 | 有配额限制 | $20/月 |
| Apify | 云端爬虫 | 大规模、预构建 | 较贵 | $49/月 |
| Crawl4AI | 开源爬虫 | 完全免费 | 需自己维护 | 免费 |

---

## 八、常见问题

### Q1: 这些工具会被封禁吗？
A:
- Playwright：模拟真实浏览器，不易被封
- Firecrawl：专业反爬虫处理
- Brave/Exa：官方 API，不会被封

### Q2: 免费额度够用吗？
A: 对于单次调研任务，免费额度完全够用：
- Brave Search：2000次/月
- Firecrawl：500次/月
- Playwright：无限制

### Q3: 如何选择工具？
A:
- **预算有限**：Playwright + Brave Search（免费）
- **深度调研**：+ Firecrawl + Exa（$30/月）
- **专业研究**：+ Tavily + Apify（$119/月）

### Q4: 可以同时使用多个工具吗？
A: 可以！建议组合使用以获得最佳效果。

---

## 九、下一步行动

### 立即行动（今天）

1. **启用 Context7 插件**
   - 修改 settings.json
   - 重启 Claude Code

2. **注册 Firecrawl 账号**
   - 访问 https://firecrawl.dev/
   - 获取免费 500次/月额度

3. **创建项目 .mcp.json**
   - 在 nju-nursing-postgrad-research 目录
   - 配置 Brave Search 和 Firecrawl

### 本周内完成

4. **测试工具**
   - 用 Brave Search 搜索考研信息
   - 用 Playwright 访问小红书
   - 用 Firecrawl 抓取官网

5. **评估效果**
   - 看是否需要升级到付费版
   - 决定是否添加 Exa 或 Tavily

---

**Sources:**
- [Top MCP Servers for Web Access](https://research.aimultiple.com/browser-mcp/)
- [Top MCP Servers for Web Access in 2026](https://blog.aimultiple.com/model-context-protocol/)
- [Brave Search MCP Server](https://github.com/brave/brave-search-mcp-server)
- [Firecrawl MCP Server Features](https://generect.com/blog/firecrawl-mcp/)
- [Using Firecrawl MCP to Automate Research](https://growthmethod.com/firecrawl-mcp-server/)
- [Top 5 Exa Alternatives](https://www.firecrawl.dev/blog/exa-alternatives)
- [MCP Servers Marketplace · LobeHub](https://lobehub.com/mcp?category=web-search&q=Firecrawl)
- [ReActMCP: Web Search & Scraping](https://mcplane.com/mcp_servers/re-act-mcp)
