FROM python:3.9.19-alpine3.19

WORKDIR /app

COPY ./ .

RUN pip3 --no-cache-dir install -r ./requirements.txt
RUN pip3 --no-cache-dir install gunicorn

# Copia el archivo de variables de entorno generado por GitHub Actions
COPY .env .env

ENV FLASK_ENV=production

CMD ["sh", "-c", "source .env && gunicorn -w 4 -b 0.0.0.0:4000 run:app"]
