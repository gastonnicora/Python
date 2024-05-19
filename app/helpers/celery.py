import json
import os
from flask import request, jsonify
import jwt
from os import environ
from uuid import uuid4
import requests as R   

import socket

from app.helpers.saveSession import loadDict

celery=environ.get("CELERY", "127.0.0.1:5000")

def get_server_url(port):
    # Obtener la dirección IP del contenedor
    ip_address = socket.gethostbyname(socket.gethostname())
    # Construir la URL del servidor usando la dirección IP y el puerto
    server_url = f'http://{ip_address}:{port}'
    return server_url

# Obtener la URL del servidor para el puerto 4000 (por ejemplo)
server_url = get_server_url(4000)

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
    token = jwt.encode({'uuid':uuid},environ.get("SECRET_KEY","1234"), algorithm="HS256")
    link,r= url(celery)
    if r== 404:
        return jsonify({"error":"La url esta mal o el servidor desconectado"}),404  
    Celery().setLink(link)
    headers = {'Referer': request.host,"X-Access-Tokens":token}
    r=R.get(link+"/login",headers=headers)

     
def deleteConfirm(uuid):
    for key, value in os.environ.items():
        print(f"{key}: {value}")

    
    print(f'La URL del servidor es: {server_url}')
    if Celery()._uuid== None:
        login()
    link= Celery().getLink()
    headers = {'Referer': request.host}
    r=R.get(link+"/deleteConfirm/"+uuid,headers=headers)

def finishedArticle(uuid,time):
    if Celery()._uuid== None:
        login()
    link= Celery().getLink()
    headers = {'Referer': request.host}
    data= {"article":uuid,"time":time}
    r=R.post(link+"/finishedArticle",headers=headers,json=data)


def startedArticle(uuid,time):
    if Celery()._uuid== None:
        login()
    link= Celery().getLink()
    headers = {'Referer': request.host}
    data= {"article":uuid,"time":time}
    r=R.post(link+"/startedArticle",headers=headers,json=data)


def startedAuction(uuid,time):
    if Celery()._uuid== None:
        login()
    link= Celery().getLink()
    headers = {'Referer': request.host}
    data= {"article":uuid,"time":time}
    r=R.post(link+"/startedAuction",headers=headers,json=data)




class Celery:
    _instance = None
    _uuid=None
    _link=None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            data= loadDict("Celery.pkl")
            if data:
                cls._uuid= data["uuid"]  
                cls._link= data["link"] 
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
    
    def toDict(cls):
        data={"uuid":cls._uuid,"link":cls._link}
        return data 