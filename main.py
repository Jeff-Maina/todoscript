import os
import pathlib
import json
import time
from yaspin import yaspin
from utils import get_configuration, linebreak

config = get_configuration()


root_directory = config['root_folder']
parent_folder = config['parent_folder_name']
file_format = config['file_format']
folders = [f for f in os.listdir(root_directory)]


def configure(config, is_editing=False):

    root_folder = config['root_folder']
    parent_folder_name = config['parent_folder_name']
    file_format = config['file_format']
    theme = config['theme']

    # create config file

    file_name = 'config.json'

    json_object = json.dumps(config, indent=4)

    try:
        with yaspin(text="Setting up config.json...", color='light_magenta') as sp:
            try:
                with open(file_name, 'w') as f:
                    f.write(json_object)

                time.sleep(1)
                sp.write("✅ Configurations saved.")
                print(" ")
            except (IOError, PermissionError) as e:
                sp.write("❌ Failed to save configurations")
                print(f"Error: {e}")
    except Exception as e:
        print(f"An unexpected error occured: {e}")

    # create todos folder
    if not is_editing:
        try:
            with yaspin(text=f'Creating {parent_folder_name} folder...', color='light_magenta') as sp:
                os.makedirs(parent_folder_name)
                time.sleep(2)
                sp.write(f"✅ {parent_folder_name} folder created.")
        except FileExistsError:
            print(f"Folder {parent_folder_name} already exists:(")
        except PermissionError:
            print(f"Permission denied: Unable to create {parent_folder_name}")
        except Exception as e:
            print(f"An error occured: {e}")


def create_folder_if_not_exists(folder):


    if not os.path.exists(folder):
        folder_path = os.path.join(parent_folder, folder)
        with yaspin(text=f'Creating {folder}...', color='light_magenta') as sp:
            time.sleep(0.2)
            os.makedirs(folder_path)
            sp.write(f"🔵 Successfully created {folder} folder")

        file_name = f'todos.{file_format}'
        file_path = os.path.join(parent_folder, folder, file_name)

        with yaspin(text=f"Creating todo.{file_format}...", color="light_magenta")as sp:
            with open(file_path, 'w') as f:
                time.sleep(0.2)
                sp.write(f"⚪ Successfully created {folder} todos.{file_format} file")
    else:
        pass


def create_tasks():
    linebreak()
    for folder in folders:
        try:
            create_folder_if_not_exists(folder)
        except FileExistsError:
            pass
        except PermissionError:
            print(f"Permission denied: Unable to create '{folder}'")
        except Exception as e:
            print(f"An error occured: {e}")


def get_folders():
    data = []
    for folder in folders:
        data.append(folder)

    return data


