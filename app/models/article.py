from app.models.db import db
from sqlalchemy.sql.schema import ForeignKey
import uuid
from sqlalchemy.orm import relationship
from app.helpers.message import Message
from app.models.auction import Auction
import datetime
from app.helpers.modelosPlanos.article import Article as A
from pytz import timezone

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
    dataAuction= relationship(Auction,foreign_keys=auction)
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
    tipe= db.Column(
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
    


    @classmethod
    def create(cls,data):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        sms=  Auction.get(data.get("auction"))
        if sms.dump()["error"]:
            return Message(error="No se puede guardar el articulo por que no existe el remate")
        
        before= cls.query.filter_by(uuid=data.get("before"),removed=0).first() or None
        article= cls(
                auction= data.get("auction"),
                before= before,
                description= data.get("description"),
                dateOfStart= data.get("dateOfStart"),
                dateOfFinish=data.get("dateOfFinish"),
                timeAfterBid= data.get("timeAfterBid") ,
                tipe= data.get("tipe"),
                minValue=data.get("minValue"),
                minStepValue=data.get("minStepValue"),
                dateOfCreate= strDate
            )
        db.session.add(article)
        db.session.commit()
        a= A(article)
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
    def delete(cls, uuid):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        article=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not article):
            return Message(error="No se pudo eliminar el articulo por que no existe")
        article.removed=1
        article.dateOfUpdate=strDate
        db.session.merge(article)
        db.session.commit()
        db.session.close()
        return Message(content="Articulo eliminado correctamente")

    @classmethod
    def update(cls, data):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        article=cls.query.filter_by(uuid=data["uuid"], removed=0).first()
        if(not article):
            return Message(error="No se pudo actualizar el articulo por que no existe")
        sms=  Auction.get(data.get("auction"))
        if sms.dump()["error"]:
            return Message(error="No se puede actualizar el articulo por que no existe el remate")
        article.description=data.get("description")
        article.dateOfStart= data.get("dateOfStart")
        article.dateOfFinish= data.get("dateOfFinish")
        article.timeAfterBid= data.get("timeAfterBid")
        article.tipe= data.get("tipe")
        article.minValue= data.get("minValue")
        article.minStepValue = data.get("minStepValue")
        article.dateOfUpdate=strDate
        db.session.merge(article)
        db.session.commit()
        art=A(article)
        db.session.close()
        return Message(content=art)
    
    @classmethod
    def setBefore(cls, uuidBefore, uuid):
        article= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not article):
            return Message(error="No se pudo obtener el articulo por que no existe")
        article2= cls.query.filter_by(uuid=uuidBefore,removed=0).first()
        if(not article2 and not uuidBefore):
            return Message(error="No se pudo obtener el articulo anterior por que no existe")
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
        article2= cls.query.filter_by(uuid=uuidNext,removed=0).first()
        if(not article2 and not uuidNext):
            return Message(error="No se pudo actualizar el articulo siguiente por que no existe")
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
        db.session.close()
        return Message(content=art)
    
    @classmethod
    def setFinished(cls, uuid):
        article= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not article):
            return Message(error="No se pudo actualizar el articulo por que no existe")
        article.finished=1
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
        db.session.close()
        return Message(content=art)
    
    
    