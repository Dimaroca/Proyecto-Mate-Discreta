import streamlit as st
from logica_rsa import encriptar, descifrar

st.set_page_config(page_title="Proyecto RSA")

st.session_state.setdefault("salida", "")


def ejecutar_encriptacion():
    try:
        mensaje = st.session_state["mensaje"]

        resultado = encriptar(
            mensaje,
            st.session_state["p"],
            st.session_state["q"],
            st.session_state["e"]
        )

        # Colocar C y L en los campos para lograr descifrar
        st.session_state["cifrado"] = resultado["cifrado"]
        st.session_state["longitud"] = str(resultado["longitud"])

        relleno = (
            "Sí, se agregó un espacio"
            if resultado["relleno"]
            else "No"
        )

        texto = (
            "ENCRIPTACIÓN COMPLETADA\n\n"
            f"Mensaje original: {mensaje!r}\n"
            f"n: {resultado['n']}\n"
            f"phi: {resultado['phi']}\n"
            "MCD(e, phi): 1\n"
            f"Llave pública (e, n): "
            f"({resultado['e']}, {resultado['n']})\n"
            f"Longitud L: {resultado['longitud']}\n"
            f"Relleno: {relleno}\n\n"
            f"Cifrado C: {resultado['cifrado']}\n\n"
            "DETALLE DE BLOQUES\n"
        )

        texto += "\n".join(resultado["detalles"])
        st.session_state["salida"] = texto

    except ValueError as error:
        st.session_state["salida"] = f"ERROR DE VALIDACIÓN\n\n{error}"


def ejecutar_descifrado():
    try:
        resultado = descifrar(
            st.session_state["cifrado"],
            st.session_state["longitud"],
            st.session_state["p"],
            st.session_state["q"],
            st.session_state["e"]
        )

        relleno = (
            "Sí, se retiró exactamente un espacio"
            if resultado["relleno"]
            else "No"
        )

        texto = (
            "DESCIFRADO COMPLETADO\n\n"
            f"n: {resultado['n']}\n"
            f"phi: {resultado['phi']}\n"
            "MCD(e, phi): 1\n"
            f"Llave pública (e, n): "
            f"({resultado['e']}, {resultado['n']})\n"
            f"Exponente privado d: {resultado['d']}\n"
            f"Llave privada (d, n): "
            f"({resultado['d']}, {resultado['n']})\n"
            f"Longitud L: {resultado['longitud']}\n"
            f"Relleno: {relleno}\n\n"
            f"Mensaje recuperado: {resultado['mensaje']!r}\n"
            "(Las comillas permiten observar los espacios "
            "y no forman parte del mensaje).\n\n"
            "DETALLE DE BLOQUES\n"
        )

        texto += "\n".join(resultado["detalles"])
        st.session_state["salida"] = texto

    except ValueError as error:
        st.session_state["salida"] = f"ERROR DE VALIDACIÓN\n\n{error}"


st.markdown(
    "<h2 style='text-align:center;'>Sistema criptográfico RSA</h2>",
    unsafe_allow_html=True
)

col_p, col_q, col_e = st.columns(3)
col_p.text_input("Primo p:", key="p")
col_q.text_input("Primo q:", key="q")
col_e.text_input("Exponente e:", key="e")

st.text_area(
    "Mensaje original M (para encriptar):",
    key="mensaje",
    height=68
)

st.text_area(
    "Cifrado C (bloques de seis dígitos separados por espacios):",
    key="cifrado",
    height=68
)

col_l, _ = st.columns([1, 3])
col_l.text_input("Longitud original L:", key="longitud")

col_b1, col_b2, _ = st.columns([1, 1, 4])
col_b1.button("Encriptar", on_click=ejecutar_encriptacion, use_container_width=True)
col_b2.button("Descifrar", on_click=ejecutar_descifrado, use_container_width=True)

st.text_area(
    "Resultados y detalle del proceso:",
    key="salida",
    height=380,
    disabled=True
)