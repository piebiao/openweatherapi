import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from config import DATABASE_URL
from models import Base

# ------------------------------
# 原生 SQLite 操作（对应文档 Part 2）
# ------------------------------
def connect_sqlite_db(db_name="weather_data.db"):
    """连接 SQLite 数据库并返回连接和游标"""
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    return conn, cursor

def create_weather_table(cursor):
    """创建 WeatherRecords 表（原生 SQL，文档 Exercise 5）"""
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS WeatherRecords (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            city_id INTEGER,
            date TEXT NOT NULL,
            temperature REAL NOT NULL,
            humidity INTEGER NOT NULL
        )
    ''')

def insert_weather_record(cursor, city_id, date, temperature, humidity):
    """插入天气记录（原生 SQL，文档 Exercise 6）"""
    cursor.execute('''
        INSERT INTO WeatherRecords (city_id, date, temperature, humidity)
        VALUES (?, ?, ?, ?)
    ''', (city_id, date, temperature, humidity))

# ------------------------------
# SQLAlchemy ORM 操作（对应文档 Part 4）
# ------------------------------
# 创建数据库引擎
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def create_tables():
    """创建所有 ORM 模型对应的数据库表"""
    Base.metadata.create_all(bind=engine)

def get_db_session():
    """获取数据库会话（依赖注入）"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()