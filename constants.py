from InquirerPy.base.control import Choice
from InquirerPy.separator import Separator

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


menu_options = [
    Separator(line=15 * ""),
    Choice(name="📋 Generate TODOs for projects", value=0),
    Choice(name="🗂️  View projects", value=1),
    Choice(name="🔍 View current configuration", value=2),
    Choice(name="🔧 Update configuration", value=3),
    Choice(name="📊 View Reports", value=4),
    Choice(name="🚫 Exit application", value=5),]
