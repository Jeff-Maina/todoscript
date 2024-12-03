from InquirerPy import inquirer, prompt, get_style
from InquirerPy.validator import NumberValidator
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
import time
from yaspin import yaspin
from InquirerPy.validator import PathValidator
from InquirerPy.base.control import Choice

import os
import mimetypes

from main import configure, create_tasks, get_folders
from utils import has_been_configured, clear_terminal, linebreak, get_configuration
from constants import file_formats, themes, menu_options
custom_syles = get_style(
    {
        "questionmark": "#EB5B00 bold",
        "answermark": "#e5c07b",
        "answer": "#61afef",
        "input": "#98c379",
        "question": "#fff",
        "answered_question": "",
        "instruction": "#abb2bf",
        "long_instruction": "#abb2bf",
        "pointer": "#A1EEBD bold",
        "checkbox": "#98c379",
        "separator": "",
        "skipped": "#5c6370",
        "validator": "",
        "marker": "#e5c07b",
        "fuzzy_prompt": "#c678dd",
        "fuzzy_info": "#abb2bf",
        "fuzzy_border": "#4b5263",
        "fuzzy_match": "#c678dd",
        "spinner_pattern": "#e5c07b",
        "spinner_text": "", }
)

console = Console()

config = get_configuration()
# DATA


def set_configuration():
    clear_terminal()
    print(" ")
    console.print(
        "[bold cyan]Welcome to the TODO Management CLI![/bold cyan]\n")

    root_folder = inquirer.filepath(
        message="Enter the root folder path: (leave blank for current directory)",
        style=custom_syles,
        default='../',
        validate=PathValidator(
            is_dir=True, message='Input is not a valid folder')
    ).execute()

    parent_folder_name = inquirer.text(
        message='What should we name the folder to hold generated TODOs? (Default: TODOs)',
        style=custom_syles,
        default='TODOs',
        validate=lambda name: not any(char in name for char in ['/', ':']),
        invalid_message='Invalid folder name (cannot contain "/" or ":")'
    ).execute()

    file_format = inquirer.select(
        message="Select the file format:",
        choices=file_formats,
        default='txt',
        pointer=">",
        style=custom_syles,
        validate=lambda result: len(result) > 0,
        instruction="(Default: .txt)",
        invalid_message="Please select a file format.",
    ).execute()

    theme = inquirer.select(
        message="Select preferred theme:",
        choices=themes,
        pointer=">",
        style=custom_syles,
        instruction="(Default: vesper)",
    ).execute()

    linebreak()
    console.print("[#e5c07b] Configurations summary:")
    linebreak()
    console.print(f"- Projects location: [#61afef bold] {root_folder}")
    console.print(f"- TODOs folder name: [#61afef bold] {parent_folder_name}")
    console.print(f"- File format: [#61afef bold] {file_format}")
    console.print(f"- Theme: [#61afef bold] {theme}")

    linebreak()
    confirm = inquirer.confirm(
        message="Save configuration?", default=True).execute()
    linebreak()

    if confirm:
        config = {
            'root_folder': root_folder, 'parent_folder_name': parent_folder_name, 'file_format': file_format, 'theme': theme
        }

        configure(config)

        linebreak()

        main_menu_confirmation = inquirer.confirm(
            message="Proceed to main menu?", default=True).execute()

        if main_menu_confirmation:
            main_menu()

    else:
        console.print(
            "[red bold] Configuration not saved. Exiting the setup process.")


def main_menu():
    clear_terminal()

    linebreak()
    console.print("[red bold] Main menu")
    linebreak()

    menu_option = inquirer.rawlist(
        message="Select an option",
        choices=menu_options,
        pointer=">",
        style=custom_syles,
        default=0
    ).execute()

    if menu_option == 0:
        generate_tasks()

    if menu_option == 1:
        view_projects()

    if menu_option == 2:
        view_configuration()

    if menu_option == 3:
        update_configuration()

    if menu_option == 5:
        clear_terminal()

        exit_app()


def view_configuration():
    clear_terminal()

    linebreak()
    console.print("[red bold] View configurations")
    linebreak()

    data = get_configuration()

    root_folder = data['root_folder']
    parent_folder_name = data['parent_folder_name']
    file_format = data['file_format']
    theme = data['theme']

    console.print(f"- Projects location: [#61afef bold] {root_folder}")
    console.print(f"- TODOs folder name: [#61afef bold] {parent_folder_name}")
    console.print(f"- File format: [#61afef bold] {file_format}")
    console.print(f"- Theme: [#61afef bold] {theme}")

    linebreak()

    menu_options = [
        Choice(name='Go back to main menu', value=0),
        Choice(name='Update configuration', value=1)
    ]

    option = inquirer.rawlist(
        message="Select option",
        choices=menu_options,
        default=0,
        style=custom_syles,
        pointer='>'
    ).execute()

    if option == 0:
        main_menu()
    else:
        update_configuration()


def update_configuration():
    clear_terminal()

    linebreak()
    console.print("[red bold] Edit configurations")
    linebreak()

    data = get_configuration()

    root_folder = data['root_folder']
    parent_folder_name = data['parent_folder_name']
    file_format = data['file_format']
    theme = data['theme']

    root_folder_input = inquirer.filepath(
        message="Enter the root folder path: (leave blank for current directory)",
        style=custom_syles,
        default=root_folder,
        validate=PathValidator(
            is_dir=True, message='Input is not a valid folder')
    ).execute()

    file_format_input = inquirer.select(
        message="Select the file format:",
        choices=file_formats,
        default=file_format,
        pointer=">",
        style=custom_syles,
        validate=lambda result: len(result) > 0,
        instruction="(Default: .txt)",
        invalid_message="Please select a file format.",
    ).execute()

    theme_input = inquirer.select(
        message="Select preferred theme:",
        choices=themes,
        pointer=">",
        default=theme,
        style=custom_syles,
        instruction="(Default: vesper)",
    ).execute()

    linebreak()
    console.print("[#e5c07b] Configurations summary:")
    linebreak()
    console.print(
        f"[red]-[bold white]Projects location: [#61afef bold] {root_folder_input}")
    console.print(
        f"[red]-[bold white]File format: [#61afef bold] {file_format_input}")
    console.print(f"[red]-[bold white]Theme: [#61afef bold] {theme_input}")

    linebreak()
    confirm = inquirer.confirm(
        message="Save configuration?", default=True).execute()
    linebreak()

    if confirm:
        config = {
            'root_folder': root_folder_input, 'parent_folder_name': parent_folder_name, 'file_format': file_format_input, 'theme': theme_input
        }

        configure(config, is_editing=True)

        main_menu_confirmation = inquirer.confirm(
            message="Proceed to main menu?", default=True).execute()

        if main_menu_confirmation:
            main_menu()

    else:
        console.print(
            "[red bold] Configuration not saved. Exiting the setup process.")


def generate_tasks():
    create_tasks()
    linebreak()
    console.print('[bold white] process completed')
    linebreak()

    menu_options = [
        Choice(name='View projects', value=0),
        Choice(name='Go back to main menu ', value=1),
        Choice(name='Exit ', value=2)
    ]

    option = inquirer.rawlist(
        message="Select option",
        choices=menu_options,
        default=0,
        style=custom_syles,
        pointer='>'
    ).execute()

    if option == 0:
        view_projects()

    if option == 1:
        main_menu()

    if option == 2:
        clear_terminal()

        exit_app()


def view_projects():
    clear_terminal()

    linebreak()
    console.print("[red bold] Select Folder")
    linebreak()

    folder_path = os.path.join(config['parent_folder_name'])
    folders = os.listdir(folder_path)
   
    option = inquirer.fuzzy(
        message='Select a folder to view its tasks',
        choices=folders,
        default=0,
        style=custom_syles,
        pointer='>'
    ).execute()

    view_folder_tasks(option)


def view_folder_tasks(folder):
    clear_terminal()

    last_index = 0

    linebreak()
    console.print(f"[red bold] {folder} tasks")
    linebreak()

    root_directory = get_configuration()['parent_folder_name']

    folder_path = os.path.join(root_directory, folder)

    file = [f for f in os.listdir(folder_path) if os.path.isfile(
        os.path.join(folder_path, f))][0]

    file_path = os.path.join(folder_path, file)

    if file.endswith("txt"):
        with open(file_path, encoding='utf-8') as file:
            for last_index, line in enumerate(file):
                line = line.rstrip("\n")
                console.print(line, markup=False)

    menu_options = [
        Choice(name='Add todo', value=0),
        Choice(name='Delete todo', value=1),
        Choice(name='Back to projects', value=2),
        Choice(name='Main menu ', value=3),
        Choice(name='Exit ', value=4)
    ]

    linebreak()

    option = inquirer.select(
        message='Select option',
        choices=menu_options,
        default=0,
        style=custom_syles,
        pointer='>'
    ).execute()

    if option == 0:
        new_todo = inquirer.text(
            message='Enter task title',
            style=custom_syles
        ).execute()

        todo_status = inquirer.select(
            message='Select task status',
            style=custom_syles,
            default="Incomplete",
            choices=[
                Choice(name='Incomplete', value='Incomplete'),
                Choice(name='Complete', value='Complete')
            ]
        ).execute()

        status = '[ ]' if todo_status == 'Incomplete' else '[x]'

        try:
            with yaspin(text='Creating task...', color='light_magenta') as sp:
                time.sleep(0.2)
                with open(file_path, 'a') as file:
                    file.write(f'{last_index + 1}. {status} {new_todo}')
                sp.write("Task added successfully")
        except Exception as e:
            print(e)

    if option == 2:
        view_projects()

    if option == 3:
        main_menu()

    if option == 4:
        exit_app()


def exit_app():
    clear_terminal()
    linebreak()
    console.print("[red bold] Exited todoscript")
    linebreak()


def main():
    if has_been_configured():
        main_menu()
    else:
        set_configuration()


if __name__ == "__main__":
    main()
