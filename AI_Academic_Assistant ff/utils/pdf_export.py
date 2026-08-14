import os
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch


def create_pdf(filename, title, content):
    """
    Create PDF from generated text.
    """

    # Create folder if it doesn't exist
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    doc = SimpleDocTemplate(
        filename,
        rightMargin=40,
        leftMargin=40,
        topMargin=40,
        bottomMargin=40
    )

    styles = getSampleStyleSheet()

    title_style = styles["Heading1"]
    title_style.alignment = TA_CENTER

    body_style = styles["BodyText"]
    body_style.leading = 20

    story = []

    # PDF Title
    story.append(Paragraph(title, title_style))
    story.append(Spacer(1, 0.3 * inch))

    if content is None:
        content = ""

    # Convert to string
    content = str(content)

    # Escape HTML characters
    content = (
        content.replace("&", "&amp;")
               .replace("<", "&lt;")
               .replace(">", "&gt;")
    )

    # Add each line
    for line in content.split("\n"):

        line = line.strip()

        if line == "":
            story.append(Spacer(1, 0.15 * inch))
        else:
            story.append(Paragraph(line, body_style))
            story.append(Spacer(1, 0.08 * inch))

    doc.build(story)

    return filename