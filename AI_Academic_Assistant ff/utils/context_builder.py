def build_context(
    syllabus_text,
    textbook_text,
    reference_text,
    faculty_text
):
    """
    Build a structured academic context for the AI model.
    Faculty Notes have the highest priority, followed by
    Textbooks, Reference Books, and finally the Syllabus.
    """

    context = f"""
You are an AI Academic Assistant.

Use the following academic resources in this priority:

1. Faculty Notes (Highest Priority)
2. Textbooks
3. Reference Books
4. Syllabus (Only for unit/course outcome mapping)

==========================
FACULTY NOTES
==========================

{faculty_text}

==========================
TEXTBOOKS
==========================

{textbook_text}

==========================
REFERENCE BOOKS
==========================

{reference_text}

==========================
SYLLABUS
==========================

{syllabus_text}

"""
    return context