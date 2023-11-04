# ArcaneOS Backend Server

## About

this is the backend server which powers user and session management,
filesystem and messaging (and prob more later) for [ArcaneOS' frontend](https://github.com/shakyevan444/ArcaneOS)

## Getting Started
Before you continue, make sure you install the system prerequisites:
- [Git](https://git-scm.com/)
- [Python](https://www.python.org/) 3.11 or higher
- [Rust](https://rust-lang.org/) Toolchain (can be installed via [`rustup`](https://rustup.rs/))

Once the prerequisites are met, you can execute the following commands to **clone the API**, **Install dependencies** and **run it for the first time**:
```bash
$ git clone https://github.com/shakyevan444/ArcaneOS-API  # Clone repository
$ cd ArcaneOS-API/

$ python -m venv venv # Create virtual enviorment for ArcaneAPI
$ py -m venv venv  # Create virtual enviroment for ArcaneAPI (Windows only)

# Activate virtual enviroment (you will need to do this each time when launching ArcAPI)
# If on *nix:
$ source venv/bin/activate
# If on windows (cmd, on powershell replace `.bat` with `.ps1`):
$ venv/Scripts/activate.bat

$ pip install -r requirements.txt  # Satisfy dependencies

$ python3 ./main.py # Start the API

$ deactivate  # Deactivate virtual enviroment
```

When running the API for the first time, a configuration file will be created called `config.yaml`, in which you can personalize your ArcAPI instance.

## Launch

to launch you can just do:
- linux: `./main.py` (assuming file permissions are transferred, otherwise
first do `chmod +x main.py`)
- windows: `py main.py`

## Configuration

default config wil be created right after the first launch and placed in
`config.yaml` file
