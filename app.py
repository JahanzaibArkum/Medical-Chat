import streamlit as st
from src.helper import download_hugging_face_embeddings
from langchain_pinecone import PineconeVectorStore
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv
from src.prompt import *
import os

# Load environment variables
load_dotenv()

# Set up the Streamlit page with colorful theme
def setup_page():
    st.set_page_config(
        page_title="MediBot - Your Medical Assistant",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for colorful design
    st.markdown("""
    <style>
        :root {
            --primary: #6C63FF;
            --secondary: #FF6584;
            --accent: #42E2B8;
            --background: #000000;
            --text: #2D3748;
        }
        
        .stApp {
            background-color: var(--background);
        }
        
        .stChatInput {
            border-radius: 20px !important;
            border: 2px solid var(--primary) !important;
        }
        
        .stButton>button {
            background-color: var(--primary) !important;
            color: white !important;
            border-radius: 20px !important;
            border: none !important;
            padding: 10px 24px !important;
        }
        
        .stMarkdown h1 {
            color: var(--primary);
            text-align: center;
            margin-bottom: 30px;
        }
        
        .stMarkdown h2 {
            color: var(--secondary);
            border-bottom: 2px solid var(--accent);
            padding-bottom: 5px;
        }
        
        .css-1fv8s86.e16nr0p34 {
            background-color: white;
            border-radius: 15px;
            padding: 20px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }
        
        .user-message {
            background-color: var(--primary) !important;
            color: white !important;
            border-radius: 15px 15px 0 15px !important;
            padding: 10px 15px !important;
            margin: 5px 0 !important;
            max-width: 80%;
            margin-left: auto;
        }
        
        .bot-message {
            background-color: white !important;
            color: var(--text) !important;
            border: 1px solid var(--accent) !important;
            border-radius: 15px 15px 15px 0 !important;
            padding: 10px 15px !important;
            margin: 5px 0 !important;
            max-width: 80%;
        }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state for chat history
def init_chat_history():
    if "messages" not in st.session_state:
        st.session_state.messages = []
        st.session_state.messages.append({
            "role": "assistant",
            "content": "Hello! I'm MediBot, your medical assistant. How can I help you today?",
            "avatar": "🩺"
        })

# Display chat messages
def display_chat():
    for message in st.session_state.messages:
        with st.chat_message(message["role"], avatar=message.get("avatar")):
            st.markdown(message["content"])

# Main function
def main():
    setup_page()
    init_chat_history()
    
    # Load environment variables
    PINECONE_API_KEY = os.environ.get('PINECONE_API_KEY')
    GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')
    
    os.environ["PINECONE_API_KEY"] = PINECONE_API_KEY
    os.environ["OPENAI_API_KEY"] = GEMINI_API_KEY
    
    # Set up the RAG chain (moved after page setup for better UX)
    with st.spinner("Loading medical knowledge..."):
        embeddings = download_hugging_face_embeddings()
        index_name = "medicalbot"
        docsearch = PineconeVectorStore.from_existing_index(
            index_name=index_name,
            embedding=embeddings
        )
        retriever = docsearch.as_retriever(search_type="similarity", search_kwargs={"k":3})
        
        llm = ChatGoogleGenerativeAI(
            model="gemini-1.5-flash",
            google_api_key=os.getenv("GEMINI_API_KEY"),
            temperature=0.4,
            max_output_tokens=500,
            transport="rest"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    
    # App header
    st.title("🩺 MediBot - Your Medical Assistant")
    st.caption("A friendly AI assistant for general medical information")
    
    # Display chat messages
    display_chat()
    
    # Chat input
    if prompt := st.chat_input("Ask me about medical topics..."):
        # Add user message to chat history
        st.session_state.messages.append({
            "role": "user",
            "content": prompt,
            "avatar": "👤"
        })
        
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        
        # Get and display assistant response
        with st.spinner("Thinking..."):
            response = rag_chain.invoke({"input": prompt})
        
        assistant_response = response["answer"]
        
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_response,
            "avatar": "🩺"
        })
        
        with st.chat_message("assistant", avatar="🩺"):
            st.markdown(assistant_response)

if __name__ == "__main__":
    main()