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
from app.resources import employee
from app.resources import role


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

    # CRUD User
    app.add_url_rule("/users", "users", user.index)
    app.add_url_rule("/user/<string:uuid>", "user", user.get)
    app.add_url_rule("/userCreate", "userCreate",
                     user.create, methods=["POST"])
    app.add_url_rule("/userUpdate", "userUpdate", user.update, methods=["PUT"])
    app.add_url_rule("/userUpdatePassword", "userUpdatePassword",
                     user.updatePassword, methods=["PUT"])
    app.add_url_rule("/userDelete/<string:uuid>", "userDelete", user.delete, methods=["DELETE"])
    app.add_url_rule("/login", "login", user.login, methods=["POST"])
    app.add_url_rule("/logout", "logout", user.logout, methods=["GET"])


    # ConfirmUSer
    app.add_url_rule("/get_confirmEmail/<string:uuid>",
                     "get_confirmEmail", confirmEmail.get)
    app.add_url_rule("/confirmEmail", "confirmEmails", confirmEmail.index)
    app.add_url_rule("/confirmEmail/<string:uuid>",
                     "confirmEmail", confirmEmail.confirm)
    
    #CRUD Company
    app.add_url_rule("/companies", "companies", company.index)
    app.add_url_rule("/company/<string:uuid>", "company",
                     company.get)
    app.add_url_rule("/companyCreate", "companyCreate",
                     company.create, methods=["POST"])
    app.add_url_rule("/companyUpdate", "companyUpdate", company.update, methods=["PUT"])
    app.add_url_rule("/companyDelete/<string:uuid>", "companyDelete", company.delete, methods=["DELETE"])

    #CRUD Employee
    app.add_url_rule("/employees", "employees", employee.index)
    app.add_url_rule("/employee/<string:uuid>", "employee",
                     employee.get)
    app.add_url_rule("/employeeByUser/<string:uuid>", "employeeByUser",
                     employee.getByUser)
    app.add_url_rule("/employeeByCompany/<string:uuid>", "employeeByCompany",
                     employee.getByCompany)
    app.add_url_rule("/employeeCreate", "employeeCreate",
                     employee.create, methods=["POST"])
    app.add_url_rule("/employeeUpdate", "employeeUpdate", employee.update, methods=["PUT"])
    app.add_url_rule("/employeeDelete/<string:uuid>", "employeeDelete", employee.delete, methods=["DELETE"])
    app.add_url_rule("/employeeDeleteByUser/<string:uuid>", "employeeDeleteByUser", employee.delete, methods=["DELETE"])
    app.add_url_rule("/employeeDeleteByCompany/<string:uuid>", "employeeDeleteByCompany", employee.delete, methods=["DELETE"])

    #CRUD Role
    app.add_url_rule("/roles", "roles", role.index)
    app.add_url_rule("/role/<string:uuid>", "role",
                     role.get)
    app.add_url_rule("/roleCreate", "roleCreate",
                     role.create, methods=["POST"])
    app.add_url_rule("/roleUpdate", "roleUpdate", role.update, methods=["PUT"])
    app.add_url_rule("/roleDelete/<string:uuid>", "roleDelete", role.delete, methods=["DELETE"])

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
