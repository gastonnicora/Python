
from flask import current_app
from flask import g


def connection(app):

    with app.app_context():
        if "db_conn" not in g:
            conf = current_app.config
            host=conf["DB_HOST"]
            user=conf["DB_USER"]
            password=conf["DB_PASS"]
            db=conf["DB_NAME"]
            g.db_conn = "mysql+pymysql://{}:{}@{}/{}".format(user, password, host, db)

        return g.db_conn