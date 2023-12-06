import datetime
import os, json
from app.helpers.message import Message
class Validador(object):
    def __init__(self, nameDB, nameUrl, data):
        self.data = data
        self.error = []
        self.haveError = False
        #todos los datos de la clase
        self.DB= EndPoint.json().get(nameDB)
        #datos del endpoint
        self.url= self.DB.get("endpoint").get(nameUrl)
        self.checkError()
    
    def checkError(self):
        for f in self.url.get("fields"):
            self._checkField(f)
    
    def errors(self):
        return Message(error=self.error)
    
    def _checkField(self, field):
        property = self.DB.get("fields").get(field).get("property")
        validation_methods = {
            "required": self._required,
            "type": {
                "string": self._string,
                "integer": self._integer,
                "date": self._date,
                "pass": self._pass,
                "email": self._email
            },
            "repeat": self._repeat,
            "max length": self._maxLength,
            "min length": self._minLength,
            "max": self._max,
            "min": self._min,
            "max date": self._maxDate,
            "min date": self._minDate
        }
        for p in property:
            value = property[p].get("value")
            if p in validation_methods:
                if isinstance(validation_methods[p], dict):
                    if value in validation_methods[p]:
                        validation_methods[p][value](field)
                else:
                    validation_methods[p](field)
            
    def _logError(self, field,property):
        self.haveError = True
        self.error.append({field: self.DB.get("fields").get(field).get("property").get(property).get("error")})

    def _string(self, field):
        data= self.data.get(field)
        if not (isinstance(data, str) or data is None):
            self._logError(field,"type")
    
    def _pass(self,field):
        data= self.data.get(field)
        if not (isinstance(data, str) or data.isalnum() or data is None):
            self._logError(field,"type")

    def _email(self,field):
        data= self.data.get(field)
        try:
            isEmail=True
            nombre, dominio = data.split('@')
            try:
                dom1, dom2 = dominio.split('.',maxsplit = 1)
                if not (len(nombre) >= 5 and dom1 and dom2):
                    isEmail=False
            except ValueError:
                # Dominio no contiene "."
                isEmail=False
        except ValueError:
            # email no contiene "@"
            isEmail=False
        if not (isinstance(data, str) or isEmail or data is None):
            self._logError(field,"type")
        
    def _integer(self, field):
        data= self.data.get(field)
        if not(isinstance(data, int) or data is None):
            self._logError(field,"type")

    def _date(self, field):
        data= self.data.get(field)
        date_format = '%d/%m/%Y'
        date_obj = None
        try:
            date_obj = datetime.datetime.strptime(data, date_format)
        finally:
            if not(isinstance(data, str) or isinstance(date_obj, datetime.datetime) or data is None):
                self._logError(field,"type")
    
    def _repeat(self,field):
        data= self.data.get(field)
        field1=self.DB.get("fields").get(field).get("property").get("repeat")["repetition"]
        data1= self.data.get(field1)
        if isinstance(data, str):
            if not(  data1==data or data is None):
                self._logError(field,"repeat")

    def _maxLength(self, field):
        max= self.DB.get("fields").get(field).get("property")["max length"]["value"]
        data= self.data.get(field)
        if isinstance(data, str):
            if not(len(data) < max or data is None):
                self._logError(field,"max length")
    
    def _minLength(self, field):
        min= self.DB.get("fields").get(field).get("property")["min length"]["value"]
        data= self.data.get(field)
        if isinstance(data, str):
            if not( len(data) > min or data is None):
                self._logError(field,"min length")
    
    def _max(self, field):
        max= self.DB.get("fields").get(field).get("property")["max"]["value"]
        data= self.data.get(field)
        if isinstance(data, int):
            if not ( data < max or data is None):
                self._logError(field,"max")
    
    def _min(self, field):
        min= self.DB.get("fields").get(field).get("property")["min"]["value"]
        data= self.data.get(field)
        if isinstance(data, int):
            if not ( data > min or data is None):
                self._logError(field,"min")
    
    def _maxDate(self, field):
        max= self.DB.get("fields").get(field).get("property")["max date"]["value"]
        data= self.data.get(field)
        date_format = '%d/%m/%Y'
        date_obj = None
        try:
            date_obj = datetime.datetime.strptime(data, date_format)
            date_max = datetime.datetime.strptime(max, date_format)
        finally:
            if isinstance(data, str):
                if not (date_obj < date_max or data is None):
                    self._logError(field,"max date")
    
    def _minDate(self, field):
        min= self.DB.get("fields").get(field).get("property")["min date"]["value"]
        data= self.data.get(field)
        date_format = '%d/%m/%Y'
        date_obj = None
        try:
            date_obj = datetime.datetime.strptime(data, date_format)
            date_min = datetime.datetime.strptime(min, date_format)
        finally:
            if isinstance(data, str):
                if not ( date_obj > date_min or data is None):
                    self._logError(field,"min date")

    def _required(self, field):
        data= self.data.get(field)
        if self._string(data) and data:
            data=data.strip()
        if not (data != None and data !="" and data != [] and data !={}):
           self._logError(field,"required")
           


class EndPoint(object):
    @classmethod
    def json(cls):
        script_dir = os.path.dirname(__file__)
        rel_path = "../endpoint.json"
        abs_file_path = os.path.join(script_dir, rel_path)

        currentFile = open(abs_file_path)
        data = json.load(currentFile)
        currentFile.close()
        return data