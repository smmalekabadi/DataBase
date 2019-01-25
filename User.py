from DataBaseUtils import DB
from Entity import Item, Medicine, Message


class User:
    def __init__(self,id, name, family, mobile_no, password, email,user_type):
        self.id=id
        self.name = name
        self.family = family
        self.mobile_no = mobile_no
        self.password = password
        self.email = email
        self.user_type = user_type
    def save(self):
        db = DB('localhost', 'root', 'db')
        db.sign_up(self)
        return
    def save_me(self,name,family,mobile_no,email,password):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        try:
            sql = "UPDATE `users` SET `name`=%s,`family`=%s,`mobile_no`=%s,`email`=%s,`password`=%s WHERE `email`=%s "
            with connection.cursor() as cursor:
                cursor.execute(sql,(name,family,mobile_no,email,password,self.email))
                connection.commit()

        finally:
            connection.close()
    @staticmethod
    def dr_time():
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'select * from `time`'
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql)
                result = cursor.fetchall()
                return result
        finally:
            connection.close()
        return result
    def send_message(self,message):
        m = Message(self.id, message.get('rid'), message.get('title'), message.get('body'))
        m.save()
        return "done"
    def see_messages(self):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        try:
            with connection.cursor() as cursor:
                sql = 'select * from `mail` where `receive_id` = %s '
                cursor.execute(sql,(self.id,))
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

class Manager(User): #user_type_id = 1
    def add_user(self, user):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'INSERT INTO `users` (`name`,`family`,`mobile_no`,`email`, `password`,`user_type`) VALUES (%s,%s,%s,%s,%s,%s)'
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (user.name, user.family,user.mobile_no,
                                     user.email,user.password, user.user_type))
                connection.commit()

        finally:
            connection.close()
        return  # add user to data base

    def delete_user(self,id):
        db = DB('localhost', 'root', 'db')
        db.delete_by_id(id)
        return  # delete user from data base
    def select_all_user(self):
        db = DB('localhost', 'root', 'db')
        return db.find_all()



class Reception(User): #user_type_id = 2
    def delete(self, id):
        # check = whether is doctor available
        return

    @staticmethod
    def set_appointment(doctor, patient, weekday, hour):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'INSERT INTO `time_table` (`dr_id`,`p_id`,`weekday`,`hour`) VALUES (%s,%s,%s,%s)'
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (doctor,patient,weekday,hour))
                connection.commit()

        finally:
            connection.close()
        return

    @staticmethod
    def set_doctors_time_table(doctor,days,hour):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'INSERT INTO `time` (`dr_id`,`week_day`,`hours`) VALUES (%s,%s,%s)'
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (doctor, days, hour))
                connection.commit()

        finally:
            connection.close()
        return

class Accountant(User): #user_type_id = 3

    @staticmethod
    def set_bill(name, patient, cost):
        item =Item(name=name,p=patient,cost=cost)
        item.add_item()
        return

    @staticmethod
    def get_bill(p):
        return Item.get_all(p)


class Pharmacy(User): #user_type_id = 4
    @staticmethod
    def get_medicine():
        med = Medicine.find_all()
        return med

    @staticmethod
    def get_medicine_filter(time):
        med = Medicine.find_all_filter(time)
        return med

class Patient(User): #user_type_id = 5
    def get_appointment(self,doctor, weekday,hour):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'INSERT INTO `time_table` (`dr_id`,`p_id`,`weekday`,`hour`) VALUES (%s,%s,%s,%s)'
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (doctor,self.id, weekday, hour))
                connection.commit()

        finally:
            connection.close()
        return "done"
    def see_my_prescription(self):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'select p.p_id,p.dr_id,i.name from `prescription` as p ' \
              'inner join `prescription_item` as pi on p.id = pi.pr_id ' \
              'inner join `item` as i on i.id = pi.item_id ' \
              'WHERE p.p_id = %s'
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (self.id,))
                result = cursor.fetchall()
                return result

        finally:
            connection.close()

    def get_bed(self):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()


        try:
            with connection.cursor() as cursor:

                sql = "SELECT * FROM `bed` WHERE `isEmpty`=%s"
                cursor.execute(sql, (True,))
                result = cursor.fetchone()

                sql = 'INSERT INTO `patient_bed` (`patient_id`,`bed_id`) VALUES (%s,%s)'

                cursor.execute(sql, (self.id,result['id']))
                connection.commit()

                sql = 'update `bed` set `isEmpty` = %s where id = %s'
                cursor.execute(sql, (False,result['id']))
                connection.commit()
        finally:
            connection.close()
        return "done"
    def get_bed_data(self):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        try:
            with connection.cursor() as cursor:
                sql = "select * from `bed` as b " \
                      "inner join `patient_bed` pb on b.id = pb.bed_id " \
                      "where pb.patient_id = %s "
                cursor.execute(sql, (self.id,))
                result = cursor.fetchone()
                return result

        finally:
            connection.close()
class Laboratory(User): #user_type_id = 6
    def take_test(self,lab_prescription):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'update `lab_prescription` set `isDone` = %s where id = %s'
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (True, lab_prescription))
                connection.commit()
        finally:
            connection.close()
        return
class Doctor(User): #user_type_id = 7
    def visit(self, patient):
        return
    def see_time_table(self):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'select * from `time_table` where `dr_id` = %s '
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql,(self.id,))
                result = cursor.fetchall()
                return result
        finally:
            connection.close()

    @staticmethod
    def see_prescription_history(pid):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'select p.p_id,p.dr_id,i.name from `prescription` as p ' \
              'inner join `prescription_item` as pi on p.id = pi.pr_id ' \
              'inner join `item` as i on i.id = pi.item_id ' \
              'WHERE p.p_id = %s'
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (pid,))
                result = cursor.fetchall()
                return result

        finally:
            connection.close()

    def lab_prescription(self,p,name):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        sql = 'INSERT INTO `lab_prescription`(`doctor_id`, `patient_id`, `name`) VALUES (%s,%s,%s)'
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, (self.id,p,name))
                connection.commit()

        finally:
            connection.close()
    def comfirm_time(self,time):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        try:
            with connection.cursor() as cursor:
                sql = 'update `time_table` set `accepted` = %s where id = %s'
                cursor.execute(sql, (True, time))
                connection.commit()
        finally:
            connection.close()

    def ignore_time(self, time):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        try:
            with connection.cursor() as cursor:
                sql = 'update `time_table` set `accepted` = %s where id = %s'
                cursor.execute(sql, (False, time))
                connection.commit()
        finally:
            connection.close()
    def make_pres(self,pid):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        try:
            with connection.cursor() as cursor:
                sql = 'insert into `prescription` ( `dr_id`, `p_id`) VALUES (%s,%s) '
                cursor.execute(sql, (self.id, pid))
                connection.commit()
        finally:
            connection.close()
        return "done"
    @staticmethod
    def add_item(pres_id, item_id):
        db = DB('localhost', 'root', 'db')
        connection = db.data_base_connection()
        try:
            with connection.cursor() as cursor:
                sql = 'insert into `prescription_item` ( `pr_id`, `item_id`) VALUES (%s,%s) '
                cursor.execute(sql, (pres_id, item_id))
                connection.commit()
        finally:
            connection.close()
        return "done"