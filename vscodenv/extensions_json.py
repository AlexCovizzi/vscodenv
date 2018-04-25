import json

def get_required_extensions(dot_vscode_path):
    '''
    Find required extensions in .vscode/extensions.json.
    '''
    required_extensions = _parse_json(dot_vscode_path + '/extensions.json', 'required')
    return required_extensions

def get_recommended_extensions(dot_vscode_path):
    '''
    Find recommended extensions in .vscode/extensions.json.
    '''
    recommended_extensions = _parse_json(dot_vscode_path + '/extensions.json', 'recommendations')
    return recommended_extensions

def extend_required_extensions(dot_vscode_path, extensions):
    '''
    Add extensions to the required extensions.
    '''
    pass

def extend_recommended_extensions(dot_vscode_path, extensions):
    '''
    Add extensions to the recommended extensions.
    '''
    pass

def _parse_json(path_json, key):
    values = []
    try:
        file_json = json.load(open(path_json))
        values = file_json[key]
    except FileNotFoundError:
        pass
    except KeyError:
        pass
    finally:
        return values