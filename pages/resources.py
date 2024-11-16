import streamlit as st

st.title("Resources")
st.markdown("### Learn and Grow")
resources = {
    "Python for Everybody": "https://www.coursera.org/specializations/python",
    "Django Documentation": "https://docs.djangoproject.com/en/stable/",
    "CompTIA Security+": "https://www.comptia.org/certifications/security",
}
for title, link in resources.items():
    st.markdown(f"- [{title}]({link})")
