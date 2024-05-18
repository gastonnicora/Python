from app import create_app,  socketio
from os import environ


env = environ.get("FLASK_ENV", "development")

app= create_app()


if __name__ == "__main__":
    # if env == "development":
        socketio.run(app,host="0.0.0.0",port=4000,debug=True,allow_unsafe_werkzeug=True)
    # else:
    #     socketio.run(app, host="0.0.0.0", port=4000)
