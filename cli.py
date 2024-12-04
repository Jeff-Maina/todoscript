from InquirerPy import inquirer, prompt, get_style
from InquirerPy.validator import NumberValidator
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text

import time
from yaspin import yaspin
from InquirerPy.validator import PathValidator
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

import os
import mimetypes
import tempfile

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
        Separator(line=15 * "-"),
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
        Separator(line=15 * "-"),
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


def view_folder_tasks(folder, prev=''):
    clear_terminal()

    last_index = 0

    linebreak()
    console.print(f"[red bold] {folder} tasks")
    linebreak()

    all_items = 0
    completed = 0
    pending_tasks = 0

    root_directory = get_configuration()['parent_folder_name']

    folder_path = os.path.join(root_directory, folder)

    file = [f for f in os.listdir(folder_path) if os.path.isfile(
        os.path.join(folder_path, f))][0]

    file_path = os.path.join(folder_path, file)

    if file.endswith("txt"):
        with open(file_path, encoding='utf-8') as file:
            for line in file:
                line = line.rstrip("\n")
                all_items += 1
                if line[:3] == "[ ]":
                    pending_tasks += 1
                elif line[:3] == "[x]":
                    completed += 1

        percentage_done = round(completed/all_items * 100)
        total_bars = int(percentage_done/100 * 10)
        bars = "█" * total_bars
        strokes = "-" * (10-total_bars)
        
        progress_bar = f'Progress: [white bold] [{bars}{strokes}] [/white bold] {percentage_done}% Complete ({completed}/{all_items})'
        # Display the counts at the top before tasks
        console.print(progress_bar)
        linebreak()

        with open(file_path, encoding='utf-8') as file:
            for index, line in enumerate(file, start=1):
                line = line.rstrip("\n")
                styled_line = Text(f"{index}.{line}") if index > 9 else Text(
                    f"{index}. {line}")

                task_start_point = 4 if index > 9 else 5

                style = "bold green" if line[:3] == '[x]' else "bold"

                styled_line.stylize(style, len(
                    str(index)) + 0, len(styled_line))

                console.print(styled_line, markup=False)

    menu_options = [
        Separator(line=15 * "-"),
        Choice(name='Add todo', value=0),
        Choice(name='Delete todos', value=1),
        Choice(name='Mark todos as complete', value=2),
        Choice(name='Enter edit mode', value=3),
        Separator(line=15 * "-"),
        Choice(name='Back to projects', value=4),
        Choice(name='Main menu ', value=5),
        Choice(name='Exit ', value=6)
    ]

    linebreak()

    option = inquirer.select(
        message='Select option',
        choices=menu_options,
        default=0,
        style=custom_syles,
        pointer='>'
    ).execute()

    linebreak()
    # add todo
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
                Choice(name='Complete', value='Complete'),
                Choice(name='Incomplete', value='Incomplete'),
            ]
        ).execute()

        status = '[ ]' if todo_status == 'Incomplete' else '[x]'

        try:
            with yaspin(text='Creating task...', color='light_magenta') as sp:
                time.sleep(0.2)
                with open(file_path, 'a') as file:
                    file.write(f'{status} {new_todo}\n')
                sp.write("Task added successfully")
        except Exception as e:
            print(e)

        view_folder_tasks(folder)

    # delete todos
    if option == 1:

        task_indices = inquirer.text(
            message='Enter index (0 to cancel)',
            instruction='use comma-separated list to delete multiple items',
            style=custom_syles,

        ).execute()

        task_indices = [int(i.strip())
                        for i in task_indices.split(",") if i.strip().isdigit()]

        try:
            with yaspin(text='Deleting task...', color="light_magenta") as sp:
                with open(file_path, 'r') as file, tempfile.NamedTemporaryFile("w", delete=False) as temp_file:
                    temp_file_name = temp_file.name
                    for index, line in enumerate(file):
                        time.sleep(0.2)
                        if index + 1 not in task_indices:
                            temp_file.write(line)
                        if index + 1 in task_indices:
                            sp.write(f'Deleted {line[3:]}')

            os.replace(temp_file_name, file_path)

        except Exception as e:
            if 'temp_file_name' in locals():
                os.unlink(temp_file_name)
            print(f"An error occured: {e}")
        view_folder_tasks(folder, prev='delete')

    # mark todo complete
    if option == 2:
        indices = inquirer.text(
            message='Enter index (0 to cancel)',
            instruction='use comma-separated list to delete multiple items',
            style=custom_syles,

        ).execute()

        selected_indices = [int(i.strip())
                            for i in indices.split(",") if i.strip().isdigit()]

        try:
            with yaspin(text='Marking task complete...', color='light_magenta') as sp:
                with open(file_path, 'r') as file, tempfile.NamedTemporaryFile("w", delete=False) as temp_file:
                    temp_file_name = temp_file.name
                    for index, line in enumerate(file):
                        if index + 1 in selected_indices:
                            temp_file.write(f"[x]{line[3:]}")
                        else:
                            temp_file.write(f'{line}')

                os.replace(temp_file_name, file_path)
        except Exception as e:
            if 'temp_file_name' in locals():
                os.unlink(temp_file_name)
            print(f"An error occured: {e}")
        view_folder_tasks(folder, prev='mark complete')

    if option == 3:
        edit_mode(folder)

    # back to projects
    if option == 4:
        view_projects()
    # main menu
    if option == 5:
        main_menu()
    # exit
    if option == 6:
        exit_app()


def edit_mode(folder):
    clear_terminal()

    linebreak()
    console.print(f"[red bold] Edit mode")
    linebreak()

    menu_options = {
        Separator(line=15*"-"),
        Choice(name="Back to read mode", value=0)
    }

    option = inquirer.select(
        message='Select option',
        choices=menu_options,
        default=0,
        style=custom_syles,
        pointer='>'
    ).execute()


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
