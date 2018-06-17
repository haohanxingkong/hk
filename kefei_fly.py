# -*- coding: utf-8 -*-
"""
Created on Wed Jun  6 20:04:08 2018

@author: bangwei
"""
import sys

def kefei_ture(cc,good):
  for i in range(len(good)):
     if cc["load_weight"]>=good[i]["weight"]:
         return True
         continue




def kefei_fly(pstUAV_we,pstMapInfo,enemy_goal,enemy_fly,FlyPlane):
#############################  我方可飞行 无人机  ###################################
    ##### 识别每个型号飞机的 总充电容量  和 单位充电容量       
    def Type_dianliang(fly,pstUAV_price):  
       for i in range(len(pstUAV_price)):
          if pstUAV_price[i]["type"]==fly["type"]:
            return pstUAV_price[i]["capacity"],pstUAV_price[i]["charge"]
            break
    def qu_bianhao(zidian):        #取编号
       result=[]
       for i in range(len(zidian)):
         result.append(zidian[i]["no"])
       return result
#################################################################################### 
    
    FlyPlane_=[]
    kefei_fly=[]
    pstUAV_price=pstMapInfo["UAV_price"]
  #  h_low       =pstMapInfo["h_low"]
    pstparking  =pstMapInfo["parking"]
    
    
    
    pstUAV_price.sort(key=lambda x: x["value"])
    pstfly_value_xiao=pstUAV_price
##################################################################
    ke=1
    for i in range(len(pstUAV_we)):     #  只针对 停机坪上的  飞机进行的充电规划 
      if pstUAV_we[i]["no"] in qu_bianhao(FlyPlane):
                  continue
      if pstUAV_we[i]["status"]!=1 and pstUAV_we[i]["x"]==pstparking["x"] and pstUAV_we[i]["y"]==pstparking["y"] and pstUAV_we[i]["z"]==0 : 
             if  pstUAV_we[i]["type"]==pstfly_value_xiao[0]["type"] :
                  capacity,charge=0,0
                  capacity,charge=Type_dianliang(pstUAV_we[i],pstUAV_price)
#                 aa=pstUAV_we[i]
#                 aa["remain_electricity"]=pstUAV_we[i]["remain_electricity"]+charge
#                 FlyPlane.append(aa)
                  dd=pstUAV_we[i].copy()
                  if ke==1:
                     kefei_fly.append(dd)  # 电量为0 可以起飞？？？？？？？？
                     ke=0
                     continue
                  
                  dd["remain_electricity"]=pstUAV_we[i]["remain_electricity"]+charge
                  if dd["remain_electricity"]>capacity:
                     dd["remain_electricity"]=capacity
                  
                  if ke!=1:
                     FlyPlane_.append(dd)  
                  
             
             if  pstUAV_we[i]["type"]!=pstfly_value_xiao[0]["type"] and pstUAV_we[i]["z"]==0 :
                 capacity,charge=0,0
                 capacity,charge=Type_dianliang(pstUAV_we[i],pstUAV_price)
              
                 cc=pstUAV_we[i].copy()
  
                 if cc["remain_electricity"]==capacity:   #防止 加法 超出总电量  and cc["no"]==0
                         
                         if ke==1  :
                            kefei_fly.append(cc)
                            
                            ke=0
                            continue
                         if ke!=1:
                            FlyPlane_.append(cc) 
                 else:
                          cc["remain_electricity"]=pstUAV_we[i]["remain_electricity"]+charge
                          if cc["remain_electricity"]>=capacity:   #防止 加法 超出总电量
                             cc["remain_electricity"]=capacity
                          FlyPlane_.append(cc)   
                    
    return kefei_fly,FlyPlane_
                     
                     