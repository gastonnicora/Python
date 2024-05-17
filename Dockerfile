FROM  python:3.8.16-alpine3.18


WORKDIR /app

COPY ./ . 

RUN pip3 --no-cache-dir install -r ./requirements.txt
ENV FLASK_ENV=production
CMD ["python3","run.py"]