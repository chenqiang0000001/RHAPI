# import pymysql
#
#
# class ConnectDB:
#     """
#     使用方法：
#     1.创建db实例 db = ConnectDB();
#     2.执行select操作 res = db("select", sql)
#     3.执行insert, update, delete操作 db("update", sql)
#     4.所有增删改查都执行完毕了，进行数据库链接的关闭 db(connect=False)
#     5.注意：数据库关闭后，需要重新实例化才可继续进行增删改查；
#     """
#     config = {
#         "host": "121.40.244.254",
#         "user": "chenqiang",
#         "password": "cozHLpjNiHfOrYBo",
#         "database": "test_femooi",
#         "charset": "utf8"
#     }
#
#     def __init__(self):
#         self.conn = pymysql.connect(**self.config)
#
#     def select_datas(self, sql):  # select
#         cur = self.conn.cursor(pymysql.cursors.DictCursor)  # 创建游标
#         cur.execute(sql)  # 通过游标执行sql语句
#         res = cur.fetchall()  # 通过游标获取执行结果
#         cur.close()
#         return res
#
#     def modify_datas(self, sql):  # update, insert, delete
#         cur = self.conn.cursor()  # 创建游标
#         cur.execute(sql)  # 执行sql语句
#         self.conn.commit()  # 提交事务
#         cur.close()
#
#     def connect_close(self):  # 关闭数据库
#         self.conn.close()
#
#     def __call__(self, act=None, sql=None, connect=True):
#         if connect:  # 如果connect 为 True
#             if act == 'select':
#                 datas = self.select_datas(sql)
#                 return datas
#             elif act in ['update', 'insert', 'delete']:
#                 self.modify_datas(sql)
#
#         else:  # 当connect 为 False 时关闭数据库的连接
#             self.connect_close()
#
#
# if __name__ == '__main__':
#     c = ConnectDB()
#     status = 'SELECT status FROM user_nurse_message WHERE tid = 16'
#     data1 = c.select_datas(status)
#     print(data1)