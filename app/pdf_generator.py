from fpdf import FPDF

def gerar_relatorio_pdf(ticket_data):
    pdf = FPDF()
    pdf.add_page()

    pdf.set_font('Arial', 'B', 16)
    pdf.cell(200, 10, f"Relatório do Chamado #{ticket_data['id']}", ln=True, align='C')

    pdf.set_font('Arial', '', 12)
    pdf.ln(10)
    pdf.cell(200, 10, f"Descrição: {ticket_data.get('description', 'N/A')}", ln=True)
    pdf.cell(200, 10, f"Data de Abertura: {ticket_data.get('date', 'N/A')}", ln=True)
    pdf.cell(200, 10, f"Status: {ticket_data.get('status', 'N/A')}", ln=True)

    pdf_output = "relatorio_chamado.pdf"
    pdf.output(pdf_output)
    print(f'Relatório salvo como {pdf_output}')
