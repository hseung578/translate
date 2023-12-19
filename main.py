import streamlit as st
import deepl

class TranslatorApp:
    def __init__(self):
        if 'raw_text' not in st.session_state:
            st.session_state.raw_text = ""
        if 'result' not in st.session_state:
            st.session_state.result = ""

    def upload_file(self):
        uploaded_file = st.file_uploader("Upload a file")
        if uploaded_file is not None:
            if uploaded_file.type == "text/plain":
                st.session_state.raw_text = str(uploaded_file.read(), "utf-8")
            else:
                st.error("This file type is not supported yet.")

    def translate_text(self):
        if st.session_state.raw_text:
            auth_key = st.secrets["auth_key"]
            translator = deepl.Translator(auth_key)
            st.session_state.result = translator.translate_text(st.session_state.raw_text, target_lang="KO").text
        else:
            st.error("No text to translate. Please upload a text file.")

    def download_button(self):
        if st.session_state.result:
            result_file = st.session_state.result.encode('utf-8')
            st.download_button(
                label="Download",
                data=result_file,
                file_name="result.txt",
                mime="text/plain"
            )

    def run(self):
        st.title('Translator')
        self.upload_file()

        if st.button('Translate'):
            self.translate_text()

        self.download_button()

def main():
    app = TranslatorApp()
    app.run()

if __name__ == "__main__":
    main()