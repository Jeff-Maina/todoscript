import os.path
import json

# helper functions


def has_been_configured():
    file_name = './config.json'

    if os.path.isfile(file_name):
        return True
    else:
        return False


def is_configuration_present(configuration):
    if has_been_configured:
        with open('config.json', 'r') as file:
            data = json.load(file)

            if (data.get(configuration) is None):
                return False
            else:
                return True


clear_terminal = lambda: os.system('cls||clear')
