from app.models.db import db
from datetime import timezone
from sqlalchemy.sql.schema import ForeignKey
import uuid
from app.helpers.message import Message
from app.models.company import Company
import datetime
from app.helpers.modelosPlanos.auction import Auction as A


date_format = '%d/%m/%YT%H:%M:%S%z'
class Auction(db.Model):
    uuid=db.Column(
        db.String(255), primary_key=True, default=uuid.uuid4, nullable=True, unique=True
        )
    company= db.Column(
        db.String(255),
        ForeignKey(Company.uuid),
        nullable= True
    ) 
    description= db.Column(
        db.String(255),
        nullable= True
    )
    dateStart= db.Column(
        db.String(255),
        nullable=True
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
    def create(cls,data):
        date= datetime.datetime.now()
        date=date.astimezone(datetime.timezone.utc)
        strDate= date.strftime(date_format)
        auction= cls(
                company=data.get("company"),
                description= data.get("description"),
                dateStart= data.get("dateStart"),
                dateOfCreate= strDate
            )
        db.session.add(auction)
        db.session.commit()
        auc= A(auction)
        db.session.close()
        return Message(content=auc)
    
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
            date_max = date_max.astimezone(timezone.utc)
            now = now.astimezone(timezone.utc)
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
            date_max = date_max.astimezone(timezone.utc)
            now = now.astimezone(timezone.utc)
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
    def delete(cls, uuid):
        date= datetime.datetime.now()
        date=date.astimezone(datetime.timezone.utc)
        strDate= date.strftime(date_format)
        auction=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not auction):
            return Message(error="No se pudo eliminar el remate por que no existe")
        auction.removed=1
        auction.dateOfUpdate=strDate
        db.session.merge(auction)
        db.session.commit()
        db.session.close()
        return Message(content="Remate eliminado correctamente")

    @classmethod
    def update(cls, data):
        date= datetime.datetime.now()
        date=date.astimezone(datetime.timezone.utc)
        strDate= date.strftime(date_format)
        auction=cls.query.filter_by(uuid=data["uuid"], removed=0).first()
        if(not auction):
            return Message(error="No se pudo actualizar el remate por que no existe")
        auction.description=data.get("description")
        auction.dateStart= data.get("dateStart")
        auction.company= data.get("company")
        auction.dateOfUpdate=strDate
        db.session.merge(auction)
        db.session.commit()
        auc=A(auction)
        db.session.close()
        return Message(content=auc)

    @classmethod
    def setFinished(cls, uuid):
        date= datetime.datetime.now()
        date=date.astimezone(datetime.timezone.utc)
        strDate= date.strftime(date_format)
        auction=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not auction):
            return Message(error="No se pudo actualizar el remate por que no existe")
        auction.finished=1
        auction.dateOfUpdate=strDate
        db.session.merge(auction)
        db.session.commit()
        auc=A(auction)
        db.session.close()
        return Message(content=auc)
        