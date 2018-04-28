# vscodenv

Project-level extensions for Visual Studio Code.

## How it works

#

## Installation

1. Clone vscodenv into `~/.vscodenv`.

    ~~~ sh
    $ git clone https://github.com/AlexCovizzi/vscodenv.git ~/.vscodenv
    ~~~

2. Add `~/.vscodenv/bin` to your `$PATH` for access to the `vscode`
   command-line utility.

    ~~~ sh
    $ echo 'export PATH="$HOME/.vscodenv/bin:$PATH"' >> ~/.bash_profile
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