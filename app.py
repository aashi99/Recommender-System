from flask import Flask,render_template,request,redirect,url_for,session
from flask_mysqldb import MySQL
import MySQLdb.cursors
#import re
import MovieImport
import logics
import csv

c=" "
app=Flask(__name__)
app.secret_key = '1999'


#setting up connection Details
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'root'
app.config['MYSQL_DB'] = 'pythonlogin'

mysql=MySQL(app)
print("hello hii")
@app.route("/")
def home():
    msg=''
    print("hello login")
    return render_template('index.html',msg=msg)

@app.route("/login",methods=['GET','POST'])
def login():
    msg1=''
    print("hello")
    # userid = ''
    #userid=''
    #password=''
    #basic check at login if data is already carried to login.html
    if request.method=='POST' and 'userid' in request.form and 'password' in request.form:
        # print("hii")
        userid=request.form["userid"]
        password=request.form["password"]

#getting required row from db
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE userid = %s AND password = %s', (userid, password))
        # Fetch one record and return result
        account = cursor.fetchone() #account is a dictionary



# user authentication
        if account:
            # print("hello")
            global c
            c=0
            session['username']=account['name']
            session['loggedin']=True
            c=session['id']=account['userid']
            msg1='hello '+session['username']
            #msg4 = list(logics.getpopular())
            return redirect(url_for('rate_movies'))
            #return render_template('rate_movies.html')
        else:
            msg1='Incorrect UserId/password'
    return render_template('login.html',msg1=msg1)

@app.route("/logout")
def logout():
    session.pop('loggedin',None)
    session.pop('username',None)
    session.pop('id',None)
    return redirect(url_for('login'))

@app.route("/register", methods = ['GET', 'POST'])
def register():
    msg3=''
    if request.method=='POST' and 'name' in request.form and 'userid' in request.form and 'password'in request.form:
        userid=request.form['userid']
        name=request.form['name']
        password=request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE userid = %s', (userid,))
        account1 = cursor.fetchone()
        if account1:
            msg3='Account already exists please login'
        else:
            cursor.execute("INSERT INTO accounts(password,name,userid) VALUES(%s,%s,%s)",(password,name,userid))
            mysql.connection.commit()
            #msg3 = list(logics.getpopular())
            msg3='You have registered, Please login '
            #return render_template('rate_movies.html',msg3=msg3)

    elif request.method=='POST':
        msg3='Please fill the form'
    else:
         return render_template('register.html',msg3=msg3)
     #when you have registered correctly and have list of random movies in msg
    return render_template('register.html',msg3=msg3)


@app.route("/recommend")
def recommend():
    if 'loggedin' in session:
        y=MovieImport.input(int(session['id']))
        return render_template('recommend.html',list=y)
    return render_template('login.html')

# function mapping for rate_movies also can be created then use url for instead of render template
@app.route("/rate_movies",methods=['GET','POST'])
def rate_movies():
    #confirm=''
    global list_of_random_movie_title
    dictionary=logics.getpopular()

    if request.method=='POST':
        print("in post")
        ratings=request.form.getlist('movies')
        print(ratings)
        list_of_random_movies=[]
        for movieid in dictionary:
            print("aaaaaaaaaaaaaaaa")
            list_of_random_movies.append(movieid)
        #logics.getDetails(ratings,session['id'])
        with open(r'demo.csv','a',newline='') as fd:
            writer = csv.writer(fd)
            print("aaaaaaa34444444444444444444444444444444444aaaaaaaaa")
            print(list_of_random_movies,ratings)

            for i,j in zip(list_of_random_movies,ratings):
                print("555555555555555555555555555555555555555555555555555555")
                if j=='0':
                    continue
                print(c,i,j,"1256677221")
                #myCsvRow=[c,i,j,"1256677221"]
                writer.writerow([c,i,j,"1256677221"])
                print("done")
                return render_template('rate_movies.html',list=list_of_random_movie_title,confirm="done")
            #return render_template('home.html')
    else:
        print("bbbbbbbbbbbbbbbb")
        list_of_random_movie_title=[]
        for movietitle in dictionary.values():
            list_of_random_movie_title.append(movietitle)

        return render_template('rate_movies.html',list=list_of_random_movie_title,confirm="")

if __name__=="__main__":
    app.run(debug=True)

  #y=MovieImport.input(int(session['id']))
            #return render_template('recommend.html',list=y)
