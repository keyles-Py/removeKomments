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
    layout="centered"
)

class GUI:
    def __init__(self):
        self.languages = LANGUAGES
        self.test_files = TEST_FILES

    def run(self):
        logic = Logic()
        st.title('RemoveKomments')
        st.header('Upload files or attach a directory to remove all comments', divider="grey")

        tab_upload, tab_dir = st.tabs(["📁 Upload File(s)", "📂 Process Local Directory"])

        uploaded_files = None
        dir_path = ""

        # Tab 1: Upload File(s)
        with tab_upload:
            uploaded_files = st.file_uploader(
                'Upload single, multiple files, or drag-and-drop a folder',
                type=[ext.lstrip('.') for ext in self.languages],
                accept_multiple_files=True,
                key="uploader"
            )
            if st.button('Show test files'):
                            columns = st.columns(len(self.test_files))
                            for (lang, file), col in zip(self.test_files.items(), columns):
                                with col:
                                    if os.path.exists(file):
                                        with open(file, 'rb') as f:
                                            col.download_button(label=lang.capitalize(), data=f, file_name=os.path.basename(file), mime='text/plain', use_container_width=True)

            if uploaded_files:
                st.info(f"**{len(uploaded_files)} file(s) attached.**")
                has_java = any(f.name.endswith('.java') for f in uploaded_files)
                has_py = any(f.name.endswith('.py') for f in uploaded_files)

                if has_java:
                    st.badge("Contains Java files (will remove JavaDoc!)", icon="⚠️", color="orange")
                if has_py:
                    st.badge("Contains Python files (will remove docstrings!)", icon="⚠️", color="orange")

                if st.button('Remove Komments', key="btn_upload"):
                    with st.spinner("Removing Komments..."):
                        cleaned_files = {}
                        for file in uploaded_files:
                            code = file.read().decode('utf-8', errors='ignore')
                            cleaned = logic.clean_code(file.name, code)
                            if cleaned is not None:
                                cleaned_files[file.name] = cleaned

                        st.success(f'Komments removed successfully from {len(cleaned_files)} file(s)!')

                        if len(cleaned_files) == 1:
                            file_name = list(cleaned_files.keys())[0]
                            cleaned_content = cleaned_files[file_name]
                            st.download_button(
                                label=f'Download {file_name}',
                                data=cleaned_content,
                                file_name=file_name,
                                mime='text/plain',
                                use_container_width=True
                            )
                        else:
                            zip_buffer = logic.create_zip(cleaned_files)
                            st.download_button(
                                label='📦 Download All Cleaned Files (.zip)',
                                data=zip_buffer.getvalue(),
                                file_name='removeKomments_cleaned.zip',
                                mime='application/zip',
                                use_container_width=True
                            )

                        with st.expander("Preview Processed Files"):
                            for fname, content in cleaned_files.items():
                                st.subheader(fname)
                                st.download_button(
                                    label=f'Download {fname}',
                                    data=content,
                                    file_name=fname,
                                    mime='text/plain',
                                    key=f"dl_{fname}"
                                )
                                st.code(content[:1000] + ('\n...' if len(content) > 1000 else ''), language='text')

        # Tab 2: Process Local Directory Directly
        with tab_dir:
            st.badge("You can try './testFiles' to see how this tab works, if you want it to work with your local directories clone the repo.", icon="⚠️", color="yellow")
            dir_path = st.text_input(
                'Enter directory path:',
                placeholder=r'e.g. C:\Projects\my_app or ./testFiles',
                key="dir_path_input"
            )
            ignore_common = st.checkbox(
                "Ignore common folders (.git, venv, node_modules, __pycache__)",
                value=True,
                key="chk_ignore"
            )

            if dir_path:
                if not os.path.exists(dir_path):
                    st.error("The specified path does not exist.")
                elif not os.path.isdir(dir_path):
                    st.error("The specified path is not a directory.")
                else:
                    ignore_dirs = {'.git', '.svn', '.hg', 'venv', '.venv', 'node_modules', '__pycache__', '.idea', '.vscode'} if ignore_common else set()
                    found_files = logic.scan_directory(dir_path, self.languages, ignore_dirs=ignore_dirs)

                    if not found_files:
                        st.warning("No supported code files (.py, .java, .html, .css, .js) found in this directory.")
                    else:
                        st.success(f"Found **{len(found_files)}** supported file(s) in directory.")
                        with st.expander("View found files"):
                            for full, rel in found_files:
                                st.write(f"- `{rel}`")

                        if st.button('Remove Komments from Directory', key="btn_dir"):
                            with st.spinner("Processing directory..."):
                                cleaned_files = logic.process_directory(dir_path, self.languages, ignore_dirs=ignore_dirs)
                                zip_buffer = logic.create_zip(cleaned_files)

                                st.success(f"Komments removed from {len(cleaned_files)} files!")
                                st.download_button(
                                    label='📦 Download Cleaned Directory (.zip)',
                                    data=zip_buffer.getvalue(),
                                    file_name='directory_cleaned.zip',
                                    mime='application/zip',
                                    use_container_width=True
                                )

                                # Option to save back to disk
                                save_to_disk = st.checkbox("Save cleaned files directly to an output folder", key="chk_save_disk")
                                if save_to_disk:
                                    default_out = os.path.join(dir_path, "cleaned_output")
                                    out_dir = st.text_input("Output folder path:", value=default_out, key="out_folder_input")
                                    if st.button("Save Files to Disk", key="btn_save_disk"):
                                        saved_count = 0
                                        for rel, content in cleaned_files.items():
                                            target = os.path.join(out_dir, rel)
                                            os.makedirs(os.path.dirname(target), exist_ok=True)
                                            with open(target, 'w', encoding='utf-8') as f:
                                                f.write(content)
                                            saved_count += 1
                                        st.success(f"Saved {saved_count} cleaned files to `{out_dir}`")

                                with st.expander("Preview Processed Directory Files"):
                                    for rel, content in cleaned_files.items():
                                        st.subheader(rel)
                                        st.code(content[:1000] + ('\n...' if len(content) > 1000 else ''), language='text')

        st.divider()
        with st.expander("How does this work?"):
            st.markdown("""
            ### Overview
            This app removes **komments** from your code using regular expressions (regex).
            It supports **single files**, **multiple uploaded files**, and **entire directories**.
            
            These are the regex patterns used for each language:
            """)
            st.code(tx.regex, language="python")
            
            st.divider()

            st.markdown("""
            ### The Process
            When you upload files or select a directory and press **'Remove Komments'**, the app identifies each language by its extension and triggers the cleaning method:
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
