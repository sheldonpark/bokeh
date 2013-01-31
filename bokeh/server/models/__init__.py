import json

class UnauthorizedException(Exception):
    pass

class ServerModel(object):
    idfield = None
    typename = None
    
    @classmethod
    def modelkey(cls, objid):
        return "model:%s:%s"% (cls.typename, objid)

    def mykey(self):
        return self.modelkey(getattr(self, self.idfield))

    def to_json(self):
        raise NotImplementedError
    
    @staticmethod
    def from_json(obj):
        raise NotImplementedError        
    
    def save(self, client):
        client.set(self.mykey(), json.dumps(self.to_json()))
        
    @classmethod
    def load(cls, client, objid):
        data = client.get(cls.modelkey(objid))
        if data is None:
            return None
        attrs = json.loads(data)
        return cls.from_json(attrs)