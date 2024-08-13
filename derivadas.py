import re

def derivar_funcion(funcion):
    # Derivar un término polinómico
    def derivar_polinomio(termino):
        if '^' in termino:
            coeficiente, exponente = re.split(r'x\^', termino)
            coeficiente = coeficiente if coeficiente else '1'
            coeficienteInt = int(coeficiente)
            exponenteInt = int(exponente)
            nuevo_coeficiente = coeficienteInt * exponenteInt
            nuevo_exponente = exponenteInt - 1
            if nuevo_exponente == 1:
                return f"{nuevo_coeficiente}x"
            elif nuevo_exponente == 0:
                return f"{nuevo_coeficiente}"
            else:
                return f"{nuevo_coeficiente}x^{nuevo_exponente}"
        elif 'x' in termino:
            coeficiente = termino.replace('x', '')
            coeficiente = coeficiente if coeficiente else '1'
            return coeficiente
        else:
            return ''

    # Derivar logaritmos
    def derivar_logaritmo(termino):
        argumento = re.findall(r'ln\((.*?)\)', termino)[0]
        derivada_argumento = derivar_funcion(argumento)
        return f"1/({argumento}) * ({derivada_argumento})"
    
    # Derivar suma y diferencia
    def derivar_suma_diferencia(funcion):
        terminos = re.split(r'(?<!\^)\+|\-(?=\d|\w)', funcion)
        terminos = [t.strip() for t in terminos if t]
        signos = re.findall(r'[+-]', funcion)
        derivadas = []
        for i, termino in enumerate(terminos):
            if '*' in termino or '/' in termino:
                derivadas.append(derivar_producto_cociente(termino))
            elif 'ln' in termino:
                derivadas.append(derivar_logaritmo(termino))
            else:
                derivadas.append(derivar_polinomio(termino))
            if i > 0 and signos[i - 1] == '-':
                derivadas[-1] = '-' + derivadas[-1]
        return ' + '.join(filter(None, derivadas)).replace('+-', '- ')

    # Derivar producto y cociente
    def derivar_producto_cociente(termino):
        if '*' in termino:
            factores = termino.split('*')
            f1, f2 = factores[0].strip(), factores[1].strip()
            df1 = derivar_funcion(f1)
            df2 = derivar_funcion(f2)
            if df1 == '' and df2 == '':
                return ''
            elif df1 == '':
                return f1 + ' * ' + df2
            elif df2 == '':
                return df1 + ' * ' + f2
            else:
                return f"({df1} * {f2}) + ({f1} * {df2})"
        elif '/' in termino:
            numerador, denominador = termino.split('/')
            numerador, denominador = numerador.strip(), denominador.strip()
            dNumerador = derivar_funcion(numerador)
            dDenominador = derivar_funcion(denominador)
            return f"(({dNumerador} * {denominador}) - ({numerador} * {dDenominador})) / ({denominador})^2"
    
    # Derivar multiplicación por constante
    def derivar_multiplo_constante(funcion):
        if '*' in funcion:
            partes = funcion.split('*')
            if partes[0].strip().isdigit():
                return partes[0] + ' * ' + derivar_funcion(partes[1].strip())
            elif partes[1].strip().isdigit():
                return partes[1] + ' * ' + derivar_funcion(partes[0].strip())
    
    # Caso base: polinomio simple, logaritmo, multiplicación/división, o múltiplo constante
    if '+' in funcion or '-' in funcion:
        return derivar_suma_diferencia(funcion)
    elif '*' in funcion and not '/' in funcion:
        if any(part.strip().isdigit() for part in funcion.split('*')):
            return derivar_multiplo_constante(funcion)
        else:
            return derivar_producto_cociente(funcion)
    elif '/' in funcion:
        return derivar_producto_cociente(funcion)
    elif 'ln' in funcion:
        return derivar_logaritmo(funcion)
    else:
        return derivar_polinomio(funcion)

# Ingresar función por teclado
funcion = input("f(x)= ")
# Calcular la derivada
derivada = derivar_funcion(funcion)
print("f'(x)=", derivada)
