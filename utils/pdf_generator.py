from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER


def create_pdf(report, output_path):
    """
    Generate a PDF report from the AI-generated summary.
    """

    # Safety check
    if not report:
        return

    styles = getSampleStyleSheet()

    title_style = styles["Title"]
    title_style.alignment = TA_CENTER

    heading_style = styles["Heading2"]

    body_style = styles["BodyText"]

    doc = SimpleDocTemplate(output_path)

    story = []

    # -------------------------
    # Title
    # -------------------------

    story.append(
        Paragraph(
            "ResearchMind AI Report",
            title_style
        )
    )

    story.append(Spacer(1, 20))

    # -------------------------
    # Report Content
    # -------------------------

    for line in report.split("\n"):

        line = line.strip()

        if not line:
            continue

        # Markdown headings
        if line.startswith("#"):
            story.append(
                Paragraph(
                    line.replace("#", "").strip(),
                    heading_style
                )
            )

        else:
            story.append(
                Paragraph(
                    line,
                    body_style
                )
            )

    # -------------------------
    # Build PDF
    # -------------------------

    doc.build(story)