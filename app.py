import streamlit as st
from logica_rsa import encriptar, descifrar

st.set_page_config(page_title="Proyecto RSA")
st.title("Sistema criptográfico RSA")
st.caption("MM2015 · Grupo 18")

c1, c2, c3 = st.columns(3)
c1.text_input("Primo p", "367", key="p")
c2.text_input("Primo q", "373", key="q")
c3.text_input("Exponente e", "17", key="e")


def hacer_encriptar():
    try:
        r = encriptar(st.session_state.mensaje, st.session_state.p,
                      st.session_state.q, st.session_state.e)
        st.session_state.cifrado = r["cifrado"]
        st.session_state.longitud = str(r["longitud"])
        st.session_state.resultado = ("enc", r)
    except ValueError as err:
        st.session_state.resultado = ("error", str(err))


def hacer_descifrar():
    try:
        r = descifrar(st.session_state.cifrado, st.session_state.longitud,
                      st.session_state.p, st.session_state.q, st.session_state.e)
        st.session_state.resultado = ("dec", r)
    except ValueError as err:
        st.session_state.resultado = ("error", str(err))


st.subheader("Encriptar")
st.text_area("Mensaje original M", "RSA", key="mensaje")
st.button("Encriptar", on_click=hacer_encriptar, type="primary")

st.subheader("Descifrar")
st.text_area("Cifrado C (bloques de seis dígitos)", key="cifrado")
st.text_input("Longitud original L", key="longitud")
st.button("Descifrar", on_click=hacer_descifrar, type="primary")

st.subheader("Resultados")
res = st.session_state.get("resultado")
if res:
    tipo, r = res
    if tipo == "error":
        st.error(r)
    else:
        if tipo == "enc":
            st.success("Encriptación completada")
            st.write(f"n = {r['n']} · φ = {r['phi']} · llave pública (e, n) = ({r['e']}, {r['n']})")
            st.code(r["cifrado"])
        else:
            st.success("Descifrado completado")
            st.write(f"n = {r['n']} · φ = {r['phi']} · d = {r['d']}")
            st.code(repr(r["mensaje"]))
        st.text("\n".join(r["detalles"]))