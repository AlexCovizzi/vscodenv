'''
Python interface for vscode cli
'''
from subprocess import Popen, PIPE
from sys import stdout, stderr

def code_install(extension, extensions_dir):
    err = _code_execute("--extensions-dir", extensions_dir, "--install-extension", extension)
    print(err)

def code_uninstall(extension, extensions_dir):
    err = _code_execute("--extensions-dir", extensions_dir, "--uninstall-extension", extension)
    print(err)

def code_open(path, extensions_dir):
    _code_execute(path, "--extensions-dir", extensions_dir)

def _code_execute(*args):
    command = list(args)
    command.insert(0, "code")
    proc = Popen(command, stdout=stdout, stderr=PIPE, universal_newlines=True)
    _,err = proc.communicate()
    return err.rstrip("\n")