from flask import request, jsonify
from app.helpers.validador import validate_request
from app.models.bid import Bid
from app.helpers.token import token_required
from app.models.article import Article

@token_required
@validate_request("Pujas","bidCreate")
def create(current_user): 
    sms=Bid.create(request.get_json(),current_user["uuid"])
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
    a= Article.get(uuid)
    from app.models.auction import Auction
    auc = Auction.get(a.content.auction)
    if auc.content.dataCompany.owner != current_user["uuid"]:
        return jsonify({"error":"No se puede ver por que no sos el dueño del remate en el que esta el articulo"}),400
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
