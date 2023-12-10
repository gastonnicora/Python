
import json
class EmployeePermissions():
    def __init__(cls,data=None, lista=None):
        if data:
            cls.uuid=data.uuid
            cls.employee = data.employee
            cls.permission=data.permission
            cls.dateOfCreate=data.dateOfCreate
        if lista:
            listado=[]
            for i in lista:
                listado.append(EmployeePermissions(i))
            cls.confirmEmail= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))