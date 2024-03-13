from flask import Flask, render_template, request, redirect, url_for
from flask_mail import Mail,Message
app1 = Flask(__name__)

from database import addUser, loginCheck

    

print ("db closed")

@app1.route('/',methods = ['POST','GET'])
def login():
    if request.method == 'POST':
        print('STEP01')
        email1 = request.form['email']
        password1 = request.form['password']

        print(email1)
        print(password1)

        if loginCheck(email1, password1):
            return redirect(url_for('messagePage'))
        else :
            text1 = 'User not registered, please register first'
            return render_template('login.html', msg = text1)
      
    else:
        print("LOGIN")
        return render_template("login.html")

@app1.route('/signup', methods=['POST','GET'])
def signup():

    if request.method == 'POST':
        # id = request.form['id']
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        password2 = request.form['confirm-password']

        if password != password2: return render_template("signup.html", msg='Password is not matching')
        print(f' {name} {email} {password}')
        password = password.encode()
        if addUser( email, name, password):
            return redirect(url_for('messagePage'))
        else :
            return render_template("signup.html")
    return render_template("signup.html")

@app1.route('/msg')
def messagePage():
    return render_template('msg.html')


if __name__=="__main__":
    app1.run(debug=True)