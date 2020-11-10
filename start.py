import subprocess
from colorit import color, init_colorit, Colors
import os
import wget

# COMMON--------------------------------------------------------------------------------------------


def print_message(message, type, prefix):  # used to print messages to console
    print(prefix, end=" ")
    if (type == "success"):
        print(color("√", Colors.green), end=" ")
    elif (type == "failure"):
        print(color("X", Colors.red), end=" ")
    elif (type == "info"):
        print(color("!", Colors.blue), end=" ")
    print(message)


# MONGODB INSTALLATION--------------------------------------------------------------------------------------------

def check_mongodb():  # used to check if mongodb has been installed
    mongoCheck = subprocess.Popen(
        "mongodd --version", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
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


# MAIN FUNCTION--------------------------------------------------------------------------------------------


if __name__ == "__main__":

    # clearing output and initializing text color engine
    init_colorit()

    # initialising mongoDb checks
    initiateMongoDbChecks()
