# iTick 数据源集成实施指南

## 🎯 目标
将 iTick 金融数据源集成到金融看板中，提供更稳定、实时的市场数据。

## 📋 实施步骤

### 阶段一：获取 iTick API 访问权限

#### 1. 注册 iTick 账号
- 访问 iTick 官方网站（需要确认具体网址）
- 完成注册流程
- 验证邮箱和身份信息

#### 2. 获取 API 密钥
- 登录 iTick 开发者控制台
- 创建新的 API 应用
- 获取 API 密钥（通常格式：`itk_xxxxxxxxxxxxxxxx`）
- 记录 API 密钥和安全注意事项

#### 3. 了解 API 限制
- 免费额度：请求次数/时间限制
- 数据范围：支持的交易所和品种
- 更新频率：实时/延迟数据
- 认证方式：API Key、Token 等

### 阶段二：测试 iTick API

#### 1. 环境准备
```bash
# 设置环境变量
export ITICK_API_KEY="your_itick_api_key_here"
export ITICK_BASE_URL="https://api.itick.com/v1"  # 根据实际文档调整

# 测试连接
curl -X GET "${ITICK_BASE_URL}/health?apikey=${ITICK_API_KEY}"
```

#### 2. 测试数据获取
```bash
# 测试获取上证指数
curl -X GET "${ITICK_BASE_URL}/market/quote?symbol=000001&exchange=SSE&apikey=${ITICK_API_KEY}"

# 测试获取标普500
curl -X GET "${ITICK_BASE_URL}/market/quote?symbol=SPX&exchange=INDEX&apikey=${ITICK_API_KEY}"
```

#### 3. 验证数据格式
检查响应数据是否包含以下字段：
- `last_price` 或 `price`：最新价格
- `change`：涨跌额
- `change_percent` 或 `change_percentage`：涨跌幅
- `volume`：成交量
- `timestamp`：时间戳

### 阶段三：集成到金融看板

#### 1. 更新服务器配置
```bash
# 停止当前服务器
pkill -f "node.*server.js"

# 备份当前配置
cd /root/.openclaw/workspace/finance-dashboard-v2
cp server.js server-backup.js

# 使用集成iTick的版本
cp server-with-itick.js server.js

# 设置环境变量
export ITICK_API_KEY="your_actual_itick_api_key"
# 可选：设置其他API密钥
export TWELVE_DATA_API_KEY="your_twelve_data_key"
export FINNHUB_API_KEY="your_finnhub_key"

# 启动服务器
node server.js &
```

#### 2. 验证集成
```bash
# 检查服务器状态
curl http://localhost:3001/api/health

# 检查iTick状态
curl http://localhost:3001/api/itick-status

# 获取市场数据
curl http://localhost:3001/api/market-data | jq '.config.itickEnabled'
```

#### 3. 监控数据质量
```bash
# 查看数据源统计
curl http://localhost:3001/api/stats | jq '.sourceStats'

# 检查缓存状态
curl http://localhost:3001/api/health | jq '.cacheAge, .dataCount'
```

### 阶段四：优化与监控

#### 1. 性能优化
- 调整缓存时间（根据 iTick 的更新频率）
- 优化重试策略（根据 iTick 的错误响应）
- 批量请求优化（如果 iTick 支持批量API）

#### 2. 错误处理
- 实现优雅降级（iTick 失败时自动切换到备用数据源）
- 添加告警机制（API 失败率超过阈值时通知）
- 日志记录（记录所有 API 调用和错误）

#### 3. 监控指标
- API 响应时间
- 数据更新成功率
- 缓存命中率
- 各数据源使用比例

## 🔧 配置文件详解

### 1. 环境变量配置
```bash
# iTick 配置
export ITICK_API_KEY="itk_xxxxxxxxxxxxxxxx"
export ITICK_BASE_URL="https://api.itick.com/v1"  # 可选，默认值

# 其他数据源（可选）
export TWELVE_DATA_API_KEY="twelve_data_key"
export FINNHUB_API_KEY="finnhub_key"

# 服务器配置
export PORT=3001  # 服务器端口
export NODE_ENV=production  # 运行环境
```

### 2. 服务器配置（server-with-itick.js）
```javascript
const CONFIG = {
  // 缓存配置：10分钟
  cacheDuration: 10 * 60 * 1000,
  
  // 数据源优先级
  dataSources: [
    'itick',           // 最高优先级
    'yahoo_finance',   // 备用1
    'twelve_data',     // 备用2（需要API密钥）
    'finnhub',         // 备用3（需要API密钥）
    'fallback'         // 最终回退
  ],
  
  // iTick 专用配置
  itick: {
    enabled: !!process.env.ITICK_API_KEY,  // 自动检测
    apiKey: process.env.ITICK_API_KEY || '',
    priority: 1  // 最高优先级
  }
};
```

### 3. 符号映射配置
```javascript
// iTick 符号映射（需要根据实际API调整）
const symbolMapping = {
  // 标准符号: { itickSymbol: 'iTick符号', exchange: '交易所', type: '类型' }
  '000001.SS': { itickSymbol: '000001', exchange: 'SSE', type: 'STOCK' },
  '^GSPC': { itickSymbol: 'SPX', exchange: 'INDEX', type: 'INDEX' },
  'BTC-USD': { itickSymbol: 'BTCUSD', exchange: 'CRYPTO', type: 'CRYPTO' },
  // ... 其他符号
};
```

## 🚀 快速部署脚本

创建部署脚本 `deploy-itick.sh`：

```bash
#!/bin/bash
# deploy-itick.sh - 部署集成iTick的金融看板

set -e

echo "🚀 开始部署集成iTick的金融看板..."

# 检查环境变量
if [ -z "$ITICK_API_KEY" ]; then
  echo "❌ 错误：未设置 ITICK_API_KEY 环境变量"
  echo "💡 请先执行：export ITICK_API_KEY='your_itick_api_key'"
  exit 1
fi

echo "✅ 检测到 iTick API 密钥"

# 进入项目目录
cd /root/.openclaw/workspace/finance-dashboard-v2

# 停止现有服务
echo "🛑 停止现有服务..."
pkill -f "node.*server.js" || true
sleep 2

# 备份当前配置
echo "💾 备份当前配置..."
if [ -f "server.js" ]; then
  cp server.js "server-backup-$(date +%Y%m%d-%H%M%S).js"
fi

# 使用集成iTick的版本
echo "🔧 配置iTick集成..."
cp server-with-itick.js server.js

# 启动服务
echo "🚀 启动服务..."
export ITICK_API_KEY="$ITICK_API_KEY"
export TWELVE_DATA_API_KEY="${TWELVE_DATA_API_KEY:-}"
export FINNHUB_API_KEY="${FINNHUB_API_KEY:-}"
export PORT=3001

node server.js > server.log 2>&1 &

# 等待服务启动
echo "⏳ 等待服务启动..."
sleep 5

# 检查服务状态
echo "🔍 检查服务状态..."
if curl -s http://localhost:3001/api/health > /dev/null; then
  echo "✅ 服务启动成功！"
  echo "📊 访问地址：http://43.156.96.119:3001"
  echo "🔧 iTick状态：http://43.156.96.119:3001/api/itick-status"
else
  echo "❌ 服务启动失败，查看日志：tail -f server.log"
  exit 1
fi

echo "🎉 部署完成！"
```

## 📊 验证与测试

### 1. 功能测试
```bash
# 测试1：基本功能
curl -s http://localhost:3001/ | grep -q "金融看板" && echo "✅ 前端页面正常"

# 测试2：API接口
curl -s http://localhost:3001/api/market-data | jq -e '.success' && echo "✅ API接口正常"

# 测试3：iTick集成
curl -s http://localhost:3001/api/itick-status | jq -e '.enabled' && echo "✅ iTick集成正常"
```

### 2. 性能测试
```bash
# 响应时间测试
time curl -s -o /dev/null http://localhost:3001/api/market-data

# 并发测试（简单版本）
for i in {1..10}; do
  curl -s -o /dev/null http://localhost:3001/api/health &
done
wait
```

### 3. 数据质量测试
```bash
# 检查数据完整性
curl -s http://localhost:3001/api/market-data | jq '.data | keys'

# 检查数据时效性
curl -s http://localhost:3001/api/market-data | jq '.cacheAge'

# 检查数据源分布
curl -s http://localhost:3001/api/market-data | jq '.data | to_entries[] | .value.source' | sort | uniq -c
```

## ⚠️ 故障排除

### 常见问题1：iTick API 连接失败
```
症状：/api/itick-status 返回 unhealthy
解决：
1. 检查 ITICK_API_KEY 是否正确
2. 检查网络连接：curl https://api.itick.com
3. 检查 API 额度是否用完
4. 查看服务器日志：tail -f server.log
```

### 常见问题2：数据格式不匹配
```
症状：iTick 返回数据但解析失败
解决：
1. 检查 iTick API 文档，确认响应格式
2. 更新 itick-integration.js 中的 parseQuoteResponse 函数
3. 测试单个符号：node -e "require('./itick-integration').testITickIntegration()"
```

### 常见问题3：性能问题
```
症状：API 响应慢或超时
解决：
1. 增加缓存时间：修改 CONFIG.cacheDuration
2. 优化重试策略：减少 maxRetries 或增加 retryDelay
3. 考虑使用批量 API（如果 iTick 支持）
4. 添加请求限流
```

### 常见问题4：数据不一致
```
症状：不同数据源显示不同价格
解决：
1. 检查时区设置：确保所有时间戳使用 UTC
2. 验证数据延迟：iTick 可能是实时，其他源可能有延迟
3. 设置数据源优先级：确保使用最可靠的数据源
4. 添加数据验证逻辑：价格变化过大时记录警告
```

## 📈 监控与维护

### 1. 监控面板
创建简单的监控脚本 `monitor.sh`：

```bash
#!/bin/bash
# monitor.sh - 监控金融看板状态

echo "📊 金融看板监控报告"
echo "=================="

# 基本健康检查
HEALTH=$(curl -s http://localhost:3001/api/health)
echo "1. 服务状态: $(echo $HEALTH | jq -r '.status')"
echo "2. 运行时间: $(echo $HEALTH | jq -r '.uptime | floor')秒"
echo "3. 缓存年龄: $(echo $HEALTH | jq -r '.cacheAge')秒"
echo "4. 数据数量: $(echo $HEALTH | jq -r '.dataCount')"

# iTick 状态
ITICK=$(curl -s http://localhost:3001/api/itick-status)
echo "5. iTick 启用: $(echo $ITICK | jq -r '.enabled')"
echo "6. iTick 健康: $(echo $ITICK | jq -r '.health.status')"

# 数据源统计
STATS=$(curl -s http://localhost:3001/api/stats)
echo -e "\n📈 数据源统计:"
echo $STATS | jq -r '.sourceStats | to_entries[] | "  \(.key): \(.value.success)/\(.value.total) (\(if .value.total > 0 then (.value.success/.value.total*100) else 0 end | floor)%)"'

# 内存使用
echo -e "\n💾 内存使用:"
echo $HEALTH | jq -r '.memory | "  堆使用: \(.heapUsed/1024/1024 | floor)MB / \(.heapTotal/1024/1024 | floor)MB"'
```

### 2. 日志管理
```bash
# 日志轮转配置
# 在 /etc/logrotate.d/finance-dashboard 中添加：
/root/.openclaw/workspace/finance-dashboard-v2/server.log {
    daily
    rotate 7
    compress
    delaycompress
    missingok
    notifempty
    create 644 root root
}
```

### 3. 自动告警
创建告警脚本 `alert.sh`：

```bash
#!/bin/bash
# alert.sh - 检查异常并发送告警

THRESHOLD=300  # 缓存最大年龄（秒）
HEALTH_URL="http://localhost:3001/api/health"

# 检查服务是否运行
if ! curl -s --max-time 5 $HEALTH_URL > /dev/null; then
  echo "🚨 告警：金融看板服务不可用"
  # 这里可以添加邮件、钉钉、微信等告警
  exit 1
fi

# 检查缓存年龄
CACHE_AGE=$(curl -s $HEALTH_URL | jq -r '.cacheAge')
if [ "$CACHE_AGE" != "null" ] && [ "$CACHE_AGE" -gt "$THRESHOLD" ]; then
  echo "⚠️ 警告：数据缓存年龄 ${CACHE_AGE}秒，超过阈值 ${THRESHOLD}秒"
fi

# 检查数据数量
DATA_COUNT=$(curl -s $HEALTH_URL | jq -r '.dataCount')
if [ "$DATA_COUNT" -lt 5 ]; then
  echo "⚠️ 警告：数据数量不足，只有 ${DATA_COUNT} 条"
fi
```

## 🎯 成功标准

### 技术指标
1. ✅ API 可用性 > 99.9%
2. ✅ 平均响应时间 < 500ms
3. ✅ 数据更新延迟 < 60秒
4. ✅ 错误率 < 1%

### 业务指标
1. ✅ 24小时不间断服务
2. ✅ 数据准确性 > 99%
3. ✅ 支持10+个市场品种
4. ✅ 用户访问体验良好

### 运维指标
1. ✅ 监控覆盖率 100%
2. ✅ 告警响应时间 < 5分钟
3. ✅ 故障恢复时间 < 10分钟
4. ✅ 日志保留时间 > 30天

## 🔄 更新与升级

### 定期维护任务
```bash
# 每周任务
1. 检查 API 密钥有效期
2. 清理旧日志文件
3. 更新依赖包版本
4. 备份配置文件

# 每月任务
1. 评估数据源质量
2. 优化性能参数
3. 更新监控指标
4. 安全漏洞扫描
```

### 版本升级
```bash
# 升级步骤
1. 备份当前版本
2. 测试新版本功能
3. 灰度发布（部分用户）
4. 全量发布
5. 监控运行状态
6. 回滚计划（如果需要）
```

---

## 📞 支持与资源

### 官方资源
- iTick 官方网站：[需要确认]
- iTick API 文档：[需要确认]
- iTick 技术支持：[需要确认]

### 项目资源
- 项目代码：`/root/.openclaw/workspace/finance-dashboard-v2/`
- 配置文件：`server-with-itick.js`, `itick-integration.js`
- 文档文件：`itick-implementation-guide.md`
- 部署脚本：`deploy-itick.sh`
- 监控脚本：`monitor.sh`, `alert.sh`

### 联系信息
- 服务器地址：http://43.156.96.119:3001
- 健康检查：http://43.156.96.119:3001/api/health
- iTick状态：http://43.156.96.119:3001/api/itick-status

---

**下一步行动：**
1. 获取 iTick API 密钥
2. 测试 iTick API 连通性
3. 部署集成版本
4. 验证数据质量和稳定性
5. 设置监控和告警