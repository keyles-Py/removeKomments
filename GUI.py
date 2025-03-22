import os
import streamlit as st
from logic import Logic


class GUI:
    def __init__(self):
        self.file = None
        self.languages = [".py", ".java", ".html", ".css", ".js"]

    def run(self):
        logic = Logic()

        st.title('removeKomments')
        st.text('Upload your file to remove all the comments')
        self.file = st.file_uploader('Upload file', type=self.languages)
        
        if self.file is not None:
            st.text('File uploaded successfully')
            if st.button('Remove comments'): 
                st.text('Comments removed successfully')
                file2download = logic.getLang(self.file.name, self.file.read().decode('utf-8', errors='ignore'))
                st.download_button(label='Download file', data=file2download, file_name=self.file.name, mime='text/plain')
                file2download.close()
                os.remove(file2download.name)
