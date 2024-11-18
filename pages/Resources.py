import streamlit as st
from typing import Dict

# Custom CSS
st.markdown("""
<style>
    .resource-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
    }
    .resource-section {
        margin: 2rem 0;
        padding: 1rem;
        border-left: 4px solid #1E3D59;
    }
</style>
""", unsafe_allow_html=True)

def get_role_resources(role: str) -> Dict:
    # Common resources for all roles (3-month initial training)
    common_resources = {
        "Introduction to Computing": "https://online.stanford.edu/courses/soe-ycscs101-computer-science-101",
        "Git Fundamentals": "https://git-scm.com/book/en/v2",
        "Python Programming": "https://www.coursera.org/specializations/python",
        "Data Structures": "https://leetcode.com/",
        "OOP Concepts": "https://realpython.com/python3-object-oriented-programming/",
    }
    
    # Role-specific resources
    role_resources = {
        "Backend Development": {
            "Django": "https://docs.djangoproject.com/en/stable/",
            "Database Systems": "https://www.coursera.org/learn/database-systems",
            "FastAPI": "https://fastapi.tiangolo.com/tutorial/",
            "Security": "https://owasp.org/www-project-top-ten/"
        },
        "Frontend Development": {
            "HTML & CSS": "https://developer.mozilla.org/en-US/docs/Web",
            "React": "https://reactjs.org/docs/getting-started.html",
            "UI/UX Design": "https://www.interaction-design.org/",
            "Streamlit": "https://docs.streamlit.io/"
        },
        # Add other roles from handbook.txt
    }
    
    return {
        "common": common_resources,
        "specific": role_resources.get(role, {})
    }

st.title("📚 Learning Resources")

# Role selection
roles = [
    "Backend Development",
    "Frontend Development",
    "Software Engineering",
    "Cybersecurity",
    "Digital Marketing",
    "Android Development"
]

selected_role = st.selectbox("Select your role:", roles)

if selected_role:
    resources = get_role_resources(selected_role)
    
    # Display common resources
    st.markdown("### 🎓 Foundation Training Resources (First 3 Months)")
    st.markdown('<div class="resource-section">', unsafe_allow_html=True)
    for title, link in resources["common"].items():
        st.markdown(f"""
        <div class="resource-card">
            <h4>{title}</h4>
            <a href="{link}" target="_blank">Access Resource</a>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Display role-specific resources
    st.markdown(f"### 🚀 {selected_role} Specific Resources")
    st.markdown('<div class="resource-section">', unsafe_allow_html=True)
    for title, link in resources["specific"].items():
        st.markdown(f"""
        <div class="resource-card">
            <h4>{title}</h4>
            <a href="{link}" target="_blank">Access Resource</a>
        </div>
        """, unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Progress tracking
st.markdown("### 📊 Learning Progress")
completed = st.multiselect(
    "Mark completed resources:",
    list(resources["common"].keys()) + list(resources["specific"].keys())
)

if completed:
    progress = len(completed) / (len(resources["common"]) + len(resources["specific"])) * 100
    st.progress(progress)
    st.write(f"You've completed {progress:.1f}% of your learning resources!")