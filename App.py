from flask import Flask, render_template, request, redirect, url_for, session, send_file, flash
import mysql.connector
import pygame
import pygame as pg
import base64, os, sys

app = Flask(__name__)
app.secret_key = 'a'
import time
import datetime
import sys


@app.route('/')
def home():
    return render_template('Index.html')


@app.route('/AdminLogin')
def AdminLogin():
    return render_template('AdminLogin.html')


@app.route('/UserLogin')
def UserLogin():
    return render_template('UserLogin.html')


@app.route('/NewUser')
def NewUser():
    return render_template('NewUser.html')


@app.route('/Game')
def Game():
    return render_template('Game.html')


@app.route("/adminlogin", methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        if request.form['uname'] == 'admin' and request.form['password'] == 'admin':

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
            cur = conn.cursor()
            cur.execute("SELECT * FROM regtb ")
            data = cur.fetchall()
            return render_template('AdminHome.html', data=data)

        else:
            alert = 'Username or Password is wrong'
            return render_template('AdminLogin.html', res=alert)


@app.route("/AdminHome")
def AdminHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/PlayInfo")
def PlayInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM gametb")
    data = cur.fetchall()
    return render_template('PlayInfo.html', data=data)


@app.route("/PaymentInfo")
def PaymentInfo():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM  paymenttb")
    data = cur.fetchall()
    return render_template('PaymentInfo.html', data=data)


@app.route("/newuser", methods=['GET', 'POST'])
def newuser():
    if request.method == 'POST':
        uname = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        username = request.form['username']
        password = request.form['password']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO regtb VALUES ('','" + uname + "','" + mobile + "','" + email + "','" + address + "','" + username + "','" + password + "')")
        conn.commit()
        conn.close()

        return render_template('UserLogin.html')


@app.route("/userlogin", methods=['GET', 'POST'])
def userlogin():
    if request.method == 'POST':

        username = request.form['uname']
        password = request.form['password']

        session['uname'] = request.form['uname']

        conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
        cursor = conn.cursor()
        cursor.execute("SELECT * from regtb where username='" + username + "' and Password='" + password + "' ")
        data = cursor.fetchone()
        if data is None:

            data = 'Username or Password is wrong'
            return render_template('UserLogin.html', res=data)

        else:

            conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
            cursor = conn.cursor()
            cursor.execute("SELECT * from paymenttb where username='" + username + "' ")
            data = cursor.fetchone()
            if data is None:
                return render_template('Payment.html')

            else:
                    session['username']=username
                    return render_template('UserWelcome.html')


@app.route("/payment", methods=['GET', 'POST'])
def payment():
    if request.method == 'POST':
        uname = session['uname']
        mobile = request.form['amt']
        email = request.form['cname']
        address = request.form['cardno']
        username = request.form['cvvno']
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
        timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO paymenttb VALUES ('','" + uname + "','" + mobile + "','" + date + "','" + email + "','" + address + "','" + username + "')")
        conn.commit()
        conn.close()
        res = 'Payment Successful'
        return render_template('Payment.html',res=res)


@app.route('/Profile')
def UserProfile():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb where username='" + session['uname'] + "'")
    data1 = cur.fetchall()
    return render_template('Profile.html', data=data1)

#@app.route('/UserHome')
#def UserHome():
#    conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
#    cur = conn.cursor()
#    cur.execute("SELECT * FROM regtb where username='" + session['uname'] + "'")
#    data1 = cur.fetchall()
#   return render_template('UserHome.html', data=data1)*/

@app.route("/UserHome")
def UserHome():
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM gametb where username='" + session['uname'] + "'")
    data = cur.fetchall()
    return render_template('UserHome.html', data=data)


@app.route('/update')
def update():
    id = request.args.get('id')
    session['id'] = id
    return render_template('Update.html')


@app.route('/delete')
def delete():
    id = request.args.get('id')
    conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
    cursor = conn.cursor()
    cursor.execute(
        "delete from   regtb  where id='" + id + "'")
    conn.commit()
    conn.close()

    conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
    cur = conn.cursor()
    cur.execute("SELECT * FROM regtb")
    data = cur.fetchall()
    return render_template('AdminHome.html', data=data)


@app.route("/uuupdate", methods=['GET', 'POST'])
def uuupdate():
    if request.method == 'POST':
        uname = request.form['uname']
        mobile = request.form['mobile']
        email = request.form['email']
        address = request.form['address']
        conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
        cursor = conn.cursor()
        cursor.execute(
            "update  regtb set Name='" + uname + "',Mobile='" + mobile + "',Email='" + email + "',Address='" + address + "' where id='" +
            session['id'] + "'")
        conn.commit()
        conn.close()

        return render_template('Update.html', res='Record Update')


@app.route("/selectgame", methods=['GET', 'POST'])
def selectgame():
    if request.method == 'POST':
        if request.form["submit"] == "Minigolf":

            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO gametb VALUES ('','" + session['uname'] + "','Minigolf','" + date + "','" + timeStamp + "')")
            conn.commit()
            conn.close()
            import sys
            from data.mini_golf.main import main
            import minigolf
            main()
            return render_template('Game.html')



        elif request.form["submit"] == "Mario":
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO gametb VALUES ('','" + session['uname'] + "','Mario','" + date + "','" + timeStamp + "')")
            conn.commit()
            conn.close()
            import mario
            return render_template('Game.html')


        else:
            ts = time.time()
            date = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d')
            timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
            conn = mysql.connector.connect(user='root', password='', host='localhost', database='arcadiadb')
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO gametb VALUES ('','" + session['uname'] + "','AngryBird','" + date + "','" + timeStamp + "')")
            conn.commit()
            conn.close()
            import angrybird
            return render_template('Game.html')
    pygame.display.quit()
    pygame.quit()
    return render_template('Game.html')


def sendmail(Mailid, message):
    import smtplib
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    from email.mime.base import MIMEBase
    from email import encoders

    fromaddr = "sampletest685@gmail.com"
    toaddr = Mailid

    # instance of MIMEMultipart
    msg = MIMEMultipart()

    # storing the senders email address
    msg['From'] = fromaddr

    # storing the receivers email address
    msg['To'] = toaddr

    # storing the subject
    msg['Subject'] = "Alert"

    # string to store the body of the mail
    body = message

    # attach the body with the msg instance
    msg.attach(MIMEText(body, 'plain'))

    # creates SMTP session
    s = smtplib.SMTP('smtp.gmail.com', 587)

    # start TLS for security
    s.starttls()

    # Authentication
    s.login(fromaddr, "hneucvnontsuwgpj")

    # Converts the Multipart msg into a string
    text = msg.as_string()

    # sending the mail
    s.sendmail(fromaddr, toaddr, text)

    # terminating the session
    s.quit()


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, port=5000)
    # app.run(debug=True, use_reloader=True)