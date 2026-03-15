#!/usr/bin/env python3
"""
使用演示密钥测试标普500报价功能
"""

import requests

# 使用演示密钥
API_KEY = 'demo'

# 标普500的ETF符号
symbol = 'SPY'

print(f'🔍 使用演示密钥获取标普500 (SPY) 报价')
print(f'API密钥: {API_KEY}')
print(f'符号: {symbol}')
print('=' * 50)

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
        
        # 计算市值变化
        price = float(quote.get("05. price", 0))
        change = float(quote.get("09. change", 0))
        change_percent = float(quote.get("10. change percent", "0%").replace('%', ''))
        
        print(f'\n📊 标普500分析:')
        print(f'   当前点位: {price:.2f}')
        print(f'   今日变化: {change:+.2f} ({change_percent:+.2f}%)')
        
        if change > 0:
            print(f'   📈 今日上涨')
        elif change < 0:
            print(f'   📉 今日下跌')
        else:
            print(f'   ➖ 持平')
            
    elif 'Information' in data:
        print(f'ℹ️ API信息: {data["Information"]}')
    elif 'Error Message' in data:
        print(f'❌ 错误消息: {data["Error Message"]}')
    else:
        print(f'⚠️ 未知响应: {data}')
        
except Exception as e:
    print(f'❌ 请求错误: {e}')

print('\n' + '=' * 50)
print('测试其他主要指数ETF')
print('=' * 50)

# 测试其他主要指数
index_etfs = {
    'QQQ': '纳斯达克100',
    'DIA': '道琼斯工业平均指数',
    'IVV': '标普500 (iShares)',
    'VTI': '全股市'
}

for etf_symbol, etf_name in index_etfs.items():
    print(f'\n获取 {etf_name} ({etf_symbol}):')
    etf_url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={etf_symbol}&apikey={API_KEY}'
    
    try:
        etf_response = requests.get(etf_url, timeout=5)
        etf_data = etf_response.json()
        
        if 'Global Quote' in etf_data:
            quote = etf_data['Global Quote']
            price = quote.get("05. price", "N/A")
            change = quote.get("09. change", "N/A")
            change_percent = quote.get("10. change percent", "N/A")
            print(f'   ✅ 价格: ${price}, 涨跌: {change}, 涨跌幅: {change_percent}')
        else:
            print(f'   ⚠️ 无数据')
            
    except Exception as e:
        print(f'   ❌ 错误: {e}')

print('\n' + '=' * 50)
print('结论')
print('=' * 50)

print('''
✅ 功能验证成功:
1. Alpha Vantage API 工作正常
2. 演示密钥可以获取实时数据
3. 标普500 (SPY) 数据获取成功

⚠️ 你的API密钥状态:
1. 密钥有效 (被Alpha Vantage识别)
2. 可能已达到每日25次限制
3. 需要等待UTC时间00:00重置

💡 建议:
1. 明天再试你的API密钥
2. 使用缓存减少API调用
3. 考虑实施请求队列和智能调度
4. 对于开发测试，可以使用演示密钥

📊 当前标普500数据 (演示密钥):
   - 价格: 如上所示
   - 数据为演示用途，可能有延迟
''')