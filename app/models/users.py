import uuid
import datetime
from werkzeug.security import check_password_hash as checkph
from werkzeug.security import generate_password_hash as genph
from app.helpers.serializacion import Serializacion
from app.models.db import db
from app.helpers.modelosPlanos.user import User  as U
from app.helpers.message import Message



class User(db.Model):
    uuid= db.Column(
        db.String(255), primary_key=True, default=uuid.uuid4, nullable=True, unique=True
        )
    name= db.Column(
        db.String(255),
        nullable= True
        )
    lastName= db.Column(
        db.String(255),
        nullable= True
        )
    email= db.Column(
        db.String(255),
        nullable=True
        )
    password = db.Column(
        db.String(255),
        nullable= True,
    ) 
    birthdate= db.Column(
        db.String(255),
        nullable=True
    )
    removed =db.Column(
        db.Integer,
        nullable=True,
        default=0
    )
    confirmEmail =db.Column(
        db.Integer,
        nullable=True,
        default=0
    )
    dateOfCreate=db.Column(
        db.String(255),
        nullable=True
    )
    terms=db.Column(
        db.Integer,
        nullable=True,
        default=1
    )

    @classmethod
    def create(cls,data):
        date_format = '%d/%m/%Y %H:%M:%S%z'
        date= datetime.datetime.now()
        strDate= date.strftime(date_format)
        usu= cls.existEmail(data.get("email"))
        if usu is not None and usu.confirmEmail == 1:
            return Message(error="El email ya fue registrado")
        if usu is not None and usu.confirmEmail == 0:
            from app.models.confirmEmail import ConfirmEMail
            c=ConfirmEMail.deleteByUser(usu.uuid)
            db.session.delete(usu)
            db.session.commit()
            db.session.close()
        user= cls(
                name= data.get("name"), 
                lastName= data.get("lastName"),
                email= data.get("email"),
                password = genph(data.get("password")), 
                birthdate= data.get("birthdate"), 
                dateOfCreate= strDate
            )
        
        db.session.add(user)
        db.session.commit()
        usuario= U(user)
        db.session.close()
        return Message(content=usuario)
    @classmethod
    def login(cls,data):
        usu= cls.existEmail(data.get("email"))
        
        if not usu  or not  checkph(usu.password, data.get("password")):
            return Message(error="El email o la contraseña son incorrectas")
        if usu is not None and usu.confirmEmail == 0:
            return Message(error="El email no fue validado. Valide el email y vuelva a intentar")
        usuario= U(usu)
        db.session.close()
        return Message(content=usuario)
    
    @classmethod
    def all(cls):
        user=cls.query.filter_by(removed=0).all()  
        users= U(None,user)
        db.session.close()
        return Message(content=users)
    
    @classmethod
    def existEmail(cls,email):
        usuario = cls.query.filter_by(email=email, removed=0).first()
        db.session.close()
        return usuario
    
    @classmethod
    def delete(cls, uuid):
        usuario=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not usuario):
            return Message(error="No se pudo eliminar el usuario por que no existe")
        usuario.removed=1
        db.session.commit()
        db.session.close()
        return Message(content="Usuario eliminado correctamente")
    
    @classmethod
    def confirm(cls,uuid):
        usuario=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not usuario):
            return Message(error="El usuario no existe")
        usuario.confirmEmail=1
        db.session.commit()
        db.session.close()
        return Message(content="El usuario confirmo correctamente su email")