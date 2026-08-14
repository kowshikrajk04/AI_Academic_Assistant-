import ollama

# Change this if your model name is different
MODEL = "gemma3:latest"


def ask_ollama(prompt):
    """
    Send prompt to Ollama and return response.
    """
    try:
        response = ollama.chat(
            model=MODEL,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )

        return response["message"]["content"]

    except Exception as e:
        return f"Error: {str(e)}"


# ----------------------------------------------------
# Learning Material
# ----------------------------------------------------

def generate_learning_material(pdf_text, topic, co, bloom, difficulty):

    prompt = f"""
You are an expert university professor.

Using the academic context below, generate detailed learning material.

ACADEMIC CONTEXT:
{pdf_text}

Topic:
{topic}

Course Outcome:
{co}

Bloom Level:
{bloom}

Difficulty:
{difficulty}

Generate:

1. Introduction

2. Concepts

3. Explanation

4. Examples

5. Advantages

6. Applications

7. Summary

Make it easy to understand for students.
"""

    return ask_ollama(prompt)


# ----------------------------------------------------
# MCQs
# ----------------------------------------------------

def generate_mcqs(pdf_text, topic, difficulty):

    prompt = f"""
Use the academic context below.

ACADEMIC CONTEXT:
{pdf_text}

Topic:
{topic}

Difficulty:
{difficulty}

Generate 10 Multiple Choice Questions.

Each MCQ must contain:

Question

A)

B)

C)

D)

Correct Answer

Explanation
"""

    return ask_ollama(prompt)


# ----------------------------------------------------
# Assignment Questions
# ----------------------------------------------------

def generate_assignments(pdf_text, topic):

    prompt = f"""
Use the academic context below.

ACADEMIC CONTEXT:
{pdf_text}

Topic:
{topic}

Generate:

5 Assignment Questions.

Include:

• Short Questions

• Long Questions

• Application Based Questions
"""

    return ask_ollama(prompt)


# ----------------------------------------------------
# Learning Activities
# ----------------------------------------------------

def generate_activities(pdf_text, topic):

    prompt = f"""
Use the academic context below.

ACADEMIC CONTEXT:
{pdf_text}

Topic:
{topic}

Generate 3 classroom learning activities.

For each activity provide:

Activity Name

Objective

Procedure

Expected Learning Outcome
"""

    return ask_ollama(prompt)