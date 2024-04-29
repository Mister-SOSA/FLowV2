import os
import subprocess
import threading
import datetime
import json
from flask import Flask, render_template, jsonify, request, send_file
import webview
from file_management import get_files
from flp_parser import parse_file
from cache_manager import CacheManager
import platform

app = Flask(__name__)


def load_project_paths():
    """
    Load project paths from the configuration file.

    Returns:
        A list of project paths.
    """
    with open('./config/dirs.json', 'r') as file:
        data = json.load(file)
        return data


@app.route("/")
def loading():
    """
    Render the loading page.
    This page will be displayed while the files are being parsed.
    """
    return render_template('index.html',
                           parse_files=parse_files,
                           number_of_files=sum(1 for _ in get_files('/Users/sosa/Documents/Image-Line/FL Studio/Projects', '.flp')))


@app.route("/dashboard", methods=['GET'])
def dashboard():
    """
    Render the dashboard page.

    Returns:
        The rendered dashboard template.
    """
    project_paths = load_project_paths()
    cache_dir = 'flp_cache'
    cache_manager = CacheManager(cache_dir)
    all_files = []

    for path in project_paths:
        files = [cache_manager.get_cached_data(
            file) for file in get_files(path, '.flp')]
        all_files.extend(files)

    # Sort and filter files
    files = sorted(
        [file for file in all_files if file is not None],
        key=lambda x: x['modified_at'],
        reverse=True
    )

    return render_template('dashboard.html', files=files, now=datetime.datetime.now(), total_time_spent=sum([file['time_spent'] for file in files if file]))


@app.route("/parse-files", methods=['POST', 'GET'])
def parse_files():
    """
    Parse FL Studio project files.

    Returns:
        A JSON response indicating the status of the operation.
    """
    project_paths = load_project_paths()
    cache_dir = 'flp_cache'
    cache_manager = CacheManager(cache_dir)

    print("Parsing files...")
    for path in project_paths:
        files_to_parse = [file for file in get_files(path, '.flp')
                          if not cache_manager.check_cache_validity(file, os.path.getmtime(file))]

        for file in files_to_parse:
            result = parse_file(file)
            if result:
                cache_manager.cache_data(result['file_path'], result)

    return jsonify({"status": "Complete"})


@app.route("/open-project", methods=['POST'])
def open_file():
    """
    Opens a file specified by the 'project_path' parameter in the request JSON.

    Returns:
        A JSON response indicating the status of the operation.
    """
    data = request.get_json()
    file_path = data['project_path']
    if platform.system() == 'Darwin':
        subprocess.call(('open', file_path))
    elif platform.system() == 'Windows':
        subprocess.call(('start', file_path), shell=True)
    elif platform.system() == 'Linux':
        subprocess.call(('xdg-open', file_path))
    else:
        print("Unsupported operating system")
    return jsonify({"status": "Complete"})


@app.route("/open-folder", methods=['POST'])
def open_folder():
    """
    Opens the specified folder path.

    This function takes a JSON payload containing the folder path and opens it using the default file explorer.

    Returns:
        A JSON response indicating the status of the operation.
    """
    data = request.get_json()
    folder_path = data['folder_path']
    if platform.system() == 'Darwin':
        subprocess.call(['open', folder_path])
    elif platform.system() == 'Windows':
        subprocess.call(['explorer', folder_path])
    elif platform.system() == 'Linux':
        subprocess.call(['xdg-open', folder_path])
    else:
        print("Unsupported operating system")
    return jsonify({"status": "Complete"})


@app.route("/change-color", methods=['POST'])
def change_color():
    """
    Change the color of a project.

    This function receives a JSON payload containing the project ID and the new color.
    It updates the cache data for the specified project ID with the new color.

    Returns:
        A JSON response indicating the status of the operation.
    """
    data = request.get_json()
    project_id = data['project_id']
    color = data['color']
    cache_dir = 'flp_cache'
    cache_manager = CacheManager(cache_dir)
    cache_manager.update_cache_data_by_project_id(project_id, {'color': color})
    return jsonify({"status": "Complete"})


@app.route("/clear-cache", methods=['GET'])
def clear_cache():
    """
    Clears the cache directory by removing all JSON files.

    Returns:
        A JSON response indicating the status of the operation.
    """
    cache_dir = 'flp_cache'
    cache_files = os.listdir(cache_dir)
    for file in cache_files:
        os.remove(os.path.join(cache_dir, file))
    return jsonify({"status": "Complete"})


@app.route('/fetch-sample', methods=['POST'])
def fetch_sample():
    """
    Fetches a sample file and sends it as a response.

    This function receives a JSON payload containing the sample path and sends the file as a response.

    Returns:
        The sample file as a response.
    """
    data = request.get_json()
    sample_path = data['sample_path']
    return send_file(sample_path, as_attachment=True)


@app.route('/add-tag', methods=['POST'])
def add_tag():
    """
    Add a tag to a project.

    This function receives a JSON payload containing the project ID and the tag to add.
    It updates the cache data for the specified project ID with the new tag.

    Returns:
        A JSON response indicating the status of the operation.
    """
    data = request.get_json()
    project_id = data['project_id']
    tag = data['tag']
    cache_dir = 'flp_cache'
    cache_manager = CacheManager(cache_dir)
    project = cache_manager.fetch_cached_project_by_id(project_id)
    current_tags = project['tags']
    cache_manager.update_cache_data_by_project_id(
        project_id, {'tags': current_tags + [tag]})
    return jsonify({"status": "Complete"})


@app.route('/delete-tag', methods=['POST'])
def remove_tag():
    """
    Remove a tag from a project.

    This function receives a JSON payload containing the project ID and the tag to remove.
    It updates the cache data for the specified project ID by removing the tag.

    Returns:
        A JSON response indicating the status of the operation.
    """
    print("Removing tag...")
    data = request.get_json()
    project_id = data['project_id']
    tag = data['tag']
    cache_dir = 'flp_cache'
    cache_manager = CacheManager(cache_dir)
    project = cache_manager.fetch_cached_project_by_id(project_id)
    current_tags = project['tags']
    updated_tags = [t for t in current_tags if t != tag]
    cache_manager.update_cache_data_by_project_id(
        project_id, {'tags': updated_tags})
    return jsonify({"status": "Complete"})


def run_flask():
    """
    Run the Flask app.

    This function is executed in a separate thread.
    """
    app.run(port=5000)  # Specify the port to avoid conflicts


if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.daemon = True
    t.start()  # Start the Flask app in a separate thread

    # Create a PyWebview window pointing to the Flask server
    webview.create_window(
        'FLow 0.2.5', 'http://127.0.0.1:5000', width=1280, height=720)
    webview.start(debug=True)
