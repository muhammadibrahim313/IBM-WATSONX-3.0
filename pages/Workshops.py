import streamlit as st
from datetime import datetime, timedelta
import random

# Custom CSS
st.markdown("""
<style>
    .workshop-card {
        background: white;
        padding: 1.5rem;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        margin: 1rem 0;
        border-left: 4px solid #1E3D59;
    }
    .workshop-date {
        color: #666;
        font-size: 0.9rem;
    }
    .register-btn {
        background-color: #1E3D59;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 4px;
        text-decoration: none;
        display: inline-block;
        margin-top: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

st.title("🎯 Workshops & Training Sessions")

# Workshop data structure based on handbook content
workshops = {
    "Common": [
        {
            "title": "Introduction to Computing Fundamentals",
            "description": "Learn basic computing concepts and principles",
            "duration": "2 hours",
            "instructor": "Dr. Sarah Chen"
        },
        {
            "title": "Git & Version Control Mastery",
            "description": "Master Git fundamentals and collaborative development",
            "duration": "3 hours",
            "instructor": "John Smith"
        },
        {
            "title": "Python Programming Essentials",
            "description": "Get started with Python programming language",
            "duration": "4 hours",
            "instructor": "Mike Johnson"
        }
    ],
    "Backend Development": [
        {
            "title": "Django Web Framework Deep Dive",
            "description": "Build robust web applications with Django",
            "duration": "6 hours",
            "instructor": "David Wilson"
        },
        {
            "title": "Database Design & Optimization",
            "description": "Learn database modeling and optimization techniques",
            "duration": "4 hours",
            "instructor": "Emma Davis"
        }
    ],
    "Frontend Development": [
        {
            "title": "Modern React Development",
            "description": "Build interactive UIs with React",
            "duration": "5 hours",
            "instructor": "Lisa Zhang"
        },
        {
            "title": "UI/UX Design Principles",
            "description": "Learn essential design principles for web applications",
            "duration": "3 hours",
            "instructor": "Alex Turner"
        }
    ]
}

# Filter workshops by role
roles = ["All"] + list(workshops.keys())
selected_role = st.selectbox("Filter by role:", roles)

# Generate upcoming dates
def generate_workshop_dates(num_workshops):
    dates = []
    start_date = datetime.now()
    for _ in range(num_workshops):
        start_date += timedelta(days=random.randint(1, 14))
        dates.append(start_date.strftime("%B %d, %Y"))
    return dates

# Display workshops
st.markdown("### 📅 Upcoming Events")

if selected_role == "All":
    # Display all workshops
    for role, role_workshops in workshops.items():
        st.markdown(f"#### {role} Track")
        dates = generate_workshop_dates(len(role_workshops))
        
        for workshop, date in zip(role_workshops, dates):
            st.markdown(f"""
            <div class="workshop-card">
                <h4>{workshop['title']}</h4>
                <p>{workshop['description']}</p>
                <p class="workshop-date">📅 {date} | ⏱️ {workshop['duration']} | 👨‍🏫 {workshop['instructor']}</p>
                <a href="#" class="register-btn">Register Now</a>
            </div>
            """, unsafe_allow_html=True)
else:
    # Display role-specific workshops
    if selected_role in workshops:
        dates = generate_workshop_dates(len(workshops[selected_role]))
        for workshop, date in zip(workshops[selected_role], dates):
            st.markdown(f"""
            <div class="workshop-card">
                <h4>{workshop['title']}</h4>
                <p>{workshop['description']}</p>
                <p class="workshop-date">📅 {date} | ⏱️ {workshop['duration']} | 👨‍🏫 {workshop['instructor']}</p>
                <a href="#" class="register-btn">Register Now</a>
            </div>
            """, unsafe_allow_html=True)

# Workshop Registration Section
st.markdown("### ✍️ Request a Workshop")
requested_topic = st.text_input("What topic would you like to learn about?")
preferred_date = st.date_input("Preferred workshop date:")

if st.button("Submit Request"):
    st.success("Thank you! Your workshop request has been submitted. We'll notify you when a relevant workshop is scheduled.")

# Upcoming Certifications Section
st.markdown("### 🏆 Upcoming Certification Tracks")
cert_tracks = {
    "Backend Development": ["AWS Certified Developer", "MongoDB Certified Developer"],
    "Frontend Development": ["React Developer Certification", "Google UX Design Certificate"],
    "Cybersecurity": ["CompTIA Security+", "Certified Ethical Hacker"],
}

if selected_role in cert_tracks:
    for cert in cert_tracks[selected_role]:
        st.write(f"🔹 **{cert}** - Coming Soon")