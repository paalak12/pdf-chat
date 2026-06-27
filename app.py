import streamlit as st
from dotenv import load_dotenv
from PyPDF2 import PdfReader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_mistralai import ChatMistralAI
from htmlTemplates import css, bot_template, user_template
import re


def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text()
    return text


def get_text_chunks(text):
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=1000,
        chunk_overlap=200,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    vectorstore = FAISS.from_texts(texts=text_chunks, embedding=embeddings)
    return vectorstore


def get_conversation_chain(vectorstore):
    retriever = vectorstore.as_retriever()
    return retriever  # just return retriever, we'll handle memory manually


def summarize_documents(text):
    llm = ChatMistralAI(model="mistral-small-latest")
    prompt = f"""Provide a concise summary of the document below.
Include main topics and key points.

Document:
{text[:3000]}

Summary:"""
    response = llm.invoke(prompt)
    return response.content

    
def get_chat_download(chat_history):
    text = ""
    for chat in chat_history:
        text += f"You: {chat['question']}\n"
        text += f"Bot: {chat['answer']}\n"
        text += "-" * 50 + "\n"
    return text

def main():
    load_dotenv()
    st.set_page_config(page_title="Chat with multiple PDFs",
                       page_icon=":books:")
    st.write(css, unsafe_allow_html=True)
    
    # CHANGED: replaced conversation with chat_history + retriever
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "retriever" not in st.session_state:
        st.session_state.retriever = None

    st.header("Chat with multiple PDFs :books:")
    user_question = st.text_input("Ask a question about your documents:")  # CHANGED: saved to variable

    # NEW: handle user question
    if user_question and st.session_state.retriever:
        docs = st.session_state.retriever.invoke(user_question)  # ✅
        context = "\n".join([doc.page_content for doc in docs])

        history_text = "\n".join([
            f"Human: {h['question']}\nAssistant: {h['answer']}"
            for h in st.session_state.chat_history
        ])

        prompt = f"""Use the context below to answer the question.
Context: {context}

Previous conversation:
{history_text}

Question: {user_question}
Answer:"""

        llm = ChatMistralAI(model="mistral-small-latest")
        response = llm.invoke(prompt)
        answer = response.content

        st.session_state.chat_history.append({
            "question": user_question,
            "answer": answer
        })

    # CHANGED: display chat history from session state instead of hardcoded templates
    for chat in st.session_state.chat_history:
        st.write(user_template.replace("{{MSG}}", chat['question']), unsafe_allow_html=True)
        clean_answer = re.sub(r'\*\*(.*?)\*\*', r'\1', chat['answer'])  # removes ** **
        st.write(bot_template.replace("{{MSG}}", clean_answer), unsafe_allow_html=True)

        
    with st.sidebar:
        st.subheader("Your documents")
        pdf_docs = st.file_uploader("Upload your PDFs here and click on 'Process'", accept_multiple_files=True)
        if st.button("Process"):
            with st.spinner("Processing"):
                raw_text = get_pdf_text(pdf_docs)
                text_chunks = get_text_chunks(raw_text)
                vectorstore = get_vectorstore(text_chunks)
                st.session_state.retriever = vectorstore.as_retriever()  # CHANGED: store retriever instead of conversation chain

        if st.button("📝 Summarize Documents"):
            if pdf_docs:
                with st.spinner("Summarizing..."):
                    raw_text = get_pdf_text(pdf_docs)
                    summary = summarize_documents(raw_text)
                    st.subheader("Summary:")
                    st.write(summary)
            else:
              st.warning("Please upload PDFs first!")

        if st.session_state.chat_history:
            chat_text = get_chat_download(st.session_state.chat_history)
            st.download_button(
                label="📥 Download Chat History",
                data=chat_text,
                file_name="chat_history.txt",
                mime="text/plain"
    )


if __name__== '__main__' :
    main()       