import streamlit as st

st.title("Kiosco de comida comestible")

cliente = st.text_input("Ingrese su nombre")

st.write(f"Bienvenido, {cliente} ,al kiosco de comida comestible")

Cantidad = st.number_input("Ingrese la cantidad de productos",0, step=1)

st.write(f"{cliente}  tu total a pagar es: {Cantidad * 1800}")


import streamlit as st
PRECIO_ALFAJOR = 1500
st.title("Kiosco Carlos Paz")
cantidad = st.number_input("Cantidad de alfajores",0, step=1)
total = cantidad * PRECIO_ALFAJOR
st.write(f"Total a pagar: ${total}")