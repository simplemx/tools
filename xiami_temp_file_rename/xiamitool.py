#! /usr/bin/env python
#coding=gbk

import os
import shutil
import urllib

XIAMI_CD_PAGE_URL="http://www.xiami.com/album/370971"
"ie临时文件夹"
USER_TEMP_WEB_DIR="C:\\Documents and Settings\\Administrator\\Local Settings\\Temporary Internet Files"
"音乐文件输出路径"
MUSIC_OUTPUT_FILE_DIR="E:\\Alcest"


def getMusicNameInfo():
    #open(SOURCE_TEXT,"r").read()#
    content = urllib.urlopen(XIAMI_CD_PAGE_URL,"utf-8").read()
    info = {}
    num = ""
    name = ""
    cdName = ""
    bandName = ""
    #查找乐队名称
    tempIndex = content.find("<div id=\"title\">",0)
    if tempIndex > 0:
        nameEndIndex = content.find("</h1>",tempIndex)
	cdname = content[tempIndex:nameEndIndex]
	cdname = cdname[cdname.rfind(">")+1:]
	cdname = cdname.decode("utf-8").encode("gbk")
	tempIndex = content.find("artist",0)
	tempIndex = content.find("artist",tempIndex+1)
	nameEndIndex = content.find("<",tempIndex)
	bandName = content[tempIndex:nameEndIndex]
	bandName = bandName[bandName.find(">")+1:]
	bandName = bandName.decode("utf-8").encode("gbk")
	MUSIC_OUTPUT_FILE_DIR = "".join(["E:\\",cdname,"-",bandName])
	print MUSIC_OUTPUT_FILE_DIR
    #查找歌名
    trackIndex = content.find("trackid",0)
    tempIndex = 0
    while trackIndex > 0 :
        num = content[trackIndex + 9:content.find("<",trackIndex)]
        tempIndex = content.find("<a",trackIndex)
        "跳过<a标签到达内容"
        tempIndex = content.find(">",tempIndex)
        name = content[tempIndex + 1:content.find("</a>",trackIndex)]
        name = name.decode("utf-8").encode('gbk')
        info[num] = name
        trackIndex = content.find("trackid",tempIndex)
    return info

def makeSureTargetDirExists():
    try:
        os.chdir(MUSIC_OUTPUT_FILE_DIR)
    except WindowsError:
        os.mkdir(MUSIC_OUTPUT_FILE_DIR)
        os.chdir(MUSIC_OUTPUT_FILE_DIR)
    

def transferMusicFile2OutputDir():
    "在临时文件夹中迁移文件到输出文件夹中并且将原来临时文件夹中的mp3数据进行删除"
    "进行迁移前应该确保临时文件夹中只有当前专辑的音乐文件"
    makeSureTargetDirExists()
    infos = getMusicNameInfo()
    filenames = findTempMusicFileNames()
    for each in filenames:
        #print each
        shutil.copy(each,MUSIC_OUTPUT_FILE_DIR + "\\" + findCorrectName(each,infos))
        #print findCorrectName(each,infos)
        os.remove(each)
        
def findTempMusicFileNames():
    result = []
    fileIter = os.walk(USER_TEMP_WEB_DIR);
    for root, dirs, files in fileIter:
        for each in files:
            if each.lower().endswith(".mp3") and "%" in each:
                result.append(root+"\\"+each)
    return result
    

def correctNameInOutputDir():
    "修正输出文件夹下的MP3名称，可以直接在临时文件夹中迁移到此再调用本方法"
    filenames = os.listdir(MUSIC_OUTPUT_FILE_DIR)
    infos = getMusicNameInfo()
    os.chdir(MUSIC_OUTPUT_FILE_DIR)
    for each in filenames:
        os.rename(each,findCorrectName(each,infos))
        #os.remove(each)

def findCorrectName(oldName,infos):
    num = oldName[oldName.rindex("\\")+1 :oldName.index("%")]
    return "".join([num," ",infos[num],".mp3"])

if __name__ == "__main__":
    print getMusicNameInfo()
    transferMusicFile2OutputDir()
    """
    fileIter = os.walk(USER_TEMP_WEB_DIR)
    for root, dirs, files in fileIter:
        for each in files:
            if each.lower().endswith(".mp3") :
                print each
    """
        
        
