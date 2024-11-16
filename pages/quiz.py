import streamlit as st

st.title("Quiz Section")
st.markdown("### Test Your Knowledge")
q1 = st.radio("1. What is Python?", ["A programming language", "A snake"])
if q1 == "A programming language":
    st.success("Correct!")
else:
    st.error("Wrong!")
