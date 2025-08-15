import random

# Vamos a ver el concepto de decorador

def mi_decorator(func):

    def nueva_funtion():
        print("Empezo")
        func()
        print("Termino")

    return nueva_funtion

@mi_decorator
def mi_funcion():
    print("mi funcion")


mi_funcion()