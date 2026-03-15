#!/bin/bash
ITICK_API_KEY="de41c52eed6b4b9f8bb55636e3add43101a1e5f69f6b491e99192af10a4b598e"
BASE_URL="https://api.itick.org"

echo "🧪 简单测试 iTick API"
echo "====================="

# 测试1: 直接访问，看看是否有文档或信息
echo -e "\n1. 直接访问根路径:"
curl -s "$BASE_URL/" | head -c 500
echo -e "\n---"

# 测试2: 尝试常见的API文档路径
echo -e "\n2. 尝试API文档路径:"
DOC_PATHS=("/docs" "/documentation" "/api-docs" "/swagger" "/openapi" "/help" "/guide")
for path in "${DOC_PATHS[@]}"; do
  echo -n "   $path ... "
  STATUS=$(curl -s -o /dev/null -w "%{http_code}" "$BASE_URL$path")
  if [ "$STATUS" = "200" ]; then
    echo "✅ 存在 (HTTP $STATUS)"
    echo "     可能有API文档: $BASE_URL$path"
  else
    echo "❌ 不存在 (HTTP $STATUS)"
  fi
done

# 测试3: 尝试带API密钥的简单请求
echo -e "\n3. 尝试带认证的请求:"
echo "   使用查询参数 apikey:"
curl -s "$BASE_URL/?apikey=$ITICK_API_KEY" | head -c 300
echo -e "\n---"

echo "   使用Bearer Token:"
curl -s -H "Authorization: Bearer $ITICK_API_KEY" "$BASE_URL/" | head -c 300
echo -e "\n---"

# 测试4: 尝试获取上证指数（常见格式）
echo -e "\n4. 尝试获取市场数据 (常见格式):"
echo "   格式1: /quote/000001"
curl -s "$BASE_URL/quote/000001?apikey=$ITICK_API_KEY" | head -c 300
echo -e "\n---"

echo "   格式2: /stock/000001/quote"
curl -s "$BASE_URL/stock/000001/quote?apikey=$ITICK_API_KEY" | head -c 300
echo -e "\n---"

echo "   格式3: /api/v1/ticker/000001"
curl -s "$BASE_URL/api/v1/ticker/000001?apikey=$ITICK_API_KEY" | head -c 300
echo -e "\n---"

echo -e "\n🎯 测试完成"
echo "如果所有测试都返回404，可能需要："
echo "1. 查看 iTick API 文档获取正确路径"
echo "2. 检查 API 密钥是否有访问权限"
echo "3. 确认 API 端点是否需要特定版本 (如 /v2/, /v3/)"