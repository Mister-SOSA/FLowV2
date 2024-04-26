import pyflp
import os


def parse_file(file_path):
    """ Attempt to parse an FLP file, handling any exceptions. """
    try:
        flp_data = pyflp.parse(file_path)
        return {
            'file_path': file_path,
            'file_name': os.path.basename(file_path),
            'title': flp_data.title,
            'tempo': flp_data.tempo,
            'time_spent': flp_data.time_spent.total_seconds(),
            'arrangements': [{'name': arrangement.name} for arrangement in flp_data.arrangements],
            'patterns': [{'name': pattern.name, 'color': pattern.color, 'length': pattern.length} for pattern in flp_data.patterns],
            'channels': [{'name': channel.name, 'color': channel.color, 'type': channel.internal_name} for channel in flp_data.channels],
            'modified_at': os.path.getmtime(file_path),
            'created_at': os.path.getctime(file_path)
        }
    except Exception as e:
        print(f"Failed to parse {file_path}: {e}")
        return None
