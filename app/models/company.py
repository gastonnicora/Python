from app.models.db import db
from sqlalchemy.sql.schema import ForeignKey
import uuid
from app.helpers.message import Message
from app.models.user import User
import datetime
from app.helpers.modelosPlanos.company import Company as C
from pytz import timezone
from app.helpers.sessions import Sessions
from app.socket.socketio import emit_updateSesion

date_format = '%d/%m/%YT%H:%M:%S%z'
zona_horaria= timezone("America/Argentina/Buenos_Aires")
class Company(db.Model):
    uuid=db.Column(
        db.String(255), primary_key=True, default=uuid.uuid4, nullable=True, unique=True
        )
    owner= db.Column(
        db.String(255),
        ForeignKey(User.uuid),
        nullable= True
    ) 
    name= db.Column(
        db.String(255),
        nullable=True
    )
    address=db.Column(
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
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        sms=  User.get(userUuid)
        if sms.dump()["error"]:
            return Message(error="No se puede crear la compañía por que no existe el usuario")
        company= cls(
                owner=userUuid,
                name= data.get("name"),
                address= data.get("address"),
                dateOfCreate= strDate
            )
        db.session.add(company)
        db.session.commit()
        c= C(company)
        user= User.get(userUuid).dump()["content"]
        Sessions().updateSessionByUser(user["uuid"],user)
        emit_updateSesion(user)
        db.session.close()

        return Message(content=c)
    @classmethod
    def insert_company_in_bulk(cls,companies_data):
        date_format = '%d/%m/%YT%H:%M:%S%z'
        zona_horaria = timezone("America/Argentina/Buenos_Aires")

        current_date = datetime.datetime.now().astimezone(zona_horaria)
        strDate = current_date.strftime(date_format)

        companies_to_create = []
        for company_data in companies_data:
            company= cls(
                owner=company_data["user"],
                name= company_data["name"],
                address= company_data["address"],
                dateOfCreate= strDate
            )
            companies_to_create.append(company)

        db.session.bulk_save_objects(companies_to_create)
        db.session.commit()
        db.session.close()
        print(f"{len(companies_to_create)} empresas insertados correctamente.")
    
    @classmethod
    def all(cls):
        companies= cls.query.filter_by(removed=0).all()
        com=C(None,companies)
        db.session.close()
        return Message(content=com)
    
    @classmethod
    def get(cls,uuid):
        company= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not company):
            return Message(error="No se pudo obtener la empresa por que no existe")
        com=C(company)
        db.session.close()
        return Message(content=com)
    
    @classmethod
    def delete(cls, uuid,owner):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        company=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not company):
            return Message(error="No se pudo eliminar la empresa por que no existe")
        if(company.owner != owner):
            return Message(error="No se pudo eliminar la empresa por que no sos el dueño de la empresa")
        company.removed=1
        company.dateOfUpdate=strDate
        db.session.merge(company)
        from app.models.auction import Auction
        Auction().deleteByCompany(company.uuid)
        db.session.commit()
        db.session.close()
        user= User.get(owner).dump()["content"]
        Sessions().updateSessionByUser(user["uuid"],user)
        emit_updateSesion(user)
        return Message(content="Empresa eliminada correctamente")
    
    @classmethod
    def deleteByOwner(cls,owner):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        companies=cls.query.filter_by(owner=owner, removed=0).all()
        from app.models.auction import Auction
        for company in companies:
            company.removed=1
            company.dateOfUpdate=strDate
            Auction().deleteByCompany(company.uuid)
            db.session.merge(auction)
        db.session.commit()
        db.session.close()
        user= User.get(owner).dump()["content"]
        Sessions().updateSessionByUser(user["uuid"],user)
        emit_updateSesion(user)
        return Message(content="Empresas eliminadas correctamente")


    @classmethod
    def update(cls, data,owner):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        company=cls.query.filter_by(uuid=data["uuid"], removed=0).first()
        if(not company):
            return Message(error="No se pudo actualizar la empresa por que no existe")
        if(company.owner != owner):
            return Message(error="No se pudo actualizar la empresa por que no sos el dueño de la empresa")
        company.name=data.get("name")
        company.address= data.get("address")
        company.dateOfUpdate=strDate
        db.session.merge(company)
        db.session.commit()
        com=C(company)
        db.session.close()
        user= User.get(company.owner).dump()["content"]
        Sessions().updateSessionByUser(user["uuid"],user)
        emit_updateSesion(user)
        return Message(content=com)
        