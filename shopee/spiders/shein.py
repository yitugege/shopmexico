import scrapy
import json
from scrapy_splash import SplashRequest
#from ..items import ShopeeItem

class SheinSpider(scrapy.Spider):
    name = 'shein'
    allowed_domains = ['shein.com.mx']
    
    script = """
    function main(splash, args)
        assert(splash:go(args.url))
        assert(splash:wait(1))
        return {html=splash:html(), 
                goods_data=splash:evaljs("window.goodsDetailV3SsrData")}
    end
    """

    def start_requests(self):
        url = "https://www.shein.com.mx/Snowflake-Print-Cushion-Cover-Without-Filler-p-11248006-cat-1947.html?mallCode=1"
        yield SplashRequest(url, self.parse, endpoint='execute', args={'lua_source': self.script})

    def parse(self, response):
        goods_data = response.data['goods_data']
        goods_data_json = json.dumps(goods_data, indent=2)  # 将 goods_data 转换为格式化的 JSON 字符串
        print(goods_data_json)


