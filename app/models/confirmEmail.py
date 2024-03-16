from app.models.db import db
from sqlalchemy.sql.schema import ForeignKey
import uuid
from app.helpers.message import Message
from app.models.user import User
import datetime
from app.helpers.modelosPlanos.confirmEmail import ConfirmEmail as C
from pytz import timezone

date_format = '%d/%m/%YT%H:%M:%S%z'
zona_horaria= timezone("America/Argentina/Buenos_Aires")

class ConfirmEMail(db.Model):
    uuid=db.Column(
        db.String(255), primary_key=True, default=uuid.uuid4, nullable=True, unique=True
        )
    user= db.Column(
        db.String(255),
        ForeignKey(User.uuid),
        nullable= True
    ) 
    dateOfCreate=db.Column(
        db.String(255),
        nullable=True
    )

    @classmethod
    def create(cls,user):
        date_format = '%d/%m/%Y %H:%M:%S%z'
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        sms=  User.get(user)
        if sms.dump()["error"]:
            return Message(error="No se puede guardar confirmación por que no existe el usuario")
        confirm= cls(
                user=user,
                dateOfCreate= strDate
            )
        
        db.session.add(confirm)
        db.session.commit()
        c= C(confirm)
        db.session.close()
        return Message(content=c)
    

    @classmethod
    def delete(cls,uuid):
        confirm=cls.query.filter_by(uuid = uuid).first()
        if(not confirm):
            return Message(error="No se puede borrar por que no existe")
        db.session.delete(confirm)
        db.session.commit()
        db.session.close()
        return Message(content="Eliminado con éxito")
    
    @classmethod
    def deleteByUser(cls,user):
        confirm=cls.query.filter_by(user = user).first()
        if(not confirm):
            return Message(error="No se puede borrar por que no existe")
        db.session.delete(confirm)
        db.session.commit()
        db.session.close()
        return Message(content="Eliminado con éxito")
    
    @classmethod
    def get(cls,uuid):
        confirm=cls.query.filter_by(uuid = uuid).first()
        if(confirm is None):
             return Message(error="No se puede confirmar el email por que ya pasaron mas de 24 horas de la creación de la cuenta ")
        c= C(confirm)
        db.session.close()
        return Message(content=c)
    @classmethod
    def all(cls):
        confirm= cls.query.filter_by().all() 
        con=C(None,confirm)
        db.session.close()
        return Message(content=con)