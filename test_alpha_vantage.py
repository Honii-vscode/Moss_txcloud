#!/usr/bin/env python3
"""
测试 Alpha Vantage 技能
"""

import sys
import os

# 添加技能目录到路径
skill_dir = "/root/.openclaw/workspace/skills/alpha_vantage"
sys.path.insert(0, skill_dir)

try:
    from alpha_vantage import AlphaVantageClient, safe_get_quote
    
    print("✅ Alpha Vantage 技能测试")
    print("=" * 50)
    
    # 测试1: 创建客户端
    client = AlphaVantageClient()
    print(f"1. 客户端创建成功")
    print(f"   API 密钥: {client.api_key[:8]}...")
    
    # 测试2: 获取报价
    print(f"\n2. 测试获取报价:")
    symbols = ['IBM', 'AAPL', 'MSFT']
    
    for symbol in symbols:
        print(f"\n   获取 {symbol}:")
        result = safe_get_quote(symbol)
        
        if result['success']:
            data = result['data']
            print(f"     ✅ 成功")
            print(f"       价格: ${data.get('05. price', 'N/A')}")
            print(f"       涨跌: {data.get('09. change', 'N/A')}")
            print(f"       涨跌幅: {data.get('10. change percent', 'N/A')}")
            print(f"       最新交易日: {data.get('07. latest trading day', 'N/A')}")
        else:
            print(f"     ❌ 失败: {result['error'][:100]}...")
    
    # 测试3: 测试其他功能
    print(f"\n3. 测试其他功能:")
    
    # 搜索功能
    print(f"\n   搜索 'apple':")
    search_result = client.search_symbols('apple')
    if 'bestMatches' in search_result:
        matches = search_result['bestMatches'][:2]
        for match in matches:
            print(f"     {match['1. symbol']}: {match['2. name']}")
    else:
        print(f"     搜索失败: {search_result.get('Information', '未知错误')}")
    
    print(f"\n✅ 测试完成!")
    
except Exception as e:
    print(f"❌ 测试失败: {e}")
    import traceback
    traceback.print_exc()