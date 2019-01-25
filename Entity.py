from DataBaseUtils import DB
class Time:
    def __init__(self,user,week_day,hour):
        self.user=user
        self.week_day=week_day
        self.hour=hour
    def add_time(self):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'INSERT INTO `time` (`user_id`,`week_day`,`hours`) VALUES (%s,%s,%s)'
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (self.user.id, self.week_day,self.hour))
                connection.commit()

        finally:
            connection.close()
        return
    def see_doctor_time(self,user):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        try:
            with connection.cursor() as cursor:
                sql = "SELECT * FROM `time` WHERE `user_id`=%s"
                cursor.execute(sql, (user.id,))
                result = cursor.fetchall()
        finally:
            connection.close()
        return result
    def set_appoinetment(self,dr_id,p_id,weekday,hour):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        try:
            with connection.cursor() as cursor:
                sql = 'INSERT INTO `time_table` (`dr_id`,`p_id`,`week_day`,`hours`) VALUES (%s,%s,%s,%s)'
                cursor.execute(sql, (dr_id,p_id,weekday,hour))
                connection.commit()

        finally:
            connection.close()
        return
class Item:
    def __init__(self,p,name,cost):
        self.p=p
        self.name=name
        self.cost=cost
    def add_item(self):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'INSERT INTO `item` (`name`,`p_id`,`cost`) VALUES (%s,%s,%s)'
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (self.name, self.p,self.cost))
                connection.commit()

        finally:
            connection.close()
        return
    @staticmethod
    def get_all(p):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'select * from `item` WHERE p_id =%s '
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql,(p,))
                result = cursor.fetchall()
        finally:
            connection.close()
        return result
class Medicine:
    def __init__(self,name,expiration,count):
        self.name=name
        self.expiration=expiration
        self.count=count
    @staticmethod
    def find_all():
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'select * from `medicine` '
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
        finally:
            connection.close()
        return result
    @staticmethod
    def find_all_filter(time):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'select * from `medicine` WHERE  `expiration_date` > %s'
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql,(time,))
                result = cursor.fetchall()
        finally:
            connection.close()
        return result
class Prescription:
    def __init__(self,dr_id,p_id):
        self.dr_id=dr_id
        self.p_id=p_id


class PrescriptionItem:
    def __init__(self,med_id,pre_id,count):
        self.pre_id=pre_id
        self.med_id=med_id
        self.count=count

class Message:
    def __init__(self, sender_id, receiver_id, title,body):
        self.sender_id = sender_id
        self.receiver_id = receiver_id
        self.title = title
        self.body=body
    def save(self):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'INSERT INTO `mail` (`sender_id`,`receive_id`,`title`,`body`) VALUES (%s,%s,%s,%s)'
        try:
            with connection.cursor() as cursor:
                 cursor.execute(sql, (self.sender_id,self.receiver_id,self.title,self.body))
                 connection.commit()
        finally:
            connection.close()

class LabPrescription:
    def __init__(self,doctor_id,patient_id,name):
        self.doctor_id = doctor_id
        self.patient_id = patient_id
        self.name=name
