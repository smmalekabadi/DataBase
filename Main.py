from User import User
import pymysql.cursors
from DataBaseUtils import DB
def login(email,password):
    connection = data_base_connection('localhost' , 'root', 'db')
    try:
        with connection.cursor() as c :
            query = "SELECT * FROM `users` WHERE `email` = %s and `password` = %s"
            c.execute(query,(email,password))
            result = c.fetchone()
    finally:
        connection.close()
    if result is None  :
        return "password or login is not correct"
    else:
        user = User(id=result['id'],name=result['name'],family=result['family'],
                    mobile_no=result['mobile_no'],email= result['email'],
                    password=result['password'],
                    user_type=result['user_type'])
        print(result['name'])
        return user


def sign_up(user):
    db = DB('localhost' , 'root', 'db')
    connection = db.data_base_connection()
    sql = 'INSERT INTO `users` (`name`,`family`,`mobile_no`,`email`, `password`,`user_type`) VALUES (%s,%s,%s,%s,%s,%s)'
    try:
        with connection.cursor() as cursor:
            cursor.execute(sql, (user.name, user.family, user.mobile_no,
                                 user.email, user.password, user.user_type))
            connection.commit()

    finally:
        connection.close()


def data_base_connection(host,user,db):
    connection = pymysql.connect(host=host,
                                 user=user,
                                 db=db,
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    return connection


def dataBaseAcces():
    # Connect to the database
    connection = pymysql.connect(host='localhost',
                                 user='root',
                                 db='db',
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)

    try:
        with connection.cursor() as cursor:
            # Create a new record
            sql = "INSERT INTO `users` (`name`,`family`,`mobile_no`,`email`, `password`) VALUES (%s, %s,%s, %s,%s)"
            cursor.execute(sql, ('morty', 'malek', '09105613709', 'webmaster@python.org', 'very-secret'))

        # connection is not autocommit by default. So you must commit to save
        # your changes.
        connection.commit()

        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT `id`, `password` FROM `users` WHERE `email`=%s"
            cursor.execute(sql, ('webmaster@python.org',))
            result = cursor.fetchone()
            print(result)
    finally:
        connection.close()
    print("end")
    return


#
# email = input("what is your email ?")
# password = input("enter your password")
# print(login(email,password))
# # (self, name, family, mobile_no, password, email)
# sign_up(None)#