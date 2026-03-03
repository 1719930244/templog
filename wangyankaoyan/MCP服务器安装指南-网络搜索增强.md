# 网络搜索与调查 MCP 服务器推荐清单

> 用于增强 Claude Code 的网络搜索、网页抓取和深度调研能力
>
> 更新日期：2026-03-01

---

## 一、推荐的 MCP 服务器（按优先级）

### 🥇 第一梯队：必装工具

#### 1. Brave Search MCP Server
**功能**：实时网络搜索，无需 API 密钥（免费版）或使用 Brave Search API（付费版）

**优势**：
- ✅ 官方支持（Brave 官方维护）
- ✅ 实时网络搜索
- ✅ 本地搜索和网页搜索
- ✅ 智能回退机制
- ✅ 灵活的过滤选项

**GitHub**：https://github.com/brave/brave-search-mcp-server

**安装方法**：
```bash
# 使用 npx（推荐）
npx -y @modelcontextprotocol/server-brave-search

# 或全局安装
npm install -g @modelcontextprotocol/server-brave-search
```

**配置（Claude Code settings.json）**：
```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-api-key-here"  // 可选，免费版不需要
      }
    }
  }
}
```

**获取 API Key**（可选）：https://brave.com/search/api/

---

#### 2. Firecrawl MCP Server
**功能**：强大的网页抓取和搜索工具

**优势**：
- ✅ 智能网页内容提取
- ✅ 支持 JavaScript 渲染
- ✅ 自动处理反爬虫
- ✅ 结构化数据提取
- ✅ 批量抓取支持

**GitHub**：https://github.com/mendableai/firecrawl-mcp-server

**安装方法**：
```bash
npm install -g @mendable/firecrawl-mcp
```

**配置**：
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

**获取 API Key**：https://firecrawl.dev/

---

#### 3. Playwright MCP Server
**功能**：浏览器自动化和网页交互

**优势**：
- ✅ 官方支持（Microsoft Playwright 团队）
- ✅ 完整的浏览器控制
- ✅ 支持截图和 PDF 生成
- ✅ 处理动态内容
- ✅ 支持多浏览器（Chrome、Firefox、Safari）

**GitHub**：https://github.com/executeautomation/mcp-playwright

**安装方法**：
```bash
npm install -g @playwright/mcp
npx playwright install  # 安装浏览器
```

**配置**：
```json
{
  "mcpServers": {
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    }
  }
}
```

---

### 🥈 第二梯队：增强工具

#### 4. Apify MCP Server
**功能**：专业级网页抓取和数据提取

**优势**：
- ✅ 预构建的抓取模板
- ✅ 云端执行（不占用本地资源）
- ✅ 大规模数据提取
- ✅ 支持复杂网站结构

**GitHub**：https://github.com/apify/apify-mcp-server

**安装方法**：
```bash
npm install -g @apify/mcp-server
```

**配置**：
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

**获取 Token**：https://apify.com/

---

#### 5. Chrome MCP Server
**功能**：通过 Chrome 扩展控制浏览器

**优势**：
- ✅ 使用真实浏览器环境
- ✅ 访问已登录的网站
- ✅ 语义搜索页面内容
- ✅ 复杂的浏览器自动化

**GitHub**：https://github.com/hangwin/mcp-chrome

**安装方法**：
1. 克隆仓库
2. 在 Chrome 中加载扩展
3. 配置 MCP 连接

**配置**：
```json
{
  "mcpServers": {
    "chrome": {
      "command": "node",
      "args": ["/path/to/mcp-chrome/server.js"]
    }
  }
}
```

---

#### 6. WebSearch MCP (免费，无需 API Key)
**功能**：使用免费 Google 搜索，无需 API 密钥

**优势**：
- ✅ 完全免费
- ✅ 无需注册
- ✅ 实时搜索结果
- ✅ 简单易用

**GitHub**：https://github.com/pskill9/web-search

**安装方法**：
```bash
git clone https://github.com/pskill9/web-search.git
cd web-search
npm install
```

**配置**：
```json
{
  "mcpServers": {
    "web-search": {
      "command": "node",
      "args": ["/path/to/web-search/index.js"]
    }
  }
}
```

---

### 🥉 第三梯队：专业工具

#### 7. Puppeteer MCP Server
**功能**：基于 Puppeteer 的浏览器自动化

**优势**：
- ✅ 轻量级
- ✅ 快速启动
- ✅ 适合简单任务

**安装方法**：
```bash
npm install -g puppeteer-mcp-server
```

---

#### 8. Fetch MCP Server
**功能**：高效的网页内容获取和转换

**优势**：
- ✅ 针对 LLM 优化的内容格式
- ✅ 自动清理无关内容
- ✅ 支持多种内容类型

**GitHub**：查看 awesome-mcp-servers 列表

---

## 二、推荐配置方案

### 方案 A：免费方案（适合个人使用）
```json
{
  "mcpServers": {
    "web-search": {
      "command": "node",
      "args": ["/path/to/web-search/index.js"]
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    }
  }
}
```

**能力**：
- ✅ 免费网络搜索
- ✅ 浏览器自动化
- ✅ 动态内容抓取

---

### 方案 B：专业方案（适合深度调研）
```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-api-key"
      }
    },
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "@mendable/firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "your-api-key"
      }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    }
  }
}
```

**能力**：
- ✅ 高质量搜索结果
- ✅ 智能内容提取
- ✅ 完整浏览器控制
- ✅ 处理复杂网站

---

### 方案 C：企业方案（适合大规模数据采集）
```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "your-api-key"
      }
    },
    "apify": {
      "command": "npx",
      "args": ["-y", "@apify/mcp-server"],
      "env": {
        "APIFY_API_TOKEN": "your-token"
      }
    },
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "@mendable/firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "your-api-key"
      }
    },
    "chrome": {
      "command": "node",
      "args": ["/path/to/mcp-chrome/server.js"]
    }
  }
}
```

**能力**：
- ✅ 多源搜索
- ✅ 云端大规模抓取
- ✅ 智能内容提取
- ✅ 真实浏览器环境

---

## 三、安装步骤（以 Brave Search 为例）

### 步骤 1：安装 Node.js
确保已安装 Node.js（v18 或更高版本）：
```bash
node --version
npm --version
```

### 步骤 2：安装 MCP Server
```bash
npm install -g @modelcontextprotocol/server-brave-search
```

### 步骤 3：配置 Claude Code
打开 Claude Code 设置文件（通常在 `~/.claude/settings.json` 或 VSCode 设置中）：

```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"]
    }
  }
}
```

### 步骤 4：重启 Claude Code
重启后，MCP 服务器会自动加载。

### 步骤 5：测试
在 Claude Code 中输入：
```
搜索南京大学护理学硕士复试相关信息
```

---

## 四、针对你的需求的推荐配置

### 目标：深度调研南京大学护理学硕士复试信息

**推荐配置**：
```json
{
  "mcpServers": {
    "brave-search": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-brave-search"],
      "env": {
        "BRAVE_API_KEY": "BSAqQxxxxxxxxxxx"  // 可选
      }
    },
    "firecrawl": {
      "command": "npx",
      "args": ["-y", "@mendable/firecrawl-mcp"],
      "env": {
        "FIRECRAWL_API_KEY": "fc-xxxxxxxxxx"
      }
    },
    "playwright": {
      "command": "npx",
      "args": ["-y", "@playwright/mcp"]
    }
  }
}
```

**使用场景**：
1. **Brave Search**：搜索考研论坛、知乎、小红书的经验分享
2. **Firecrawl**：抓取南京大学研究生院官网的招生通知
3. **Playwright**：访问需要登录的考研论坛，获取内部资料

---

## 五、快速开始（免费方案）

如果你想立即开始，不想注册 API：

### 1. 安装 WebSearch MCP（免费）
```bash
cd /d/OneDrive/Projects
git clone https://github.com/pskill9/web-search.git
cd web-search
npm install
```

### 2. 配置 Claude Code
在 `C:\Users\daoge\.claude\settings.json` 中添加：
```json
{
  "mcpServers": {
    "web-search": {
      "command": "node",
      "args": ["D:/OneDrive/Projects/web-search/index.js"]
    }
  }
}
```

### 3. 重启 Claude Code

### 4. 测试
```
使用网络搜索查找南京大学护理学硕士2024年复试分数线
```

---

## 六、资源链接

### 官方文档
- [MCP 官方文档](https://modelcontextprotocol.io/)
- [Claude Code MCP 指南](https://docs.anthropic.com/claude/docs/mcp)

### MCP 服务器列表
- [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers) - 最全面的 MCP 服务器列表
- [PipedreamHQ/awesome-mcp-servers](https://github.com/PipedreamHQ/awesome-mcp-servers)
- [serp-ai/awesome-mcp-servers](https://github.com/serp-ai/awesome-mcp-servers/)

### 教程和指南
- [Top 10 awesome MCP servers](https://composio.dev/blog/10-awesome-mcp-servers-to-make-your-life-easier)
- [50+ Best MCP Servers for Claude Code](https://claudefa.st/blog/tools/mcp-extensions/best-addons)
- [Web Access Through MCP Servers](https://claudefa.st/blog/tools/mcp-extensions/search-tools)
- [Building an MCP Server for Web Scraping](https://spider.cloud/blog/building-mcp-server-for-web-scraping)

### API 密钥获取
- [Brave Search API](https://brave.com/search/api/) - 免费额度：2000 次/月
- [Firecrawl API](https://firecrawl.dev/) - 免费额度：500 次/月
- [Apify](https://apify.com/) - 免费额度：$5/月

---

## 七、常见问题

### Q1: MCP 服务器安装后不生效？
A:
1. 检查 settings.json 路径是否正确
2. 确保 Node.js 版本 >= 18
3. 重启 Claude Code
4. 查看 Claude Code 日志（Help → Show Logs）

### Q2: 需要代理才能访问某些网站？
A: 在 MCP 配置中添加代理：
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

### Q3: 免费方案够用吗？
A: 对于个人调研，免费方案完全够用：
- WebSearch MCP：无限制
- Brave Search：2000 次/月
- Playwright：本地运行，无限制

### Q4: 如何选择 MCP 服务器？
A:
- **简单搜索**：WebSearch MCP 或 Brave Search
- **复杂网站**：Playwright 或 Puppeteer
- **大规模抓取**：Apify 或 Firecrawl
- **需要登录**：Chrome MCP

---

## 八、下一步行动

### 立即行动（5 分钟）
1. [ ] 安装 WebSearch MCP（免费，无需 API）
2. [ ] 配置 Claude Code settings.json
3. [ ] 重启 Claude Code
4. [ ] 测试搜索功能

### 短期计划（本周）
1. [ ] 注册 Brave Search API（免费额度）
2. [ ] 安装 Playwright MCP
3. [ ] 测试抓取南大研究生院官网

### 长期计划（按需）
1. [ ] 评估是否需要付费 API
2. [ ] 探索更多专业 MCP 服务器
3. [ ] 自定义 MCP 服务器（如有特殊需求）

---

**Sources:**
- [wong2/awesome-mcp-servers](https://github.com/wong2/awesome-mcp-servers)
- [Brave Search MCP Server](https://github.com/brave/brave-search-mcp-server)
- [Firecrawl MCP Server](https://github.com/mendableai/firecrawl-mcp-server)
- [Playwright MCP](https://github.com/executeautomation/mcp-playwright)
- [Apify MCP Server](https://github.com/apify/apify-mcp-server)
- [Chrome MCP Server](https://github.com/hangwin/mcp-chrome)
- [WebSearch MCP (Free)](https://github.com/pskill9/web-search)
- [Top 10 awesome MCP servers](https://composio.dev/blog/10-awesome-mcp-servers-to-make-your-life-easier)
- [50+ Best MCP Servers](https://claudefa.st/blog/tools/mcp-extensions/best-addons)
- [Web Access Through MCP Servers](https://claudefa.st/blog/tools/mcp-extensions/search-tools)
