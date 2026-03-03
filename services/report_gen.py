import csv
import re
import os
from fpdf import FPDF


def strip_markdown(text: str) -> str:
    """Remove common Markdown syntax for plain-text rendering in PDF."""
    if not text:
        return ""
    # Remove bold/italic markers
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"\*(.+?)\*",     r"\1", text)
    text = re.sub(r"__(.+?)__",     r"\1", text)
    text = re.sub(r"_(.+?)_",       r"\1", text)
    # Replace ### headers with plain label
    text = re.sub(r"^###\s*",  "", text, flags=re.MULTILINE)
    text = re.sub(r"^##\s*",   "", text, flags=re.MULTILINE)
    text = re.sub(r"^#\s*",    "", text, flags=re.MULTILINE)
    # Convert bullet dashes to bullet char
    text = re.sub(r"^[-*]\s+", "• ", text, flags=re.MULTILINE)
    return text.strip()


def safe_text(text: str) -> str:
    """Encode to latin-1 safely, replacing unsupported characters."""
    return text.encode("latin-1", errors="replace").decode("latin-1")


def generate_csv_report(data, output_path):
    """Generates a CSV report from summary data, including evaluation scores."""
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        fieldnames = ["filename", "summary", "coverage", "faithfulness", "clarity", "structure", "overall", "reason"]
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        for item in data:
            ev = item.get("evaluation") or {}
            writer.writerow({
                "filename":    item.get("filename", ""),
                "summary":     item.get("summary", ""),
                "coverage":    ev.get("coverage", ""),
                "faithfulness":ev.get("faithfulness", ""),
                "clarity":     ev.get("clarity", ""),
                "structure":   ev.get("structure", ""),
                "overall":     ev.get("overall", ""),
                "reason":      ev.get("reason", ""),
            })
    return output_path


class HoliPDF(FPDF):
    """Custom FPDF with a simple Holi-themed header stripe."""

    COLORS = [
        (233, 30, 140),   # Pink
        (245, 101, 0),    # Orange
        (232, 168, 0),    # Yellow
        (21,  168, 50),   # Green
        (0,   153, 204),  # Cyan
        (123, 44,  191),  # Purple
    ]

    def header(self):
        # Rainbow stripe at top
        stripe_w = self.w / len(self.COLORS)
        for i, (r, g, b) in enumerate(self.COLORS):
            self.set_fill_color(r, g, b)
            self.rect(i * stripe_w, 0, stripe_w + 1, 5, "F")
        self.ln(8)
        self.set_font("Arial", "B", 18)
        self.set_text_color(30, 30, 30)
        self.cell(0, 10, safe_text("DocSummarizer - Report"), ln=True, align="C")
        self.ln(4)

    def footer(self):
        self.set_y(-15)
        self.set_font("Arial", "I", 8)
        self.set_text_color(150, 140, 160)
        self.cell(0, 10, safe_text(f"Page {self.page_no()}"), align="C")


def generate_pdf_report(data, output_path):
    """Generates a styled PDF report, including evaluation scores."""
    pdf = HoliPDF()
    pdf.set_auto_page_break(auto=True, margin=20)
    pdf.add_page()

    row_colors = HoliPDF.COLORS

    for idx, item in enumerate(data):
        r, g, b = row_colors[idx % len(row_colors)]

        # ── File name header bar ──────────────────────────────────
        pdf.set_fill_color(r, g, b)
        pdf.set_text_color(255, 255, 255)
        pdf.set_font("Arial", "B", 11)
        filename = safe_text(item.get("filename", "Unknown"))
        pdf.cell(0, 9, f"  {filename}", ln=True, fill=True)
        pdf.ln(2)

        # ── Summary ───────────────────────────────────────────────
        pdf.set_text_color(30, 30, 30)
        pdf.set_font("Arial", "B", 9)
        pdf.set_text_color(r, g, b)
        pdf.cell(0, 6, "SUMMARY", ln=True)
        pdf.set_text_color(50, 40, 60)
        pdf.set_font("Arial", "", 9)
        summary_plain = safe_text(strip_markdown(item.get("summary", "")))
        pdf.multi_cell(0, 5, summary_plain)
        pdf.ln(3)

        # ── Evaluation scores ─────────────────────────────────────
        ev = item.get("evaluation")
        if ev:
            pdf.set_font("Arial", "B", 9)
            pdf.set_text_color(r, g, b)
            pdf.cell(0, 6, "QUALITY EVALUATION", ln=True)

            # Score grid (2 columns)
            pdf.set_font("Arial", "", 9)
            pdf.set_text_color(50, 40, 60)
            metrics = [
                ("Coverage",    ev.get("coverage",    "?")),
                ("Faithfulness",ev.get("faithfulness","?")),
                ("Clarity",     ev.get("clarity",     "?")),
                ("Structure",   ev.get("structure",   "?")),
            ]
            col_w = 90
            for i in range(0, len(metrics), 2):
                for j in range(2):
                    if i + j < len(metrics):
                        label, val = metrics[i + j]
                        pdf.set_font("Arial", "B", 9)
                        pdf.cell(col_w, 6, f"{label}: ", border=0)
                    if j == 1 or i + 1 >= len(metrics):
                        pass
                pdf.ln()
                for j in range(2):
                    if i + j < len(metrics):
                        label, val = metrics[i + j]
                        pdf.set_font("Arial", "", 9)
                        score_text = safe_text(f"{val}/10")
                        # Colour the score
                        try:
                            v = int(val)
                            if v >= 8:   pdf.set_text_color(21, 168, 50)
                            elif v >= 6: pdf.set_text_color(232, 168, 0)
                            else:        pdf.set_text_color(214, 40, 40)
                        except Exception:
                            pdf.set_text_color(50, 40, 60)
                        pdf.cell(col_w, 5, f"  {label}: {score_text}")
                        pdf.set_text_color(50, 40, 60)
                pdf.ln()

            # Overall score
            overall = ev.get("overall", "?")
            pdf.set_font("Arial", "B", 10)
            try:
                v = int(overall)
                if v >= 8:   pdf.set_text_color(21, 168, 50)
                elif v >= 6: pdf.set_text_color(232, 168, 0)
                else:        pdf.set_text_color(214, 40, 40)
            except Exception:
                pdf.set_text_color(50, 40, 60)
            pdf.cell(0, 7, f"  Overall: {overall}/10", ln=True)

            # Reason
            pdf.set_font("Arial", "I", 8)
            pdf.set_text_color(100, 90, 110)
            reason = safe_text(ev.get("reason", ""))
            if reason:
                pdf.multi_cell(0, 4, f"  \"{reason}\"")

        pdf.ln(4)

        # ── Divider ───────────────────────────────────────────────
        pdf.set_draw_color(r, g, b)
        pdf.set_line_width(0.8)
        pdf.line(10, pdf.get_y(), 200, pdf.get_y())
        pdf.ln(6)

    pdf.output(output_path)
    return output_path
