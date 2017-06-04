# encoding:utf-8

import ConfigParser

cf = ConfigParser.ConfigParser()
cf.readfp(open('mysql.conf'))

def get_config(myinfo):
    # read values
    myinfo['my_host']   = cf.get('db', 'db_host_ip')
    myinfo['my_port']   = cf.getint('db', 'db_port')
    myinfo['my_user'] = cf.get('db', 'db_user')
    myinfo['my_passwd']  = cf.get('db', 'db_passwd')
    myinfo['my_dbname'] = cf.get('db', 'db_dbname')


# #===========================================================
# def get_config():
