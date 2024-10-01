from app.models.db import db
from datetime import timezone
from sqlalchemy.sql.schema import ForeignKey
import uuid
from app.helpers.message import Message
from app.models.company import Company
import datetime
from app.helpers.modelosPlanos.auction import Auction as A
from pytz import timezone
from sqlalchemy.orm import relationship

from app.helpers.celery import startedAuction, finishedAuction

date_format = '%d/%m/%YT%H:%M:%S%z'
zona_horaria= timezone("America/Argentina/Buenos_Aires") 
class Auction(db.Model):
    uuid=db.Column(
        db.String(255), primary_key=True, default=uuid.uuid4, nullable=True, unique=True
        )
    company= db.Column(
        db.String(255),
        ForeignKey(Company.uuid),
        nullable= True
    ) 
    dataCompany = relationship(Company, foreign_keys=[company])
    articles=db.relationship('Article', backref="Auction", lazy='dynamic',
                                primaryjoin="and_(Article.auction==Auction.uuid, Article.removed==0)")
    description= db.Column(
        db.String(255),
        nullable= True
    )
    dateStart= db.Column(
        db.String(255),
        nullable=True
    )
    dateFinish= db.Column(
        db.String(255)
    )
    type= db.Column(
        db.Integer,
        nullable=True,
        default=0
    )
    timeAfterBid= db.Column(
        db.Integer
    )
    finished= db.Column(
        db.Integer,
        nullable=True,
        default=0
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
    def create(cls,data,owner):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        sms=  Company.get(data.get("company"))
        if data.get("type")==0 and not data.get("dateFinish"):
            return Message(error="No se puede guardar el remate por que debe ingresar una fecha de finalización  valida")
        if data.get("type")==1 and not data.get("timeAfterBid"):
            return Message(error="No se puede guardar el remate por que debe ingresar un tiempo para finalizar el remate después de la ultima puja")
        if sms.dump()["error"]:
            return Message(error="No se puede guardar el remate por que no existe la compañía")
        if sms.dump()["content"]["owner"]!= owner:
            return Message(error="No se puede guardar el remate por que no sos el dueño de la compañía")
        auction= cls(
                company=data.get("company"),
                description= data.get("description"),
                dateStart= data.get("dateStart"),
                dateOfCreate= strDate,
                type= data.get("type"),
                dateFinish= data.get("dateFinish"),
                timeAfterBid= data.get("timeAfterBid")
            )
        db.session.add(auction)
        db.session.commit()
        auc= A(auction)
        db.session.close()
        startedAuction(auc.uuid,auc.dateStart)
        return Message(content=auc)
    
    @classmethod
    def insert_auction_in_bulk(cls,auctions_data):
        date_format = '%d/%m/%YT%H:%M:%S%z'
        zona_horaria = timezone("America/Argentina/Buenos_Aires")

        current_date = datetime.datetime.now().astimezone(zona_horaria)
        strDate = current_date.strftime(date_format)

        auctions_to_create = []

        now= datetime.datetime.now()
        now=now.astimezone(zona_horaria)
        for auction_data in auctions_data:
            auction= cls(
                company=auction_data["company"],
                description= auction_data["description"],
                dateStart= auction_data["dateStart"],
                dateOfCreate= strDate,
                type= auction_data["type"],
                dateFinish= auction_data["dateFinish"],
                timeAfterBid= auction_data["timeAfterBid"],
                finished= 1 if now >= datetime.datetime.strptime(auction_data["dateFinish"], date_format) else 0,
            )
            if strDate < auction_data["dateStart"] and auction.finished == 0:
                startedAuction(auction.uuid,auction_data["dateStart"])
            auctions_to_create.append(auction)

        db.session.bulk_save_objects(auctions_to_create)
        db.session.commit()
        db.session.close()
        print(f"{len(auctions_to_create)} remates insertados correctamente.")
    
    @classmethod
    def all(cls):
        auctions= cls.query.filter_by(removed=0).all()
        auc=A(None,auctions)
        db.session.close()
        return Message(content=auc)

    @classmethod
    def allNotFinished(cls):
        auctions= cls.query.filter_by(removed=0,finished= 0).all()
        auc=A(None,auctions)
        db.session.close()
        return Message(content=auc)

    @classmethod
    def allFinished(cls):
        auctions= cls.query.filter_by(removed=0,finished= 1).all()
        auc=A(None,auctions)
        db.session.close()
        return Message(content=auc)
    
    @classmethod
    def allStarted(cls):
        auctions= cls.query.filter_by(removed=0,finished= 0).all()
        aucs=[]
        for auc in auctions:
            now=datetime.datetime.now()
            date_max = datetime.datetime.strptime(auc.dateStart, date_format)
            date_max = date_max.astimezone(datetime.timezone.utc)
            now = now.astimezone(zona_horaria)
            if(date_max < now):
                aucs.append(auc)
        auc=A(None,aucs)
        db.session.close()
        return Message(content=auc)   

    @classmethod
    def allNotStarted(cls):
        auctions= cls.query.filter_by(removed=0,finished= 0).all()
        aucs=[]
        for auc in auctions:
            now=datetime.datetime.now()
            date_max = datetime.datetime.strptime(auc.dateStart, date_format)
            date_max = date_max.astimezone(datetime.timezone.utc)
            now = now.astimezone(zona_horaria)
            if(date_max > now):
                aucs.append(auc)
        auc=A(None,aucs)
        db.session.close()
        return Message(content=auc)    
    
    @classmethod
    def get(cls,uuid):
        auction= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not auction):
            return Message(error="No se pudo obtener el remate por que no existe")
        auc=A(auction)
        db.session.close()
        return Message(content=auc)
    
    @classmethod
    def getByCompany(cls,uuid):
        auction= cls.query.filter_by(company=uuid,removed=0).all()
        auc=A(data=None,lista=auction)
        db.session.close()
        return Message(content=auc)
    
    @classmethod
    def delete(cls, uuid, owner):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        auction=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not auction):
            return Message(error="No se pudo eliminar el remate por que no existe")
        if auction.dataCompany.owner != owner:
            return Message(error="No se puede eliminar el remate por que no sos el dueño de la compañía propietaria del remate")
        auction.removed=1
        auction.dateOfUpdate=strDate
        db.session.merge(auction)
        db.session.commit()
        db.session.close()
        from app.models.article import Article
        Article.deleteByAuction(uuid)
        return Message(content="Remate eliminado correctamente")
    
    @classmethod
    def deleteByCompany(cls, uuid):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        auctions=cls.query.filter_by(company=uuid, removed=0).all()
        from app.models.article import Article
        for auction in auctions:
            auction.removed=1
            auction.dateOfUpdate=strDate
            Article.deleteByAuction(auction.uuid)
            db.session.merge(auction)
        db.session.commit()
        db.session.close()
        return Message(content="Remate eliminado correctamente")

    @classmethod
    def update(cls, data,owner):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        sms=  Company.get(data.get("company"))
        if data.get("type")==0 and not data.get("dateFinish"):
            return Message(error="No se puede actualizar el remate por que debe ingresar una fecha de finalización  valida")
        if data.get("type")==1 and not data.get("timeAfterBid"):
            return Message(error="No se puede actualizar el remate por que debe ingresar un tiempo para finalizar el remate despues de la ultima puja")
        if sms.dump()["error"]:
            return Message(error="No se puede actualizar el remate por que no existe la compañía")
        auction=cls.query.filter_by(uuid=data["uuid"], removed=0).first()
        if(not auction):
            return Message(error="No se pudo actualizar el remate por que no existe")
        if auction.dataCompany.owner != owner:
            return Message(error="No se puede actualizar el remate por que no sos el dueño de la compañía propietaria del remate")
        auction.description=data.get("description")
        auction.dateStart= data.get("dateStart")
        auction.company= data.get("company")
        auction.type= data.get("type"),
        auction.dateFinish= data.get("dateFinish"),
        auction.timeAfterBid= data.get("timeAfterBid")
        auction.dateOfUpdate=strDate
        db.session.merge(auction)
        db.session.commit()
        auc=A(auction)
        from app.models.article import Article
        Article.updateForAuction(auc)
        db.session.close()
        startedAuction(auc.uuid,auc.dateStart)
        if auc.type==0:
            finishedAuction(auc.uuid,auc.dateFinish)
        return Message(content=auc)

    @classmethod
    def setFinished(cls, uuid):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        auction=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not auction):
            return Message(error="No se pudo actualizar el remate por que no existe")
        auction.finished=1
        auction.dateOfUpdate=strDate
        db.session.merge(auction)
        db.session.commit()
        auc=A(auction)
        if auc.type == 0:
            from app.models.article import Article
            Article.finishAll(auc.uuid)
        db.session.close()
        return Message(content=auc)
    
    @classmethod
    def start(cls, uuid):
        auction=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not auction):
            return Message(error="No se pudo actualizar el remate por que no existe")
        
        auc=A(auction)
        from app.models.article import Article
        if auction.type==0:
            Article.startAll(auction.uuid)
            finishedAuction(auc.uuid,auc.dateFinish)
        else:
            Article.startBefore(auction.uuid)
        
        db.session.close()
        return Message(content=auc)
    
    
    
    