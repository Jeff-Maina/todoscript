from InquirerPy import inquirer, prompt, get_style
from InquirerPy.validator import NumberValidator
from rich.table import Table
from rich.console import Console
from rich.prompt import Prompt
import time
from yaspin import yaspin
from InquirerPy.validator import PathValidator

import os

from main import configure
from utils import has_been_configured,clear_terminal

custom_syles = get_style(
    {
        "questionmark": "#EB5B00 bold",
        "answermark": "#e5c07b",
        "answer": "#61afef",
        "input": "#98c379",
        "question": "",
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

file_formats = [{
    "name": "Markdown (.md)",
    "value": "md"
}, {
    "name": "JSON (.json)",
    "value": "json"
}, {
    "name": "CSV (.csv)",
    "value": "csv"
}, {
    "name": "YAML (.yaml)",
    "value": "yaml"
}, {
    "name": "Plain Text (.txt)",
    "value": "txt"
}]

themes = [{
    "name": "Vesper",
    "value": "vesper"
}, {
    "name": "Dracula",
    "value": "dracula"
}, {
    "name": "Monokai",
    "value": "monokai"
}]


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

    print("")
    console.print("[#e5c07b] Configurations summary:")
    print("")
    console.print(f"- Projects location: [#61afef bold] {root_folder}")
    console.print(f"- TODOs folder name: [#61afef bold] {parent_folder_name}")
    console.print(f"- File format: [#61afef bold] {file_format}")
    console.print(f"- Theme: [#61afef bold] {theme}")

    print(" ")
    confirm = inquirer.confirm(
        message="Save configuration?", default=True).execute()
    print(" ")

    if confirm:
        config = {
            'root_folder': root_folder, 'parent_folder_name': parent_folder_name, 'file_format': file_format, 'theme': theme
        }

        configure(config)

        print(" ")

        main_menu_confirmation = inquirer.confirm(
            message="Proceed to main menu?", default=True).execute()

        if main_menu_confirmation:
            main_menu()

    else:
        console.print(
            "[red bold] Configuration not saved. Exiting the setup process.")


def main_menu():
    clear_terminal()

    print(" ")
    console.print("[red bold] main menu")
    print(" ")
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


def main():
    if has_been_configured():
        main_menu()
    else:
        set_configuration()


if __name__ == "__main__":
    main()
