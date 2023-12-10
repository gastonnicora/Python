import json
class Employee():
    def __init__(cls,data=None,lista=None):
        if data: 
            cls.uuid=data.uuid
            cls.user=data.user
            cls.company=data.company
            cls.dateOfCreate=data.dateOfCreate
            cls.dateOfUpdate=data.dateOfUpdate
        if lista:
            listado=[]
            for i in lista:
                listado.append(Employee(i))
            cls.employees= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))