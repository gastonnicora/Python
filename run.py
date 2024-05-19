import os
from app import create_app,  socketio
from os import environ
from dotenv import load_dotenv
import logging


env = environ.get("FLASK_ENV", "development")

load_dotenv()
app= create_app()

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
app.logger.addHandler(console_handler)

if __name__ == "__main__":
     
     
    # if env == "development":
    socketio.run(app,host="0.0.0.0",port=4000,debug=True,allow_unsafe_werkzeug=True)
    # else:
    #     socketio.run(app, host="0.0.0.0", port=4000)
