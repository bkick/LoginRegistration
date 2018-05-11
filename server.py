from flask import Flask, render_template, request, redirect, flash, session
from flask_bcrypt import Bcrypt
from mysqlconnection import connectToMySQL
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
app = Flask(__name__)
bcrypt = Bcrypt(app)
mysql = connectToMySQL('mydb')

app.secret_key='swag'
@app.route('/')
def index():
    return render_template("index.html")
@app.route('/reg', methods=['POST'])
def submit():
    if len(request.form['email']) < 1:
        flash("Email cannot be blank!", 'email')
        print(1)
        return redirect('/')
    elif not EMAIL_REGEX.match(request.form['email']):
        print(2)
        flash("Invalid Email Address!", 'email')
        return redirect('/')
    if len(request.form['first_name']) < 1:
        print(3)
        flash("Name cannot be blank!")
        return redirect('/')
    elif len(request.form['first_name']) <= 3:
        print(4)
        flash("First Name must be 3+ characters")
        return redirect('/')
    if len(request.form['last_name']) < 1:
        print(5)
        flash("Last Name cannot be blank!",)
        return redirect('/')
    elif len(request.form['last_name']) <= 3:
        print(6)
        flash("Last Name must be 3+ characters")
        return redirect('/')
    if len(request.form['pwd'])<1:
        print(7)
        flash("Password cannot be empty")
        return redirect('/')
    if request.form['pwdconf']!= request.form['pwd']:
        print(8)
        flash("Password and confirm password must match")
        return redirect('/')
    else:
        pw_hash=bcrypt.generate_password_hash(request.form['pwd'])
        session ['name']=request.form['first_name']
        query="INSERT INTO persons (first_name,last_name, email, password)VALUES(%(first_name)s, %(last_name)s, %(email)s, %(password)s);"
        data={'email':request.form['email'], 'first_name': request.form['first_name'], 'last_name': request.form['last_name'], 'password':pw_hash}
        result=mysql.query_db(query,data)
        print(query)
        print(result)
        return redirect('/success')
@app.route('/login', methods=['POST'])
def login():
    query = "SELECT * FROM persons WHERE email = %(email)s;"
    data = { 'email' : request.form['email'] }
    result = mysql.query_db(query, data)
    print (result)
    print(result[0]['password'])
    if result:
        if bcrypt.check_password_hash(result[0]['password'], request.form['password']):
            session['name']=result[0]['first_name']
            return render_template ('success.html')  
        else:
            print('password incorrect')
            flash("you could not be logged in")
            return redirect('/')      
    else:
        flash("you could not be logged in")
        return redirect('/')

@app.route('/success')
def success():
    return render_template('success.html')
if __name__ == "__main__":
    app.run(debug=True)