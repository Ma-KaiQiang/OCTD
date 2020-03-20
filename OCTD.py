#/usr/bin/python
#-*- coding:utf-8 -*-
import os
import shutil
import time
import re
import threading
import queue
import datetime
import multiprocessing


def choosetype () :
    global seleck_num
    for i in range ( 1000 ) :
        seleck_num = int ( input (
            "Select the version you want to download---\r\n0:dri2  1:mpu2  2:mpc2  3:is2.2  4:mcs  5:h900  6:mtc  7:hdu2  8:apu2  9:cri2  10:All versions \r\n\r\nPlease select a type:\n" ) )
        if -1 < seleck_num < 11 :
            print ( "You choose the [%s] download type,Start downloading later.." %seleck_num)
            return
        else :
            print ( "Please enter the correct number! " )


def  listdir(path,list_name):
    '''返回path路径下的目录名称及最后创建时间'''
    for dir in os.listdir(path):
        file_path=os.path.join(path,dir)#将多个路径组合后返回
        if os.path.isdir(file_path):
            list_name.append((file_path,os.path.getmtime(file_path)))


def  newetfile(list_name):
    '''
    冒泡排序选出今天新更新的版本路径
    '''
    newest_dir=list_name[0]
    for i in range(len(list_name)):
        #为什么冒泡排序
        if i <(len(list_name)-1) and newest_dir[1] <list_name[i+1][1]:
            newest_dir=list_name[i+1]
        else:
            continue
    return newest_dir


def checkdir(new,checklist):
    '''
    将os.walk()函数遍历查询到的文件添加到列表全局列表内
    '''
    os.chdir(new)
    a=os.getcwd()
    # os.walk()top参数有单个返回值，所有用三个变量进行接收区分，除当前路径的文件
    for root,dirs,file in os.walk(a,topdown=False):
        for name in file:
            checklist.append(os.path.join(root,name))


def mkdir():
    '''
    创建本地文件夹以本地系统时间为名称
    '''
    if not os.path.exists(new_path):
        os.mkdir(new_path)
    if not os.path.exists(new_path+"\\"+dirname):
        os.makedirs ( new_path + "\\" + dirname , mode=0o777 , exist_ok=False )


def path1(old_path,checkpath,i):
    '''
    选择匹配路径
    '''
    # 字符与列表不能直接相连接，需要使用字符格式化函数，将列表转化为字符。
    checkpath="{}{}".format(old_path,checkpath[i])
    return  checkpath

def threads1(j):
    shutil.copy2(checklist[0][j], new_path + '\\' + dirname)


def threads2(j):
    shutil.copy2(checklist[1][j], new_path + '\\' + dirname)


def copy_mdimfile():
    '''
    将按条件匹配到的文件复制到指定目录下面
    '''

    mdimpath=path1(old_path,checkpath,0)
    # 返回路径下需要选择的目录
    listdir( mdimpath , list1 )
    new = newetfile (list1)
    checkdir ( new[0],checklist[0])
    th=[]
    for i in range(5):
         for j in range (len(checklist[0])):
        #使用完全匹配模式匹配字符串，防止模糊查询复制其他文件，
            if  re.fullmatch(copyfilelist[i] , os.path.basename(checklist[0][j])):
                t = threading.Thread(target=threads1,args=(j,))
                t.start()
                th.append(t)
                time.sleep(0.5)
                print("[%s] download over." % copyfilelist[i])
    for p in th:
        t.join()


def copy_mtfile():
    '''
    将按条件匹配到的文件复制到指定目录下面
    '''

    mtpath=path1(old_path,checkpath,5)
    # 返回路径下需要选择的目录
    listdir( mtpath , list1 )
    new = newetfile (list1)
    checkdir ( new[0],checklist[2])

    i=5
    while i<7:
        for j in range (len(checklist[2])):
            #使用完全匹配模式匹配字符串，防止模糊查询复制其他文件
            if re.fullmatch(copyfilelist[i], os.path.basename(checklist[1][j])):
                shutil.copy2(checklist[1][j], new_path + '\\' + dirname)
                print("[%s] download over." % copyfilelist[i])
        i += 1


def copy_adcfile ( ) :
    adcpath = path1( old_path , checkpath , 7 )
    listdir ( adcpath , list2 )
    new = newetfile ( list2 )
    checkdir ( new[0],checklist[1] )
    i = 7
    th=[]
    for i in range(7, 10):
        for j in range ( len ( checklist[1] ) ) :
            if re.fullmatch ( copyfilelist[i] , os.path.basename(checklist[1][j] ) ):
                t4=threading.Thread(target=threads2,args=(j,))
                t4.start()
                th.append(t4)
                time.sleep(0.5)
                print("[%s] download over." % copyfilelist[i])
    for l in th:
        t4.join()
def copy_singlefile( ):
    '''
    拷贝单个版本到指定目录下
    '''
    adcpath = path1(old_path, checkpath, seleck_num)
    listdir(adcpath, list1)
    new = newetfile(list1)
    checkdir(new[0],checklist[0])
    # print(checklist[0])
    for i in range(len(checklist[0])):
        # print("这是"+checklist[0][i])
        if re.search(copyfilelist[seleck_num], checklist[0][i]):
            if seleck_num==6:
                if os.path.getsize(checklist[0][i]) >20000000:
                    shutil.copy2(checklist[0][i], new_path + '\\' + dirname)
                    print("[%s] download over"%copyfilelist[seleck_num])
                    return
            shutil.copy2(checklist[0][i], new_path + '\\' + dirname)
            print("[%s] download over"%copyfilelist[seleck_num])


if __name__ == '__main__':
    '''以下为环境变量'''
    seleck_num = 0
    old_path = r"Z:\\"
    checkpath=[r"\XGB\20171017_PDS_V4R7B3SP1_IPE1",r"\XGB\20171017_PDS_V4R7B3SP1_IPE1",
               r"\XGB\20171017_PDS_V4R7B3SP1_IPE1",r"\XGB\20171017_PDS_V4R7B3SP1_IPE1",
               r"\XGB\20171017_PDS_V4R7B3SP1_IPE1",r"\NB\20171017_HD3_SP5_H900_IPE1",
               r"\NB\20171017_HD3_SP5_H900_IPE1", r"\SH\20180828_PDS_V4R7B3SP1_SHTY",
               r"\SH\20180828_PDS_V4R7B3SP1_SHTY",r"\SH\20180828_PDS_V4R7B3SP1_SHTY" ]
    new_path = r'D:\版本'
    list1 =[]
    list2 =[]
    copyfilelist = ["kdvdri2_h320.bin", "kdvmpu2.bin", "mcu2.bin", "kdvis22.bin","KdvMCS安装程序.exe","h900.bin.gz",
                    "setup.exe","kdvhdu2.bin", "kdvapu2.bin", "kdvcri2.bin"]
    checklist=[[],[],[]]

    '''以下为脚本运行代码'''
    try:

        choosetype()
        dirname = (time.strftime('%Y-%m-%d', time.localtime()))
        mkdir()
        #q = queue.Queue()
        if 10 == seleck_num:
            start=datetime.datetime.now()
            print("开始时间：%s"%start)
            T1=threading.Thread(target=copy_mdimfile,)
            # T1=multiprocessing.Process(target=copy_mdimfile(),)
            T2 = threading.Thread(target=copy_adcfile, )
            # T2 = multiprocessing.Process(target=copy_adcfile(), )
            T1.start()
            T2.start()
            T1.join()
            T2.join()
            print("All versions download over！")
            end=datetime.datetime.now()
            print("结束时间：%s"%end)
            input('press enter key to exit')

        else:
            T3=threading.Thread(copy_singlefile())
            T3.start()
            input('press enter key to exit')
    except:
        print("download error")
        input('press enter key to exit')



