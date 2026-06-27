# 📚 Chat with Multiple PDFs

An AI-powered chatbot that lets you upload multiple PDF documents and ask questions about them in natural language.

## 🚀 Live Demo
[Click here to try it out](https://pdf-chat-pg6gnqhdpyyuamew7u2ats.streamlit.app/)

## ✨ Features
- Upload multiple PDF documents at once
- Ask questions about your documents in natural language
- Get AI-powered answers with context from your PDFs
- Document summarizer — get a quick summary of uploaded PDFs
- Download chat history as a text file
- Clean and intuitive chat interface

## 🛠️ Built With
- [Streamlit](https://streamlit.io/) — frontend and backend
- [LangChain](https://langchain.com/) — AI orchestration
- [Mistral AI](https://mistral.ai/) — language model
- [HuggingFace](https://huggingface.co/) — embeddings (all-MiniLM-L6-v2)
- [FAISS](https://faiss.ai/) — vector store for document search

## ⚙️ How It Works
1. Upload your PDFs
2. Text is extracted and split into chunks
3. Chunks are converted to embeddings and stored in FAISS
4. When you ask a question, relevant chunks are retrieved
5. Mistral AI generates an answer based on the retrieved context

## 🔧 How to Run Locally
1. Clone the repo
