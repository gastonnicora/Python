import json
from app.helpers.modelosPlanos.bid import Bid

class Article():
    def __init__(cls,data=None,lista:list=[]):
        if data: 
            cls.uuid=data.uuid 
            cls.auction= data.auction
            cls.dateOfCreate=data.dateOfCreate
            cls.dateOfUpdate=data.dateOfUpdate
            cls.before= data.before
            cls.next= data.next
            cls.maxBid= data.maxBid
            cls.description= data.description
            cls.started= data.started
            cls.finished = data.finished
            cls.removed= data.removed
            cls.dateOfStart= data.dateOfStart
            cls.dateOfFinish= data.dateOfFinish
            cls.timeAfterBid= data.timeAfterBid
            cls.tipe= data.tipe
            cls.minValue= data.minValue
            cls.minStepValue= data.minStepValue
            cls.maxBid= data.maxBid
            cls.dataBid= Bid(data.dataBid)

        if lista:
            listado=[]
            for i in lista:
                listado.append(Article(i))
            cls.articles= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))