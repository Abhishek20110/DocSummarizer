import pandas as pd
from fpdf import FPDF
import os

def generate_csv_report(data, output_path):
    """Generates a CSV report from summary data."""
    # data is expected to be a list of dicts: [{'filename': ..., 'summary': ...}]
    df = pd.DataFrame(data)
    df.to_csv(output_path, index=False)
    return output_path

def generate_pdf_report(data, output_path):
    """Generates a PDF report from summary data."""
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt="Document Summarization Report", ln=True, align='C')
    pdf.ln(10)

    for item in data:
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(200, 10, txt=f"File: {item['filename']}", ln=True)
        pdf.set_font("Arial", '', 10)
        # Multi_cell for long summaries
        pdf.multi_cell(0, 5, txt=item['summary'])
        pdf.ln(5)
        pdf.cell(200, 0, txt="", border='T', ln=True) # Divider line
        pdf.ln(5)

    pdf.output(output_path)
    return output_path
