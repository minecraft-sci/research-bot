import os

def createFolderIfNotExist(path):
    if not os.path.exists(path):
        os.makedirs(path)

def exists(path):
    return os.path.exists(path)