#!/usr/bin/env python3
"""
Alpha Vantage 技能使用示例
"""

import sys
import os

# 添加当前目录到路径
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from alpha_vantage import (
    get_stock_quote,
    get_daily,
    AlphaVantageClient,
    get_stock_price,
    get_stock_change,
    get_forex_rate,
    get_crypto_rate,
    safe_get_quote
)

def example_basic_functions():
    """基础函数示例"""
    print("=" * 50)
    print("Alpha Vantage 基础函数示例")
    print("=" * 50)
    
    # 1. 获取实时报价
    print("\n1. 获取实时报价 (get_stock_quote):")
    quote = get_stock_quote('AAPL')
    if quote:
        print(f"   AAPL 报价: {quote}")
    else:
        print("   无数据")
    
    # 2. 获取日线数据
    print("\n2. 获取日线数据 (get_daily):")
    daily = get_daily('MSFT')
    if 'Time Series (Daily)' in daily:
        dates = list(daily['Time Series (Daily)'].keys())[:3]
        print(f"   MSFT 最近3天数据日期: {dates}")
    else:
        print(f"   无数据，信息: {daily.get('Information', '未知')}")
    
    # 3. 使用便捷函数获取价格
    print("\n3. 使用便捷函数获取价格 (get_stock_price):")
    price = get_stock_price('GOOGL')
    print(f"   GOOGL 当前价格: ${price if price else '无数据'}")
    
    # 4. 获取涨跌信息
    print("\n4. 获取涨跌信息 (get_stock_change):")
    change = get_stock_change('TSLA')
    print(f"   TSLA 价格: ${change['price']}, 涨跌: {change['change']}, 涨跌幅: {change['change_percent']}%")
    
    # 5. 获取外汇汇率
    print("\n5. 获取外汇汇率 (get_forex_rate):")
    usd_cny = get_forex_rate('USD', 'CNY')
    print(f"   USD/CNY 汇率: {usd_cny if usd_cny else '无数据'}")
    
    # 6. 获取加密货币价格
    print("\n6. 获取加密货币价格 (get_crypto_rate):")
    btc_price = get_crypto_rate('BTC')
    print(f"   BTC/USD 价格: ${btc_price if btc_price else '无数据'}")

def example_client_class():
    """客户端类示例"""
    print("\n" + "=" * 50)
    print("Alpha Vantage 客户端类示例")
    print("=" * 50)
    
    # 创建客户端
    client = AlphaVantageClient()
    
    # 1. 获取实时报价
    print("\n1. 使用客户端获取实时报价:")
    quote_data = client.get_global_quote('NVDA')
    if 'Global Quote' in quote_data:
        quote = quote_data['Global Quote']
        print(f"   NVDA 实时报价:")
        print(f"     价格: ${quote.get('05. price')}")
        print(f"     涨跌: {quote.get('09. change')}")
        print(f"     涨跌幅: {quote.get('10. change percent')}")
    else:
        print(f"   无数据: {quote_data.get('Information', '未知错误')}")
    
    # 2. 搜索符号
    print("\n2. 搜索符号:")
    search_result = client.search_symbols('apple')
    if 'bestMatches' in search_result:
        matches = search_result['bestMatches'][:3]
        print(f"   'apple' 搜索结果 (前3个):")
        for match in matches:
            print(f"     {match['1. symbol']} - {match['2. name']}")
    else:
        print("   无搜索结果")
    
    # 3. 获取市场状态
    print("\n3. 获取市场状态:")
    market_status = client.get_market_status()
    if 'markets' in market_status:
        us_markets = [m for m in market_status['markets'] if m['region'] == 'United States']
        print(f"   美国市场状态 (前3个):")
        for market in us_markets[:3]:
            print(f"     {market['market_type']}: {market['current_status']}")
    else:
        print("   无法获取市场状态")

def example_safe_functions():
    """安全函数示例"""
    print("\n" + "=" * 50)
    print("安全函数示例")
    print("=" * 50)
    
    # 使用安全函数获取报价
    symbols = ['AAPL', 'INVALID', 'MSFT', 'UNKNOWN']
    
    for symbol in symbols:
        print(f"\n获取 {symbol} 报价:")
        result = safe_get_quote(symbol)
        
        if result['success']:
            data = result['data']
            print(f"   成功!")
            print(f"     价格: ${data.get('05. price')}")
            print(f"     涨跌: {data.get('09. change')}")
            print(f"     涨跌幅: {data.get('10. change percent')}")
        else:
            print(f"   失败: {result['error']}")

def example_batch_requests():
    """批量请求示例"""
    print("\n" + "=" * 50)
    print("批量请求示例 (注意速率限制)")
    print("=" * 50)
    
    # 重要符号列表
    important_symbols = ['SPY', 'QQQ', 'AAPL', 'MSFT']
    
    print(f"\n批量获取 {len(important_symbols)} 个重要符号:")
    
    client = AlphaVantageClient()
    
    for symbol in important_symbols:
        print(f"\n  获取 {symbol}:")
        result = safe_get_quote(symbol)
        
        if result['success']:
            data = result['data']
            price = data.get('05. price', 'N/A')
            change = data.get('09. change', 'N/A')
            change_percent = data.get('10. change percent', 'N/A')
            print(f"     价格: ${price}")
            print(f"     涨跌: {change}")
            print(f"     涨跌幅: {change_percent}")
        else:
            print(f"     失败: {result['error']}")
        
        # 模拟延迟（实际使用时需要）
        # time.sleep(client.rate_limit_delay)

def main():
    """主函数"""
    print("Alpha Vantage 技能演示")
    print("API 密钥:", os.environ.get("ALPHA_VANTAGE_API_KEY", "使用默认密钥"))
    print()
    
    try:
        # 运行各个示例
        example_basic_functions()
        example_client_class()
        example_safe_functions()
        example_batch_requests()
        
        print("\n" + "=" * 50)
        print("演示完成!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\n错误: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()