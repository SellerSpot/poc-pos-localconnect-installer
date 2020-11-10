import subprocess
from colorit import *


def check_mongodb():  # used to check if mongodb has been installed
    mongoCheck = subprocess.Popen(
        "mongodd --version", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
    mongoCheck_status = mongoCheck.wait()
    return (mongoCheck_status == 0)


def printMessage(message, type):
    if (type == "success"):
        print(color("√", Colors.green), end=" ")
        print(message)
    elif (type == "failure"):
        print(color("X", Colors.red), end=" ")
        print(message)
    elif (type == "info"):
        print(color("!", Colors.blue), end=" ")
        print(message)


if __name__ == "__main__":
    init_colorit()
    # checking mongodb existance
    if check_mongodb():
        printMessage("MongoDB Exists", "success")

    else:
        printMessage("Should install MondoDB", "failure")
