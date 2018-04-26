import argparse
import os
from subprocess import Popen, PIPE, call
import json
import sys

parser = argparse.ArgumentParser(description='')
parser.add_argument("path", metavar='',nargs='?', default=os.getcwd(), help=argparse.SUPPRESS)
group = parser.add_mutually_exclusive_group()
group.add_argument("-i", "--install", metavar='', nargs='?', const="", required=False, help="Install an extension.")
group.add_argument("-g", "--install-global", metavar='', nargs='?', const="", required=False, help="Install an extension globally and symlink it locally.")
group.add_argument("-u", "--uninstall", metavar='', required=False, help="Uninstall an extension.")
group.add_argument("-l", "--list", action='store_true', help="List installed extensions")
group.add_argument("-r", "--generate-required", action='store_true', help="Set all your local extensions as required.")

args = parser.parse_args()
WORK_DIR = args.path if os.path.isdir(args.path) else os.path.dirname(args.path)
DOT_VSCODE_DIR = WORK_DIR + '/.vscode'
LOCAL_EXTENSIONS_DIR = DOT_VSCODE_DIR + '/extensions'
GLOBAL_EXTENSIONS_DIR = os.path.expanduser("~") + '/.vscode/extensions'

def main():
    install_ext = args.install
    install_ext_global = args.install_global
    uninstall_ext = args.uninstall
    list_ext = args.list
    generate_required = args.generate_required

    # argument --install
    if install_ext is not None:
        local_extensions = get_extensions(LOCAL_EXTENSIONS_DIR)
        if install_ext:
            if install_ext in local_extensions:
                print("Extension '" + install_ext + "' is already installed.")
            else:
                install_local_extension(install_ext)
        else:
            # no param for passed, install everything from extensions.json
            required_extensions = get_required_extensions()
            print("Found %d extensions to install: %s" % (len(required_extensions), *required_extensions))

            for req_ext in required_extensions:
                install_local_extension(req_ext)

    # argument --install-global
    elif install_ext_global is not None:
        if install_ext_global:
            # install extension globally and then symlink it in the workspace
            install_global_extension(install_ext_global)
            install_local_extension(install_local_extension)
        else:
            # no param for passed, install everything from extensions.json globally and then symlink
            required_extensions = get_required_extensions()
            print("Found %d extensions to install: %s" % (len(required_extensions), *required_extensions))

            for req_ext in required_extensions:
                install_global_extension(req_ext)
                install_local_extension(req_ext)

    # argument --uninstall
    elif uninstall_ext:
        # uninstall extension from local workspace
        uninstall_local_extension(uninstall_ext)

    # argument --list
    elif list_ext:
        print_local_extensions()

    # argument --generate-required
    elif generate_required:
        local_extensions = get_extensions(LOCAL_EXTENSIONS_DIR)

        extensions_json = {}
        try:
            extensions_json = json.load(open(DOT_VSCODE_DIR + '/extensions.json'))
        except FileNotFoundError:
            extensions_json = {'recommendations':[]}
        
        required_extensions = []
        try:
            required_extensions = extensions_json['required']
        except KeyError:
            pass
            
        for local_extension in local_extensions:
            ext = local_extension[0]
            if ext not in required_extensions:
                required_extensions.append(ext)
        
        extensions_json['required'] = required_extensions
        with open(DOT_VSCODE_DIR + '/extensions.json', 'w') as extensions_file:
            json.dump(extensions_json, extensions_file, indent=4)

    # no argument
    # install required extensions and open vscode
    else:
        required_extensions = get_required_extensions()
        
        for req_ext in required_extensions:
            install_local_extension(req_ext)

        open_vscode()

# parse .vscode/extensions.json
# if it doesn't exist it's created
def get_required_extensions():
    extensions = []
    try:
        extensions_json = json.load(open(DOT_VSCODE_DIR + '/extensions.json'))
        extensions = extensions_json['required']
    except FileNotFoundError:
        print("File 'extensions.json' not found.")
        '''
        if not os.path.exists(DOT_VSCODE_DIR):
            os.makedirs(DOT_VSCODE_DIR)
        print("File 'extensions.json' not found. Creating it.")
        data = {"recommendations": [], "required": []}
        with open(DOT_VSCODE_DIR + '/extensions.json', 'w') as extensions_file:
            json.dump(data, extensions_file, indent=4)
        '''
        return extensions
    except KeyError:
        # required is not a key in extensions.json
        print("No required extensions in 'extensions.json'.")
        pass
    finally:
        return extensions

def remove_extension_from_dot_obsolete_json(extension):
    try:
        obsolete_json = json.load(open(LOCAL_EXTENSIONS_DIR + '/.obsolete'))
        obsolete_extensions = obsolete_json.keys()
        data = {}
        for obsolete_extension in obsolete_extensions:
            if not obsolete_extension.startswith(obsolete_extension):
                data[obsolete_extension] = True

        with open(LOCAL_EXTENSIONS_DIR + '/.obsolete', 'w') as dot_obsolete:
            json.dump(data, dot_obsolete, indent=4)

    except FileNotFoundError:
        pass
    except KeyError:
        pass

def install_local_extension(extension):
    remove_extension_from_dot_obsolete_json(extension)
    
    global_extensions = get_extensions(GLOBAL_EXTENSIONS_DIR)
    for g_ext in global_extensions:
        if extension == g_ext[0]:
            try:
                ext_fullname = g_ext[0] + "-" + g_ext[1]
                os.symlink(GLOBAL_EXTENSIONS_DIR + "/" + ext_fullname,
                        LOCAL_EXTENSIONS_DIR + "/" + ext_fullname)
                print("Found extension in '~/.vscode/extensions'. Created symlink.")
            except FileExistsError:
                pass
            break
    else:
        command = "code --extensions-dir " + LOCAL_EXTENSIONS_DIR + " --install-extension " + extension
        execute_command(command)

def install_global_extension(extension):
    command = "code --install-extension " + extension
    execute_command(command)

def uninstall_local_extension(extension):
    command = "code --extensions-dir " + LOCAL_EXTENSIONS_DIR + " --uninstall-extension " + extension
    execute_command(command)

def open_vscode():
    command = "code " + WORK_DIR + " --extensions-dir " + LOCAL_EXTENSIONS_DIR
    execute_command(command)

def print_local_extensions():
    local_extensions = get_extensions(LOCAL_EXTENSIONS_DIR)
    for ext_name, ext_ver in local_extensions:
        print(ext_name + ":" + ext_ver)

def get_extensions(path):
    '''
    Find all vscode extensions in a folder.
    The extensions are return as a list of pairs (name, version)
    '''
    extensions = []
    candidates_ext = os.listdir(path)
    for candidate in candidates_ext:
        candidate_path = path + "/" + candidate
        if os.path.isdir(candidate_path):
            candidates_ext = os.listdir(candidate_path)
            if 'package.json' in candidates_ext:
                last_dash = candidate.rfind('-')
                ext = candidate[:last_dash]
                ver = candidate[last_dash+1:]
                extensions.append( (ext, ver) )
    return extensions

def execute_command(command, return_out=False):
    '''
    Execute a shell command. If return_out is False the stdout and stderr are redirected
    to terminal, if return_out is True the output is returned after completion.
    '''
    if return_out:
        proc = Popen(command.split(), stdout=PIPE, stderr=PIPE)
        out, err = proc.communicate()
        return out
    else:
        proc = Popen(command.split(), stdout=sys.stdout, stderr=sys.stderr)
        proc.wait()
        return ""

def run_with_time(fun):
    import time
    start_time = time.time()
    fun()
    end_time = time.time()
    d_time = end_time-start_time
    print("Time: {:.{prec}f} ms".format(d_time*1000, prec=4))

if __name__ == "__main__":
    #run_with_time(main)
    main()