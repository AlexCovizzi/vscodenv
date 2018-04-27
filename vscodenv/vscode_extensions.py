'''
Module to search, install, uninstall vscode extensions
'''
import os
from . import vscode_cli
from .utils import get_global_extensions_dir, extension_base_name
import json


def install_extension(extension, extensions_dir):
    global_extensions_dir = get_global_extensions_dir()
    installed_extension = is_extension_installed(extension, global_extensions_dir)
    if installed_extension:
        installed_extension_path = os.path.join(global_extensions_dir, installed_extension)
        local_extension_path = os.path.join(extensions_dir, installed_extension)
        try:
            os.symlink(installed_extension_path, local_extension_path)
        except IOError:
            pass
    else:
        vscode_cli.code_install(extension, extensions_dir)

def uninstall_extension(extension, extensions_dir):
    vscode_cli.code_uninstall(extension, extensions_dir)

def is_extension_installed(extension, extensions_dir):
    '''
    Check if the extension is already in the directory specified.
    If it is the full name of the extension (name-version) is returned otherwise None is returned.
    '''
    if not extensions_dir:
        extensions_dir = get_global_extensions_dir()
    installed_extensions = get_extensions(extensions_dir)
    for installed_extension in installed_extensions:
        if installed_extension.startswith(extension):
            return installed_extension
    return None

def get_extensions(extensions_dir):
    '''
    Find all vscode extensions in a folder.
    The extensions are returned as a list of strings formatted as:
    [extension name]-[extension version]
    '''
    extensions = []
    candidate_extensions = []
    try:
        candidate_extensions = os.listdir(extensions_dir)
    except IOError:
        pass
    
    obsolete_extensions = parse_dot_obsolete(extensions_dir)
    for candidate in candidate_extensions:
        candidate_path = os.path.join(extensions_dir, candidate)
        # an extension MUST be a directory
        if os.path.isdir(candidate_path):
            # an extension MUST have a 'package.json' file
            package_json_path = os.path.join(candidate_path, 'package.json')
            package_json_exists = os.path.exists(package_json_path)
            # an extension must not be in .obsolete file
            extension_in_dot_obsolete = (candidate in obsolete_extensions)
            if package_json_exists and not extension_in_dot_obsolete:
                extensions.append(candidate)
    return extensions

def parse_dot_obsolete(extensions_dir):
    dot_obsolete_path = os.path.join(extensions_dir, '.obsolete')
    obsolete_extensions = []
    if os.path.exists(dot_obsolete_path):
        try:
            data = json.load(open(dot_obsolete_path))
            obsolete_extensions = list(data.keys())
        except IOError:
            pass
        except json.JSONDecodeError:
            pass

    return obsolete_extensions