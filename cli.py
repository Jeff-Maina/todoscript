#!/usr/bin/env python3

from InquirerPy import inquirer, prompt, get_style
from InquirerPy.validator import NumberValidator, EmptyInputValidator
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
from rich.text import Text
from InquirerPy.prompts.expand import ExpandChoice

import time
from yaspin import yaspin
from InquirerPy.validator import PathValidator
from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

import os
import mimetypes
import tempfile
import webbrowser
import subprocess
import re

from main import configure, create_tasks, get_folders
from utils import open_file, has_been_configured, export_tasks, clear_terminal, linebreak, get_configuration, generate_reports
from constants import file_formats, themes, main_menu_options
custom_syles = get_style(
    {
        "questionmark": "#EB5B00 bold",
        "answermark": "#e5c07b",
        "answer": "#61afef",
        "input": "#98c379",
        "question": "#6c6c6c",
        "answered_question": "",
        "instruction": "#abb2bf",
        "long_instruction": "#abb2bf",
        "pointer": "#48bfef",
        "checkbox": "#98c379",
        "separator": "#626262",
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

    menu_option = inquirer.fuzzy(
        message="Choose action",
        choices=main_menu_options,
        pointer=" >",
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

    if menu_option == 4:
        view_reports()

    if menu_option == 5:
        clear_terminal()

        exit_app()


def view_reports():

    clear_terminal()

    linebreak()
    console.print("[red bold] Reports")
    linebreak()

    all_folders = get_folders()

    reports_table = Table(title="Tasks")

    reports_data = []

    reports_table.add_column("ID", justify="center", style="bright_cyan")
    reports_table.add_column("Folder", justify="left", style="#e5c07b")
    reports_table.add_column("Progress", justify="left", style="#e5c07b")

    for fol_index, folder in enumerate(all_folders):
        total_tasks = 0
        completed_tasks = 0
        pending_tasks = 0

        with open(os.path.join(config['parent_folder_name'], folder, 'todos.txt'), 'r') as file:
            for index, line in enumerate(file):
                line = line.rstrip("\n")

                if line[:3] == '[x]':
                    completed_tasks += 1
                if line[:3] == '[ ]':
                    pending_tasks += 1

                if line[:3] == '[ ]' or line[:3] == '[x]':
                    total_tasks += 1

                percentage_complete = round(
                    (completed_tasks / total_tasks) * 100) if total_tasks > 0 else 0
                bars = int(percentage_complete / 10) if total_tasks > 0 else 0
                strokes = 10 - bars

                graph = f"[{'[white]█[/white]'*bars}{'-'*strokes}]"

                stats = f"{graph} {percentage_complete}% ({completed_tasks}/{total_tasks})"

        reports_data.append({
            'id': fol_index + 1,
            'project': folder,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'total_tasks': total_tasks
        })

        reports_table.add_row(str(fol_index + 1), folder, stats)

    console.print(reports_table)

    linebreak()

    reports_menu_options = [
        Choice(name=' Return to the main menu', value=0),
        Choice(name=' Export reports', value=1),
        Choice(name=" Exit application", value=2)
    ]

    selected_option = inquirer.select(
        message='Select option',
        style=custom_syles,
        choices=reports_menu_options
    ).execute()

    if selected_option == 0:
        main_menu()

    if selected_option == 1:
        format_options = [
            Choice(name='CSV', value='csv'),
            Choice(name='JSON', value='json'),
            Choice(name='HTML', value='html'),
            Choice(name='SVG', value='svg'),
        ]

        selected_formats = inquirer.select(
            message='Select format',
            style=custom_syles,
            choices=format_options,
            multiselect=True

        ).execute()

        clear_terminal()

        linebreak()
        console.print("[red bold] Reports exported")
        linebreak()
        generate_reports(reports_data, reports_table, selected_formats)

        report_menu_options = [
            Choice(name="Go back to reports", value=0),
            Choice(name="Return to the main menu", value=1),
            Choice(name="Open report in browser", value=2),
            Choice(name="Exit application", value=3),
        ]

        linebreak()

        selected_reports_option = inquirer.select(
            message='Select option',
            style=custom_syles,
            choices=report_menu_options
        ).execute()

        if selected_reports_option == 0:
            view_reports()

        if selected_reports_option == 1:
            main_menu()

        if selected_reports_option == 2:
            webbrowser.open("reports/reports_table.html")
            view_reports()

        if selected_reports_option == 3:
            exit_app()

    if selected_option == 2:
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
        Separator(line=15 * " "),
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
        Choice(name="Return to the main menu", value=1),
        Choice(name='Exit application', value=2)
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


def view_folder_tasks(folder, prev='', tasks_filter=''):
    clear_terminal()

    last_index = 0

    linebreak()
    all_items = 0
    completed = 0
    pending_tasks = 0

    task_list = []
    all_tags = []

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

        percentage_done = round(completed/all_items *
                                100) if all_items > 0 else 0
        total_bars = int(percentage_done/100 * 10) if all_items > 0 else 0
        bars = "█" * total_bars
        strokes = "-" * (10-total_bars)

        progress_bar = f' [bright_white underline]{folder} tasks[/bright_white underline] [grey39][{completed}/{all_items}] [/grey39]'
        # Display the counts at the top before tasks
        console.print(progress_bar)
        linebreak()

        with open(file_path, encoding='utf-8') as file:
            for index, line in enumerate(file, start=1):
                task_list.append(f"{line.strip()}")

                last_index += 1
                line = line.rstrip("\n")

                tags = [x for x in line.split(" ") if x.startswith("@")]

                for tag in tags:
                    all_tags.append(tag)

                status = "completed" if line[:3] == "[x]" else "pending"

                if tasks_filter == '' or tasks_filter == 'all':
                    render_task(line, index)
                    
                
                if tasks_filter and tasks_filter == status:
                    render_task(line, index)

                if tasks_filter.startswith("@") and tasks_filter in line.split():
                    render_task(line, index)
              


                
    linebreak()

    menu_options = [
        Choice(name='Select tasks', value=0),
        Choice(name='Add task', value=1),
        Choice(name='Filter tasks', value=2),
        Choice(name='Edit task', value=3),
        Choice(name='Import/ Export tasks', value=4),
        Choice(name='Back to projects', value=5),
        Choice(name='Back to main menu', value=6),
        Choice(name='Exit application', value=7)
    ]

    option = inquirer.fuzzy(
        message='Select option',
        choices=menu_options,
        default=0,
        style=custom_syles,
        pointer='>'
    ).execute()

    if option == 0:
        selected_tasks = inquirer.text(
            message="Enter task indices (comma-separated)",
            style=custom_syles,
        ).execute()

        selected_tasks_indices = [
            int(i.strip()) for i in selected_tasks.split(",") if i.strip().isdigit()]

        view_selected_tasks(
            task_list, selected_tasks_indices, file_path, folder)

    # add todo
    if option == 1:
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

    #    filter tasks
    if option == 2:

        filter_categories = [
            {"key": "s", "value": "status", "name": "Filter by Status"},
            {"key": "t", "value": "tag", "name": "Filter by Tags"},
            {"key": "p", "value": "priority", "name": "Filter by Priority"},
        ]

        status_filters = [
            {"key": "a", "value": "all", "name": "All tasks"},
            {"key": "c", "value": "completed", "name": "Completed tasks"},
            {"key": "p", "value": "pending", "name": "Pending tasks"},
        ]


        tag_filters = []

        for index,tag in enumerate(list(dict.fromkeys(all_tags))):
            tag_dict = {
                "key" : f'{index}',
                "value": tag,
                "name" : tag
            }

            tag_filters.append(tag_dict)

        
        

        filter_type = inquirer.expand(
            message="How would you like to filter?",
            instruction='press h to view all choices',
            choices=filter_categories,
        ).execute()

        if filter_type == "status":
            result = inquirer.expand(
                message="Select status filter:",
                instruction='press h to view all choices',
                choices=status_filters,
                pointer='>'
            ).execute()

            view_folder_tasks(folder, '', result)
            print("Invalid selection!")

        if filter_type == 'tag':
            result = inquirer.expand(
                message="Select tag filter:",
                instruction='press h to view all choices',
                choices=tag_filters,
            ).execute()

            view_folder_tasks(folder, '', result)
            print("Invalid selection!")
    # edit task
    if option == 3:
        task_index = inquirer.number(
            message="Enter task index",
            min_allowed=1,
            max_allowed=last_index,
            validate=EmptyInputValidator(),
            style=custom_syles
        ).execute()

        selected_task = task_list[int(task_index) - 1].rstrip()

        edit_task = inquirer.text(
            message='Edit task',
            style=custom_syles,
            default=selected_task[3:]
        ).execute()

        confirm_edit = inquirer.confirm(
            message='Save changes',
            default=True,
            style=custom_syles
        ).execute()

        task_status = selected_task[:3]

        if confirm_edit:
            try:
                with open(file_path, 'r') as edit_file, tempfile.NamedTemporaryFile('w', delete=False) as edit_temp_file:
                    edit_temp_name = edit_temp_file.name

                    for index, line in enumerate(edit_file):
                        line = line.rstrip("\n")
                        if index == (int(task_index) - 1):
                            edit_temp_file.write(f"{task_status}{edit_task}\n")
                        else:
                            edit_temp_file.write(f"{line}\n")

                os.replace(edit_temp_name, file_path)
            except Exception as e:
                if 'edit_temp_name' in locals():
                    os.unlink(edit_temp_name)
                print(f"An error occured: {e}")
            view_folder_tasks(folder)
        else:
            view_folder_tasks(folder)

    if option == 4:

        selection_options = [
            Choice(name='Import tasks from project', value='import'),
            Choice(name='Export tasks', value='export')
        ]

        export_or_import = inquirer.select(
            message="Select option",
            choices=selection_options,
            default='import',
            style=custom_syles,
            pointer='>'
        ).execute()

      
        if export_or_import == 'export':
            export_format_options = [
                Choice(name="Markdown (.md)", value="md"),
                Choice(name="JSON (.json)", value="json"),
                Choice(name="CSV (.csv)", value="csv"),
                Choice(name="YAML (.yaml)", value="yaml"),
                Choice(name="HTML (.html)", value="html")
            ]
            

            export_format = inquirer.select(
                message="Select format to export tasks",
                choices=export_format_options,
                default="txt",
                style=custom_syles,
                pointer=">"
            ).execute()

            delimiter = ','

            if export_format == 'csv':

                select_delimeter = inquirer.text(
                    message="Enter delimiter",
                    default=",",
                    style=custom_syles
                ).execute()

                delimiter = select_delimeter

            export_tasks(folder, task_list, export_format, delimiter)

            linebreak()

            view_export = inquirer.select(
                message="Select option",
                default=False,
                style=custom_syles,
                choices=[
                    Choice(name="View exported file", value=True),
                    Choice(name="Go back to tasks", value=False)
                ]
            ).execute()

            file_name = ''

            if export_format == 'md':
                file_name = 'exported_tasks.md'
            if export_format == 'json':
                file_name = 'exported_tasks.json'
            if export_format == 'csv':
                file_name = 'exported_tasks.csv'
            if export_format == 'yaml':
                file_name = 'exported_tasks.yaml'
            if export_format == 'txt':
                file_name = 'exported_tasks.txt'
            if export_format == 'html':
                file_name = 'exported_tasks.html'

            export_file_path = os.path.join(
                config['parent_folder_name'], folder, 'exports', file_name)

            linebreak()
            if view_export == True:
                with yaspin(text=f'Opening {file_name}...', color='light_magenta') as sp:
                    time.sleep(0.3)

                if export_format == 'html':
                    webbrowser.open(export_file_path)
                else:
                    open_file(export_file_path)
                view_folder_tasks(folder, prev='')
            else:
                view_folder_tasks(folder, prev='')

        if export_or_import == 'import':
            view_folder_tasks(folder)

    # back to projects
    if option == 5:
        view_projects()
    # main menu
    if option == 6:
        main_menu()
    # exit
    if option == 7:
        exit_app()
    # export tasks


def view_selected_tasks(tasks, selected_indices, file_path, folder):
    clear_terminal()
    print(file_path)

    linebreak()

    selected_tasks = [
        f"{task}" for i, task in enumerate(tasks) if i in selected_indices
    ]

    console.print(
        f"  [underline]Selected tasks [/] [grey39]{len(selected_tasks)} selected.")

    linebreak()

    for index, task in enumerate(selected_tasks):
        render_task(task, index)

    linebreak()

    def change_status(status):
        task_status = "[x]" if status == 'complete' else "[ ]"

        try:
            with open(file_path, 'r') as file, tempfile.NamedTemporaryFile("w", delete=False) as temp_file:
                temp_file_name = temp_file.name

                for index, line in enumerate(file):
                    line = line.rstrip("\n")

                    if index in selected_indices:
                        temp_file.write(f"{task_status}{line[3:]} \n")
                        print(line)
                    else:
                        temp_file.write(f'{line}\n')

            os.replace(temp_file_name, file_path)
        except Exception as e:
            if 'temp_file_name' in locals():
                os.unlink(temp_file_name)
            print(f"An error occurred: {e}")

    # menu

    action_options = [
        Choice(name="Mark as complete", value=1),
        Choice(name="Mark as incomplete", value=2),
        Choice(name="Add tags", value=3),
        Choice(name="Delete Tasks", value=4),
        Choice(name="Back to task list", value=5),
    ]

    action = inquirer.fuzzy(
        message=' Choose action',
        choices=action_options,
        style=custom_syles,
        pointer=' >',
    ).execute()

    linebreak()

    if action == 1:
        change_status('complete')
        view_folder_tasks(folder)

    if action == 2:
        change_status('incomplete')
        view_folder_tasks(folder)

    if action == 3:
        tags = inquirer.text(
            message='Enter tags (use comma-separated list)', style=custom_syles
        ).execute()

        added_tags = tags.split(',')

        try:
            with open(file_path, 'r') as file, tempfile.NamedTemporaryFile("w", delete=False) as temp_file:
                temp_file_name = temp_file.name

                for index, line in enumerate(file):
                    line = line.rstrip("\n")

                    if index in selected_indices:
                        temp_file.write(
                            f"{line.rstrip()} {' '.join([f'@{tag.strip()}' for tag in added_tags])}\n")
                        print(line)
                    else:
                        temp_file.write(f'{line}\n')

            os.replace(temp_file_name, file_path)
        except Exception as e:
            if 'temp_file_name' in locals():
                os.unlink(temp_file_name)
            print(f"An error occurred: {e}")

        view_folder_tasks(folder)

    if action == 4:
        try:
            with yaspin(text='Deleting task...', color="light_magenta") as sp:
                with open(file_path, 'r') as file, tempfile.NamedTemporaryFile("w", delete=False) as temp_file:
                    temp_file_name = temp_file.name
                    for index, line in enumerate(file):
                        if index + 1 not in selected_indices:
                            temp_file.write(line)
                        if index + 1 in selected_indices:
                            sp.write(f'Deleted {line[3:]}')

            os.replace(temp_file_name, file_path)

        except Exception as e:
            if 'temp_file_name' in locals():
                os.unlink(temp_file_name)
            print(f"An error occured: {e}")

        view_folder_tasks(folder, prev='delete')


def render_task(line, index):
    status = '✔' if line[:3] == '[x]' else '☐'

    styled_line = Text(f"  {index}. {status} {line[3:]}") if index > 9 else Text(
        f"  {index}.  {status} {line[3:]}")

    text = 'grey39' if line[:3] == '[x]' else 'bright_white'

    styled_line.stylize(
        text, len(str(index)) + 7, len(styled_line))

    styled_line.stylize("grey39", 0, 6)

    for match in re.finditer(r'@(\w+)', line):
        start, end = match.span()
        styled_line.stylize("yellow", start + 5, end + 5)

    console.print(styled_line, markup=False)


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
