import os
import subprocess
import csv
import codecs
from pathlib import Path

applicationFolderPath = str(Path.home())+"\\SellerSpot"


def get_installed_mongodb_version():  # used to get the version of mongodb installed

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
            return mongoDBVersion


def delete_created_csv_file():  # used to delete the app listing csv files
    subprocess.Popen(
        "del installedapps.csv", shell=True,
        stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)


if __name__ == "__main__":

    # navigating to the server folder
    os.chdir(applicationFolderPath+"\\server")

    # running server
    mongoCheck = subprocess.Popen(
        "LocalConnectServer.exe", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)

    # getting installed mongodb version
    installedMongoDBVersion = get_installed_mongodb_version()

    # deleting the created csv file
    delete_created_csv_file()

    os.chdir("C:\\Program Files\\MongoDB\\Server\\" +
             installedMongoDBVersion+"\\bin")

    os.system("mongod.exe --config "+applicationFolderPath+"\\mongoconfig.cgf")

    # # initializing database
    # mongoCheck = subprocess.Popen(
    #     "mongod.exe --config "+applicationFolderPath+"\\mongoconfig.cgf", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
