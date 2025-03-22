import re
import streamlit as st

class Logic:

    def __init__(self):
        pass

    def remove_komments(self, code, lang):
        if lang == "python":
            data = re.sub(r'(#.*?$)|("""[\s\S]*?""")|(\'\'\'[\s\S]*?\'\'\')', '', code, flags=re.MULTILINE)
            result = open("result.py", "w+")
            result.write(data)
            return self.download_file(result)
        
        if lang == "java":
            with open(code) as code:
                contenido = code.read()
                data = re.sub(r'(/\*[\s\S]*?\*/)|(//.*?$)', '', contenido, flags=re.MULTILINE)
            with open("result.java", "w+") as result:
                result.write(data)
            return self.download_file("result.java")
        
        if lang == "html":
            with open(code) as code:
                contenido = code.read()
                data = re.sub(r'<!--.*?-->', '', contenido, flags=re.MULTILINE)
            with open("testing/result.html", "w+") as result:
                result.write(data)
            return self.download_file("result.html")

        if lang == "css":
            with open(code) as code:
                contenido = code.read()
                data = re.sub(r'/\*[\s\S]*?\*/', '', contenido, flags=re.MULTILINE)
            with open("testing/result.css", "w+") as result:
                result.write(data)
            return self.download_file("result.css")

        if lang == "js":
            with open(code) as code:
                contenido = code.read()
                data = re.sub(r'(/\*[\s\S]*?\*/)|(//.*?$)', '', contenido, flags=re.MULTILINE)
            with open("testing/result.js", "w+") as result:
                result.write(data)
            return self.download_file("result.js")

    def getLang(self, fileName, code):
        if fileName.endswith(".py"):
            return self.remove_komments(code, "python")
        if fileName.endswith(".java"):
            return self.remove_komments(code, "java")
        if fileName.endswith(".html"):
            return self.remove_komments(code, "html")
        if fileName.endswith(".css"):
            return self.remove_komments(code, "css")
        if fileName.endswith(".js"):
            return self.remove_komments(code, "js")
    
    def download_file(self, file):
        file.seek(0)
        return file