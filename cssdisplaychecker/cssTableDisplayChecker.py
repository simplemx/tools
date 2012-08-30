#! /usr/bin/env python
#coding=utf-8
import os
import string
import re

#path of your web app root
webRootPath = "D:\\project_wap\\aiwapcs\\xhtml"
#the dir that ignore
filterPaths = ["svn","classes","lib"]
#the file appendix of html/jsp or anything you want to check for
checkFilesAppendx = [".jsp",".html"]
#the tag that will ignore when it's in a error place but will not cause a error msg
ignoreTag = ["<cm:"]
#css files be found
cssFiles = []
table = []
row = []
cell = []
hash = {"table":table,"table-row":row,"table-cell":cell}

def isPathAccessable(path):
    for p in filterPaths:
        if path.find(p)>0:
            return False
    return True

def getCssFiles():
    for (path,d,files) in os.walk(webRootPath):
        if not isPathAccessable(path):
            continue
        t = [ path+"\\"+file for file in files if file.find(".css")>0]
        if len(t) > 0 :
            cssFiles.extend(t)
    
def translateCss(cssfiles):
    for f in cssfiles:
        file = open(f)
        try:
            content = file.read()
        finally:
            file.close()
        units = content.split("{")
        last = ""
        for unit in units:
            displayIndex = unit.find("display")
            if displayIndex > 0 :
                sub = unit[displayIndex+7:]
                sub = sub[sub.find(":")+1:]
                index = sub.find(";")
                if index > 0:
                    add2Table(sub[0:index],last)
                else:
                    parentIndex = sub.find("}")
                    if parentIndex > 0 :
                        add2Table(sub[0:parentIndex],last)
                    else:
                        pass
            last = unit

def add2Table(elem,lastStr):
    elem = string.strip(elem)
    lastStr = lastStr[lastStr.find("}")+1 : ]
    lastStr = string.strip(lastStr)
    lastStr = lastStr[lastStr.find(".")+1:]
    if elem in hash:
        hash[elem].append(lastStr)

def isFileAccessable(file):
    return len([each for each in checkFilesAppendx if file.find(each) > 0]) > 0

pattern = re.compile(r'class\s*=(\"|\').*?(\"|\')',re.DOTALL)
checkPattern = re.compile(r'<.*?>',re.DOTALL)

def isUnit(elem):
    "remove jsp include etc"
    return elem.find("<%") != 0 and (elem.find("class") > 0 or  elem.find("/>") == -1)

def filterUnits(array):
    return [ elem for elem in array if isUnit(elem["content"])]

def isBeginTag(elem):
    return not isSelfTag(elem) and not isEndTag(elem)

def isSelfTag(elem):
    return elem.find("/>") >= 0

def isEndTag(elem):
    return elem.find("</") >= 0

def getCorrectName(cls):
    cls = cls[cls.find("\"")+1:]
    return cls[:cls.find("\"")]
    
def getClassNames(elem):
    return [getCorrectName(cls.group()) for cls in pattern.finditer(elem)]

def getTableStuff(clsArray):
    return [cls for cls in clsArray if cls in table or cls in row or cls in cell]

def isInIgnoreTag(elem):
    return len([x for x in ignoreTag if elem.find(x) != -1]) > 0

def getLastClsArray(stack,hash):
    if len(stack) > 0 :
        "if last is a jstl tag that continue to search the second last tag"
        index = len(stack)-1
        while index >= 0 :
            if stack[index].find("<c:") != -1 or isInIgnoreTag(stack[index]):
                index = index-1
            else:
                break
            
        if index >= 0:
            return hash[stack[index]]
        else:
            return []
    else:
        return []

def msg(tag,filePath,lineNum,position,appendix):
    return "".join([tag," in file:",filePath," in line:",lineNum," in position:",position,appendix])

def checkLayout(filePath,elem,clsArray,stack,hash):
    "check the class name is layout correct"
    lastClsArray = getLastClsArray(stack,hash)
    for cls in clsArray:
        if len(lastClsArray) > 0:
            for lastCls in lastClsArray:
                if lastCls in table and cls in cell:
                    print msg(elem["content"],filePath,str(elem["lineNumber"]),str(elem["position"])," is not correct because it lay out in a table as a cell")
                elif cls in table:
                    print msg(elem["content"],filePath,str(elem["lineNumber"]),str(elem["position"])," should be careful beacause it's a layout and under a table stuff tag")
                elif lastCls in row and cls in row or lastCls in cell and cls in cell:
                    print msg(elem["content"],filePath,str(elem["lineNumber"]),str(elem["position"])," is not correct because it and it's parent tag are same table stuff tag")
                elif cls in row and lastCls in cell :
                    print msg(elem["content"],filePath,str(elem["lineNumber"]),str(elem["position"])," is not correct because it's a row and under a cell")
        else:
            if cls in row :
                print msg(elem["content"],filePath,str(elem["lineNumber"]),str(elem["position"])," is not correct because it has not layout in a table")
            if cls in cell:
                print msg(elem["content"],filePath,str(elem["lineNumber"]),str(elem["position"])," is not correct because it has not layout in a row")

def checkFiles():
    print "begin check"
    for (path,d,files) in os.walk(webRootPath):
        if not isPathAccessable(path):
            continue
        for f in files :
            if isFileAccessable(f):
                filePath = path + "\\" + f
                file = open(filePath)
                try:
                    found = getLineInfo(file)
                finally:
                    file.close()
                array = filterUnits(found)
                stack = []
                hash = {}
                for elem in array:
                    if isBeginTag(elem["content"]):
                        "check layout"
                        clsArray = getClassNames(elem["content"])
                        tableStuff = getTableStuff(clsArray)
                        if len(tableStuff) > 0:
                           checkLayout(filePath,elem,tableStuff,stack,hash) 
                        hash[elem["content"]] = tableStuff
                        stack.append(elem["content"])
                    elif isSelfTag(elem["content"]):
                        clsArray = getClassNames(elem["content"])
                        "check table stuff is layout correct,if is not table stuff it will be ignore"
                        tableStuff = getTableStuff(clsArray)
                        if len(tableStuff) > 0:
                            "check is table stuff layout correct"
                            checkLayout(filePath,elem,tableStuff,stack,hash)
                    elif isEndTag(elem["content"]):
                        "get the current begin tag ,it will be end and pop it from the stack"
                        if len(stack)>0:
                            "some jsp has part of an end tag"
                            stack.pop()
                    else:
                        print elem
                        raise Exception("elem error")

def getLineInfo(file):
    lineNum = 1;
    found = []
    needNextLine = False
    for line in file.readlines():
        if needNextLine:
            index = line.find(">")
            if index != -1:
                sub = sub+line[:index+1]
                found.append({"content":sub,"lineNumber":lineNum,"position":position})
                needNextLine = False
                sub = line[index+1:]
                sub,position = findTag(sub,lineNum,found)
                if sub:
                    needNextLine = True
            else:
                sub = sub+line    
        else:
            sub,position = findTag(line,lineNum,found)
            if sub:
                needNextLine = True
        lineNum = lineNum + 1
    return found
        
def findTag(line,lineNum,found):
    position = index = line.find("<")
    if index != -1:
        "found"
        sub = line[index:]
        index = sub.find(">")
        if index != -1:
            rest = sub[index + 1 :]
            sub = sub[:index + 1]
            found.append({"content":sub,"lineNumber":lineNum,"position":position})
            return findTag( rest, lineNum,found)
        else:
            return sub,position
    return (None,None)

if __name__ == "__main__":
    getCssFiles()
    print cssFiles
    if len(cssFiles) < 1:
        print "can't find css files"
    else:
        translateCss(cssFiles)
        print table
        print row
        print cell
        if len(table) < 1 and len(row) < 1 and len(cell) < 1:
            print "can't find any table css attribute" 
        else:
            checkFiles()
