from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
from os import path, environ
from config import config
from app import db_config
import os

from app.socket.socketio import socketio


from app.models.db import db
from app.resources import user
from app.resources import confirmEmail
from app.resources import company


def create_app(environment="development"):

    # Configuración inicial de la app
    app = Flask(__name__)
    app.jinja_env.line_statement_prefix = '#'
    app.config['CORS_HEADERS'] = 'Content-Type'
    cors = CORS(app)

    env = environ.get("FLASK_ENV", environment)
    app.config.from_object(config[env])
    socketio.init_app(app)
    app.config["SQLALCHEMY_DATABASE_URI"] = db_config.connection(app)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    with app.app_context():
        db.create_all()

    # Rutas API-REST
    app.add_url_rule("/users", "users", user.index)
    app.add_url_rule("/user/<string:uuid>", "user", user.get)
    app.add_url_rule("/userCreate", "userCreate",
                     user.create, methods=["POST"])
    app.add_url_rule("/userUpdate", "userUpdate", user.update, methods=["PUT"])
    app.add_url_rule("/userUpdatePassword", "userUpdatePassword",
                     user.updatePassword, methods=["PUT"])
    app.add_url_rule("/userDelete/<string:uuid>", "userDelete", user.delete)
    app.add_url_rule("/login", "login", user.login, methods=["POST"])
    app.add_url_rule("/logout", "logout", user.logout, methods=["GET"])

    app.add_url_rule("/get_confirmEmail/<string:uuid>",
                     "get_confirmEmail", confirmEmail.get)
    app.add_url_rule("/confirmEmail", "confirmEmails", confirmEmail.index)
    app.add_url_rule("/confirmEmail/<string:uuid>",
                     "confirmEmail", confirmEmail.confirm)
    

    app.add_url_rule("/companies", "companies", company.index)
    app.add_url_rule("/company/<string:uuid>", "company",
                     company.get)
    app.add_url_rule("/companyCreate", "companyCreate",
                     company.create, methods=["POST"])
    app.add_url_rule("/companyUpdate", "companyUpdate", company.update, methods=["PUT"])
    app.add_url_rule("/companyDelete/<string:uuid>", "companyDelete", company.delete)

    @app.route("/")
    def home():

        script_dir = os.path.dirname(__file__)
        rel_path = "endpoint.json"
        abs_file_path = os.path.join(script_dir, rel_path)

        currentFile = open(abs_file_path)
        data = json.load(currentFile)
        currentFile.close()
        return render_template("home.html", data=data)

    return app
