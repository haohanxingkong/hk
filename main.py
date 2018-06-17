# -*- coding: utf-8 -*-
"""
Created on Mon May 21 20:15:22 2018

@author: bangwei
"""

# -*- coding: utf-8 -*-
"""
Created on Wed May 16 14:48:21 2018

@author: bangwei
"""

# -*- coding:utf-8 -*-
import sys
import socket
import json
from rec_print import*
from A_suanfa3 import*
from purchase1 import*
#从服务器接收一段字符串, 转化成字典的形式

def RecvJuderData(hSocket):
    nRet = -1
    Message = hSocket.recv(1024 * 1024 * 4)
    
    
    len_json = int(Message[:8])
    str_json = Message[8:].decode()
    
    while len(str_json)!=len_json:
        Message=hSocket.recv(1024 * 1024 * 4)
        str_json=str_json+Message.decode()
    nRet=0
    Dict = json.loads(str_json)
#############################################
  #  print(Message)
    if not('we_value' in Dict.keys()):
        print(Message)
    else:
        rec_print(Dict)
#############################################        
    return nRet, Dict

# 接收一个字典,将其转换成json文件,并计算大小,发送至服务器
def SendJuderData(hSocket, dict_send):
    str_json = json.dumps(dict_send)
    len_json = str(len(str_json)).zfill(8)
    str_all = len_json + str_json
#################################################
   # print(dict_send)    
    if not('purchase_UAV' in dict_send.keys()):
        print(dict_send)
    else:
        sed_print(dict_send)
##################################################        
    ret = hSocket.sendall(str_all.encode())
    if  ret == None:
        ret = 0  
    print('sendall', ret)
    print("-----------------------------------------------------")
    return ret

#用户自定义函数, 返回字典FlyPlane, 需要包括 "UAV_info", "purchase_UAV" 两个key.
#def AlgorithmCalculationFun(pstMapInfo, pstMatchStatus, pstFlayPlane):
  #  FlyPlane = c["astUav"]
    
    
    
    #return FlyPlane





def main(szIp, nPort, szToken):
    print("server ip %s, prot %d, token %s\n", szIp, nPort, szToken)

    #Need Test // 开始连接服务器
    hSocket = socket.socket()

    hSocket.connect((szIp, nPort))

    #接受数据  连接成功后，Judger会返回一条消息：
    nRet, _ = RecvJuderData(hSocket)
    if (nRet != 0):
        return nRet
    

    # // 生成表明身份的json
    token = {}
    token['token'] = szToken        
    token['action'] = "sendtoken"   

    
    #// 选手向裁判服务器表明身份(Player -> Judger)
    nRet = SendJuderData(hSocket, token)
    if nRet != 0:
        return nRet

    #//身份验证结果(Judger -> Player), 返回字典Message
    nRet, Message = RecvJuderData(hSocket)
    if nRet != 0:
        return nRet
    
    if Message["result"] != 0:
        print("token check error\n")
        return -1

    # // 选手向裁判服务器表明自己已准备就绪(Player -> Judger)
    stReady = {}
    stReady['token'] = szToken
    stReady['action'] = "ready"

    nRet = SendJuderData(hSocket, stReady)
    if nRet != 0:
        return nRet

    # //对战开始通知(Judger -> Player)
    nRet, Message = RecvJuderData(hSocket)
    if nRet != 0:
        return nRet
    
    #初始化地图信息
    pstMapInfo = Message["map"]  
    
    #初始化比赛状态信息
    pstMatchStatus = {}
    pstMatchStatus["time"] = 0

    #初始化飞机状态信息
    pstFlyPlane = {}
    pstFlyPlane["nUavNum"] = len(pstMapInfo["init_UAV"])   # 无人机种类信息
    pstFlyPlane["astUav"] = []

    #每一步的飞行计划
    FlyPlane_send = {}
    FlyPlane_send["token"] = szToken
    FlyPlane_send["action"] = "flyPlane"

    for i in range(pstFlyPlane["nUavNum"]):
        pstFlyPlane["astUav"].append(pstMapInfo["init_UAV"][i])
    
#############################循环中需要 记住的变量###############################################
    
        
###############################################################################################
    # // 根据服务器指令，不停的接受发送数据
    while True:

        # // 进行当前时刻的数据计算, 填充飞行计划，注意：1时刻不能进行移动，即第一次进入该循环时
       
        if pstMatchStatus["time"]==0:
           FlyPlane=pstFlyPlane["astUav"]
           FlyPlane_send['UAV_info'] = FlyPlane
        if pstMatchStatus["time"]>=1 :
           
            
           FlyPlane = AlgorithmCalculationFun(pstMapInfo, pstMatchStatus, pstFlyPlane)
           FlyPlane_send['UAV_info'] = FlyPlane
        
           purchase_plane=purchasefly(pstMapInfo, pstMatchStatus)
           #purchase_plane=[]
           FlyPlane_send['purchase_UAV'] = purchase_plane
        print("***********************************************************************")
        print(pstMatchStatus["time"])
        
        # //发送飞行计划
        nRet = SendJuderData(hSocket, FlyPlane_send)
        if nRet != 0:
            return nRet
        
        # // 接受当前比赛状态
        
        nRet, pstMatchStatus = RecvJuderData(hSocket)
        if nRet != 0:
            return nRet
        
        
        if pstMatchStatus["match_status"] == 1:
            print("game over, we value %d, enemy value %d\n", pstMatchStatus["we_value"], pstMatchStatus["enemy_value"])
            hSocket.close()
            return 0

if __name__ == "__main__":
    if len(sys.argv) == 4:
        print("Server Host: " + sys.argv[1])
        print("Server Port: " + sys.argv[2])
        print("Auth Token: " + sys.argv[3])
        main(sys.argv[1], int(sys.argv[2]), sys.argv[3])
    else:
        print("need 3 arguments")