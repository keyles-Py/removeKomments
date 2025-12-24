regex = """
"python": r"((?:'''|\"\"\")[\s\S]*?(?:'''|\"\"\"))|([\"'].*?[\"'])|(#.*?$)",
"java": r'(/\*[\s\S]*?\*/)|(["\'].*?["\'])|(//.*?$)',
"html": r'(<!--[\s\S]*?-->)|(".*?")',
"css": r'(/\*[\s\S]*?\*/)|(["\'].*?["\'])',
"js": r'(/\*[\s\S]*?\*/)|(["\'].*?["\'])|(//.*?$)', """

function1 = """
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
"""
function2 = """
def replacer(self, code):
    if code.group(2):
        return code.group(2)
    else:
        return ''
"""
function3 = """
def remove_komments(self, code, lang):
    cleaned_code = re.sub(self.regexs[lang], self.replacer, code, flags=re.MULTILINE)
    file_buffer = io.StringIO(cleaned_code)
    file_buffer.seek(0)
    return file_buffer
"""
        
