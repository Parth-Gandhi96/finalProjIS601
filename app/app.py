from typing import List, Dict
import simplejson as json
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

from flask import Flask, request, Response, redirect
from flask import render_template,current_app, url_for
import urllib

import os
import re
import string
import random

from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

app = Flask(__name__)
cursor = None

def startApp():

    mysql = MySQL(cursorclass=DictCursor)

    app.config['MYSQL_DATABASE_HOST'] = 'db'
    app.config['MYSQL_DATABASE_USER'] = 'root'
    app.config['MYSQL_DATABASE_PASSWORD'] = ''
    # app.config['MYSQL_DATABASE_PORT'] = 3306
    app.config['MYSQL_DATABASE_DB'] = 'finalProjData'
    mysql.init_app(app)

    global cursor
    try:
        cursor = mysql.get_db().cursor()
    except Exception as e:
        print("Cursor init in APP didnt work correctly.")
        print(e)

@app.route('/', methods=['GET'])
def homePage():
    return render_template('signin.html',msg={'errorMsg':'None'})

@app.route('/', methods=['POST'])
def login():
    email = str(request.form.get("inputUsername"))
    password = str(request.form.get("inputPassword"))

    passInDB = fetchUserPassword(email)
    print("pass:"+str(passInDB)+" -- "+str(password)+"  bool :  "+str(str(passInDB)==str(password)))
    if (passInDB is not None and str(passInDB)==str(password)):
        return redirect("/homePage", code=302)
    return render_template('signin.html',msg={'errorMsg':'Wrong id and password, or User has not verified the email.'})

@app.route('/signup', methods=['GET'])
def signupPage():
    return render_template('signup.html',msg={'errorMsg':'None'})


@app.route('/signup', methods=['POST'])
def signup():
    email = str(request.form.get("inputUsername"))
    password = str(request.form.get("inputPassword"))
    confpassword = str(request.form.get("inputConfPassword"))

    if (password!=confpassword):
        return render_template("signup.html", msg={'errorMsg':'Passwords donot match.'})

    regex = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if (re.search(regex, email) == False):
        return render_template("signup.html", msg={'errorMsg':'Passwords Enter valid Email address.'})

    if (fetchUserPassword(email) is not None):
        return render_template("signup.html", msg={'errorMsg':'Entered Email is already Registered.'})

    verificationNewCode = getNewVerificationCode()
    urlToSend = os.environ.get('HOST_IP') + 'emailVerification/'+verificationNewCode
    sendEmail(email, 'Verify your account', '<strong> Please confirm you account by clicking this URL: '+urlToSend+' </strong>')

    addUserData(email, password, verificationNewCode)
    return redirect("/", code=302)

@app.route('/emailVerification/<verificationCode>',methods=['GET'])
def emailVerify(verificationCode):
    usersEmail = makeUserVerified(verificationCode)
    if (usersEmail is False):
        print('User is already verified OR using malfunctioned URL')
        return redirect("/", code=302)

    password = fetchUserPassword(usersEmail)
    if(password is None):
        print('Someerror in code, couldnt find user in user database!')
        return redirect("/", code=302)

    sendEmail(usersEmail, 'Registered', '<strong>You have successfully Verified your new account!</strong>')

    return redirect("/", code=302)



@app.route('/forgetpass', methods=['GET'])
def forgetPassPage():
    return render_template('forgetPassPage.html',msg={'errorMsg':'None'})

@app.route('/forgetpass', methods=['POST'])
def forgetPass():
    email = str(request.form.get("inputUsername"))

    regex = r'^(\w|\.|\_|\-)+[@](\w|\_|\-|\.)+[.]\w{2,3}$'
    if (re.search(regex, email) == False):
        return render_template('forgetPassPage.html', msg={'errorMsg': 'None'})

    if (fetchUserPassword(email) is None):
        return render_template("signup.html", msg={'errorMsg': 'Email is not Registered or Not verified yet.'})

    newCode = updateUserCode(email)
    print('code to send in email : '+newCode)
    urlToSend = os.environ.get('HOST_IP') + 'resetPass/'+newCode
    print('url sent in mail for reseting password : '+urlToSend)
    sendEmail(email, 'Reset Password', '<strong>Click Here to reset your password: '+urlToSend+'</strong>')

    return redirect("/", code=302)


@app.route('/resetPass/<code>', methods=['GET'])
def resetPassPage(code):
    print('code for reseting password '+str(code))
    if checkCode(code) is False:
        return redirect("/", code=302)
    return render_template('resetPassPage.html', msg={'errorMsg': 'None','code':str(code)})

@app.route('/resetPass', methods=['POST'])
def resetPass():
    code = str(request.form.get("userCode"))
    password = str(request.form.get("inputPassword"))
    confpassword = str(request.form.get("inputConfPassword"))

    print('code for reseting password'+str(code)+'   password:'+password)
    if (password!=confpassword):
        render_template('resetPassPage.html', msg={'errorMsg': 'Both password are not same','code':str(code)})

    email = updateUserPass(code,password)
    if(email is False):
        print('Wrong url using to reset the password, no email address associated with code is found!')
        return redirect('/', code=302)

    sendEmail(email, 'Password Changed', '<strong> Password successfully changed!</strong>')

    return redirect('/', code=302)

@app.route('/logout', methods=['GET'])
def logout():
    return redirect('/',code=302)


@app.route('/homePage', methods=['GET'])
def landingPage():
    return render_template('homePage.html',msg={'errorMsg':'None'})


@app.route('/top10Profited', methods=['GET'])
def top10Profited():
    movieData = fetchTop10Profited();
    movieNames = []
    movieCollections = []
    movieBudgets = []
    movieProfit = []

    for x in movieData:
        movieNames.append(x['film_title'])
        movieCollections.append(x['worldwide_gross'])
        movieBudgets.append(x['film_budget'])
        movieProfit.append(x['profit'])

    data1 = {
            'x': movieNames,
            'y': movieProfit,
            'type': 'bar',
            'name': 'Profit in %',
            'marker': {
                'color': 'rgb(49,130,189)',
                'opacity': 0.7
            }
        };
    return render_template('chart.html', data1=data1,plot_title='Top 10 profited films amongst Top grossing movies')


@app.route('/top10ProfitedJSON', methods=['GET'])
def top10ProfitedJSON():
    movieData = fetchTop10Profited();
    json_result = json.dumps(movieData);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/avgProfitImdbWise', methods=['GET'])
def avgProfitImdbWise():
    movieData = fetchAvgProfitImdbWise();
    range = []
    avgProfit = []

    for x in movieData:
        range.append(str(x['a'])+"-"+str(x['b']))
        avgProfit.append(x['avg_profit'])

    data1 = {
            'x': range,
            'y': avgProfit,
            'type': 'bar',
            'name': 'Avg Profit in %',
            'marker': {
                'color': 'rgb(49,130,189)',
                'opacity': 0.7
            }
        };
    return render_template('chart.html', data1=data1,plot_title='IMDB Range wise Avg profit in Highest grossing movies')

@app.route('/avgProfitImdbWiseJSON', methods=['GET'])
def avgProfitImdbWiseJSON():
    movieData = fetchAvgProfitImdbWise();
    json_result = json.dumps(movieData);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/avgProfitGenreWise', methods=['GET'])
def avgProfitGenreWise():
    movieData = fetchAvgProfitGenreWise();
    genre = []
    count = []
    avgProfit = []

    for x in movieData:
        genre.append(x['genre'])
        count.append(x['count'])
        avgProfit.append(x['avg_profit'])

    data1 = {
            'x': genre,
            'y': avgProfit,
            'type': 'bar',
            'name': 'Avg Profit in %',
            'marker': {
                'color': 'rgb(49,130,189)',
                'opacity': 0.7
            }
        };
    data2 = {
        'x': genre,
        'y': count,
        'type': 'bar',
        'name': 'count of Movies',
        'marker': {
            'color': 'rgb(204,204,204)',
            'opacity': 0.5
        }
    }
    return render_template('chart.html', data1=data1,data2=data2,
                           plot_title='Genre wise Avg profit  in Highest grossing movies',
                           plot_title_2='Genre wise Count of movies in Highest grossing movies')

@app.route('/avgProfitGenreWiseJSON', methods=['GET'])
def avgProfitGenreWiseJSON():
    movieData = fetchAvgProfitGenreWise();
    json_result = json.dumps(movieData);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

@app.route('/last5yearCharts', methods=['GET'])
def last5yearCharts():
    movieData = fetchMovieCollectionLast5Years();
    movieNames = []
    movieCollections = []
    movieBudgets = []

    for x in movieData:
        movieNames.append(x['film_title'])
        movieCollections.append(x['worldwide_gross'])
        movieBudgets.append(x['film_budget'])

    data1 = {
            'x': movieNames,
            'y': movieCollections,
            'type': 'bar',
            'name': 'Collection',
            'marker': {
                'color': 'rgb(49,130,189)',
                'opacity': 0.7
            }
        };
    data2 = {
            'x': movieNames,
            'y': movieBudgets,
            'type': 'bar',
            'name': 'Budget',
            'marker': {
                'color': 'rgb(204,204,204)',
                'opacity': 0.5
            }
        }
    return render_template('chart2.html', data1=data1,data2=data2,plot_title='Top grossing Movies released in last 5 years, with their budget and collections')

@app.route('/last5yearChartsJSON', methods=['GET'])
def last5yearChartsJSON():
    movieData = fetchMovieCollectionLast5Years();
    json_result = json.dumps(movieData);
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp

## Movie Database operations:
def fetchMovieCollectionLast5Years():
    inputData = (2016)
    select_query = """SELECT t.film_title, t.worldwide_gross, t.film_budget FROM movieData t WHERE t.release_year > %s """
    cursor.execute(select_query, inputData)
    fetchedData = cursor.fetchall()
    movieData = json.loads(json.dumps(fetchedData))
    # print("movie Data: \n"+str(movieData))
    return movieData

def fetchTop10Profited():
    select_query = """select t.film_title,t.worldwide_gross,t.film_budget,(t.worldwide_gross-t.film_budget)*100/t.film_budget as profit
from movieData t order by profit desc limit 10"""
    cursor.execute(select_query)
    fetchedData = cursor.fetchall()
    movieData = json.loads(json.dumps(fetchedData))
    # print("fetchTop10Profited: \n"+str(movieData))
    return movieData

def fetchAvgProfitImdbWise():
    select_query = """select (t.imdb)-1 as a,(t.imdb) as b, avg((t.worldwide_gross-t.film_budget)*100/t.film_budget) as avg_profit
                    from (select *,ceil(imdb_rating) as imdb from movieData) t group by t.imdb"""
    cursor.execute(select_query)
    fetchedData = cursor.fetchall()
    movieData = json.loads(json.dumps(fetchedData))
    # print("fetchTop10Profited: \n"+str(movieData))
    return movieData

def fetchAvgProfitGenreWise():
    select_query = """select (t.genre_1) as genre, count(*) as count, 
                    round(avg((t.worldwide_gross-t.film_budget)*100/t.film_budget)) as avg_profit
                    from movieData t group by t.genre_1"""
    cursor.execute(select_query)
    fetchedData = cursor.fetchall()
    movieData = json.loads(json.dumps(fetchedData))
    # print("fetchTop10Profited: \n"+str(movieData))
    return movieData


## User Database operations:
def getAllUserData() -> str:
    cursor.execute('SELECT * FROM userTable')
    result = cursor.fetchall()
    return result

def fetchUserPassword(email):
    # Code for fetching data from Users table from DB and returning in Directory format (JSON)

    inputData = (email)
    select_query = """SELECT * FROM userTable t WHERE t.email = %s """
    cursor.execute(select_query, inputData)
    fetchedData = cursor.fetchall()

    if fetchedData is None or len(json.loads(json.dumps(fetchedData)))==0:
        return None

    userInfo = json.loads(json.dumps(fetchedData))[0]
    # not verified user:
    if str(userInfo['verificationCode'])!='':
        return None

    return str(userInfo['pass'])

def addUserData(email,password,verificationNewCode):
    # userData[email] = {'pass':password,'code':'','verificationCode':verificationNewCode}

    # Code for adding new user in Users table
    inputData = (email, password,'', verificationNewCode)
    sql_insert_query = """INSERT INTO userTable (email,pass,code,verificationCode) VALUES (%s, %s, %s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return True

def updateUserPass(code,password):
    # Code for updating users info in Users table, make sure to change the code to ''

    inputData = (code)
    select_query = """SELECT * FROM userTable t WHERE t.code = %s """
    cursor.execute(select_query,inputData)
    emailResult = cursor.fetchall()
    userInfo = json.loads(json.dumps(emailResult))[0]

    if userInfo is None:
        return False
    print("userInfo:"+str(userInfo))

    inputData = ( password,'', '',code)
    sql_update_query = """UPDATE userTable t SET t.pass = %s, t.code = %s, t.verificationCode = %s WHERE t.code = %s """
    cursor.execute(sql_update_query, inputData)
    try:
        mysql.get_db().commit()
        return userInfo['email']
    except:
        return False

def updateUserCode(email):
    newCode = getNewCode()
    # update in DB for that user, in code column
    # userData[email]['code'] = newCode
    inputData = (newCode,email)
    sql_update_query = """UPDATE userTable t SET t.code = %s WHERE t.email = %s """
    cursor.execute(sql_update_query, inputData)
    try:
        mysql.get_db().commit()
        return newCode
    except:
        return False

def makeUserVerified(verificationCode):

    inputData = (verificationCode)
    select_query = """SELECT * FROM userTable t WHERE t.verificationCode = %s """
    cursor.execute(select_query, inputData)
    emailResult = cursor.fetchall()
    userInfo = json.loads(json.dumps(emailResult))[0]

    if userInfo is None:
        return False
    print("userInfo:" + str(userInfo))

    inputData = ('',userInfo['email'])
    sql_update_query = """UPDATE userTable t SET t.verificationCode = %s WHERE t.email = %s """
    cursor.execute(sql_update_query, inputData)
    try:
        mysql.get_db().commit()
        return userInfo['email']
    except:
        return False


def getNewCode():
    # fetch all the code from DB of userData and store in codeMap
    codeSet = set()

    userData = json.loads(json.dumps(getAllUserData()));
    for x in userData:
        codeSet.add(x['code'])

    letters = string.ascii_lowercase + string.digits
    temp = ''.join(random.choice(letters) for i in range(10))
    while(temp in codeSet):
        temp = ''.join(random.choice(letters) for i in range(10))
    return temp

def getNewVerificationCode():
    # fetch all the code from DB of userData and store in codeMap
    codeSet = set()

    userData = json.loads(json.dumps(getAllUserData()));
    for x in userData:
        codeSet.add(x['verificationCode'])

    letters = string.ascii_lowercase + string.digits
    temp = ''.join(random.choice(letters) for i in range(10))
    while(temp in codeSet):
        temp = ''.join(random.choice(letters) for i in range(10))
    return temp

def checkCode(code):
    # fetch all the code from DB of userData and store in codeMap
    codeSet = set()

    userData = json.loads(json.dumps(getAllUserData()));
    for x in userData:
        codeSet.add(x['code'])

    if code not in codeSet:
        return False
    return True

@app.route('/sendtempemail', methods=['GET'])
def getUsersList():
    sendEmail('neo.anderson449@gmail.com','Temp email','<strong>Its fun to send an email, right!</strong>')
    return "done"

def sendEmail(to_email,subject_email,content_email):
    message = Mail(
        from_email=os.environ.get('SENDER_EMAIL_ADDRESS'),
        to_emails=to_email,
        subject=subject_email,
        html_content=content_email)
    try:
        sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
        response = sg.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(e)

if __name__ == '__main__':
    startApp()
    app.run(host='0.0.0.0')