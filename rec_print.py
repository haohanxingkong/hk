# -*- coding: utf-8 -*-
"""
Created on Sat Jun  9 12:05:56 2018

@author: bangwei
"""
import  json
def rec_print( Dict):
    
    
    
#    len_json = int(Message[:8])
#    str_json = Message[8:].decode()
#    while len(str_json)!=len_json:
#        Message=hSocket.recv(1024 * 1024 * 4)
#        str_json=str_json+Message.decode()
#    
#    Dict = json.loads(str_json)
#   # print(len_json)
   
    
   
    print("token:",Dict["token"])

    print("notice:",Dict["notice"])

    print("match_status:",Dict["match_status"])

    print("time:",Dict["time"])

    print("we_value:",Dict["we_value"])

    UAV_we=Dict["UAV_we"]
    print("UAV_we:")
    print(*UAV_we,sep = '\n')

    print("enemy_value:",Dict["enemy_value"])

    UAV_enemy=Dict["UAV_enemy"]
    print("UAV_enemy:")
    print(*UAV_enemy,sep = '\n')

    goods=Dict["goods"]
    print("goods:")
    print(*goods,sep = '\n')

def sed_print(Message):
    print("action:",Message["action"])
    
    print("token:",Message["token"])
    
    UAV_info=Message["UAV_info"]
    print("UAV_info:")
    print(*UAV_info,sep = '\n')
    
    purchase_UAV=Message["purchase_UAV"]
    print("purchase_UAV:")
    print(*purchase_UAV,sep = '\n')
    
    
    
    