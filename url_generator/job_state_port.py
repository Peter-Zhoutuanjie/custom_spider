# encoding: utf-8
import pymysql.cursors
import distribute_setting as distribute_setting


class JobState(object):

    url_lst = []

    def __init__(self):
        # 连接数据库
        self.connect = pymysql.connect(
            host=distribute_setting.MYSQL_HOST,
            port=3306,
            db=distribute_setting.MYSQL_DB,
            user=distribute_setting.MYSQL_USERNAME,
            passwd=distribute_setting.MYSQL_PASSWORD,
            charset='utf8',
            use_unicode=True)
        # 通过cursor执行增删查改
        self.cursor = self.connect.cursor()

    def url_job(self):
        years = [2017]
        for year in years:
            self.cursor.execute("SELECT code FROM `sel_trade_port`")
            port_codes = self.cursor.fetchall()
            for port_code in port_codes:
                self.cursor.execute("SELECT code FROM `goods_code` where code_length = 2 and year_id = %s" % year)
                goods_codes = self.cursor.fetchall()
                for good_code in goods_codes:
                    ie_types = [0, 1]
                    for ie_type in ie_types:
                        self.do_process(ie_type, year, port_code[0], good_code[0])
                self.insertDataBatch(year)

    def do_process(self, ie_type, year, port_code, goods_code):
        url = 'pageNum=1&pageSize=9999&iEType' \
              '=%s&currencyType=rmb&year=%s&startMonth=1&endMonth=12&monthFlag=1&codeTsFlag=true' \
              '&codeLength=2&outerField1=CODE_TS&outerField2=&outerField3' \
              '=TRADE_CO_PORT&outerField4=&outerValue1=%s&outerValue2=&outerValue3=%s&outerValue4' \
              '=&orderType=PRICE+DESC&historyTable=true' % (ie_type, year, goods_code, port_code)
        item = (url, ie_type)
        self.url_lst.append(item)

    def insertDataBatch(self, year):
        # SQL 插入语句
        sql = "INSERT INTO `job_url_port` (`url`,`ie_type`,`year`) VALUES (%s, %s,'"+str(year)+"')"
        try:
            # 执行sql语句
            self.cursor.executemany(sql, self.url_lst)
            # 提交到数据库执行
            self.connect.commit()
            self.url_lst = []
        except Exception as e:
            print(e)


if __name__ == '__main__':
    job = JobState()
    job.url_job()
