import os
import streamlit as st
from logic import Logic

LANGUAGES = [".py", ".java", ".html", ".css", ".js"]
TEST_FILES = {
    "python": 'testFiles/test.py',
    "java": 'testFiles/Test.java',
    "html": 'testFiles/test.html',
    "css": 'testFiles/test.css',
    "js": 'testFiles/test.js'
}

st.set_page_config(
    page_title="RemoveKomments",
    page_icon="🤖",
)

class GUI:
    def __init__(self):
        self.file = None
        self.languages = LANGUAGES
        self.test_files = TEST_FILES

    def run(self):
        logic = Logic()
        st.title('RemoveKomments')
        st.text('Upload your file to remove all the comments')
        self.file = st.file_uploader('Upload file', type=self.languages)
        
        if self.file is not None:
            codigo = self.file.read().decode('utf-8', errors='ignore')
            if self.file.name.endswith('.java'):
                st.text('This will remove JavaDoc')
            if self.file.name.endswith('.py'):
                st.text('This will remove docstrings')

            st.text('File uploaded successfully!')
            if st.button('Remove comments'): 
                    with st.spinner("Removing comments..."):
                        file2download = logic.getLang(self.file.name, codigo)
                        st.success('Comments removed successfully!')
                        st.download_button(label='Download file', data=file2download.getvalue(), file_name=self.file.name, mime='text/plain')

        if self.file is None:
            if st.button('Show test files'):
                columns = st.columns(len(self.test_files))
                for (lang, file), col in zip(self.test_files.items(), columns):
                    with col:
                        with open(file, 'rb') as f:
                            col.download_button(label=lang.capitalize(), data=f, file_name=os.path.basename(file), mime='text/plain', use_container_width=True)

        gitprofile = 'https://github.com/keyles-Py'
        st.markdown(f'Developed by: [Keyles-Py]({gitprofile})')
        url = 'https://github.com/keyles-Py/removeKomments'
        st.markdown(f'[Repository of this project]({url})')
        st.markdown('Last update: 13-04-2025')