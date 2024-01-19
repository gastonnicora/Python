import json
class Article():
    def __init__(cls,data=None,lista:list=[]):
        if data: 
            cls.uuid=data.uuid 
            cls.auction= data.auction
            cls.dateOfCreate=data.dateOfCreate
            cls.dateOfUpdate=data.dateOfUpdate
            cls.before= data.get("before")
            cls.next= data.get("next")
            cls.maxBid= data.get("maxBid")
            cls.description= data.description
            cls.started= data.started
            cls.finished = data.finished
            cls.removed= data.removed
            cls.dateOfStart= data.get("dateOfStart")
            cls.dateOfFinish= data.get("dateOfFinish")
            cls.timeAfterBid= data.get("timeAfterBid")
            cls.tipe= data.tipe
            cls.minValue= data.get("minValue")
            cls.minStepValue= data.get("minStepValue")

        if lista:
            listado=[]
            for i in lista:
                listado.append(Article(i))
            cls.articles= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))