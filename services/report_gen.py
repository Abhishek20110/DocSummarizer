import csv
import re
import os
from fpdf import FPDF


# ─────────────────────────────────────────────
# Markdown Stripping (kept exactly as you had)
# ─────────────────────────────────────────────

def strip_markdown(text: str) -> str:
    if not text:
        return ""

    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*",     r"\1", text)
    text = re.sub(r"__(.+?)__",     r"\1", text)
    text = re.sub(r"_(.+?)_",       r"\1", text)

    text = re.sub(r"^###\s*", "", text, flags=re.MULTILINE)
    text = re.sub(r"^##\s*",  "", text, flags=re.MULTILINE)
    text = re.sub(r"^#\s*",   "", text, flags=re.MULTILINE)

    text = re.sub(r"^[-*]\s+", "• ", text, flags=re.MULTILINE)

    return text.strip()


# ─────────────────────────────────────────────
# CSV (unchanged)
# ─────────────────────────────────────────────

def generate_csv_report(data, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["filename", "summary", "coverage", "faithfulness", "clarity", "structure", "overall", "reason"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            ev = item.get("evaluation") or {}
            writer.writerow({
                "filename": item.get("filename", ""),
                "summary": item.get("summary", ""),
                "coverage": ev.get("coverage", ""),
                "faithfulness": ev.get("faithfulness", ""),
                "clarity": ev.get("clarity", ""),
                "structure": ev.get("structure", ""),
                "overall": ev.get("overall", ""),
                "reason": ev.get("reason", ""),
            })
    return output_path


# ─────────────────────────────────────────────
# PDF CLASS (Style 100% maintained)
# ─────────────────────────────────────────────

class HoliPDF(FPDF):

    COLORS = [
        (233, 30, 140),
        (245, 101, 0),
        (232, 168, 0),
        (21, 168, 50),
        (0, 153, 204),
        (123, 44, 191),
    ]

    def __init__(self):
        super().__init__()
        import os
        # Get project root (go one level up from services/)
        BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        FONT_DIR = os.path.join(BASE_DIR, "ttf")
        # Register Unicode fonts (fpdf2)
        self.add_font("DejaVu", "", os.path.join(FONT_DIR, "DejaVuSans.ttf"))
        self.add_font("DejaVu", "B", os.path.join(FONT_DIR, "DejaVuSans-Bold.ttf"))
        self.add_font("DejaVu", "I", os.path.join(FONT_DIR, "DejaVuSans-Oblique.ttf"))

    def header(self):
        stripe_w = self.w / len(self.COLORS)
        for i, (r, g, b) in enumerate(self.COLORS):
            self.set_fill_color(r, g, b)
            self.rect(i * stripe_w, 0, stripe_w + 1, 5, "F")

        self.ln(8)
        self.set_font("DejaVu", "B", 18)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, "DocSummarizer - Report", ln=True, align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("DejaVu", "I", 8)
        self.set_text_color(150, 140, 160)
        self.cell(0, 10, f"Page {self.page_no()}", align="C")


# ─────────────────────────────────────────────
# PDF Generator (Style fully preserved)
# ─────────────────────────────────────────────

def generate_pdf_report(data, output_path):
    pdf = HoliPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    row_colors = HoliPDF.COLORS

    for idx, item in enumerate(data):
        r, g, b = row_colors[idx % len(row_colors)]

        # File Header Bar
        pdf.set_fill_color(r, g, b)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("DejaVu", "B", 11)
        filename = item.get("filename", "Unknown")
        pdf.cell(0, 9, f"  {filename}", ln=True, fill=True)
        pdf.ln(2)

        # SUMMARY
        pdf.set_font("DejaVu", "B", 9)
        pdf.set_text_color(r, g, b)
        pdf.cell(0, 6, "SUMMARY", ln=True)

        pdf.set_text_color(50, 40, 60)
        pdf.set_font("DejaVu", "", 9)

        summary_plain = strip_markdown(item.get("summary", ""))
        pdf.multi_cell(0, 5, summary_plain)
        pdf.ln(3)

        # Evaluation (unchanged logic)
        ev = item.get("evaluation")
        if ev:
            pdf.set_font("DejaVu", "B", 9)
            pdf.set_text_color(r, g, b)
            pdf.cell(0, 6, "QUALITY EVALUATION", ln=True)

            pdf.set_font("DejaVu", "", 9)
            pdf.set_text_color(50, 40, 60)

            metrics = [
                ("Coverage", ev.get("coverage", "?")),
                ("Faithfulness", ev.get("faithfulness", "?")),
                ("Clarity", ev.get("clarity", "?")),
                ("Structure", ev.get("structure", "?")),
            ]

            col_w = 90

            for i in range(0, len(metrics), 2):
                for j in range(2):
                    if i + j < len(metrics):
                        label, val = metrics[i + j]
                        pdf.set_font("DejaVu", "", 9)

                        try:
                            v = int(val)
                            if v >= 8:
                                pdf.set_text_color(21, 168, 50)
                            elif v >= 6:
                                pdf.set_text_color(232, 168, 0)
                            else:
                                pdf.set_text_color(214, 40, 40)
                        except:
                            pdf.set_text_color(50, 40, 60)

                        pdf.cell(col_w, 5, f"  {label}: {val}/10")

                pdf.ln()
                pdf.set_text_color(50, 40, 60)

            # Overall
            overall = ev.get("overall", "?")
            pdf.set_font("DejaVu", "B", 10)

            try:
                v = int(overall)
                if v >= 8:
                    pdf.set_text_color(21, 168, 50)
                elif v >= 6:
                    pdf.set_text_color(232, 168, 0)
                else:
                    pdf.set_text_color(214, 40, 40)
            except:
                pdf.set_text_color(50, 40, 60)

            pdf.cell(0, 7, f"  Overall: {overall}/10", ln=True)

            # Reason
            pdf.set_font("DejaVu", "I", 8)
            pdf.set_text_color(100, 90, 110)

            reason = ev.get("reason", "")
            if reason:
                pdf.multi_cell(0, 4, f'  "{reason}"')

        pdf.ln(4)

        # Divider
        pdf.set_draw_color(r, g, b)
        pdf.set_line_width(0.8)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(6)

    pdf.output(output_path)
    return output_path