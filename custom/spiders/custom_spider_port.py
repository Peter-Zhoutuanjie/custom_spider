import scrapy
from ..items import TradeGoodsPortItem
import threading
from datasource import DataSource
import distribute_setting as distribute_setting


class CustomSpider(scrapy.Spider):
    name = "custom_spider_port"

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
        for i in range(distribute_setting.START_URL_NUM):
            url = self.get_url()
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)

    def parse(self, response):
        for i in range(distribute_setting.SUR_URL_NUM):
            url = self.get_url()
            yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)
        data_num = len(response.xpath('//div/tr'))
        url_obj = self.find_url_obj(response.url)
        if data_num > 0:
            for i in range(data_num):
                try:
                    i = i + 1
                    item = TradeGoodsPortItem()
                    item['month'] = response.xpath("//div/tr[%d]/td[1]/div/text()" % i).extract()[0]
                    item['goods_code'] = response.xpath("//div/tr[%d]/div[1]/td[1]/div/text()" % i).extract()[0]
                    item['goods'] = response.xpath("//div/tr[%d]/div[1]/td[2]/div/@title" % i).extract()[0]
                    item['port_code'] = response.xpath("//div/tr[%d]/div[2]/td[1]/div/text()" % i).extract()[0]
                    item['port_name'] = response.xpath("//div/tr[%d]/div[2]/td[2]/div/text()" % i).extract()[0]
                    first_num_lst = response.xpath("//div/tr[%d]/td[2]/div/text()" % i).extract()
                    if len(first_num_lst) > 0:
                        first_num = str(first_num_lst[0])
                        if first_num.find('—') > -1:
                            item['first_num'] = 0
                        else:
                            item['first_num'] = first_num
                    else:
                        item['first_num'] = 0
                    first_unit = response.xpath("//div/tr[%d]/td[3]/div/text()" % i).extract()
                    if len(first_unit) > 0:
                        item['first_unit'] = first_unit[0]
                    else:
                        item['first_unit'] = ''
                    second_num_lst = response.xpath("//div/tr[%d]/td[4]/div/text()" % i).extract()
                    if len(second_num_lst) > 0:
                        second_num = str(second_num_lst[0])
                        if second_num.find('—') > -1:
                            item['second_num'] = 0
                        else:
                            item['second_num'] = second_num
                    else:
                        item['second_num'] = 0
                    second_unit = response.xpath("//div/tr[%d]/td[5]/div/text()" % i).extract()
                    if len(second_unit) > 0:
                        item['second_unit'] = second_unit[0]
                    else:
                        item['second_unit'] = ''
                    item['price'] = str(response.xpath("//div/tr[%d]/td[6]/div/text()" % i).extract()[0]).replace(',', '')
                    item['ie_type'] = url_obj[2]
                    yield item
                except Exception as e:
                    print(e)
        print('删除:%s' % url_obj[0])
        CustomSpider.datasource.del_url_port(url_obj[0])

    @staticmethod
    def get_url():
        CustomSpider.lock.acquire()
        try:
            if len(CustomSpider.url_lst) == 0:
                temp = CustomSpider.datasource.get_urls_port()
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
