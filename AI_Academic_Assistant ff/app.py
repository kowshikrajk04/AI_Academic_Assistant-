import streamlit as st
import os
from datetime import date
import db

# ----------------------------------------------------
# EXISTING MODULES
# ----------------------------------------------------
from utils.context_builder import build_context

from utils.pdf_reader import extract_text

from utils.generator import (
    generate_learning_material,
    generate_mcqs,
    generate_assignments,
    generate_activities
)

from utils.pdf_export import create_pdf

# ----------------------------------------------------
# NEW MODULES
# ----------------------------------------------------

from utils.syllabus_parser import SyllabusParser
from utils.logo_extractor import LogoExtractor

from utils.questionpaper import QuestionPaperGenerator
from utils.question_pdf import QuestionPaperPDF

from utils.answerkey import AnswerKeyGenerator
from utils.answer_pdf import AnswerKeyPDF
from utils.rag import AcademicRAG

# ----------------------------------------------------
# PAGE CONFIG
# ----------------------------------------------------

st.set_page_config(
    page_title="AI Academic Assistant",
    page_icon="🎓",
    layout="wide"
)

st.title("🎓 AI Academic Assistant")

st.markdown("""
Generate

- 📘 Learning Material
- ❓ MCQs
- 📝 Assignments
- 🎯 Learning Activities
- 📄 Question Papers
- 📘 Answer Keys

using Ollama (Gemma3).
""")

# ----------------------------------------------------
# CREATE GENERATED FOLDER
# ----------------------------------------------------

os.makedirs("generated", exist_ok=True)

# ----------------------------------------------------
# SESSION STATE
# ----------------------------------------------------

session_defaults = {

    "learning_material": "",

    "mcqs": "",

    "assignments": "",

    "activities": "",

    "question_paper": "",

    "answer_key": "",

    "parsed_data": {},

    "logo_path": None,

    "authenticated": False,

    "user_info": None

}

for key, value in session_defaults.items():

    if key not in st.session_state:

        st.session_state[key] = value

# ----------------------------------------------------
# AUTHENTICATION GUARD
# ----------------------------------------------------

def show_auth_page():
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        tab_login, tab_signup = st.tabs(["🔑 Sign In", "📝 Sign Up"])
        
        with tab_login:
            st.subheader("Login to your Account")
            login_email = st.text_input("Email Address", key="login_email")
            login_password = st.text_input("Password", type="password", key="login_password")
            login_btn = st.button("Login", use_container_width=True)
            
            if login_btn:
                if not login_email or not login_password:
                    st.error("Please fill in all fields.")
                else:
                    user_info, msg = db.verify_faculty(login_email, login_password)
                    if user_info:
                        st.session_state.authenticated = True
                        st.session_state.user_info = user_info
                        st.success(msg)
                        st.rerun()
                    else:
                        st.error(msg)
                        
        with tab_signup:
            st.subheader("Create Faculty Profile")
            reg_name = st.text_input("Full Name", key="reg_name")
            reg_email = st.text_input("Email Address", key="reg_email")
            reg_dept = st.text_input("Department", key="reg_dept")
            reg_password = st.text_input("Password", type="password", key="reg_password")
            reg_confirm = st.text_input("Confirm Password", type="password", key="reg_confirm")
            signup_btn = st.button("Create Account", use_container_width=True)
            
            if signup_btn:
                if not reg_name or not reg_email or not reg_password or not reg_dept:
                    st.error("All fields are required.")
                elif reg_password != reg_confirm:
                    st.error("Passwords do not match.")
                else:
                    success, msg = db.register_faculty(reg_name, reg_email, reg_password, reg_dept)
                    if success:
                        st.success(msg + " You can now sign in.")
                    else:
                        st.error(msg)

if not st.session_state.authenticated:
    show_auth_page()
    st.stop()

# ----------------------------------------------------
# SIDEBAR
# ----------------------------------------------------

st.sidebar.markdown("### 👤 Faculty Profile")
st.sidebar.write(f"**Name:** {st.session_state.user_info['name']}")
st.sidebar.write(f"**Dept:** {st.session_state.user_info['department']}")
if st.sidebar.button("Logout", use_container_width=True):
    st.session_state.authenticated = False
    st.session_state.user_info = None
    st.rerun()
st.sidebar.markdown("---")

st.sidebar.header("📚 Course Details")

st.sidebar.subheader("📂 Academic Resources")

syllabus_pdf = st.sidebar.file_uploader(
    "📘 Syllabus (PDF)",
    type=["pdf"],
    key="syllabus"
)

textbook_pdfs = st.sidebar.file_uploader(
    "📚 Textbooks (PDF)",
    type=["pdf"],
    accept_multiple_files=True,
    key="textbooks"
)

reference_pdfs = st.sidebar.file_uploader(
    "📖 Reference Books (PDF)",
    type=["pdf"],
    accept_multiple_files=True,
    key="references"
)

faculty_notes = st.sidebar.file_uploader(
    "📝 Faculty Notes (Optional)",
    type=["pdf"],
    accept_multiple_files=True,
    key="notes"
)
topic = st.sidebar.text_input(
    "Topic"
)

course_outcome = st.sidebar.selectbox(
    "Course Outcome",
    [
        "CO1",
        "CO2",
        "CO3",
        "CO4",
        "CO5"
    ]
)

bloom = st.sidebar.selectbox(

    "Bloom's Taxonomy",

    [

        "Remember",

        "Understand",

        "Apply",

        "Analyze",

        "Evaluate",

        "Create"

    ]

)

difficulty = st.sidebar.selectbox(

    "Difficulty",

    [

        "Easy",

        "Medium",

        "Hard"

    ]

)

# ----------------------------------------------------
# EXAM DETAILS
# ----------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.header("📝 Exam Details")

academic_year = st.sidebar.text_input(

    "Academic Year",

    "2026-2027"

)

exam_name = st.sidebar.selectbox(

    "Examination",

    [

        "CIA I",

        "CIA II",

        "Model Examination",

        "Semester Examination"

    ]

)

department = st.sidebar.text_input(

    "Department"

)
college_name = st.sidebar.text_input(
    "College Name"
)

semester = st.sidebar.selectbox(
    "Semester",
    ["I","II","III","IV","V","VI","VII","VIII"]
)

course_code = st.sidebar.text_input(
    "Course Code"
)

course_name = st.sidebar.text_input(
    "Course Name"
)

exam_date = st.sidebar.date_input(

    "Exam Date",

    value=date.today()

)

session = st.sidebar.selectbox(

    "Session",

    [

        "FN",

        "AN"

    ]

)

duration = st.sidebar.text_input(

    "Exam Duration",

    "3 Hours"

)

maximum_marks = st.sidebar.number_input(

    "Maximum Marks",

    min_value=10,

    max_value=200,

    value=100

)

# ----------------------------------------------------
# BUTTONS
# ----------------------------------------------------

st.sidebar.markdown("---")

st.sidebar.subheader("Generate")

learning_btn = st.sidebar.button(
    "📘 Learning Material"
)

mcq_btn = st.sidebar.button(
    "❓ MCQs"
)

assignment_btn = st.sidebar.button(
    "📝 Assignments"
)

activity_btn = st.sidebar.button(
    "🎯 Activities"
)

question_btn = st.sidebar.button(
    "📄 Question Paper"
)

answer_btn = st.sidebar.button(
    "📘 Answer Key"
)

# ----------------------------------------------------
# VALIDATION
# ----------------------------------------------------

if syllabus_pdf is None:

    st.info("Upload a syllabus PDF.")

    st.stop()

if topic.strip() == "":

    st.info("Enter a Topic.")

    st.stop()
def save_uploaded_files(files, folder):

    os.makedirs(folder, exist_ok=True)

    saved_files = []

    if files:

        for file in files:

            file_path = os.path.join(folder, file.name)

            with open(file_path, "wb") as f:
                f.write(file.getbuffer())

            saved_files.append(file_path)

    return saved_files

# ----------------------------------------------------
# SAVE PDF
# ----------------------------------------------------

os.makedirs("uploads/syllabus", exist_ok=True)

syllabus_path = os.path.join(
    "uploads/syllabus",
    syllabus_pdf.name
)

with open(syllabus_path, "wb") as f:
    f.write(syllabus_pdf.getbuffer())

textbook_paths = save_uploaded_files(
    textbook_pdfs,
    "uploads/textbooks"
)

reference_paths = save_uploaded_files(
    reference_pdfs,
    "uploads/reference_books"
)

faculty_note_paths = save_uploaded_files(
    faculty_notes,
    "uploads/faculty_notes"
)

# ----------------------------------------------------
# EXTRACT PDF TEXT & BUILD RAG INDEX
# ----------------------------------------------------

syllabus_text = extract_text(syllabus_path)

# Initialize and build local RAG Engine
rag_engine = AcademicRAG()
rag_engine.add_pdf(syllabus_path, "Syllabus")

textbook_text = ""

for pdf in textbook_pdfs or []:
    textbook_text += "\n" + extract_text(pdf)

reference_text = ""

for pdf in reference_pdfs or []:
    reference_text += "\n" + extract_text(pdf)

faculty_text = ""

for pdf in faculty_notes or []:
    faculty_text += "\n" + extract_text(pdf)

# Add all saved files to the RAG index
for path in textbook_paths:
    rag_engine.add_pdf(path, "Textbook")

for path in reference_paths:
    rag_engine.add_pdf(path, "Reference")

for path in faculty_note_paths:
    rag_engine.add_pdf(path, "Faculty Note")

rag_engine.build_index()
st.session_state.rag_engine = rag_engine

pdf_text = build_context(
    syllabus_text,
    textbook_text,
    reference_text,
    faculty_text
)

# ----------------------------------------------------
# PARSE SYLLABUS
# ----------------------------------------------------

parser = SyllabusParser(syllabus_text)

parsed_data = parser.parse()

st.session_state.parsed_data = parsed_data

# ----------------------------------------------------
# EXTRACT COLLEGE LOGO
# ----------------------------------------------------

logo_extractor = LogoExtractor(syllabus_path)

logo_path = logo_extractor.extract_logo()

st.session_state.logo_path = logo_path
# ----------------------------------------------------
# GENERATE LEARNING MATERIAL
# ----------------------------------------------------

if learning_btn:

    with st.spinner("Generating Learning Material..."):

        try:

            # Retrieve context using RAG if available
            if "rag_engine" in st.session_state and st.session_state.rag_engine is not None:
                context = st.session_state.rag_engine.get_combined_context(topic)
            else:
                context = pdf_text

            st.session_state.learning_material = generate_learning_material(

                context,

                topic,

                course_outcome,

                bloom,

                difficulty

            )

            st.success("Learning Material Generated Successfully!")

        except Exception as e:

            st.error(f"Error : {e}")


# ----------------------------------------------------
# GENERATE MCQs
# ----------------------------------------------------

if mcq_btn:

    with st.spinner("Generating MCQs..."):

        try:

            # Retrieve context using RAG if available
            if "rag_engine" in st.session_state and st.session_state.rag_engine is not None:
                context = st.session_state.rag_engine.get_combined_context(topic)
            else:
                context = pdf_text

            st.session_state.mcqs = generate_mcqs(

                context,

                topic,

                difficulty

            )

            st.success("MCQs Generated Successfully!")

        except Exception as e:

            st.error(f"Error : {e}")


# ----------------------------------------------------
# GENERATE ASSIGNMENTS
# ----------------------------------------------------

if assignment_btn:

    with st.spinner("Generating Assignment Questions..."):

        try:

            # Retrieve context using RAG if available
            if "rag_engine" in st.session_state and st.session_state.rag_engine is not None:
                context = st.session_state.rag_engine.get_combined_context(topic)
            else:
                context = pdf_text

            st.session_state.assignments = generate_assignments(

                context,

                topic

            )

            st.success("Assignments Generated Successfully!")

        except Exception as e:

            st.error(f"Error : {e}")


# ----------------------------------------------------
# GENERATE LEARNING ACTIVITIES
# ----------------------------------------------------

if activity_btn:

    with st.spinner("Generating Learning Activities..."):

        try:

            # Retrieve context using RAG if available
            if "rag_engine" in st.session_state and st.session_state.rag_engine is not None:
                context = st.session_state.rag_engine.get_combined_context(topic)
            else:
                context = pdf_text

            st.session_state.activities = generate_activities(

                context,

                topic

            )

            st.success("Learning Activities Generated Successfully!")

        except Exception as e:

            st.error(f"Error : {e}")
            # ----------------------------------------------------
# GENERATE QUESTION PAPER
# ----------------------------------------------------

if question_btn:

    with st.spinner("Generating Question Paper..."):

        try:

            generator = QuestionPaperGenerator()

            question_paper = generator.generate(

                syllabus_text=pdf_text,

                parsed_data=parsed_data,

                academic_year=academic_year,

                exam_name=exam_name,

                exam_date=str(exam_date),

                session=session,

                duration=duration,

                maximum_marks=maximum_marks,

                difficulty=difficulty,

                bloom_level=bloom,

                rag_engine=st.session_state.get("rag_engine")

            )

            st.session_state.question_paper = question_paper

            pdf_generator = QuestionPaperPDF(
                "generated/QuestionPaper.pdf"
            )

            pdf_generator.build(

    logo_path=logo_path,

    college_name=college_name,

    academic_year=academic_year,

    exam_name=exam_name,

    department=department,

    semester=semester,

    course_code=course_code,

    course_name=course_name,

    exam_date=str(exam_date),

    session=session,

    duration=duration,

    maximum_marks=maximum_marks,

    course_outcomes=parsed_data["course_outcomes"],

    question_paper=question_paper

)

            st.success("Question Paper Generated Successfully!")

        except Exception as e:

            st.error(f"Question Paper Error : {e}")


# ----------------------------------------------------
# GENERATE ANSWER KEY
# ----------------------------------------------------

if answer_btn:

    if st.session_state.question_paper == "":

        st.warning(
            "Generate the Question Paper first."
        )

    else:

        with st.spinner("Generating Answer Key..."):

            try:

                generator = AnswerKeyGenerator()

                answer_key = generator.generate(

                    question_paper=st.session_state.question_paper,

                    syllabus_text=pdf_text

                )

                st.session_state.answer_key = answer_key

                pdf_generator = AnswerKeyPDF(
                    "generated/AnswerKey.pdf"
                )

                pdf_generator.build(

    logo_path=logo_path,

    college_name=college_name,

    academic_year=academic_year,

    exam_name=exam_name,

    department=department,

    semester=semester,

    course_code=course_code,

    course_name=course_name,

    exam_date=str(exam_date),

    session=session,

    duration=duration,

    maximum_marks=maximum_marks,

    answer_key=answer_key

)

                st.success("Answer Key Generated Successfully!")

            except Exception as e:

                st.error(f"Answer Key Error : {e}")
                # ----------------------------------------------------
# DISPLAY OUTPUT
# ----------------------------------------------------

st.divider()

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    [
        "📘 Learning Material",
        "❓ MCQs",
        "📝 Assignments",
        "🎯 Activities",
        "📄 Question Paper",
        "📘 Answer Key"
    ]
)

# ====================================================
# LEARNING MATERIAL
# ====================================================

with tab1:

    st.subheader("📘 Learning Material")

    if st.session_state.learning_material:

        st.write(st.session_state.learning_material)

        learning_pdf = create_pdf(
            "generated/Learning_Material.pdf",
            "Learning Material",
            st.session_state.learning_material
        )

        with open(learning_pdf, "rb") as file:

            st.download_button(
                "📥 Download Learning Material",
                file,
                file_name="Learning_Material.pdf",
                mime="application/pdf"
            )

    else:

        st.info("Generate Learning Material.")

# ====================================================
# MCQs
# ====================================================

with tab2:

    st.subheader("❓ Multiple Choice Questions")

    if st.session_state.mcqs:

        st.write(st.session_state.mcqs)

        mcq_pdf = create_pdf(
            "generated/MCQs.pdf",
            "MCQs",
            st.session_state.mcqs
        )

        with open(mcq_pdf, "rb") as file:

            st.download_button(
                "📥 Download MCQs",
                file,
                file_name="MCQs.pdf",
                mime="application/pdf"
            )

    else:

        st.info("Generate MCQs.")

# ====================================================
# ASSIGNMENTS
# ====================================================

with tab3:

    st.subheader("📝 Assignment Questions")

    if st.session_state.assignments:

        st.write(st.session_state.assignments)

        assignment_pdf = create_pdf(
            "generated/Assignment_Questions.pdf",
            "Assignment Questions",
            st.session_state.assignments
        )

        with open(assignment_pdf, "rb") as file:

            st.download_button(
                "📥 Download Assignments",
                file,
                file_name="Assignment_Questions.pdf",
                mime="application/pdf"
            )

    else:

        st.info("Generate Assignment Questions.")

# ====================================================
# ACTIVITIES
# ====================================================

with tab4:

    st.subheader("🎯 Learning Activities")

    if st.session_state.activities:

        st.write(st.session_state.activities)

        activity_pdf = create_pdf(
            "generated/Learning_Activities.pdf",
            "Learning Activities",
            st.session_state.activities
        )

        with open(activity_pdf, "rb") as file:

            st.download_button(
                "📥 Download Activities",
                file,
                file_name="Learning_Activities.pdf",
                mime="application/pdf"
            )

    else:

        st.info("Generate Learning Activities.")

# ====================================================
# QUESTION PAPER
# ====================================================

with tab5:

    st.subheader("📄 Question Paper")

    if st.session_state.question_paper:

        st.text_area(
            "Generated Question Paper",
            st.session_state.question_paper,
            height=650
        )

        if os.path.exists("generated/QuestionPaper.pdf"):

            with open("generated/QuestionPaper.pdf", "rb") as file:

                st.download_button(

                    "📥 Download Question Paper",

                    file,

                    file_name="QuestionPaper.pdf",

                    mime="application/pdf"

                )

    else:

        st.info("Generate Question Paper.")

# ====================================================
# ANSWER KEY
# ====================================================

with tab6:

    st.subheader("📘 Answer Key")

    if st.session_state.answer_key:

        st.text_area(

            "Generated Answer Key",

            st.session_state.answer_key,

            height=650

        )

        if os.path.exists("generated/AnswerKey.pdf"):

            with open("generated/AnswerKey.pdf", "rb") as file:

                st.download_button(

                    "📥 Download Answer Key",

                    file,

                    file_name="AnswerKey.pdf",

                    mime="application/pdf"

                )

    else:

        st.info("Generate Answer Key.")

# ----------------------------------------------------
# FOOTER
# ----------------------------------------------------

st.divider()

st.markdown("## 🎓 AI Academic Assistant")

st.caption(
    """
Powered by

• Ollama (Gemma3)

• Streamlit

• PyMuPDF

• ReportLab

AI-Based Academic Content Generation System
"""
)