import streamlit as st

st.title("FAQ")
question = st.text_input("Ask your question:")
if question:
    st.write(f"Answer for '{question}' will be here.")  # Integrate Watson API here
