import sqlite3

def view_all_sqlite_data(db_path):
    # 1. 连接数据库
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # 2. 查询数据库中所有表名
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()  # 格式：[(表1名,), (表2名,), ...]
        print(f"数据库中共有 {len(tables)} 张表：{[table[0] for table in tables]}\n")
        
        # 3. 遍历每张表，查看所有数据
        for table in tables:
            table_name = table[0]
            print(f"=== 表：{table_name} 的所有数据 ===")
            
            # 3.1 查询表的列名（字段名）
            cursor.execute(f"PRAGMA table_info({table_name});")
            columns = [col[1] for col in cursor.fetchall()]  # 提取列名列表
            print(f"字段名：{columns}")
            
            # 3.2 查询表中所有数据
            cursor.execute(f"SELECT * FROM {table_name};")
            all_data = cursor.fetchall()  # 所有行数据，每行是一个元组
            
            # 3.3 打印数据（若数据量大，可限制打印行数，避免刷屏）
            if len(all_data) == 0:
                print("该表无数据\n")
                continue
            
            # 打印前10行（可修改数字调整，或直接打印全部：for row in all_data）
            for i, row in enumerate(all_data):
                print(f"第{i+1}行：{dict(zip(columns, row))}")  # 转为字典，更易读
            
            if len(all_data) > 10:
                print(f"... 共 {len(all_data)} 行数据，已显示前10行\n")
            else:
                print(f"共 {len(all_data)} 行数据\n")
    
    except Exception as e:
        print(f"读取数据库出错：{e}")
    
    finally:
        # 关闭连接
        cursor.close()
        conn.close()

# ------------------------------
# 调用函数：替换为你的 .db 文件路径（若误写为 .bd，直接填 .bd 路径即可）
# ------------------------------
view_all_sqlite_data(db_path="e:/pythonProject/供应链/database/weather_data.db")