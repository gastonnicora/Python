import json
from app.helpers.modelosPlanos.company import Company
class User():
    def __init__(cls,data=None,lista=None):
        if data: 
            cls.uuid=data.uuid
            cls.name= data.name
            cls.lastName=data.lastName
            cls.email=data.email
            cls.birthdate= data.birthdate
            cls.removed = data.removed
            cls.dateOfCreate=data.dateOfCreate
            cls.dateOfUpdate=data.dateOfUpdate
            cls.terms=data.terms
            cls.confirmEmail= data.confirmEmail
            cls.companies = Company(lista=data.companies)
        cls.users=[]
        if lista:
            listado=[]
            for i in lista:
                listado.append(User(i))
            cls.users= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))
    