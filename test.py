import pyflp
import os


dir = '/Users/sosa/Documents/Image-Line/FL Studio/Projects/'

FLPs = []

for root, dirs, files in os.walk(dir):
    for file in files:
        if file.endswith('.flp') and 'Brick' in file:
            FLPs.append(pyflp.parse(os.path.join(root, file)))
flp_data = FLPs[0]

arrangements = flp_data.arrangements


def calculate_arrangement_duration(arrangement, bpm, ppq_per_beat):
    max_end_time_ppq = 0
    for track in arrangement.tracks:  # Assuming tracks is a method or property that yields Track objects
        for item in track:  # Here we use the track's __iter__ method implicitly
            # Assuming length is now correctly understood/calculated
            end_time = item.position + item.length
            max_end_time_ppq = max(max_end_time_ppq, end_time)

    # Convert PPQ to seconds  # Common value for FL Studio, adjust if your configuration is different
    duration_seconds = (max_end_time_ppq / ppq_per_beat) * (60 / bpm)
    return duration_seconds


# Example usage
# Assuming 'arrangements' is an instance of Arrangements loaded with your .flp data
# And you want to get the duration of the first arrangement
 # You will need to fetch or know the actual BPM of your project
# or arrangements[0] if indexing is supported
arrangement = next(iter(arrangements))
duration = calculate_arrangement_duration(
    arrangement, flp_data.tempo, flp_data.ppq)
# print in MM:SS format
print(
    f"The running time of the arrangement is: {duration // 60}:{duration % 60}")
