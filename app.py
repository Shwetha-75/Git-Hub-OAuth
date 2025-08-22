from flask import Flask, redirect, url_for, session,render_template
import os
from flask_dance.contrib.github import make_github_blueprint, github
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv('SECRET_KEY')

github_blueprint = make_github_blueprint(
    client_id=os.getenv('CLIENT_ID'),
    client_secret=os.getenv('CLIENT_SECRET_KEY')
)
app.register_blueprint(github_blueprint, url_prefix="/login")

@app.route("/")
def index():
    return render_template("index.html")
@app.route("/route-github",methods=['POST','GET'])
def login():
    if not github.authorized:
        return redirect(url_for("github.login"))

    account_info = github.get("/user")

    if account_info.ok:
        account_info_json = account_info.json()
        print("Account 'Information",account_info_json)
        username = account_info_json['login']
        return f"<h1>Your GitHub username is {username}</h1><a href='/logout'>Logout</a>"
    else:
        return "<h1>Failed to fetch user info from GitHub.</h1><a href='/logout'>Logout</a>"

@app.route("/logout")
def logout():
    session.pop('github_oauth_token', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, port=5001)