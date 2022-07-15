# mm-language-server

A [Language Server](https://microsoft.github.io/language-server-protocol/) for the config files of OpenMMLab
based on [Jedi](https://jedi.readthedocs.io/en/latest/). The Neovim/Vim and VS code plugin are planned.
Supports Python versions 3.7 and newer.

**Note:** This project is forked from [jedi-language-server](https://github.com/pappasam/jedi-language-server), thanks!

**WARN:** This project is still working in progress, I don't suggest you using it unless you want to join
development.

## Installation

Before the Neovim/Vim and VS code plugins are implemented, you may have to set up it manually.

```bash
pip install .
```

## Capabilities

Since mm-language-server is based on jedi-language-server and Jedi, it supports most language features of
Python. Besides it, it implements some extra functionalilies for OpenMMLab config files.

### Code Jump

- Go from the inherited configuration item to the base configuration item.

- Go from the `type` field to the implementation in the source code.

### Hover document

- Display the entire dict of the configuration item.

- Preview the class docstring from the `type` field.

## Editor Setup

The following instructions show how to use mm-language-server with your development tooling. The instructions assume you have already installed mm-language-server.

### Vim / Neovim

The maintainer is using [coc.nvim](https://github.com/neoclide/coc.nvim) as the LSP client provider. Other LSP
client provider may also availiable.

### Visual Studio Code (not implemented)

## Command line

mm-language-server can be run directly from the command line.

```console
$ mm-language-server --help
usage: mm-language-server [-h] [--version] [--tcp] [--ws] [--host HOST] [--port PORT] [--log-file LOG_FILE] [-v]

OpenMMLab language server: an LSP server for configuration file of OpenMMLab.

optional arguments:
  -h, --help           show this help message and exit
  --version            display version information and exit
  --tcp                use TCP web server instead of stdio
  --ws                 use web socket server instead of stdio
  --host HOST          host for web server (default 127.0.0.1)
  --port PORT          port for web server (default 2087)
  --log-file LOG_FILE  redirect logs to file specified
  -v, --verbose        increase verbosity of log output

Examples:

    Run over stdio     : mm-language-server
    Run over tcp       : mm-language-server --tcp
    Run over websockets:
        # only need to pip install once per env
        pip install pygls[ws]
        mm-language-server --ws

Notes:

    For use with web sockets, user must first run
    'pip install pygls[ws]' to install the correct
    version of the websockets library.
```

## Configuration (TODO)


## Local Development

To build and run this project from source:

### Dependencies

Install the following tools manually:

- [Poetry](https://github.com/sdispater/poetry#installation)
- [GNU Make](https://www.gnu.org/software/make/)

#### Recommended

- [asdf](https://github.com/asdf-vm/asdf)

### Get source code

[Fork](https://help.github.com/en/github/getting-started-with-github/fork-a-repo) this repository and clone the fork to your development machine:

```bash
git clone https://github.com/<YOUR-USERNAME>/mm-language-server
cd mm-language-server
```

### Set up development environment

```bash
make setup
```

### Run tests

```bash
make test
```
