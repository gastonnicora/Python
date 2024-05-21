import datetime
from flask import request, jsonify
from app.models.auction import Auction
from app.helpers.token import token_required
from app.helpers.validador import validate_request
from app.socket.socketio import emit_finish, emit_start

@token_required
@validate_request("Remates","auctionCreate")
def create(current_user): 
    sms=Auction.create(request.get_json(),current_user["uuid"])
    if sms.dump()["error"]:
        return jsonify(sms.dump()),sms.cod
    auc=sms.content
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


@token_required 
def start(uuid):
    emit_start(uuid,0)

@token_required 
def finished(uuid):
    sms=Auction.setFinished(uuid)
    emit_finish(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required 
def start(uuid):
    sms=Auction.start(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Remates","auctionUpdate")
def update(session): 
    sms=Auction.update(request.get_json(),session["uuid"])
    if sms.dump()["error"]:
        return jsonify(sms.dump()),sms.cod
    auc=sms.content
    return jsonify(sms.dump()),sms.cod

@token_required 
def delete(session,uuid):
    sms= Auction.delete(uuid,session["uuid"])
    return jsonify(sms.dump()),sms.cod