import json
from app.helpers.modelosPlanos.company import Company
from app.helpers.modelosPlanos.article import Article
class Auction():
    def __init__(cls,data=None,lista:list=[], simplify:bool=False):
        if data and not lista: 
            cls.uuid=data.uuid
            cls.description= data.description
            cls.company= data.company
            cls.dateStart= data.dateStart
            cls.dateFinish= data.dateFinish
            cls.dataCompany= Company(data.dataCompany)
            cls.type= data.type
            if not simplify:
                cls.removed= data.removed
                cls.finished= data.finished
                cls.articles= Article(lista=data.articles)
                cls.dateOfCreate=data.dateOfCreate
                cls.dateOfUpdate=data.dateOfUpdate
                cls.timeAfterBid= data.timeAfterBid

        cls.auctions=[]
        if lista and not data:
            listado=[]
            for i in lista:
                listado.append(Auction(i),None,True)
            cls.auctions= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))
    
    def basic(cls):
        if cls.auctions:
            listado=[]
            for auction in cls.auctions:
                listado.append({"uuid":auction.uuid,"description":auction.description,
                "dateStart":auction.dateStart,"dataCompany":auction.dataCompany,
                 "type":auction.type,"dateFinish":auction.dateFinish })
            return 