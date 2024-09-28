from flask import request, jsonify
from app.helpers.validador import validate_request
from app.models.article import Article
from app.helpers.token import token_required


@token_required
@validate_request("Articulos","articleCreate")
def create(current_user): 
    sms=Article.create(request.get_json(),current_user["uuid"])
    return jsonify(sms.dump()),sms.cod

def index():
    sms = Article.all()
    return jsonify(sms.dump()),sms.cod

def get(uuid):
    sms=Article.get(uuid)
    return jsonify(sms.dump()),sms.cod

@token_required
@validate_request("Articulos","articleUpdate")
def update(session): 
    sms=Article.update(request.get_json(),session["uuid"])
    return jsonify(sms.dump()),sms.cod

@token_required
def myArticlesBought(session):
    sms=Article.myArticlesBought(session["uuid"])
    return jsonify(sms.dump()),sms.cod


@token_required 
def delete(session,uuid):
    article= Article.get(uuid)    
    sms= Article.delete(uuid,session["uuid"])
    if not sms.dump()["error"]:
        before= article.dump()["content"]["before"]
        next= article.dump()["content"]["next"]
        if before and next:
            Article.setBefore(before,next)
            Article.setNext(next,before)
        elif before:
            Article.setNext(None,before)
        elif next:
            Article.setBefore(None,next)
    return jsonify(sms.dump()),sms.cod


@token_required 
def start(session,uuid):
    if not session.get("name"):
        sms= Article.setStarted(uuid)
        return jsonify(sms.dump()),sms.cod
    else: 
        return jsonify({"error":"No sos celery"}),404



@token_required 
def finish(session,uuid):

    if not session.get("name"):
        sms= Article.setFinished(uuid)
        return jsonify(sms.dump()),sms.cod
    else: 
        return jsonify({"error":"No sos celery"}),404


