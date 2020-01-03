import scrapy
# from scrapy_selenium import SeleniumRequest
from ..items import GoodsCodeItem


class CustomCodeSpider(scrapy.Spider):
    name = "custom_code_spider"

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
        year_lst = ['2019', '2018', '2017']
        codeLength_lst = ['2', '4', '6', '8']

        for year in year_lst:
            for codeLength in codeLength_lst:
                url = 'http://43.248.49.97/paramManager/selComplexList?pageNum=1&pageSize=9999&enFlag=CN&searchKey=&codeLength=%s&yearId=%s' % (codeLength, year)
                yield scrapy.Request(url=url, callback=self.parse, headers=self.headers)


    def parse(self, response):
        print("111111")
        data_num = len(response.xpath('//*[@id="table"]/tbody/tr'))
        for i in range(data_num):
            i = i + 1
            item = GoodsCodeItem()
            item['code'] = response.xpath('//*[@id="table"]/tbody/tr[%s]/td[1]/div/text()' % i).extract()[0]
            item['code_length'] = len(item['code'])
            item['name'] = response.xpath('//*[@id="table"]/tbody/tr[%s]/td[2]/div/@title' % i).extract()[0]
            item['year_id'] = response.xpath('//*[@id="table"]/tbody/tr[%s]/td[3]/div/text()' % i).extract()[0]
            item['first_unit_code'] = response.xpath('//*[@id="table"]/tbody/tr[%s]/td[4]/div/text()' % i).extract()[0]
            item['first_unit_name'] = response.xpath('//*[@id="table"]/tbody/tr[%s]/td[5]/div/text()' % i).extract()[0]
            item['second_unit_code'] = response.xpath('//*[@id="table"]/tbody/tr[%s]/td[6]/div/text()' % i).extract()[0]
            item['second_unit_name'] = response.xpath('//*[@id="table"]/tbody/tr[%s]/td[7]/div/text()' % i).extract()[0]
            yield item