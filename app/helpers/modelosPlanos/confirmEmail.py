import json
class ConfirmEmail():
    def __init__(cls,data=None, lista=None):
        if data:
            cls.uuid=data.uuid
            cls.user = data.user
            cls.dateOfCreate=data.dateOfCreate
        if lista:
            listado=[]
            for i in lista:
                listado.append(ConfirmEmail(i))
            cls.confirmEmail= listado
    def toJSON(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4))