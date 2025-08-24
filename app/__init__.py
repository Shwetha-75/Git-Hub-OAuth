from flask import Flask 
from flask_dance.contrib.github import make_github_blueprint,github 
from dotenv import load_dotenv
from app.routes.route import route    
import os
load_dotenv()

def createApp():
    app=Flask(__name__)
    app.secret_key=os.getenv("SECRET_KEY")
    github_blueprint=make_github_blueprint(
        client_id=os.getenv("CLIENT_ID"),
        client_secret=os.getenv("CLIENT_SECRET_KEY"),
        redirect_to="github_login"
    )
    app.register_blueprint(route)
    app.register_blueprint(github_blueprint,url_prefix="/login")
    return app
    