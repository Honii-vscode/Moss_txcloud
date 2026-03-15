---
name: alpha_vantage
description: Alpha Vantage 金融数据API集成。提供实时股价、历史数据、外汇、加密货币等金融数据。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python3"] },
        "install":
          [
            {
              "id": "pip",
              "kind": "pip",
              "package": "requests",
              "label": "安装 requests 库",
            },
          ],
      },
  }
---

# Alpha Vantage 技能

## 概述

Alpha Vantage 提供免费的金融数据API，包括：
- 实时股价和报价
- 历史日线/周线/月线数据
- 外汇汇率
- 加密货币价格
- 技术指标
- 基本面数据

## 安装

```bash
pip install requests
```

## 配置

### 环境变量（推荐）
```bash
export ALPHA_VANTAGE_API_KEY="8D0W8IKUZ37ISN29"
```

### 或在代码中直接设置
```python
API_KEY = "8D0W8IKUZ37ISN29"
```

## 核心功能

### 1. 获取实时股价

```python
import requests
import os

# 从环境变量读取密钥（更安全），或直接填字符串
API_KEY = os.environ.get("ALPHA_VANTAGE_API_KEY", "8D0W8IKUZ37ISN29")

def get_stock_quote(symbol: str):
    """获取实时股价"""
    url = f"https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={symbol}&apikey={API_KEY}"
    data = requests.get(url).json()
    return data.get("Global Quote", {})

def get_daily(symbol: str):
    """获取日线数据"""
    url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={API_KEY}"
    return requests.get(url).json()
```

### 2. 完整功能模块

```python
import requests
import os
from typing import Dict, List, Optional
import time

class AlphaVantageClient:
    """Alpha Vantage API 客户端"""
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key or os.environ.get("ALPHA_VANTAGE_API_KEY", "8D0W8IKUZ37ISN29")
        self.base_url = "https://www.alphavantage.co/query"
        self.rate_limit_delay = 12  # 免费版限制：5次/分钟，建议12秒间隔
        
    def _make_request(self, params: Dict) -> Dict:
        """发送API请求"""
        params['apikey'] = self.api_key
        response = requests.get(self.base_url, params=params, timeout=10)
        return response.json()
    
    def get_global_quote(self, symbol: str) -> Dict:
        """获取实时报价"""
        params = {
            'function': 'GLOBAL_QUOTE',
            'symbol': symbol
        }
        return self._make_request(params)
    
    def get_time_series_daily(self, symbol: str, outputsize: str = 'compact') -> Dict:
        """获取日线数据"""
        params = {
            'function': 'TIME_SERIES_DAILY',
            'symbol': symbol,
            'outputsize': outputsize  # 'compact' (100点) 或 'full' (20+年)
        }
        return self._make_request(params)
    
    def get_time_series_intraday(self, symbol: str, interval: str = '5min') -> Dict:
        """获取日内数据（需要高级订阅）"""
        params = {
            'function': 'TIME_SERIES_INTRADAY',
            'symbol': symbol,
            'interval': interval,
            'outputsize': 'compact'
        }
        return self._make_request(params)
    
    def get_currency_exchange_rate(self, from_currency: str, to_currency: str) -> Dict:
        """获取外汇汇率"""
        params = {
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': from_currency,
            'to_currency': to_currency
        }
        return self._make_request(params)
    
    def get_crypto_price(self, symbol: str, market: str = 'USD') -> Dict:
        """获取加密货币价格"""
        params = {
            'function': 'CURRENCY_EXCHANGE_RATE',
            'from_currency': symbol,  # 如 'BTC'
            'to_currency': market
        }
        return self._make_request(params)
    
    def search_symbols(self, keywords: str) -> Dict:
        """搜索符号"""
        params = {
            'function': 'SYMBOL_SEARCH',
            'keywords': keywords
        }
        return self._make_request(params)
    
    def get_market_status(self) -> Dict:
        """获取市场状态"""
        params = {
            'function': 'MARKET_STATUS'
        }
        return self._make_request(params)
    
    def get_company_overview(self, symbol: str) -> Dict:
        """获取公司概况"""
        params = {
            'function': 'OVERVIEW',
            'symbol': symbol
        }
        return self._make_request(params)
    
    def batch_quotes(self, symbols: List[str]) -> List[Dict]:
        """批量获取报价（注意速率限制）"""
        results = []
        for symbol in symbols:
            quote = self.get_global_quote(symbol)
            results.append({
                'symbol': symbol,
                'data': quote
            })
            # 避免速率限制
            time.sleep(self.rate_limit_delay)
        return results

# 便捷函数
def get_stock_price(symbol: str) -> Optional[float]:
    """获取股票当前价格"""
    client = AlphaVantageClient()
    data = client.get_global_quote(symbol)
    quote = data.get('Global Quote', {})
    if quote:
        return float(quote.get('05. price', 0))
    return None

def get_stock_change(symbol: str) -> Dict[str, float]:
    """获取股票涨跌信息"""
    client = AlphaVantageClient()
    data = client.get_global_quote(symbol)
    quote = data.get('Global Quote', {})
    if quote:
        return {
            'price': float(quote.get('05. price', 0)),
            'change': float(quote.get('09. change', 0)),
            'change_percent': float(quote.get('10. change percent', '0%').replace('%', ''))
        }
    return {'price': 0, 'change': 0, 'change_percent': 0}

def get_forex_rate(from_currency: str, to_currency: str) -> Optional[float]:
    """获取外汇汇率"""
    client = AlphaVantageClient()
    data = client.get_currency_exchange_rate(from_currency, to_currency)
    rate = data.get('Realtime Currency Exchange Rate', {})
    if rate:
        return float(rate.get('5. Exchange Rate', 0))
    return None

def get_crypto_rate(crypto: str, fiat: str = 'USD') -> Optional[float]:
    """获取加密货币汇率"""
    client = AlphaVantageClient()
    data = client.get_crypto_price(crypto, fiat)
    rate = data.get('Realtime Currency Exchange Rate', {})
    if rate:
        return float(rate.get('5. Exchange Rate', 0))
    return None
```

### 3. 使用示例

```python
# 初始化客户端
client = AlphaVantageClient()

# 获取实时报价
quote = client.get_global_quote('AAPL')
print(f"AAPL 实时报价: {quote}")

# 获取日线数据
daily_data = client.get_time_series_daily('MSFT', outputsize='compact')
print(f"MSFT 日线数据: {len(daily_data.get('Time Series (Daily)', {}))} 天")

# 获取外汇汇率
forex = client.get_currency_exchange_rate('USD', 'CNY')
print(f"USD/CNY 汇率: {forex.get('Realtime Currency Exchange Rate', {}).get('5. Exchange Rate')}")

# 获取加密货币价格
crypto = client.get_crypto_price('BTC', 'USD')
print(f"BTC/USD 价格: {crypto.get('Realtime Currency Exchange Rate', {}).get('5. Exchange Rate')}")

# 使用便捷函数
price = get_stock_price('GOOGL')
print(f"GOOGL 当前价格: ${price}")

change_info = get_stock_change('TSLA')
print(f"TSLA 涨跌: {change_info['change_percent']}%")

usd_cny = get_forex_rate('USD', 'CNY')
print(f"美元兑人民币: {usd_cny}")

btc_price = get_crypto_rate('BTC')
print(f"比特币价格: ${btc_price}")
```

## 速率限制

### 免费版限制
- **每日请求**：25次/天
- **建议间隔**：12秒/请求（避免429错误）
- **批量处理**：使用延迟避免超限

### 处理速率限制
```python
import time

def safe_batch_request(symbols, delay=12):
    """安全的批量请求"""
    results = []
    for symbol in symbols:
        try:
            data = get_stock_price(symbol)
            results.append({'symbol': symbol, 'price': data})
            time.sleep(delay)  # 避免速率限制
        except Exception as e:
            print(f"获取 {symbol} 失败: {e}")
    return results
```

## 错误处理

```python
def safe_get_quote(symbol: str):
    """安全的获取报价，包含错误处理"""
    try:
        client = AlphaVantageClient()
        data = client.get_global_quote(symbol)
        
        if 'Global Quote' in data:
            return {
                'success': True,
                'data': data['Global Quote']
            }
        elif 'Error Message' in data:
            return {
                'success': False,
                'error': data['Error Message']
            }
        elif 'Information' in data:
            return {
                'success': False,
                'error': 'API限制: ' + data['Information']
            }
        else:
            return {
                'success': False,
                'error': '未知错误'
            }
            
    except requests.exceptions.RequestException as e:
        return {
            'success': False,
            'error': f'网络错误: {str(e)}'
        }
    except Exception as e:
        return {
            'success': False,
            'error': f'系统错误: {str(e)}'
        }
```

## 常用符号参考

### 美国股票
- `AAPL` - 苹果
- `MSFT` - 微软
- `GOOGL` - 谷歌
- `AMZN` - 亚马逊
- `TSLA` - 特斯拉
- `NVDA` - 英伟达
- `META` - Meta
- `JPM` - 摩根大通

### ETF（指数替代）
- `SPY` - 标普500 ETF
- `QQQ` - 纳斯达克100 ETF
- `IVV` - iShares标普500
- `VTI` - 全股市ETF

### 中国概念股
- `BABA` - 阿里巴巴
- `PDD` - 拼多多
- `JD` - 京东
- `BIDU` - 百度
- `NIO` - 蔚来

### 外汇
- `USD/CNY` - 美元/人民币
- `EUR/USD` - 欧元/美元
- `GBP/USD` - 英镑/美元
- `USD/JPY` - 美元/日元

### 加密货币
- `BTC` - 比特币
- `ETH` - 以太坊
- `SOL` - Solana

## 集成到OpenClaw

### 作为工具使用
```python
# 在OpenClaw技能中调用
from alpha_vantage import get_stock_price, get_stock_change

def handle_stock_query(symbol: str):
    price = get_stock_price(symbol)
    change = get_stock_change(symbol)
    return f"{symbol} 当前价格: ${price}, 涨跌: {change['change_percent']}%"
```

### 环境配置
在OpenClaw配置中添加环境变量：
```bash
# 在启动脚本或配置文件中
export ALPHA_VANTAGE_API_KEY="8D0W8IKUZ37ISN29"
```

## 注意事项

1. **API密钥安全**：不要将API密钥提交到版本控制系统
2. **速率限制**：严格遵守API调用频率限制
3. **数据延迟**：免费版数据可能有15分钟延迟
4. **错误处理**：始终包含适当的错误处理逻辑
5. **缓存策略**：对频繁查询的数据实施缓存

## 故障排除

### 常见问题
1. **429错误**：请求过于频繁，增加请求间隔
2. **无效符号**：确认符号格式正确（如`.HK`、`.SS`后缀）
3. **无数据返回**：检查API密钥是否有效，符号是否支持
4. **网络超时**：增加请求超时时间或重试机制

### 调试建议
```python
# 启用调试模式
import logging
logging.basicConfig(level=logging.DEBUG)

# 检查响应
response = requests.get(url, params=params)
print(f"状态码: {response.status_code}")
print(f"响应头: {response.headers}")
print(f"响应内容: {response.text[:500]}")  # 只打印前500字符
```

## 更新日志

### v1.0.0 (2026-03-05)
- 初始版本发布
- 支持实时报价、历史数据、外汇、加密货币
- 包含完整的错误处理和速率限制管理
- 提供便捷函数和完整客户端类

## 许可证

本技能基于Alpha Vantage API，使用时请遵守其[服务条款](https://www.alphavantage.co/terms/)。

## 支持

- Alpha Vantage文档：https://www.alphavantage.co/documentation/
- 问题反馈：通过OpenClaw社区或GitHub Issues
- API密钥申请：https://www.alphavantage.co/support/#api-key

---

**提示**：此技能已预配置你的API密钥 `8D0W8IKUZ37ISN29`，可以直接使用。