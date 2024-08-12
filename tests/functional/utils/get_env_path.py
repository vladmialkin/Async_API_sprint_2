import os


def detect_env_file(file_name: str, path: str) -> str:
    for root, dirs, files in os.walk(path):
        if file_name in files:
            return os.path.join(root, file_name)
