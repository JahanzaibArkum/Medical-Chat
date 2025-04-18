# Medical Chatbot

## Overview

The Medical Chatbot is an AI-powered assistant designed to provide medical information and guidance based on user queries. It leverages Retrieval-Augmented Generation (RAG) to fetch relevant medical knowledge from a Pinecone vector store and generate responses using Google's Gemini AI model. The chatbot is built with Streamlit for an interactive and user-friendly interface.

## Features

* **Conversational AI:** Users can ask medical-related questions and receive informative responses.

* **Retrieval-Augmented Generation (RAG):** Enhances response accuracy by retrieving relevant documents before generating an answer.

* **Integration with Pinecone:** Stores medical text embeddings for efficient similarity search.

* **Streamlit UI:** A colorful, interactive frontend for seamless user interaction.

* **Optimized for Performance:** Utilizes embeddings from Hugging Face and a lightweight Gemini model.

## Tech Stack

* **Python**

* **Streamlit** (UI Framework)

* **LangChain** (for chaining LLM calls and retrieval)

* **Pinecone** (Vector Store for document retrieval)

* **Google Gemini AI** (LLM for response generation)

* **Hugging Face** (Embeddings for medical documents)

* **dotenv** (For managing API keys securely)

## Installation
### 1. Clone the Repository
```bash
   git clone https://github.com/0792211827/Gen-Ai-medical-chatbot.git
   cd  Gen-Ai-medical-chatbot
   
```
### 2. Create a Virtual Environment
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use 'venv\Scripts\activate'
```
### 3. Install Dependencies
```bash
   pip install -r requirements.txt
```
### 4. Set Up Environment Variables
Create a .env file in the project root and add the following:
```bash
   PINECONE_API_KEY=your_pinecone_api_key
   GEMINI_API_KEY=your_gemini_api_key
```
### 5. Run the Chatbot
```bash
   streamlit run app.py
```

## Project Structure

```bash
   medical-chatbot/
   │── src/
   │   ├── helper.py       # Functions for embedding download & processing
   │   ├── prompt.py       # System prompts for the chatbot
   │── app.py              # Streamlit UI
   │── requirements.txt    # Required dependencies
   │── .env                # API keys (not included in repo)
   │── README.md           # Project documentation
```

## License

This project is licensed under the MIT License.

## Contributors

WESLEY NYAMOSI

Feel free to contribute by submitting pull requests or opening issues!

## ⚠️ Disclaimer
This chatbot provides general health information only and is not a substitute for professional medical advice. Always consult a healthcare provider for personal medical concerns.
