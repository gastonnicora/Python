
import json
from app.helpers.modelosPlanos.permission import Permission

class EmployeePermissions():
    def __init__(cls,data=None, lista=None):
        if data:
            cls.uuid=data.uuid
            cls.employee = data.employee
            cls.permission=data.permission
            cls.dateOfCreate=data.dateOfCreate
            cls.dataPermission= Permission(data.dataPermission)
        cls.employeePermissions=[]
        if lista:
            listado=[]
            for i in lista:
                listado.append(EmployeePermissions(i))
            cls.employeePermissions= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))