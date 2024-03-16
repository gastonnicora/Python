import pickle

# Función para guardar el diccionario en un archivo
def saveDict(diccionario, archivo):
    with open(archivo, 'wb') as f:
        pickle.dump(diccionario, f)

# Función para cargar el diccionario desde un archivo
def loadDict(archivo):
    try:
        with open(archivo, 'rb') as f:
            return pickle.load(f)
    except FileNotFoundError:
        return {}

