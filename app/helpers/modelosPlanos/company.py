import json
class Company():
    def __init__(cls,data=None,lista:list=[]):
        if data: 
            cls.uuid=data.uuid
            cls.name= data.name
            cls.dateOfCreate=data.dateOfCreate
            cls.dateOfUpdate=data.dateOfUpdate
            cls.addres= data.address
            cls.owner= data.owner
            cls.removed= data.removed
        if lista:
            listado=[]
            for i in lista:
                listado.append(Company(i))
            cls.companies= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))