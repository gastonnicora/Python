import json
from app.helpers.modelosPlanos.company import Company
from app.helpers.modelosPlanos.article import Article
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
            cls.dataCompany= Company(data.dataCompany)
            cls.articles= Article(lista=data.articles)
            cls.type= data.type
            cls.dateFinish= data.dateFinish
            cls.timeAfterBid= data.timeAfterBid
        cls.auctions=[]
        if lista:
            listado=[]
            for i in lista:
                listado.append(Auction(i))
            cls.auctions= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))
    
    def basic(cls):
        return {"uuid":cls.uuid,"description":cls.description,
                "dateStart":cls.dateStart,"dataCompany":cls.dataCompany,
                 "type":cls.type,"dateFinish":cls.dateFinish }