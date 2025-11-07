import requests
from datetime import datetime
from config import API_KEY, API_BASE_URL

def get_weather(city_name, country_code=""):
    """获取城市天气数据（文档 Exercise 7）"""
    # 拼接城市名（支持国家代码过滤，如 "New York,US"）
    query_city = f"{city_name},{country_code}" if country_code else city_name
    
    params = {
        "q": query_city,
        "appid": API_KEY,
        "units": "metric"  # 温度单位：摄氏度
    }
    
    try:
        response = requests.get(API_BASE_URL, params=params)
        response.raise_for_status()  # 抛出 HTTP 错误
        data = response.json()
        
        # 格式化返回数据（提取核心字段）
        return {
            "city_name": data["name"],
            "country": data["sys"]["country"],
            "date": datetime.fromtimestamp(data["dt"]),  # 转换为 datetime 对象
            "temperature": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"]
        }
    except requests.exceptions.RequestException as e:
        print(f"API 请求失败：{e}")
        return None