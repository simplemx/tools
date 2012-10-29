#! /usr/bin/env python
#coding=gbk

import os
import shutil
import urllib

class MyURLopener(urllib.FancyURLopener):
	#伪装成Firefox
	version = "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9.0.2)"

urllib._urlopener = MyURLopener()

def getHtmlContent(url):
	return urllib.urlopen(url,"gbk").read()

if __name__ == "__main__":
	t = getHtmlContent("http://simplemx.iteye.com/")
	print t
	f = open("D://temp222.txt","w")
	f.write(t)
	f.close()
