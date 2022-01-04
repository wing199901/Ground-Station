import pymysql

from config import MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB


class MysqlDb():
    def __init__(self, host, port, user, passwd, db):
        self.conn = pymysql.connect(
            host=host,
            port=port,
            user=user,
            passwd=passwd,
            db=db
        )
        self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)

    def select_db(self, sql):
        # check connection
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        return data

    def execute_db(self, sql):
        try:
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql)
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            return e

    def __del__(self):
        self.cursor.close()
        # database disconnect
        self.conn.close()


db = MysqlDb(MYSQL_HOST, MYSQL_PORT, MYSQL_USER, MYSQL_PASSWD, MYSQL_DB)
