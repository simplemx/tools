#! /usr/bin/env python
#coding=gbk

import os
import shutil
import urllib

XIAMI_CD_PAGE_URL="http://www.xiami.com/album/370971"
"ie��ʱ�ļ���"
USER_TEMP_WEB_DIR="C:\\Documents and Settings\\Administrator\\Local Settings\\Temporary Internet Files"
"�����ļ����·��"
MUSIC_OUTPUT_FILE_DIR="E:\\Alcest"


def getMusicNameInfo():
    #open(SOURCE_TEXT,"r").read()#
    content = urllib.urlopen(XIAMI_CD_PAGE_URL,"utf-8").read()
    info = {}
    num = ""
    name = ""
    cdName = ""
    bandName = ""
    #�����ֶ�����
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
    #���Ҹ���
    trackIndex = content.find("trackid",0)
    tempIndex = 0
    while trackIndex > 0 :
        num = content[trackIndex + 9:content.find("<",trackIndex)]
        tempIndex = content.find("<a",trackIndex)
        "����<a��ǩ��������"
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
    "����ʱ�ļ�����Ǩ���ļ�������ļ����в��ҽ�ԭ����ʱ�ļ����е�mp3���ݽ���ɾ��"
    "����Ǩ��ǰӦ��ȷ����ʱ�ļ�����ֻ�е�ǰר���������ļ�"
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
    "��������ļ����µ�MP3���ƣ�����ֱ������ʱ�ļ�����Ǩ�Ƶ����ٵ��ñ�����"
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
        
        
