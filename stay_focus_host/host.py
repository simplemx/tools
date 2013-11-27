#! /usr/bin/env python
#coding=utf-8
import sys

host_path = "C:\\WINDOWS\\system32\\drivers\\etc"

forbid_web_sites = ["weibo.com","v2ex.com","zhihu.com","smzdm.com","douban.com","z.cn"]

if __name__ == "__main__":
	type = sys.argv[1]
	if "d" == type:
		#disable web sites 
		file = open(host_path + "\\hosts","a")
		file.write("\n")
		for site  in forbid_web_sites:
			file.write("127.127.127.127 " + site + "\n")
		file.close()
	else :
		#enable web sites
		pass
