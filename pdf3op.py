import streamlit as st
from fpdf import FPDF
from datetime import date
import os

NOMBRE_KIOSCO = "Kiosco Carlos Paz"
LOGO = "logo.png"
DESCUENTO = 10
DESCUENTO_EFECTIVO = 5

productos = {
    "Gaseosa": 2800,
    "Alfajor": 1500,
    "Agua": 1000,
    "Chicles": 2000
}


def renglon(pdf, texto, valor):
    pdf.cell(120, 9, str(texto))
    pdf.cell(
        0, 9, str(valor),
        align="R",
        new_x="LMARGIN",
        new_y="NEXT"
    )


def armar_pdf(numero, fecha, cliente, items, pago,
              subtotal, descuento, porcentaje_descuento,
              iva, total):

    pdf = FPDF()
    pdf.add_page()

    if os.path.exists(LOGO):
        pdf.image(LOGO, x=12, y=5, w=50)

    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(
        0, 12, NOMBRE_KIOSCO,
        align="R",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(
        0, 7, f"Presupuesto N° {numero}",
        align="R",
        new_x="LMARGIN",
        new_y="NEXT"
    )
    pdf.cell(
        0, 7, f"Fecha: {fecha}",
        align="R",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    pdf.ln(15)

    pdf.set_font("Helvetica", "", 12)
    renglon(pdf, "Cliente", cliente or "Sin ingresar")
    renglon(pdf, "Forma de pago", pago)

    pdf.ln(4)

    pdf.set_font("Helvetica", "B", 12)
    renglon(pdf, "PRODUCTOS", "IMPORTE")

    pdf.set_font("Helvetica", "", 12)

    for producto, cantidad, precio, importe in items:
        renglon(
            pdf,
            f"{cantidad} x {producto} (${precio:.2f} c/u)",
            f"${importe:.2f}"
        )

    pdf.ln(4)

    renglon(pdf, "Subtotal", f"${subtotal:.2f}")
    renglon(
        pdf,
        f"Descuento ({porcentaje_descuento}%)",
        f"-${descuento:.2f}"
    )
    renglon(pdf, "IVA 21%", f"${iva:.2f}")

    pdf.set_font("Helvetica", "B", 14)
    pdf.set_text_color(0, 128, 0)
    renglon(pdf, "TOTAL", f"${total:.2f}")

    pdf.set_text_color(0, 0, 0)

    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(
        0, 6, "Presupuesto válido por 7 días.",
        new_x="LMARGIN",
        new_y="NEXT"
    )

    return bytes(pdf.output())

st.title("Kiosco Carlos Paz")
st.header("Crear pedido")

cliente = st.text_input("Nombre del cliente")

numero = st.number_input(
    "Número de pedido",
    min_value=1,
    step=1
)

fecha = st.date_input("Fecha", value=date.today())

st.subheader("Elegir hasta 3 productos diferentes")

opciones = ["Ninguno"] + list(productos.keys())

producto1 = st.selectbox(
    "Producto 1", opciones, index=1
)
cantidad1 = st.number_input(
    "Cantidad del producto 1",
    min_value=1, value=1, step=1,
    key="cantidad1",
    disabled=(producto1 == "Ninguno")
)

producto2 = st.selectbox(
    "Producto 2", opciones, index=2
)
cantidad2 = st.number_input(
    "Cantidad del producto 2",
    min_value=1, value=1, step=1,
    key="cantidad2",
    disabled=(producto2 == "Ninguno")
)

producto3 = st.selectbox(
    "Producto 3", opciones, index=3
)
cantidad3 = st.number_input(
    "Cantidad del producto 3",
    min_value=1, value=1, step=1,
    key="cantidad3",
    disabled=(producto3 == "Ninguno")
)

pago = st.selectbox(
    "Forma de pago",
    ["Efectivo", "Transferencia"]
)

selecciones = [
    (producto1, cantidad1),
    (producto2, cantidad2),
    (producto3, cantidad3)
]

items = [
    (nombre, cantidad, productos[nombre],
     productos[nombre] * cantidad)
    for nombre, cantidad in selecciones
    if nombre != "Ninguno"
]

nombres = [item[0] for item in items]
productos_repetidos = len(nombres) != len(set(nombres))

if not items:
    st.warning("Elegí al menos un producto.")

elif productos_repetidos:
    st.error("Elegí productos diferentes, sin repetir.")

else:
    subtotal = sum(item[3] for item in items)

    if pago == "Efectivo":
        porcentaje_descuento = (
            DESCUENTO + DESCUENTO_EFECTIVO
        )
    else:
        porcentaje_descuento = DESCUENTO

    descuento = subtotal * porcentaje_descuento / 100
    iva = (subtotal - descuento) * 0.21
    total = subtotal - descuento + iva

    st.header("Resumen del pedido")

    st.write("Cliente:", cliente if cliente else "Sin ingresar")
    st.write("Número de pedido:", numero)
    st.write("Fecha:", fecha)

    st.subheader("Productos")

    for nombre, cantidad, precio, importe in items:
        st.write(
            f"{cantidad} x {nombre} — "
            f"${precio:.2f} c/u — Importe: ${importe:.2f}"
        )

    st.write("Forma de pago:", pago)
    st.write(f"Subtotal: ${subtotal:.2f}")
    st.write(
        f"Descuento ({porcentaje_descuento}%): "
        f"-${descuento:.2f}"
    )
    st.write(f"IVA (21%): ${iva:.2f}")
    st.write(f"Total a pagar: ${total:.2f}")
    contenido_pdf = armar_pdf(
        numero, fecha, cliente, items, pago,
        subtotal, descuento, porcentaje_descuento,
        iva, total
    )

    st.download_button(
        "Descargar presupuesto PDF",
        data=contenido_pdf,
        file_name=f"presupuesto_{numero}.pdf",
        mime="application/pdf"
    )