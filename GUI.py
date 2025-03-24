import os
import streamlit as st
from logic import Logic
import re


class GUI:
    def __init__(self):
        self.file = None
        self.languages = [".py", ".java", ".html", ".css", ".js"]

    def run(self):
        logic = Logic()
        st.title('RemoveKomments')
        st.text('Upload your file to remove all the comments')
        self.file = st.file_uploader('Upload file', type=self.languages)
        
        if self.file is not None:
            codigo = self.file.read().decode('utf-8', errors='ignore')
            if self.file.name.endswith('.java'):
                st.text('This will not remove comments from JavaDoc')
            st.text('File uploaded successfully!')
            if st.button('Remove comments'): 
                st.text('Comments removed successfully!')
                file2download = logic.getLang(self.file.name, codigo)
                st.download_button(label='Download file', data=file2download.getvalue(), file_name=self.file.name, mime='text/plain')
        

        gitprofile = 'https://github.com/keyles-Py'
        st.markdown(f'Developed by: [Keyles-Py]({gitprofile})')
        url = 'https://github.com/keyles-Py/removeKomments'
        st.markdown(f'[Repository of this project]({url})')