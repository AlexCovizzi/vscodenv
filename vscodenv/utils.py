'''
Some methods used in different modules
'''
from os import environ, path


def get_global_extensions_dir():
    '''
    Get the global directory to store vscode extensions, by default it's ~/.vscode/extension
    '''
    default_global_extensions_dir = path.join(path.expanduser("~"), '.vscode', 'extensions')
    global_extensions_dir = environ.get('VSCODE_EXTENSIONS', default_global_extensions_dir)
    return global_extensions_dir

def extension_base_name(extension):
    last_dot = extension.rfind('.')
    n = extension[last_dot+1:]
    if n.isdigit():
        last_dash = extension.rfind('-')
        base_name = extension[:last_dash]
        # version = extension[last_dash+1:]
        return base_name
    else:
        return extension