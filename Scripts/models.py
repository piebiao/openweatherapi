from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy.orm import validates
from config import MIN_TEMPERATURE, MAX_TEMPERATURE

Base = declarative_base()

class City(Base):
    """城市模型"""
    __tablename__ = "cities"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False, unique=True)
    country = Column(String(50), nullable=False)
    
    # 关联天气记录（一对多）
    weather_records = relationship("WeatherRecord", back_populates="city", cascade="all, delete-orphan")
    # 关联气象站（多对一）
    weather_station_id = Column(Integer, ForeignKey("weather_stations.id"))
    weather_station = relationship("WeatherStation", back_populates="cities")

class WeatherStation(Base):
    """气象站模型"""
    __tablename__ = "weather_stations"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    location = Column(String(100), nullable=False)
    
    # 关联城市（一对多）
    cities = relationship("City", back_populates="weather_station")

class WeatherRecord(Base):
    """天气记录模型（含文档要求的 wind_speed 字段）"""
    __tablename__ = "weather_records"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    city_id = Column(Integer, ForeignKey("cities.id"), nullable=False)
    date = Column(DateTime, nullable=False)
    temperature = Column(Float, nullable=False)  # 单位：°C
    humidity = Column(Integer, nullable=False)    # 单位：%
    wind_speed = Column(Float, nullable=False)   # 单位：m/s（文档要求新增字段）
    
    # 关联城市
    city = relationship("City", back_populates="weather_records")
    
    # 温度验证（文档奖金挑战要求）
    @validates("temperature")
    def validate_temperature(self, key, temperature):
        if not (MIN_TEMPERATURE <= temperature <= MAX_TEMPERATURE):
            raise ValueError(f"温度必须在 {MIN_TEMPERATURE}°C 至 {MAX_TEMPERATURE}°C 之间")
        return temperature