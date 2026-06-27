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
1. Clone the repo (git clone https://github.com/paalak12/pdf-chat.git)
2. Install dependencies (pip install -r requirements.txt)
3. Create a `.env` file and add your API keys (MISTRAL_API_KEY=your_key_here)
4. Run the app (streamlit run app.py)

## 💡 Challenges & Solutions
- **Python 3.13 compatibility** — LangChain core didn't support Python 3.13, switched to `langchain_community` and separate provider packages
- **Deprecated LangChain memory** — `ConversationBufferMemory` unavailable, replaced with `st.session_state` for manual chat history management
- **Free LLM integration** — Navigated quota issues across OpenAI, Google Gemini, HuggingFace before settling on Mistral AI

## 🔮 Future Improvements
- Google login with saved chat history per user
- Support for Word and text files
- Multiple language support
- Compare answers across multiple PDFs

## 👩‍💻 Author
Palak Gupta
