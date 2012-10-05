#! /usr/bin/env python
#coding=gbk

import os
import shutil
import urllib

class MyURLopener(urllib.FancyURLopener):
	#伪装成Firefox
	version = "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.30 (KHTML, like Gecko) Chrome/12.0.742.30 Safari/534.30"

urllib._urlopener = MyURLopener()

def getHtmlContent(url):
	return urllib.urlopen(url,"gbk").read()

if __name__ == "__main__":
	t = getHtmlContent("http://simplemx.iteye.com/")
	print t
	f = open("D://temp222.txt","w")
	f.write(t)
	f.close()
