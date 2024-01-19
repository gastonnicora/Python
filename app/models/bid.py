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
    User= db.Column(
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
    def create(cls,data, userUuid):
        date= datetime.datetime.now()
        date=date.astimezone(datetime.timezone.utc)
        strDate= date.strftime(date_format)
        company= cls(
                owner=userUuid,
                name= data.get("name"),
                address= data.get("address"),
                dateOfCreate= strDate
            )
        db.session.add(company)
        db.session.commit()
        c= B(company)
        db.session.close()
        return Message(content=c)
    
    @classmethod
    def all(cls):
        companies= cls.query.filter_by(removed=0).all()
        com=B(None,companies)
        db.session.close()
        return Message(content=com)
    
    @classmethod
    def get(cls,uuid):
        company= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not company):
            return Message(error="No se pudo obtener la empresa por que no existe")
        com=B(company)
        db.session.close()
        return Message(content=com)
    
    @classmethod
    def delete(cls, uuid):
        date= datetime.datetime.now()
        date=date.astimezone(datetime.timezone.utc)
        strDate= date.strftime(date_format)
        company=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not company):
            return Message(error="No se pudo eliminar la empresa por que no existe")
        company.removed=1
        company.dateOfUpdate=strDate
        db.session.merge(company)
        db.session.commit()
        db.session.close()
        return Message(content="Empresa eliminada correctamente")

    @classmethod
    def update(cls, data):
        date= datetime.datetime.now()
        date=date.astimezone(datetime.timezone.utc)
        strDate= date.strftime(date_format)
        company=cls.query.filter_by(uuid=data["uuid"], removed=0).first()
        if(not company):
            return Message(error="No se pudo actualizar la empresa por que no existe")
        company.name=data.get("name")
        company.address= data.get("address")
        company.dateOfUpdate=strDate
        db.session.merge(company)
        db.session.commit()
        com=B(company)
        db.session.close()
        return Message(content=com)
        