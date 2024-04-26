import os
import json

CACHE_DIR = './flp_cache'


class CacheManager:
    def __init__(self, cache_dir):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)

    def is_cached(self, file_path):
        return os.path.exists(self.get_cache_path(file_path))

    def get_cache_path(self, file_path):
        return os.path.join(self.cache_dir, os.path.basename(file_path).replace('.flp', '.json'))

    def get_cached_data(self, file_path):
        if self.is_cached(file_path):
            with open(self.get_cache_path(file_path), 'r') as f:
                return json.load(f)
        return None

    def cache_data(self, file_path, data):
        with open(self.get_cache_path(file_path), 'w') as f:
            json.dump(data, f, indent=4)

    def check_cache_validity(self, file_path, modification_time):
        cached_data = self.get_cached_data(file_path)
        if cached_data and cached_data['modified_at'] == modification_time:
            return True
        return False

    def fetch_cached_project_by_id(self, project_id):
        cache_files = os.listdir(CACHE_DIR)

        for file in cache_files:
            with open(os.path.join(CACHE_DIR, file), 'r') as f:
                cached_data = json.load(f)
                if int(cached_data['file_id']) == int(project_id):
                    return cached_data
        return None

    def update_cache_data_by_project_id(self, project_id, data):
        cache_files = os.listdir(CACHE_DIR)

        for file in cache_files:
            with open(os.path.join(CACHE_DIR, file), 'r') as f:
                cached_data = json.load(f)
                if int(cached_data['file_id']) == int(project_id):
                    print(f"Updating cache for {cached_data['file_name']}")
                    cached_data.update(data)
                    with open(os.path.join(CACHE_DIR, file), 'w') as f:
                        json.dump(cached_data, f, indent=4)
                    break
