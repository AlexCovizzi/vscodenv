import argparse
import os
from .vscode_extensions import *
from .extensions_json import *
from .vscode_cli import code_open

parser = argparse.ArgumentParser(description='', add_help=False)
parser.add_argument("path", metavar='',nargs='?', default=os.getcwd(), help=argparse.SUPPRESS)
group = parser.add_mutually_exclusive_group()
group.add_argument("-i", "--install", metavar='', nargs='?', const="", required=False)
# group.add_argument("-g", "--install-global", metavar='', nargs='?', const="", required=False, help="Install an extension globally and symlink it locally.")
group.add_argument("-u", "--uninstall", metavar='', required=False)
group.add_argument("-l", "--list", action='store_true')
group.add_argument("-h", "--help", action='store_true')
# group.add_argument("-r", "--generate-required", action='store_true', help="Set all your local extensions as required.")

def main():
    args = parser.parse_args()

    work_dir = args.path if os.path.isdir(args.path) else os.path.dirname(args.path)
    dot_vscode_dir = os.path.join(work_dir, '.vscode')
    extensions_dir = os.path.join(dot_vscode_dir, 'extensions')

    install_ext = args.install
    uninstall_ext = args.uninstall
    list_ext = args.list
    show_help = args.help

    if install_ext is not None:
        install(install_ext, extensions_dir)
    elif uninstall_ext is not None:
        uninstall(uninstall_ext, extensions_dir)
    elif list_ext:
        list_extensions(extensions_dir)
    elif show_help:
        print_help()
    else:
        code_open(extensions_dir)


# --install
def install(extension, extensions_dir):
    local_extensions = get_extensions(extensions_dir)
    if extension:
        if extension in local_extensions:
            print("Extension '" + extension + "' is already installed.")
        else:
            install_extension(extension, extensions_dir)
    else:
        # no param passed, install everything from extensions.json
        extensions_json_path = extensions_dir + ".json"
        required_extensions = get_required_extensions(extensions_json_path)
        # print("Found %d extensions to install: %s" % (len(required_extensions), *required_extensions))

        for required_ext in required_extensions:
            install_extension(required_ext, extensions_dir)

# --unistall
def uninstall(extension, extensions_dir):
    uninstall_extension(extension, extensions_dir)


# --list
def list_extensions(extensions_dir):
    extensions = get_extensions(extensions_dir)
    for extension in extensions:
        print(extension)

# --help
# because argparse help message is formatted ugly
def print_help():
    help_file_path = os.path.join(os.path.dirname(__file__), "help.txt")
    with open(help_file_path, 'r') as help_file:
        print(help_file.read())