import flask
from flask import Flask, redirect, url_for, request, render_template
from flask_cors import CORS, cross_origin

from User import *
import json

import Main
app = flask.Flask(__name__)
app.config["DEBUG"] = True
CORS(app, support_credentials=True)

@app.route('/', methods=['GET'])
@cross_origin()

def home():
    return app.send_static_file("signIn.html")

@app.route('/sign-in',methods=['get','post'])
@cross_origin()
def sign_in():
    if request.method == 'POST':
        email = request.form['email']
        passwd = request.form['pass']
    else:
        login_json = request.args
        email = login_json.get('email')
        passwd = login_json.get('pass')
    user = Main.login(email , passwd)
    if user is not None :
        if user.user_type  == 1:
            return render_template('managerPage.html' ,var=user.email)
        elif user.user_type == 2:
            return render_template('reception.html',var=email)
        elif user.user_type == 3:
            return render_template('accountant.html',var=email)
        elif user.user_type == 4:
            return render_template('pharmacy.html',var=email)
        elif user.user_type == 5:
            return render_template('patient.html' ,var=email)
        elif user.user_type == 6 :
            return render_template('laboratory.html',var=email)
        elif user.user_type == 7 :
            return render_template('doctor.html',var=email)
        else :
            return app.send_static_file("my.html")
    else:
        return app.send_static_file("sign_in.html")


@app.route('/user-list' , methods=['GET'])
@cross_origin()
def user_list():
    db = DB('localhost', 'root', 'db')
    result = db.find_user_by_email(request.args.get('email'))
    manager = Manager(id=result['id'],name=result['name'], family=result['family'],
                mobile_no=result['mobile_no'], email=result['email'],
                password=result['password'],
                user_type=result['user_type'])


    res =  manager.select_all_user()
    json_s = json.dumps(res)
    return json_s
@app.route('/delete-user',methods=['get'])
@cross_origin()

def delete_user():
    db = DB('localhost', 'root', 'db')
    result = db.find_user_by_email(request.args.get('email'))
    print(result)
    manager = Manager(id=result['id'],name=result['name'], family=result['family'],
                      mobile_no=result['mobile_no'], email=result['email'],
                      password=result['password'],
                      user_type=result['user_type'])
    print(request.args.get('id'))
    manager.delete_user(request.args.get('id'))
    return "hi"
@app.route('/add-user',methods=['get'])
@cross_origin()

def add_user():
    db = DB('localhost', 'root', 'db')
    result = db.find_user_by_email(request.args.get('myEmail'))
    res = request.args
    manager = Manager(id=result['id'],name=result['name'], family=result['family'],
                      mobile_no=result['mobile_no'], email=result['email'],
                      password=result['password'],
                      user_type=result['user_type'])
    user = User(id=res.get('id'),name=res.get('name'), family=res.get('family'),
                mobile_no=res.get('mobile'), email=res.get('email'),
                password=res.get('password'),
                user_type=res.get('user_type'))

    manager.add_user(user)
    return "jodas"

@app.route('/sign-up',methods=['get'])
@cross_origin()

def sign_up():
    res = request.args
    user = User(id=res.get('id'),name=res.get('name'), family=res.get('family'),
                mobile_no=res.get('mobile'), email=res.get('email'),
                password=res.get('password'),
                user_type=res.get('user_type'))
    Main.sign_up(user)
    return "singed up"
@app.route('/time-list',methods=['get'])
@cross_origin()

def dr_time_table():
    json_s = json.dumps(User.dr_time())
    return json_s
@app.route('/add-time-pa-dr',methods=['get'])
@cross_origin()

def set_time_pa_dr():
    res = request.args
    Reception.set_appointment(res.get('dr'),res.get('p'),res.get('week'),res.get('hour'))
    return "done"
@app.route('/add-dr-time',methods=['get'])
@cross_origin()
def add_dr_time():
    res = request.args
    Reception.set_doctors_time_table(res.get('dr'),res.get('week'),res.get('hour'))
    return "done"
@app.route('/bill-list', methods=['get'])
@cross_origin()
def bill_list():
    res = request.args
    json_s = json.dumps(Accountant.get_bill(res.get('p')))
    return json_s
@app.route('/add-item',methods=['get'])
@cross_origin()
def add_bill_item():
    res = request.args
    Accountant.set_bill(cost=res.get('cost'),name=res.get('name'),patient=res.get('p'))
    return "done"

@app.route('/see-medicine',methods=['get'])
@cross_origin()
def see_medicine():
    json_s = json.dumps(Pharmacy.get_medicine())
    return json_s
@app.route('/see-medicine-filter',methods=['get'])
@cross_origin()
def see_medicine_filter():
    json_s = json.dumps(Pharmacy.get_medicine_filter(request.args.get('time')))
    return json_s
@app.route('/add-appo',methods=['get'])
@cross_origin()
def add_appo():
    db = DB('localhost', 'root', 'db')
    result = db.find_user_by_email(request.args.get('email'))
    patient = Patient(id=result['id'], name=result['name'], family=result['family'],
                      mobile_no=result['mobile_no'], email=result['email'],
                      password=result['password'],
                      user_type=result['user_type'])
    patient.get_appointment(request.args.get('dr'),request.args.get('week'),request.args.get('hour'))
    return "done"
@app.route('/see-prescription')
@cross_origin()
def see_prescription():
    db = DB('localhost', 'root', 'db')
    result = db.find_user_by_email(request.args.get('email'))
    patient = Patient(id=result['id'], name=result['name'], family=result['family'],
                      mobile_no=result['mobile_no'], email=result['email'],
                      password=result['password'],
                      user_type=result['user_type'])
    res = patient.see_my_prescription()
    json_S =json.dumps(res)
    return json_S
@app.route('/det-bed')
@cross_origin()
def get_bed():
    db = DB('localhost', 'root', 'db')
    result = db.find_user_by_email(request.args.get('email'))
    patient = Patient(id=result['id'], name=result['name'], family=result['family'],
                      mobile_no=result['mobile_no'], email=result['email'],
                      password=result['password'],
                      user_type=result['user_type'])

app.run()