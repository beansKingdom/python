# -*- coding: UTF-8 -*-

import get_conf as gcf
import pymysql
import tkMessageBox

class ConnectMysql:
    def __init__(self):
        self.mysql_dict = {}
        self.get_mysql_conf()

    def get_mysql_conf(self):
        gcf.get_config(self.mysql_dict)

    def connect_mysql(self):
        try:
            # self.conn   : the connect of mysql
            self.conn = pymysql.connect(self.mysql_dict['my_host'], self.mysql_dict['my_user'], self.mysql_dict['my_passwd'],
                                        self.mysql_dict['my_dbname'],int(self.mysql_dict['my_port']), charset='utf8')
        except pymysql.Error as err:
            tkMessageBox.showerror("ERROR INFO", "Mysql Error %d: %s" % (err.args[0], err.args[1]))
            raise Exception("ERROR INFO : Mysql Error %d: %s" % (err.args[0], err.args[1]))

