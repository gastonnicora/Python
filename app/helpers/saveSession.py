import pickle


def saveDict(diccionario, archivo):
    with open(archivo, 'wb') as f:
        pickle.dump(diccionario, f)


def loadDict(archivo):
    try:
        with open(archivo, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

