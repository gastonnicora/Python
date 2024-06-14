FROM python:3.9.19-alpine3.19

WORKDIR /app

COPY ./ . 

RUN pip3 --no-cache-dir install -r requirements.txt
RUN pip3 --no-cache-dir install gunicorn gevent redis

ENV FLASK_ENV=production
ENV REDIS_HOST=redis

CMD ["gunicorn", \
     "-k", "gevent", "-w", "1", "-b", "0.0.0.0:4000", \
     "--log-level", "debug", \
     "run:app", \
     "--access-logfile", "-", "--error-logfile", "-"]
