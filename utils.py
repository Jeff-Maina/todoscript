import os.path
import json
from rich.console import Console
import webbrowser
import time
from yaspin import yaspin
import os
import subprocess

console = Console(record=True)

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


def linebreak(): return print(" ")


def clear_terminal(): return os.system('cls||clear')


def get_configuration():
    if has_been_configured():
        with open('config.json', 'r') as file:
            data = json.load(file)

            return data
    else:
        return None


# export utils


def generate_reports(reports_data, table, formats):
    if "html" in formats or 'svg' in formats:
        console.print(table)

    reports_folder = 'reports'
    os.makedirs(reports_folder, exist_ok=True)

    tasks = []

    for format in formats:
        tasks.append(f'Generate reports.{format} report')

    for format in formats:
        if format == 'html':
            html_file = 'reports_table.html'

            html = console.export_html(clear=False)

            with open(os.path.join(reports_folder, html_file), 'w') as file:
                file.write(html)

        if format == 'svg':
            svg_file = 'reports_table.svg'

            svg = console.export_svg(clear=False)

            with open(os.path.join(reports_folder, svg_file), 'w') as file:
                file.write(svg)

        if format == 'csv':

            cols = 'Index,Folder,Completed tasks,Pending tasks,Total tasks'

            with open(os.path.join(reports_folder, 'reports.csv'), 'w') as file:
                file.write(f"{cols}\n")
                for data in reports_data:
                    file.write(
                        f"{data['id']},{data['project']},{data['completed_tasks']},{data['pending_tasks']},{data['total_tasks']}\n")

        if format == 'json':
            with open(os.path.join(reports_folder, 'reports.json'), 'w') as file:
                file.write("[\n")
                for index, data in enumerate(reports_data):
                    if index == len(reports_data) - 1:
                        file.write(f"{json.dumps(data)}\n")
                    else:
                        file.write(f"{json.dumps(data)},\n")
                file.write("]\n")

    linebreak()
    with console.status("[bold bright_magenta]Generating reports...") as status:
        while tasks:
            task = tasks.pop(0)
            time.sleep(1)
            console.log(f"{task} complete")


def export_tasks(folder, tasks, format, delimiter=','):
    '''
        md,json,html,csv
    '''

    config = get_configuration()
    tasks_folder = config['parent_folder_name']

    exports_folder = 'exports'
    exports_folder_path = os.path.join(tasks_folder, folder,
                                       exports_folder)
    if os.path.exists(exports_folder_path):
        pass
    else:
        os.makedirs(exports_folder_path, exist_ok=True)

    linebreak()

    tasks_list = []

    def get_tags(task):
        return list(set(f'{tag[1:]}' for tag in task.split(" ") if tag.startswith("@")))

    def get_task_without_tags(task):
        return ' '.join(word for word in task.split(' ') if not word.startswith('@'))

    for index, task in enumerate(tasks):
        tasks_list.append({
            'id': index,
            'task': get_task_without_tags(task[3:]),
            'status': 'Complete' if task[:3] == '[x]' else "Incomplete",
            'tags': get_tags(task)
        })


    if format == 'csv':
        with open(os.path.join(exports_folder_path, 'exported_tasks.csv'), 'w') as file:
            file.write(f"ID{delimiter}Task{delimiter}Tags{delimiter}Status\n")
            for index, task in enumerate(tasks):
                tags = get_tags(task)
                line_without_tags = get_task_without_tags(task)

                file.write(
                    f'{index+1}{delimiter}{line_without_tags}{delimiter}{" | ".join(tags)}{delimiter}{"completed" if task[:3] == "[x]" else "pending"}\n')
            console.print(
                f" [bright_magenta]✔ Successfully generated exported_tasks.csv")

    if format == 'json':
        with open(os.path.join(exports_folder_path, 'exported_tasks.json'), 'w') as file:
            file.write("[\n")
            for index, task in enumerate(tasks_list):
           
                if index == len(tasks_list) - 1:
                    file.write(f"{json.dumps(task)}")
                else:
                    file.write(f"{json.dumps(task)},\n")

            file.write("]\n")
            console.print(f" [bright_magenta]✔ Successfully generated exported_tasks.json")

    if format == 'html':
        html_style = "<style>body{font-family: 'Inter' }#tags_container{display: flex; flex-wrap: wrap; gap: 10px;} .tag{color: #d50dd5; font-weight: 600;} .task{display:flex; gap:10px; align-items: center}</style>"
        linked_styles = '<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin><link href="https://fonts.googleapis.com/css2?family=Inter:ital,opsz,wght@0,14..32,100..900;1,14..32,100..900&display=swap" rel="stylesheet">'
        with open(os.path.join(exports_folder_path, 'exported_tasks.html'), 'w') as file:
            file.write(f"<html><head>{html_style}{linked_styles}</head><body><h1>{folder} tasks</h1><main>\n")
            for index, task in enumerate(tasks_list):
                tags = task['tags']

                tags_html = [f"<span class='tag'>@{tag}</span>" for tag in tags]

                file.write(
                    f'<div class="task"><input type="checkbox" id="task-{index}" {"checked" if task["status"] == "Complete" else ""}><label for="task-{index}">{task["task"]}</label> <div id="tags_container">{",".join(tags_html)}</div></div>'
                )
            file.write("</main></body></html>\n")
            console.print(f" [bright_magenta]✔ Successfully generated exported_tasks.html")

    if format == 'yaml':
        with open(os.path.join(exports_folder_path, 'exported_tasks.yaml'), 'w') as file:
            file.write("tasks:\n")
            for (index, task) in enumerate(tasks_list):
                file.write(
                    f"- id: {index}\n"
                    f"  task: {task['task']}\n"
                    f"  status: {task['status']}\n"
                )
            console.print(f" [bright_magenta]✔ Successfully generated exported_tasks.yaml")

    if format == 'md':
        with (open(os.path.join(exports_folder_path, 'exported_tasks.md'), 'w')) as file:
            file.write("## Tasks \n")

            for (index, line) in enumerate(tasks):
                file.write(f'- {line}. \n')

            console.print(f" [bright_magenta]✔ Successfully generated exported_tasks.md")


def open_file(exports_folder_path):
    try:
        if os.name == 'posix':
            subprocess.call(['xdg-open', exports_folder_path])
        elif os.name == 'nt':
            os.startfile(exports_folder_path)
        else:
            raise OSError("Unsupported OS. Cannot open file automatically.")
    except FileNotFoundError:
        print(f"Error: The file {exports_folder_path} does not exist.")
    except PermissionError:
        print(
            f"Error: Permission denied when trying to open {exports_folder_path}.")
    except OSError as e:
        print(f"Error: Failed to open file. Details: {e}")
        pass
