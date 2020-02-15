import sys
import os
import datetime
from xml.dom import minidom

"""
xml 格式定义
node1 的命名在root里是唯一的
node2 的命名在node1里是唯一的

<root>
    <node1 val1 = "..." val2 = "...."></node1>
    <node1>
        <node2 val1 = "..." val2 = "..."></node2>
    </node1>
</root>
"""

class XmlCmd():

    # 功能： 判断文件是否存在
    # 参数： filepath - 文件路径
    # 返回值：
    @staticmethod
    def isFileExist(filepath = str):
        rn = os.path.isfile(filepath)
        return rn

    # 功能： 创建XmlFile
    # 参数： filepath - 文件路径
    # 返回值：
    @staticmethod
    def createXml(filepath = str):
        rn = XmlCmd.isFileExist(filepath)
        if(rn == False):
            dom = minidom.Document()
            root = dom.createElement("root")
            dom.appendChild(root)

            date = dom.createElement("createDate")
            now_time = datetime.datetime.now()
            dtm = now_time.strftime("%Y-%m-%d %H:%M:%S")
            date.setAttribute("val",dtm)
            root.appendChild(date)

            with open(filepath,"w",encoding="utf-8") as fh:
                dom.writexml(fh, addindent='\t', newl='\n', encoding="utf-8")
                rn = True

            del dom
        else:
            print("文件已经存在")
            rn = True
        return rn

    # 功能： 读取字段
    # 参数： filepath - 文件路径
    #        node1 - 第一级名称
    #        node2 - 第二级名称
    # 返回值： 返回字符串列表，没有则返回空列表
    @staticmethod
    def readXml(filepath = str,node1 = str,node2 = str):
        ls = []
        bflg = XmlCmd.isFileExist(filepath)
        if  bflg== False:
            bflg = XmlCmd.createXml(filepath)
        if bflg == True:
            try:
                dom = minidom.parse(filepath)
                root = dom.documentElement
                lsnd1 = root.getElementsByTagName(node1)
                if lsnd1 != None and lsnd1.__len__() > 0:
                    nd1 = lsnd1[0]
                    if node2 != "":                                                                                     #判断是否存在第二级
                        lsnd2 = nd1.getElementsByTagName(node2)
                        if lsnd2 != None and lsnd2.__len__() > 0:
                            nd2 = lsnd2[0]
                            args = nd2.attributes                                                                       #读取所有元素
                            for it in args.values():
                                ls.append(it.name)
                                ls.append(it.value)
                    else:
                        args = nd1.attributes                                                                           #读取所有元素
                        for it in args.values():
                            ls.append(it.name)
                            ls.append(it.value)
            except Exception as e:
                print(e)
        return ls

    # 功能： 写xml文件
    # 参数： filepath - 文件路径
    #        lsdata - 文件列表
    #        node1 - 第一级名称
    #        node2 - 第二级名称
    # 返回值： 写入成功与否
    @staticmethod
    def writeXml(filepath = str,lsdata = [],node1 = str,node2 = str):
        rn = XmlCmd.isFileExist(filepath)
        if rn == False:
            rn = XmlCmd.createXml(filepath)
        if rn == True:
            rn = False
            dom = minidom.parse(filepath)
            root = dom.documentElement                                                                                  #根节点
            lsnd1 = root.getElementsByTagName(node1)
            if lsnd1 != None and lsnd1.__len__() > 0:
                nd1 = lsnd1[0]
                if node2 != "":                                                                                         #如果查询的是第二级
                    lsnd2 = nd1.getElementsByTagName(node2)
                    if lsnd2 != None and lsnd2.__len__() > 0:
                        nd2 = lsnd2[0]
                        nd1.removeChild(nd2)                                                                            #删除已存在的子项
                else:                                                                                                   #第一级
                    root.removeChild(nd1)
                    nd1 = dom.createElement(node1)
                    root.appendChild(nd1)                                                                               #删除已存在的子项
            else:
                nd1 = dom.createElement(node1)
                root.appendChild(nd1)                                                                                   #如果一级不存在 则添加

            if node2 == "":
                for i in range(0,lsdata.__len__(),2):
                    nd1.setAttribute(lsdata[i],lsdata[i+1])                                                             #添加元素
            else:
                nd2 = dom.createElement(node2)
                for i in range(0,lsdata.__len__(),2):
                    nd2.setAttribute(lsdata[i],lsdata[i+1])                                                             #添加元素
                nd1.appendChild(nd2)

            with open(filepath, "w", encoding="utf-8") as fh:
                dom.writexml(fh, indent="", addindent="", newl="", encoding="utf-8")                                    #写入文件
                rn = True
        return rn

    # 功能： 删除某个节点
    # 参数：
    # 返回值：
    @staticmethod
    def removeOneNode(filepath = str,node1 = str,node2 = str):
        pass