# AI-Powered Skill Assessment & Personalized Learning Plan Agent

## Overview

Resumes often reflect what candidates *claim* to know, but not how well they actually understand those skills.
This project solves that gap by building an **AI-powered agent** that evaluates real proficiency through an adaptive interview and generates a **personalized learning roadmap**.

---

## Problem Statement

Given a **Job Description (JD)** and a **candidate’s resume**, build a system that:

* Assesses real skill proficiency conversationally
* Identifies skill gaps
* Generates a personalized learning plan with actionable steps

---

## Solution Approach

Instead of relying only on static resume analysis, this system introduces an **adaptive AI interviewer**.

###  Core Idea

1. Analyze resume vs job requirements
2. Ask targeted questions
3. Evaluate answers in real-time
4. Adapt interview difficulty dynamically
5. Recommend what to learn next

---

##  Key Features

###  Resume & Job Description Analysis

* Extracts required skills from JD
* Analyzes candidate profile using LLM
* Identifies matched and missing skills

---

### Adaptive AI Interview Agent

* Generates skill-based interview questions
* Dynamically adjusts difficulty:

  * Low score → easier questions
  * High score → deeper/advanced questions
* Simulates real interview behavior

---

### Intelligent Scoring System

* Evaluates answers based on:

  * correctness
  * clarity
  * depth
* Produces:

  * score (0–10)
  * feedback
  * improvement suggestions

---

### Skill Gap Identification

* Tracks performance per skill
* Identifies weakest areas

---

### Personalized Learning Roadmap

* Focuses on weakest skills
* Generates:

  * root cause of weakness
  * bridge skills
  * structured 3-week plan
  * curated resources

---

## System Architecture
This system is designed as an end-to-end AI-driven pipeline that transforms a static resume into an interactive skill assessment and learning experience. It begins with a Streamlit-based frontend where the user uploads a resume and provides a job description. The resume is parsed to extract relevant candidate information, while the job description is analyzed to identify required skills and expectations. These inputs are then processed by an LLM-powered analysis engine, which compares the candidate’s profile with job requirements to generate a skill match and gap analysis. Based on the identified gaps, the system dynamically generates interview questions and initiates an adaptive interview process, where the difficulty of questions adjusts in real time according to the candidate’s performance. Each response is evaluated using the LLM based on correctness, clarity, and depth, producing a score along with detailed feedback. The system aggregates these results to identify weak skill areas and finally generates a personalized learning roadmap, including reasons for gaps, bridge skills, structured weekly plans, and curated resources. This architecture ensures a seamless flow from assessment to improvement, making the system both evaluative and developmental rather than just a static screening tool.

<img width="1536" height="1024" alt="Architecture_diagram" src="https://github.com/user-attachments/assets/dfb3e589-ba56-4e2a-85dd-c1a136ce0433" />


### Pipeline

```
Resume + Job Description
          ↓
AI Analysis (LLM)
          ↓
Interview Question Generator
          ↓
Adaptive Interview Agent (Dynamic Loop)
          ↓
Answer Evaluation & Scoring
          ↓
Skill Gap Identification
          ↓
Personalized Learning Plan
```

---

## How It Works

### 1. Input

* Upload resume (PDF)
* Paste job description

---

### 2. AI Analysis

* Extract skills from JD
* Compare with resume
* Identify skill gaps

---

### 3. Adaptive Interview

* Generate 3–5 questions
* Adjust next question based on performance

---

### 4. Evaluation

* Score each answer (0–10)
* Provide feedback and improvements

---

### 5. Learning Plan

* Identify weakest skills
* Generate personalized roadmap

---

## Design Decisions & Trade-offs

| Decision                        | Reason                                             |
| ------------------------------- | -------------------------------------------------- |
| LLM-based evaluation            | Provides human-like reasoning & feedback           |
| Keyword-based skill mapping     | Faster and more reliable for real-time interaction |
| Structured 3-week learning plan | Keeps output concise and actionable                |
| Streamlit UI                    | Rapid prototyping and usability                    |

---

## Tech Stack

* **Python**
* **Streamlit** (UI & App)
* **Groq LLM API** (AI reasoning & evaluation)
* **PDFPlumber** (Resume parsing)
* **Regex** (Text processing)

---

## Running the Project Locally

### 1. Clone Repository

```bash
git clone <your-repo-link>
cd <project-folder>
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set API Key

**Windows (PowerShell):**

```bash
$env:GROQ_API_KEY="your_api_key_here"
```

**Mac/Linux:**

```bash
export GROQ_API_KEY="your_api_key_here"
```

### 4. Run Application

```bash
streamlit run app.py
```

---

## Demo Video

https://drive.google.com/file/d/12EJuxLphl2DfIniL_-ZzHgBSB6l2dEuH/view?usp=drive_link

---

## Deployed URL
https://ai-skill-assessment-agent-4cvq7ramkp4ypichknl6na.streamlit.app/

---
## Sample Outputs

### AI Analysis

* Candidate summary
* Skill match vs gap

### Interview

* Dynamic question flow
* Real-time scoring

### Learning Plan

* Personalized roadmap
* Weekly breakdown

(Add screenshots here)

---

## Future Improvements

* Semantic skill matching using embeddings
* Multi-turn conversational memory
* Domain-specific evaluation tuning
* Progress tracking dashboard

---

##  Author

**Kavya Kosaraju**
B.E. Information Technology
Hyderabad, India

---

##  Final Note

This project demonstrates how AI can move beyond static resume screening to **actively evaluate real skills and guide candidates toward improvement**, making hiring and learning more intelligent and effective.
