import json
from app.helpers.modelosPlanos.user import User
class Bid():
    def __init__(cls,data=None,lista:list=[]):
        if data: 
            cls.uuid=data.uuid
            cls.dateOfCreate=data.dateOfCreate
            cls.dateOfUpdate=data.dateOfUpdate
            cls.removed= data.removed
            cls.user= data.user
            cls.value= data.value
            cls.article= data.article
            cls.dataUser= User(data.dataUser)
        cls.bids=[]
        if lista:
            listado=[]
            for i in lista:
                listado.append(Bid(i))
            cls.bids= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))

    def to_dict(self):
        return {
            'uuid': self.uuid,
            'dateOfCreate': self.dateOfCreate,
            'dateOfUpdate': self.dateOfUpdate,
            'removed': self.removed,
            'user': self.user,
            'value': self.value,
            'article': self.article,
            'dataUser': self.dataUser.to_dict() if self.dataUser else None,
            'bids': [bid.to_dict() for bid in self.bids]
        }