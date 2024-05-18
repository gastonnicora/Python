FROM python:3.9.19-alpine3.19

WORKDIR /app

COPY ./ . 

RUN pip3 --no-cache-dir install -r ./requirements.txt

# Configuración del entorno de Flask para desarrollo
ENV FLASK_ENV=development

# Comando para ejecutar la aplicación con Gunicorn en modo debug
CMD ["gunicorn", "-b", "0.0.0.0:4000", "run:app", "--reload", "--log-level", "debug"]
