import argparse
import os
from .vscode_extensions import *
from .extensions_json import *
from .vscode_cli import code_open
from .utils import extension_base_name

parser = argparse.ArgumentParser(add_help=False)
parser.add_argument("path", nargs='?', default=os.getcwd())
group = parser.add_mutually_exclusive_group()
group.add_argument("-i", "--install", nargs='?', const="")
group.add_argument("-u", "--uninstall")
group.add_argument("-l", "--list", action='store_true')
group.add_argument("-r", "--generate-required", action='store_true')
group.add_argument("-h", "--help", action='store_true')


def main():
    args = parser.parse_args()

    path = args.path
    work_dir = path if os.path.isdir(path) else os.path.dirname(path)
    dot_vscode_dir = os.path.join(work_dir, '.vscode')
    extensions_dir = os.path.join(dot_vscode_dir, 'extensions')

    install_ext = args.install
    uninstall_ext = args.uninstall
    list_ext = args.list
    gen_required = args.generate_required
    show_help = args.help

    if install_ext is not None:
        install(install_ext, extensions_dir)
    elif uninstall_ext is not None:
        uninstall(uninstall_ext, extensions_dir)
    elif list_ext:
        list_extensions(extensions_dir)
    elif gen_required:
        generate_required(extensions_dir)
    elif show_help:
        print_help()
    else:
        print("Current working directory: %s" % work_dir)
        install_required(extensions_dir)
        print("Launching Visual Studio Code...")
        code_open(path, extensions_dir)


# --install
def install(extension, extensions_dir):
    local_extensions = get_extensions(extensions_dir)
    if extension:
        if extension in local_extensions:
            print("Extension '" + extension + "' is already installed.")
        else:
            install_extension(extension, extensions_dir)
    else:
        # no param passed, install required from extensions.json
        install_required(extensions_dir)


# --unistall
def uninstall(extension, extensions_dir):
    uninstall_extension(extension, extensions_dir)


# --list
def list_extensions(extensions_dir):
    extensions = get_extensions(extensions_dir)
    for extension in extensions:
        base_name = extension_base_name(extension)
        print(base_name)


# --generate-required
def generate_required(extensions_dir):
    extensions = get_extensions(extensions_dir)
    # keep only base name
    extensions = [extension_base_name(ext) for ext in extensions]
    extensions_json_path = os.path.join(os.path.dirname(extensions_dir), "extensions.json")
    extend_required_extensions(extensions_json_path, extensions)


# --help
# because argparse help message is formatted ugly
def print_help():
    help_file_path = os.path.join(os.path.dirname(__file__), "help.txt")
    try:
        with open(help_file_path, 'r') as help_file:
            print(help_file.read())
    except IOError:
        try:
            ans = input("Did you remove 'help.txt' ?? [y/n]: ")
            if ans == 'y':
                print("https://i.imgur.com/Br00TCn.gif")
        except KeyboardInterrupt:
            print("iao!")


def install_required(extensions_dir):
    '''
    Install required extension (found in extensions.json)
    '''
    extensions_json_path = extensions_dir + ".json"
    required_extensions = get_required_extensions(extensions_json_path)
    installed_extensions = get_extensions(extensions_dir)
    # keep only base name (remove version) from installed extensions
    installed_extensions = [extension_base_name(ext) for ext in installed_extensions]

    # install only required extensions that are not already installed
    extensions_to_install = list(set(required_extensions) - set(installed_extensions))

    if extensions_to_install:
        print("Found %d extensions to install: %s" % (
            len(extensions_to_install),
            *extensions_to_install))
    else:
        print("No extension to install.")

    for required_ext in required_extensions:
        install_extension(required_ext, extensions_dir)
