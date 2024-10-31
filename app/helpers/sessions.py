import uuid
import datetime
import os
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
            cls._load(cls)
        return cls._instance

    def addSession(cls, data):
        id = str(uuid.uuid4())
        session = cls._dataSession(id, data)
        cls._addUser(id, data)
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
        if acquire_lock(user_uuid):
            try:
                cls._load(cls)
                if cls._users.get(user_uuid):
                    cls._users[user_uuid].append(id)
                else:
                    cls._users[user_uuid] = [id]
                cls._save_to_redis(cls)
            finally:
                release_lock(user_uuid)

    def _addCompany(cls, id, data):
        company_uuid = data.get("company", {}).get("uuid")
        if company_uuid:
            if acquire_lock(company_uuid):
                try:
                    cls._load(cls)
                    if cls._companies.get(company_uuid):
                        cls._companies[company_uuid].append(id)
                    else:
                        cls._companies[company_uuid] = [id]

                    cls._save_to_redis(cls)
                finally:
                    release_lock(company_uuid)
        
            

    def updateSession(cls, uuid, data):
        if acquire_lock(uuid):
            try:
                cls._load(cls)
                session = cls.getSession(uuid)
                newSession = data
                newSession["login"] = session["login"]
                cls._sessions[uuid] = newSession
                cls._save_to_redis(cls)
            finally:
                release_lock(uuid)

    def updateSessionByUser(cls, uuid, data):
        if acquire_lock(uuid):
            try:
                uuidS = cls._users.get(uuid, [])
                newSession = data
                for i in uuidS:
                    cls.updateSession(i,newSession)
            finally:
                release_lock(uuid)


    def getSession(cls, uuid):
        session= None
        if acquire_lock(uuid):
            try:
                cls._load(cls)
                session= cls._sessions.get(uuid)
            finally:
                release_lock(uuid)
        return session

    def getSessionsByUser(cls, uuid):
        sessions= None
        if acquire_lock(uuid):
            try:
                cls._load(cls)
                uuidS = cls._users.get(uuid, [])
                sessions = [cls.getSession(i) for i in uuidS]
            finally:
                release_lock(uuid)
        return sessions

    def deleteSession(cls, uuid):
        if acquire_lock(uuid):
            try:
                cls._load(cls)
                session = cls._sessions.pop(uuid, None)
                if session:
                    cls._users[session["uuid"]].remove(uuid)
                    cls._save_to_redis(cls)
            finally:
                release_lock(uuid)
        

    def deleteSessionsByUser(cls, uuid):
        if acquire_lock(uuid):
            try:
                cls._load(cls)
                uuidS = cls._users.get(uuid, [])
                for i in uuidS:
                    cls.deleteSession(i)
                cls._save_to_redis(cls)
            finally:
                release_lock(uuid)
        

    def toDict(cls):
        return {
            "sessions": cls._sessions,
            "users": cls._users,
            "companies": cls._companies
        }

    def _load_from_redis(cls):
        data = redis_client.get('sessions_data')
        if data:
            return pickle.loads(data)
        return None

    def _load(cls):
        data= cls._load_from_redis()
        if data:
            cls._sessions = data["sessions"]
            cls._users = data["users"]
            cls._companies = data["companies"]
    def _save_to_redis(cls):
        data = cls.toDict()
        redis_client.set('sessions_data', pickle.dumps(data))

