from sqlalchemy import and_
from app.models.db import db
from sqlalchemy.sql.schema import ForeignKey
import uuid
from sqlalchemy.orm import relationship
from app.helpers.message import Message
from app.models.auction import Auction
import datetime
from app.helpers.modelosPlanos.article import Article as A
from pytz import timezone
from app.socket.socketio import start, emit_start,emit_finish
from app.helpers.celery import startedArticle, finishedArticle


date_format = '%d/%m/%YT%H:%M:%S%z'
zona_horaria= timezone("America/Argentina/Buenos_Aires")
class Article(db.Model):
    uuid=db.Column(
        db.String(255), primary_key=True, default=uuid.uuid4, nullable=True, unique=True
        )
    auction= db.Column(
        db.String(255),
        ForeignKey(Auction.uuid),
        nullable= True
    ) 
    before = db.Column(
        db.String(255),
        ForeignKey("article.uuid")
    ) 
    next = db.Column(
        db.String(255),
        ForeignKey("article.uuid") 
    ) 
    maxBid= db.Column(
        db.String(255),
        ForeignKey("bid.uuid")
    )
    dataBid = relationship("Bid", foreign_keys=[maxBid])
    bidValue= db.Column(
        db.Integer
    )
    description=db.Column(
        db.String(255),
        nullable=True
    )
    removed =db.Column(
        db.Integer,
        nullable=True,
        default=0
    )
    started =db.Column(
        db.Integer,
        nullable=True,
        default=0
    )
    finished= db.Column(
        db.Integer,
        nullable=True,
        default=0
    )
    dateOfStart=db.Column(
        db.String(255)
    )
    dateOfFinish=db.Column(
        db.String(255)
    )
    timeAfterBid=db.Column(
        db.Integer
    )
    type= db.Column(
        db.Integer,
        nullable=True,
        default=0
    )
    minValue= db.Column(
        db.Integer
    )
    minStepValue = db.Column(
        db.Integer
    )
    dateOfCreate=db.Column(
        db.String(255),
        nullable=True
    )
    dateOfUpdate=db.Column(
        db.String(255),
        nullable=True,
        default=None
    )
    urlPhoto=db.Column(
        db.String(255),
        nullable=True
    )
    


    @classmethod
    def create(cls,data,owner):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        sms=  Auction.get(data.get("auction"))
        if sms.dump()["error"]:
            return Message(error="No se puede guardar el articulo por que no existe el remate")
        if sms.dump()["content"]["dataCompany"]["owner"]!= owner:
            return Message(error="No se puede guardar el articulo por que eres el propietario del remate")
        
        before= cls.query.filter(and_(cls.auction == data.get("auction"),cls.removed == 0,cls.next.is_(None) )).first()
        article= None
        if not before:
            article= cls(
                    auction= data.get("auction"),
                    description= data.get("description"),
                    dateOfStart= data.get("dateOfStart"),
                    dateOfFinish=data.get("dateOfFinish"),
                    timeAfterBid= data.get("timeAfterBid") ,
                    type= data.get("type"),
                    minValue=data.get("minValue"),
                    minStepValue=data.get("minStepValue"),
                    dateOfCreate= strDate,
                    urlPhoto=data.get("urlPhoto")
                )
        else:
            article= cls(
                auction= data.get("auction"),
                before= before.uuid or None,
                description= data.get("description"),
                dateOfStart= data.get("dateOfStart"),
                dateOfFinish=data.get("dateOfFinish"),
                timeAfterBid= data.get("timeAfterBid") ,
                type= data.get("type"),
                minValue=data.get("minValue"),
                minStepValue=data.get("minStepValue"),
                dateOfCreate= strDate,
                urlPhoto=data.get("urlPhoto")
            )
        
        db.session.add(article)
        db.session.commit()
        a= A(article)
        if before:
            cls.setNext(article.uuid,before.uuid)
        db.session.close()
        return Message(content=a)
    
    @classmethod
    def all(cls):
        articles= cls.query.filter_by(removed=0).all()
        art=A(None,articles)
        db.session.close()
        return Message(content=art)
    
    @classmethod
    def get(cls,uuid):
        article= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not article):
            return Message(error="No se pudo obtener el articulo por que no existe")
        art=A(article)
        db.session.close()
        return Message(content=art)
    
    @classmethod
    def delete(cls, uuid,owner):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        article=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not article):
            return Message(error="No se pudo eliminar el articulo por que no existe")
        sms=  Auction.get(article.auction)
        if sms.dump()["content"]["dataCompany"]["owner"]!= owner:
            return Message(error="No se puede eliminar el articulo por que eres el propietario del remate")
        article.removed=1
        article.dateOfUpdate=strDate
        db.session.merge(article)
        db.session.commit()
        db.session.close()
        return Message(content="Articulo eliminado correctamente")
    
    @classmethod
    def deleteByAuction(cls, uuid):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        articles=cls.query.filter_by(auction=uuid, removed=0).all()
        for article in articles:
            article.removed=1
            article.dateOfUpdate=strDate
        db.session.commit()
        db.session.close()
        return Message(content="Artículos eliminados correctamente")

    @classmethod
    def update(cls, data,owner):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        article=cls.query.filter_by(uuid=data["uuid"], removed=0).first()
        if(not article):
            return Message(error="No se pudo actualizar el articulo por que no existe")
        sms=  Auction.get(data.get("auction"))
        if sms.dump()["error"]:
            return Message(error="No se puede actualizar el articulo por que no existe el remate")
        if sms.dump()["content"]["dataCompany"]["owner"]!= owner:
            return Message(error="No se puede eliminar el articulo por que eres el propietario del remate")
        article.description=data.get("description")
        article.dateOfStart= data.get("dateOfStart")
        article.dateOfFinish= data.get("dateOfFinish")
        article.timeAfterBid= data.get("timeAfterBid")
        article.type= data.get("type")
        article.minValue= data.get("minValue")
        article.minStepValue = data.get("minStepValue")
        article.dateOfUpdate=strDate
        article.urlPhoto=data.get("urlPhoto")
        db.session.merge(article)
        db.session.commit()
        art=A(article)
        db.session.close()
        return Message(content=art)
    
    @classmethod
    def updateForAuction(cls, data):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        articles=cls.query.filter_by(auction=data.uuid, removed=0).all()
        for article in articles: 
            article.dateOfStart= data.dateStart
            article.dateOfFinish= data.dateFinish
            article.timeAfterBid= data.timeAfterBid
            article.type= data.type
            article.dateOfUpdate=strDate
            db.session.merge(article)
            db.session.commit()
        db.session.close()
        return Message(content="Artículos actualizados")
    
    @classmethod
    def setBefore(cls, uuidBefore, uuid):
        article= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not article):
            return Message(error="No se pudo obtener el articulo por que no existe")
        article.before= uuidBefore
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        article.dateOfUpdate=strDate
        db.session.merge(article)
        db.session.commit()
        art=A(article)
        db.session.close()
        return Message(content=art)

    @classmethod
    def setNext(cls, uuidNext, uuid):
        article= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not article):
            return Message(error="No se pudo actualizar el articulo por que no existe")
        article.next= uuidNext
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        article.dateOfUpdate=strDate
        db.session.merge(article)
        db.session.commit()
        art=A(article)
        db.session.close()
        return Message(content=art)

    @classmethod
    def setStarted(cls, uuid):
        article= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not article):
            return Message(error="No se pudo actualizar el articulo por que no existe")
        article.started=1
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        article.dateOfUpdate=strDate
        db.session.merge(article)
        db.session.commit()
        art=A(article)
        emit_start(art.uuid,art.timeAfterBid)
        if art.type ==1:
            finishedArticle(art.uuid,art.timeAfterBid)
            if art.next:
                startedArticle(art.next,art.timeAfterBid)
        db.session.close()
        return Message(content=art)
    
    @classmethod
    def setFinished(cls, uuid):
        article= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not article):
            return Message(error="No se pudo actualizar el articulo por que no existe")
        article.finished=1
        article.started=1
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        article.dateOfUpdate=strDate
        emit_finish(article.uuid)
        db.session.merge(article)
        db.session.commit()
        art=A(article)
        if not  art.next and article.type == 1 :
            Auction.setFinished(art.auction)
        db.session.close()
        return Message(content=art)

    @classmethod
    def getFinished(cls):
        article= cls.query.filter_by(removed=0,finished= 1).all()
        art=A(None,article)
        db.session.close()
        return Message(content=art)

    
    @classmethod
    def setMaxBid(cls, uuid,uuidBid,value):
        article= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not article):
            return Message(error="No se pudo actualizar el articulo por que no existe")
        if article.bidValue and (value- article.bidValue)< article.minStepValue:
            return Message(error="La diferencia con la puja mas alta anterior es menor a lo permitido")
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        article.maxBid=uuidBid
        article.bidValue=value
        article.dateOfUpdate=strDate
        db.session.commit()
        art=A(article)
        if article.type == 1:
            finishedArticle(art.uuid,art.timeAfterBid)
            if art.next:
                startedArticle(art.next,art.timeAfterBid)
        db.session.close()
        return Message(content=art)
    
    @classmethod
    def startAll(cls, uuid):
        articles= cls.query.filter_by(auction=uuid,removed=0).all()
        if(not articles):
            return Message(error="")
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        for article in articles: 
            article.started= 1
            article.dateOfUpdate=strDate
            start(article.uuid)
            db.session.merge(article)
            db.session.commit()
        db.session.close()
        return Message(content="")
    
    @classmethod
    def finishAll(cls, uuid):
        articles= cls.query.filter_by(auction=uuid,removed=0).all()
        if(not articles):
            return Message(error="")
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        for article in articles: 
            article.finished= 1
            article.started= 1
            article.dateOfUpdate=strDate   
            emit_finish(article.uuid)
            db.session.merge(article)
            db.session.commit()
        db.session.close()
        return Message(content="")
    
    @classmethod
    def myArticlesBought(cls, uuid,):
        from app.models.bid import Bid  

        articles = (
            cls.query
            .join(Bid, cls.maxBid == Bid.uuid)
            .filter(Bid.user == uuid, cls.finished == 1,cls.removed == 0)  
            .order_by(Bid.dateOfCreate.desc())
            .all()
        )
        
        if not articles:
            return Message(error="Usted todavía no compro ningún articulo")
        
        art=A(None,articles)
        db.session.close()
        return Message(content=art)

    @classmethod
    def startBefore(cls, uuid):
        before= cls.query.filter(and_(cls.auction == uuid,cls.removed == 0,cls.before.is_(None) )).first()
        if(not before):
            return Message(error="")
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format) 
        before.started= 1
        before.dateOfUpdate=strDate
        emit_start(before.uuid,before.timeAfterBid)
        if before.next:
            startedArticle(before.next,before.timeAfterBid)
        finishedArticle(before.uuid,before.timeAfterBid)
        db.session.merge(before)
        db.session.commit()
        db.session.close()
        return Message(content="")
    
    @classmethod
    def insert_article_in_bulk(cls, articles_data):
        date_format = '%d/%m/%YT%H:%M:%S%z'
        zona_horaria = timezone("America/Argentina/Buenos_Aires")

        current_date = datetime.datetime.now().astimezone(zona_horaria)
        strDate = current_date.strftime(date_format)

        now = datetime.datetime.now().astimezone(zona_horaria)

        articles_to_create = []
        article_map = {} 

        import logging

        logging.info('articles_data: ' + str(len(articles_data)))
        auxArticle={}
        for i, article_data in enumerate(articles_data):
            article = Article(
                auction=article_data["auction"],
                description=article_data["description"],
                dateOfStart=article_data["dateOfStart"],
                dateOfFinish=article_data["dateOfFinish"],
                timeAfterBid=article_data["timeAfterBid"],
                type=article_data["type"],
                minValue=article_data["minValue"],
                minStepValue=article_data["minStepValue"],
                dateOfCreate=strDate,
                urlPhoto=article_data["urlPhoto"],
                next=None, 
                before=None,  
                finished=1 if now >= datetime.datetime.strptime(article_data["dateOfFinish"], date_format) else 0,
                started=1 if now >= datetime.datetime.strptime(article_data["dateOfStart"], date_format) else 0
            )
            if auxArticle.get(article_data["auction"]) != None:
                tam=len(auxArticle[article_data["auction"]])
                uuidB,index= next(iter(auxArticle[article_data["auction"]][tam-1].items()))
                articles_data[index]["next"]= article.uuid
                article_data["before"]=uuidB
                auxArticle[article_data["auction"]].append({article.uuid:i})
            else:
                auxArticle[article_data["auction"]]=[{article.uuid:i}]
            article_data["uuid"]=article.uuid
            articles_to_create.append(article)
            article_map[article.uuid] = article  

        for article_data in articles_data:
            logging.info('uuid ' + article.uuid)
            article = article_map.get(article.uu)
            if article:
                if article_data.get("before") in article_map:
                    article.before = article_map[article_data["before"]]
                if article_data.get("next") in article_map:
                    article.next = article_map[article_data["next"]]

        logging.info('articles_to_create: ' + str(len(articles_to_create)))
        db.session.bulk_save_objects(articles_to_create)
        db.session.commit()
        db.session.close()
        print(f"{len(articles_to_create)} artículos insertados correctamente.")


        
    @classmethod
    def setMaxBidBulk(cls, uuid,uuidBid,value):
        article= cls.query.filter_by(uuid=uuid,removed=0).first()
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        article.maxBid=uuidBid
        article.bidValue=value
        article.dateOfUpdate=strDate
        db.session.commit()
        return 
    
    
    