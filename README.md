# vscodenv

Project-level extensions for Visual Studio Code.

## How it works

This command line tool leverages the VSCode CLI to manage your extensions on a project level.

You can open Visual Studio Code from the console using the command `vscode`, the workspace is then opened loading only the extensions found in that workspace's `.vscode/extensions`.

When you open a workspace this way every required extension in `.vscode/extensions.json` is installed for that workspace.

To install an extension in your workspace you can run the command `vscode -i <extension-id>` or, after launching Visual Studio Code with the command `vscode`, you can install an extension from the marketplace like you normally do.  
**Note**: using the command `vscode -i <extension-id>`, if the extension is found in `~/.vscode/extensions`, the extension will not be downloaded but symlinked.

Finally you can set all the extensions installed in your workspace as required (in `.vscode/extensions.json`) using the command `vscode --generate-required`.


## Installation

1. Clone vscodenv into `~/.vscodenv`.

    ~~~ sh
    $ git clone https://github.com/AlexCovizzi/vscodenv.git ~/.vscodenv
    ~~~

2. Add `~/.vscodenv/bin` to your `$PATH` for access to the `vscode`
   command-line utility.

    ~~~ sh
    $ echo 'export PATH="$HOME/.vscodenv:$PATH"' >> ~/.bash_profile
    ~~~

    **Ubuntu note**: Modify your `~/.bashrc` instead of `~/.bash_profile`.

    **Zsh note**: Modify your `~/.zshrc` file instead of `~/.bash_profile`.

3. Restart your shell so that PATH changes take effect. (Opening a new
   terminal tab will usually do it.)

### Upgrading

You can upgrade vscodenv to the
latest version by pulling from GitHub:

~~~ sh
$ cd ~/.vscodenv
$ git pull
~~~