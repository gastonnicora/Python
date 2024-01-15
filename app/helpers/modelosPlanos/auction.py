import json
class Auction():
    def __init__(cls,data=None,lista:list=[]):
        if data: 
            cls.uuid=data.uuid
            cls.description= data.description
            cls.dateOfCreate=data.dateOfCreate
            cls.dateOfUpdate=data.dateOfUpdate
            cls.company= data.company
            cls.dateStart= data.dateStart
            cls.removed= data.removed
            cls.finished= data.finished
        if lista:
            listado=[]
            for i in lista:
                listado.append(Auction(i))
            cls.auctions= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))