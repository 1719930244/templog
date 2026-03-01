# MCP 工具配置说明

## 已安装的工具

### 1. Playwright ✅（官方插件，已启用）
- 浏览器自动化
- 访问动态网页、截图、表单填写
- 完全免费，无限制

### 2. Context7 ✅（官方插件，已启用）
- 查询最新技术文档
- 获取版本特定的代码示例
- 完全免费

### 3. Brave Search ✅（已配置）
- 实时网络搜索
- 免费额度：2000次/月
- 无需 API Key 即可使用
- 已配置代理：http://127.0.0.1:7890

### 4. Firecrawl ⚠️（已配置，需要 API Key）
- 智能网页内容提取
- 免费额度：500次/月
- **需要操作**：访问 https://firecrawl.dev/ 注册并获取 API Key
- 然后在 `.mcp.json` 中替换 `FIRECRAWL_API_KEY` 的值

## 如何获取 Firecrawl API Key

1. 访问：https://firecrawl.dev/
2. 点击 "Sign Up" 注册账号
3. 登录后进入 Dashboard
4. 找到 "API Keys" 部分
5. 复制 API Key
6. 编辑 `.mcp.json` 文件，替换 `待填写-访问...` 为你的 API Key

## 重启 Claude Code

配置完成后，需要重启 Claude Code 才能生效：
1. 关闭当前 Claude Code 窗口
2. 重新打开
3. MCP 服务器会自动加载

## 测试工具

重启后，可以测试：

```
使用 Brave Search 搜索"南京大学护理学硕士复试经验"
```

```
使用 Playwright 访问 https://www.xiaohongshu.com/ 并搜索"南大护理考研"
```

```
使用 Firecrawl 抓取 https://grawww.nju.edu.cn/ 的招生信息
```

## 可选：添加 Exa（语义搜索，最强）

如果需要更强大的语义搜索能力，可以添加 Exa：

1. 访问 https://exa.ai/ 注册（$10/月）
2. 获取 API Key
3. 在 `.mcp.json` 中添加：

```json
{
  "mcpServers": {
    "brave-search": { ... },
    "firecrawl": { ... },
    "exa": {
      "command": "npx",
      "args": ["-y", "@exa/mcp-server"],
      "env": {
        "EXA_API_KEY": "your-exa-key",
        "HTTP_PROXY": "http://127.0.0.1:7890",
        "HTTPS_PROXY": "http://127.0.0.1:7890"
      }
    }
  }
}
```

## 总成本

- Playwright：免费
- Context7：免费
- Brave Search：免费（2000次/月）
- Firecrawl：免费（500次/月）或 $20/月
- Exa（可选）：$10/月

**当前配置总成本：$0/月**（使用免费额度）

## 下一步

1. 访问 https://firecrawl.dev/ 注册并获取 API Key
2. 编辑 `.mcp.json` 填入 API Key
3. 重启 Claude Code
4. 开始调研！
