import re


class SyllabusParser:

    def __init__(self, syllabus_text):
        self.text = syllabus_text


    # ------------------------------
    # College Name
    # ------------------------------
    def extract_college_name(self):

        lines = self.text.split("\n")

        for line in lines[:20]:

            line = line.strip()

            if len(line) > 5 and any(word in line.upper() for word in [
                "COLLEGE",
                "INSTITUTE",
                "UNIVERSITY",
                "TECHNOLOGY",
                "ENGINEERING"
            ]):
                return line

        return "College Name"


    # ------------------------------
    # Course Code
    # ------------------------------
    def extract_course_code(self):

        patterns = [

            r"[A-Z]{2,5}\d{3,5}",

            r"\b\d{2}[A-Z]{2,5}\d{3}\b"
        ]

        for pattern in patterns:

            match = re.search(pattern, self.text)

            if match:

                return match.group()

        return "Course Code"


    # ------------------------------
    # Course Name
    # ------------------------------
    def extract_course_name(self):

        lines = self.text.split("\n")

        for line in lines:

            if "Course Name" in line:

                parts = line.split(":")

                if len(parts) > 1:

                    return parts[1].strip()

        return "Course Name"


    # ------------------------------
    # Department
    # ------------------------------
    def extract_department(self):

        lines = self.text.split("\n")

        for line in lines:

            if "Department" in line:

                parts = line.split(":")

                if len(parts) > 1:

                    return parts[1].strip()

        return "Department"


    # ------------------------------
    # Semester
    # ------------------------------
    def extract_semester(self):

        match = re.search(r"Semester\s*[:\-]?\s*(\w+)", self.text, re.I)

        if match:

            return match.group(1)

        return "Semester"


    # ------------------------------
    # Units
    # ------------------------------
    def extract_units(self):

        units = {}

        current_unit = None

        lines = self.text.split("\n")

        for line in lines:

            line = line.strip()

            unit_match = re.match(
                r"(UNIT\s*[-:]?\s*[IVX0-9]+)",
                line,
                re.I
            )

            if unit_match:

                current_unit = unit_match.group()

                units[current_unit] = []

                continue

            if current_unit and line != "":

                units[current_unit].append(line)

        return units


    # ------------------------------
    # Course Outcomes
    # ------------------------------
    def extract_course_outcomes(self):

        outcomes = {}

        lines = self.text.split("\n")

        for line in lines:

            line = line.strip()

            match = re.match(
                r"(CO\d+)\s*[:\-]?\s*(.*)",
                line,
                re.I
            )

            if match:

                outcomes[match.group(1).upper()] = match.group(2)

        return outcomes


    # ------------------------------
    # Topics
    # ------------------------------
    def extract_topics(self):

        topics = []

        lines = self.text.split("\n")

        for line in lines:

            line = line.strip()

            if len(line) < 3:

                continue

            if line.upper().startswith("UNIT"):

                continue

            if line.upper().startswith("CO"):

                continue

            if len(line.split()) <= 10:

                topics.append(line)

        return topics


    # ------------------------------
    # Everything
    # ------------------------------
    def parse(self):

        return {

            "college_name": self.extract_college_name(),

            "course_code": self.extract_course_code(),

            "course_name": self.extract_course_name(),

            "department": self.extract_department(),

            "semester": self.extract_semester(),

            "course_outcomes": self.extract_course_outcomes(),

            "units": self.extract_units(),

            "topics": self.extract_topics()
        }