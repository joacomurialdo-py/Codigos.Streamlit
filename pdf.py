from fpdf import FPDF

def armar_pdf(cliente,total):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial","B", size=20)
    pdf.cell(0, 12, txt="Kiosoco de cosas", new_x="LMARGIN", new_y="NEXT")
    pdf.set_font("Arial","B", size=12)
    pdf.cell(0, 9, txt=f"Cliente: {cliente}", new_x="LMARGIN", new_y="NEXT")
    pdf.cell(0, 9, txt=f"Total a pagar: ${total:,.2f}", new_x="LMARGIN", new_y="NEXT")
    return bytes(pdf.output())
 