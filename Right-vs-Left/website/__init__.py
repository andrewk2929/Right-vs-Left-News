from flask import *
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

def configure():
    load_dotenv()

# db = SQLAlchemy()
# DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)

    configure()

    from .views import views

    app.register_blueprint(views, url_prefix="/view")

    # create database
    # create_database(app)

    # redirect user to home page
    @app.route('/')
    def redirect_home():
        return redirect(url_for("views.home"))

    return app