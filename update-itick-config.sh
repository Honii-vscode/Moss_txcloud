#!/bin/bash
cd /root/.openclaw/workspace/finance-dashboard-v2

echo "🔧 更新 iTick 配置为: https://api.itick.org"

# 停止当前服务
echo "🛑 停止当前服务..."
pkill -f "node.*server.js" 2>/dev/null || true
sleep 2

# 设置环境变量
export ITICK_API_KEY="de41c52eed6b4b9f8bb55636e3add43101a1e5f69f6b491e99192af10a4b598e"
export ITICK_BASE_URL="https://api.itick.org"
export ITICK_AUTH_TYPE="param"
export ITICK_AUTH_PARAM="apikey"

echo "✅ 环境变量已设置"
echo "   ITICK_BASE_URL: $ITICK_BASE_URL"
echo "   ITICK_AUTH_TYPE: $ITICK_AUTH_TYPE"

# 启动服务
echo "🚀 启动服务..."
node server.js > server.log 2>&1 &
SERVER_PID=$!

echo "   进程ID: $SERVER_PID"
echo "   日志文件: server.log"

# 等待服务启动
echo "⏳ 等待服务启动..."
for i in {1..10}; do
  if curl -s http://localhost:3001/api/health >/dev/null 2>&1; then
    echo "✅ 服务启动成功！"
    break
  fi
  echo "   等待... ($i/10)"
  sleep 2
done

# 检查状态
echo -e "\n🔍 检查服务状态:"
curl -s http://localhost:3001/api/health | jq '.status, .version, .cacheAge'

echo -e "\n📊 检查 iTick 状态:"
ITICK_STATUS=$(curl -s http://localhost:3001/api/itick-status)
echo "$ITICK_STATUS" | jq '.'

echo -e "\n📝 查看 iTick 相关日志:"
grep -i "itick" server.log | tail -5 || echo "暂无 iTick 日志"

echo -e "\n🎯 配置更新完成！"
echo "访问地址: http://43.156.96.119:3001"
echo "iTick状态: http://43.156.96.119:3001/api/itick-status"