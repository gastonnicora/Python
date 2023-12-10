import json
class Role():
    def __init__(cls,data=None,lista:list=[]):
        if data: 
            cls.uuid=data.uuid
            cls.name= data.name
            cls.dateOfCreate=data.dateOfCreate
            cls.dateOfUpdate=data.dateOfUpdate
            cls.description= data.description
            cls.removed= data.removed
        if lista:
            listado=[]
            for i in lista:
                listado.append(Role(i))
            cls.roles= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))