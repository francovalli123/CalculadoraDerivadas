# main.py
import time
from derivadas import derivar_funcion
from diferencial import diferencial_term

def menu():
    print("Bienvenido")
    time.sleep(0.5)
    eleccion = int(input("""¿Qué desea hacer? 
    1- Derivación
    2- Derivación implícita
    3- Calcular diferencial
    Elección: """))

    if eleccion == 1:
        funcion = input("f(x)= ")
        derivada = derivar_funcion(funcion)
        time.sleep(0.5)
        print("f'(x)=", derivada)
    elif eleccion == 2:
        # Aquí iría el código para derivación implícita
        pass
    elif eleccion == 3:
        termino = input("f(x)= ")
        diferencial = diferencial_term(termino)
        time.sleep(0.5)
        print("dy/dx=", diferencial)
    else:
        print("Opción no válida")

if __name__ == "__main__":
    menu()
