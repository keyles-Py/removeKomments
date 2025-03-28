import io
import re
import streamlit as st

class Logic:
    def __init__(self):
        self.regexs = {
            "python": r'("""[\s\S]*?""")|(\'\'\'[\s\S]*?\'\'\')|(["\'].*?["\'])|#.*?$',
            "java": r'(/\*[\s\S]*?\*/)|(//.*?$)',
            "html": r'<!--.*?-->',
            "css": r'/\*[\s\S]*?\*/',
            "js": r'(/\*[\s\S]*?\*/)|(//.*?$)'
        }

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
            
    def replacer(self, code):
        if code.group(3):
            return code.group(3)
        else:
            return ''
        
    def remove_komments(self, code, lang):
        cleaned_code = re.sub(self.regexs[lang], self.replacer, code, flags=re.MULTILINE)
        file_buffer = io.StringIO(cleaned_code)
        file_buffer.seek(0)
        return file_buffer