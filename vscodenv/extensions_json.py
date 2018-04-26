import json

def get_required_extensions(extensions_json_path):
    '''
    Find required extensions in extensions.json.
    '''
    required_extensions = _parse_json(extensions_json_path, 'required')
    return required_extensions

def get_recommended_extensions(extensions_json_path):
    '''
    Find recommended extensions in extensions.json.
    '''
    recommended_extensions = _parse_json(extensions_json_path, 'recommendations')
    return recommended_extensions

def extend_required_extensions(extensions_json_path, extensions):
    '''
    Add extensions to the required extensions.
    '''
    _extend_list_json(extensions_json_path, "required", extensions)

def extend_recommended_extensions(extensions_json_path, extensions):
    '''
    Add extensions to the recommended extensions.
    '''
    _extend_list_json(extensions_json_path, "recommended", extensions)

def _extend_list_json(path_json, list_key, values):
    try:
        with open(path_json, 'r+') as file_json:
            data = {}
            try:
                data = json.load(file_json)
            except json.decoder.JSONDecodeError:
                pass
            
            file_json.seek(0)
            
            f_values = []
            try:
                f_values = data[list_key]
            except KeyError:
                pass

            for value in values:
                if value not in f_values:
                    f_values.append(value)

            data[list_key] = f_values
            json.dump(data, file_json, indent=4)

            file_json.truncate()
    except IOError:
        pass

def _parse_json(path_json, key):
    values = []
    try:
        file_json = json.load(open(path_json))
        values = file_json[key]
    except IOError:
        pass
    except KeyError:
        pass
    finally:
        return values
