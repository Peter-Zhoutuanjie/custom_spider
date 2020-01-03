# encoding: utf-8
from datasource import DataSource

class JobState(object):

    url_lst = []

    years = [2017]

    datasource = DataSource()

    def url_job(self):
        for year in self.years:
            self.cursor.execute("SELECT code FROM `sel_trade_port`")
            port_codes = self.cursor.fetchall()
            for port_code in port_codes:
                self.cursor.execute("SELECT code FROM `goods_code` where code_length = 2 and year_id = %s" % year)
                goods_codes = self.cursor.fetchall()
                for good_code in goods_codes:
                    ie_types = [0, 1]
                    for ie_type in ie_types:
                        self.do_process(ie_type, year, port_code[0], good_code[0])
                self.datasource.insertUrlsBatch('port', self.url_lst, year)
                self.url_lst = []

    def do_process(self, ie_type, year, port_code, goods_code):
        url = 'pageNum=1&pageSize=9999&iEType' \
              '=%s&currencyType=rmb&year=%s&startMonth=1&endMonth=12&monthFlag=1&codeTsFlag=true' \
              '&codeLength=2&outerField1=CODE_TS&outerField2=&outerField3' \
              '=TRADE_CO_PORT&outerField4=&outerValue1=%s&outerValue2=&outerValue3=%s&outerValue4' \
              '=&orderType=PRICE+DESC&historyTable=true' % (ie_type, year, goods_code, port_code)
        item = (url, ie_type)
        self.url_lst.append(item)


if __name__ == '__main__':
    job = JobState()
    job.url_job()
