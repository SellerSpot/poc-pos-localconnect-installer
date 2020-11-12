import os
import subprocess

applicationFolderPath = "C:\SellerSpot"

if __name__ == "__main__":

    # navigating to the server folder
    os.chdir(applicationFolderPath+"\server")

    # running server
    mongoCheck = subprocess.Popen(
        "LocalConnectServer.exe", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)

    # initializing database
    mongoCheck = subprocess.Popen(
        "mongod --config C:\SellerSpot\mongoconfig.cgf", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
