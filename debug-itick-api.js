const axios = require('axios');

const ITICK_API_KEY = 'de41c52eed6b4b9f8bb55636e3add43101a1e5f69f6b491e99192af10a4b598e';
const BASE_URL = 'https://api.itick.org';

// 常见的金融数据API路径模式
const COMMON_PATHS = [
  // 健康检查
  '/health',
  '/status',
  '/ping',
  '/api/health',
  '/api/status',
  '/api/ping',
  '/v1/health',
  '/v1/status',
  '/v1/ping',
  '/api/v1/health',
  '/api/v1/status',
  '/api/v1/ping',
  
  // 市场数据
  '/quote',
  '/quotes',
  '/market/quote',
  '/market/quotes',
  '/api/quote',
  '/api/quotes',
  '/api/market/quote',
  '/api/market/quotes',
  '/v1/quote',
  '/v1/quotes',
  '/v1/market/quote',
  '/v1/market/quotes',
  '/api/v1/quote',
  '/api/v1/quotes',
  '/api/v1/market/quote',
  '/api/v1/market/quotes',
  
  // 其他常见路径
  '/data',
  '/api/data',
  '/v1/data',
  '/api/v1/data',
  '/ticker',
  '/api/ticker',
  '/v1/ticker',
  '/api/v1/ticker',
  '/price',
  '/api/price',
  '/v1/price',
  '/api/v1/price'
];

// 常见的认证方式
const AUTH_METHODS = [
  { type: 'bearer', header: 'Authorization', value: `Bearer ${ITICK_API_KEY}` },
  { type: 'api_key', header: 'X-API-Key', value: ITICK_API_KEY },
  { type: 'api_key', header: 'api-key', value: ITICK_API_KEY },
  { type: 'api_key', header: 'X-API-KEY', value: ITICK_API_KEY },
  { type: 'param', param: 'apikey', value: ITICK_API_KEY },
  { type: 'param', param: 'api_key', value: ITICK_API_KEY },
  { type: 'param', param: 'token', value: ITICK_API_KEY },
  { type: 'param', param: 'access_token', value: ITICK_API_KEY }
];

async function testPath(path, authMethod) {
  const url = `${BASE_URL}${path}`;
  const config = {
    timeout: 3000,
    headers: {}
  };
  
  // 设置认证
  if (authMethod.type === 'bearer' || authMethod.type === 'api_key') {
    config.headers[authMethod.header] = authMethod.value;
  } else if (authMethod.type === 'param') {
    // 对于参数认证，需要添加到URL
    const separator = path.includes('?') ? '&' : '?';
    const testUrl = `${url}${separator}${authMethod.param}=${encodeURIComponent(authMethod.value)}`;
    return testUrlWithConfig(testUrl, config);
  }
  
  return testUrlWithConfig(url, config);
}

async function testUrlWithConfig(url, config) {
  try {
    const response = await axios.get(url, config);
    
    // 检查响应内容
    const contentType = response.headers['content-type'] || '';
    const isJson = contentType.includes('application/json');
    const data = isJson ? response.data : response.data.toString().substring(0, 200);
    
    return {
      success: true,
      status: response.status,
      data: data,
      url: url,
      headers: response.headers
    };
  } catch (error) {
    if (error.response) {
      // 服务器响应了错误状态码
      return {
        success: false,
        status: error.response.status,
        error: error.response.statusText,
        data: error.response.data,
        url: url
      };
    } else if (error.request) {
      // 请求发送了但没有收到响应
      return {
        success: false,
        status: null,
        error: 'No response',
        url: url
      };
    } else {
      // 请求配置错误
      return {
        success: false,
        status: null,
        error: error.message,
        url: url
      };
    }
  }
}

async function discoverITickAPI() {
  console.log('🔍 探索 iTick API 结构...');
  console.log(`基础URL: ${BASE_URL}`);
  console.log(`API密钥: ${ITICK_API_KEY.substring(0, 20)}...\n`);
  
  let foundPaths = [];
  
  // 首先测试根路径
  console.log('1. 测试根路径:');
  for (const authMethod of AUTH_METHODS) {
    const result = await testPath('/', authMethod);
    if (result.status !== 404) {
      console.log(`   ${authMethod.type} (${authMethod.header || authMethod.param}): HTTP ${result.status}`);
      if (result.success) {
        console.log(`   ✅ 发现有效响应: ${JSON.stringify(result.data).substring(0, 100)}...`);
        foundPaths.push({ path: '/', authMethod, result });
      }
    }
  }
  
  // 测试常见路径
  console.log('\n2. 测试常见API路径:');
  for (const path of COMMON_PATHS) {
    let found = false;
    
    for (const authMethod of AUTH_METHODS) {
      const result = await testPath(path, authMethod);
      
      if (result.status !== 404) {
        if (!found) {
          console.log(`\n   📍 路径: ${path}`);
          found = true;
        }
        
        console.log(`     认证: ${authMethod.type} (${authMethod.header || authMethod.param}) → HTTP ${result.status}`);
        
        if (result.success) {
          console.log(`     ✅ 成功! 响应: ${JSON.stringify(result.data).substring(0, 150)}...`);
          foundPaths.push({ path, authMethod, result });
          break; // 找到成功响应就跳过其他认证方式
        } else if (result.status === 401 || result.status === 403) {
          console.log(`     🔐 需要认证 (路径存在)`);
          foundPaths.push({ path, authMethod, result });
        }
      }
    }
    
    // 限制请求频率
    await new Promise(resolve => setTimeout(resolve, 100));
  }
  
  // 输出发现结果
  console.log('\n🎯 探索结果:');
  if (foundPaths.length > 0) {
    console.log(`找到 ${foundPaths.length} 个有效路径:`);
    
    foundPaths.forEach((item, index) => {
      console.log(`\n${index + 1}. 路径: ${item.path}`);
      console.log(`   认证: ${item.authMethod.type} (${item.authMethod.header || item.authMethod.param})`);
      console.log(`   状态: HTTP ${item.result.status}`);
      
      if (item.result.success) {
        console.log(`   ✅ 可用!`);
        
        // 检查是否是市场数据API
        const data = item.result.data;
        if (data && typeof data === 'object') {
          const hasPrice = data.price || data.last_price || data.lastPrice;
          const hasSymbol = data.symbol || data.code;
          
          if (hasPrice || hasSymbol) {
            console.log(`   📊 看起来是市场数据API`);
            console.log(`      价格字段: ${hasPrice || '未找到'}`);
            console.log(`      符号字段: ${hasSymbol || '未找到'}`);
          }
        }
      } else if (item.result.status === 401 || item.result.status === 403) {
        console.log(`   🔐 需要正确认证 (路径存在)`);
      }
    });
    
    // 生成配置建议
    console.log('\n💡 配置建议:');
    const successfulPaths = foundPaths.filter(item => item.result.success);
    if (successfulPaths.length > 0) {
      const best = successfulPaths[0];
      console.log(`export ITICK_BASE_URL="${BASE_URL}"`);
      console.log(`export ITICK_API_KEY="${ITICK_API_KEY}"`);
      console.log(`export ITICK_AUTH_TYPE="${best.authMethod.type}"`);
      
      if (best.authMethod.type === 'bearer' || best.authMethod.type === 'api_key') {
        console.log(`export ITICK_AUTH_HEADER="${best.authMethod.header}"`);
      } else if (best.authMethod.type === 'param') {
        console.log(`export ITICK_AUTH_PARAM="${best.authMethod.param}"`);
      }
      
      // 猜测API端点
      const path = best.path;
      if (path.includes('/quote')) {
        console.log(`export ITICK_QUOTE_ENDPOINT="${path}"`);
      } else if (path.includes('/health') || path.includes('/status') || path.includes('/ping')) {
        console.log(`export ITICK_HEALTH_ENDPOINT="${path}"`);
      }
    }
  } else {
    console.log('❌ 未找到有效的API路径');
    console.log('可能原因:');
    console.log('1. iTick API 需要特定的请求参数');
    console.log('2. API 密钥无效或已过期');
    console.log('3. 需要查看 iTick 官方文档获取正确路径');
    console.log('4. API 可能需要特定的请求方法 (POST 而不是 GET)');
  }
}

// 运行探索
discoverITickAPI().catch(console.error);