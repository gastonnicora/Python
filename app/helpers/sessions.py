import uuid 
import datetime

class Sessions:
    _instance = None
    _sessions={}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(cls):
        cls.variable = "Soy un Singleton"
    
    def addSession(cls,data):
        id= str(uuid.uuid4())
        session=data
        date_format = '%d/%m/%Y %H:%M:%S%z'
        date= datetime.datetime.now()
        strDate= date.strftime(date_format)
        session["login"]=strDate 
        cls._sessions[id]=session
        return id,session
    
    def updateSession(cls,uuid,data):
        session= cls.getSession(uuid)
        newSession= data
        newSession["login"]=session["login"]
        cls._sessions[session["uuid"]]=newSession
    
    def getSession(cls,uuid):
        return cls._sessions[uuid] 
    
    def deleteSession(cls,uuid):
        cls._sessions.pop(uuid)
    
    


