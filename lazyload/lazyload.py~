#! /usr/bin/env python
#coding=utf-8
import os
import sys
from PIL import Image

root_dir = "D:\\project_mobileDemo\\guizhoudocument\\系统设计\\UIUE设计\\V5.0"
source_file = "D:\\project_mobileDemo\\guizhoudocument\\系统设计\\UIUE设计\\V5.0\\index.html"
target_file = "D:\\project_mobileDemo\\guizhoudocument\\系统设计\\UIUE设计\\V5.0\\index2.html"
default_img = "src='www/qust/1.0/img/blank.gif'"
default_original = "data-original="

def is_img_tag(content, cursor):
	if len(content) > cursor+ 4:
		return content[cursor] == '<' and content[cursor + 1] == 'i' and content[cursor + 2] == 'm' and content[cursor + 3] == 'g'

def find_img_content(content, cursor):
	end = cursor
	while(end < len(content)):
		if content[end] == '>':
			break
		end = end + 1
	return content[cursor:end+1]

def get_img_size(url):
	url = url.replace("/","\\")
	url = root_dir +"\\" + url
	im = Image.open(url)
	return im.size

def is_attr_begin(content, cursor, attr):
	if len(content) - cursor <= len(attr):
		return False
	"匹配属性"
	for c in attr:
		if content[cursor] != c:
			return False
		cursor = cursor + 1
	"匹配="	
	while(cursor < len(content)):
		if content[cursor] == ' ':
			cursor = cursor + 1
		else:
			break
	if content[cursor] != '=':
		return False
	cursor = cursor + 1
	"匹配' or \""
	while(cursor < len(content)):
		if content[cursor] == ' ':
			cursor = cursor + 1
		else:
			break
	if content[cursor] != '\'' and content[cursor] != '"':
		return False
	return True

def get_attr_value(content, cursor):
	"find the next ' or \" after the cursor"
	sub = content[cursor:]
	index = 0
	type = '"'
	if '"' in sub:
		index = sub.index('"')
	if '\'' in sub and (index == 0 or sub.index('\'') < index) :
		index = sub.index('\'')
		type = '\''
	sub = sub[index + 1:]
	if type == '"':
		value_end = sub.index('"')
	else:
		value_end = sub.index('\'')
	
	return sub[:value_end] , content[cursor : cursor + index + value_end + 2]

def get_src_height_width(tag_content):
	cursor = 0
	src = width = height = src_attr = width_attr = height_attr = None
	while(cursor < len(tag_content)):
		if is_attr_begin(tag_content, cursor, "src"):
			src, src_attr = get_attr_value(tag_content, cursor)
		elif  is_attr_begin(tag_content, cursor, "width"):
			width, width_attr = get_attr_value(tag_content, cursor)
		elif is_attr_begin(tag_content, cursor, "height"):
			height, height_attr = get_attr_value(tag_content, cursor)
		cursor = cursor + 1
	return src, src_attr, height, height_attr, width, width_attr

def conver_new_content(tag_content):
	if "src" not in tag_content or default_original in tag_content:
		return None
	src, src_attr, height, height_attr, width, width_attr = get_src_height_width(tag_content)
	"""
	print src
	print src_attr
	print height
	print height_attr
	print width
	print width_attr
	"""
	h , w = height, width
	if not height or not width:
		"read img file size to get the width and height "
		img_width, img_height = get_img_size(src)
		if not height and not width:
			h = img_height
			w = img_width
		elif not height:
			"only has width"
			h = (width / img_width) * img_height
		elif not width:
			"only has height"
			w = (height / img_height) * img_width
	w_attr = " width='" + str(w) + "' "
	h_attr = " height='" + str(h) + "' "
	append = default_img + " " + default_original + "'" + src + "'"
	if width_attr:
		tag_content = tag_content.replace(width_attr , w_attr)
	else : 
		append = append + w_attr

	if height_attr :
		tag_content = tag_content.replace(height_attr, h_attr)
	else :
		append = append + h_attr
	tag_content = tag_content.replace(src_attr, append)
	return tag_content

hash = {}

def conver_content(content):
	cursor = 0
	count = 0
	while(cursor < len(content)):
		if is_img_tag(content, cursor):
			count = count + 1
			tag_content = find_img_content(content, cursor)
			if tag_content not in hash:
				"has not convered"
				new_tag_content = conver_new_content(tag_content)
				#print tag_content
				#print new_tag_content
				if new_tag_content and tag_content != new_tag_content:
					hash[new_tag_content] = True
					content = content.replace(tag_content, new_tag_content)
					cursor = cursor + len(new_tag_content)
		cursor = cursor + 1
	return content

def conver_file(spath, tpath):
	sfile = open(spath)
	tfile = open(tpath,"w")
	try:
		content = sfile.read()
		new_content = conver_content(content) 
		tfile.write(new_content)
	finally:
		tfile.close()
		sfile.close()

if __name__ == "__main__":
	conver_file(len(sys.argv) > 1 and sys.argv[1] or source_file, len(sys.argv) > 2 and sys.argv[2] or target_file)

