# -*- coding: utf-8 -*-

import json
import pymysql

serverIp = "localhost"
userName = "root"
password = "Lh.697148"
databaseName = "spider_dianping"

# 打开数据库连接  注意最后一个参数charset='utf8'
db = pymysql.connect(host=serverIp, user=userName, passwd=password, db=databaseName, port=3306, charset="utf8")

# 使用cursor()方法创建一个游标对象cursor
cursor = db.cursor()

data = []
with open('yuecai-yuecaiguan.json') as f:
    for line in f:
        # 需要数据为json格式，所以去掉每行末尾的','
        data.append(json.loads(line[0:-2]))


for item in data:
    # 使用get方法如果对应key没有值，则赋一个默认值

    # 防止字符串中包含单引号
    shop_name_str = item.get('shop_name', "").replace("'", "\\\'")
    shop_img_str = item.get('shop_img', '')
    shop_star_str = item.get('shop_star', '')
    shop_evaluation_str = item.get('shop_evaluation', 0)
    shop_price_stro = item.get('shop_price', '0')

    if shop_price_stro != '0':
        # 将前面的'￥'过滤掉
        shop_price_str = shop_price_stro[1:]
    else:
        shop_price_str = 0
    shop_type_str = item.get('shop_type', '')
    shop_address1_str = item.get('shop_address1', '')
    shop_address2_str = item.get('shop_address2', '')
    shop_food1_str = item.get('shop_food1', '')
    shop_food2_str = item.get('shop_food2', '')
    shop_food3_str = item.get('shop_food3', '')
    shop_sweet_str = item.get('shop_sweet', 0.0)
    shop_environment_str = item.get('shop_environment', 0.0)
    shop_server_str = item.get('shop_server', 0.0)

    str = "INSERT INTO yuecaiguan(shop_name, shop_img, shop_star, shop_evaluation, shop_price, shop_type, shop_address1, shop_address2, shop_food1, shop_food2, shop_food3, shop_sweet, shop_environment, shop_server) VALUES "
    str = str + "('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');\r\n" % (shop_name_str, shop_img_str, shop_star_str, shop_evaluation_str, shop_price_str, shop_type_str, shop_address1_str, shop_address2_str, shop_food1_str, shop_food2_str, shop_food3_str, shop_sweet_str, shop_environment_str, shop_server_str)
    # str = "UPDATE shops SET shop_price = '%s' WHERE shop_name = '%s';" % (shop_price_str, shop_name_str)
    cursor.execute(str)

f.close()
cursor.close()
db.commit()
db.close()

print("success")