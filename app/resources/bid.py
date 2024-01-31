from flask import request, jsonify
from app.helpers.validador import Validador
from app.models.bid import Bid
from app.helpers.token import token_required
from app.helpers.celery import finishedArticle
from app.models.article import Article

@token_required
def create(current_user): 
    v= Validador("Pujas","bidCreate",request.get_json())
    if v.haveError:
        return jsonify(v.errors().dump()),v.errors().cod
    sms=Bid.create(request.get_json(),current_user["uuid"])
    a= Article.get(request.get_json().get("article"))
    if a.content.tipe and a.content.tipe== 1:
        finishedArticle(a.content.uuid, a.content.timeAfterBid)
    return jsonify(sms.dump()),sms.cod

@token_required
def index(current_user):
    sms = Bid.all()
    return jsonify(sms.dump()),sms.cod

@token_required
def get(current_user,uuid):
    sms=Bid.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
def getByArticle(current_user,uuid):
    sms=Bid.getByArticle(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
def getByUser(current_user,uuid):
    sms=Bid.getByUser(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
def delete(current_user,uuid):
    sms= Bid.delete(uuid)
    return jsonify(sms.dump()),sms.cod
