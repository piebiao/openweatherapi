from datetime import datetime, timedelta
from sqlalchemy import func
from models import City, WeatherRecord

def store_weather_data(db, weather_data):
    """存储天气数据到数据库（ORM 版本，文档 Exercise 7）"""
    # 1. 查找或创建城市
    city = db.query(City).filter_by(
        name=weather_data["city_name"],
        country=weather_data["country"]
    ).first()
    
    if not city:
        city = City(
            name=weather_data["city_name"],
            country=weather_data["country"]
        )
        db.add(city)
        db.commit()
        db.refresh(city)
    
    # 2. 创建天气记录
    weather_record = WeatherRecord(
        city_id=city.id,
        date=weather_data["date"],
        temperature=weather_data["temperature"],
        humidity=weather_data["humidity"],
        wind_speed=weather_data["wind_speed"]
    )
    
    db.add(weather_record)
    db.commit()
    print(f"成功存储 {city.name} 的天气数据（{weather_data['date'].strftime('%Y-%m-%d')}）")

def monthly_avg_temperatures(db, city_name):
    """计算城市一年中每月平均气温（文档 Exercise 13）"""
    # 获取当前年份
    current_year = datetime.now().year
    
    # 提取月份并分组计算平均温度
    results = db.query(
        func.strftime("%m", WeatherRecord.date).label("month"),
        func.avg(WeatherRecord.temperature).label("avg_temp")
    ).join(City).filter(
        City.name == city_name,
        func.strftime("%Y", WeatherRecord.date) == str(current_year)
    ).group_by("month").all()
    
    # 转换为 {月份: 平均温度} 字典（月份补前导零）
    return {
        f"{int(month):02d}": round(avg_temp, 2)
        for month, avg_temp in results
    }

def get_cities_above_35_last_week(db):
    """查询上周气温超过 35°C 的城市（文档 Exercise 11）"""
    last_week = datetime.now() - timedelta(days=7)
    
    cities = db.query(City).join(WeatherRecord).filter(
        WeatherRecord.date >= last_week,
        WeatherRecord.temperature > 25.0
    ).distinct().all()
    
    return [{"id": city.id, "name": city.name, "country": city.country} for city in cities]

def get_hottest_city_in_date_range(db, start_date, end_date):
    """查找日期范围内平均气温最高的城市（文档奖金挑战）"""
    hottest_city = db.query(
        City,
        func.avg(WeatherRecord.temperature).label("avg_temp")
    ).join(WeatherRecord).filter(
        WeatherRecord.date >= start_date,
        WeatherRecord.date <= end_date
    ).group_by(City.id).order_by(func.avg(WeatherRecord.temperature).desc()).first()
    
    if hottest_city:
        return {
            "city_name": hottest_city.City.name,
            "country": hottest_city.City.country,
            "avg_temperature": round(hottest_city.avg_temp, 2)
        }
    return None