import os
import pathlib

root_directory = "./TODOS"
folders = [f for f in os.listdir("../")]


def create_folder_if_not_exists(folder):

    if not os.path.exists(folder):
        folder_path = os.path.join(root_directory, folder)
        os.makedirs(folder_path)
        print(f"🔵 Successfully created {folder} todos.txt file")

        file_name = 'todos.txt'
        file_path = os.path.join(root_directory, folder, file_name)

        with open(file_path, 'w') as f:
            f.write(f'#{folder} todos')

        print(f"⚪ Successfully created {folder} todos.txt file")

        print("___________________________________________________")
        print(" ")

    else:
        pass


for folder in folders:

    try:
        create_folder_if_not_exists(folder)
    except FileExistsError:
        pass
    except PermissionError:
        print(f"Permission denied: Unable to create '{folder}'")
    except Exception as e:
        print(f"An error occured: {e}")
