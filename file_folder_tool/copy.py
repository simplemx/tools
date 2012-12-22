#! /usr/bin/env python
#coding=utf-8
import os
import sys
import shutil

targetPath = "D:\\target"
sourcePath = "D:\\source"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        sourcePath = sys.argv[0]
        targetPath = sys.argv[1]
    shutil.move(sourcePath, targetPath)

