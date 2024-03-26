import os
import time
from struct import unpack
import pandas as pd


# 获取day文件然后转换为正常文本
def read_data(fname, code):
    ''' 读取day数据 '''
    data = []
    with open(fname, 'rb') as f:
        buf = f.read()
    num = len(buf)  # 总长度
    no = num / 32  # 分块长度
    b = 0  # 开始指针
    e = 32  # 每一个小块的长度

    for i in range(int(no)):
        a = unpack('IIIIIfII', buf[b:e])
        data_time = toDataTime(a[0])
        openPrice = a[1] / 100.0
        high = a[2] / 100.0
        low = a[3] / 100.0
        close = a[4] / 100.0
        amount = a[5] / 100.0
        vol = a[6] / 100.0
        # 把数据添加到列表
        # [股票代码,开盘价，最高价，最低价，收盘价，成交额，成交量]
        
        data.append([code, a[0], openPrice, high, low, close, amount, vol])
        print(f"code: {code}, data_time: {a[0]}, openPrice: {openPrice}, high: {high}, low: {high}, low: {low}, close: {close}, amount: {amount}, vol: {vol}")
        b += 32
        e += 32
    return data


# 将数据转换为时间
def toDataTime(longTime):
    # val = val*100
    longTime = longTime / 1000  # float 时间戳格式(1019948462.2750368)
    t = time.localtime(longTime)
    # 👆 输出time.struct_time(tm_year=2002, tm_mon=4, tm_mday=28, tm_hour=7, tm_min=1, tm_sec=2, tm_wday=6, tm_yday=118, tm_isdst=0)
    week = time.strftime("%A", t)  # 输出Sunday 星期几
    strTime = time.strftime("%Y-%m-%d %H:%M:%S", t)  # 输出 2002-04-28 07:01:02
    return strTime


# 将目录与检索的文件名组合为路径，得到一个包含所有文件的路径
def getfileName(fname, suf):
    fileNames = []
    for i in range(0, len(suf)):
        fileNames.append(fname + suf[i])
    return fileNames


# 检索文件名得到一个包含所有文件名的列表
def getFileSuf(fname):
    suf = os.listdir(fname)
    return suf


def getData():
    data = []
    fname = r'/Users/henrychen/Desktop/test/py/sh/lday/'
    suf = getFileSuf(fname)  # 股票代码
    fileNameList = getfileName(fname, suf)  # 股票路径
    code = []
    for i in suf:
        code.append(i.split(".")[0])
    for i in range(0, len(fileNameList)):  # 循环获取 len(fileNameList)   数据量太大 取 10 减少数据量
        data.append(read_data(fileNameList[i], code[i]))
    return data


# 制作表格，返回
def makeDataFrame():
    col = ['股票代码', '日期', '开盘价', '最高价', '最低价', '收盘价', '成交额', '成交量']
    data = getData()
    suf = getFileSuf('/Users/henrychen/Desktop/test/py/sh/lday/')
    for i in range(0,len(data)):
        index = [j for j in range(1, len(data[i]) + 1)]
        df = pd.DataFrame(data[i], index=index, columns=col)
        saveDataFrame(df, suf[i])



# 保存表格
def saveDataFrame(df, code):
    codeList = code.split(".")
    df.to_excel("/Users/henrychen/Desktop/test/py/sh/" + codeList[0] + ".xlsx")


if __name__ == '__main__':
    makeDataFrame()
