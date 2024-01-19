import json
class Bid():
    def __init__(cls,data=None,lista:list=[]):
        if data: 
            cls.uuid=data.uuid
            cls.dateOfCreate=data.dateOfCreate
            cls.dateOfUpdate=data.dateOfUpdate
            cls.removed= data.removed
        if lista:
            listado=[]
            for i in lista:
                listado.append(Bid(i))
            cls.bids= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))