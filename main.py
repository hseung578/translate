import streamlit as st
from langchain.text_splitter import CharacterTextSplitter
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os
import time

load_dotenv()

key = os.getenv('OPENAI_KEY')
st.title('Translator')

uploaded_file = st.file_uploader("Upload a file")


    

if uploaded_file is not None:
    if uploaded_file.type == "text/plain":
        raw_text = str(uploaded_file.read(), "utf-8")
    else:
        st.error("This file type is not supported yet.")
        raw_text = None

scroll_container = """
<div style="height: 400px; overflow-y: scroll;">
    {} <!-- 여기에 텍스트 삽입 -->
</div>
"""

if st.button('Translate'):
    
    if raw_text:
        text_splitter = CharacterTextSplitter(
                        separator = "\n\n",
                        chunk_size = 2000,
                        chunk_overlap  = 0,
                        length_function = len,
                        is_separator_regex = False,
                    )
        texts = text_splitter.create_documents([raw_text])
        llm = ChatOpenAI(model="gpt-4-1106-preview", temperature=0, openai_api_key=key)
        message_placeholder = st.empty()
        full = ""
        for t in texts:
            for chunk in llm.stream(f"Translate the following English Yotube caption to Korean. {t}"): 
                full += chunk.content
                time.sleep(0.05)
                message_placeholder.markdown(scroll_container.format(full + "▌"), unsafe_allow_html=True)
            message_placeholder.markdown(scroll_container.format(full), unsafe_allow_html=True)
    else:
        st.error("No text to translate. Please upload a text file.")

