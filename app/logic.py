import io
import os
import re
import zipfile
import streamlit as st

class Logic:
    def __init__(self):
        self.regexs = {
            "python": r"((?:'''|\"\"\")[\s\S]*?(?:'''|\"\"\"))|([\"'].*?[\"'])|(#.*?$)",
            "java": r'(/\*[\s\S]*?\*/)|(["\'].*?["\'])|(//.*?$)',
            "html": r'(<!--[\s\S]*?-->)|(".*?")',
            "css": r'(/\*[\s\S]*?\*/)|(["\'].*?["\'])',
            "js": r'(/\*[\s\S]*?\*/)|(["\'].*?["\'])|(//.*?$)',
        }
        self.ext_to_lang = {
            ".py": "python",
            ".java": "java",
            ".html": "html",
            ".css": "css",
            ".js": "js"
        }

    def clean_code(self, fileName, code):
        """
        Returns cleaned code string if fileName extension is supported,
        otherwise returns None.
        """
        for ext, lang in self.ext_to_lang.items():
            if fileName.endswith(ext):
                cleaned_buffer = self.remove_komments(code, lang)
                return cleaned_buffer.getvalue()
        return None

    def getLang(self, fileName, code):
        """
        Maintained for backward compatibility. Returns io.StringIO of cleaned code.
        """
        for ext, lang in self.ext_to_lang.items():
            if fileName.endswith(ext):
                return self.remove_komments(code, lang)
        return None

    def replacer(self, code):
        if code.group(2):
            return code.group(2)
        else:
            return ''

    def remove_komments(self, code, lang):
        cleaned_code = re.sub(self.regexs[lang], self.replacer, code, flags=re.MULTILINE)
        file_buffer = io.StringIO(cleaned_code)
        file_buffer.seek(0)
        return file_buffer

    def create_zip(self, files_dict):
        """
        Given a dict of {filename_or_relpath: string_content},
        creates an in-memory zip file BytesIO buffer.
        """
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w", zipfile.ZIP_DEFLATED) as zip_file:
            for rel_path, content in files_dict.items():
                zip_file.writestr(rel_path, content)
        zip_buffer.seek(0)
        return zip_buffer

    def scan_directory(self, dir_path, supported_extensions, ignore_dirs=None):
        """
        Scans a local directory recursively for supported files.
        Returns a list of tuples: (full_file_path, relative_file_path).
        """
        if ignore_dirs is None:
            ignore_dirs = {'.git', '.svn', '.hg', 'venv', '.venv', 'node_modules', '__pycache__', '.idea', '.vscode'}

        found_files = []
        if not dir_path or not os.path.exists(dir_path) or not os.path.isdir(dir_path):
            return found_files

        for root, dirs, files in os.walk(dir_path):
            dirs[:] = [d for d in dirs if d not in ignore_dirs and not d.startswith('.')]
            for file in files:
                if any(file.endswith(ext) for ext in supported_extensions):
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, dir_path)
                    found_files.append((full_path, rel_path))
        return found_files

    def process_directory(self, dir_path, supported_extensions, ignore_dirs=None):
        """
        Scans and cleans all supported files in dir_path.
        Returns a dict of {rel_path: cleaned_code_str}.
        """
        files_info = self.scan_directory(dir_path, supported_extensions, ignore_dirs)
        cleaned_files = {}
        for full_path, rel_path in files_info:
            try:
                with open(full_path, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                cleaned = self.clean_code(full_path, code)
                if cleaned is not None:
                    cleaned_files[rel_path] = cleaned
            except Exception:
                pass
        return cleaned_files