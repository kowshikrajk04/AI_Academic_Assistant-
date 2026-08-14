from reportlab.platypus import (
    SimpleDocTemplate,
    Table,
    TableStyle,
    Paragraph,
    Spacer,
    Image
)

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib.colors import black


class QuestionPaperPDF:

    def __init__(self, filename):

        self.filename = filename
        self.styles = getSampleStyleSheet()

        self.title_style = self.styles["Heading1"]
        self.title_style.alignment = TA_CENTER

        self.heading_style = self.styles["Heading2"]

        self.normal_style = self.styles["BodyText"]


    def build(
        self,
        logo_path,
        college_name,
        academic_year,
        exam_name,
        department,
        semester,
        course_code,
        course_name,
        exam_date,
        session,
        duration,
        maximum_marks,
        course_outcomes,
        question_paper
    ):

        doc = SimpleDocTemplate(self.filename)

        elements = []

        # --------------------------------------------------
        # Logo
        # --------------------------------------------------

        if logo_path:

            try:

                logo = Image(
                    logo_path,
                    width=0.8 * inch,
                    height=0.8 * inch
                )

                logo.hAlign = "CENTER"

                elements.append(logo)

            except:
                pass

        # --------------------------------------------------
        # College Name
        # --------------------------------------------------

        elements.append(
            Paragraph(
                f"<b>{college_name}</b>",
                self.title_style
            )
        )

        elements.append(
            Paragraph(
                academic_year,
                self.normal_style
            )
        )

        elements.append(
            Paragraph(
                f"<b>{exam_name}</b>",
                self.heading_style
            )
        )

        elements.append(Spacer(1, 12))

        # --------------------------------------------------
        # Exam Details
        # --------------------------------------------------

        details = [

            ["Department", department],

            ["Semester", semester],

            ["Course Code", course_code],

            ["Course Name", course_name],

            ["Date", str(exam_date)],

            ["Session", session],

            ["Duration", duration],

            ["Maximum Marks", str(maximum_marks)]

        ]

        table = Table(details, colWidths=[120, 320])

        table.setStyle(

            TableStyle([

                ("GRID", (0, 0), (-1, -1), 1, black),

                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 8)

            ])

        )

        elements.append(table)

        elements.append(Spacer(1, 15))

        # --------------------------------------------------
        # Question Paper
        # --------------------------------------------------

        elements.append(
            Paragraph(
                "<b>QUESTION PAPER</b>",
                self.heading_style
            )
        )

        lines = question_paper.split("\n")

        for line in lines:

            if line.strip() == "":

                elements.append(Spacer(1, 6))

            else:

                elements.append(
                    Paragraph(line, self.normal_style)
                )

        elements.append(Spacer(1, 20))

        # --------------------------------------------------
        # Bloom Taxonomy
        # --------------------------------------------------

        elements.append(
            Paragraph(
                "<b>Bloom's Taxonomy</b>",
                self.heading_style
            )
        )

        bloom = [

            ["Level", "Description"],

            ["K1", "Remember"],

            ["K2", "Understand"],

            ["K3", "Apply"],

            ["K4", "Analyze"],

            ["K5", "Evaluate"],

            ["K6", "Create"]

        ]

        table = Table(bloom, colWidths=[80, 250])

        table.setStyle(

            TableStyle([

                ("GRID", (0, 0), (-1, -1), 1, black),

                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 8)

            ])

        )

        elements.append(table)

        doc.build(elements)

        return self.filename