import subprocess
from colorit import color, init_colorit, Colors
import os
import wget
from pathlib import Path
import requests
import time
import ctypes
import sys
import pymongo
import winapps
import csv
import codecs


# COMMON--------------------------------------------------------------------------------------------

# download urls
localServerURL = "https://sellerspotdev.s3.ap-south-1.amazonaws.com/LocalConnectServer.exe?versionId=vcIhPcMi_yqP9_XYZbh8N9iLLMr4hEV7"
localServerInvokeScriptURL = "https://sellerspotdev.s3.ap-south-1.amazonaws.com/sellerspotServerInvoke.exe?versionId=OSQU50Q2JI1eXGtj9wHjy.VPZWetyKT5"
mongoDBURL = "https://fastdl.mongodb.org/windows/mongodb-windows-x86_64-4.4.1-signed.msi"
mongoDBConfigURL = "https://sellerspotdev.s3.ap-south-1.amazonaws.com/mongoconfig.cgf?versionId=zTlArQUWldwQGKSZuC399GIY7lKTLOJo"

# file paths
applicationFolderPath = str(Path.home())+"\SellerSpot"
startupFolderPath = str(Path.home()) + \
    "\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup"
mongoDBRootPath = r"C:\Program Files\MongoDB\Server"


def print_message(message, type, prefix, end="\n"):  # used to print messages to console
    print(prefix, end=" ")
    if (type == "success"):
        print(color("√", Colors.green), end=" ")
    elif (type == "failure"):
        print(color("X", Colors.red), end=" ")
    elif (type == "info"):
        print(color("!", Colors.blue), end=" ")
    print(message, end=end)


def create_application_folder():  # used to create the application folder in Program Files
    if not os.path.isdir(applicationFolderPath):
        os.mkdir(applicationFolderPath)


# MONGODB INSTALLATION--------------------------------------------------------------------------------------------


# custom download progress bar for wget
def bar_custom_mongodb(current, total, width=80):
    if current == total:
        print_message(
            "Downloading Mongo DB: %d%%" % (
                current / total * 100), "info", "  -", "\n")
    else:
        print_message(
            "Downloading Mongo DB: %d%%" % (
                current / total * 100), "info", "  -", "\r")


# custom download progress bar for wget mongodb config file
def bar_custom_mongodbconfig(current, total, width=80):
    if current == total:
        print_message(
            "Downloading Mongo DB Config File: %d%%" % (
                current / total * 100), "info", "  -", "\n")
    else:
        print_message(
            "Downloading Mongo DB Config File: %d%%" % (
                current / total * 100), "info", "  -", "\r")


def create_custom_data_store():  # used to create the custom data store location for sellerspot mongodb instance
    print_message("Creating custom store folders...", "info", "  -")
    # navigating to sellerspot server folder
    pathStr = applicationFolderPath+"\data"
    if not os.path.isdir(pathStr):
        os.mkdir(pathStr)
    # creating log store
    pathStr = applicationFolderPath+"\log"
    if not os.path.isdir(pathStr):
        os.mkdir(pathStr)
    # creating log file
    if not os.path.isfile(applicationFolderPath+"\log\mongod.log"):
        f = open(applicationFolderPath+"\log\mongod.log", "w")
        f.close()


def delete_existing_mongodb_config():  # used to delete the existing mongodb config file
    print_message(
        "Deleting existing Mongo DB Config (if exists)...", "info", "  -")
    os.chdir(applicationFolderPath)
    subprocess.Popen(
        "del mongoconfig.cgf", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)


def download_mongodb_config():  # used to download the config file for sellerspot mongodb
    print_message("Initiating download of Mongo DB Config...", "info", "  -")
    wget.download(
        mongoDBConfigURL, applicationFolderPath, bar=bar_custom_mongodbconfig)


def check_mongodb():  # used to check if mongodb has been installed
    client = pymongo.MongoClient(serverSelectionTimeoutMS=500)
    try:
        # The ismaster command is cheap and does not require auth.
        client.admin.command('ismaster')
        return True
    except pymongo.errors.ConnectionFailure:
        return False


# used to invoke custom mongodb server
def invoke_custom_database_server(mongoDBVersion):
    os.chdir(mongoDBRootPath+"\\"+mongoDBVersion+"\\bin")
    mongoCheck = subprocess.Popen(
        "mongod.exe --config C:\SellerSpot\mongoconfig.cgf", shell=True,
        stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)


def check_mongodb_installer():  # used to check if mongodb installer is already downloaded
    for file in os.listdir(os.curdir):
        if (file.startswith("mongodb-windows") and file.endswith(".msi")):
            return file
    return False


def invoke_downloaded_mongodbinstaller():  # used to invoke the local mongodb installer
    print_message(
        "Opening downloaded MongoDB installer...", "info", "  -")
    os.system(f'msiexec /i {check_mongodb_installer()}')
    initiateMongoDbChecks()


def download_mongodbinstaller():  # used to download mongodb installer
    print_message("Initiating download of Mongo DB...", "info", "  -")
    wget.download(
        mongoDBURL, bar=bar_custom_mongodb)


def get_installed_mongodb_version():  # used to get the version of mongodb installed
    print_message("Checking version of MongoDB...",
                  "info", "  -", "\r")
    # getting all the apps installed in the local system into a csv file
    os.system("wmic product get name,version /format:csv > installedapps.csv")
    # opening app to read using codec pkg to handle conversion to utf-16
    spamreader = csv.reader(codecs.open(
        'installedapps.csv', 'rU', 'utf-16'), delimiter=',', quotechar='|')
    # finding the right version of mongodb installed
    for row in spamreader:
        if len(row) > 0 and "MongoDB" in row[1]:
            # updating global instances
            mongoDBVersion = str('.'.join(row[2].split('.')[0:2]))
            print_message("Installed version of Mongo DB - v%s" %
                          mongoDBVersion, "info", "  -", "\n")
            return mongoDBVersion


def initiateMongoDbChecks():  # used to initiate and handle mongodb installation checks

    if check_mongodb():  # checking mongodb existance
        print_message("Mongo DB Exists", "success", "")
        mongoDbVersion = get_installed_mongodb_version()
        create_custom_data_store()
        delete_existing_mongodb_config()
        time.sleep(1)
        download_mongodb_config()
        invoke_custom_database_server(mongoDbVersion)

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


def delete_server_instance():  # used to delete the local copy of server
    print_message(
        "Deleting local server instance (if exists)...", "info", "  -")
    subprocess.Popen(
        "del LocalConnectServer.exe", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)


def stop_server():  # used to stop execution of any running server instances
    print_message("Stopping running server instance", "info", "  -")
    subprocess.Popen(
        "taskkill /f /im LocalConnectServer.exe", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)


def get_latest_server(pathStr):  # used to get the latest version of local server
    wget.download(
        localServerURL, pathStr, bar=bar_custom_local_server)


def initiate_server():  # used to initiate the latest downloaded server
    print_message(
        "Initialising local server instance...", "info", "  -")
    subprocess.Popen(
        "LocalConnectServer.exe", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)


def check_local_server_status():  # used to check the status of local server
    try:
        response = requests.head('http://localhost:4000')
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
    # creating server folder
    pathStr = applicationFolderPath+"\server"
    if not os.path.isdir(pathStr):
        os.mkdir(pathStr)
    os.chdir(pathStr)
    # stopping running servers
    stop_server()
    time.sleep(1)
    # deleting local server instance
    delete_server_instance()
    # dowloading latest version of localconnect server
    get_latest_server(pathStr)
    # initializing local server instance
    initiate_server()
    # waiting for server to initialize
    time.sleep(5)
    # check if local server is up and running
    check_local_server_status()


# SERVER INVOKE SCRIPT INSTALLATION--------------------------------------------------------------------------------------------

# custom download progress bar for wget
def bar_custom_startup_script(current, total, width=80):
    if current == total:
        print_message(
            "Downloading startup script: %d%%" % (
                current / total * 100), "info", "  -", "\n")
    else:
        print_message(
            "Downloading startup script: %d%%" % (
                current / total * 100), "info", "  -", "\r")


# used to download the server invoke script
def download_invokeScript():
    wget.download(
        localServerInvokeScriptURL, startupFolderPath, bar=bar_custom_startup_script)


# used to delete the local copy of invoke script
def delete_invoke_script():
    print_message(
        "Deleting local copy of invoke script (if exists)...", "info", "  -")
    os.chdir(startupFolderPath)
    subprocess.Popen(
        "del sellerspotServerInvoke.exe", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)


def initiateInvokeScriptInstallation():  # used to install the startup script to invoke server on each restart
    print_message("Startup Script Check", "success", "")
    # deleting existing copy of invoke script
    delete_invoke_script()
    # downloading the invoke script into the startup folder
    download_invokeScript()
    print_message(
        "Startup Script installation successfull", "success", "  -")

# MAIN FUNCTION--------------------------------------------------------------------------------------------


if __name__ == "__main__":

    # clearing output and initializing text color engine
    init_colorit()

    # creating application folder in Program Files
    create_application_folder()

    # initialising mongoDb checks
    initiateMongoDbChecks()

    # initialising localServer checks
    initiateLocalServerChecks()

    # initialising startup script checks
    initiateInvokeScriptInstallation()

    # closing message
    print_message(
        "SellerSpot LocalConnect successfully installed", "success", "")

    input()
