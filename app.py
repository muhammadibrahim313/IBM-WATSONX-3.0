import streamlit as st
from langchain_ibm import WatsonxLLM
from langchain.memory import ConversationBufferMemory


# Page config
st.set_page_config(
    page_title="Employee Training Portal",
    page_icon="🎓",
    layout="wide"
)

# Enhanced CSS with better styling
st.markdown("""
<style>
    .main { padding: 0rem 1rem; }
    .header {
        background: linear-gradient(90deg, #1E3D59 0%, #2E5E88 100%);
        padding: 2rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    .role-card {
        background: white;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        margin: 1.5rem 0;
        transition: all 0.3s ease;
    }
    .role-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 6px 12px rgba(0, 0, 0, 0.15);
    }
    .nav-button {
        background-color: #1E3D59;
        color: white;
        padding: 0.8rem 1.5rem;
        border-radius: 8px;
        text-decoration: none;
        margin: 0.8rem;
        text-align: center;
        transition: all 0.2s ease;
    }
    .nav-button:hover {
        background-color: #2E5E88;
        transform: scale(1.05);
    }
</style>
""", unsafe_allow_html=True)

# Initialize WatsonX using the credentials from .env
@st.cache_resource
def init_watsonx():
    try:
        credentials = {
            "url": st.secrets["WATSONX_URL"],
            "apikey": st.secrets["WATSONX_APIKEY"]
        }
        project_id = st.secrets["WATSONX_PROJECT_ID"]
        
        llm = WatsonxLLM(
            model_id="ibm/granite-3-8b-instruct",
            url=credentials.get("url"),
            apikey=credentials.get("apikey"),
            project_id=project_id
        )
        return llm
    except Exception as e:
        st.error(f"Error initializing WatsonX: {str(e)}")
        return None

# Header
st.markdown('<div class="header"><h1>🎓 Employee Training Portal</h1></div>', unsafe_allow_html=True)

# Career Vision Section
st.markdown("### 🎯 Your Career Vision")
years = st.slider("Where do you see yourself in how many years?", 1, 10, 5)
vision = st.text_area("Describe your career goals:", height=100)

# Role Selection (Updated with handbook roles)
roles = {
    "Backend Development": "🔧 Master server-side technologies and databases",
    "Frontend Development": "🎨 Create engaging user interfaces",
    "Software Engineering": "⚙️ Design and architect software solutions",
    "Cybersecurity": "🔒 Protect systems and data",
    "Digital Marketing": "📢 Drive online presence and growth",
    "Android Development": "📱 Build mobile applications",
    "Fullstack Development": "💻 Master both frontend and backend"
}

st.markdown("### 🚀 Select Your Role")
selected_role = st.selectbox("Choose your role:", list(roles.keys()))

# Display personalized learning path
if selected_role and vision:
    st.markdown(f"""
    <div class="role-card">
        <h3>{selected_role}</h3>
        <p>{roles[selected_role]}</p>
        <p>Based on your {years}-year vision, here's your personalized learning path:</p>
        <a href="/pages/learning_paths?role={selected_role}" class="nav-button">Start Your Journey</a>
    </div>
    """, unsafe_allow_html=True)

# Navigation
cols = st.columns(4)
nav_items = {
    "📚 Resources": "resources",
    "❓ FAQ & Help": "faq",
    "📊 Progress": "progress",
    "🎯 Workshops": "workshops"
}

for col, (label, page) in zip(cols, nav_items.items()):
    with col:
        if st.button(label):
            st.switch_page(f"pages/{page}.py")