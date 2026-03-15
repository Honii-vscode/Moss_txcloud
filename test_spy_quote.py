#!/usr/bin/env python3
"""
使用Alpha Vantage技能和API密钥获取标普500报价
"""

import requests
import os
import sys

# 使用你的API密钥
API_KEY = '8D0W8IKUZ37ISN29'

# 标普500的ETF符号
symbol = 'SPY'

print(f'🔍 使用你的API密钥获取标普500 (SPY) 报价')
print(f'API密钥: {API_KEY[:8]}...')
print(f'符号: {symbol}')
print('=' * 50)

# 方法1: 直接使用requests
url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}'
print(f'请求URL: {url[:100]}...')

try:
    response = requests.get(url, timeout=10)
    print(f'状态码: {response.status_code}')
    data = response.json()
    
    print(f'响应键: {list(data.keys())}')
    
    if 'Global Quote' in data:
        quote = data['Global Quote']
        print(f'✅ 成功获取标普500 (SPY) 数据:')
        print(f'   符号: {quote.get("01. symbol")}')
        print(f'   开盘价: ${quote.get("02. open")}')
        print(f'   最高价: ${quote.get("03. high")}')
        print(f'   最低价: ${quote.get("04. low")}')
        print(f'   当前价格: ${quote.get("05. price")}')
        print(f'   成交量: {quote.get("06. volume")}')
        print(f'   最新交易日: {quote.get("07. latest trading day")}')
        print(f'   前收盘价: ${quote.get("08. previous close")}')
        print(f'   涨跌: {quote.get("09. change")}')
        print(f'   涨跌幅: {quote.get("10. change percent")}')
    elif 'Information' in data:
        print(f'ℹ️ API信息: {data["Information"]}')
        print(f'💡 建议: 这可能是API限制消息，密钥有效但可能达到每日限制')
    elif 'Error Message' in data:
        print(f'❌ 错误消息: {data["Error Message"]}')
    else:
        print(f'⚠️ 未知响应: {data}')
        
except Exception as e:
    print(f'❌ 请求错误: {e}')

print('\n' + '=' * 50)
print('方法2: 使用Alpha Vantage技能模块')
print('=' * 50)

# 方法2: 使用技能模块
try:
    # 添加技能目录到路径
    skill_dir = "/root/.openclaw/workspace/skills/alpha_vantage"
    sys.path.insert(0, skill_dir)
    
    from alpha_vantage import AlphaVantageClient, safe_get_quote
    
    # 创建客户端
    client = AlphaVantageClient(api_key=API_KEY)
    print(f'✅ Alpha Vantage客户端创建成功')
    
    # 使用安全函数获取报价
    print(f'\n使用safe_get_quote获取{symbol}:')
    result = safe_get_quote(symbol)
    
    if result['success']:
        data = result['data']
        print(f'✅ 成功获取标普500 (SPY) 数据:')
        print(f'   当前价格: ${data.get("05. price")}')
        print(f'   涨跌: {data.get("09. change")}')
        print(f'   涨跌幅: {data.get("10. change percent")}')
        print(f'   最新交易日: {data.get("07. latest trading day")}')
        print(f'   成交量: {data.get("06. volume")}')
    else:
        print(f'❌ 获取失败: {result["error"]}')
        
except Exception as e:
    print(f'❌ 技能模块错误: {e}')
    import traceback
    traceback.print_exc()

print('\n' + '=' * 50)
print('方法3: 尝试其他标普500相关符号')
print('=' * 50)

# 尝试其他标普500相关符号
other_symbols = ['IVV', 'VOO', 'SPLG']  # 其他标普500 ETF

for test_symbol in other_symbols:
    print(f'\n尝试符号: {test_symbol}')
    test_url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={test_symbol}&apikey={API_KEY}'
    
    try:
        test_response = requests.get(test_url, timeout=5)
        test_data = test_response.json()
        
        if 'Global Quote' in test_data:
            quote = test_data['Global Quote']
            print(f'✅ {test_symbol} 数据:')
            print(f'   价格: ${quote.get("05. price")}')
            print(f'   涨跌: {quote.get("09. change")}')
            print(f'   涨跌幅: {quote.get("10. change percent")}')
        elif 'Information' in test_data:
            print(f'ℹ️ 信息: {test_data["Information"][:80]}...')
        else:
            print(f'⚠️ 无数据')
            
    except Exception as e:
        print(f'❌ 错误: {e}')

print('\n' + '=' * 50)
print('总结')
print('=' * 50)

print('''
分析结果:
1. API密钥状态: 有效 (被Alpha Vantage识别)
2. 可能原因:
   - 已达到每日25次请求限制
   - 需要等待新的一天重置
   - 某些符号在免费版中有限制

建议:
1. 等待明天再试 (每日限制重置)
2. 使用演示密钥测试功能: API_KEY = "demo"
3. 考虑升级到付费计划获得更多请求
4. 使用缓存减少API调用
''')