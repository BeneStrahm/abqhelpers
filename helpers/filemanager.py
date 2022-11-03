# ------------------------------------------------------------------------------
# Description:  Helper functions for file/folder management - ABQ Version
# Author:       benedikt.strahm@ilek.uni-stuttgart.de
# Created:      2022-10-04
# Execution:    Import functions / collections (from pylek.helpers import util)
# ------------------------------------------------------------------------------
# ------------------------------------------------------------------------------
# Libraries
# ------------------------------------------------------------------------------
import os
import sys
import shutil
# ------------------------------------------------------------------------------
# Functions
# ------------------------------------------------------------------------------


def delFilesInFolder(fname):
    """Delete all files in a specified folder
    :param fname: string with name of folder
    """
    folder = fname
    for filename in os.listdir(folder):
        file_path = os.path.join(folder, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('Failed to delete %s. Reason: %s' % (file_path, e))


def getPathOfFile():
    """Allows to drag&drop file on your script and read path of file, see 
    filemanager.sample_getPathOfFile for an example
    :rtype cwd: current working directory
    :rtype filepath: str w/ absolute path of file
    :rtype folderpath: str w/ absolute path of folder containing file
    """
    # Current working directory
    cwd = os.getcwd()

    try:
        # If file was dropped on script
        filePath = sys.argv[1]
        folderPath = os.path.dirname(filePath)
    except IndexError:
        # If no file was dropped on script
        print("IndexWarning: Drag&Drop file on script to read path. Returning \"None\" for filePath and folderPath")
        filePath = None
        folderPath = None

    return cwd, filePath, folderPath


def scanFolder(fname):
    """Scans for all files and folders in a specified folder
    :param fname: string with name of folder
    :rtype dirpath: directory that was scanned
    :rtype dirnames: list w/ all folders in dirpath
    :rtype filenames: list w/ all files in dirpath
    """
    folder = fname
    # Walk through selected folder and scan for all files
    f = []
    for (dirpath, dirnames, filenames) in os.walk(folder):
        f.extend(filenames)
        break
    return dirpath, dirnames, filenames


def scanSubdirsForFilesWithExtension(dirpath, extension):
    """Scans for all files in directory and subdirectories with extension
    :param dirpath: string with name of folder to scan
    :param extension: string w/ extension to match
    :rtype filenames: list w/ of files
    :rtype filepaths: list w/ abspaths to files
    """
    import os
    filenames = []
    filepaths = []
    for root, directories, file in os.walk(dirpath):
        for file in file:
            if(file.endswith(extension)):
                filenames.append(file)
                filepaths.append(os.path.join(root, file))
    return filenames, filepaths


# ------------------------------------------------------------------------------
# Samples
# ------------------------------------------------------------------------------
if __name__ == "__main__":
    pass
