from app.models.article import Article
from app.models.auction import Auction
from app.models.bid import Bid
from app.models.company import Company
from app.models.user import User
import datetime
from pytz import timezone
import logging
import uuid

from random import randint, randrange

date_format = '%d/%m/%YT%H:%M:%S%z'
zona_horaria= timezone("America/Argentina/Buenos_Aires")

date= datetime.datetime.now()
date=date.astimezone(zona_horaria)
strDate= date.strftime(date_format)


articlesList=[
    {
        "description": "Juego de llaves desde 8 a 22",
        "urlPhoto": "https://http2.mlstatic.com/D_NQ_NP_860631-MLA49061077232_022022-O.webp"
    },
    {
        "description": "Martillos",
        "urlPhoto": "https://blogger.googleusercontent.com/img/b/R29vZ2xl/AVvXsEhwVwfAW8LeDN57UZ20vHdaGXZmcXWLtonHVMFkG8FrA16km1Bf6CcTEamDgUm5-CxDiIyr3kbYKD8LhjP7bOUXS9QA9TQXhq8_QM1ySKzY7Ks5arqr4TlvYGUiNcVDic2q1ebMZLt4LivY/s1600/tipos-de-martillos.jpg"
    },
    {
        "description": "Camioneta dodge ram 2024 roja",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRYfaF8FAY06uhmIZNbAzpIImPu2m9pF6jaBFEhxGn-hA&s"
    },
    {
        "description": "Un año de gasoil",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEpHBtRoJh3R1lSUFZU4QKbdm1Ff1xhvgpsl0nj1OkqA&s"
    },
    {
        "description": "Casa quinta en 25 de Mayo",
        "urlPhoto": "https://cristinaleonpropiedades.com/uploads/cristinaleonpropiedades/images/1632118067x85zt-whatsapp-image-2020-11-21-at-094742-1.jpeg"
    },
    {
        "description": "Botellas antiguas",
        "urlPhoto": "https://http2.mlstatic.com/D_NQ_NP_776348-MLA53686471413_022023-O.webp"
    },
    {
        "description": "Botellas de licor de frutillas",
        "urlPhoto": "https://statics.dinoonline.com.ar/imagenes/full_600x600_ma/3070252_f.jpg"
    },
    {
        "description": "Tractor jonh deere 3420",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSZSVbXQloJTHnq0yg0cRzm7sKRPOp4HJlK_DlJvzaQ_g&s"
    },
    {
        "description": "Tractor deutz 55",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSSooeKp3_0Ps31hcez0sXk6rMewQVY64Zto5Fg5wysDg&s"
    },
    {
        "description": "Tractor deutz 85",
        "urlPhoto": "https://argentina.agrofystatic.com/media/catalog/product/cache/850x600/d/e/deutz-85-2114-Agro-Ventas-Hernandez-agrofy-2-20230721121932.png"
    },
    {
        "description": "Florero antiguo",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT5zwu-5Q3Yr76IkuRLDgQKfhyqZ9Wfb6qZz744nG8X5Q&s"
    },
    {
        "description": "Cuadro de elefante",
        "urlPhoto": "https://http2.mlstatic.com/D_NQ_NP_707341-MLA51062310657_082022-O.webp"
    },
    {
        "description": "Cuadro retro",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSh3k6dVtF9wlXRUteV_4qWDq638OWTs7k0uz6iLVyb4Q&s"
    },
    {
        "description": "Cocina usada",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTLjoVH9M2td71B42HGAp5p7-Kh-lib-BvtLXNVJU23zw&s"
    },
    {
        "description": "Casa de madera para que jueguen los niños",
        "urlPhoto": "https://http2.mlstatic.com/D_NQ_NP_699415-MLU71758413073_092023-O.webp"
    },
    {
        "description": "Juguetes",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT6FdgVtavOxzALuPlf2RxNwNOeIjeImsww8fxlFG1Rdg&s"
    },
    {
        "description": "Caballo bayo de andar",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTXwtxnq7wd-nSKRM6Oxr5LdJS4PDtqpkcM1a-ZqQd1rw&s"
    },
    {
        "description": "Caballo alazán redomon",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQt_jbW-mrtamI-sVJ8kR7YB0Akr-cdX3otecrhhTCJtA&s"
    },
    {
        "description": "Recado nuevo",
        "urlPhoto": "https://http2.mlstatic.com/D_NQ_NP_903347-MLA71045918077_082023-O.webp"
    },
    {
        "description": "Cuchillo 12 cm",
        "urlPhoto": "https://http2.mlstatic.com/D_NQ_NP_974220-MLA43916047119_102020-O.webp"
    },
    {
        "description": "Llave francesa bahco 18",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQi3oaP3cINlD6PJzhrwPFoDlRdB80KsupPK1O3dH7l&s"
    },
    {
        "description": "Taladro eléctrico usado",
        "urlPhoto": "https://http2.mlstatic.com/D_NQ_NP_602169-MLA75318768115_032024-O.webp"
    },
    {
        "description": "Cortadora de pasto usada",
        "urlPhoto": "https://http2.mlstatic.com/D_NQ_NP_775782-MLA76181659104_052024-O.webp"
    },
    {
        "description": "Motoguadaña usada",
        "urlPhoto": "https://http2.mlstatic.com/D_NQ_NP_754307-MLA53944730967_022023-O.webp"
    },
    {
        "description": "Destornilladores",
        "urlPhoto": "https://http2.mlstatic.com/D_NQ_NP_749356-MLA69333993028_052023-O.webp"
    },
    {
        "description": "10 chapas",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTYDZWOBMGP82XgVMOv_Usmhypsn_qetm491DVf7miA2g&s"
    },
    {
        "description": "Comederos para gallinas",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQxKfDl2iBTIqi9JLOVPYvxkPMhKAwenop1DIQo9fMzsg&s"
    },
    {
        "description": "Ventilados antiguo",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUFIeDa6ghRX4t6FjFhrfv2hbkbwcXUOru3EI7O9d94w&s"
    },
    {
        "description": "Notebook lenovo",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQYXkpfq3RqS04Ef48ESwvNKEmCXhLxGCjUwUmy4tZalg&s"
    },
    {
        "description": "Pala de punta",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSUA9QE5Hy-I8i6Mg0lWRCKrZ0p4pfFzUqAwufkPsU8Lg&s"
    },
    {
        "description": "Vasos de vidrio",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQEithsq4tsG67bvXEgbC3xugHapZlqII4C17kPDV0jeA&s"
    },
    {
        "description": "Copas de cristal",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRY_0tLpILjIlwk5Pd3nHz15IPmi9uK3qyBPZrcLcqGCA&s"
    },
    {
        "description": "Revistas antiguas",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSvwkaGM7uKdXuQes3jnrPybXbpo31zXANV64R-tQR1Uw&s"
    },
    {
        "description": "Plafones de techo antiguos",
        "urlPhoto": "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSEZ3uFKK6abqrqzo0PhNL6yE1qSrgn9nDy2zqp2357xQ&s"
    }
    ]
auctionsList =[
    {
        "description":"Gran remate de artículos varios"
    },
    {
        "description":"Gran remate de muchos artículos en excelente estado"
    },
    {
        "description":"Gran remate con excelentes ofertas"
    },
]
companiesList=[
  {
    "name": "Company A",
    "address": "123 Main St"
  },
  {
    "name": "Company B",
    "address": "456 Elm St"
  },
  {
    "name": "Company C",
    "address": "789 Oak St"
  },
  {
    "name": "Company D",
    "address": "321 Maple St"
  },
  {
    "name": "Company E",
    "address": "654 Pine St"
  },
  {
    "name": "Company F",
    "address": "987 Cedar St"
  },
  {
    "name": "Company G",
    "address": "159 Birch St"
  },
  {
    "name": "Company H",
    "address": "753 Walnut St"
  },
  {
    "name": "Company I",
    "address": "246 Spruce St"
  },
  {
    "name": "Company J",
    "address": "580 Fir St"
  }
]
usersList=[
  {
    "name": "John",
    "lastName": "Doe",
    "birthdate": "01/01/1990",
    "password": "password1",
    "repetitionPass": "password1",
    "email": "john.doe@example.com"
  },

  {
    "name": "Usuario",
    "lastName": "Usuario",
    "birthdate": "01/01/1990",
    "password": "12345678",
    "repetitionPass": "12345678",
    "email": "usuario@example.com"
  },
  {
    "name": "Jane",
    "lastName": "Smith",
    "birthdate": "02/02/1995",
    "password": "password2",
    "repetitionPass": "password2",
    "email": "jane.smith@example.com"
  },
  {
    "name": "Michael",
    "lastName": "Johnson",
    "birthdate": "03/03/1988",
    "password": "password3",
    "repetitionPass": "password3",
    "email": "michael.johnson@example.com"
  },
  {
    "name": "Emily",
    "lastName": "Brown",
    "birthdate": "04/04/1992",
    "password": "password4",
    "repetitionPass": "password4",
    "email": "emily.brown@example.com"
  },
  {
    "name": "David",
    "lastName": "Taylor",
    "birthdate": "05/05/1985",
    "password": "password5",
    "repetitionPass": "password5",
    "email": "david.taylor@example.com"
  },
  {
    "name": "Olivia",
    "lastName": "Miller",
    "birthdate": "06/06/1993",
    "password": "password6",
    "repetitionPass": "password6",
    "email": "olivia.miller@example.com"
  },
  {
    "name": "James",
    "lastName": "Anderson",
    "birthdate": "07/07/1989",
    "password": "password7",
    "repetitionPass": "password7",
    "email": "james.anderson@example.com"
  },
  {
    "name": "Sophia",
    "lastName": "Wilson",
    "birthdate": "08/08/1991",
    "password": "password8",
    "repetitionPass": "password8",
    "email": "sophia.wilson@example.com"
  },
  {
    "name": "Benjamin",
    "lastName": "Thomas",
    "birthdate": "09/09/1987",
    "password": "password9",
    "repetitionPass": "password9",
    "email": "benjamin.thomas@example.com"
  },
  {
    "name": "Ava",
    "lastName": "Clark",
    "birthdate": "10/10/1994",
    "password": "password10",
    "repetitionPass": "password10",
    "email": "ava.clark@example.com"
  }
]


def initialize():
    u= len(User.all().content.users)
    au=len(Auction.all().content.auctions)
    ar= len(Article.all().content.articles)
    co=len(Company.all().content.companies)
    bi= len(Bid.all().content.bids)
    if not (u==0 and au==0 and ar==0 and co==0 and bi==0):
        return

    logging.info('Creando  usuarios')

    User.insert_users_in_bulk(usersList)
    users= User.all().content.users

    logging.info('Creando  empresas')
    company= []
    lenUser=len(users)
    for i, com in enumerate(companiesList):
        num=randint(0, lenUser-1)
        com["user"]=users[num].uuid
        company.append(com)
    Company.insert_company_in_bulk(company)
    companies= Company.all().content.companies

    listAuction=[]
    logging.info('Creando  remates')
    lenCompanies=len(companies)
    lenAuctions= len(auctionsList)
    for i in range(0,randrange(10, lenCompanies*10)):
        a=randint(0,lenAuctions -1)
        num=randint(0, lenCompanies-1)
        data= auctionsList[a]
        data["company"]= companies[num].uuid
        data["type"]= randint(0, 1)
        data["timeAfterBid"]= randint(10, 60)
        minutesS= randint(-1000, 1000)
        minutesF = randint(100, 1000) + minutesS 
        dateS=date + datetime.timedelta(minutes = minutesS)
        dateF=date + datetime.timedelta(minutes = minutesF)
        dateF= dateF.astimezone(zona_horaria)
        data["dateFinish"]= dateF.strftime(date_format)
        dateS= dateS.astimezone(zona_horaria)
        data["dateStart"]= dateS.strftime(date_format)
        listAuction.append(data)
    Auction.insert_auction_in_bulk(listAuction)
    listAuction= Auction.all().content.auctions

    logging.info('Creando  articulos')

    listArticle=[]   
    num=len(listAuction)-1

    now= datetime.datetime.now()
    now=now.astimezone(zona_horaria)
    lenArticles =len(articlesList)
    auxArticle={}
    uuids=set()
    for i in range(0,randrange(num*5, 20*num)):
        au=randint(0, (num-1))
        a=randint(0, lenArticles -1)
        auction= listAuction[au]
        data= articlesList[a]
        u=str(uuid.uuid4())
        while u in uuids:
            logging.info('uuid repetido '+ u)
            u=str(uuid.uuid4())
            logging.info('uuid nuevo '+ u)
        
        logging.info('uuid in '+ str(u in uuids))
        logging.info('uuid nuevo '+ u)
        uuids.add(u)
        data["uuid"]=u
        data["auction"]= auction.uuid
        data["dateOfStart"]= auction.dateStart
        data["dateOfFinish"]= auction.dateFinish
        data["minValue"]=randint(1000, 100000)
        data["minStepValue"]=randint(1000, 100000)
        data["type"]= auction.type
        data["timeAfterBid"]= auction.timeAfterBid
        data["next"]=None
        data["before"]=None
        # if auxArticle.get(data["auction"]) != None:
        #     tam=len(auxArticle[data["auction"]])
        #     uuidB,index= next(iter(auxArticle[data["auction"]][tam-1].items()))
        #     listArticle[index]["next"]= data["uuid"]
        #     data["before"]=uuidB
        #     auxArticle[data["auction"]].append({data["uuid"]:i})
        # else:
        #     auxArticle[data["auction"]]=[{data["uuid"]:i}]
        listArticle.append(data)

    logging.info('uuids: ' + str(len(uuids)))
    logging.info('articles: ' + str(len(listArticle)))
    Article.insert_article_in_bulk(listArticle)
    listArticle = Article.getFinished().content.articles
    
    if len(listArticle) >0:
        logging.info('Creando pujas')
        bids=[]
        lenArticles = len(listArticle)
        auxBid={}
        uuids=[]
        for i in range(0,randrange(0, (5*(lenArticles-1)) )) :
            art= randint(0,lenArticles-1) 
            user= randint(0,lenUser-1) 
            u=str(uuid.uuid4())
            while u in uuids:
                u=str(uuid.uuid4())
            uuids.append(u)
            data={"article":listArticle[art].uuid}
            data["uuid"]= u
            data["user"]=user
            if listArticle[art].bidValue:
                data["value"]=listArticle[art].bidValue + listArticle[art].minStepValue
            else:
                data["value"]=listArticle[art].minValue
            
            listArticle[art].bidValue =data["value"]
            if auxBid.get(data["article"]):
                bids[auxBid[data["article"]]]["max"]=False

            auxBid[data["article"]]=i
            data["max"]=True
            bids.append(data)
        Bid.insert_bid_in_bulk(bids)

        for auc in listAuction:
            dateS=datetime.datetime.strptime(auc.dateStart, date_format)
            dateF=datetime.datetime.strptime(auc.dateFinish, date_format)
            if now >= dateS and now >= dateF:
                Auction.start(auc.uuid)
            if now >= dateF :
                Auction.setFinished(auc.uuid)
        for art in listArticle:
            Article.setFinished(art.uuid)
    logging.info('Ya puede usar la aplicacion')

    print('Ya puede usar la aplicación')