import os
import streamlit as st
from app.logic import Logic
from app.styles import footer
import app.texts as tx

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
        st.header('Upload your file to remove all the comments', divider="grey")
        self.file = st.file_uploader('Upload file', type=self.languages)
        
        if self.file is not None:
            codigo = self.file.read().decode('utf-8', errors='ignore')
            if self.file.name.endswith('.java'):
                st.badge("This will remove JavaDoc!", icon="⚠️", color="orange")
            if self.file.name.endswith('.py'):
                st.badge("This will remove docstrings!", icon="⚠️", color="orange")

            st.success('File uploaded successfully!')
            if st.button('Remove Komments'): 
                    with st.spinner("Removing Komments..."):
                        file2download = logic.getLang(self.file.name, codigo)
                        st.success('Komments removed successfully!')
                        st.download_button(label='Download file', data=file2download.getvalue(), file_name=self.file.name, mime='text/plain')

        if self.file is None:
            if st.button('Show test files'):
                columns = st.columns(len(self.test_files))
                for (lang, file), col in zip(self.test_files.items(), columns):
                    with col:
                        with open(file, 'rb') as f:
                            col.download_button(label=lang.capitalize(), data=f, file_name=os.path.basename(file), mime='text/plain', use_container_width=True)
        st.divider()
        with st.expander("How does this work?"):
            st.markdown("""
            ### Overview
            This app removes **komments** from your code using regular expressions (regex).
            
            These are the regex patterns used for each language:
            """)
            st.code(tx.regex, language="python")
            
            st.divider()

            st.markdown("""
            ### The Process
            When you upload a file and press **'Remove Komments'**, the app identifies the language by its extension and triggers the cleaning method:
            """)
            st.code(tx.function1, language="python")
            
            st.markdown("Then, the main logic is executed using `re.sub()` to replace detected patterns:")
            st.code(tx.function3, language="python")

            st.divider()

            st.markdown("### The 'Replacer' Logic")
            st.write("To avoid accidentally deleting code, we use a helper function:")
            st.code(tx.function2, language="python")
            
            st.info("""
            **Why is this necessary?** The regex is designed to capture BOTH strings and comments. 
            - If it matches a **string** (Group 2), the function returns it intact.
            - If it matches a **comment**, the function returns an empty string, effectively deleting it.
            """)

            st.write("This ensures that statements like the one below stay safe:")
            st.code('print("this # is not a comment")', language="python")
            
            st.divider()
            st.caption("The rest of the app is built with Streamlit. Thanks for reading! :)")

        st.markdown(footer, unsafe_allow_html=True)