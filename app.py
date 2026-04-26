import streamlit as st
import pdfplumber
import re
from groq import Groq
import os

import traceback



st.markdown("""
<style>

/*  REMOVE HEADER */
header[data-testid="stHeader"] {
    background: transparent !important;
}

/*  SKY BLUE BACKGROUND */
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #38bdf8, #60a5fa, #3b82f6) !important;
}

/* remove default background */
.stApp {
    background: transparent;
}

/*  GLASS EFFECT CONTAINERS */
[data-testid="stFileUploader"],
[data-testid="stTextArea"],
[data-testid="stTextInput"] {
    background: rgba(255, 255, 255, 0.25) !important;
    border-radius: 16px !important;
    padding: 15px !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.4);
}

/*  INPUT FIELDS */
textarea, input {
    background: rgba(255,255,255,0.95) !important;
    color: black !important;
    border-radius: 10px !important;
}

/*  MAIN BUTTONS */
.stButton>button {
    background: linear-gradient(135deg, #2563eb, #1d4ed8) !important;
    color: white !important;
    border-radius: 12px;
    padding: 12px 20px;
    border: none;
    font-weight: 600;
    font-size: 15px;
    transition: 0.3s;
}

.stButton>button:hover {
    transform: scale(1.05);
    box-shadow: 0 8px 25px rgba(29, 78, 216, 0.4);
}

/* 🔄 RESET BUTTON */
.stButton>button[kind="secondary"] {
    background: rgba(255,255,255,0.4) !important;
    color: black !important;
    border: 1px solid rgba(255,255,255,0.6);
}

/*  UPLOAD DROPZONE */
[data-testid="stFileUploaderDropzone"] {
    background: rgba(255,255,255,0.2) !important;
    border: 2px dashed rgba(255,255,255,0.6) !important;
    border-radius: 15px;
    padding: 20px;
}

/*  UPLOAD BUTTON */
[data-testid="stFileUploader"] button {
    background: rgba(255,255,255,0.5) !important;
    color: black !important;
    border-radius: 10px;
    border: 1px solid rgba(255,255,255,0.6);
}

/* upload text */
[data-testid="stFileUploader"] label {
    color: black !important;
}

/* helper text */
[data-testid="stFileUploader"] small {
    color: #1e3a8a !important;
}

/*  TEXT */
h1, h2, h3 {
    color: #0f172a !important;
}

p, label {
    color: #1e293b !important;
}

/* spacing fix */
.block-container {
    padding-top: 1rem;
}

</style>
""", unsafe_allow_html=True)






#  Secure API key (set in terminal)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

#  ADD HERE (RIGHT AFTER CLIENT)
def match_skill_semantically(question, jd_skills):
    question = question.lower()

    for skill in jd_skills:
        if skill.lower() in question:
            return skill

    return jd_skills[0] if jd_skills else "General"

#  Session State Initialization
if "report" not in st.session_state:
    st.session_state.report = ""

if "questions" not in st.session_state:
    st.session_state.questions = []

if "start_interview" not in st.session_state:
    st.session_state.start_interview = False

if "current_q" not in st.session_state:
    st.session_state.current_q = 0

if "score" not in st.session_state:
    st.session_state.score = 0

if "answers_review" not in st.session_state:
    st.session_state.answers_review = []

if "skill_scores" not in st.session_state:
    st.session_state.skill_scores = {}

#  STEP 1: Read PDF
def read_pdf(file):
    text = ""
    with pdfplumber.open(file) as pdf:
        for page in pdf.pages:
            extracted = page.extract_text()
            if extracted:
                text += extracted + "\n"

    text = text.replace("•", "\n•")
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)

    return text

def extract_skills_from_jd(jd_text):
    prompt = f"""
Extract the main skills required in this job description.

Return ONLY a list (max 6 skills).
Each skill must be 1–3 words.
No explanation.

Job Description:
{jd_text}
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    skills = response.choices[0].message.content.strip().split("\n")

    return [s.strip("- ").strip() for s in skills if s.strip()]

#  STEP 2: AI Analysis
def analyze_with_ai(resume_text, jd_text):
    prompt = f"""
You are an expert AI recruiter.

Analyze the resume and job description carefully and produce a clean, professional, structured output.

IMPORTANT RULES (STRICT):
- Do NOT repeat any headings
- Do NOT mix sections
- Do NOT duplicate the same work in multiple sections
- Keep formatting clean and readable
- If unsure, prioritize accuracy over guessing

-------------------------------------

STRUCTURE YOUR OUTPUT EXACTLY LIKE THIS:



Candidate Information
- Name:
- Contact Information:
- Objective:

-------------------------------------

Candidate Skills (all categories)

IMPORTANT:
- Display skills in ONE LINE per category
- Format MUST be:

Programming: Java, Python, C  
Web Development: HTML, CSS, JavaScript  
Database: SQL  
Cloud & Tools: Firebase, VS Code, Git, Jupyter Notebook  
Core CS: DSA, OOPs, Computer Networks, Software Engineering  
AI/ML: Machine Learning, Deep Learning, NLP  
Soft Skills: Problem Solving, Teamwork, Communication, Adaptability, Time Management  
Languages: English, Hindi, Telugu  

DO NOT:
- Use bullet points
- Use new lines for each skill
- Use symbols like "|"

-------------------------------------

Education
- Degree, College, Location (Year) – Score/Percentage

-------------------------------------

Projects (ONLY personal/academic projects)
1. Project Name
- Description (2 lines max)

-------------------------------------

Internship/Experience (ONLY real-world work)
1. Role, Company, Location (Duration)
- Responsibilities and work done (clear bullet points)

IMPORTANT:
- If project was done during internship → include ONLY here
- If multiple roles (Intern + Team Lead) → merge into ONE entry

-------------------------------------

Required Skills (from Job Description)
- List important required skills clearly

-------------------------------------

Skill Gap Analysis (what is missing)
- List ONLY missing or weak skills
- Do NOT repeat skills candidate already has

-------------------------------------

Interview Questions (3–5)
- Ask questions specifically to test missing or important skills

-------------------------------------

Learning Plan (PERSONALIZED)

For EACH gap, include:
- Skill to learn
- Time estimate (in days/weeks)
- Resource (YouTube / Docs / Course)

Example format:
Skill: Salesforce Declarative Functions  
Time: 2 weeks  
Resource: Salesforce Trailhead  

-------------------------------------

Resume:
{resume_text}

Job Description:
{jd_text}
"""
    
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content   


def evaluate_answer(question, answer):
    prompt = f"""
You are an AI interviewer.

Evaluate the candidate's answer in a realistic and balanced way.

SCORING RULES:
- 8–10 → Strong, clear, correct, with examples
- 6–7 → Good understanding but missing depth or clarity
- 4–5 → Partial understanding, vague or incomplete
- 0–3 → Incorrect or no knowledge

IMPORTANT:
- Do NOT be too strict
- Do NOT expect perfect answers
- Reward partial knowledge
- If candidate shows basic understanding → give at least 5+

Return ONLY:

Score: X
Feedback: short explanation

Also include:
Improvement: one clear suggestion to improve the answer

Question:
{question}

Answer:
{answer}
"""
   
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0
    )

    return response.choices[0].message.content 


def generate_adjacent_skill_plan(skill, candidate_profile, client):
    prompt = f"""
You are a senior career mentor.

Candidate Profile:
{candidate_profile}

Weak Skill: {skill}

Your job:
Analyze WHY the candidate is weak and give a realistic improvement plan.

STRICT FORMAT:

Why Weak:
<1–2 line reason>

Bridge Skills:
<skills they already have that can help>

Learning Plan:

Week 1:
- what to learn
- small goal

Week 2:
- what to learn
- practice task

Week 3:
- advanced concept or project

Resources:
- 1 YouTube or course
- 1 documentation

IMPORTANT:
- Be specific
- No generic answers
- Make it feel personalized
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.4
    )

    return response.choices[0].message.content

def generate_followup_question(skill, previous_answer, score):
    prompt = f"""
You are an AI interviewer.

Skill: {skill}
Previous Answer: {previous_answer}
Score: {score}/10

If score < 6:
- Ask an easier or foundational question

If score between 6-8:
- Ask a moderate depth question

If score > 8:
- Ask an advanced or scenario-based question

Return ONLY the next question.
"""

    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3
    )

    return response.choices[0].message.content.strip()

#  UI
st.set_page_config(page_title="AI Skill Assessment Agent", layout="wide")


st.title(" AI Skill Assessment & Learning Plan Agent")

# Reset Button
if st.button("🔄 Reset"):
    st.session_state.clear()
    st.rerun()

st.write("Upload your resume and paste the job description to get AI analysis.")

# Inputs
resume = st.file_uploader(" Upload Resume (PDF)", type=["pdf"])
jd = st.text_area(" Paste Job Description", height=200)


#  Start Analysis
if st.button("Start Assessment") and not st.session_state.get("report"):
    if resume is not None and jd.strip() != "":
        with st.spinner("🤖 AI is analyzing... please wait..."):
            resume_text = read_pdf(resume)
            st.session_state.resume_text = resume_text
            st.session_state.jd_text = jd
            st.session_state.jd_skills = extract_skills_from_jd(jd)
            result = analyze_with_ai(resume_text, jd)

        st.session_state.report = result

        import re

        questions = []

        if st.session_state.get("report"):
            match = re.search(
                r'Interview Questions.*?\n(.*?)\n\s*Learning Plan',
                st.session_state.report,
                re.DOTALL
            )

            if match:
                raw_questions = match.group(1)

                questions = [
                    q.strip("•- 1234567890. ")
                    for q in raw_questions.split("\n")
                    if q.strip()
                ]

        st.session_state.questions = questions[:5]

        st.success("Analysis Complete!")

    else:
        st.warning(" Please upload resume and enter job description")


#  Show Report
if st.session_state.report:
    st.subheader("📊 AI Analysis Result")
    st.markdown(st.session_state.report)

    #  ADD THIS BUTTON
    if st.button(" Start Interview"):
        st.session_state.start_interview = True
        st.session_state.current_q = 0
        st.session_state.score = 0
        st.rerun()


if st.session_state.start_interview:

    q_index = st.session_state.current_q

    if q_index < len(st.session_state.questions):
        
       
        #  If it's the first question → use original generated question
        question = st.session_state.questions[q_index]

        #  For next questions → use dynamically generated follow-up
        

        st.subheader(f"Question {q_index + 1} of {len(st.session_state.questions)}")
        st.write(question)
        
        default_answer = ""

        if "test_answers" in st.session_state:
            if q_index < len(st.session_state.test_answers):
                default_answer = st.session_state.test_answers[q_index]

        answer = st.text_area("Your Answer", key=f"ans_{q_index}")

        if st.button("Submit Answer"):

            if answer.strip() == "":
                st.warning("Enter answer")

            else:
                result = evaluate_answer(question, answer)

                score_match = re.search(r'Score:\s*(\d+)', result)
                feedback_match = re.search(r'Feedback:\s*(.*?)(?:\nImprovement:|$)', result, re.DOTALL)
                improvement_match = re.search(r'Improvement:\s*(.*?)(?:\n|$)', result, re.DOTALL)

                score = int(score_match.group(1)) if score_match else 0
                feedback = feedback_match.group(1) if feedback_match else ""
                improvement = improvement_match.group(1).strip() if improvement_match else ""

                #  STEP 1: DEFINE SKILL FIRST
                skill = match_skill_semantically(
                    question,
                    st.session_state.jd_skills
                )

                print("Question:", question)
                print("Final Skill:", skill)

                #  STEP 2: NOW generate follow-up
                if st.session_state.current_q < len(st.session_state.questions) - 1:
                    next_q = generate_followup_question(
                        skill,
                        answer,
                        score
                    )

                    st.session_state.questions[st.session_state.current_q + 1] = next_q

                # REMOVE DUPLICATE SENTENCES
                lines = improvement.split("\n")
                unique_lines = []

                for line in lines:
                    if line.strip() and line.strip() not in unique_lines:
                        unique_lines.append(line.strip())

                improvement = " ".join(unique_lines)

                
                
                #  NEW skill mapping using embeddings
                

                if skill not in st.session_state.skill_scores:
                    st.session_state.skill_scores[skill] = []

                st.session_state.skill_scores[skill].append(score)

                # store review
                st.session_state.answers_review.append({
                    "question": question,
                    "answer": answer,
                    "score": score,
                    "skill": skill,
                    "feedback": feedback,
                    "improvement": improvement
                })

                st.write(f"Score: {score}/10")
                st.write(f"Feedback: {feedback}")
                st.write(improvement)

                st.session_state.score += score
                st.session_state.current_q += 1

                st.rerun()

    else:
        st.success("Interview Completed")
        avg = st.session_state.score / len(st.session_state.questions)
        st.subheader(f"Final Score: {round(avg,1)} / 10")
   
        #  Personalized Learning Plan
        st.subheader(" Personalized Learning Roadmap (AI Generated)")

        #  Sort skills by lowest score
        sorted_skills = sorted(
            st.session_state.skill_scores.items(),
            key=lambda x: sum(x[1]) / len(x[1])
        )

        #  Take weakest 2 skills
        weak_skills = sorted_skills[:2]

        #  Show learning plan ONLY for weak skills
        for skill, scores in weak_skills:
            avg_skill = sum(scores) / len(scores)

            st.write(f" {skill} ({round(avg_skill,1)}/10)")

            plan = generate_adjacent_skill_plan(
                skill,
                st.session_state.report,
                client
            )
            st.info(plan)
            st.markdown("---")
        #  Skill-wise Performance
        st.subheader("📊 Skill-wise Performance")

        for skill, scores in st.session_state.skill_scores.items():
            avg_skill = sum(scores) / len(scores)
            st.write(f"{skill} → {round(avg_skill,1)} / 10")

        st.subheader(" Detailed Breakdown")
        for i, item in enumerate(st.session_state.answers_review):
            st.write(f"### Q{i+1}")
            st.write(item["question"])
            st.write(f"Score: {item['score']}")
            st.write("Feedback:", item["feedback"])
            st.write("Improvement:", item["improvement"])
            st.markdown("---")

        