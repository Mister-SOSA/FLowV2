import pyflp
import os
import random


def parse_file(file_path):
    """ Attempt to parse an FLP file, handling any exceptions. """
    try:
        flp_data = pyflp.parse(file_path)
        return {
            'file_id': random.randint(1000000000, 9999999999),
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'title': flp_data.title,
            'tempo': flp_data.tempo,
            'time_spent': flp_data.time_spent.total_seconds(),
            'arrangements': [{'name': arrangement.name} for arrangement in flp_data.arrangements],
            'patterns': [{'name': pattern.name, 'color': pattern.color, 'length': pattern.length} for pattern in flp_data.patterns],
            'channels': [{'name': channel.name, 'color': channel.color, 'type': channel.internal_name} for channel in flp_data.channels],
            'running_time': calculate_arrangement_duration(flp_data.arrangements[0], flp_data.tempo, flp_data.ppq),
            'modified_at': os.path.getmtime(file_path),
            'created_at': os.path.getctime(file_path),
            'tags': [],
            'color': 'blue'
        }
    except Exception as e:
        print(f"Failed to parse {file_path}: {e}")
        return None


def calculate_arrangement_duration(arrangement, bpm, ppq_per_beat):
    max_end_time_ppq = 0
    for track in arrangement.tracks:  # Assuming tracks is a method or property that yields Track objects
        for item in track:  # Here we use the track's __iter__ method implicitly
            # Assuming length is now correctly understood/calculated
            end_time = item.position + item.length
            max_end_time_ppq = max(max_end_time_ppq, end_time)

    # Convert PPQ to seconds
    duration_seconds = (max_end_time_ppq / ppq_per_beat) * (60 / bpm)
    return duration_seconds
