import os
import subprocess

if __name__ == "__main__":

    # navigating to the server folder
    pathStr = os.environ["ProgramW6432"]+"\SellerSpotServer"
    os.chdir(pathStr)

    # running server
    mongoCheck = subprocess.Popen(
        "LocalConnectServer.exe", shell=True, stdout=subprocess.PIPE, creationflags=subprocess.CREATE_NO_WINDOW)
