import sys

if __name__ == "__main__":
    sys.exit(2)

import os
import re
from io import BytesIO
import zipfile
from typing import Optional, Tuple
from flask import send_file
from jinja2 import Environment, select_autoescape, Undefined

CURRENT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
TEMPLATES_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "templates")
PROJECTS_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "projects")

class SilentUndefined(Undefined):
    "Class to not get an error when specifying a non-existent argument"

    def _fail_with_undefined_error(self, *args, **kwargs):
        return None

class WebPage:
    "Class with useful tools for WebPages"

    @staticmethod
    def _minimize_tag_content(html: str, tag: str) -> str:
        """
        Minimizes the content of a given tag
        
        :param html: The HTML page where the tag should be minimized
        :param tag: The HTML tag e.g. "script" or "style"
        """

        tag_pattern = rf'<{tag}\b[^>]*>(.*?)<\/{tag}>'
        
        def minimize_tag_content(match: re.Match):
            content = match.group(1)
            content = re.sub(r'\s+', ' ', content)
            return f'<{tag}>{content}</{tag}>'

        return re.sub(tag_pattern, minimize_tag_content, html, flags=re.DOTALL | re.IGNORECASE)

    @staticmethod
    def minimize(html: str) -> str:
        """
        Minimizes an HTML page

        :param html: The content of the page as html
        """

        html = re.sub(r'<!--(.*?)-->', '', html, flags=re.DOTALL)
        html = re.sub(r'\s+', ' ', html)

        html = WebPage._minimize_tag_content(html, 'script')
        html = WebPage._minimize_tag_content(html, 'style')
        return html
    
    @staticmethod
    def render_template(file_name: Optional[str] = None, **args) -> str:
        """
        Function to render a HTML template (= insert arguments / minimization)

        :param file_name: From which file HTML code should be loaded (Optional)
        :param args: Arguments to be inserted into the WebPage with Jinja2
        """

        file_path = os.path.join(TEMPLATES_DIR_PATH, file_name)
        
        if not os.path.isfile(file_path):
            raise FileNotFoundError(f"File `{file_path}` does not exist")
        
        env = Environment(
            autoescape=select_autoescape(['html', 'xml']),
            undefined=SilentUndefined
        )

        with open(file_path, "r", encoding = "utf-8") as file:
            html = file.read()
        
        template = env.from_string(html)

        html = template.render(**args)
        html = WebPage.minimize(html)

        return html

def is_obj_in_gitignore(gitignore_content: str, obj: str) -> bool:
    """
    Checks if a specified object (file or directory) is ignored based on the rules
    defined in a Gitignore file.

    :param gitignore_content: The content of the Gitignore file as a string.
    :param file_path: The path of the object to check for being ignored.
    """
    
    gitignore_content += "\n.git\n.gitignore"

    for ignorance in gitignore_content.split("\n"):
        ignorance = ignorance.strip()
        if not ignorance.startswith("#"):
            if ignorance.endswith("/") or ignorance.endswith("\\"):
                ignorance = ignorance[:-1]
            
            if ignorance.startswith("*") and ignorance.endswith("*"):
                ignorance = ignorance[1:][:-1]
                if ignorance in obj:
                    return True

            elif ignorance.startswith("*"):
                ignorance = ignorance[1:]
                if obj.endswith(ignorance):
                    return True

            elif ignorance.endswith("*"):
                ignorance = ignorance[:-1]
                if obj.startswith(ignorance):
                    return True
            
            if ignorance == obj:
                return True

    return False

def get_all_files_and_dirs(directory_path: str, recursive: Optional[bool] = True) -> Tuple[list, list]:
    """
    This function returns all files and directorys

    :param directory_path: The path to the directory
    :param recursive: If True, the function is called recursively
    """

    if not os.path.isdir(directory_path):
        return [], []

    files = []
    directories = []

    all_objs = os.listdir(directory_path)

    gitignore_content = ""
    if ".gitignore" in all_objs:
        with open(os.path.join(directory_path, ".gitignore"), "r", encoding = "utf-8") as readable_file:
            gitignore_content = readable_file.read()

    for obj in all_objs:
        obj_path = os.path.join(directory_path, obj)
        if not is_obj_in_gitignore(gitignore_content, obj):
            if os.path.isfile(obj_path):
                files.append(obj_path)
            else:
                if recursive:
                    all_files, all_directorys = get_all_files_and_dirs(obj_path)
                    files.extend(all_files)
                    directories.extend(all_directorys)
                directories.append(obj_path)

    return files, directories

def zip_download(directory_path: str) -> send_file:
    """
    Compresses all files in the specified directory into a zip file and sends it for download.

    :param directory_path: The path of the directory containing files to be compressed.
    """

    in_memory_buffer = BytesIO()
    with zipfile.ZipFile(in_memory_buffer, 'a', zipfile.ZIP_DEFLATED, False) as zipf:
        this_directory_path = directory_path
        def add_all_files_to_zip(directory_path: str):
            all_objs = os.listdir(directory_path)

            gitignore_content = ""
            if ".gitignore" in all_objs:
                with open(os.path.join(directory_path, ".gitignore"), "r", encoding = "utf-8") as readable_file:
                    gitignore_content = readable_file.read()

            for obj in all_objs:
                obj_path = os.path.join(directory_path, obj)
                if not is_obj_in_gitignore(gitignore_content, obj):
                    if os.path.isfile(obj_path):
                        zipf.write(obj_path, os.path.relpath(obj_path, this_directory_path))
                    else:
                        add_all_files_to_zip(obj_path)

        add_all_files_to_zip(directory_path)

    in_memory_buffer.seek(0)

    zip_name = directory_path.replace(PROJECTS_DIR_PATH, "").replace("/", "_") + ".zip"
    if zip_name.startswith("_"):
        zip_name = zip_name[1:]
    elif zip_name == ".zip":
        zip_name = "Projects.zip"

    return send_file(in_memory_buffer, as_attachment=True, download_name = zip_name)
