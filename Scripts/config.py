import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# OpenWeatherMap API 配置
API_KEY = os.getenv("OPEN_WEATHER_API_KEY", "your_default_api_key")
API_BASE_URL = "http://api.openweathermap.org/data/2.5/weather"

# 数据库配置
DATABASE_URL = "sqlite:///weather_data.db"

# 温度验证范围（-50°C 至 50°C）
MIN_TEMPERATURE = -50.0
MAX_TEMPERATURE = 50.0

# 定时任务配置（每天凌晨 2 点执行）
SCHEDULE_TIME = "02:00"