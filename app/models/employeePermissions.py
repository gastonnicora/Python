from app.models.db import db
from sqlalchemy.sql.schema import ForeignKey
import uuid
from app.helpers.message import Message
import datetime
from app.helpers.modelosPlanos.employeePermissions import EmployeePermissions as R
from app.models.employee import Employee
from app.models.permission import Permission
from pytz import timezone
from sqlalchemy.orm import relationship

date_format = '%d/%m/%YT%H:%M:%S%z'
zona_horaria= timezone("America/Argentina/Buenos_Aires")
class EmployeePermissions(db.Model):
    uuid=db.Column(
        db.String(255), primary_key=True, default=uuid.uuid4, nullable=True, unique=True
        )
    employee= db.Column(
        db.String(255),
        ForeignKey(Employee.uuid),
        nullable= True
    )
    permission= db.Column(
        db.String(255),
        ForeignKey(Permission.uuid),
        nullable= True
    )
    dataPermission = relationship(Permission, foreign_keys=[permission])
    dateOfCreate=db.Column(
        db.String(255),
        nullable=True
    )
    dateOfUpdate=db.Column(
        db.String(255),
        nullable=True
    )

    @classmethod
    def create(cls,data, userUuid):
        date= datetime.datetime.now()
        date=date.astimezone(zona_horaria)
        strDate= date.strftime(date_format)
        sms=  Employee.get(data.get("employee"))
        if sms.dump()["error"]:
            return Message(error="No se puede crear la relación empleado/permisos por que no existe el empleado")
        sms=  Permission.get(data.get("permission"))
        if sms.dump()["error"]:
            return Message(error="No se puede crear la relación empleado/permisos por que no existe el permiso")
        employeePermissions= cls(
                employee= data.get("employee"),
                permission= data.get("permission"),
                dateOfCreate= strDate
            )
        db.session.add(employeePermissions)
        db.session.commit()
        c= R(employeePermissions)
        db.session.close()
        return Message(content=c)
    
    @classmethod
    def all(cls):
        employeePermissions= cls.query.filter_by().all()
        rol=R(None,employeePermissions)
        db.session.close()
        return Message(content=rol)
    
    @classmethod
    def get(cls,uuid):
        employeePermissions= cls.query.filter_by(uuid=uuid).first()
        if(not employeePermissions):
            return Message(error="No se pudo obtener la relación permiso/empleado por que no existe")
        rol=R(employeePermissions)
        db.session.close()
        return Message(content=rol)
    
    @classmethod
    def delete(cls, uuid):
        employeePermissions=cls.query.filter_by(uuid=uuid).first()
        if(not employeePermissions):
            return Message(error="No se pudo eliminar la relación permiso/empleado por que no existe")
        db.session.delete(employeePermissions)
        db.session.commit()
        db.session.close()
        return Message(content="Relación permiso/empleado  eliminado correctamente")

    
        