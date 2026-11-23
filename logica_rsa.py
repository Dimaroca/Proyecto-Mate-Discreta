import re
from matematica import es_primo, mcd, potencia_modular, inverso_modular


def validar_parametros(p, q, e):
    # Convertimos los datos ingresados a números enteros
    try:
        p = int(p)
        q = int(q)
        e = int(e)
    except ValueError:
        raise ValueError("p, q y e deben ser números enteros.")

    if p < 2 or q < 2:
        raise ValueError("p y q deben ser mayores o iguales que 2.")

    if p == q:
        raise ValueError("p y q deben ser distintos.")

    n = p * q

    if not 126126 < n < 1000000:
        raise ValueError(
            "Debe cumplirse: 126126 < p * q < 1000000."
        )

    if not es_primo(p) or not es_primo(q):
        raise ValueError("p y q deben ser números primos.")

    phi = (p - 1) * (q - 1)

    if e <= 1:
        raise ValueError("e debe ser mayor que 1.")

    if mcd(e, phi) != 1:
        raise ValueError("e y phi deben ser primos relativos.")

    return n, phi


def preparar_mensaje(mensaje):
    if mensaje == "":
        raise ValueError("Ingrese un mensaje.")

    # Validamos los caracteres sin modificarlos
    for caracter in mensaje:
        if not 32 <= ord(caracter) <= 126:
            raise ValueError(
                "Solo se permite ASCII del 32 al 126, "
                "sin tildes, ñ, tabulaciones ni saltos de línea."
            )

    # Guardar la longitud original, incluidos sus espacios
    longitud = len(mensaje)
    relleno = longitud % 2 == 1

    if relleno:
        mensaje = mensaje + " "

    bloques = []

    # Separar el mensaje en las parejas de caracteres
    for i in range(0, len(mensaje), 2):
        pareja = mensaje[i:i + 2]

        codigo_1 = f"{ord(pareja[0]):03d}"
        codigo_2 = f"{ord(pareja[1]):03d}"

        bloques.append(codigo_1 + codigo_2)

    return bloques, longitud, relleno


def encriptar(mensaje, p, q, e):
    n, phi = validar_parametros(p, q, e)
    e = int(e)

    bloques, longitud, relleno = preparar_mensaje(mensaje)

    bloques_cifrados = []
    detalles = []

    for bloque in bloques:
        m = int(bloque)

        # Calcular c = m elevado a e, módulo n
        c = potencia_modular(m, e, n)

        # Escribir cada bloque cifrado con seis dígitos obligatoriamente
        bloques_cifrados.append(f"{c:06d}")

        detalles.append(
            f"ASCII: {bloque[:3]} + {bloque[3:]} "
            f"| m: {m:06d} | c: {c:06d}"
        )

    # Separar los bloques cifrados con un espacio
    cifrado = " ".join(bloques_cifrados)

    return {
        "cifrado": cifrado,
        "longitud": longitud,
        "relleno": relleno,
        "n": n,
        "phi": phi,
        "e": e,
        "detalles": detalles
    }


def descifrar(cifrado, longitud, p, q, e):
    n, phi = validar_parametros(p, q, e)
    e = int(e)

    # Admitir únicamente bloques de seis dígitos
    # separados por espacios ASCII
    patron = r" *[0-9]{6}(?: +[0-9]{6})* *"

    if re.fullmatch(patron, cifrado) is None:
        raise ValueError(
            "El cifrado debe contener bloques de seis dígitos "
            "separados por espacios."
        )

    try:
        longitud = int(longitud)
    except ValueError:
        raise ValueError("La longitud L debe ser un entero.")

    bloques = [
        bloque
        for bloque in cifrado.split(" ")
        if bloque != ""
    ]

    cantidad = len(bloques)

    # Cada bloque representa dos caracteres.
    # Solo puede sobrar un espacio de relleno.
    if longitud not in (2 * cantidad, 2 * cantidad - 1):
        raise ValueError(
            f"Para {cantidad} bloques, L debe ser "
            f"{2 * cantidad - 1} o {2 * cantidad}."
        )

    if any(int(bloque) >= n for bloque in bloques):
        raise ValueError(
            f"Cada bloque cifrado debe ser menor que n = {n}."
        )

    # Obtener el exponente privado
    d = inverso_modular(e, phi)

    parejas = []
    detalles = []

    for bloque in bloques:
        c = int(bloque)

        # Calcular m = c elevado a d, módulo n
        m = potencia_modular(c, d, n)

        # Recuperar los dos códigos ASCII
        texto_ascii = f"{m:06d}"
        codigo_1 = int(texto_ascii[:3])
        codigo_2 = int(texto_ascii[3:])

        if not (32 <= codigo_1 <= 126 and 32 <= codigo_2 <= 126):
            raise ValueError(
                "Un bloque recuperado contiene ASCII inválido. "
                "Revise el cifrado y los parámetros."
            )

        pareja = chr(codigo_1) + chr(codigo_2)
        parejas.append(pareja)

        detalles.append(
            f"c: {c:06d} | m: {m:06d} "
            f"| ASCII: {codigo_1:03d} + {codigo_2:03d} "
            f"| Pareja: {pareja!r}"
        )

    mensaje = "".join(parejas)
    relleno = longitud % 2 == 1

    if relleno:
        if mensaje[-1] != " ":
            raise ValueError(
                "L indica relleno, pero falta el espacio final."
            )

        # Quitar exactamente solol un espacio del relleno.
        # Se conservan todos los espacios originales.
        mensaje = mensaje[:-1]

    return {
        "mensaje": mensaje,
        "longitud": longitud,
        "relleno": relleno,
        "n": n,
        "phi": phi,
        "e": e,
        "d": d,
        "detalles": detalles
    }


# La prueba de que solo se va a ejecutar al ejecutar este archivo directamente
if __name__ == "__main__":
    resultado = encriptar("RSA", "367", "373", "17")

    print("Cifrado:", resultado["cifrado"])
    print("Longitud:", resultado["longitud"])
    print("Relleno:", resultado["relleno"])
    print("n:", resultado["n"])
    print("phi:", resultado["phi"])

    print("\nDetalle de encriptación:")

    for detalle in resultado["detalles"]:
        print(detalle)

    recuperado = descifrar(
        resultado["cifrado"],
        resultado["longitud"],
        "367",
        "373",
        "17"
    )

    print("\nExponente privado d:", recuperado["d"])
    print("Mensaje recuperado:", repr(recuperado["mensaje"]))

    print("\nDetalle de descifrado:")

    for detalle in recuperado["detalles"]:
        print(detalle)