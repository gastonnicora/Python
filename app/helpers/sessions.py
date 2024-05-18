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
            env = os.getenv("FLASK_ENV", "development")
            if env == "production":
                cls._redis = redis.StrictRedis(host='redis', port=6379, db=0)
                data = cls._load_from_redis()
            else:
                data = loadDict("Sessions.pkl")
            if data:
                cls._sessions = data["sessions"]
                cls._users = data["users"]
                cls._companies = data["companies"]
        return cls._instance

    def __init__(cls):
        cls.variable = "Soy un Singleton"

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
        if cls._users.get(data["uuid"]) and len(cls._users[data["uuid"]]) != 0:
            cls._users[data["uuid"]].append(id)
        else:
            cls._users[data["uuid"]] = [id]

    def _addCompany(cls, id, data):
        if cls._companies.get(data.get("company")) and cls._companies.get(data["company"].get("uuid")) and len(data["company"].get("uuid")) != 0:
            cls._companies[data["company"]["uuid"]].append(id)
        else:
            cls._companies[data["company"]["uuid"]] = [id]

    def updateSession(cls, uuid, data):
        session = cls.getSession(uuid)
        newSession = data
        newSession["login"] = session["login"]
        cls._sessions[uuid] = newSession
        cls._save()

    def updateSessionByUser(cls, uuid, data):
        uuidS = cls._users[uuid]
        newSession = data
        for i in uuidS:
            newSession["login"] = cls._sessions[i]["login"]
            cls._sessions[i] = newSession
        cls._save()

    def getSession(cls, uuid):
        return cls._sessions[uuid]

    def getSessionsByUser(cls, uuid):
        uuidS = cls._users[uuid]
        sessions = []
        for i in uuidS:
            sessions.append(cls._sessions[i])
        return sessions

    def deleteSession(cls, uuid):
        session = cls._sessions.pop(uuid)
        cls._users[session["uuid"]].remove(uuid)
        cls._save()

    def deleteSessionsByUser(cls, uuid):
        uuidS = cls._users[uuid]
        for i in uuidS:
            cls._sessions.pop(i)
        cls._users[uuid] = []
        cls._save()

    def toDict(cls):
        dict = {}
        dict["sessions"] = cls._sessions
        dict["users"] = cls._users
        dict["companies"] = cls._companies
        return dict

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
