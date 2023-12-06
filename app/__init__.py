from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
import json
from os import  path,environ
from config import config
from app import db_config
import os

from app.socket.socketio import socketio


from app.models.db import  db


def create_app(environment="development"):

    from app.resources import user
    from app.resources import confirmEmail

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
    app.add_url_rule("/createUser","createUser",user.create,methods=["POST"])
    # app.add_url_rule("/user_editar","user_put",user.update,methods=["POST"])
    # app.add_url_rule("/user_editar_pass","user_put_pass",user.update_pass,methods=["POST"])
    # app.add_url_rule("/user_borrar/<int:id>", "user_delete", user.delete)
    # app.add_url_rule("/user/alumnos/<int:id>", "user_get_alumnos", user.get_alumnos)
    # app.add_url_rule("/user/Alumnos/<int:id>", "user_alumnos", user.alumnos) #falta
    app.add_url_rule("/login","login",user.login,methods=["POST"])

    app.add_url_rule("/get_confirmEmail/<string:uuid>","get_confirmEmail",confirmEmail.get)
    app.add_url_rule("/confirmEmail","confirmEmails",confirmEmail.index)
    app.add_url_rule("/confirmEmail/<string:uuid>","confirmEmail",confirmEmail.confirm)

    

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


