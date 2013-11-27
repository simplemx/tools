#! /usr/bin/env python
#coding=utf-8
"""
用途：将UAT/准生产的WEB目录下待上线文件移动到统一一个新的文件夹，PSO可以直接拖动这个文件夹到防篡改等服务器，减少人工操作

使用例子:
getpatch.py -s changelist -j ics.jar -d target
-s changelist
变更文件记录目录 默认为changelist文件
-j *.jar
class打包进的jar文件
-d target
待发布到目标服务器的文件夹 默认为target目录
-c WEB-INF/classes
class文件的所处目录
"""
import os
import sys,getopt
import shutil

changelist_file = "changelist"
target_dir = "target"
jar_file = ""
class_dir = "WEB-INF/classes"

def parse_opt():
    global changelist_file, target_dir, jar_file, class_dir
    opts, args = getopt.getopt(sys.argv[1:], "s:d:j:c:")
    for op, value in opts:
        if op == "-s":
            changelist_file = value
        elif op == "-d":
            target_dir = value
        elif op == "-j":
            jar_file = value
        elif op == "-c":
            class_dir = value
    print "changelist file is %s\ntarget dir is %s\njar_file is %s\nclass_dir is %s\n" % (changelist_file, target_dir, jar_file, class_dir)

def parse_change_list():
    try:
        file = open(changelist_file)
    except:
        print >>sys.stderr, "can not read changelist file, please check!(default file is changelist, do u missing pass -s argument or is changelist file not present?)"
        sys.exit(2)
    content = file.read()
    return content.split("\n")

def get_file_name(name):
    if name.find("|") > -1 :
        name = name[: name.index("|")]
    if name.find(".java") > -1:
        name = name[:name.index(".java")] + ".class"
    if name.find("com") > -1:
        name = name[name.index("com"):]
    return name

def mkdir(target_dir):
    if not os.path.isdir(target_dir):
        os.makedirs(target_dir)

def get_target_path(target_dir, path):
    return target_dir + "\\" + path

def move(file):
    if file.find('\\') > -1:
        file_name = file[file.rindex('\\') + 1:]
        path = file[:file.rindex('\\') + 1]
    else:
        file_name = file
        path = "\\"
    print "moving file %s from %s to %s" % (file_name, path, target_dir)
    mkdir(get_target_path(target_dir, path))
    shutil.copy(file, get_target_path(target_dir, path))
    print "moving file %s completed" % file_name 

def move_classes(class_files):
    global jar_file, target_dir
    if jar_file == "" or jar_file.find(".jar") == -1:
        print >>sys.stderr, "\n\nError!\nError!\nPlease ensure target jar file in this dictory(do you forget -jar parameter?)"
        sys.exit(2)
    print "****begin moving classes"
    mkdir("tmp")
    os.chdir("tmp")
    os.system("jar xvf ../%s" % jar_file)
    os.chdir("../")
    for file in class_files:
        file_name = file[file.rindex('\\') + 1:]
        path = file[:file.rindex('\\') + 1]
        print "moving file %s from %s to %s" % (file_name, path, "tmp")
        mkdir(get_target_path("tmp", path))
        shutil.copy(file, get_target_path("tmp", path))
        print "moving file %s completed" % file_name 
    print "****moving classes completed"
    print "****begin jar classes"
    os.chdir("tmp")
    os.system("jar cvf ../%s *.*" % jar_file)
    os.chdir("../")
    print "****end jar classes"
    print "begin delete tmp files"
    if os.path.isdir("tmp"):
        shutil.rmtree("tmp")
    print "end delete tmp files"
    print "moving target jar into WEB-INF/lib"
    lib_dir = target_dir + "\\WEB-INF\\lib"
    mkdir(lib_dir)
    shutil.copy(jar_file, lib_dir)
    print "moving target jar complete"

def move_files(file_names):
    print "to be moved file names is\n" + "\n".join(file_names)
    class_files = []
    for file_name in file_names:
        if file_name.find(".class") > -1:
            class_files.append(file_name) 
        else:
            move(file_name)
    if len(class_files) > 0:
        move_classes(class_files)

def patch():
    change_files = parse_change_list()
    change_files = [get_file_name(name) for name in change_files]
    mkdir(target_dir)
    move_files(change_files)

def clean():
    print "****begin clean"
    if os.path.isdir(target_dir):
        shutil.rmtree(target_dir)
    print "****clean completed"

if __name__ == "__main__":
    parse_opt()
    clean()
    patch()
    print "**** finish"
    
