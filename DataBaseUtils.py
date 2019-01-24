import pymysql.cursors
class DB:
    def __init__(self,host,user,db):
        self.host=host
        self.user=user
        self.db=db

    def data_base_connection(self):
        connection = pymysql.connect(host=self.host,
                                     user=self.user,
                                     db=self.db,
                                     charset='utf8mb4',
                                     cursorclass=pymysql.cursors.DictCursor)

        return connection

    def sign_up(self,user):

        connection = self.data_base_connection()
        sql = 'INSERT INTO `users` (`name`,`family`,`mobile_no`,`email`, `password`,`user_type`) VALUES (%s,%s,%s,%s,%s,%s)'
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (user.name, user.family, user.mobile_no , user.email , user.password , user.user_type))
                connection.commit()

        finally:
            connection.close()

    def find_all(self):
        connection = self.data_base_connection()
        try:
            with connection.cursor() as cursor:
                sql= "select * from `users`"
                cursor.execute(sql)
                result = cursor.fetchall()

        finally:
            connection.close()

        return result

    def find_user_by_email(self,email):
        connection = self.data_base_connection()
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT * FROM `users` WHERE `email`=%s"
                cursor.execute(sql, (email,))
                result = cursor.fetchone()
        finally:
            connection.close()
        return result

    def delete_by_id(self,id):
        connection = self.data_base_connection()
        try:
            with connection.cursor() as cursor:
                # Read a single record
                sql = "delete FROM `users` WHERE `id`=%s"
                cursor.execute(sql, id)
                connection.commit()
        finally:
            connection.close()
        return
