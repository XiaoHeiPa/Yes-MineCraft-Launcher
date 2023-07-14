from os import makedirs
from urllib.request import urlretrieve  # 下载函数
from sys import stdout
from os.path import exists, split
from json import loads

# 下载文件函数
def download(url: str, path: str):
    try:
        (filepath, filename) = split(path)
        if not exists(filepath):
            makedirs(filepath)

        def hook(blocknum, bs, size):  # 回调
            # blocknum数据块数量
            # bs数据块大小
            # size下载下来的总大小
            # 下载进度 = (blocknum x bs) / size
            a = int(float(blocknum * bs) / size * 100)
            if a >= 100:
                a = 100
            stdout.write("\r>>正在下载" + filename + ":" + str(a) + "%")

        urlretrieve(url=url, filename=path, reporthook=hook)
        print("\n")
    except:
        print("\n由于网络原因，下载发生错误，正在尝试重新下载\n")
        download(url=url, path=path)

def downloadList():
    # 下载版本清单文件
    # url = "https://launchermeta.mojang.com/mc/game/version_manifest.json"
    url = "https://bmclapi2.bangbang93.com/mc/game/version_manifest.json"  # 国内源
    path = "./version_manifest.json"

    download(url=url, path=path)
    print("下载完成\n")


downloadList()


def Outversion(isOut=False, release=False, snapshot=False, old=False):
    # isOut是否在屏幕上输出版本列表
    # release正式版
    file = open("./version_manifest.json")
    VersionListDict = loads(file.read())
    for v in VersionListDict["versions"]:
        if isOut:  # 输出列表
            if release:
                if v["type"] == "release":
                    print("版本号" + v["id"] + "版本类型" + v["type"])
            if snapshot:
                if v["type"] == "snapshot":
                    print("版本号" + v["id"] + "版本类型" + v["type"])
            if old:
                if "old" in v["type"]:
                    print("版本号" + v["id"] + "版本类型" + v["type"])
    return VersionListDict

Outversion(isOut=True, release=True, snapshot=True, old=True)


def isRightVersion(version: str):
    VLD = Outversion()
    flag = False  # 判断是否有这个版本
    for v in VLD["versions"]:
        if v["id"] == version:
            flag = True
    return flag


# 下载游戏部分
def downloadVersion(version: str, mcDir: str):
    # mcDir.minecraft路径

    # 1,下载版本json文件
    if isRightVersion(version):
        VLD = Outversion()
        for v in VLD["versions"]:
            if v["id"] == version:
                url = v["url"]
                path = mcDir + "\\versions\\" + version + "\\" + version + ".json"
                if not exists(mcDir + "\\versions\\" + version):
                    makedirs(mcDir + "\\versions\\" + version)

                download(url=url, path=path)
                print("版本json下载完成\n")

    # 2,下载客户端
    file = open(mcDir + "\\versions\\" + version + "\\" + version + ".json")
    VersionDict = loads(file.read())
    url = VersionDict["downloads"]["client"]["url"]
    path = mcDir + "\\versions\\" + version + "\\" + version + ".jar"

    download(url=url, path=path)
    print("游戏本体下载完成\n")

    # 3,下载依赖库
    for lib in VersionDict["libraries"]:
        # 下载普通库
        if "artifact" in lib["downloads"] and not "classifiers" in lib["downloads"]:
            url = lib["downloads"]["artifact"]["url"]
            (filepath, tempfilename) = split(lib["downloads"]["artifact"]["path"])
            if not exists(mcDir + "\\libraries\\" + filepath):
                makedirs(mcDir + "\\libraries\\" + filepath)
            path = mcDir + "\\libraries\\" + lib["downloads"]["artifact"]["path"]

            download(url=url, path=path)

        # 下载natives库
        if "classifiers" in lib["downloads"]:
            # 下载artifact部分
            url = lib["downloads"]["artifact"]["url"]
            (filepath, tempfilename) = split(lib["downloads"]["artifact"]["path"])
            if not exists(mcDir + "\\libraries\\" + filepath):
                makedirs(mcDir + "\\libraries\\" + filepath)
            path = mcDir + "\\libraries\\" + lib["downloads"]["artifact"]["path"]

            download(url=url, path=path)
            # 下载classifiers部分
            for cl in lib["downloads"]["classifiers"].values():
                url = cl["url"]
                (filepath, tempfilename) = split(cl["path"])
                if not exists(mcDir + "\\libraries\\" + filepath):
                    makedirs(mcDir + "\\libraries\\" + filepath)
                path = mcDir + "\\libraries\\" + cl["path"]

                download(url=url, path=path)
    print("\n依赖库下载完成\n")



a = input("请输入您需要下载的版本：")




downloadVersion(a, ".\\.minecraft")
