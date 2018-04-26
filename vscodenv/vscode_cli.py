'''
Python interface for vscode cli
'''
from subprocess import Popen, PIPE
from sys import stdout, stderr

def code_install(extension, extensions_dir):
    _code_execute("--extensions-dir", extensions_dir, "--install-extension", extension)

def code_uninstall(extension, extensions_dir):
    _code_execute("--extensions-dir", extensions_dir, "--uninstall-extension", extension)

def code_open(extensions_dir):
    _code_execute("--extensions-dir", extensions_dir)

def _code_execute(*args):
    command = list(args)
    command.insert(0, "code")
    proc = Popen(command, stdout=stdout, stderr=PIPE, universal_newlines=True)
    _,err = proc.communicate()
    return err