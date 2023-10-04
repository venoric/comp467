# Source https://towardsdatascience.com/implementing-a-file-watcher-in-python-73f8356a425d

watchDirectory = '/Users/casey/Desktop/csun/comp467/week3'
pollTime = 3

from os import listdir
from os.path import isfile, join

#function to return files in a directory
def fileInDirectory(my_dir: str):
    onlyfiles = [f for f in listdir(my_dir) if isfile(join(my_dir, f))]
    return(onlyfiles)

def listComparison(OriginalList: list, NewList: list):
    differencesList = [x for x in NewList if x not in OriginalList]
    return(differencesList)


def doThingsWithNewFiles(newFiles: list):
    print(f'I would do things with file(s) {newFiles}')

import time
def fileWatcher(my_dir: str, pollTime: int):
    while True:
        if 'watching' not in locals(): #Check if this is the first time the function has run
            previousFileList = fileInDirectory(watchDirectory)
            watching = 1
        
        time.sleep(pollTime)
        
        newFileList = fileInDirectory(watchDirectory)
        
        fileDiff = listComparison(previousFileList, newFileList)
        
        previousFileList = newFileList
        if len(fileDiff) == 0: continue
        doThingsWithNewFiles(fileDiff)

fileWatcher(watchDirectory, pollTime)