import streamlit as st

PRODUCTOS = ["Alfajor", "Gaseosa", "Mantecol"]
PRECIO = [1500, 2800, 2000]

st.title("Tienda de cosas")

cliente = st.text_input("Ingrese su nombre")

st.write(f"Bienvenido, {cliente} ,a la tienda de cosas")

st.write("Seleccione el producto que desea comprar")

cantidad = st.number_input("Ingrese la cantidad de productos",0, step=1)

seleccion = st.selectbox("Seleccione un producto", PRODUCTOS)

st.write(f"{cliente}  tu total a pagar es: {PRECIO[PRODUCTOS.index(seleccion)] * cantidad}")

st.write("Que metodo de pago desea utilizar?")

metodo_pago = st.radio("Seleccione un metodo de pago", ["Efectivo", "Taransferencia"])

st.write(f"{cliente}  Tu metodo de pago seleccionado es: {metodo_pago}")

def calcular_descuento(total, metodo):
    if metodo == "Efectivo":
        return total * 0.1
    else:
        return 0
st.write(f"{cliente}  Tu descuento es: {calcular_descuento(PRECIO[PRODUCTOS.index(seleccion)] * cantidad, metodo_pago)}")