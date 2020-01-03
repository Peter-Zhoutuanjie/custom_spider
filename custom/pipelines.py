import pymysql.cursors
from .items import *
import distribute_setting as distribute_setting


class MySQLPipeline(object):
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

    def process_item(self, item, spider):
        try:
            if isinstance(item, TradeGoodsPortItem):
                sql = "INSERT INTO `trade_goods_port_" + distribute_setting.CRAWL_YEAR + "` (`month`, `goods_code`, `goods`, `port_code`, `port_name`, `first_num`, `first_unit`, `second_num`, `second_unit`, `price`, `ie_type`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                self.cursor.execute(sql, (item['month'], item['goods_code'], item['goods'],item['port_code'], item['port_name'], item['first_num'],item['first_unit'], item['second_num'], item['second_unit'], item['price'], item['ie_type']))
                self.connect.commit()
            elif isinstance(item, TradeGoodsPartnerItem):
                sql = "INSERT INTO `trade_goods_partner_" + distribute_setting.CRAWL_YEAR + "` (`month`, `goods_code`, `goods`, `partner_code`, `partner_name`, `first_num`, `first_unit`, `second_num`, `second_unit`, `price`, `ie_type`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);"
                self.cursor.execute(sql, (item['month'], item['goods_code'], item['goods'], item['partner_code'], item['partner_name'], item['first_num'],item['first_unit'], item['second_num'], item['second_unit'], item['price'], item['ie_type']))
                self.connect.commit()
            elif isinstance(item, TradeGoodsItem):
                sql = "INSERT INTO `trade_goods_" + distribute_setting.CRAWL_YEAR + "` (`month`, `goods_code`, `goods`, `partner_code`, `partner_name`, `port_code`, `port_name`, `first_num`, `first_unit`, `second_num`, `second_unit`, `price`, `ie_type`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
                self.cursor.execute(sql, (item['month'], item['goods_code'], item['goods'], item['partner_code'], item['partner_name'],item['port_code'], item['port_name'], item['first_num'],item['first_unit'], item['second_num'], item['second_unit'], item['price'], item['ie_type']))
                self.connect.commit()
        except Exception as e:
            print(e)
        return item  # 必须实现返回
