import json
class Permission():
    def __init__(cls,data=None,lista:list=[]):
        if data: 
            cls.uuid=data.uuid
            cls.name= data.name
            cls.url= data.url
            cls.dateOfCreate=data.dateOfCreate
            cls.dateOfUpdate=data.dateOfUpdate
            cls.description= data.description
            cls.removed= data.removed
        if lista:
            listado=[]
            for i in lista:
                listado.append(Permission(i))
            cls.permissions= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))