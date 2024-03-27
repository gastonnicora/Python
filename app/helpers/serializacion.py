class  Serializacion(object):

    @classmethod
    def dump(cls, obj,name="", paged=False, many=False):
        if paged and many:
            return cls._serialize_collection(obj,name)
        elif many:
            return cls._serialize_collection_all(obj,name)
        else:
            return cls._serialize(obj)

    @classmethod
    def _serialize_collection_all(cls, all,name):
        return {
            "Total": len(all),
            name: [cls._serialize(elem) for elem in all]
        }

    @classmethod
    def _serialize_collection(cls, pagination,name):
        return {
            "Total": pagination.total,
            "Pagina": pagination.page,
            "Paginas_totales":pagination.pages,
            name: [cls._serialize(elem) for elem in pagination.items]
        }


    @classmethod
    def _serialize(cls, obj):
        return  { attr.name: getattr(obj, attr.name) for attr in obj.__table__.columns }