import ollama

from utils.prompt_builder import PromptBuilder


class QuestionPaperGenerator:

    def __init__(self, model="gemma3:latest"):
        self.model = model


    def generate(
        self,
        syllabus_text,
        parsed_data,
        academic_year,
        exam_name,
        exam_date,
        session,
        duration,
        maximum_marks,
        difficulty,
        bloom_level,
        rag_engine=None
    ):

        # Determine the context to use
        context_text = syllabus_text
        if rag_engine is not None:
            qp_chunks = []
            seen_chunks = set()
            units = parsed_data.get("units", {})
            
            # Query the RAG engine for each unit to cover the entire course syllabus
            for unit_name, unit_topics in units.items():
                # Form a search query combining unit name and first few topics
                query_str = f"{unit_name} " + " ".join(unit_topics[:5])
                results = rag_engine.query(query_str, top_k=2)
                for res in results:
                    chunk_text = res["chunk"]["text"]
                    if chunk_text not in seen_chunks:
                        seen_chunks.add(chunk_text)
                        qp_chunks.append(res["chunk"])
            
            if qp_chunks:
                context_parts = []
                for chunk in qp_chunks:
                    header = f"[{chunk['type']} | Source: {chunk['source']} | Page {chunk['page']}]"
                    context_parts.append(f"{header}\n{chunk['text']}")
                context_text = "\n\n=========================================\n".join(context_parts)

        prompt = PromptBuilder.build_question_paper_prompt(
            syllabus_text=context_text,

            course_name=parsed_data["course_name"],

            course_code=parsed_data["course_code"],

            department=parsed_data["department"],

            semester=parsed_data["semester"],

            academic_year=academic_year,

            exam_name=exam_name,

            exam_date=exam_date,

            session=session,

            duration=duration,

            maximum_marks=maximum_marks,

            course_outcomes=parsed_data["course_outcomes"],

            difficulty=difficulty,

            bloom_level=bloom_level
        )

        import random

        # Generate a unique session token for this specific run to guarantee output variance
        generation_seed = random.randint(1, 1000000)
        prompt_with_seed = f"{prompt}\n\n[Generation Seed ID: {generation_seed}]"

        try:

            response = ollama.chat(

                model=self.model,

                messages=[
                    {
                        "role": "system",
                        "content":
                        f"""
                        You are an experienced Anna University
                        Question Paper Setter.

                        Always generate professional
                        university examination papers.

                        Follow the format exactly.

                        Never generate questions
                        outside the syllabus.

                        Generation reference: {generation_seed}
                        """
                    },

                    {
                        "role": "user",
                        "content": prompt_with_seed
                    }

                ],
                options={
                    "temperature": 0.8,
                    "seed": generation_seed
                }

            )

            return response["message"]["content"]

        except Exception as e:

            return f"Error : {e}"