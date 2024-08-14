from derivadas import derivar_funcion

def diferencial_term(termino):
    termino_derivado = derivar_funcion(termino)
    return f"{termino_derivado} dx"

