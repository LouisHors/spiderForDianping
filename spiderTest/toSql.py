# -*- coding: utf-8 -*-

import pymysql

serverIp = "localhost"
userName = "root"
password = "Lh.697148"
databaseName = "spider_dianping"

# 打开数据库连接
db = pymysql.connect(serverIp, userName, password, databaseName)

# 使用cursor()方法创建一个游标对象cursor
cursor = db.cursor()

# 创建表语句 注意长度限制
sql = """CREATE TABLE yuecaiguan (
         shop_id  INT PRIMARY KEY auto_increment,
         shop_name  VARCHAR(50),
         shop_img VARCHAR(150),  
         shop_star VARCHAR(10),
         shop_evaluation INT,
        shop_price INT,
       shop_type VARCHAR(10),
       shop_address1 VARCHAR(15),
       shop_address2 VARCHAR(100),
       shop_food1 VARCHAR(20), 
       shop_food2 VARCHAR(20), 
       shop_food3 VARCHAR(20), 
       shop_sweet FLOAT, 
       shop_environment FLOAT, 
       shop_server FLOAT)"""

# 使用execute()方法执行SQL查询
cursor.execute(sql)

# 使用 fetchone() 方法获取单条数据.
# data = cursor.fetchone()

# print("Database version : %s " % data)
cursor.close()

# 关闭数据库连接
db.close()