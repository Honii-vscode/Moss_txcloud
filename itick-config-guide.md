# iTick API 配置指南

## 📊 当前状态

### ✅ 已完成的配置
1. **API 密钥已设置**: `de41c52eed6b4b9f8bb55636e3add43101a1e5f69f6b491e99192af10a4b598e`
2. **服务器已部署**: 集成 iTick 的金融看板正在运行
3. **基础架构就绪**: 多数据源、缓存、监控都已配置

### ❌ 需要解决的问题
**iTick API 端点配置不正确**
- 当前使用的端点: `https://api.itick.com/v1`
- 错误信息: `getaddrinfo EAI_AGAIN api.itick.com` (域名无法解析)

## 🔍 如何找到正确的 iTick API 端点

### 方法一：查看 iTick 官方文档
1. 登录 iTick 开发者控制台
2. 查看 API 文档
3. 找到 "Base URL" 或 "Endpoint"
4. 常见格式：
   - `https://api.itickdata.com/v1`
   - `https://data.itick.com/api/v1`
   - `https://open.itick.com/api`
   - `https://itick.cn/api/v1`

### 方法二：检查 API 密钥邮件或控制台
1. 查看注册 iTick 时收到的欢迎邮件
2. 登录 iTick 用户控制台
3. 在 "API 设置" 或 "开发者" 部分查找端点信息

### 方法三：测试常见端点
```bash
# 设置你的 API 密钥
export ITICK_API_KEY="de41c52eed6b4b9f8bb55636e3add43101a1e5f69f6b491e99192af10a4b598e"

# 测试不同的端点（将 YOUR_BASE_URL 替换为实际值）
export ITICK_BASE_URL="YOUR_BASE_URL"

# 重启服务
cd /root/.openclaw/workspace/finance-dashboard-v2
pkill -f "node.*server.js"
node server.js > server.log 2>&1 &

# 检查状态
curl http://localhost:3001/api/itick-status | jq '.'
```

## 🚀 快速配置步骤

### 步骤1：确定正确的 API 端点
找到 iTick 的以下信息：
- **Base URL**: 例如 `https://api.itickdata.com/v1`
- **认证方式**: Bearer Token、API Key、参数等
- **API 路径**: `/quote`, `/quotes`, `/health` 等

### 步骤2：配置环境变量
```bash
# 编辑配置文件
nano /root/.openclaw/workspace/finance-dashboard-v2/.env

# 添加以下内容（根据实际情况调整）
ITICK_API_KEY="de41c52eed6b4b9f8bb55636e3add43101a1e5f69f6b491e99192af10a4b598e"
ITICK_BASE_URL="https://正确的API端点"
ITICK_AUTH_TYPE="bearer"  # 或 "api_key", "param"
ITICK_AUTH_HEADER="Authorization"  # 或 "X-API-Key"
ITICK_AUTH_PARAM="apikey"  # 如果使用参数认证
```

### 步骤3：重启服务
```bash
cd /root/.openclaw/workspace/finance-dashboard-v2
pkill -f "node.*server.js"
node server.js > server.log 2>&1 &
```

### 步骤4：验证配置
```bash
# 检查服务状态
curl http://localhost:3001/api/health | jq '.'

# 检查 iTick 状态
curl http://localhost:3001/api/itick-status | jq '.'

# 测试数据获取
curl http://localhost:3001/api/market-data | jq '.config.itickEnabled, .sourceStats'
```

## 🔧 高级配置选项

### 完整环境变量配置
```bash
# iTick 核心配置
export ITICK_API_KEY="de41c52eed6b4b9f8bb55636e3add43101a1e5f69f6b491e99192af10a4b598e"
export ITICK_BASE_URL="https://api.itickdata.com/v1"

# 认证配置（根据 iTick 文档调整）
export ITICK_AUTH_TYPE="bearer"           # bearer, api_key, param
export ITICK_AUTH_HEADER="Authorization"  # HTTP 头名称
export ITICK_AUTH_PARAM="apikey"          # 参数名称（如果使用参数认证）

# API 端点路径（根据 iTick 文档调整）
export ITICK_HEALTH_ENDPOINT="/health"
export ITICK_QUOTE_ENDPOINT="/market/quote"
export ITICK_QUOTES_ENDPOINT="/market/quotes"

# 其他数据源（可选）
export TWELVE_DATA_API_KEY="your_key_here"
export FINNHUB_API_KEY="your_key_here"
```

### 符号映射配置
如果需要调整符号格式，编辑文件：
`/root/.openclaw/workspace/finance-dashboard-v2/itick-integration.js`

找到 `symbolMapping` 部分，根据 iTick 的符号格式调整：
```javascript
symbolMapping: {
  // 格式：'我们的符号': { itickSymbol: 'iTick符号', exchange: '交易所', type: '类型' }
  '000001.SS': { itickSymbol: '000001', exchange: 'SSE', type: 'STOCK' },
  '^GSPC': { itickSymbol: 'SPX', exchange: 'INDEX', type: 'INDEX' },
  // ... 其他符号
}
```

## 📊 验证与测试

### 测试脚本
创建测试文件 `test-itick-config.sh`：
```bash
#!/bin/bash
echo "🧪 测试 iTick 配置..."

# 检查服务运行
if ! curl -s http://localhost:3001/api/health > /dev/null; then
  echo "❌ 服务未运行"
  exit 1
fi

echo "✅ 服务运行正常"

# 检查 iTick 状态
ITICK_STATUS=$(curl -s http://localhost:3001/api/itick-status)
echo "iTick 状态:"
echo "$ITICK_STATUS" | jq '.'

# 检查数据源
MARKET_DATA=$(curl -s http://localhost:3001/api/market-data)
echo -e "\n数据源统计:"
echo "$MARKET_DATA" | jq '.sourceStats'

# 检查 iTick 数据
echo -e "\niTick 数据示例:"
echo "$MARKET_DATA" | jq '.data | to_entries[] | select(.value.source == "itick") | "\(.key): \(.value.price) (\(.value.changePercent)%)"' 2>/dev/null || echo "暂无 iTick 数据"
```

### 监控指标
成功配置后，你应该看到：
1. `/api/itick-status` 返回 `{"enabled": true, "health": {"status": "healthy"}}`
2. `/api/market-data` 的 `sourceStats` 中包含 `itick` 数据源
3. 数据中的 `source` 字段显示 `"itick"`

## ⚠️ 常见问题与解决

### 问题1：域名解析失败
```
错误: getaddrinfo EAI_AGAIN api.itick.com
解决: 使用正确的 API 端点，不是 api.itick.com
```

### 问题2：认证失败
```
错误: 401 Unauthorized 或 403 Forbidden
解决:
1. 检查 API 密钥是否正确
2. 检查认证方式（Bearer Token vs API Key）
3. 检查密钥是否有访问权限
```

### 问题3：API 端点不存在
```
错误: 404 Not Found
解决:
1. 检查 Base URL 是否正确
2. 检查 API 路径是否正确
3. 查看 iTick API 文档
```

### 问题4：网络连接问题
```
错误: ECONNREFUSED 或 timeout
解决:
1. 检查服务器网络连接
2. 检查防火墙设置
3. 确认 iTick 服务是否可用
```

## 🚀 一键配置脚本

创建 `configure-itick.sh`：
```bash
#!/bin/bash
# 配置 iTick API

read -p "请输入 iTick Base URL (例如 https://api.itickdata.com/v1): " BASE_URL
read -p "请输入认证方式 (bearer/api_key/param, 默认 bearer): " AUTH_TYPE
AUTH_TYPE=${AUTH_TYPE:-bearer}

# 创建配置文件
cat > /root/.openclaw/workspace/finance-dashboard-v2/.env << EOF
ITICK_API_KEY="de41c52eed6b4b9f8bb55636e3add43101a1e5f69f6b491e99192af10a4b598e"
ITICK_BASE_URL="$BASE_URL"
ITICK_AUTH_TYPE="$AUTH_TYPE"
EOF

echo "✅ 配置已保存"
echo "重启服务中..."

cd /root/.openclaw/workspace/finance-dashboard-v2
pkill -f "node.*server.js" 2>/dev/null || true
node server.js > server.log 2>&1 &

sleep 5
echo "服务已重启"
echo "检查状态: curl http://localhost:3001/api/itick-status | jq '.'"
```

## 📞 获取帮助

### 需要的信息
要正确配置 iTick，我需要以下信息：
1. **iTick 官方文档链接**
2. **正确的 API 端点 (Base URL)**
3. **认证方式** (如何在请求中包含 API 密钥)
4. **API 路径** (获取行情数据的路径)

### 如何获取这些信息
1. 登录 iTick 网站
2. 查看 "开发者文档" 或 "API 文档"
3. 查找 "Getting Started" 或 "Quick Start"
4. 查看 API 参考文档

### 临时解决方案
在找到正确的 iTick 配置前，金融看板会：
1. ✅ 继续使用 Yahoo Finance 和其他数据源
2. ✅ 使用回退数据保证服务可用
3. ✅ 保持所有监控和统计功能
4. ✅ 随时可以切换到 iTick（一旦配置正确）

## 🎯 下一步行动

### 立即行动
1. **查找 iTick API 文档** - 获取正确的端点信息
2. **测试配置** - 使用找到的信息更新配置
3. **验证连接** - 确保 iTick API 可以正常访问

### 后续优化
1. **性能调优** - 根据 iTick 的速率限制调整请求频率
2. **功能扩展** - 利用 iTick 的高级功能（历史数据、技术指标等）
3. **监控增强** - 添加 iTick 专用的监控指标

---

**当前服务状态：**
- ✅ 金融看板运行正常: http://43.156.96.119:3001
- ⚠️ iTick 已启用但未连接: 需要正确的 API 端点配置
- ✅ 备用数据源正常工作: 保证服务可用性

**需要你提供：**
iTick 的 **API 端点 (Base URL)** 信息，例如：
- `https://api.itickdata.com/v1`
- `https://data.itick.com/api/v1`
- 或其他 iTick 官方提供的端点