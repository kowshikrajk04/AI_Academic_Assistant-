import ollama

from utils.prompt_builder import PromptBuilder


class AnswerKeyGenerator:

    def __init__(self, model="gemma3:latest"):
        self.model = model


    def generate(
        self,
        question_paper,
        syllabus_text=""
    ):

        prompt = PromptBuilder.build_answer_key_prompt(
            question_paper
        )

        try:

            response = ollama.chat(

                model=self.model,

                messages=[

                    {
                        "role": "system",

                        "content":
                        """
You are an experienced Anna University Professor.

Generate accurate answer keys for university examination papers.

Rules:

• Answer every question.

• Part A should contain short answers.

• Part B should contain detailed answers.

• Include examples wherever possible.

• Include diagrams if required.

• Include algorithms for programming questions.

• Include code snippets where applicable.

• Use only the uploaded syllabus.

• Maintain university standards.

• Return only the Answer Key.
                        """
                    },

                    {
                        "role": "user",
                        "content": prompt
                    }

                ]

            )

            return response["message"]["content"]

        except Exception as e:

            return f"Error : {str(e)}"