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
            try:
                if env == "production":
                    cls._redis = redis.StrictRedis(host=redis_host, port=6379, db=0, decode_responses=True)
                else:
                    cls._redis = None  
                cls._load_from_redis()  
            except redis.RedisError as e:
                print(f"Error connecting to Redis: {e}")
                cls._redis = None  
            
            if cls._redis is None or not cls._load_from_redis():
                data = loadDict("Sessions.pkl")
                if data:
                    cls._sessions = data["sessions"]
                    cls._users = data["users"]
                    cls._companies = data["companies"]
        return cls._instance
    def addSession(cls, data):
        cls._load_from_redis()
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
        cls._load_from_redis()
        uuidS = cls._users.get(uuid, [])
        newSession = data
        for i in uuidS:
            newSession["login"] = cls._sessions[i]["login"]
            cls._sessions[i] = newSession
        cls._save()

    def getSession(cls, uuid):
        cls._load_from_redis()
        return cls._sessions.get(uuid)

    def getSessionsByUser(cls, uuid):
        cls._load_from_redis()
        uuidS = cls._users.get(uuid, [])
        sessions = [cls._sessions[i] for i in uuidS]
        return sessions

    def deleteSession(cls, uuid):
        cls._load_from_redis()
        session = cls._sessions.pop(uuid, None)
        if session:
            cls._users[session["uuid"]].remove(uuid)
            cls._save()

    def deleteSessionsByUser(cls, uuid):
        cls._load_from_redis()
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
        try:
            data = cls._redis.get('sessions_data')
            if data:
                loaded_data = pickle.loads(data)
                cls._sessions = loaded_data.get("sessions", {})
                cls._users = loaded_data.get("users", {})
                cls._companies = loaded_data.get("companies", {})
                return True
        except Exception as e:
            print(f"Error loading data from Redis: {e}")
        return False
    


    def _save(cls):
        data = cls.toDict()
        if cls._redis:
            try:
                cls._redis.set('sessions_data', pickle.dumps(data))
            except Exception as e:
                print(f"Error saving data to Redis: {e}")
        else:
            
            with open("Sessions.pkl", "wb") as file:
                pickle.dump(data, file)
