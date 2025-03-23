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
        data = re.sub(regexs[lang], '', code, flags=re.MULTILINE)
        result = open("result.txt", "w+")
        result.write(data)
        return self.download_file(result)

        if lang == "python":
            data = re.sub(r'(#.*?$)|("""[\s\S]*?""")|(\'\'\'[\s\S]*?\'\'\')', '', code, flags=re.MULTILINE)
            result = open("result.py", "w+")
            result.write(data)
            return self.download_file(result)
        
        if lang == "java":
            data = re.sub(r'(/\*[\s\S]*?\*/)|(//.*?$)', '', code, flags=re.MULTILINE)
            result = open("result.java", "w+")
            result.write(data)
            return self.download_file(result)
        
        if lang == "html":
            data = re.sub(r'<!--.*?-->', '', code, flags=re.MULTILINE)
            result = open("result.html", "w+")
            result.write(data)
            return self.download_file(result)

        if lang == "css":
            data = re.sub(r'/\*[\s\S]*?\*/', '', code, flags=re.MULTILINE)
            result = open("result.css", "w+")
            result.write(data)
            return self.download_file(result)

        if lang == "js":
            data = re.sub(r'(/\*[\s\S]*?\*/)|(//.*?$)', '', code, flags=re.MULTILINE)
            result = open("result.js", "w+")
            result.write(data)
            return self.download_file(result)

    def download_file(self, file):
        file.seek(0)
        return file