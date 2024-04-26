import os
from flask import Flask, render_template, jsonify, request, send_file
from flaskwebgui import FlaskUI
from file_management import get_files
from flp_parser import parse_file
from cache_manager import CacheManager
import datetime

app = Flask(__name__)


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
    This page will display the parsed FL Studio project files.
    """

    flp_dir = '/Users/sosa/Documents/Image-Line/FL Studio/Projects'
    cache_dir = 'flp_cache'
    cache_manager = CacheManager(cache_dir)

    files = [cache_manager.get_cached_data(
        file) for file in get_files(flp_dir, '.flp')]

    # sort the files by the last modified date
    files = sorted(
        [file for file in files if file is not None],
        key=lambda x: x['modified_at'],
        reverse=True
    )

    return render_template('dashboard.html', files=files, now=datetime.datetime.now(), total_time_spent=sum([file['time_spent'] for file in files]))


@ app.route("/parse-files", methods=['POST', 'GET'])
def parse_files():
    """
    Parse all FL Studio project files in the specified directory.

    Returns:
        dict: A JSON response indicating the status of the parsing operation.
    """
    print("Parsing files...")
    flp_dir = '/Users/sosa/Documents/Image-Line/FL Studio/Projects'
    cache_dir = 'flp_cache'
    cache_manager = CacheManager(cache_dir)

    files_to_parse = [file for file in get_files(flp_dir, '.flp')
                      if not cache_manager.check_cache_validity(file, os.path.getmtime(file))]

    for file in files_to_parse:
        result = parse_file(file)
        if result:
            cache_manager.cache_data(result['file_path'], result)

    return jsonify({"status": "Complete"})


@ app.route("/open-project", methods=['POST'])
def open_file():
    """
    Opens a file specified by the 'project_path' parameter in the request JSON.

    Returns:
        A JSON response indicating the status of the operation.
    """
    data = request.get_json()
    file_path = data['project_path']
    os.system(f'open "{file_path}"')
    return jsonify({"status": "Complete"})


@ app.route("/open-folder", methods=['POST'])
def open_folder():
    """
    Opens the specified folder path.

    This function takes a JSON payload containing the folder path and opens it using the default file explorer.

    Returns:
        A JSON response indicating the status of the operation.
    """
    data = request.get_json()  # Use get_json() to properly parse the JSON data
    folder_path = data['folder_path']
    os.system(f'open "{folder_path}"')
    return jsonify({"status": "Complete"})


@ app.route("/change-color", methods=['POST'])
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


@ app.route("/clear-cache", methods=['GET'])
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


if __name__ == "__main__":
    FlaskUI(app=app, server="flask").run()
