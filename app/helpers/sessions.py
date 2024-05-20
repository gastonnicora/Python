import uuid
import datetime
import os
import pickle
import redis
from app.helpers.saveSession import loadDict

class Sessions:
    _instance = None
    _sessions = {}
    _users = {}
    _companies = {}
    _redis = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            env = os.environ.get("FLASK_ENV", "development")
            redis_host = os.environ.get("REDIS_HOST", "localhost")
            if env == "production":
                cls._redis = redis.StrictRedis(host=redis_host, port=6379, db=0)
                data = cls._load_from_redis()
            else:
                data = loadDict("Sessions.pkl")
            if data:
                cls._sessions = data["sessions"]
                cls._users = data["users"]
                cls._companies = data["companies"]
        return cls._instance

    def addSession(cls, data):
        id = str(uuid.uuid4())
        session = cls._dataSession(id, data)
        cls._addUser(id, data)
        cls._save()
        return id, session

    def _dataSession(cls, id, data):
        session = data
        date_format = '%d/%m/%Y %H:%M:%S%z'
        date = datetime.datetime.now()
        strDate = date.strftime(date_format)
        session["login"] = strDate
        cls._sessions[id] = session
        return session

    def _addUser(cls, id, data):
        user_uuid = data["uuid"]
        if cls._users.get(user_uuid):
            cls._users[user_uuid].append(id)
        else:
            cls._users[user_uuid] = [id]

    def _addCompany(cls, id, data):
        company_uuid = data.get("company", {}).get("uuid")
        if company_uuid:
            if cls._companies.get(company_uuid):
                cls._companies[company_uuid].append(id)
            else:
                cls._companies[company_uuid] = [id]

    def updateSession(cls, uuid, data):
        session = cls.getSession(uuid)
        newSession = data
        newSession["login"] = session["login"]
        cls._sessions[uuid] = newSession
        cls._save()

    def updateSessionByUser(cls, uuid, data):
        uuidS = cls._users.get(uuid, [])
        newSession = data
        for i in uuidS:
            newSession["login"] = cls._sessions[i]["login"]
            cls._sessions[i] = newSession
        cls._save()

    def getSession(cls, uuid):
        return cls._sessions.get(uuid)

    def getSessionsByUser(cls, uuid):
        uuidS = cls._users.get(uuid, [])
        sessions = [cls._sessions[i] for i in uuidS]
        return sessions

    def deleteSession(cls, uuid):
        session = cls._sessions.pop(uuid, None)
        if session:
            cls._users[session["uuid"]].remove(uuid)
            cls._save()

    def deleteSessionsByUser(cls, uuid):
        uuidS = cls._users.get(uuid, [])
        for i in uuidS:
            cls._sessions.pop(i, None)
        cls._users[uuid] = []
        cls._save()

    def toDict(cls):
        return {
            "sessions": cls._sessions,
            "users": cls._users,
            "companies": cls._companies
        }

    def _load_from_redis(cls):
        data = cls._redis.get('sessions_data')
        if data:
            return pickle.loads(data)
        return None

    def _save_to_redis(cls):
        data = cls.toDict()
        cls._redis.set('sessions_data', pickle.dumps(data))

    def _save(cls):
        if cls._redis:
            cls._save_to_redis()
        else:
            data = cls.toDict()
            with open("Sessions.pkl", "wb") as file:
                pickle.dump(data, file)
