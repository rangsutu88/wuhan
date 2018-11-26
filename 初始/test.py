# import pymongo
# 
# conn=pymongo.MongoClient(host='127.0.0.1',port=27017)
# db=conn['jj']
# collection=db['test']
# collection.insert_one({'name':'jackys'})
# collection.create_index()
ss="fun_CmsDetail('CorpInfoDetail.do?id=713f259d-7aa2-4b55-bc6d-bcfdb71d36bf','ProjectAgengyRateListInit.do','detail')"
import re
req=re.findall(r"'(.+)'",ss)[0].split(r"','")[0]
print(req)
a=None
print(str(a))

# class To_db():
#
#     def __init__(self):
#         self.conn=connect(host='127.0.0.1',
#             user='root',
#             password="123456",
#             database='wuhan',
#             port=3306,
#             charset='utf8')
#         self.cursor=self.conn.cursor()
#
#     def create_db(self):
#
#         self.cursor.execute("DROP TABLE IF EXISTS {}".format(DB_NAME))
#
#
#
#         sql = """CREATE TABLE {} (
#                  FIRST_NAME  CHAR(20),
#                  LAST_NAME  CHAR(20),
#                  AGE INT,
#                  SEX CHAR(1),
#                  INCOME FLOAT )""".format(DB_NAME)
#
#         self.cursor.execute(sql)
#
#     def insert_db(self):
#         try:
#             sql = "INSERT INTO %s (FIRST_NAME,LAST_NAME, AGE, SEX, INCOME) \
#                    VALUES ('%s', '%s', '%s', '%s', '%s' )" % \
#               (DB_NAME,'Mac', 'Mohan', 20, 'M', 2000)
#             # 插入数据
#             self.cursor.execute(sql)  # 执行sql
#             self.conn.commit()  # 提交
#         except:
#             self.conn.rollback()
#
#     def colse_db(self):
#         self.cursor.close()
#         self.conn.close()

str_='abcd'
url='http://'
print(''.join((url,str_)))
