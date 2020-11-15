# POS LocalConnect Installer

Python based installer for Sellerspot LocalConnect

## Tasks Performed:

- Creates **directory** for Sellerspot in the user folder `c:\Users\<username>\Sellerspot`.
- Creates **config file** for an isolated mongodb instance.
- Verifies if mongodb is installed:
  - If installed, it will use the config file to invoke the isolated database instance with the **data store** and **logger** directed to `c:\Users\<username>\Sellerspot\store` and `c:\Users\<username>\Sellerspot\log`.
  - If not installed, the **official MongoDB installer** will be downloaded and invoked, and after installation, it will rerun this step.
- Downloads and invokes the **LocalConnect Server** into `c:\Users\<username>\Sellerspot\Server`.
- Downloads the **startup script** and adds it to the user's startup schedule.

## Setup and execution:

### Installer

- To run python script
  `python run installer.py`

- To create executable
  `pyinstaller --onefile installer.py`

### Startup Script

- To run python script
  `python run sellerspotServerInvoke.py`

- To create executable
  `pyinstaller --onefile sellerspotServerInvoke.py`

## Progress Log

- [x] Installation of local database, server and startup script.
- [x] Creation of isolated database server.
- [ ] Get installer certified by windows to prevent virus flags.
- [ ] Add window UI to installer progress view.
