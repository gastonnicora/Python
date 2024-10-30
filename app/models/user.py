import uuid
import datetime
from werkzeug.security import check_password_hash as checkph
from werkzeug.security import generate_password_hash as genph
from app.helpers.serializacion import Serializacion
from app.connections.db import db
from app.helpers.modelosPlanos.user import User  as U
from app.helpers.message import Message
from pytz import timezone
from app.helpers.sessions import Sessions
from app.connections.socketio import emit_updateSesion

date_format = '%d/%m/%YT%H:%M:%S%z'
zona_horaria= timezone("America/Argentina/Buenos_Aires")

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
    dateOfUpdate=db.Column(
        db.String(255),
        nullable=True,
        default=None
    )
    terms=db.Column(
        db.Integer,
        nullable=True,
        default=1
    )

    companies = db.relationship('Company', backref="User", lazy=False,
                                primaryjoin="and_(Company.owner==User.uuid, Company.removed==0)")

    @classmethod
    def create(cls,data):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        usu= cls.existEmail(data.get("email"))
        if usu is not None and usu.confirmEmail == 1:
            return Message(error="El email ya fue registrado")
        if usu is not None and usu.confirmEmail == 0:
            return Message(error="El email ya fue registrado. Por favor valide su email")
        user= cls(
                name= data.get("name"), 
                lastName= data.get("lastName"),
                email= data.get("email"),
                password = genph(data.get("password")), 
                birthdate= data.get("birthdate"), 
                dateOfCreate= strDate,
                confirmEmail=1
                
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
    def get(cls,uuid):
        usuario = cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not usuario):
            return Message(error="No se pudo obtener el usuario por que no existe")
        usu= U(usuario)
        db.session.close()
        return Message(content=usu)
    
    @classmethod
    def delete(cls, uuid):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        usuario=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not usuario):
            return Message(error="No se pudo eliminar el usuario por que no existe")
        usuario.removed=1
        usuario.dateOfUpdate=strDate
        db.session.merge(usuario)
        db.session.commit()
        db.session.close()
        from app.models.company import Company
        Company().deleteByOwner(uuid)
        return Message(content="Usuario eliminado correctamente")
    
    @classmethod
    def confirm(cls,uuid):
        usuario=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not usuario):
            return Message(error="El usuario no existe")
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        usuario.dateOfUpdate=strDate
        usuario.confirmEmail=1
        db.session.merge(usuario)
        db.session.commit()
        db.session.close()
        return Message(content="El usuario confirmo correctamente su email")
    
    @classmethod
    def update(cls,uuid,data):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        
        usu= cls.query.filter_by(uuid=uuid, removed=0).first()
        if not usu:
            return Message(error="El usuario no se pudo editar por que no existe")
        if usu.email != data.get("email"):
            usu.confirmEmail=0
        usu.name= data.get("name")
        usu.lastName= data.get("lastName")
        usu.birthdate= data.get("birthdate")
        usu.dateOfUpdate=strDate
        db.session.merge(usu)
        db.session.commit()
        usuario= U(usu)
        db.session.close()
        user= User.get(usu.uuid).dump()["content"]
        Sessions().updateSessionByUser(user["uuid"],user)
        emit_updateSesion(user)
        return Message(content=usuario)
    
    @classmethod
    def updatePassword(cls,uuid,data):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        usu= cls.query.filter_by(uuid=uuid, removed=0).first()
        if not usu:
            return Message(error="El usuario no se pudo editar por que no existe")
        if not  checkph(usu.password, data.get("oldPassword")):
            return Message(error="la contraseña antigua es incorrecta")
        usu.password = genph(data.get("password"))
        usu.dateOfUpdate=strDate
        db.session.commit()
        usuario= U(usu)
        db.session.close()
        return Message(content=usuario)
    
    @classmethod
    def insert_users_in_bulk(cls,users_data):
        date_format = '%d/%m/%YT%H:%M:%S%z'
        zona_horaria = timezone("America/Argentina/Buenos_Aires")

        current_date = datetime.datetime.now().astimezone(zona_horaria)
        strDate = current_date.strftime(date_format)

        users_to_create = []
        for user_data in users_data:
            user = User(
                name=user_data["name"],
                lastName=user_data["lastName"],
                email=user_data["email"],
                password=genph(user_data["password"]),
                birthdate=user_data["birthdate"],
                dateOfCreate=strDate,
                confirmEmail=1  
            )
            users_to_create.append(user)

        db.session.bulk_save_objects(users_to_create)
        db.session.commit()
        db.session.close()
        print(f"{len(users_to_create)} usuarios insertados correctamente.")
