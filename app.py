import streamlit as st

# Inline CSS for styling
st.markdown("""
<style>
    body {
        font-family: 'Arial', sans-serif;
        background-color: #f4f4f9;
    }
        .header {
        text-align: center;
        font-size: 40px;
        color: black;
        font-weight: bold;
        background: white;
        padding: 20px;
        border-radius: 10px;
        margin: 20px 0;
        text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
    }
    .buttons {
        display: flex;
        justify-content: center;
        gap: 10px;
        margin-top: 20px;
    }
    .carousel img {
        width: 100%;
        height: auto;
        margin: 10px 0;
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)

# Landing Page Content
st.markdown('<div class="header">Ahmad Don Pawa </div>', unsafe_allow_html=True)
st.subheader("Empowering Employees with Knowledge and Skills")

# Buttons for navigation
st.markdown('<div class="buttons">', unsafe_allow_html=True)
if st.button("Workshops & Trainings"):
    st.experimental_set_query_params(page="workshops")
if st.button("Resources"):
    st.experimental_set_query_params(page="resources")
if st.button("FAQ"):
    st.experimental_set_query_params(page="faq")
if st.button("Quiz"):
    st.experimental_set_query_params(page="quiz")
st.markdown('</div>', unsafe_allow_html=True)

# Image carousel
st.markdown("""
<div class="carousel">
    <img src="https://via.placeholder.com/800x200?text=Welcome+to+BTaji" alt="Welcome">
    <img src="https://via.placeholder.com/800x200?text=Training+Programs" alt="Training">
    <img src="https://via.placeholder.com/800x200?text=Employee+Success" alt="Success">
</div>
""", unsafe_allow_html=True)
