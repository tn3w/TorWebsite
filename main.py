import sys

if __name__ != "__main__":
    sys.exit(2)

import os
import logging
from flask import Flask, request, send_file, abort, render_template_string
from utils import WebPage, get_all_files_and_dirs, zip_download

CURRENT_DIR_PATH = os.path.dirname(os.path.abspath(__file__))
PROJECTS_DIR_PATH = os.path.join(CURRENT_DIR_PATH, "projects")
PUBLIC_KEY_PATH = os.path.join(CURRENT_DIR_PATH, "public-key.asc")

if not os.path.isdir(PROJECTS_DIR_PATH):
    os.mkdir(PROJECTS_DIR_PATH)

app = Flask("TN3W-Tor")

log = logging.getLogger('werkzeug')
log.setLevel(logging.WARNING)

@app.route("/")
def index():
    "Returns the main page"

    return WebPage.render_template("index.html")

@app.route("/github")
def github():
    "Returns a warning page before redirecting to Github"

    return WebPage.render_template("redirection_to_github.html")

@app.route("/projects")
@app.route("/projects/")
@app.route("/projects/<project_name>")
def projects(project_name = None):
    """
    Handles requests related to project routes. Renders the project directory or initiates a zip download if applicable.

    :param project_name: Optional project name.
    """

    def render_project_dir():
        "Renders the template for listing the project directory with shortened names."

        files, dirs = get_all_files_and_dirs(PROJECTS_DIR_PATH, recursive = False)

        def revise_list(_list: list):
            new_list = []
            
            for object in _list:
                obj_name = object.split("\\")[-1].replace(PROJECTS_DIR_PATH, "").replace("/", "")
                if len(obj_name) > 12:
                    obj_name = obj_name[:10] + "..."
                obj_path = "/projects" + object.replace(PROJECTS_DIR_PATH, "")
                new_list.append({"name": obj_name, "path": obj_path})
                        
            return new_list

        files, dirs = revise_list(files), revise_list(dirs)

        return WebPage.render_template(
            "list_directory.html", listed_directory = "/", directorys = dirs, files = files,
            path_figure = "?", path_arg = "", is_empty = (len(files) + len(dirs)) == 0
        )

    if project_name is None:
        if request.args.get("as_zip") == "1":
            return zip_download(PROJECTS_DIR_PATH)
        return render_project_dir()
    
    project_path = os.path.join(PROJECTS_DIR_PATH, project_name)
    if not os.path.isdir(project_path):
        if request.args.get("as_zip") == "1":
            return zip_download(PROJECTS_DIR_PATH)
        return render_project_dir()

    def render_directory(directory_path, is_valid_path = True):
        """
        Renders the template for listing a directory with shortened names and navigation links.

        :param directory_path: Path of the directory to render.
        :param is_valid_path: Boolean indicating whether the path is valid.
        """

        files, dirs = get_all_files_and_dirs(directory_path, recursive = False)

        def revise_list(_list: list):
            new_list = []
            
            for object in _list:
                obj_name = object.split("\\")[-1].replace(directory_path, "").replace("/", "")
                if len(obj_name) > 12:
                    obj_name = obj_name[:10] + "..."
                obj_path = "?path=" + object.replace(project_path, "").replace("\\", "/")
                
                new_list.append({"name": obj_name, "path": obj_path})
                        
            return new_list
        
        files, dirs = revise_list(files), revise_list(dirs)

        back_url = "/projects"
        if is_valid_path:
            back_url += "/" + project_name
            
            new_path = os.path.dirname(directory_path.replace(project_path, ""))
            if new_path != "/" and new_path != "\\":
                back_url += "?path=" + new_path
        
        dirs = [{"name": "..", "path": back_url}] + dirs

        directory_path = directory_path.replace(PROJECTS_DIR_PATH, "").replace("\\", "/")
        if directory_path.startswith("\\"):
            directory_path = directory_path[1:]
        if not directory_path.startswith("/"):
            directory_path = "/" + directory_path
        if not directory_path.endswith("/"):
            directory_path += "/"

        path_figure = "?"
        path_arg = ""
        if is_valid_path:
            path_figure = "&"
            path_arg = "?path=" + request.args.get("path")

        return WebPage.render_template(
            "list_directory.html", listed_directory = directory_path, directorys = dirs, files = files,
            path_figure = path_figure, path_arg = path_arg, is_empty = (len(files) + len(dirs)) == 0
        )
    
    files, dirs = get_all_files_and_dirs(project_path)
    files.extend(dirs)

    all_existing_paths = [path.replace(project_path, "").replace("\\", "/") for path in files]

    actual_path = project_path
    is_valid_path = False
    if request.args.get("path") in all_existing_paths:
        new_path = request.args.get("path")
        if new_path.startswith("/"):
            new_path = new_path[1:]
        actual_path = os.path.join(project_path, new_path)
        is_valid_path = True
    
    if not os.path.exists(actual_path):
        return abort(404)
    
    if os.path.isfile(actual_path):
        return send_file(actual_path, as_attachment=True)
    else:
        if request.args.get("as_zip") == "1":
            return zip_download(actual_path)
        return render_directory(actual_path, is_valid_path)

@app.route("/public-key.asc")
def public_key():
    "Returns the public key if it exists"

    if os.path.isfile(PUBLIC_KEY_PATH):
        return send_file(PUBLIC_KEY_PATH, as_attachment=True)
    return "No Public Key found.", 404

@app.route("/cat")
def cat():
    "Returns a cat ascii, as a ping page"

    cat_ascii = """
 ,_     _
 |\\_,-~/
 / _  _ |    ,--.
(  @  @ )   / ,-'
 \  _T_/-._( (
 /         `. \\
|         _  \ |
 \ \ ,  /      |
  || |-_\\__   /
 ((_/`(____,-'
"""
    return render_template_string("<pre>{{ cat }}</pre>", cat=cat_ascii)

@app.errorhandler(404)
def errorhandler_404(_):
    return "Page not found.", 404

app.run(host = "0.0.0.0", port = 8080)