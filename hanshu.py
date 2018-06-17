# -*- coding: utf-8 -*-
"""
Created on Sun Jun 10 10:02:47 2018

@author: bangwei
"""

#  所有功能函数定义
import sys
from math import*
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from A_STAR_xiugai import*

####  取种类  和 载重函数      (可以不用 返回信息 中 有load_weight )
def Type_loadweight(fly,pstUAV_price):               
    for i in range(len(pstUAV_price)):
        if pstUAV_price[i]["type"]==fly["type"]:
           return pstUAV_price[i]["load_weight"]
           break
##### 识别每个型号飞机的 总充电容量  和 单位充电容量       
def Type_dianliang(fly,pstUAV_price):  
    for i in range(len(pstUAV_price)):
        if pstUAV_price[i]["type"]==fly["type"]:
            return pstUAV_price[i]["capacity"],pstUAV_price[i]["charge"]
            break
####  飞机 与货物的距离 
def juli_fly_good(fly,good):
    good_start_end=sqrt((good["start_x"]-good["end_x"])**2+(good["start_y"]-good["end_y"])**2)  #预估飞机电量重要依据
    
    fly_good_start=sqrt((fly["x"]-good["start_x"])**2+(fly["y"]-good["start_x"])**2)
    
    fly_good= fly_good_start+good_start_end
    
    return fly_good
####  自我碰撞检测     (有错误  仔细检查  'int' object is not subscriptable )
    
def qu_pstwe(fly,pstUAV_we):   # 取之前的状态
    for i in range(len(pstUAV_we)):
        if fly["no"]==pstUAV_we[i]["no"]:
            cc=pstUAV_we[i].copy()
            continue
    return cc  

def self_pengzhuang(fly,FlyPlane,pstUAV_we,pstMapInfo):   #  不能和自己对比
    h_low       =pstMapInfo["h_low"]
    h_high      =pstMapInfo["h_high"]
    pstparking  =pstMapInfo["parking"]
    k=1
    
    for i in range(len(FlyPlane)): 
        pstwe = qu_pstwe(fly,pstUAV_we)
        if  pstwe["x"]==pstparking["x"] and pstwe["y"]==pstparking["y"]:   # 停机坪  上空 不进行 碰撞检测
            continue
        
            
        if fly["z"]==FlyPlane[i]["z"] and fly["z"]>=h_low:
             juli=sqrt((fly["x"]-FlyPlane[i]["x"])**2 + (fly["y"]-FlyPlane[i]["y"])**2)
             if 0<=juli  and juli <=sqrt(2):
                 pstwe = qu_pstwe(fly,pstUAV_we)
                 fly1=pstwe.copy()
                 fly1["z"]=fly1["z"]+1
                 
                 k=0
                 if  fly1["z"]>h_high:
                     fly1["z"]=h_high
                     k=0
                 continue
    if k==1:
       return fly 
    else:
       return fly1 
def self_xia_peng(fly,FlyPlane,pstMapInfo):
    h_low       =pstMapInfo["h_low"]
    h_high      =pstMapInfo["h_high"]
    k=1
    for i in range(len(FlyPlane)):   
       juli=sqrt((fly["x"]-FlyPlane[i]["x"])**2 + (fly["y"]-FlyPlane[i]["y"])**2) 
       if juli <=sqrt(2):
          if fly["z"]==FlyPlane[i]["z"] :
               fly["z"]=fly["z"]+1
    return fly
    
def wjun_pengzhuang(FlyPlane,now,pstfly_value_xiao):
     kk=0
     for i in range(len(FlyPlane)):
         if  FlyPlane[i]["type"]==pstfly_value_xiao[0]["type"]:
             if now["x"]==FlyPlane[i]["x"] and now["y"]==FlyPlane[i]["y"] and now["z"]==FlyPlane[i]["z"]:
                 now["z"]=now["z"]+1
                 kk=1
     return now
           
###############################################################################
def qu_bianhao(zidian):        #取编号
     result=[]
     for i in range(len(zidian)):
         result.append(zidian[i]["no"])
     return result    

def in_build(w,build,pstmap):          
        x=w["x"]
        y=w["y"]
        width=pstmap["x"]
        length=pstmap["y"]
        if x < 0 or x >= width or y < 0 or y >= length:

           return True
        for i in range(len(build)):
            
            b0_x=build[i]["x"]
            b0_y=build[i]["y"]
            
            b2_x=build[i]["x"]+build[i]["l"]-1
            b2_y=build[i]["y"]+build[i]["w"]-1
            
            if x >= b0_x and x <= b2_x and y >= b0_y and y <= b2_y:
               return True          
###############################################################################
def weiguohua_good(guihua_fly_1,guihua_fly_2,pstgoods_kejian):
    good=[]
    for i in range(len(pstgoods_kejian)):
        if pstgoods_kejian[i]["no"] in qu_bianhao(guihua_fly_1):
            continue
        if pstgoods_kejian[i]["no"] in qu_bianhao(guihua_fly_2):
            continue
        
        good.append(pstgoods_kejian[i])
        
##############################################################################   敌军有货飞机 攻击  终点        
def good_enemy_plan(FlyPlane,pstgoods,enemy_fly_good,enemy_goal_good,h_low,pstmap,h_Low_build):
    FlyPlane_=[]
    for i in range(len(enemy_fly_good)):    # 我方 攻击飞机  及我方攻击目标 计划
         
         
         if enemy_fly_good[i]["z"]==h_low:    #攻击无人机 平移高度 h_low+1  避免撞击我方无人机 
             eee=enemy_fly_good[i]
             eee["z"]=enemy_fly_good[i]["z"]+1
             FlyPlane.append(eee)     #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@         
         if enemy_fly_good[i]["no"] in qu_bianhao(FlyPlane):
             continue
         if enemy_fly_good[i]["no"] in qu_bianhao(FlyPlane_):
             continue         
         path_12 =  []
         star    = enemy_fly_good[i]
                                                               #雾区处理
         for j in range(len(pstgoods)):
           if enemy_goal_good[i]["goods_no"]==pstgoods[j]["no"]:
                 end={"x":pstgoods[j]["end_x"],"y":pstgoods[j]["end_y"]} 
                     
         path02=find_path(star,end,h_Low_build,pstmap)
         path12=path02[::-1]

         del path12[0]
         
         path_12.append(path12)
         bb=enemy_fly_good[i].copy()
         bb["x"]=path_12[0][0]["x"]
         bb["y"]=path_12[0][0]["y"]
         
         path_12.clear()
         
         #be=self_pengzhuang(enemy_fly[i],FlyPlane,pstUAV_we,pstMapInfo)
         FlyPlane_.append(bb)            #00000000000000000000000000000000000000000    
    return  FlyPlane_    
        
   
    