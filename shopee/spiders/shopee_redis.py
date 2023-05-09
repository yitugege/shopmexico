from requests import delete
from scrapy.spiders import Rule
from scrapy import Request
from scrapy.linkextractors import LinkExtractor
import re
from datetime import date
from ..items import ParentItem
from ..items import ChildItem
from scrapy_redis.spiders import RedisSpider



class  ShopeeRedisSpider(RedisSpider):
    name = 'shopemexico'
    redis_key = name + ':start_urls'

    def parse(self, response):
        main_detail_response = response.json()['data']['category_list']
        for category_list in main_detail_response:
            #child_cat_list = []
            # 分类信息
            item = ParentItem()
            item['catid'] = category_list['catid']
            item['display_name'] = category_list['display_name']
            for child_catid in category_list['children']:
                item['second_cage_catid'] = child_catid['catid']
                item['second_cage_display_name'] = child_catid['display_name']
                #item['second_url'] = f"https://www.shopee.com.mx/{item['second_cage_display_name'].replace(' ', '-')}-cat.{child_catid['catid']}?page="
                #https://shopee.com.mx/api/v4/recommend/recommend?bundle=category_landing_page&cat_level=1&catid=11057097&limit=60&offset=60
                #https://shopee.com.mx/api/v4/recommend/recommend?bundle=category_landing_page&cat_level=1&catid=11057097&limit=60&offset=120
                item['second_url'] = f"https://shopee.com.mx/api/v4/recommend/recommend?bundle=category_landing_page&catid={child_catid['catid']}&limit=60&offset="
                # item['child_cat_list'] = child_cat_list
                # 获取下一页URL，并生成Request请求，提交给引擎
                # 1.获取下一页URL
                current_page = 0  # 设置当前页，起始为0
                total_page=category_list
                while current_page <= 10:
                    current_page += 1
                    next_url = f"{item['second_url']}{current_page}"
                    print(f"正在爬取类别{next_url}")
                    # 2.根据URL生成Request，使用yield返回给引擎
                    yield Request(url=next_url, callback=self.parse_product, meta={'item': item})
                    
    # 解析product的数据
    def parse_product(self, response):
        parent_item = response.meta['item']
        product_list = response.json()['data']['sections'][0]['data']['item']
        #https://shopee.com.mx/Mochila-Escolar-Impermeable-Antirrobo-Portátil-15.6-Carga-USB-i.653878025.21866321753
        for product in product_list:
            item = ChildItem()
            item['id'] = product['itemid']
            item['title'] = parent_item['display_name']
            item['category'] = product['catid']
            item['title'] = product['name']
            item[
                'url'] = f"https://www.shopee.com.mx/{product['name'].replace(' ', '-')}s-i.{product['shopid']}.{product['itemid']}"
            item['image'] = ','.join(
                ['https://own-mx.img.susercontent.com/file/' + images_url for images_url in product['images']])
            item['price'] = int(product['price'] / 100000)
            item['Num_sell'] = product['historical_sold']
            item['like_count'] = product['liked_count']
            item['tablename'] = self.name
            yield item
    
            

      

        