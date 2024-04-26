import os
import json


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
