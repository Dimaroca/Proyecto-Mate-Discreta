def es_primo(numero):
    # Aqui definimos que los números menores que 2 no son números primos
    if numero < 2:
        return False

    divisor = 2

    # Buscamos los divisores hasta llegar a la raíz cuadrada del número
    while divisor * divisor <= numero:
        if numero % divisor == 0:
            return False

        divisor += 1

    return True

def mcd(a, b):
    while b != 0:
        residuo = a % b
        a = b
        b = residuo

    return a

def inverso_modular(e, phi):
    # Los residuos del algoritmo de Euclides
    r_anterior = phi
    r_actual = e % phi

    # Los coeficientes que permiten encontrar el inverso
    t_anterior = 0
    t_actual = 1

    while r_actual != 0:
        cociente = r_anterior // r_actual

        nuevo_r = r_anterior - cociente * r_actual
        r_anterior = r_actual
        r_actual = nuevo_r

        nuevo_t = t_anterior - cociente * t_actual
        t_anterior = t_actual
        t_actual = nuevo_t

    if r_anterior != 1:
        raise ValueError("No existe inverso modular.")

    return t_anterior % phi


def potencia_modular(base, exponente, modulo):
    resultado = 1
    base = base % modulo

    while exponente > 0:
        # Si es que el exponente es impar, se multiplica
        if exponente % 2 == 1:
            resultado = (resultado * base) % modulo

        # Elevamos la base al cuadrado y lo reducimos
        base = (base * base) % modulo

        # Dividimos el exponente entre 2, sin decimales
        exponente = exponente // 2

    return resultado


