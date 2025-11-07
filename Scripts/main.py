import schedule
import time
from datetime import datetime, timedelta
from database import create_tables, get_db_session
from weather_api import get_weather
from utils import (
    store_weather_data,
    monthly_avg_temperatures,
    get_cities_above_35_last_week,
    get_hottest_city_in_date_range
)
from config import SCHEDULE_TIME

# 初始化数据库（创建所有表）
create_tables()

def daily_weather_task(city_names=["New York", "London", "Tokyo","hubei","foshan","guangzhou","shanghai","beijing"]):
    """每日天气采集任务（文档 Exercise 7）"""
    db = next(get_db_session())
    for city in city_names:
        weather_data = get_weather(city)
        if weather_data:
            store_weather_data(db, weather_data)
    db.close()

def main():
    # 1. 立即执行一次采集任务
    print("开始首次天气数据采集...")
    daily_weather_task()
    
    # 2. 配置定时任务（每天指定时间执行）
    schedule.every().day.at(SCHEDULE_TIME).do(daily_weather_task)
    print(f"定时任务已配置：每天 {SCHEDULE_TIME} 执行")
    
    # 3. 示例：执行文档要求的查询功能
    db = next(get_db_session())
    
    # 示例 1：查询上周气温超 35°C 的城市
    print("\n上周气温超过 35°C 的城市：")
    hot_cities = get_cities_above_35_last_week(db)
    print(hot_cities if hot_cities else "无符合条件的城市")
    
    # 示例 2：查询纽约今年每月平均气温
    print("\n纽约今年每月平均气温：")
    ny_avg = monthly_avg_temperatures(db, "New York")
    print(ny_avg if ny_avg else "暂无数据")
    
    # 示例 3：查询近 7 天平均气温最高的城市
    start_date = datetime.now() - timedelta(days=7)
    end_date = datetime.now()
    print(f"\n{start_date.strftime('%Y-%m-%d')} 至 {end_date.strftime('%Y-%m-%d')} 平均气温最高的城市：")
    hottest_city = get_hottest_city_in_date_range(db, start_date, end_date)
    print(hottest_city if hottest_city else "暂无数据")
    
    db.close()
    
    # 4. 保持程序运行以执行定时任务
    while True:
        schedule.run_pending()
        time.sleep(60)  # 每分钟检查一次

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序已退出")