const axios = require('axios');

const ITICK_API_KEY = 'de41c52eed6b4b9f8bb55636e3add43101a1e5f69f6b491e99192af10a4b598e';

// 常见的 iTick API 端点猜测
const API_ENDPOINTS = [
  'https://api.itick.com/v1',
  'https://api.itickdata.com/v1',
  'https://data.itick.com/api/v1',
  'https://open.itick.com/api',
  'https://itick-api.com/v1',
  'https://api.itick.cn/v1',
  'https://data.itick.cn/api/v1'
];

// 常见的健康检查路径
const HEALTH_PATHS = [
  '/health',
  '/status',
  '/ping',
  '/api/health',
  '/market/health',
  '/v1/health'
];

async function testEndpoint(baseUrl, path) {
  const url = `${baseUrl}${path}`;
  
  try {
    console.log(`测试: ${url}`);
    
    // 尝试不同的认证方式
    const configs = [
      { headers: { 'Authorization': `Bearer ${ITICK_API_KEY}` } },
      { headers: { 'X-API-Key': ITICK_API_KEY } },
      { headers: { 'api-key': ITICK_API_KEY } },
      { params: { apikey: ITICK_API_KEY } },
      { params: { token: ITICK_API_KEY } }
    ];
    
    for (const config of configs) {
      try {
        const response = await axios.get(url, {
          ...config,
          timeout: 3000
        });
        
        console.log(`✅ 成功！认证方式: ${JSON.stringify(config.headers || config.params)}`);
        console.log(`   状态码: ${response.status}`);
        console.log(`   响应: ${JSON.stringify(response.data).substring(0, 200)}...`);
        return { success: true, url, config };
      } catch (error) {
        if (error.response) {
          console.log(`   ❌ ${error.response.status}: ${error.response.statusText}`);
        }
      }
    }
  } catch (error) {
    if (error.code === 'ECONNREFUSED' || error.code === 'ENOTFOUND') {
      console.log(`   ❌ 无法连接`);
    } else {
      console.log(`   ❌ ${error.message}`);
    }
  }
  
  return { success: false, url };
}

async function discoverITickAPI() {
  console.log('🔍 探索 iTick API 端点...\n');
  
  for (const baseUrl of API_ENDPOINTS) {
    console.log(`\n=== 测试基础URL: ${baseUrl} ===`);
    
    for (const path of HEALTH_PATHS) {
      const result = await testEndpoint(baseUrl, path);
      if (result.success) {
        console.log(`\n🎉 找到可用的 iTick API 端点: ${result.url}`);
        console.log(`   认证配置: ${JSON.stringify(result.config)}`);
        return result;
      }
    }
  }
  
  console.log('\n❌ 未找到可用的 iTick API 端点');
  console.log('可能需要：');
  console.log('1. 检查网络连接');
  console.log('2. 确认 iTick 官方网站');
  console.log('3. 查看 API 文档获取正确端点');
  
  return null;
}

// 运行探索
discoverITickAPI().then(result => {
  if (result) {
    console.log('\n✅ iTick API 发现完成！');
    console.log('建议配置：');
    console.log(`export ITICK_BASE_URL="${result.url.replace(/\/health$/, '').replace(/\/status$/, '').replace(/\/ping$/, '')}"`);
  } else {
    console.log('\n⚠️ 需要手动查找 iTick API 信息');
  }
}).catch(error => {
  console.error('探索过程中出错:', error);
});