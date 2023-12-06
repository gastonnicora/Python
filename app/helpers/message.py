from app.helpers.serializacion import Serializacion
import json
class Message(object):
    codError=404
    def __init__(self,content=None,error=None):
        self.content=content
        self.error=error
        self.cod=202
        if self.error !="" and self.error!=None and self.error!=[] and self.error!={} :
            self.cod=400
    def dump(self):
        return json.loads(json.dumps(self, default=lambda o: o.__dict__, 
            sort_keys=True, indent=4)) 
    