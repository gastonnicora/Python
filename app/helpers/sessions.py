import uuid 
import datetime

class Sessions:
    _instance = None
    _sessions={}
    _users={}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(cls):
        cls.variable = "Soy un Singleton"
    
    def addSession(cls,data):
        id= str(uuid.uuid4())
        session=  cls._dataSession(id,data)
        cls._addUser(id,data)
        return id,session
    
    def _dataSession(cls,id,data):
        session=data
        date_format = '%d/%m/%Y %H:%M:%S%z'
        date= datetime.datetime.now()
        strDate= date.strftime(date_format)
        session["login"]=strDate 
        cls._sessions[id]=session
        return session
    
    def _addUser(cls,id,data):
        if cls._users.get(data["uuid"]) and len(cls._users[data["uuid"]])!=0:
            cls._users[data["uuid"]].append(id)
        else:
            cls._users[data["uuid"]]=[id]
    
    def updateSession(cls,uuid,data):
        session= cls.getSession(uuid)
        newSession= data
        newSession["login"]=session["login"]
        cls._sessions[session["uuid"]]=newSession
    
    def getSession(cls,uuid):
        return cls._sessions[uuid] 
    
    def deleteSession(cls,uuid):
        session=cls._sessions.pop(uuid)
        cls._users[session["uuid"]].remove(uuid)
    
    


