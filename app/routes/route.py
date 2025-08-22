from flask import Blueprint,render_template,session,redirect,jsonify,url_for
from flask_dance.contrib.github import github
from dotenv import load_dotenv
load_dotenv()

route=Blueprint('route',__name__)



@route.route("/")
def index():
    return render_template("index.html")
@route.route("/route-github",methods=["POST","GET"])
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))
    account_info=github.get("/user")
    if account_info.ok:
        account_info_json=account_info.json()
        print("Account Information : ",account_info_json)
        username=account_info_json['login']
        return f"<h1>Your Github User name {username}</h1><a href='/logout'>Logout</a>"
    else:
        return "<h1>Failed to fetch user info from Github.</h1><a href='/logout'>Logout</a>"
@route.route("/logout")
def logout():
    session.pop('github_oauth_token',None)
    return render_template("index.html")

@route.route("/github-login",methods=['POST','GET'])
def githubLogin():
    try:
        if not github.authorized:
            return jsonify({'status':False,'Message':'Git hub is not authorized'})
        user_info=github.get("/user")
        if user_info.ok:
            user_info_json=user_info.json()
            print("User Info : ",user_info_json)
            return jsonify({'status':True,'data':user_info_json})
        else:
            return jsonify({'status':False})
    except Exception as exception:
           print("Error while authenticating user ",exception)
           return jsonify({'status':False,'message':'Data is not retrieved failed :( authenticating user)'})


    