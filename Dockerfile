FROM python:3.9.19-alpine3.19

WORKDIR /app

COPY ./ . 

RUN pip3 --no-cache-dir install -r requirements.txt
RUN pip3 --no-cache-dir install gunicorn eventlet

ENV FLASK_ENV=production
ENV REDIS_HOST=redis
CMD ["gunicorn", "-b", \
     "0.0.0.0:4000", "-w", "4",\
      "-k", "eventlet", "--worker-class", "eventlet",\
       "--worker-connections", "1000", \
       "--log-level", "debug", \
       "run:app", \
       "--access-logfile", "-", "--error-logfile", "-"]


