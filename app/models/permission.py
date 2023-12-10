from app.models.db import db
import uuid
from app.helpers.message import Message
import datetime
from app.helpers.modelosPlanos.permission import Permission as R


date_format = '%d/%m/%Y %H:%M:%S%z'
class Permission(db.Model):
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
        date_format = '%d/%m/%Y %H:%M:%S%z'
        date= datetime.datetime.now()
        strDate= date.strftime(date_format)
        permission= cls(
                name= data.get("name"),
                description= data.get("description"),
                dateOfCreate= strDate
            )
        db.session.add(permission)
        db.session.commit()
        c= R(permission)
        db.session.close()
        return Message(content=c)
    
    @classmethod
    def all(cls):
        permissions= cls.query.filter_by(removed=0).all()
        rol=R(None,permissions)
        db.session.close()
        return Message(content=rol)
    
    @classmethod
    def get(cls,uuid):
        permission= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not permission):
            return Message(error="No se pudo obtener el permiso por que no existe")
        rol=R(permission)
        db.session.close()
        return Message(content=rol)
    
    @classmethod
    def delete(cls, uuid):
        date= datetime.datetime.now()
        strDate= date.strftime(date_format)
        permission=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not permission):
            return Message(error="No se pudo eliminar el permiso por que no existe")
        permission.removed=1
        permission.dateOfUpdate=strDate
        db.session.merge(permission)
        db.session.commit()
        db.session.close()
        return Message(content="Permiso eliminado correctamente")

    @classmethod
    def update(cls, data):
        date= datetime.datetime.now()
        strDate= date.strftime(date_format)
        permission=cls.query.filter_by(uuid=data["uuid"], removed=0).first()
        if(not permission):
            return Message(error="No se pudo actualizar el permiso por que no existe")
        permission.name=data.get("name")
        permission.description= data.get("description")
        permission.dateOfUpdate=strDate
        db.session.merge(permission)
        db.session.commit()
        rol= R(permission)
        db.session.close()
        return Message(content=rol)
        