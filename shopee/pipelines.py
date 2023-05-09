# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter


from scrapy.exceptions import DropItem
import pymysql
from datetime import datetime


class QidianHotPipeline(object):
    def process_item(self, item, spider):
        if item["child_detail_url"] == "":
            return f"商品{item['child_detail_url']}无需爬取"
        else:
            print(f"正在爬取商品{item['child_detail_url']}")
        return item


# 去除重复作者的Item Pipeline
class DuplicatesPipeline(object):
    def __init__(self):
        # 定义一个保存商品信息的集合，
        self.author_set = set()

    def process_item(self, item, spider):
        if item['child_detail_url'] in self.author_set:
            # 抛弃重复的Item项
            raise DropItem("查找到重复的商品链接: %s" % item)
        else:
            self.author_set.add(item['child_detail_url'])
        return item
    

def dbHandle():
    conn = pymysql.connect(
        host = "192.168.3.200",
        user = "root1",
        password = "123456",
        charset = "utf8",
        port = 3306
    )
    return conn

class ShopeeRedisPipeline:
    def process_item(self, item, spider):
        dbObject = dbHandle()
        cursor = dbObject.cursor()
        cursor.execute("USE shopee")
        tablename= item['tablename']
        #如果没有抓到标题那么说明连接已经死了，那么删除数据库连接
        if (item['title'] == "delete") or (item['price'] == "delete") or (item['Num_sell'] == "delete"):

            # #return print("--无效链接放弃:"+item['url'])

            # if "delete" in item['title']:
            #     sql = "delete from scrapy.%s" %tablename + " where id = %s" %item['id']
            #     print(sql)
            #     try:
            #         cursor.execute(sql)
            #         cursor.connection.commit()
            #     except BaseException as e:
            #         print("The error is here>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<<The error is here")
            #         dbObject.close()
                 #return print("--删除成功:"+item['url']) 
            return   
        else:
            #判断如果存在则更新，如果不存在则插入
            sql = "INSERT INTO %s" % tablename + "(Num_sell,title,url,price,id,category,like_count,image) VALUES(%s,%s,%s,%s,%s,%s,%s,%s) ON DUPLICATE KEY UPDATE Num_sell=%s,title=%s,url=%s,price=%s,category=%s,like_count=%s,image=%s"
            #print (sql)
            try:
                    cursor.execute(sql,(item['Num_sell'],item['title'],item['url'],item['price'],item['id'],item['category'],item['like_count'],item['image'],item['Num_sell'],item['title'],item['url'],item['price'],item['category'],item['like_count'],item['image']))
                    cursor.connection.commit()
            except BaseException as e:
                    print("The error is here>>>>>>>>>>>>>", e, "<<<<<<<<<<<<<<The error is here")
                    dbObject.close()
            return item    


