import uuid 
import datetime
from app.helpers.saveSession import loadDict

class Sessions:
    _instance = None
    _sessions={}
    _users={}
    _companies={}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            data= loadDict("Sessions")
            if data:
                cls._sessions= data["sessions"]  
                cls._users= data["users"] 
                cls._companies= data["companies"]
        return cls._instance

    def __init__(cls):
        cls.variable = "Soy un Singleton"
       
    
    def addSession(cls,data):
        id= str(uuid.uuid4())
        session=  cls._dataSession(id,data)
        cls._addUser(id,data) 
        # cls._addCompany(id,data)
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
    def _addCompany(cls,id,data):
        if cls._companies.get(data.get("company")) and cls._companies.get(data["company"].get("uuid")) and len(data["company"].get("uuid"))!=0:
            cls._companies[data["company"]["uuid"]].append(id)
        else:
            cls._companies[data["company"]["uuid"]]=[id]

    def updateSession(cls,uuid,data):
        session= cls.getSession(uuid)
        newSession= data
        newSession["login"]=session["login"]
        cls._sessions[uuid]=newSession
    
    def updateSessionByUser(cls,uuid,data):
        uuidS= cls._users[uuid] 
        newSession=data
        for i in uuidS:
            newSession["login"]=cls._sessions[i]["login"]
            cls._sessions[i]=newSession
    
    def getSession(cls,uuid):
        return cls._sessions[uuid] 
    
    def getSessionsByUser(cls,uuid):
        uuidS= cls._users[uuid] 
        sessions=[]
        for i in uuidS:
            sessions.append(cls._sessions[i])
        return sessions
    
    def deleteSession(cls,uuid):
        session=cls._sessions.pop(uuid)
        cls._users[session["uuid"]].remove(uuid)
    
    def deleteSessionsByUser(cls,uuid):
        uuidS= cls._users[uuid] 
        for i in uuidS:
            cls._sessions.pop(i)
        cls._users[uuid]=[]

    def toDict(cls):
        dict= {}
        dict["sessions"]= cls._sessions
        dict["users"]= cls._users
        dict["companies"]= cls._companies
        return dict
         
    