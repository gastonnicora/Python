import os
from app import create_app,  socketio
from os import environ
from dotenv import load_dotenv
import logging

from logging.handlers import RotatingFileHandler
from flask import  send_file


env = environ.get("FLASK_ENV", "development")

load_dotenv()
app= create_app()

# Configuración del manejador de registros para escribir en un archivo
file_handler = RotatingFileHandler('app.log', maxBytes=1024 * 1024 * 10, backupCount=10)
file_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
file_handler.setLevel(logging.DEBUG)  # Establecer el nivel de registro al más bajo

# Añadir el manejador al logger de la aplicación
if not app.logger.handlers:
    app.logger.addHandler(file_handler)

# Asegurarse de que el logger principal también esté en el nivel correcto
app.logger.setLevel(logging.DEBUG)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
app.logger.addHandler(console_handler)
@app.route('/logs')
def serve_logs():
    app.logger.debug('Esta es una mensaje de depuración.')
    app.logger.info('Esta es una mensaje de información.')
    app.logger.warning('Esta es una advertencia.')
    app.logger.error('Este es un error.')
    app.logger.critical('Este es un mensaje crítico.')
    log_file_path = os.getcwd() + '/app.log'  # Ruta al archivo de registro
    return send_file(log_file_path, mimetype='text/plain')

if __name__ == "__main__":
     
     
    # if env == "development":
    socketio.run(app,host="0.0.0.0",port=4000,debug=True,allow_unsafe_werkzeug=True)
    # else:
    #     socketio.run(app, host="0.0.0.0", port=4000)
