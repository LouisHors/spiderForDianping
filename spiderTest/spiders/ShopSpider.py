# -*- coding: utf-8 -*-
import scrapy
from spiderTest.items import SpidertestItem


class ShopspiderSpider(scrapy.Spider):
    name = 'ShopSpider'
    allowed_domains = ['dianping.com']
    url = 'http://www.dianping.com/guangzhou/ch10/g205r22p'
    offset = 2
    start_urls = [url + str(offset)]

    def parse(self, response):
        for each in response.xpath("//div[@class='shop-list J_shop-list shop-all-list']/ul/li"):
            item = SpidertestItem()
            item['shop_name'] = each.xpath(".//img/@title").extract()[0]
            imgurl = each.xpath(".//img/@src").extract()[0]
            img = imgurl.split('%')[0]
            item['shop_img'] = img

            item['shop_star'] = each.xpath(".//div[@class='comment']/span/@title").extract()[0]

            price_tag = 0
            for price in  each.xpath(".//div[@class='comment']"):
                if price_tag == 0:
                    # 当评价人数为空的时候，第一个获得到的数据包含'￥'那么就是价格，否则是评价人数
                    ep = price.xpath(".//a/b/text()").extract()[0]
                    if '￥' in ep:
                        item['shop_price'] = ep
                    else:
                        item['shop_evaluation'] = ep
                    price_tag += 1
                elif price_tag == 1:
                    item['shop_price'] = price.xpath(".//a/b/text()").extract()[1]
                    price_tag += 1

            # 商店类型 和 地址，防止地址1不存在，需要判断
            at_tag = 0
            for at in each.xpath(".//div[@class='tag-addr']"):
                for att in at.xpath(".//a/span[@class='tag']/text()"):
                    if at_tag == 0:
                        item['shop_type'] = at.xpath(".//a/span[@class='tag']/text()").extract()[0]
                        at_tag += 1
                    elif at_tag == 1:
                        item['shop_address1'] = at.xpath(".//a/span[@class='tag']/text()").extract()[1]
                        at_tag += 1
            # 地址2
            item['shop_address2'] = each.xpath(".//div[@class='tag-addr']/span[@class='addr']/text()").extract()[0]

            # 推荐菜 判断个数
            food_tag = 0
            for food in each.xpath(".//div[@class='recommend']"):
                for f in food.xpath(".//a/text()"):
                    if food_tag == 0:
                        item['shop_food1'] = food.xpath(".//a/text()").extract()[0]
                        food_tag += 1
                    elif food_tag == 1:
                        item['shop_food2'] = food.xpath(".//a/text()").extract()[1]
                        food_tag += 1
                    elif food_tag == 2:
                        item['shop_food3'] = food.xpath(".//a/text()").extract()[2]
                        food_tag += 1
            # 其他评分
            score_tag = 0
            for score in each.xpath(".//span[@class='comment-list']"):
                for s in score.xpath(".//span/b/text()"):
                    if score_tag == 0:
                        item['shop_sweet'] = score.xpath(".//span/b/text()").extract()[0]
                        score_tag += 1
                    elif score_tag == 1:
                        item['shop_environment'] = score.xpath(".//span/b/text()").extract()[1]
                        score_tag += 1
                    elif score_tag == 2:
                        item['shop_server'] = score.xpath(".//span/b/text()").extract()[2]
                        score_tag += 1

            yield item

            if self.offset < 51:
                self.offset += 1
            #
            # # 每次处理完一页的数据之后，重新发送下一页页面请求
            # # self.offset自增10，同时拼接为新的url，并调用回调函数self.parse处理Response
            yield scrapy.Request(self.url + str(self.offset), callback=self.parse)

        pass
