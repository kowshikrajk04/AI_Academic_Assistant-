class PromptBuilder:

    @staticmethod
    def build_question_paper_prompt(
        syllabus_text,
        course_name,
        course_code,
        department,
        semester,
        academic_year,
        exam_name,
        exam_date,
        session,
        duration,
        maximum_marks,
        course_outcomes,
        difficulty,
        bloom_level
    ):

        prompt = f"""
You are an experienced university question paper setter.

Generate a professional university question paper using the provided academic context.

========================
COURSE DETAILS
========================

Course Name : {course_name}

Course Code : {course_code}

Department : {department}

Semester : {semester}

Academic Year : {academic_year}

Exam : {exam_name}

Exam Date : {exam_date}

Session : {session}

Duration : {duration}

Maximum Marks : {maximum_marks}

Difficulty Level : {difficulty}

Bloom's Taxonomy Level : {bloom_level}

========================
COURSE OUTCOMES
========================

{course_outcomes}

========================
ACADEMIC CONTEXT
========================

{syllabus_text}

=========================================================
QUESTION PAPER FORMAT
=========================================================

Generate the question paper exactly in the following format.

---------------------------------------------------------
PART A (10 × 2 = 20 Marks)
---------------------------------------------------------

• Generate exactly 10 questions.

• Every question carries 2 marks.

• Cover all important syllabus topics.

• Mention Bloom's Level.

• Mention CO.

Example:

1. Explain Dependency Injection.
(BTL-2) (CO1)

---------------------------------------------------------
PART B (5 × 16 = 80 Marks)
---------------------------------------------------------

Generate exactly FIVE questions.

Each question must contain:

11(a)
OR
11(b)

12(a)
OR
12(b)

13(a)
OR
13(b)

14(a)
OR
14(b)

15(a)
OR
15(b)

Rules:

• Each question carries 16 Marks.

• Each OR question should come from the SAME UNIT.

• Questions should not repeat concepts.

• Include analytical and application questions.

• Use Bloom's taxonomy.

• Mention CO.

=========================================================
IMPORTANT RULES
=========================================================

1. Use only the provided academic context.

2. Do not generate questions outside the academic context.

3. Maintain university examination standards.

4. Avoid duplicate questions.

5. Balance all units.

6. Include K-Level for every question.

7. Include Course Outcome for every question.

8. Questions should match the selected difficulty level.

9. Generate clear and grammatically correct questions.

10. Return ONLY the question paper.

Do not include explanations.

Do not include answers.

Do not use Markdown.

Return clean plain text.
"""

        return prompt


    @staticmethod
    def build_answer_key_prompt(question_paper):

        prompt = f"""
You are an experienced university professor.

Generate the complete answer key for the following question paper.

QUESTION PAPER

{question_paper}

Rules:

1. Answer every question.

2. Part A should contain short answers.

3. Part B should contain detailed answers.

4. Include examples wherever possible.

5. Include diagrams if required.

6. Include algorithms if required.

7. Include programs if required.

8. Include outputs wherever applicable.

9. Return only the answer key.

10. Do not repeat the question paper.
"""

        return prompt