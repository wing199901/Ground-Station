import pymysql
from mysql_config import *
import threading


lock = threading.Lock()


class MysqlDb():

    isConnected = False

    # init mysql
    def __init__(self):
        if not self.isConnected:
            self.isConnected = self.connect()

    def connect(self):
        try:
            self.conn = pymysql.connect(
                host=MYSQL_HOST,
                port=MYSQL_PORT,
                user=MYSQL_USER,
                passwd=MYSQL_PASSWD,
                db=MYSQL_DB,
                connect_timeout=2,
                read_timeout=5
            )
            self.cursor = self.conn.cursor(cursor=pymysql.cursors.DictCursor)
            print("connect mysql success")
            return True
        except pymysql.Error as err:
            print("Connect mysql fail, error =", err)
            return False

    def select_db(self, sql):
        lock.acquire()
        # check connection
        self.conn.ping(reconnect=True)
        self.cursor.execute(sql)
        data = self.cursor.fetchall()
        lock.release()
        return data

    def execute_db(self, sql):
        try:
            lock.acquire()
            self.conn.ping(reconnect=True)
            self.cursor.execute(sql)
            self.conn.commit()
            lock.release()
        except Exception as err:
            self.conn.rollback()
            return err

    def __del__(self):
        try:
            self.cursor.close()
            # MySQL disconnect
            self.conn.close()
        except Exception as err:
            return err


db = MysqlDb()
