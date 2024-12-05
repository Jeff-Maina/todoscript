import os.path
import json
from rich.console  import Console
import webbrowser

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



  


def generate_reports(reports_data,table,formats):
    console.print(table)

    print(reports_data)

    for format in formats:
        if format == 'html':
            html_file = 'reports_table.html'

            html = console.export_html(clear=False)

            with open(html_file,'w') as file:
                file.write(html)

        if format == 'svg':
            svg_file = 'reports_table.svg'

            svg = console.export_svg(clear=False)

            with open(svg_file,'w') as file:
                file.write(svg)
        
        if format == 'csv':
            
            cols = 'Index,Folder,Completed,Pending,Total'

            with open("reports.csv", 'w') as file:
                file.write(f"{cols}\n")
                for data in reports_data:
                    file.write(f"{data['id']},{data['folder']},{data['completed']},{data['pending']},{data['total']}\n")

        if format == 'json':
            json_obj = {}
            with open('reports.json', 'w') as file:
                file.write("[\n")
                for index,data in enumerate(reports_data):
                    if index == len(reports_data) - 1:
                        file.write(f"{json.dumps(data)}\n")
                    else:
                        file.write(f"{json.dumps(data)},\n")
                file.write("]\n")
            


