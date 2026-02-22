import streamlit as st
from datetime import date
import requests
import random
import os




# CONFIG
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")

if not OPENROUTER_API_KEY:
    st.error("❌ OPENROUTER_API_KEY not found")
    st.stop()

MODEL = "google/gemma-3n-e4b-it:free"

st.set_page_config(page_title="PassMate", page_icon="📘", layout="wide")

# ================= AI FUNCTION =================
def generate(prompt, temp):
    try:
        r = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "http://localhost",
                "X-Title": "PassMate"
            },
            json={
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": temp,
                "max_tokens": 4096
            },
            timeout=120
        )

        data = r.json()

        if "choices" not in data:
            st.error(data)
            st.stop()

        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        st.error(f"OpenRouter Error: {e}")
        st.stop()

# ================= UI =================
st.title("📘 PassMate – AI Study Planner")

student_class = st.selectbox(
    "Class / Level",
    ["Class 9","Class 10","Class 11","Class 12","UG","PG"]
)

exam_date = st.date_input("Exam Date", min_value=date.today())
subjects = st.text_input("Subjects (comma separated)")
hours = st.slider("Study Hours Per Day", 1, 12, 4)
hobbies = st.text_input("Your Hobbies")
study_style = st.selectbox(
    "Study Style",
    ["Pomodoro","Deep sessions","Mixed","Visual","Practice"],
    index=2
)

submit = st.button("✨ Generate Study Plan")

# ================= ON SUBMIT =================
if submit:

    if not subjects.strip():
        st.warning("Enter subjects"); st.stop()

    remaining_days = (exam_date - date.today()).days - 1

    if remaining_days <= 0:
        st.warning("Pick future exam date"); st.stop()

    with st.spinner("Creating your personalized plan..."):

        motivation = generate(f"""
Write ONE warm motivational line for a {student_class} student.
""",0.8)

        plan = generate(f"""
You are a calm, friendly study mentor.

Student:
Class: {student_class}
Subjects: {subjects}
Days: {remaining_days}
Hours/day: {hours}
Hobbies: {hobbies}
Style: {study_style}

Rules:

• EXACTLY {remaining_days} days
• {hours} hours per day
• Final day revision only
• Markdown headings ### Day 1 etc
• Bullet sessions
• Human tone

Formatting:

• Each day heading
• Morning / Afternoon / Evening blocks
• Blank lines
• Horizontal dividers ---

Tone:

Warm, motivating, human.

End with short uplifting message.
""",0.4)

    st.success(motivation)
    st.markdown(plan)

    st.info(random.choice([
        "Progress beats perfection.",
        "Your future self will thank you.",
        "Consistency creates confidence.",
        "Small steps daily = big results."
    ]))