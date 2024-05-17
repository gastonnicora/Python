from app import create_app,  socketio

app= create_app()


if __name__ == "__main__":
    socketio.run(app,host="0.0.0.0",port=4000,debug=True,allow_unsafe_werkzeug=True, cors_allowed_origins="*")
    