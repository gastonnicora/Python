
from os import environ
import requests as R   


celery=environ.get("CELERY", "127.0.0.1:5000")

     
def deleteConfirm(uuid):
    r=R.get(f"http://celery:5000/deleteConfirm/{uuid}")
    if r.status_code == 202:
        print("La solicitud se realizó correctamente.")
        print("Respuesta:", r.json())
    else:
        print("Hubo un problema al realizar la solicitud a Celery.")
        print("Código de estado:", r.status_code)

def finishedArticle(uuid,time):
    data= {"article":uuid,"time":time}
    r=R.post(celery+"/finishedArticle",json=data)


def startedArticle(uuid,time):
    data= {"article":uuid,"time":time}
    r=R.post(celery+"/startedArticle",json=data)


def startedAuction(uuid,time):
    data= {"article":uuid,"time":time}
    r=R.post(celery+"/startedAuction",json=data)



