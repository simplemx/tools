#!/usr/bin/env python
# coding=utf-8

import config
import os
import xml.dom.minidom

def deploy():
	if not os.path.isdir(config.TongWebPath):
		print "请确认config.py文件里的TongWebPath设置或者是否东方通服务器的文件路径准确"	
		return
	
	print "begin deploying"

	"bak server file"
	bak_dir = config.TongWebPath + "_bak"
	cmd = "cp -fr " + config.TongWebPath + " " + bak_dir
	print cmd
	os.system(cmd)
	for node in config.targetPath:
		if "path" not in node:
			print "path missing ,skip this node "
			continue
		cmd = "cp -fr " + bak_dir + " " + node["path"]
		print cmd
		os.system(cmd)	
		"begin to change port"
		port_config(node)
		mv_license(node)
		jvm_config(node)
		if config.is_start:
			start_server(node)
	"运行完毕删除bak文件夹"
	cmd = "rm -r " + bak_dir
	print cmd
	os.system(cmd)

def start_server(config_node):
	"启动应用"
	cmd = config_node["path"] + "/bin/startserver.sh &"
	print cmd
	os.system(cmd)

def jvm_config(config_node):
	"将copyfiles下的startserver.sh复制到东方通服务器下"
	cmd = "mv " + config_node["path"] + "/bin/startserver.sh " + config_node["path"] + "/bin/startserver.shbak"
	print cmd
	os.system(cmd)
	cmd = "cp ./copyfiles/startserver.sh " + config_node["path"] + "/bin/startserver.sh"
	print cmd
	os.system(cmd)

def mv_license(config_node):
	"将copyfiles下的license文件复制到东方通服务器下"
	cmd = "cp ./copyfiles/license.dat " + config_node["path"]
	print cmd
	os.system(cmd)

def port_config(config_node) :
	"修改端口配置，也就是修改应用下的twns.xml"
	"bak twns.xml"
	cmd = "cp " + config_node["path"] + "/config/twns.xml " + config_node["path"] + "/config/twns.xmlbak"
	print cmd
	os.system(cmd)
	
	"change xml"
	xml_path = config_node["path"] + "/config/twns.xml"
	doc = xml.dom.minidom.parse(xml_path)
	iiop_node = doc.getElementsByTagName("iiop-service")
    	iiop_node = iiop_node[0]
    	listener_node = iiop_node.getElementsByTagName("listener")
    	listener_node = listener_node[0]
    	listener_node.setAttribute("port", config_node["iiop_port"])

    	jmx_node = doc.getElementsByTagName("jmx-connector")
    	jmx_node = jmx_node[0]
    	jmx_node.setAttribute("port", config_node["jmx_port"])

    	http_nodes = doc.getElementsByTagName("http-listener")
    	for node in http_nodes:
        	if node.getAttribute("default-virtual-server") == "server":
            		node.setAttribute("port", config_node["http_port"])
        	else:
            		node.setAttribute("port", config_node["admin_port"])
	file = open(xml_path, "w")
    	file.write(doc.toxml())	 

if __name__ == "__main__":
	deploy()
