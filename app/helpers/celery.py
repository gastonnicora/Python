import json
import os
from flask import request, jsonify
import jwt
from os import environ
from uuid import uuid4
import requests as R   

import socket

from app.helpers.saveSession import loadDict



celery=environ.get("CELERY", "http://127.0.0.1:5000")

     
def deleteConfirm(uuid):
    r=R.get(celery+"/deleteConfirm/"+uuid)

def finishedArticle(uuid,time):
    data= {"article":uuid,"time":time}
    r=R.post(celery+"/finishedArticle",json=data)


def startedArticle(uuid,time):
    data= {"article":uuid,"time":time}
    r=R.post(celery+"/startedArticle",json=data)


def startedAuction(uuid,time):
    data= {"article":uuid,"time":time}
    r=R.post(celery+"/startedAuction",json=data)



