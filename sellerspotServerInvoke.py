import os
import subprocess

applicationFolderPath = "C:\SellerSpot"
mongoDBRootPath = r"C:\Program Files\MongoDB\Server\4.2\bin"

if __name__ == "__main__":

    # navigating to the server folder
    os.chdir(applicationFolderPath+"\server")

    # running server
    mongoCheck = subprocess.Popen(
        "LocalConnectServer.exe", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)

    os.chdir(r"C:\Program Files\MongoDB\Server\4.2\bin")
    # initializing database
    mongoCheck = subprocess.Popen(
        "mongod.exe --config C:\SellerSpot\mongoconfig.cgf", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
