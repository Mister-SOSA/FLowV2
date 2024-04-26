import os


def get_files(dir_path, extension):
    """ Retrieve files with a specific extension from given directory, excluding backups. """
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith(extension) and 'Backup' not in root:
                yield os.path.join(root, file)
