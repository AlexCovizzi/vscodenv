'''
Some methods used in different modules
'''
from os import environ, path, listdir, getcwd


def get_global_extensions_dir():
    '''
    Get the global directory to store vscode extensions, by default it's ~/.vscode/extension.
    '''
    default_global_extensions_dir = path.join(path.expanduser("~"), '.vscode', 'extensions')
    # global_extensions_dir = environ.get('VSCODE_EXTENSIONS', default_global_extensions_dir)
    return default_global_extensions_dir

def extension_base_name(extension):
    '''
    Get the extension base name, that is the full name of the extension
    (e.g. ms-python.python-2018.3.1) without the version (e.g. ms-python.python).
    '''
    last_dot = extension.rfind('.')
    n = extension[last_dot+1:]
    if n.isdigit():
        last_dash = extension.rfind('-')
        base_name = extension[:last_dash]
        # version = extension[last_dash+1:]
        return base_name
    else:
        return extension


def get_work_dir(file_path):
    '''
    Find the first .vsocde directory going up the directory tree.
    If none is found the global .vscode directory is used (usually ~/.vscode).
    This is used when opening a single file so that the correct extensions are loaded.
    '''
    file_path = path.join(getcwd(), file_path)
    if path.isdir(file_path):
        return file_path
    else:
        return _find_dir_with_dot_vscode(file_path)

def _find_dir_with_dot_vscode(file_path, up_limit=10):
    if up_limit == 0:
        return get_global_extensions_dir()
    up_dir = path.dirname(file_path)
    files_in_dir = listdir(up_dir)
    if '.vscode' in files_in_dir:
        return up_dir
    else:
        lim = up_limit-1
        return _find_dir_with_dot_vscode(up_dir, up_limit=lim)
