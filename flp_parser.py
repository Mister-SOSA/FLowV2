import os
import random
import json
from mutagen.mp3 import MP3
from mutagen.wave import WAVE
import pyflp

import pyflp.arrangement
import pyflp.project

BLACKLISTED_SAMPLE_TERMS = json.load(open('./config/blacklist.json'))


def get_audio_duration(file_path):
    """
    Get the duration of an audio file.

    Args:
        file_path (str): The path to the audio file.

    Returns:
        float: The duration of the audio file in seconds.
    """
    if '%FLStudioFactoryData%' in file_path:
        return 0
    if file_path.endswith('.mp3'):
        audio = MP3(file_path)
    elif file_path.endswith('.wav'):
        audio = WAVE(file_path)
    else:
        print(f"Unsupported file format: {file_path}")
    return audio.info.length


def is_valid_sample(sample_path):
    """
    Check if a sample file is valid.

    Args:
        sample_path (str): The path to the sample file.

    Returns:
        bool: True if the sample is valid, False otherwise.
    """
    if not sample_path.endswith('.wav'):
        return False
    print(sample_path.split('/')[-1].lower())
    if any(term in sample_path.split('/')[-1].lower() for term in BLACKLISTED_SAMPLE_TERMS):
        return False
    if '%FLStudioFactoryData%' in sample_path:
        return False
    if '%FLStudioUserData%' in sample_path:
        return False
    if get_audio_duration(sample_path) < 5:
        return False
    return True


def validate_sample(sample):
    """
    Validates a sample file to ensure it is a valid audio file.

    Args:
        sample (pyflp.channel.Sampler): The sample to validate.

    Returns:
        bool: True if the sample is valid, False otherwise.
    """
    try:
        if not isinstance(sample, pyflp.channel.Sampler):
            return False
        if not is_valid_sample(str(sample.sample_path)):
            return False
        if get_audio_duration(str(sample.sample_path)) < 5:
            return False

        return True

    except:
        return False


def parse_file(file_path: str):
    """
    Parses an FL Studio project file and returns a dictionary containing relevant information.

    Args:
        file_path (str): The path to the FL Studio project file.

    Returns:
        dict or None: A dictionary containing the parsed information if successful, or None if an error occurs.
    """
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
            'samples': [{'name': sample.name, 'path': str(sample.sample_path)} for sample in flp_data.channels if validate_sample(sample)],
            'running_time': calculate_arrangement_duration(flp_data.arrangements[0], flp_data.tempo, flp_data.ppq),
            'modified_at': os.path.getmtime(file_path),
            'created_at': os.path.getctime(file_path),
            'tags': [],
            'color': 'blue'
        }
    except Exception as e:
        print(f"Failed to parse {file_path}: {e}")
        return None


def calculate_arrangement_duration(arrangement: pyflp.arrangement, bpm: float, ppq_per_beat: int) -> float:
    """
    Calculate the duration of an arrangement in seconds.

    Args:
        arrangement (pyflp.arrangement): The arrangement to calculate the duration for.
        bpm (float): The beats per minute of the arrangement.
        ppq_per_beat (int): The pulses per quarter note of the arrangement.

    Returns:
        float: The duration of the arrangement in seconds.
    """
    max_end_time_ppq = 0
    for track in arrangement.tracks:
        for item in track:
            end_time = item.position + item.length
            max_end_time_ppq = max(max_end_time_ppq, end_time)

    duration_seconds = (max_end_time_ppq / ppq_per_beat) * (60 / bpm)
    return duration_seconds
