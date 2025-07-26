from ..models.llm import gemini as llm
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
import re
from typing import Dict, List, Optional
from dataclasses import dataclass

# Prompt template with 5 difficulty levels
prompt_template = """
You are an expert educator tasked with creating a multiple-choice question for the skill '{skill_name}'.
Use the skill level {skill_level} (where 1 = absolute beginner, 5 = expert) to determine the difficulty of the question.

Guidelines:
1. Create a clear, concise question appropriate for level {skill_level}:
   - Level 1: Very basic facts or recognition 
   - Level 2: Basic application 
   - Level 3: Intermediate concepts 
   - Level 4: Advanced logic and problem solving 
   - Level 5: Expert-level reasoning or implementation 
2. Ensure the question is **different** from the previous one: '{previous_question}'
3. Provide four answer options (A, B, C, D) — all should be plausible but only one must be correct.
4. Specify the correct answer (e.g., '**Correct Answer: B**').

Use this format exactly:

**Question:** [Your question here]  
**Options:**  
A. [Option A]  
B. [Option B]  
C. [Option C]  
D. [Option D]  
**Correct Answer:** [Letter]
"""

# Prompt and chain setup
prompt = ChatPromptTemplate.from_template(prompt_template)
chain = prompt | llm | StrOutputParser()

# MCQ data structure
@dataclass
class MCQ:
    number: int
    question: str
    options: Dict[str, str]
    correct_answer: str

# Parse LLM output into MCQ object
def parse_output(output: str, number: int) -> Optional[MCQ]:
    try:
        question_match = re.search(r"\*\*Question:\*\*\s*(.+)", output)
        options_matches = re.findall(r"([A-D])\. (.+)", output)
        answer_match = re.search(r"\*\*Correct Answer:\*\*\s*([A-D])", output)

        if not (question_match and options_matches and answer_match):
            raise ValueError("Output format is incorrect")

        question = question_match.group(1).strip()
        options = {opt: text.strip() for opt, text in options_matches}
        correct_answer = answer_match.group(1).strip()

        return MCQ(
            number=number,
            question=question,
            options=options,
            correct_answer=correct_answer
        )
    except Exception as e:
        print(f"❌ Error parsing question {number}: {e}")
        return None

# Generate one MCQ using the LLM
def generate_question(skill_name: str, skill_level: float, previous_question: str, number: int) -> Optional[MCQ]:
    try:
        raw_output = chain.invoke({
            "skill_name": skill_name,
            "skill_level": skill_level,
            "previous_question": previous_question
        })
        return parse_output(raw_output, number)
    except Exception as e:
        print(f"❌ Error generating question {number}: {e}")
        return None

# Generate N unique MCQs
def generate_questions(skill_name: str, skill_level: float, num_questions: int = 10) -> List[MCQ]:
    questions = []
    previous_questions = set()
    retry_limit = 50  # to avoid infinite loop
    attempts = 0

    while len(questions) < num_questions and attempts < retry_limit:
        attempts += 1
        number = len(questions) + 1
        prev_q = questions[-1].question if questions else "N/A"

        mcq = generate_question(skill_name, skill_level, prev_q, number)

        if mcq and mcq.question not in previous_questions:
            questions.append(mcq)
            previous_questions.add(mcq.question)
            print(f"✅ Added Question {number}")
        else:
            print(f"🔁 Retrying (current: {len(questions)}/{num_questions})...")

    if len(questions) < num_questions:
        raise Exception(f"Failed to generate {num_questions} unique questions after {attempts} attempts.")
    return questions

# Print MCQs nicely
def print_questions(questions: List[MCQ], skill_name: str, skill_level: float):
    print(f"\n🧠 Skill: {skill_name} | Difficulty Level: {skill_level}\n")
    for q in questions:
        print(f"{q.number}. {q.question}")
        for key in ['A', 'B', 'C', 'D']:
            print(f"   {key}. {q.options.get(key, 'N/A')}")
        print(f"   ✅ Correct Answer: {q.correct_answer}\n")

# === MAIN RUN ===
if __name__ == "__main__":
    skill_name = "Computer Graphics"
    skill_level = 5  # You can change from 1 to 5

    try:
        questions = generate_questions(skill_name, skill_level, num_questions=10)
        print_questions(questions, skill_name, skill_level)
    except Exception as e:
        print(f"\n❌ Failed: {e}")
