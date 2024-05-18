FROM  python:3.9.19-alpine3.19


WORKDIR /app

COPY ./ . 

RUN pip3 install -r ./requirements.txt
ENV FLASK_ENV=production
CMD ["python3","run.py"]