
from os import environ
import requests as R   


celery_url= "http://"+environ.get("CELERY", "127.0.0.1:5000")
     
def deleteConfirm(uuid):
    try:
        # Hacer una solicitud GET al servicio de Celery
        response = R.get(f"{celery_url}/deleteConfirm/{uuid}")
        
        # Verificar si la solicitud fue exitosa (código de estado 200)
        if response.status_code == 200:
            print("Solicitud exitosa a Celery")
            print("Contenido de la respuesta:", response.text)
        else:
            print("La solicitud a Celery falló. Código de estado:", response.status_code)
    
    except Exception as e:
        print("Error al hacer la solicitud a Celery:", str(e))

def finishedArticle(uuid,time):
    data= {"article":uuid,"time":time}
    r=R.post(celery+"/finishedArticle",json=data)


def startedArticle(uuid,time):
    data= {"article":uuid,"time":time}
    r=R.post(celery+"/startedArticle",json=data)


def startedAuction(uuid,time):
    data= {"article":uuid,"time":time}
    r=R.post(celery+"/startedAuction",json=data)



