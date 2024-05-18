FROM python:3.9.19-alpine3.19

WORKDIR /app

COPY ./ . 

RUN pip3 --no-cache-dir install -r ./requirements.txt
RUN pip3 --no-cache-dir install gunicorn

# Establece las variables de entorno necesarias
ENV FLASK_ENV=production
# Configura Gunicorn con más tiempo de espera y un número adecuado de workers
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:4000", "--timeout", "120", "run:app"]
