#! /usr/bin/env python
#coding=utf-8
import os
import sys
import string
import re

targetPath = "D:\\target"
filterList = []

def matchFile(file):
    for each in filterList:
        if file.endswith(each):
            return True
    return False

def matchFolder(folder):
    for each in filterList:
        if folder.endswith(each):
            return True
    return False


def filter():
    for (path,d,files) in os.walk(targetPath):
        for each in files:
            if matchFile(each):
                os.remove(os.path.join(path, each))
        for each in d:
            if matchFolder(each):
                os.rmdir(os.path.join(path, each))
        

if __name__ == "__main__":
    if len(sys.argv) > 1:
        list = sys.argv[1:]
        if list[0].find("path") == 0:
            targetPath = list[1]
            filterList = list[2:]
        else :
            filterList = list
        filter()

