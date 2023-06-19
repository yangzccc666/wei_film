#coding:utf8
from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:root123@localhost/movie'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UP_DIR'] = r"E:\Programs\Python_projects\weifilm\app\static\uploads\\"
app.config['FC_DIR'] = r"E:\Programs\Python_projects\weifilm\app\static\uploads\users\\"
app.debug = True
app.config['SECRET_KEY'] = '123456*!@#'
db = SQLAlchemy(app)

from app.home import home as home_blueprint
from app.admin import admin as admin_blueprint

app.register_blueprint(home_blueprint)
app.register_blueprint(admin_blueprint,url_prefix="/admin")

@app.errorhandler(404)
def page_not_found(e):
    return render_template('home/404.html'),404
