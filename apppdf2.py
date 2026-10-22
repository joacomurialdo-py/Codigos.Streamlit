
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
    pdf.cell(120, 9, texto)
    pdf.cell(0, 9, valor, align="R",
             new_x="LMARGIN", new_y="NEXT")


def armar_pdf(numero, fecha, cliente, producto, cantidad,
              precio, pago, subtotal, descuento, porcentaje_descuento,
              iva, total):

    pdf = FPDF()
    pdf.add_page()

    # Encabezado
    if os.path.exists(LOGO):
        pdf.image(LOGO, x=12, y=5, w=50)

    pdf.set_font("Helvetica", "B", 20)
    pdf.cell(0, 12, NOMBRE_KIOSCO, align="R",
             new_x="LMARGIN", new_y="NEXT")

    pdf.set_font("Helvetica", "", 11)
    pdf.cell(0, 7, f"Presupuesto N° {numero}", align="R",
             new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 7, f"Fecha: {fecha}", align="R",
             new_x="LMARGIN", new_y="NEXT")

    pdf.ln(15)

   
    pdf.set_font("Helvetica", "", 12)
    renglon(pdf, "Cliente", cliente or "Sin ingresar")
    renglon(pdf, "Forma de pago", pago)
    renglon(pdf, f"{cantidad} x {producto}",
            f"${precio:.2f} c/u")

    pdf.ln(4)


    renglon(pdf, "Subtotal", f"${subtotal:.2f}")
    renglon(pdf, f"Descuento ({porcentaje_descuento}%)",
            f"-${descuento:.2f}")
    renglon(pdf, "IVA 21%", f"${iva:.2f}")

    pdf.set_font("Helvetica", "B", 14)
    renglon(pdf, "TOTAL", f"${total:.2f}")

    # Pie del presupuesto
    pdf.ln(10)
    pdf.set_font("Helvetica", "I", 9)
    pdf.cell(0, 6, "Presupuesto válido por 7 días.",
             new_x="LMARGIN", new_y="NEXT")

    return bytes(pdf.output())

st.title("Kiosco Carlos Paz")
st.header("Crear pedido")


cliente = st.text_input("Nombre del cliente")
numero = st.number_input("Número de pedido",
                         min_value=1, step=1)
fecha = st.date_input("Fecha", value=date.today())


producto = st.selectbox("Elegir producto",
                        list(productos.keys()))
cantidad = st.number_input("Cantidad",
                           min_value=1, value=1, step=1)

pago = st.selectbox("Forma de pago",
                    ["Efectivo", "Transferencia"])

precio_unitario = productos[producto]
subtotal = precio_unitario * cantidad

if pago == "Efectivo":
    porcentaje_descuento = DESCUENTO + DESCUENTO_EFECTIVO
else:
    porcentaje_descuento = DESCUENTO

descuento = subtotal * porcentaje_descuento / 100
iva = (subtotal - descuento) * 0.21
total = subtotal - descuento + iva


st.header("Resumen del pedido")

st.write("Cliente:", cliente if cliente else "Sin ingresar")
st.write("Número de pedido:", numero)
st.write("Fecha:", fecha)
st.write("Producto:", producto)
st.write("Cantidad:", cantidad)
st.write("Precio unitario: $", f"{precio_unitario:.2f}")
st.write("Forma de pago:", pago)
st.write("Subtotal: $", f"{subtotal:.2f}")
st.write(f"Descuento ({porcentaje_descuento}%): $",
         f"{descuento:.2f}")
st.write("IVA (21%): $", f"{iva:.2f}")
st.write("Total a pagar: $", f"{total:.2f}")

contenido_pdf = armar_pdf(
    numero, fecha, cliente, producto, cantidad,
    precio_unitario, pago, subtotal, descuento,
    porcentaje_descuento, iva, total
)

st.download_button(
    "Descargar presupuesto PDF",
    data=contenido_pdf,
    file_name=f"presupuesto_{numero}.pdf",
    mime="application/pdf"
)