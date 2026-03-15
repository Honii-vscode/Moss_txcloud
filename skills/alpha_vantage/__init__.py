"""
Alpha Vantage 金融数据API集成
提供实时股价、历史数据、外汇、加密货币等金融数据
"""

import requests
import os
from typing import Dict, List, Optional
import time

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

# 导出主要功能
__all__ = [
    'API_KEY',
    'get_stock_quote',
    'get_daily',
    'AlphaVantageClient',
    'get_stock_price',
    'get_stock_change',
    'get_forex_rate',
    'get_crypto_rate',
    'safe_get_quote',
    'safe_batch_request'
]