import uuid
import datetime
import redis
import json
from app.helpers.saveSession import loadDict

class Sessions:
    _instance = None

    def __new__(cls, redis_host='localhost', redis_port=6379):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._redis = redis.StrictRedis(host=redis_host, port=redis_port, decode_responses=True)
            # Cargar datos iniciales si existen
            cls._load_initial_data()
        return cls._instance

    def __init__(cls):
        cls.variable = "Soy un Singleton"
    
    @classmethod
    def _load_initial_data(cls):
        data = cls._redis.get("SessionsData")
        if data:
            data = json.loads(data)
            cls._sessions = data.get("sessions", {})
            cls._users = data.get("users", {})
            cls._companies = data.get("companies", {})
        else:
            cls._sessions = {}
            cls._users = {}
            cls._companies = {}

    def _save_to_redis(cls):
        data = {
            "sessions": cls._sessions,
            "users": cls._users,
            "companies": cls._companies
        }
        cls._redis.set("SessionsData", json.dumps(data))
    
    def addSession(cls, data):
        id = str(uuid.uuid4())
        session = cls._dataSession(id, data)
        cls._addUser(id, data)
        cls._save_to_redis()
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
        if data["uuid"] in cls._users and cls._users[data["uuid"]]:
            cls._users[data["uuid"]].append(id)
        else:
            cls._users[data["uuid"]] = [id]
        cls._save_to_redis()

    def updateSession(cls, uuid, data):
        session = cls.getSession(uuid)
        newSession = data
        newSession["login"] = session["login"]
        cls._sessions[uuid] = newSession
        cls._save_to_redis()

    def updateSessionByUser(cls, uuid, data):
        uuidS = cls._users.get(uuid, [])
        newSession = data
        for i in uuidS:
            newSession["login"] = cls._sessions[i]["login"]
            cls._sessions[i] = newSession
        cls._save_to_redis()

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
        cls._save_to_redis()

    def deleteSessionsByUser(cls, uuid):
        uuidS = cls._users.get(uuid, [])
        for i in uuidS:
            cls._sessions.pop(i, None)
        cls._users[uuid] = []
        cls._save_to_redis()

    def toDict(cls):
        return {
            "sessions": cls._sessions,
            "users": cls._users,
            "companies": cls._companies
        }

