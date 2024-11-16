import streamlit as st
from langchain_ibm import WatsonxLLM
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.chains import RetrievalQA

# Initialize RAG components
@st.cache_resource
def init_rag_system():
    try:
        # Initialize WatsonX
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
        
        # Load handbook content
        with open("handbook.txt", "r") as f:
            handbook_content = f.read()
            
        # Split content
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000,
            chunk_overlap=200
        )
        texts = text_splitter.split_text(handbook_content)
        
        # Create vector store
        embeddings = HuggingFaceEmbeddings()
        vectorstore = Chroma.from_texts(texts, embeddings)
        
        # Create QA chain
        qa_chain = RetrievalQA.from_chain_type(
            llm=llm,
            chain_type="stuff",
            retriever=vectorstore.as_retriever()
        )
        
        return qa_chain
    except Exception as e:
        st.error(f"Error initializing RAG system: {str(e)}")
        return None

st.title("FAQ & Help Center")

# Common Questions Section
st.markdown("### 📌 Frequently Asked Questions")
faqs = {
    "How do I start the training program?": 
        "Begin with our 3-month foundational training covering computing basics, programming, and problem-solving.",
    "What resources are available?":
        "We provide video tutorials, documentation, interactive courses, and mentorship opportunities.",
    "How long is the initial training?":
        "The initial training is 3 months, followed by role-specific specialization.",
    "Can I switch roles later?":
        "Yes, you can switch roles after completing the initial training period."
}

for question, answer in faqs.items():
    with st.expander(question):
        st.write(answer)

# AI Assistant Section
st.markdown("### 🤖 AI Learning Assistant")
st.write("Ask any question about your training program, technical concepts, or career path.")

# Initialize RAG system
rag_chain = init_rag_system()

question = st.text_input("Your question:")
if question and rag_chain:
    with st.spinner("Finding the best answer..."):
        try:
            response = rag_chain.run(question)
            st.write(response)
        except Exception as e:
            st.error(f"Error processing question: {str(e)}")