from app.models.db import db
from sqlalchemy.sql.schema import ForeignKey
import uuid
from app.helpers.message import Message
from app.models.user import User
from app.models.company import Company
import datetime
from app.helpers.modelosPlanos.employee import Employee as C


date_format = '%d/%m/%YT%H:%M:%S%z'
class Employee(db.Model):
    uuid=db.Column(
        db.String(255), primary_key=True, default=uuid.uuid4, nullable=True, unique=True
        )
    user= db.Column(
        db.String(255),
        ForeignKey(User.uuid),
        nullable= True
    ) 
    user= db.Column(
        db.String(255),
        ForeignKey(User.uuid),
        nullable= True
    ) 
    company= db.Column(
        db.String(255),
        ForeignKey(Company.uuid),
        nullable= True
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
        employee= cls(
                user= data.get("user"),
                company= data.get("company"),
                dateOfCreate= strDate
            )
        db.session.add(employee)
        db.session.commit()
        c= C(employee)
        db.session.close()
        return Message(content=c)
    
    @classmethod
    def all(cls):
        companies= cls.query.filter_by(removed=0).all()
        con=C(None,companies)
        db.session.close()
        return Message(content=con)
    
    @classmethod
    def get(cls,uuid):
        employee= cls.query.filter_by(uuid=uuid,removed=0).first()
        if(not employee):
            return Message(error="No se pudo obtener la relación empleado/empresa por que no existe")
        con=C(employee)
        db.session.close()
        return Message(content=con)

    @classmethod
    def getByUser(cls,user):
        employee= cls.query.filter_by(user=user,removed=0).all()
        if(not employee):
            return Message(error="No se pudo obtener la relación empleado/empresa por que no existe")
        con=C(lista=employee)
        db.session.close()
        return Message(content=con)

    @classmethod
    def getByCompany(cls,company):
        employee= cls.query.filter_by(company=company,removed=0).all()
        if(not employee):
            return Message(error="No se pudo obtener la relación empleado/empresa por que no existe")
        con=C(lista=employee)
        db.session.close()
        return Message(content=con)
    
    @classmethod
    def delete(cls, uuid):
        date= datetime.datetime.now()
        date=date.astimezone(datetime.timezone.utc)
        strDate= date.strftime(date_format)
        employee=cls.query.filter_by(uuid=uuid, removed=0).first()
        if(not employee):
            return Message(error="No se pudo eliminar la relación empleado/empresa por que no existe")
        employee.removed=1
        employee.dateOfUpdate=strDate
        db.session.merge(employee)
        db.session.commit()
        db.session.close()
        return Message(content="Relación empleado/empresa eliminada correctamente")
    
    @classmethod
    def deleteByUser(cls,uuid):
        employees= cls.query.filter_by(user=uuid,removed=0).all()
        if(not employees):
            return Message(error="No se pudo obtener la relación empleado/empresa por que no existe")
        for i in employees:
            cls.delete(i.uuid)
        db.session.close()
        return Message(content="Relaciones empleado/empresa eliminadas correctamente")
    
    @classmethod
    def deleteByCompany(cls,uuid):
        employees= cls.query.filter_by(company=uuid,removed=0).all()
        if(not employees):
            return Message(error="No se pudo obtener la relación empleado/empresa por que no existe")
        for i in employees:
            cls.delete(i.uuid)
        db.session.close()
        return Message(content="Relaciones empleado/empresa eliminadas correctamente")

    @classmethod
    def update(cls, data):
        date= datetime.datetime.now()
        date=date.astimezone(datetime.timezone.utc)
        strDate= date.strftime(date_format)
        employee=cls.query.filter_by(uuid=data["uuid"], removed=0).first()
        if(not employee):
            return Message(error="No se pudo actualizar la relación empleado/empresa por que no existe")
        employee.name=data.get("name")
        employee.address= data.get("address")
        employee.dateOfUpdate=strDate
        db.session.merge(employee)
        db.session.commit()
        c= C(employee)
        db.session.close()
        return Message(content=c)
    
    
        