import streamlit as st

# Precios
PRECIO_ALFAJOR = 10000
PRECIO_GASEOSA = 2800

st.title("kiosco Carlos Paz")

nombre = st.text_input("Nombre del cliente")


cant_alfajores = st.number_input("Cantidad de alfajores",0, step=1)
cant_gaseosas = st.number_input("Cantidad de gaseosas",0, step=1)

def calcular_total(cantidad, precio):
    return cantidad * precio


subtotal_alfajores = calcular_total(cant_alfajores, PRECIO_ALFAJOR)
subtotal_gaseosas = calcular_total(cant_gaseosas, PRECIO_GASEOSA)
total = subtotal_alfajores + subtotal_gaseosas


if nombre:
    st.write(f"pedido de {nombre}")

st.write(f"alfajores: ${subtotal_alfajores}")
st.write(f"gaseosas: ${subtotal_gaseosas}")
st.write(f"total: ${total}")
st.title("promo 3x2 en alfajores")

cant_promo = st.number_input("cantidad de alfajores (promo)",0, step=1)

grupos = cant_promo // 3
resto = cant_promo % 3

paga = grupos * 2 + resto
total_promo = paga * PRECIO_ALFAJOR
ahorro = (cant_promo - paga) * PRECIO_ALFAJOR

st.write(f"lleva {cant_promo} alfajores")
st.write(f"paga {paga}")
st.write(f"total: ${total_promo}")
st.write(f"ahorro: ${ahorro}")


