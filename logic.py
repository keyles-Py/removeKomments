import io
import re
import streamlit as st

class Logic:

    def getLang(self, fileName, code):
        ext_to_lang = {
            ".py": "python",
            ".java": "java",
            ".html": "html",
            ".css": "css",
            ".js": "js"
        }
        for ext, lang in ext_to_lang.items():
            if fileName.endswith(ext):
                return self.remove_komments(code, lang)
        
    def remove_komments(self, code, lang):
        regexs = {
            "python": r'(#.*?$)|("""[\s\S]*?""")|(\'\'\'[\s\S]*?\'\'\')',
            "java": r'(/\*[\s\S]*?\*/)|(//.*?$)',
            "html": r'<!--.*?-->',
            "css": r'/\*[\s\S]*?\*/',
            "js": r'(/\*[\s\S]*?\*/)|(//.*?$)'
        }
        lines = code.splitlines(keepends=True)

        cleaned_lines = [re.sub(regexs[lang], '', line, flags=re.MULTILINE) if line.strip() else line for line in lines]

        cleaned_code = "".join( cleaned_lines )

        file_buffer = io.StringIO(cleaned_code)
        file_buffer.seek(0)
        return file_buffer