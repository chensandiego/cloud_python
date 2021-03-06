from flask import Flask, render_template, request, jsonify, redirect, session
from flask import jsonify,abort
import json
import sqlite3
from flask_cors import CORS,cross_origin


app = Flask(__name__)
app.config.from_object(__name__)
app.secret_key = 'F12Zr47j\3yX R~X@H!jmM]Lwf/,?KT'
CORS(app)

@app.route('/')
def main():
    return render_template('main.html')





@app.route('/addname')
def addname():
    if request.args.get('yourname'):
        session['name']=request.args.get('yourname')
        return redirect(url_for('main'))
    else:
        return render_template('addname.html',session=session)

@app.route('/clear')
def clearsession():
    session.clear()
    return redirect(url_for('main'))

@app.route("/api/v1/info")
def home_index():
    conn = sqlite3.connect("mydb.db")
    print ("Opened db successfully")
    api_list=[]
    cursor=conn.execute("select buildtime,version,methods,links from apirelease")

    for row in cursor:
        a_dict={}
        a_dict['version']=row[0]
        a_dict['buildtime']=row[1]
        a_dict['methods']=row[2]
        a_dict['links']=row[3]
        api_list.append(a_dict)
    conn.close()
    return jsonify({'api_version':api_list}), 200

@app.route('/adduser')
def adduser():
    return render_template('adduser.html')

@app.route('/addtweets')
def addtweetjs():
    return render_template('addtweets.html')

@app.errorhandler(404)
def resource_not_found(error):
    return make_response(jsonify({'error':'Resource not found'}),404)

@app.errorhandler(400)
def invalid_request(error):
    return make_response(jsonify({'error':'Bad Request'}),400)


@app.route('/api/v1/users/<int:user_id>',methods=['GET'])
def get_user(user_id):
    return list_user(user_id)



@app.route('/api/v1/users',methods=['GET'])
def get_users():
    return list_users()


@app.route('/api/v1/users',methods=['POST'])
def create_user():
    if not request.json or not 'username' in request.json or not 'email' in request.json or not 'password' in request.json:
        abort(400)
    else:
        user={
            'username':request.json['username'],
            'email': request.json['email'],
            'name':request.json.get('name',""),
            'password':request.json['password']

        }
        return jsonify({'status':add_user(user)}),201



def list_users():
    conn = sqlite3.connect('mydb.db')
    print("open db successfully")
    api_list=[]
    cursor=conn.execute("select username,full_name,emailid,password,id from users")

    for row in cursor:
        a_dict={}
        a_dict['username']=row[0]
        a_dict['full_name']=row[1]
        a_dict['emailid']=row[2]
        a_dict['password']=row[3]
        a_dict['id']=row[4]
        api_list.append(a_dict)
    conn.close()
    return jsonify({'user_list':api_list}), 200


def list_user(user_id):
    conn=sqlite3.connect('mydb.db')
    print("open db")

    api_list=[]
    cursor=conn.execute("select * from users where id=?",(user_id,))
    data=cursor.fetchall()
    if len(data) !=0:
        user={}
        user['username']=data[0][0]
        user['full_name']=data[0][1]
        user['emailid']=data[0][2]
        user['password']=data[0][3]
        user['id']=data[0][4]
        api_list.append(user)
    conn.close()
    return jsonify({'user':api_list}), 200


def add_user(new_user):
    conn=sqlite3.connect('mydb.db')
    print("open db")
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("select * from users where username=? or emailid=?",(new_user['username'],new_user['email']))
    data = cursor.fetchall()
    if len(data) !=0:
        abort(409)
    else:
        cursor.execute("insert into users (username,emailid,password,full_name) values(?,?,?,?)",(new_user['username'],new_user['email'],new_user['password'],new_user['name']))
        conn.commit()
        return "success"
    conn.close()
    return jsonify(a_dict)



@app.route('/api/v2/tweets', methods=['GET'])
def get_tweets():
    return list_tweets()

@app.route('/api/v2/tweets', methods=['POST'])
def add_tweets():

    user_tweet = {}
    if not request.json or not 'username' in request.json or not 'body' in request.json:
        abort(400)
    user_tweet['username'] = request.json['username']
    user_tweet['body'] = request.json['body']
    user_tweet['created_at']=strftime("%Y-%m-%dT%H:%M:%SZ", gmtime())
    print (user_tweet)
    return  jsonify({'status': add_tweet(user_tweet)}), 201

@app.route('/api/v2/tweets/<int:id>', methods=['GET'])
def get_tweet(id):
    return list_tweet(id)









def list_tweets():
    conn = sqlite3.connect('mydb.db')
    print ("Opened database successfully");
    api_list=[]
    cursor=conn.cursor()
    cursor.execute("SELECT username, body, tweet_time, id from tweets")
    data = cursor.fetchall()
    print (data)
    print (len(data))
    if len(data) == 0:
        return api_list
    else:
        for row in data:
            tweets = {}

            tweets['tweetedby'] = row[0]
            tweets['body'] = row[1]
            tweets['timestamp'] = row[2]
            tweets['id'] = row[3]

            print (tweets)
            api_list.append(tweets)

    conn.close()
    print (api_list)
    return jsonify({'tweets_list': api_list})

if __name__=="__main__":
    app.run(host='127.0.0.1',port=5000,debug=True)
