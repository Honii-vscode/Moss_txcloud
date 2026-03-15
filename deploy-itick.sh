#!/bin/bash
# deploy-itick.sh - 部署集成iTick的金融看板

set -e

echo "🚀 开始部署集成iTick的金融看板..."

# 设置iTick API密钥
export ITICK_API_KEY="de41c52eed6b4b9f8bb55636e3add43101a1e5f69f6b491e99192af10a4b598e"

echo "✅ 使用提供的 iTick API 密钥"
echo "   密钥前20位: ${ITICK_API_KEY:0:20}..."

# 进入项目目录
cd /root/.openclaw/workspace/finance-dashboard-v2

# 停止现有服务
echo "🛑 停止现有服务..."
pkill -f "node.*server.js" || true
sleep 2

# 备份当前配置
echo "💾 备份当前配置..."
if [ -f "server.js" ]; then
  BACKUP_FILE="server-backup-$(date +%Y%m%d-%H%M%S).js"
  cp server.js "$BACKUP_FILE"
  echo "   备份到: $BACKUP_FILE"
fi

# 使用集成iTick的版本
echo "🔧 配置iTick集成..."
if [ -f "server-with-itick.js" ]; then
  cp server-with-itick.js server.js
  echo "   使用 server-with-itick.js"
else
  echo "❌ 错误：server-with-itick.js 不存在"
  exit 1
fi

# 设置其他环境变量（可选）
export TWELVE_DATA_API_KEY="${TWELVE_DATA_API_KEY:-}"
export FINNHUB_API_KEY="${FINNHUB_API_KEY:-}"
export PORT=3001

# 启动服务
echo "🚀 启动服务..."
node server.js > server.log 2>&1 &
SERVER_PID=$!

echo "   进程ID: $SERVER_PID"
echo "   日志文件: server.log"

# 等待服务启动
echo "⏳ 等待服务启动..."
for i in {1..10}; do
  if curl -s http://localhost:3001/api/health > /dev/null 2>&1; then
    echo "✅ 服务启动成功！"
    break
  fi
  echo "   等待... ($i/10)"
  sleep 2
done

# 检查服务状态
echo "🔍 检查服务状态..."
if curl -s http://localhost:3001/api/health > /dev/null; then
  echo "✅ 服务运行正常"
else
  echo "❌ 服务启动失败"
  echo "   查看日志: tail -f server.log"
  exit 1
fi

# 检查iTick状态
echo "🔧 检查iTick集成状态..."
ITICK_STATUS=$(curl -s http://localhost:3001/api/itick-status)
ITICK_ENABLED=$(echo "$ITICK_STATUS" | jq -r '.enabled' 2>/dev/null || echo "error")

if [ "$ITICK_ENABLED" = "true" ]; then
  echo "✅ iTick 已启用"
  ITICK_HEALTH=$(echo "$ITICK_STATUS" | jq -r '.health.status' 2>/dev/null || echo "unknown")
  echo "   iTick 健康状态: $ITICK_HEALTH"
elif [ "$ITICK_ENABLED" = "false" ]; then
  echo "⚠️ iTick 未启用（可能API端点配置不正确）"
else
  echo "❌ 无法获取iTick状态"
fi

# 获取市场数据测试
echo "📊 测试市场数据获取..."
MARKET_DATA=$(curl -s http://localhost:3001/api/market-data)
DATA_COUNT=$(echo "$MARKET_DATA" | jq -r '.count' 2>/dev/null || echo "0")
SUCCESS=$(echo "$MARKET_DATA" | jq -r '.success' 2>/dev/null || echo "false")

if [ "$SUCCESS" = "true" ]; then
  echo "✅ 市场数据获取成功"
  echo "   数据条数: $DATA_COUNT"
  
  # 显示数据源统计
  echo "📈 数据源使用情况:"
  echo "$MARKET_DATA" | jq -r '.sourceStats | to_entries[] | "   \(.key): \(.value.success)/\(.value.total)"' 2>/dev/null || echo "   暂无统计信息"
else
  echo "⚠️ 市场数据获取失败，但服务仍在运行"
  ERROR_MSG=$(echo "$MARKET_DATA" | jq -r '.error // .message' 2>/dev/null || echo "未知错误")
  echo "   错误信息: $ERROR_MSG"
fi

echo ""
echo "🎉 部署完成！"
echo ""
echo "📱 访问地址："
echo "   主页面: http://43.156.96.119:3001"
echo "   API数据: http://43.156.96.119:3001/api/market-data"
echo "   健康检查: http://43.156.96.119:3001/api/health"
echo "   iTick状态: http://43.156.96.119:3001/api/itick-status"
echo ""
echo "🔧 管理命令："
echo "   查看日志: tail -f server.log"
echo "   重启服务: pkill -f 'node.*server.js' && node server.js > server.log 2>&1 &"
echo "   停止服务: pkill -f 'node.*server.js'"
echo ""
echo "💡 提示："
echo "   1. iTick API端点可能需要根据官方文档调整"
echo "   2. 查看 server.log 获取详细错误信息"
echo "   3. 可以设置 ITICK_BASE_URL 环境变量调整API端点"