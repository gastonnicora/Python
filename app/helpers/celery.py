import json
from flask import request, jsonify
import jwt
from os import environ
from uuid import uuid4
import requests as R   

celery=environ.get("CELERY", "127.0.0.1:5000")

def url(referer):
    r=None
    try:
        link="https://"+referer
        r=R.get(link+"/ping")
        return link,202
    except:
        try:
            link="http://"+referer
            r=R.get(link+"/ping")
            return link,202
        except:
            return None,404

def login():
    uuid=str(uuid4())
    Celery().setUuid(uuid)
    token = jwt.encode({'uuid':uuid}, environ.get("SECRET_KEY", "1234"), algorithm="HS256")
    link,r= url(celery)
    if r== 404:
        return jsonify({"error":"La url esta mal o el servidor desconectado"}),404  
    Celery().setLink(link)
    headers = {'Referer': request.headers.get("Host"),"X-Access-Tokens":token}
    r=R.get(link+"/login",headers=headers)

     
def deleteConfirm(uuid):
    if Celery()._uuid== None:
        login()
    link= Celery().getLink()
    headers = {'Referer': request.headers.get("Host")}
    r=R.get(link+"/deleteConfirm/"+uuid,headers=headers)

def finishedArticle(uuid,time):
    if Celery()._uuid== None:
        login()
    link= Celery().getLink()
    headers = {'Referer': request.headers.get("Host")}
    data= {"article":uuid,"time":time}
    r=R.post(link+"/finishedArticle",headers=headers,json=data)


def startedArticle(uuid,time):
    if Celery()._uuid== None:
        login()
    link= Celery().getLink()
    headers = {'Referer': request.headers.get("Host")}
    data= {"article":uuid,"time":time}
    r=R.post(link+"/startedArticle",headers=headers,json=data)





class Celery:
    _instance = None
    _uuid=None
    _link=None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(cls):
        cls.variable = "Soy un Singleton"
    
    def _getUuid(cls):
        return cls._uuid
    
    def setUuid(cls, uuid):
        cls._uuid=uuid

    def setLink(cls,link):
        cls._link= link
    
    def getLink(cls):
        return cls._link