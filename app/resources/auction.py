import datetime
from flask import request, jsonify
from app.helpers.validador import Validador
from app.models.auction import Auction
from app.helpers.token import token_required
from app.helpers.tokenCelery import token_required_celery
from app.helpers.celery import startedAuction

@token_required
def create(current_user): 
    v= Validador("Remates","auctionCreate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    
    sms=Auction.create(request.get_json())
    auc=sms.content
    date_format="%d/%m/%YT%H:%M:%S%z"
    d=  datetime.datetime.strptime(auc.dateStart, date_format)
    d=d.astimezone(datetime.timezone.utc)
    now=datetime.datetime.now()
    now=now.astimezone(datetime.timezone.utc)
    delta= (d-now).total_seconds()
    startedAuction(auc.uuid,delta)
    return jsonify(sms.dump()),sms.cod

def index():
    sms = Auction.all()
    return jsonify(sms.dump()),sms.cod

def allNotFinished():
    sms = Auction.allNotFinished()
    return jsonify(sms.dump()),sms.cod

def allFinished():
    sms = Auction.allFinished()
    return jsonify(sms.dump()),sms.cod

def allStarted():
    sms = Auction.allStarted()
    return jsonify(sms.dump()),sms.cod

def allNotStarted():
    sms = Auction.allNotStarted()
    return jsonify(sms.dump()),sms.cod


def get(uuid):
    sms=Auction.get(uuid)
    return jsonify(sms.dump()),sms.cod


def getByCompany(uuid):
    sms=Auction.getByCompany(uuid)
    return jsonify(sms.dump()),sms.cod


@token_required_celery
def finished(uuid):
    sms=Auction.setFinished(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
def update(session): 
    v= Validador("Remates","auctionUpdate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=Auction.update(request.get_json())
    auc=sms.content
    date_format="%d/%m/%YT%H:%M:%S%z"
    d=  datetime.datetime.strptime(auc.dateStart, date_format)
    d=d.astimezone(datetime.timezone.utc)
    now=datetime.datetime.now()
    now=now.astimezone(datetime.timezone.utc)
    delta= (d-now).total_seconds()
    startedAuction(auc.uuid,delta)
    return jsonify(sms.dump()),sms.cod

@token_required 
def delete(session,uuid):
    sms= Auction.delete(uuid)
    return jsonify(sms.dump()),sms.cod