#!/bin/bash
cd /root/.openclaw/workspace/finance-dashboard-v2

echo "🎯 配置 iTick API 集成"
echo "======================"

# 停止当前服务
echo "🛑 停止当前服务..."
pkill -f "node.*server.js" 2>/dev/null || true
sleep 2

# 设置环境变量 - 基于测试结果
export ITICK_API_KEY="de41c52eed6b4b9f8bb55636e3add43101a1e5f69f6b491e99192af10a4b598e"
export ITICK_BASE_URL="https://api.itick.org"
export ITICK_AUTH_TYPE="param"
export ITICK_AUTH_PARAM="apikey"
export ITICK_QUOTE_ENDPOINT="/stock/{symbol}/quote"
export ITICK_HEALTH_ENDPOINT="/stock/AAPL/quote"  # 使用已知符号测试健康检查

echo "✅ 环境变量已设置:"
echo "   ITICK_BASE_URL: $ITICK_BASE_URL"
echo "   ITICK_AUTH_TYPE: $ITICK_AUTH_TYPE"
echo "   ITICK_AUTH_PARAM: $ITICK_AUTH_PARAM"
echo "   ITICK_QUOTE_ENDPOINT: $ITICK_QUOTE_ENDPOINT"

# 修改 iTick 集成代码以使用新路径
echo "🔧 更新 iTick 集成代码..."
cat > itick-integration-fixed.js << 'EOF'
// iTick 集成 - 针对 api.itick.org 优化
const axios = require('axios');

const ITICK_CONFIG = {
  apiKey: process.env.ITICK_API_KEY || '',
  baseUrl: process.env.ITICK_BASE_URL || 'https://api.itick.org',
  
  // 认证方式
  authType: process.env.ITICK_AUTH_TYPE || 'param',
  authParam: process.env.ITICK_AUTH_PARAM || 'apikey',
  
  // API端点
  endpoints: {
    quote: process.env.ITICK_QUOTE_ENDPOINT || '/stock/{symbol}/quote',
    health: process.env.ITICK_HEALTH_ENDPOINT || '/stock/AAPL/quote'
  },
  
  timeout: 5000,
  maxRetries: 2
};

class ITickClient {
  constructor(config = ITICK_CONFIG) {
    this.config = config;
  }
  
  isValid() {
    return !!this.config.apiKey && this.config.apiKey.length > 10;
  }
  
  // 获取实时报价
  async getRealTimeQuote(symbol) {
    if (!this.isValid()) return null;
    
    // 转换符号格式
    const itickSymbol = this.convertSymbol(symbol);
    if (!itickSymbol) return null;
    
    // 构建URL
    let url = this.config.endpoints.quote.replace('{symbol}', itickSymbol);
    url = `${this.config.baseUrl}${url}`;
    
    // 添加认证参数
    const params = {};
    if (this.config.authType === 'param') {
      params[this.config.authParam] = this.config.apiKey;
    }
    
    try {
      console.log(`🔍 iTick请求: ${url}`);
      const response = await axios.get(url, {
        params,
        timeout: this.config.timeout
      });
      
      console.log(`✅ iTick响应: HTTP ${response.status}`);
      return this.parseResponse(response.data, symbol);
      
    } catch (error) {
      console.log(`❌ iTick错误: ${error.message}`);
      if (error.response) {
        console.log(`   状态码: ${error.response.status}`);
        console.log(`   响应: ${JSON.stringify(error.response.data)}`);
      }
      return null;
    }
  }
  
  // 转换符号格式
  convertSymbol(symbol) {
    const mapping = {
      '000001.SS': '000001',
      '^GSPC': 'SPX',
      '^IXIC': 'NDX',
      '^DJI': 'DJI',
      'GC=F': 'XAU',
      'BTC-USD': 'BTC',
      'ETH-USD': 'ETH',
      'USDCNY': 'USDCNY'
    };
    return mapping[symbol] || symbol.replace(/[^a-zA-Z0-9]/g, '');
  }
  
  // 解析响应
  parseResponse(data, originalSymbol) {
    // 尝试解析不同的响应格式
    let price, change, changePercent;
    
    if (data.price !== undefined) {
      price = data.price;
      change = data.change;
      changePercent = data.changePercent;
    } else if (data.last_price !== undefined) {
      price = data.last_price;
      change = data.change;
      changePercent = data.change_percent;
    } else if (data.data && data.data.price) {
      price = data.data.price;
      change = data.data.change;
      changePercent = data.data.changePercent;
    }
    
    if (price === undefined) {
      console.log(`⚠️ 无法解析iTick响应: ${JSON.stringify(data)}`);
      return null;
    }
    
    return {
      name: this.getStockName(originalSymbol),
      symbol: originalSymbol,
      price: parseFloat(price),
      change: change ? parseFloat(change) : 0,
      changePercent: changePercent ? parseFloat(changePercent) : 0,
      source: 'itick',
      timestamp: new Date().toISOString()
    };
  }
  
  getStockName(symbol) {
    const names = {
      '000001.SS': '上证指数',
      '^GSPC': '标普 500',
      '^IXIC': '纳斯达克',
      '^DJI': '道琼斯',
      'GC=F': '黄金',
      'BTC-USD': '比特币',
      'ETH-USD': '以太坊'
    };
    return names[symbol] || symbol;
  }
  
  // 健康检查
  async healthCheck() {
    try {
      const url = `${this.config.baseUrl}${this.config.endpoints.health}`;
      const params = {};
      if (this.config.authType === 'param') {
        params[this.config.authParam] = this.config.apiKey;
      }
      
      const response = await axios.get(url, {
        params,
        timeout: 3000
      });
      
      return {
        status: response.status === 200 ? 'healthy' : 'unhealthy',
        message: `HTTP ${response.status}`,
        data: response.data
      };
    } catch (error) {
      return {
        status: 'unhealthy',
        message: error.message,
        error: error.response?.data || error.message
      };
    }
  }
}

// 导出
module.exports = {
  ITickClient,
  fetchFromITick: async (symbol) => {
    const client = new ITickClient();
    return client.getRealTimeQuote(symbol);
  }
};
EOF

# 替换原来的集成文件
cp itick-integration-fixed.js itick-integration.js
echo "✅ iTick 集成代码已更新"

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
curl -s http://localhost:3001/api/health | jq '.status, .version, .uptime'

echo -e "\n📊 检查 iTick 状态:"
ITICK_STATUS=$(curl -s http://localhost:3001/api/itick-status)
echo "$ITICK_STATUS" | jq '.'

# 手动测试 iTick
echo -e "\n🧪 手动测试 iTick 数据获取:"
echo "   测试上证指数..."
curl -s "http://localhost:3001/api/test-itick?symbol=000001.SS" 2>/dev/null || echo "测试端点未实现"

# 查看日志
echo -e "\n📝 查看最新日志:"
tail -20 server.log | grep -i "itick\|iTick" || echo "暂无 iTick 相关日志"

echo -e "\n🎯 配置完成！"
echo "访问地址: http://43.156.96.119:3001"
echo "iTick状态: http://43.156.96.119:3001/api/itick-status"
echo -e "\n💡 如果 iTick 仍然返回 'auth failed'，可能需要："
echo "1. 检查 API 密钥是否有效"
echo "2. 查看 iTick 控制台确认密钥状态"
echo "3. 联系 iTick 技术支持"