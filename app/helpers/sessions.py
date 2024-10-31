import uuid
import datetime
import pickle
from app.connections.redis import redis_client, acquire_lock, release_lock

class Sessions:
    _instance = None
    _sessions = {}
    _users = {}
    _companies = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._load()
        return cls._instance

    @classmethod
    def addSession(cls, data):
        id = str(uuid.uuid4())
        session = cls._dataSession(id, data)
        cls._addUser(id, data)
        return id, session

    @classmethod
    def _dataSession(cls, id, data):
        session = data.copy()
        date_format = '%d/%m/%Y %H:%M:%S%z'
        date = datetime.datetime.now()
        strDate = date.strftime(date_format)
        session["login"] = strDate
        cls._sessions[id] = session
        return session

    @classmethod
    def _addUser(cls, id, data):
        user_uuid = data["uuid"]
        if acquire_lock(user_uuid):
            try:
                cls._load()
                cls._users.setdefault(user_uuid, []).append(id)
                cls._save_to_redis()
            finally:
                release_lock(user_uuid)

    @classmethod
    def _addCompany(cls, id, data):
        company_uuid = data.get("company", {}).get("uuid")
        if company_uuid:
            if acquire_lock(company_uuid):
                try:
                    cls._load()
                    cls._companies.setdefault(company_uuid, []).append(id)
                    cls._save_to_redis()
                finally:
                    release_lock(company_uuid)

    @classmethod
    def updateSession(cls, uuid, data):
        if acquire_lock(uuid):
            try:
                cls._load()
                session = cls.getSession(uuid)
                newSession = data
                newSession["login"] = session["login"]
                cls._sessions[uuid] = newSession
                cls._save_to_redis()
            finally:
                release_lock(uuid)

    @classmethod
    def updateSessionByUser(cls, uuid, data):
        if acquire_lock(uuid):
            try:
                uuidS = cls._users.get(uuid, [])
                newSession = data
                for i in uuidS:
                    cls.updateSession(i, newSession)
            finally:
                release_lock(uuid)

    @classmethod
    def getSession(cls, uuid):
        session = None
        print("uuid "+uuid)
        if acquire_lock(uuid):
            try:
                cls._load()
                session = cls._sessions.get(uuid)
                print("session "+str(session))
            finally:
                release_lock(uuid)
        return session

    @classmethod
    def getSessionsByUser(cls, uuid):
        sessions = None
        if acquire_lock(uuid):
            try:
                cls._load()
                uuidS = cls._users.get(uuid, [])
                sessions = [cls.getSession(i) for i in uuidS]
            finally:
                release_lock(uuid)
        return sessions

    @classmethod
    def deleteSession(cls, uuid):
        if acquire_lock(uuid):
            try:
                cls._load()
                session = cls._sessions.pop(uuid, None)
                if session:
                    cls._users[session["uuid"]].remove(uuid)
                    cls._save_to_redis()
            finally:
                release_lock(uuid)

    @classmethod
    def deleteSessionsByUser(cls, uuid):
        if acquire_lock(uuid):
            try:
                cls._load()
                uuidS = cls._users.get(uuid, [])
                for i in uuidS:
                    cls.deleteSession(i)
                cls._save_to_redis()
            finally:
                release_lock(uuid)

    @classmethod
    def toDict(cls):
        return {
            "sessions": cls._sessions,
            "users": cls._users,
            "companies": cls._companies
        }

    @classmethod
    def _load_from_redis(cls):
        try:
            data = redis_client.get('sessions_data')
            if data:
                return pickle.loads(data)
        except Exception as e:
            print(f"Error al cargar desde Redis: {e}")
        return None


    @classmethod
    def _load(cls):
        data = cls._load_from_redis()
        if data:
            cls._sessions = data.get("sessions", {})
            cls._users = data.get("users", {})
            cls._companies = data.get("companies", {})
            print("sessions :"+ str(cls._sessions))

    @classmethod
    def _save_to_redis(cls):
        try:
            data = cls.toDict()
            print("save "+str(data))
            redis_client.set('sessions_data', pickle.dumps(data))
        except Exception as e:
            print(f"Error al guardar en Redis: {e}")

