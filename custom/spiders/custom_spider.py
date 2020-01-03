import scrapy
from ..items import TradeGoodsItem
import threading
from custom.datasource import DataSource
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
# from scrapy_selenium import SeleniumRequest


class CustomSpider(scrapy.Spider):
    name = "custom_spider"

    url_pre = 'http://43.248.49.97/queryData/getQueryDataListByWhere?'

    url_lst = []

    url_dict = {}

    lock = threading.Lock()

    datasource = DataSource()

    headers = {
        'Accept': ' text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
        'Accept-Encoding': ' gzip, deflate',
        'Accept-Language': ' zh-CN,zh;q=0.9',
        'Content-Type': ' application/x-www-form-urlencoded',
        'Host': ' 43.248.49.97',
        'Origin': ' http://43.248.49.97',
        'Referer': ' http://43.248.49.97/paramManager/selComplexList',
        'User-Agent': ' Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.100 Safari/537.36', }

    def start_requests(self):
        for i in range(100):
            url = self.get_url()
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        for i in range(5):
            url = self.get_url()
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)
        data_num = len(response.xpath('//div/tr'))
        url_obj = self.find_url_obj(response.url)
        if data_num > 0:
            for i in range(data_num):
                i = i + 1
                item = TradeGoodsItem()
                item['month'] = response.xpath("//div/tr[%d]/td[1]/div/text()" % i).extract()[0]
                item['goods_code'] = response.xpath("//div/tr[%d]/div[1]/td[1]/div/text()" % i).extract()[0]
                item['goods'] = response.xpath("//div/tr[%d]/div[1]/td[2]/div/@title" % i).extract()[0]
                item['partner_code'] = response.xpath("//div/tr[%d]/div[2]/td[1]/div/text()" % i).extract()[0]
                item['partner_name'] = response.xpath("//div/tr[%d]/div[2]/td[2]/div/text()" % i).extract()[0]
                item['port_code'] = response.xpath("//div/tr[%d]/div[3]/td[1]/div/text()" % i).extract()[0]
                item['port_name'] = response.xpath("//div/tr[%d]/div[3]/td[2]/div/text()" % i).extract()[0]
                first_num = str(response.xpath("//div/tr[%d]/td[2]/div/text()" % i).extract()[0])
                if first_num.find('—') > -1:
                    item['first_num'] = 0
                else:
                    item['first_num'] = first_num
                item['first_unit'] = response.xpath("//div/tr[%d]/td[3]/div/text()" % i).extract()[0]
                second_num = str(response.xpath("//div/tr[%d]/td[4]/div/text()" % i).extract()[0])
                if second_num.find('—') > -1:
                    item['second_num'] = 0
                else:
                    item['second_num'] = second_num
                item['second_unit'] = response.xpath("//div/tr[%d]/td[5]/div/text()" % i).extract()[0]
                item['price'] = str(response.xpath("//div/tr[%d]/td[6]/div/text()" % i).extract()[0]).replace(',', '')
                item['ie_type'] = url_obj[2]
                yield item
        print('删除')
        CustomSpider.datasource.delUrl(url_obj[0])

    @staticmethod
    def get_url():
        CustomSpider.lock.acquire()
        try:
            if len(CustomSpider.url_lst) == 0:
                temp = CustomSpider.datasource.getUrlLst()
                for obj in temp:
                    url = CustomSpider.url_pre + obj[1]
                    CustomSpider.url_dict[url] = obj
                    CustomSpider.url_lst.append(url)
            url = CustomSpider.url_lst[-1]
            CustomSpider.url_lst.pop()
            return url
        finally:
            # 改完了一定要释放锁:
            CustomSpider.lock.release()

    @staticmethod
    def find_url_obj(url):
        obj = CustomSpider.url_dict[url]
        CustomSpider.url_dict.pop(url)
        return obj
