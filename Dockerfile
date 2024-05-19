FROM python:3.9.19-alpine3.19

WORKDIR /app

COPY ./ . 

RUN pip3 --no-cache-dir install -r ./requirements.txt
RUN pip3 --no-cache-dir install gunicorn gevent

ENV FLASK_ENV=production
ENV CELERY=celery
ENV REDIS_HOST=redis

CMD ["gunicorn", \
     "-k", "gevent", "-w", "4", "-b", "0.0.0.0:4000", \
     "run:app", \
     "--access-logfile", "-", "--error-logfile", "-"]
