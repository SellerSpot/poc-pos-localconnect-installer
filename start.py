import subprocess
from colorit import color, init_colorit, Colors
import os
import wget
from pathlib import Path
import requests
import time


# COMMON--------------------------------------------------------------------------------------------


def print_message(message, type, prefix, end="\n"):  # used to print messages to console
    print(prefix, end=" ")
    if (type == "success"):
        print(color("√", Colors.green), end=" ")
    elif (type == "failure"):
        print(color("X", Colors.red), end=" ")
    elif (type == "info"):
        print(color("!", Colors.blue), end=" ")
    print(message, end=end)


# MONGODB INSTALLATION--------------------------------------------------------------------------------------------

def check_mongodb():  # used to check if mongodb has been installed
    mongoCheck = subprocess.Popen(
        "mongod --version", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
    mongoCheck_status = mongoCheck.wait()
    return (mongoCheck_status == 0)


def check_mongodb_installer():  # used to check if mongodb installer is already downloaded
    for file in os.listdir(os.curdir):
        if (file.startswith("mongodb-windows") and file.endswith(".msi")):
            return file
    return False


def invoke_downloaded_mongodbinstaller():  # used to invoke the local mongodb installer
    print_message(
        "Opening downloaded MongoDB installer...", "info", "  -")
    subprocess.call(f'msiexec /i {check_mongodb_installer()}', shell=True)
    initiateMongoDbChecks()


def download_mongodbinstaller():  # used to download mongodb installer
    print_message("Initiating download of Mongo DB...", "info", "  -")
    wget.download(
        'https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-4.4.1-signed.msi')


def initiateMongoDbChecks():  # used to initiate and handle mongodb installation checks

    if check_mongodb():  # checking mongodb existance
        print_message("Mongo DB Exists", "success", "")

    else:
        print_message("Mongo DB not installed", "failure", "")

        if check_mongodb_installer():  # checking if mongodb is already downloaded
            invoke_downloaded_mongodbinstaller()

        else:
            download_mongodbinstaller()
            invoke_downloaded_mongodbinstaller()


# SERVER INSTALLATION--------------------------------------------------------------------------------------------

# custom download progress bar for wget
def bar_custom_local_server(current, total, width=80):
    if current == total:
        print_message(
            "Downloading latest server version: %d%%" % (
                current / total * 100), "info", "  -", "\n")
    else:
        print_message(
            "Downloading latest server version: %d%%" % (
                current / total * 100), "info", "  -", "\r")


def delete_server_instance(pathStr):  # used to delete the local copy of server
    print_message("Deleting local server instance", "info", "  -")
    subprocess.Popen(
        "del sellerspotserver.exe", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)


def stop_server():  # used to stop execution of any running server instances
    print_message("Stopping running server instance", "info", "  -")
    subprocess.Popen(
        "taskkill /f /im sellerspotserver.exe", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)


def get_latest_server(pathStr):  # used to get the latest version of local server
    wget.download(
        'https://sellerspotdev.s3.ap-south-1.amazonaws.com/sellerspotserver.exe', pathStr, bar=bar_custom_local_server)


def initiate_server(pathStr):  # used to initiate the latest downloaded server
    print_message(
        "Initialising local server instance...", "info", "  -")
    subprocess.Popen(
        "sellerspotserver.exe", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)


def check_local_server_status():  # used to check the status of local server
    try:
        response = requests.head('http://localhost:40040')
        if response.status_code == 200:
            print_message(
                "Local server up and running", "success", "  -")
        else:
            print_message(
                "Local server initialisation failed - please contact developers", "failure", "  -")
    except requests.exceptions.ConnectionError as e:
        print_message(
            "Local server initialisation failed - please contact developers", "failure", "  -")


def initiateLocalServerChecks():  # used to initiate and handle installation of local server
    print_message("Local server check", "success", "")
    # path to store the local server in
    pathStr = str(Path.home()) + \
        "\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
    os.chdir(pathStr)
    # stopping running servers
    stop_server()
    time.sleep(1)
    # deleting local server instance
    delete_server_instance(pathStr)
    # dowloading latest version of localconnect server
    get_latest_server(pathStr)
    # initializing local server instance
    initiate_server(pathStr)
    # waiting for server to initialize
    time.sleep(5)
    # check if local server is up and running
    check_local_server_status()


# MAIN FUNCTION--------------------------------------------------------------------------------------------
if __name__ == "__main__":

    # clearing output and initializing text color engine
    init_colorit()

    # initialising mongoDb checks
    initiateMongoDbChecks()

    # initialising localServer checks
    initiateLocalServerChecks()
