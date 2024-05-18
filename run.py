from app import create_app, socketio
from os import environ
from app.helpers.sessions import Sessions

env = environ.get("FLASK_ENV", "development")

# Pasar los parámetros de conexión a Redis a la clase Sessions
redis_host = environ.get("REDIS_HOST", "localhost")
Sessions(redis_host=redis_host)

app = create_app()

if __name__ == "__main__":
    if env == "development":
        socketio.run(app, host="0.0.0.0", port=4000, debug=True, allow_unsafe_werkzeug=True)
    else:
        socketio.run(app, host="0.0.0.0", port=4000)
