from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    Table,
    TableStyle
)

from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.units import inch
from reportlab.lib import colors


class AnswerKeyPDF:

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

        answer_key

    ):

        doc = SimpleDocTemplate(self.filename)

        elements = []

        # -----------------------------------------
        # College Logo
        # -----------------------------------------

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

        # -----------------------------------------
        # College Name
        # -----------------------------------------

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
                f"<b>{exam_name} - ANSWER KEY</b>",
                self.heading_style
            )
        )

        elements.append(Spacer(1, 12))

        # -----------------------------------------
        # Exam Details Table
        # -----------------------------------------

        details = [

            ["Department", department],

            ["Semester", semester],

            ["Course Code", course_code],

            ["Course Name", course_name],

            ["Exam Date", str(exam_date)],

            ["Session", session],

            ["Duration", duration],

            ["Maximum Marks", str(maximum_marks)]

        ]

        table = Table(details, colWidths=[120, 330])

        table.setStyle(

            TableStyle([

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BACKGROUND", (0, 0), (0, -1), colors.lightgrey),

                ("FONTNAME", (0, 0), (-1, -1), "Helvetica"),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 8)

            ])

        )

        elements.append(table)

        elements.append(Spacer(1, 20))

        # -----------------------------------------
        # Answer Key Heading
        # -----------------------------------------

        elements.append(

            Paragraph(
                "<b>ANSWER KEY</b>",
                self.heading_style
            )

        )

        elements.append(Spacer(1, 10))

        # -----------------------------------------
        # Answers
        # -----------------------------------------

        lines = answer_key.split("\n")

        for line in lines:

            if line.strip() == "":

                elements.append(Spacer(1, 6))

            else:

                elements.append(

                    Paragraph(
                        line,
                        self.normal_style
                    )

                )

        elements.append(Spacer(1, 20))

        # -----------------------------------------
        # Footer
        # -----------------------------------------

        footer = [

            ["Prepared By", "Verified By", "HOD"]

        ]

        table = Table(
            footer,
            colWidths=[160, 160, 160]
        )

        table.setStyle(

            TableStyle([

                ("GRID", (0, 0), (-1, -1), 1, colors.black),

                ("BACKGROUND", (0, 0), (-1, 0), colors.lightgrey),

                ("ALIGN", (0, 0), (-1, -1), "CENTER"),

                ("BOTTOMPADDING", (0, 0), (-1, -1), 20)

            ])

        )

        elements.append(table)

        doc.build(elements)

        return self.filename