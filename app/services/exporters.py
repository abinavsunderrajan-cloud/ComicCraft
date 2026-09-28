from datetime import datetime
from pathlib import Path
from fpdf import FPDF
from app.config import EXPORTS_DIR, PANELS_DIR

def save_pdf(comic):

    timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    filename = f"comic_{timestamp}.pdf"

    output_path: Path = EXPORTS_DIR / filename

    pdf = FPDF(
        orientation="P",
        unit="mm",
        format="A4"
    )

    for panel in comic["panels"]:

        pdf.add_page()

        # -------------------------
        # Panel title
        # -------------------------

        pdf.set_font(
            "Helvetica",
            "B",
            18
        )

        pdf.cell(
            0,
            12,
            str(panel["title"]),
            ln=True
        )

        # -------------------------
        # Panel image
        # -------------------------

        image_url = panel["image_url"]

        image_filename = Path(
            image_url
        ).name

        image_path = PANELS_DIR / image_filename

        if image_path.exists():

            pdf.image(
                str(image_path),
                x=15,
                y=30,
                w=180,
                h=100
            )

        # -------------------------
        # Text area
        # -------------------------

        pdf.set_y(135)

        pdf.set_font(
            "Helvetica",
            "",
            11
        )

        narration = panel.get(
            "narration",
            ""
        )

        if narration:

            pdf.multi_cell(
                0,
                7,
                f"Narration: {narration}"
            )

        dialogue = panel.get(
            "dialogue",
            ""
        )

        if dialogue:

            pdf.ln(3)

            pdf.multi_cell(
                0,
                7,
                f"Dialogue: {dialogue}"
            )

    pdf.output(str(output_path))

    return f"/static/exports/{filename}"