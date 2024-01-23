from app.models.db import db
from sqlalchemy.sql.schema import ForeignKey
import uuid
from app.helpers.message import Message
from app.models.user import User
import datetime
from app.helpers.modelosPlanos.bid import Bid as B
from app.models.article import Article


date_format = '%d/%m/%YT%H:%M:%S%z'
class Bid(db.Model):
    uuid=db.Column(
        db.String(255), primary_key=True, default=uuid.uuid4, nullable=True, unique=True
        )
    
    article= db.Column(
        db.String(255),
        ForeignKey(Article.uuid),
        nullable= True
    ) 
    user= db.Column(
        db.String(255),
        ForeignKey(User.uuid),
        nullable= True
    )
    value=db.Column(
        db.Integer,
        nullable=True
    )
    removed =db.Column(
        db.Integer,
        nullable=True,
        default=0
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
    def create(cls,data,userUuid):
        date= datetime.datetime.now()
        date=date.astimezone(datetime.timezone.utc)
        strDate= date.strftime(date_format)
        bid= cls(
                user=userUuid,
                value= data.get("value"),
                article= data.get("article"),
                dateOfCreate= strDate
            )
        db.session.add(bid)
        sms=Article.setMaxBid(data.get("article"), bid.uuid,data.get("value"))
        if(sms.cod == 202):
            db.session.commit()
            c= B(bid)
            db.session.close()
            return Message(content=c)
        else: 
            return Message(error=sms.error)
    
    @classmethod
    def all(cls):
        bids= cls.query.filter_by(removed=0).all()
        com=B(None,bids)
        db.session.close()
        return Message(content=com)
    
    @classmethod
    def get(cls,uuid):
        bid= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not bid):
            return Message(error="No se pudo obtener la puja por que no existe")
        com=B(bid)
        db.session.close()
        return Message(content=com)
   
    @classmethod
    def getByArticle(cls,article):
        bids= cls.query.filter_by(article=article, removed=0).all()
        return bids

    @classmethod
    def getByUser(cls,user):
        bids= cls.query.filter_by(user=user).all()
        return bids

    @classmethod
    def delete(cls,uuid):
        bids= cls.query.filter_by(uuid=uuid).first()
        return bids