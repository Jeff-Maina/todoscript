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
    with console.status("[bold green]Generating reports...") as status:
        while tasks:
            task = tasks.pop(0)
            time.sleep(1)
            console.log(f"{task} complete")


def export_tasks(folder, tasks, format):
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

    for index,task in enumerate(tasks):
        obj = {
            'id': index,
            'task': task[3:].strip(),
            'status': 'Complete' if task[:3] == '[x]' else "Incomplete"
        }  

        tasks_list.append(obj)

    if format == 'csv':
        with yaspin(text="Generating tasks.csv...", color='light_magenta') as sp:
            with open(os.path.join(exports_folder_path, 'exported_tasks.csv'), 'w') as file:
                file.write("ID,Task,Status\n")
                time.sleep(0.2)
                for index, task in enumerate(tasks):
                    file.write(f"{index+1},{task[3:].strip()},{'completed' if task[:3] == '[x]' else 'pending'}\n")
                
                sp.write(f"Successfully generated tasks.csv")

    if format == 'json':
        with yaspin(text="Generating tasks.json...", color='light_magenta') as sp:
            with open(os.path.join(exports_folder_path, 'exported_tasks.json'), 'w') as file:
                file.write("[\n")
                for index, task in enumerate(tasks_list):
                    if index == len(tasks_list) - 1:
                        file.write(f"{json.dumps(task)}")
                    else:
                        file.write(f"{json.dumps(task)},\n")

                file.write("]\n")
                time.sleep(0.2)
                sp.write(f"Successfully generated tasks.json")

    if format == 'html':
        with yaspin(text="Generating tasks.json...", color='light_magenta') as sp:
            with open(os.path.join(exports_folder_path, 'exported_tasks.html'), 'w') as file:
                file.write(f"<html><body><h1>{folder} tasks</h1><main>\n")
                for index, task in enumerate(tasks_list):
                    file.write(
                        f'<div><input type="checkbox" id="task-{index}" {"checked" if task["status"] == "Complete" else ""}><label for="task-{index}">{task["task"]}</label></div>'
                        )
                file.write("</main></body></html>\n")
                time.sleep(0.2)
                sp.write(f"Successfully generated tasks.html")



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
        print(f"Error: Permission denied when trying to open {exports_folder_path}.")
    except OSError as e:
        print(f"Error: Failed to open file. Details: {e}")
        pass