FROM python:3.9.19-alpine3.19

WORKDIR /app

COPY ./ .

RUN pip3 --no-cache-dir install -r ./requirements.txt
RUN pip3 --no-cache-dir install gunicorn

ENV FLASK_ENV=production
RUN --mount=type=secret,id=SECRET_KEY \
  --mount=type=secret,id=EMAIL \
  --mount=type=secret,id=MAIL_USERNAME \
  --mount=type=secret,id=MAIL_PASSWORD \
  export SECRET_KEY=$(cat /run/secrets/SECRET_KEY) && \
  export EMAIL=$(cat /run/secrets/EMAIL) && \
  export MAIL_USERNAME=$(cat /run/secrets/MAIL_USERNAME) && \
  export MAIL_PASSWORD=$(cat /run/secrets/MAIL_PASSWORD) && \
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:4000", "run:app"]
