import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq


# --------------------------------------------------
# 1. LOAD API KEY
# --------------------------------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")


# --------------------------------------------------
# 2. PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="AI Study Assistant",
    page_icon="📚"
)


# --------------------------------------------------
# 3. APP TITLE
# --------------------------------------------------

st.title("📚 AI Study Assistant")

st.write(
    "A beginner-friendly AI learning assistant for students."
)


# --------------------------------------------------
# 4. CHECK API KEY
# --------------------------------------------------

if not api_key:
    st.error(
        "GROQ_API_KEY is missing. Add it to your .env file."
    )
    st.stop()


# --------------------------------------------------
# 5. CREATE GROQ CLIENT
# --------------------------------------------------

client = Groq(
    api_key=api_key
)


# --------------------------------------------------
# 6. SIDEBAR SETTINGS
# --------------------------------------------------

st.sidebar.header("⚙️ Learning Settings")


# --------------------------------------------------
# 7. SUBJECT SELECTION
# --------------------------------------------------

subject = st.sidebar.selectbox(
    "Subject",
    [
        "Programming",
        "General Questions",
        "Mathematics"
    ]
)


# --------------------------------------------------
# 8. PROGRAMMING LANGUAGE
# --------------------------------------------------

programming_language = "Not applicable"

if subject == "Programming":

    programming_language = st.sidebar.selectbox(
        "Programming Language",
        [
            "C",
            "C++",
            "Python",
            "Java",
            "JavaScript",
            "C#",
            "Other"
        ]
    )


# --------------------------------------------------
# 9. LEARNING MODE
# --------------------------------------------------

mode = st.sidebar.selectbox(
    "Choose a mode",
    [
        "Explain",
        "Summarize",
        "Quiz",
        "Code Review",
        "Flashcards",
        "Ask AI"
    ]
)


# --------------------------------------------------
# 10. EXPLANATION LANGUAGE
# --------------------------------------------------

language = st.sidebar.selectbox(
    "Explanation Language",
    [
        "English",
        "Hindi",
        "Hinglish",
        "Urdu"
    ]
)


# --------------------------------------------------
# 11. CREATE LANGUAGE INSTRUCTION
# --------------------------------------------------

if language == "English":

    language_instruction = """
Use simple English.
Keep the explanation beginner-friendly.
"""

elif language == "Hindi":

    language_instruction = """
Explain in simple Hindi.
Keep programming keywords and important technical terms in English.
"""

elif language == "Hinglish":

    language_instruction = """
Explain in very simple Hindi-English (Hinglish).
Keep programming keywords, syntax and code terms in English.
"""

else:

    language_instruction = """
Explain in simple Urdu.
Keep programming keywords, syntax and important technical terms in English.
"""


# --------------------------------------------------
# 12. CREATE AI PROMPT
# --------------------------------------------------

def create_prompt(
    mode,
    subject,
    programming_language,
    language,
    user_input
):

    # ----------------------------------------------
    # PROGRAMMING SUBJECT
    # ----------------------------------------------

    if subject == "Programming":

        subject_context = f"""
The student is learning {programming_language}.
"""

    # ----------------------------------------------
    # MATHEMATICS SUBJECT
    # ----------------------------------------------

    elif subject == "Mathematics":

        subject_context = """
The student is learning Mathematics.
Use step-by-step calculations.
Do not skip important calculation steps.
Explain formulas before using them when necessary.
Do not use raw LaTeX commands like \\displaystyle, \\frac, or \\theta.
Write all formulas in simple, plain, readable text (e.g., sin^2(x) + cos^2(x) = 1, sec(x) = 1/cos(x)).
"""

    # ----------------------------------------------
    # GENERAL QUESTIONS
    # ----------------------------------------------

    else:

        subject_context = """
The student is asking a general academic question.
Explain the answer clearly and simply.
"""


    # ==================================================
    # EXPLAIN MODE
    # ==================================================

    if mode == "Explain":

        return f"""
You are a friendly AI tutor for a beginner   student.

{subject_context}

{language_instruction}

The student may forget basic concepts and syntax.
Do not assume that the student already understands technical terms.

Explain the student's question using:

1. A simple real-life analogy when useful.
2. A very simple explanation.
3. A small example.
4. Line-by-line explanation when code is involved.
5. Explain why the syntax or method is used.
6. Mention one common beginner mistake.
7. Give one small practice question.

For programming questions:

- Explain the syntax clearly.
- Explain why each important part is used.
- Give a small code example when useful.
- Explain the code line by line.
- Do not use unnecessarily advanced concepts.

For C programming, when relevant:

- Explain semicolon ; as terminating a statement.
- Explain braces {{ }} as a block/group of statements.
- Explain parentheses ( ) using simple function or condition examples.
- Explain indentation as a way to make code easier to read.

Never say that a semicolon means the end of a paragraph.
Use the technically correct term "statement".

Student question:

{user_input}
"""


    # ==================================================
    # SUMMARIZE MODE
    # ==================================================

    elif mode == "Summarize":

        return f"""
You are a helpful AI tutor for a beginner  student. 

{subject_context}

{language_instruction}

Summarize the following study material into easy revision notes.

Include:

- Main idea
- Important points
- Important formulas or syntax when relevant
- One small example if useful
- 3 quick revision points

Keep the notes short, clear and easy to revise.

Study material:

{user_input}
"""


    # ==================================================
    # QUIZ MODE
    # ==================================================

    elif mode == "Quiz":

        return f"""
You are a friendly {subject} teacher for a beginner student.

{subject_context}

{language_instruction}

Create a beginner-friendly practice quiz.

Create:

- If user specifies a number of question,generate exactly that many question. otherwise ,default to 5 multiple-choice questions
- 4 options for each question (A, B, C, D)
-  Dot NOT reveal the Answers and Explanation at the very bottom hidden inside a Markdown spoiler like:
 <details>
 <summary> click here to view Correct answer</summary>Explanation here.</details>
 1.Answer:
 2.Answer:
 3.Answer:
 4.Answer:
 - One-line explanation for each answer

Keep the questions appropriate for a beginner.

Topic:

{user_input}
"""


    # ==================================================
    # CODE REVIEW MODE
    # ==================================================

    elif mode == "Code Review":

        return f"""
You are a friendly {programming_language} programming tutor
for a beginner  student. 

{language_instruction}

Review the student's code carefully.

Explain:

1. What the code is trying to do.
2. What is correct in the code.
3. What errors or mistakes are present.
4. Why each mistake is happening.
5. The corrected code.
6. The corrected code line by line.
7. Important syntax used.
8. One common beginner mistake.
9. One small practice task.

Do not make the explanation unnecessarily advanced.

Student's code:

{user_input}
"""


    # ==================================================
    # FLASHCARDS MODE
    # ==================================================

    elif mode == "Flashcards":

        return f"""
You are a helpful AI tutor for a beginner   student.

{subject_context}

{language_instruction}

Create 10 beginner-friendly study flashcards
from the topic given below.

For every flashcard provide:

Card 1
Question:
Answer:

Card 2
Question:
Answer:

Continue until Card 10.

Keep the questions short.
Keep the answers simple and useful for revision.

Topic:

{user_input}
"""


    # ==================================================
    # ASK AI MODE
    # ==================================================

    else:

        return f"""
You are a helpful AI tutor for a beginner  student. 

{subject_context}

{language_instruction}

Answer the student's question accurately and simply.

If it is a programming question:

- Give a small example.
- Explain important syntax.
- Explain why the code works.
- Explain the code line by line when useful.
- Mention a common beginner mistake when useful.

If it is a mathematics question:

- Solve it step by step.
- Show important calculations.
- Explain the formula or method used.
- Clearly show the final answer.

Student question:

{user_input}
"""


# --------------------------------------------------
# 13. MAIN PAGE BASED ON MODE
# --------------------------------------------------

if mode == "Explain":

    st.subheader("💡 Learn a Concept Simply")

    placeholder = (
        "Example: C में braces { } क्यों लगाते हैं?"
    )


elif mode == "Summarize":

    st.subheader("📝 Make Revision Notes")

    placeholder = (
        "Paste your notes or study text here..."
    )


elif mode == "Quiz":

    st.subheader("🧠 Practice with a Quiz")

    placeholder = (
        "Example: C language loops"
    )


elif mode == "Code Review":

    st.subheader("🔍 Review Your Code")

    placeholder = (
        "Paste your C, C++ or Python code here..."
    )


elif mode == "Flashcards":

    st.subheader("🃏 Create Flashcards")

    placeholder = (
        "Example: C pointers"
    )


else:

    st.subheader("🤖 Ask Your AI Tutor")

    placeholder = (
        "Example: What is a pointer in C?"
    )


# --------------------------------------------------
# 14. USER INPUT
# --------------------------------------------------

user_input = st.text_area(
    "Enter your question, topic or code:",
    height=180,
    placeholder=placeholder
)


# --------------------------------------------------
# 15. GENERATE BUTTON
# --------------------------------------------------

if st.button(
    "✨ Generate",
    use_container_width=True
):

    # ----------------------------------------------
    # CHECK EMPTY INPUT
    # ----------------------------------------------

    if not user_input.strip():

        st.warning(
            "Please enter a question, topic or code first."
        )

        st.stop()


    # ----------------------------------------------
    # CREATE PROMPT
    # ----------------------------------------------

    prompt = create_prompt(
        mode,
        subject,
        programming_language,
        language,
        user_input
    )


    # ----------------------------------------------
    # CALL GROQ + GET RESPONSE
    # ----------------------------------------------

    with st.spinner(
        "🤖 AI is preparing your answer..."
    ):

        try:

            response = client.chat.completions.create(
                model="openai/gpt-oss-120b",
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.3
            )


            # --------------------------------------
            # GET AI ANSWER
            # --------------------------------------

            answer = response.choices[0].message.content


            # --------------------------------------
            # DISPLAY RESPONSE
            # --------------------------------------

            st.divider()

            st.subheader(
                "🤖 AI Tutor Response"
            )

            st.write(answer)


        # ------------------------------------------
        # ERROR HANDLING
        # ------------------------------------------

        except Exception as e:

            st.error(
                "Something went wrong while contacting the AI model."
            )

            st.caption(
                str(e)
            )


# --------------------------------------------------
# 16. FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "AI Study Assistant • Python + Streamlit + Groq +openai/gpt-oss-120b "
)