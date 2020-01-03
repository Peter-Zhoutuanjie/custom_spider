# encoding: utf-8
import pymysql.cursors
import distribute_setting as distribute_setting

class DataSource(object):

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


    def get_url_lst(self):
        self.cursor.execute("SELECT id,url,ie_type FROM `job_url_state_%s` ORDER BY id %s limit %s" % (
        distribute_setting.CRAWL_YEAR, distribute_setting.CRAWL_SEQ, distribute_setting.START_URL_NUM))
        return self.cursor.fetchall()

    def del_url(self, id):
        self.cursor.execute("delete FROM `job_url_state_%s` where id = %s" % (distribute_setting.CRAWL_YEAR, id))
        self.connect.commit()

    def get_urls_port(self):
        self.cursor.execute("SELECT id,url,ie_type FROM `job_url_port` where year = '%s' ORDER BY id %s limit %s" % (
        distribute_setting.CRAWL_YEAR, distribute_setting.CRAWL_SEQ, distribute_setting.START_URL_NUM))
        return self.cursor.fetchall()

    def del_url_port(self, id):
        self.cursor.execute("delete FROM `job_url_port` where id = %s" % id)
        self.connect.commit()

    def get_urls_partner(self):
        self.cursor.execute("SELECT id,url,ie_type FROM `job_url_partner` where year = '%s' ORDER BY id %s limit %s" % (
        distribute_setting.CRAWL_YEAR, distribute_setting.CRAWL_SEQ, distribute_setting.START_URL_NUM))
        return self.cursor.fetchall()

    def del_url_partner(self, id):
        self.cursor.execute("delete FROM `job_url_partner` where id = %s" % id)
        self.connect.commit()

    def insertUrlsBatch(self,table,url_lst, year):
        sql = "INSERT INTO `job_url_"+table+"` (`url`,`ie_type`,`year`) VALUES (%s, %s,'" + str(year) + "')"
        try:
            self.cursor.executemany(sql, url_lst)
            self.connect.commit()
        except Exception as e:
            print(e)
