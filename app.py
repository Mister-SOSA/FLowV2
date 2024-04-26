import os
from flask import Flask, render_template, jsonify, request
from flaskwebgui import FlaskUI
from file_management import get_files
from flp_parser import parse_file
from cache_manager import CacheManager
import datetime

app = Flask(__name__)


@app.route("/")
def loading():
    return render_template('index.html',
                           parse_files=parse_files,
                           number_of_files=sum(1 for _ in get_files('/Users/sosa/Documents/Image-Line/FL Studio/Projects', '.flp')))


@app.route("/dashboard", methods=['GET'])
def dashboard():
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

    return render_template('dashboard.html', files=files, now=datetime.datetime.now())


@ app.route("/parse-files", methods=['POST', 'GET'])
def parse_files():
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


@ app.route("/home", methods=['GET'])
def home():
    return render_template('index.html')


if __name__ == "__main__":
    FlaskUI(app=app, server="flask").run()
