#! /usr/bin/env python
#coding=utf-8

import sys

path_name="QueryTest"
target_path = "D:\\"
package = "package com.ailk.ics.view.QUST.fee.monthbill;"
page_content = """
import org.apache.tapestry.IRequestCycle;

import com.ailk.ics.core.QUST.SimplePage;
import com.linkage.component.PageData;

/**
 * %s
 *  
 * @author：chenmx@asiainfo-linkage.com
 * @version 1.0
 */
public abstract class %s extends SimplePage {
	
	/**
	 * 初始化页面
	 * initPage
	 *
	 * @param cycle
	 * @throws Exception void
	 * @Exception
	 */
	public void initPage(IRequestCycle cycle) throws Exception{
		PageData pd = getPageData();
		%s action = getAction();
		action.initPage(pd);
	}
	
	/**
	 *
	 * @param cycle
	 * @throws Exception void
	 * @Exception
	 */
	public void query(IRequestCycle cycle) throws Exception{
		PageData pd = getPageData();
		%s action = getAction();
		action.initPage(pd);
	}
}
"""
action_content = """
import com.ailk.ech.framework.spring.base.BaseAction;
import com.linkage.component.PageData;

public class %s extends BaseAction {

	@Override
	public void initPage(PageData pd) throws Exception {
		%s handler = getHandler(pd);
		handler.initPage(pd);
	}

	public void query(PageData pd) throws Exception {
		%s handler = getHandler(pd);
		handler.query(pd);
	}

}
"""
handler_content = """
import org.apache.log4j.Logger;

import com.ailk.ech.framework.spring.base.BaseHandler;
import com.linkage.appframework.data.DatasetList;
import com.linkage.appframework.data.IDataset;
import com.linkage.component.PageData;

public class %s extends BaseHandler {
	private static final Logger logger = Logger.getLogger(%s.class);

	public void initPage(PageData pd) throws Exception {
		%s page = getPage(pd);
	}

	public void query(PageData pd) throws Exception {

	}
}
"""
def writeFile(content, class_name):
	file = open(target_path + class_name + ".java","w")
	file.write(content)
	file.close()

html_content = """
<span jwcid="@DocType"/>
<html>
	<head jwcid="@icsframework:Head">
		<span jwcid="@HeadDoc"/>
	</head>
	<body jwcid="@Body">
		<span jwcid="@CommonBusiTop"/>
		<span jwcid="@Conditional" condition="ognl:isPageValidate">
			<!-- 业务逻辑开始 -->
			<!-- 业务逻辑结束 -->
		</span> 
		<span jwcid="@CommonBusiBottom" needRelativeBusi="true"/>
	</body>
</html>
"""
config_content = """
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE page-specification PUBLIC
  "-//Apache Software Foundation//Tapestry Specification 3.0//EN"
  "http://jakarta.apache.org/tapestry/dtd/Tapestry_3_0.dtd">

<page-specification class="com.ailk.ics.view.QUST.fee.monthbill.%s">
</page-specification>
"""
def writeHtml():
	file = open(target_path + path_name + ".html", "w")
	file.write(html_content)
	file.close()
	file = open(target_path + path_name + ".page", "w")
	file.write(config_content % (package[0:-1] + "." + path_name + "Page"))
	file.close()

def generate():
	page_name = path_name + "Page"
	action_name = path_name + "Action"
	handler_name = path_name + "Handler"
	page_gen_content = package + page_content % (page_name,page_name,action_name,action_name)
	action_gen_content = package + action_content % (action_name, handler_name, handler_name)
	handler_gen_content = package + handler_content % (handler_name, handler_name, page_name)
	print page_gen_content
	print action_gen_content
	print handler_gen_content
	writeFile(page_gen_content, page_name)
	writeFile(action_gen_content, action_name)
	writeFile(handler_gen_content, handler_name)
	writeHtml()

if __name__ == "__main__" :
	if len(sys.argv) > 1:
		path_name = sys.argv[1]
	print path_name
	generate()

