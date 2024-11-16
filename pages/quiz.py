import streamlit as st
from langchain_ibm import WatsonxLLM
import json

# Initialize WatsonX
@st.cache_resource
def init_watsonx():
    try:
        credentials = {
            "url": st.secrets["WATSONX_URL"],
            "apikey": st.secrets["WATSONX_APIKEY"]
        }
        project_id = st.secrets["WATSONX_PROJECT_ID"]
        
        return WatsonxLLM(
            model_id="ibm/granite-3-8b-instruct",
            url=credentials.get("url"),
            apikey=credentials.get("apikey"),
            project_id=project_id
        )
    except Exception as e:
        st.error(f"Error initializing WatsonX: {str(e)}")
        return None

# Quiz generation function
def generate_quiz(role: str, topic: str, llm) -> dict:
    prompt = f"""Generate 5 multiple choice questions about {topic} for a {role} role.
    Format the response as a JSON with the following structure:
    {{
        "questions": [
            {{
                "question": "question text",
                "options": ["A) option1", "B) option2", "C) option3", "D) option4"],
                "correct": "A"
            }}
        ]
    }}
    """
    try:
        response = llm(prompt)
        return json.loads(response)
    except Exception as e:
        st.error(f"Error generating quiz: {str(e)}")
        return None

st.title("🎯 Knowledge Assessment")

# Role and topic selection
roles = ["Backend Development", "Frontend Development", "Software Engineering", 
         "Cybersecurity", "Digital Marketing", "Android Development"]
selected_role = st.selectbox("Select your role:", roles)

topics = {
    "Common": ["Python Basics", "Git", "Data Structures", "OOP"],
    "Backend Development": ["Django", "Databases", "API Design"],
    "Frontend Development": ["HTML/CSS", "React", "UI/UX"],
    # Add topics for other roles
}

selected_topic = st.selectbox(
    "Select topic:", 
    topics["Common"] + topics.get(selected_role, [])
)

if st.button("Start Quiz"):
    llm = init_watsonx()
    if llm:
        with st.spinner("Generating quiz questions..."):
            quiz_data = generate_quiz(selected_role, selected_topic, llm)
            
            if quiz_data:
                st.session_state.quiz = quiz_data
                st.session_state.answers = {}
                st.session_state.submitted = False

if 'quiz' in st.session_state:
    for i, q in enumerate(st.session_state.quiz["questions"]):
        st.markdown(f"### Question {i+1}")
        st.write(q["question"])
        st.session_state.answers[i] = st.radio(
            "Select your answer:",
            q["options"],
            key=f"q_{i}"
        )

    if st.button("Submit Quiz"):
        score = 0
        for i, q in enumerate(st.session_state.quiz["questions"]):
            user_answer = st.session_state.answers[i][0]  # Get first letter (A, B, C, D)
            if user_answer == q["correct"]:
                score += 1
        
        st.session_state.submitted = True
        st.session_state.score = score

    if st.session_state.get("submitted", False):
        score = st.session_state.score
        st.markdown(f"### Quiz Results")
        st.write(f"You scored {score} out of {len(st.session_state.quiz['questions'])}")
        
        if score == len(st.session_state.quiz["questions"]):
            st.balloons()
            st.success("Perfect score! You've mastered this topic! 🎉")
        elif score >= len(st.session_state.quiz["questions"]) * 0.7:
            st.success("Great job! You're doing well! 👏")
        else:
            st.warning("Keep practicing! Review the resources for this topic. 📚")