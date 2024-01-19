from app.models.db import db
import uuid
from app.helpers.message import Message
import datetime
from app.helpers.modelosPlanos.role import Role as R


date_format = '%d/%m/%YT%H:%M:%S%z'
class Role(db.Model):
    uuid=db.Column(
        db.String(255), primary_key=True, default=uuid.uuid4, nullable=True, unique=True
        )
    name= db.Column(
        db.String(255),
        nullable=True
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
        role= cls(
                name= data.get("name"),
                description= data.get("description"),
                dateOfCreate= strDate
            )
        db.session.add(role)
        db.session.commit()
        c= R(role)
        db.session.close()
        return Message(content=c)
    
    @classmethod
    def all(cls):
        roles= cls.query.filter_by(removed=0).all()
        rol=R(None,roles)
        db.session.close()
        return Message(content=rol)
    
    @classmethod
    def get(cls,uuid):
        role= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not role):
            return Message(error="No se pudo obtener el rol por que no existe")
        rol=R(role)
        db.session.close()
        return Message(content=rol)
    
    @classmethod
    def delete(cls, uuid):
        date= datetime.datetime.now()
        date=date.astimezone(datetime.timezone.utc)
        strDate= date.strftime(date_format)
        role=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not role):
            return Message(error="No se pudo eliminar el rol por que no existe")
        role.removed=1
        role.dateOfUpdate=strDate
        db.session.merge(role)
        db.session.commit()
        db.session.close()
        return Message(content="Rol eliminado correctamente")

    @classmethod
    def update(cls, data):
        date= datetime.datetime.now()
        date=date.astimezone(datetime.timezone.utc)
        strDate= date.strftime(date_format)
        role=cls.query.filter_by(uuid=data["uuid"], removed=0).first()
        if(not role):
            return Message(error="No se pudo actualizar el rol por que no existe")
        role.name=data.get("name")
        role.description= data.get("description")
        role.dateOfUpdate=strDate
        db.session.merge(role)
        db.session.commit()
        rol= R(role)
        db.session.close()
        return Message(content=rol)
        