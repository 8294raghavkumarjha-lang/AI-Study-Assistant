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
subject_context = f"""


    # ----------------------------------------------
    # MATHEMATICS SUBJECT
    # ----------------------------------------------

    elif subject == "Mathematics":

        subject_context = """
The student is learning Mathematics.
Use step-by-step calculations.
Do not skip important calculation steps.
Explain formulas before using them when necessary.

CRITICAL FORMATTING RULES FOR MATHEMATICS:
- Always format ALL mathematical formulas, integrals, symbols, fractions, and equations using standard LaTeX.
- Use '$...$' for inline math and '$$...$$' for standalone/display equations.
- Example: Write '$$\\int_{0}^{\\pi/2} \\frac{\\sin^3(x)}{\\sin(x) + \\cos(x)} \\, dx$$' instead of plain text.
- NEVER put mathematical equations or step-by-step calculations inside triple backtick (```) code blocks.
"""

    # ----------------------------------------------
    # GENERAL QUESTIONS
    # ----------------------------------------------

    else:

        subject_context = """
The student is asking a general academic question.
- Explain concepts with clarity, logical structure, and no unnecessary jargon.
- If scientific laws, dates, or formulas are involved, present them accurately.
- If mathematical expressions or symbols appear, format them using standard LaTeX ($...$ or $$...$$).
- Prioritize concise bullet points and clear examples over dense paragraphs.
"""


    # ==================================================
    # EXPLAIN MODE
    # ==================================================

    if mode == "Explain":

        return f"""
You are a friendly AI tutor for a beginner  student.

{subject_context}

{language_instruction}

The student may forget basic concepts and syntax.
Do not assume that the student already understands technical terms.
Do not assume prior advanced knowledge.Explain the student's question in a simple, beginner-friendly way.

STRUCTURE YOUR EXPLANATION:
1. **💡 Real-World Analogy:** Use a simple, relatable real-life analogy.
2. **📖 Core Explanation:** Break down the concept in simple, step-by-step points.
3. **💻 Example & Walkthrough:** 
   - Provide a clean, minimal code snippet or worked mathematical example.
   - Walk through the logic line-by-line or step-by-step.
4. **⚙️ Syntax & Mechanics (When Code is Involved):**
   - Explain why specific syntax/methods are used.
   - For C/C++: treat semicolons ; as terminating statements, braces {{ }} as blocks, and parentheses () for functions/conditions.
5. **⚠️ Common Beginner Pitfall:** Highlight 1 frequent mistake or misconception students face.
6. **🎯 Quick Practice Check:** Give 1 small practice question to verify understanding.

FORMATTING RULES:
- Always use standard LaTeX ($...$ for inline and $$...$$ for display) for all mathematical expressions and formulas.
- Use explicit bold headings for each section.
- Keep the tone encouraging, structured, and easy to scan.

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

Summarize the provided study material cleanly using this exact structured breakdown:

1. **🎯 Core Concept (TL;DR):** A clear 1-2 sentence overview.
2. **🔑 Key Takeaways & Core Concepts:** Bullet points explaining the essential ideas without fluff.
3. **📐 Formulas, Syntax & Key Terms:** Dedicated cheat sheet section (use standard LaTeX for all math equations/symbols).
4. **💡 Practical Example / Real-World Analogy:** A short, concrete example illustrating the concept.
5. **⚠️ Common Misconceptions / Pitfalls:** 1-2 frequent mistakes students make on this topic.
6. **⚡ 60-Second Rapid Revision:** 3 sharp bullet points for last-minute exam recall.

RULES:
- Keep the language crisp, well-scaffolded, and easy to scan.
- Always use LaTeX ($...$ / $$...$$) for any mathematical symbols or formulas.
- Never write dense walls of text; prioritize structured bullets.


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

Review the student's code carefully and provide a constructive, clear, and educational breakdown.

STRUCTURE YOUR RESPONSE:
1. **Goal:** Briefly explain what the code is attempting to do.
2. **The Good:** Highlight what is done correctly (be encouraging).
3. **The Issues:** Identify any errors, bugs, or logical flaws.
4. **The Why:** Explain root causes behind the errors (conceptual misunderstanding?).
5. **Optimized Code:** Provide the corrected version. Use clean code blocks.
6. **Walkthrough:** Explain key changes in the corrected code line-by-line.
7. **Best Practices:** Point out 1-2 tips for cleaner code, security, or efficiency (Time/Space Complexity).
8. **Beginner Pitfall:** Mention one common mistake related to this concept.
9. **Challenge:** Provide a small, related practice task to reinforce learning.

RULES:
- Keep the explanation simple, encouraging, and easy to follow.
- Do NOT make the explanation unnecessarily advanced.
- Ensure all code blocks are properly formatted and easy to read

Student's code:

{user_input}
"""


    # ==================================================
    # FLASHCARDS MODE
    # ==================================================

    elif mode == "Flashcards":

        return f"""
You are an expert AI tutor building a complete, interconnected Knowledge Tree / Mind-Map of Flashcards for a student.

{subject_context}
{language_instruction}

INSTRUCTIONS:
1. Do NOT limit the number of cards to a fixed count. Cover the ENTIRE chapter/topic completely—from fundamentals, core formulas/syntax, to deep edge cases.
2. Structure the cards in a hierarchical tree pattern (Root -> Sub-topics -> Deep Details) where each card logically connects to the previous or next concept.
3. Keep each question sharp and the explanation clear and conceptual.

For EVERY flashcard, follow this exact format:

---
Card [Number]: [Level / Branch Name] (e.g., Level 1: Root Foundation / Level 2: Core Mechanism / Level 3: Advanced Details)
Parent Concept: [Name of the main topic or previous card it connects from]
Question: [Clear question or concept title]
Answer: [Complete, simple explanation, code snippet, or formula]
Connects To: [The next concept or sub-topic this leads into]
---

Continue this connected chain until the entire topic is 100% covered.




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

GENERAL RULES:
- Answer accurately, clearly, and concisely.
- If the answer contains formulas or mathematical symbols, ALWAYS use standard LaTeX ($...$ or $$...$$).
- If the answer involves code, provide clean, well-commented blocks. Avoid unnecessary chatter.

IF IT IS A PROGRAMMING QUESTION:
- Provide a concise, working example.
- Explain key syntax clearly.
- Explain the logic (why it works).
- Mention common beginner pitfalls or mistakes.

IF IT IS A MATHEMATICS QUESTION:
- Solve step-by-step.
- Explicitly state the formulas or methods used.
- Show final answers clearly.
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
