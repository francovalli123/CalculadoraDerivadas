import re

def derivar_funcion(funcion):
    def derivar_polinomio(termino):
        if '^' in termino:
            coeficiente, exponente = re.split(r'x\^', termino)
            coeficiente = coeficiente if coeficiente else '1'
            coeficienteInt = int(coeficiente)
            exponente = re.sub(r'[^\d]', '', exponente)  # Limpiar exponente de caracteres no numéricos
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
        
    def derivar_coseno(termino):
        match = re.findall(r'cos\((.*)\)', termino)
        if match:
            argumento_coseno = match[0]
            derivada_argumento = derivar_funcion(argumento_coseno)
            if 'ln' in argumento_coseno:
                derivada_ln = derivar_logaritmo(argumento_coseno)
                return f"-sin({argumento_coseno}) * {derivada_ln}"
            return f"-sin({argumento_coseno}) * ({derivada_argumento})"
        return ''

    def derivar_seno(termino):
        match = re.findall(r'sin\((.*)\)', termino)
        if match:
            argumento_seno = match[0]
            if 'ln' in argumento_seno:
                # Aplicar la regla de la cadena para seno con ln
                derivada_argumento = derivar_funcion(argumento_seno)
                derivada_ln = derivar_logaritmo(argumento_seno)
                return f"cos({argumento_seno}) * ({derivada_ln})"
            else:
                # Caso simple sin ln en el argumento
                derivada_argumento = derivar_funcion(argumento_seno)
                return f"cos({argumento_seno}) * ({derivada_argumento})"
        return ''

    def derivar_logaritmo(termino):
        match = re.findall(r'ln\((.*)\)', termino)
        if match:
            argumento = match[0]
            derivada_argumento = derivar_funcion(argumento)
            return f"1/({argumento}) * ({derivada_argumento})"
        return ''

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
            elif 'cos' in termino:
                derivadas.append(derivar_coseno(termino))
            elif 'sin' in termino:
                derivadas.append(derivar_seno(termino))
            else:
                derivadas.append(derivar_polinomio(termino))
            if i > 0 and signos[i - 1] == '-':
                derivadas[-1] = '-' + derivadas[-1]
        return ' + '.join(filter(None, derivadas)).replace('+-', '- ')

    def derivar_producto_cociente(termino):
        if '*' in termino:
            factores = termino.split('*')
            f1, f2 = factores[0].strip(), factores[1].strip()
            df1 = derivar_funcion(f1)
            df2 = derivar_funcion(f2)
            return f"({df1} * {f2}) + ({f1} * {df2})"
        elif '/' in termino:
            numerador, denominador = termino.split('/')
            numerador, denominador = numerador.strip(), denominador.strip()
            dNumerador = derivar_funcion(numerador)
            dDenominador = derivar_funcion(denominador)
            return f"(({dNumerador} * {denominador}) - ({numerador} * {dDenominador})) / ({denominador})^2"

    def derivar_multiplo_constante(funcion):
        if '*' in funcion:
            partes = funcion.split('*')
            if partes[0].strip().isdigit():
                return partes[0] + ' * ' + derivar_funcion(partes[1].strip())
            elif partes[1].strip().isdigit():
                return partes[1] + ' * ' + derivar_funcion(partes[0].strip())

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
    elif 'cos' in funcion:
        return derivar_coseno(funcion)
    elif 'sin' in funcion:
        return derivar_seno(funcion)
    else:
        return derivar_polinomio(funcion)
