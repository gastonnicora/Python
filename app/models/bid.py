from app.models.db import db
from sqlalchemy.sql.schema import ForeignKey
import uuid
from app.helpers.message import Message
from app.models.user import User
import datetime
from app.helpers.modelosPlanos.bid import Bid as B
from app.models.article import Article
from pytz import timezone
from sqlalchemy.orm import relationship

from app.socket.socketio import emit_bid

date_format = '%d/%m/%YT%H:%M:%S%z'
zona_horaria= timezone("America/Argentina/Buenos_Aires")
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
    dataUser = relationship(User, foreign_keys=[user])
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
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        sms=  User.get(userUuid)
        if sms.dump()["error"]:
            return Message(error="No se puede guardar la puja por que no existe el usuario")
        sms=  Article.get(data.get("article"))
        if sms.dump()["error"]:
            return Message(error="No se puede guardar la puja por que no existe el articulo")
        if sms.dump()["content"]["started"] == 0:
            return Message(error="No se puede guardar la puja por que el la subasta del articulo no comenzó")
        if sms.dump()["content"]["finished"] == 1:
            return Message(error="No se puede guardar la puja por que el la subasta del articulo ya finalizo")
        bid= cls(
                user=userUuid,
                value= data.get("value"),
                article= data.get("article"),
                dateOfCreate= strDate
            )
        db.session.add(bid)
        db.session.commit()
        c= B(bid)
        db.session.close()
        sms=Article.setMaxBid(data.get("article"),bid.uuid,data.get("value"))
        if(sms.cod != 202 ):
            cls.delete(bid.uuid)
            return sms
        else: 
            emit_bid({"bid":c.to_dict(), "room":data.get("article")})
            return Message(content=c)
        
    @classmethod
    def insert_bid_in_bulk(cls,bids_data):
        date_format = '%d/%m/%YT%H:%M:%S%z'
        zona_horaria = timezone("America/Argentina/Buenos_Aires")

        current_date = datetime.datetime.now().astimezone(zona_horaria)
        strDate = current_date.strftime(date_format)

        bids_to_create = []
        for bid_data in bids_data:
            bid= cls(
                uuid=bid_data["uuid"],
                user=bid_data["user"],
                value= bid_data["value"],
                article= bid_data["article"],
                dateOfCreate= strDate
            )
            bids_to_create.append(bid)

        db.session.bulk_save_objects(bids_to_create)
        db.session.commit()
        Article.setMaxBidBulk(bids_data)
        db.session.close()
        print(f"{len(bids_to_create)} pujas insertados correctamente.")
    
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
        bids= cls.query.filter_by(article=article, removed=0).order_by(cls.value).all()
        com=B(lista=bids)
        return Message(content=com)

    @classmethod
    def getByUser(cls,user):
        bids= cls.query.filter_by(user=user).all()
        com=B(lista=bids)
        return  Message(content=com)

    @classmethod
    def delete(cls,uuid):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        bid= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not bid):
            return Message(error="No se pudo eliminar la puja por que no existe")
        bid.removed= 1
        bid.dateOfUpdate=strDate
        db.session.commit()
        c= B(bid)
        db.session.close()
        return  Message(content="Puja eliminada correctamente")