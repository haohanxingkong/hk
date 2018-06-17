# -*- coding: utf-8 -*-
"""
Created on Mon May 21 19:43:05 2018

@author: bangwei
"""
import sys
from math import*
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from A_STAR_xiugai import*
from kefei_fly import*
from path_cost import*
from hanshu import*
import random
def AlgorithmCalculationFun(pstMapInfo, pstMatchStatus, pstFlayPlane):
######   初始化变量     ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~   
    pstmap      =pstMapInfo["map"]   #初始化地图 寻路要用
    pstparking  =pstMapInfo["parking"]
    pstfog      =pstMapInfo["fog"]
    pstbuilding =pstMapInfo["building"]
    pstUAV_price=pstMapInfo["UAV_price"]
    h_low       =pstMapInfo["h_low"]
    h_high      =pstMapInfo["h_high"]
    pstUAV_we = pstMatchStatus["UAV_we"]              # 返回的飞机信息
    UAV_we=pstUAV_we    
    pstgoods=pstMatchStatus["goods"]                  # 返回的物品信息
    pstUAV_enemy=pstMatchStatus["UAV_enemy"]          #返回敌军信息
    time=pstMatchStatus["time"] 
#######  障碍  初始化  
    h_Low_build=[]
    for i in range(len(pstbuilding)):
        if pstbuilding[i]["h"]>=pstMapInfo["h_low"]:
            h_Low_build.append(pstbuilding[i])
    
                            ## 慎用！！！！  可能会导致 我飞机在“建筑物”中  而陷入死循环
    
#####~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~    
######################################################
    FlyPlane=[] # 飞行计划表
    pstgoods_kejian=[]
    pstgoods_bu_kejian=[]    
    guihua_fly_1=[]
    guihua_good_1=[]
####################################################    
                                                     # 每次接受的飞机  按价值排序   从小到大
    pstUAV_price.sort(key=lambda x: x["value"])
    pstfly_value_xiao=pstUAV_price
    
    for i in range(len(pstUAV_enemy)):
        for m in range(len(pstUAV_price)):
            if pstUAV_enemy[i]["type"]==pstUAV_price[m]["type"]:
                    pstUAV_enemy[i]["value"]=pstUAV_price[m]["value"]

    pstUAV_enemy.sort(key=lambda x: -x["value"])     #  只限于  敌军飞机  排序   从大到小

    #pstUAV_we.sort(key=lambda x: x["load_weight"])
             
################################################对所有线上 飞机规划  #############################################
####  攻击无人机  规划 （别人用我就用）  
    enemy_guihua_goal=[]        #所有 正常没拿货 的敌军飞机
    enemy_guihua_goal_good=[]   #所有 没坠毁 拿货 的敌军飞机
    for i in range(len(pstUAV_enemy)):
        if in_build(pstUAV_enemy[i],h_Low_build,pstmap):
            continue     
        if  pstUAV_enemy[i]["status"]!=2 and pstUAV_enemy[i]["goods_no"]==-1:
                  enemy_guihua_goal.append(pstUAV_enemy[i])         #  我方飞机攻击目标  不包含雾区
        if  pstUAV_enemy[i]["goods_no"]!=-1 : 
                  enemy_guihua_goal_good.append(pstUAV_enemy[i])
#####################################################################    
    gongji_xia_good=[]   # 规划的敌军飞机
    for i in range(len(pstUAV_we)):  #攻击飞机下降
        
        if pstUAV_we[i]["no"] in qu_bianhao(FlyPlane):
              continue
        
            
        if pstUAV_we[i]["type"]==pstfly_value_xiao[0]["type"] and pstUAV_we[i]["status"]!=1:
           kk=1
           for m in range(len(enemy_guihua_goal_good)):  #  带货 但不在雾区
             if enemy_guihua_goal_good[m]["status"]!=2 :   ####不包含雾区 
               if kk==1 and pstUAV_we[i]["x"]==enemy_guihua_goal_good[m]["x"] and pstUAV_we[i]["y"]==enemy_guihua_goal_good[m]["y"] and enemy_guihua_goal_good[m]["z"]<pstUAV_we[i]["z"]:
                     if 1==pstUAV_we[i]["z"]:
                         FlyPlane.append(pstUAV_we[i])
                         kk=-1
                     else:
                         cc=pstUAV_we[i].copy()
                         cc["z"]=cc["z"]-1
                         FlyPlane.append(wjun_pengzhuang(FlyPlane,cc,pstfly_value_xiao))
                        #FlyPlane.append(cc)                   
                         gongji_xia_good.append(enemy_guihua_goal_good[m])
                         kk=-1  
                         continue
           for m in range(len(enemy_guihua_goal_good)):   # 带货  但攻击飞机 不在头顶
             
                for j in range(len(pstgoods)):
                  if enemy_guihua_goal_good[m]["goods_no"]==pstgoods[j]["no"]:
                     if kk==1 and pstUAV_we[i]["x"]==pstgoods[j]["end_x"] and pstUAV_we[i]["y"]==pstgoods[j]["end_y"] :
                        if 1==pstUAV_we[i]["z"]:
                             FlyPlane.append(pstUAV_we[i])
                             kk=-1
                        else:
                            cc=pstUAV_we[i].copy()
                            cc["z"]=cc["z"]-1
                            #FlyPlane.append(wjun_pengzhuang(FlyPlane,cc,pstfly_value_xiao))
                            FlyPlane.append(cc)                   
                            gongji_xia_good.append(enemy_guihua_goal_good[m])
                            kk=-1
                            continue
#++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++                        
           for m in range(len(enemy_guihua_goal)):
             if enemy_guihua_goal[m]["status"]!=2 :   ####不包含雾区 
               if kk==1 and pstUAV_we[i]["x"]==enemy_guihua_goal[m]["x"] and pstUAV_we[i]["y"]==enemy_guihua_goal[m]["y"] and enemy_guihua_goal[m]["z"]<pstUAV_we[i]["z"]:
                     if 1==pstUAV_we[i]["z"]:
                         FlyPlane.append(pstUAV_we[i])
                         kk=-1
                     else:
                         cc=pstUAV_we[i].copy()
                         cc["z"]=cc["z"]-1
                         FlyPlane.append(wjun_pengzhuang(FlyPlane,cc,pstfly_value_xiao))
                        #FlyPlane.append(cc)                   
                         gongji_xia_good.append(enemy_guihua_goal[m])
                         kk=-1
                         continue
               if kk==1 and pstUAV_we[i]["x"]==enemy_guihua_goal[m]["x"] and pstUAV_we[i]["y"]==enemy_guihua_goal[m]["y"] and enemy_guihua_goal[m]["z"]>pstUAV_we[i]["z"]:
                   cc=pstUAV_we[i].copy()
                   cc["z"]=cc["z"]+1
                   FlyPlane.append(cc)
                   gongji_xia_good.append(enemy_guihua_goal[m])
                   kk=-1          
###################################################################
    enemy_guihua_fly=[]     #  我方攻击飞机          
    for i in range(len(pstUAV_we)): 
        if  pstUAV_we[i]["no"] in qu_bianhao(FlyPlane):
            continue        
        if  pstUAV_we[i]["type"]==pstfly_value_xiao[0]["type"] and pstUAV_we[i]["z"]>=h_low and pstUAV_we[i]["status"]!=1:
                  enemy_guihua_fly.append(pstUAV_we[i])  #  我方攻击飞机
##################################################################### 
    enemy_fly_good=[]                             ###有货飞机攻击
    enemy_goal_good=[]
    for i in range(len(enemy_guihua_goal_good)):
         aa=10000 
         ee_fly=[]
         ee_goal=[]
         if  enemy_guihua_goal_good[i]["no"] in  qu_bianhao(gongji_xia_good):
                 continue 
         if  enemy_guihua_goal_good[i]["no"] in  qu_bianhao(enemy_goal_good):
                 continue
         for m in range(len(enemy_guihua_fly)):
              if  enemy_guihua_fly[m]["no"] in qu_bianhao(FlyPlane):
                 continue
              if  enemy_guihua_fly[m]["no"] in qu_bianhao(enemy_fly_good):
                 continue
              if 0<sqrt(((enemy_guihua_fly[m]["x"]-enemy_guihua_goal_good[i]["x"])**2+(enemy_guihua_fly[m]["y"]-enemy_guihua_goal_good[i]["y"])**2))<aa:
                 ee_fly.clear()
                 ee_goal.clear()
                 aa=sqrt(((enemy_guihua_fly[m]["x"]-enemy_guihua_goal_good[i]["x"])**2+(enemy_guihua_fly[m]["y"]-enemy_guihua_goal_good[i]["y"])**2))
                 
                 ee_fly.append(enemy_guihua_fly[m])
                 ee_goal.append(enemy_guihua_goal_good[i])
         if len(ee_fly)!=0:
           enemy_fly_good.append(ee_fly[0]) 
         if len(ee_goal)!=0:
           enemy_goal_good.append(ee_goal[0]) 
  
    FlyPlane_1  =  good_enemy_plan(FlyPlane,pstgoods,enemy_fly_good,enemy_goal_good,h_low,pstmap,h_Low_build)
    FlyPlane= FlyPlane + FlyPlane_1
####################################################################                                     
    enemy_fly=[]                              # 我方攻击无人机 列表
    enemy_goal=[]                             # 我方攻击目标列表
    for i in range(len(enemy_guihua_goal)):
        aa=10000 
        e_fly=[]
        e_goal=[]
        if  enemy_guihua_goal[i]["no"] in  qu_bianhao(gongji_xia_good):
               continue 
        if  enemy_guihua_goal[i]["no"] in  qu_bianhao(enemy_goal):
               continue
        for m in range(len(enemy_guihua_fly)):
             if  enemy_guihua_fly[m]["no"] in qu_bianhao(FlyPlane):
                 continue
             if  enemy_guihua_fly[m]["no"] in qu_bianhao(enemy_fly):
                 continue
             if  0<sqrt(((enemy_guihua_fly[m]["x"]-enemy_guihua_goal[i]["x"])**2+(enemy_guihua_fly[m]["y"]-enemy_guihua_goal[i]["y"])**2))<aa:
                 e_fly.clear()
                 e_goal.clear()
                 aa=sqrt(((enemy_guihua_fly[m]["x"]-enemy_guihua_goal[i]["x"])**2+(enemy_guihua_fly[m]["y"]-enemy_guihua_goal[i]["y"])**2))
                 
                 e_fly.append(enemy_guihua_fly[m])
                 e_goal.append(enemy_guihua_goal[i])
                 
        if len(e_fly)!=0:
           enemy_fly.append(e_fly[0]) 
        if len(e_goal)!=0:
           enemy_goal.append(e_goal[0])            
###############################################################################   bug  bug   bug   bug  bug 
    for i in range(len(enemy_fly)):    # 我方 攻击飞机  及我方攻击目标 计划
         if len(enemy_fly)!=len(enemy_goal):
             continue
         
         if enemy_fly[i]["z"]==h_low:    #攻击无人机 平移高度 h_low+1  避免撞击我方无人机 
             eee=enemy_fly[i]
             eee["z"]=enemy_fly[i]["z"]+1
             FlyPlane.append(eee)                         #@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@         
         if enemy_fly[i]["no"] in qu_bianhao(FlyPlane):
             continue
                  
         path_12 =  []
         star    = enemy_fly[i]
             
         end     = {"x":enemy_goal[i]["x"],"y":enemy_goal[i]["y"]} 
             
         path02=find_path(star,end,h_Low_build,pstmap)
         path12=path02[::-1]
         
         del path12[0]
         
         path_12.append(path12)
         
         enemy_fly[i]["x"]=path_12[0][0]["x"]
         enemy_fly[i]["y"]=path_12[0][0]["y"]
         
         path_12.clear()
         be=enemy_fly[i]
         #be=self_pengzhuang(enemy_fly[i],FlyPlane,pstUAV_we,pstMapInfo)
         FlyPlane.append(be)            #00000000000000000000000000000000000000000
##############################################################################################################
  
####################################################
    enemy_good=[]    ######   耗时间
    
    for m in range(len(enemy_guihua_goal)):                          #  判断货物 是否处在  地方正下降阶段
       for i in range(len(pstgoods)):
             if pstgoods[i]["status"]==0: 
               if pstgoods[i]["start_x"]==enemy_guihua_goal[m]["x"] and pstgoods[i]["start_y"]==enemy_guihua_goal[m]["y"] and enemy_guihua_goal[m]["z"]<=h_low:
                     enemy_good.append(pstgoods[i])
## # 现在可捡起的货物   
    for i in range(len(pstgoods)):
           if pstgoods[i]["no"] in qu_bianhao(enemy_good):
                 continue
           if pstgoods[i]["status"]==0 and pstgoods[i]["start_time"]<=pstMatchStatus["time"]+h_low+4 and pstgoods[i]["left_time"]>=h_low+1:   #@@@@@@@@@@
              pstgoods_kejian.append(pstgoods[i]) 
              
           if pstgoods[i]["status"]!=0:
              pstgoods_bu_kejian.append(pstgoods[i]) 
#######################################################################            
#### 到达最终目的地  下降 
    for i in range (len(pstUAV_we)):
          if pstUAV_we[i].get("no") in qu_bianhao(FlyPlane):
                  continue
          if pstUAV_we[i]["status"]!=3 and pstUAV_we[i]["goods_no"]!=-1 and pstUAV_we[i]["status"]!=1:
              for m in range(len(pstgoods_bu_kejian)):
                  if pstUAV_we[i]["goods_no"]==pstgoods_bu_kejian[m]["no"]:
                      if  pstUAV_we[i]["x"]==pstgoods_bu_kejian[m]["end_x"] and pstUAV_we[i]["y"]==pstgoods_bu_kejian[m]["end_y"]:
                          if pstUAV_we[i]["z"]!=0:
                             qq=pstUAV_we[i].copy()
                             qq["z"]=pstUAV_we[i]["z"]-1
                             qq=good_cost_dian(qq,pstgoods_bu_kejian[m])
                             FlyPlane.append(qq)          # 00000000000000000000000000000000000000000000000
#### 取货后运送
    guihua_fly_3=[]
    guihua_good_3=[]
    for i in range(len(pstUAV_we)):
        if pstUAV_we[i].get("no") in qu_bianhao(FlyPlane):
                continue
        if pstUAV_we[i]["status"]!=3 and pstUAV_we[i]["goods_no"]!=-1 and pstUAV_we[i]["z"]>=h_low and pstUAV_we[i]["status"]!=1:
            guihua_fly_3.append(pstUAV_we[i])
            for m in range(len(pstgoods_bu_kejian)):
                if pstUAV_we[i]["goods_no"]==pstgoods_bu_kejian[m]["no"]:
                   guihua_good_3.append(pstgoods_bu_kejian[m])
    for i in range(len(guihua_fly_3)): 
         if guihua_fly_3[i]["no"] in qu_bianhao(FlyPlane):
                      continue
         path_1=[]
         star = guihua_fly_3[i]
         end  = {"x":guihua_good_3[i]["end_x"],"y":guihua_good_3[i]["end_y"]}
  
         path01=find_path(star,end,h_Low_build,pstmap)
         path11=path01[::-1]
         
                       #防止把目的地 删除
         del path11[0]
         bb=guihua_fly_3[i].copy()
         path_1.append(path11)
         bb["x"]=path_1[0][0]["x"]
         bb["y"]=path_1[0][0]["y"]
         path_1.clear()

         #FlyPlane.append(guihua_fly_3[i])            #000000000000000000000000
         bc=self_pengzhuang(bb,FlyPlane,guihua_fly_3,pstMapInfo)
         bc=good_cost_dian(bc,guihua_good_3[i])
         FlyPlane.append(bc)       
               
########### 取货后上升              
    for i in range (len(pstUAV_we)):
       if pstUAV_we[i]["no"] in qu_bianhao(FlyPlane):
            continue        
       aa=[]
       if pstUAV_we[i]["status"]!=3 and pstUAV_we[i]["goods_no"]!=-1 and pstUAV_we[i]["z"]<h_low and pstUAV_we[i]["status"]!=1:
           aa=pstUAV_we[i]
           aa["z"]=aa["z"]+1 
           for m in range(len(pstgoods_bu_kejian)):
              if  pstUAV_we[i]["goods_no"]==pstgoods_bu_kejian[m]["no"]:
                  
                  aa["remain_electricity"]=aa["remain_electricity"]-pstgoods_bu_kejian[m]["weight"]
                  FlyPlane.append(aa) 
                  continue
            
                 ##@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@
###############################################################################
    guihua_fly_2=[]      #下降取货
    guihua_good_2=[]
    
    for i in range (len(pstUAV_we)):
        if  pstUAV_we[i]["no"] in qu_bianhao(FlyPlane):
                       continue
        if pstUAV_we[i]["status"]!=3 and pstUAV_we[i]["goods_no"]==-1 and pstUAV_we[i]["z"]<h_low and pstUAV_we[i]["status"]!=1:   #
            for m in range(len(pstgoods_kejian)):              
                if pstgoods_kejian[m]["weight"]<=Type_loadweight(pstUAV_we[i],pstUAV_price) :
                    if  pstUAV_we[i]["x"]==pstgoods_kejian[m]["start_x"] and pstUAV_we[i]["y"]==pstgoods_kejian[m]["start_y"] and pstUAV_we[i]["z"]<h_low:
                        guihua_fly_2.append(pstUAV_we[i])
                        guihua_good_2.append(pstgoods_kejian[m])
    for i in range(len( guihua_fly_2)):
           if  guihua_fly_2[i]["no"] in qu_bianhao(FlyPlane):
                       continue
           if  guihua_fly_2[i]["z"]>0:   
               ee=guihua_fly_2[i].copy()
               ee["z"]=guihua_fly_2[i]["z"]-1
              
               if ee["z"]==0:
                  ee["goods_no"]=guihua_good_2[i]["no"]
                 
                  ee["remain_electricity"]=ee["remain_electricity"]-guihua_good_2[i]["weight"]
                  FlyPlane.append(ee) 
               else:
                  FlyPlane.append(ee)
                                                    #00000000000000000000000000000000000                       
###############################################################################
    for i in range (len(pstUAV_we)):
         #所有可用 没载货的均参与规划
            if  pstUAV_we[i]["no"] in qu_bianhao(FlyPlane):
                  continue
            if  pstUAV_we[i]["no"] in qu_bianhao(guihua_fly_2) :
                 continue
            if  pstUAV_we[i]["no"] in qu_bianhao(guihua_fly_3) :
                  continue
            #if  pstUAV_we[i]["no"] in qu_bianhao(guihua_good_1):
                 # continue
            if pstUAV_we[i]["status"]!=1 and pstUAV_we[i]["goods_no"]==-1 and pstUAV_we[i]["z"]>=h_low : 
               zuihao_juli=10000
               zuihao_good=[]
               zuihao_fly=[]
               #zuihao_bizhong=10000
               zuihao_value=0
               zuihao=0
               
               
               pstgoods_kejian.sort(key=lambda x: -x["value"])   #从大到小
               
               for m in range(len(pstgoods_kejian)):
                 if  pstgoods_kejian[m]["no"] in qu_bianhao(guihua_good_2) :
                           continue              
                
                 if  pstgoods_kejian[m]["no"] in qu_bianhao(guihua_good_1):
                           continue          
                 if  pstgoods_kejian[m]["weight"]<=Type_loadweight(pstUAV_we[i],pstUAV_price) :
                     
                     
                     if  path_cost(pstUAV_we[i],pstgoods_kejian[m],h_Low_build,pstMapInfo):   #  判断电量是否可以任务
                           continue 
                     juli=juli_fly_good(pstUAV_we[i],pstgoods_kejian[m])
                     if juli==0:
                         juli=0.1
                     pingjia=pstgoods_kejian[m]["value"]/juli
                     if  pingjia > zuihao :
                         zuihao_good.clear()
                         zuihao_good.append(pstgoods_kejian[m])
                         zuihao_fly.clear()
                         zuihao_fly.append(pstUAV_we[i])
                         
                         zuihao_juli=juli_fly_good(pstUAV_we[i],pstgoods_kejian[m])
                         zuihao=pingjia
                         zuihao_value=pstgoods_kejian[m]["value"]
                         #zuihao_bizhong=abs(pstUAV_we[i]["load_weight"]-pstgoods_kejian[m]["weight"])
                         break
               if len(zuihao_fly)!=0:           ####  陷阱        
                  guihua_fly_1.append(zuihao_fly[0])
               if len(zuihao_good)!=0:
                  guihua_good_1.append(zuihao_good[0])


##########  飞机 到达目的地 下降取货#############################################            
    guihua_fly_21=[]    # 下降取货飞机 列表       防止 中途 遇见可栽货物  提前下降
    guihua_good_21=[]   # 下降取货货物 列表
    for i in range (len(guihua_fly_1)):    #   
        if  guihua_fly_1[i]["no"] in qu_bianhao(FlyPlane):
                       continue
        if  guihua_fly_1[i]["x"]==guihua_good_1[i]["start_x"] and guihua_fly_1[i]["y"]==guihua_good_1[i]["start_y"]:
                        guihua_fly_21.append(guihua_fly_1[i])
                        guihua_good_21.append(guihua_good_1[i])    
    for i in range(len( guihua_fly_21)):
           if  guihua_fly_21[i]["no"] in qu_bianhao(FlyPlane):
                       continue            
           if guihua_fly_21[i]["z"]>1:
              guihua_fly_21[i]["z"]=guihua_fly_21[i]["z"]-1
              FlyPlane.append(guihua_fly_21[i])   #@@@@@@@@@@@@@@@@@           
###########################################################################
    k=1
    for i in range (len(pstUAV_we)):         
          #所有可用 没载货  但不在规划中                
          if pstUAV_we[i]["no"] in qu_bianhao(FlyPlane):
                  continue
          if pstUAV_we[i]["no"] in qu_bianhao(guihua_fly_1):
                  continue
          if pstUAV_we[i]["no"] in qu_bianhao(guihua_fly_2):          
                  continue
          if pstUAV_we[i]["status"]!=1 and pstUAV_we[i]["goods_no"]==-1 and pstUAV_we[i]["z"]>=h_low :
   
              ww=pstUAV_we[i]
              if ww["z"]<h_high and pstUAV_we[i]["x"]!=pstparking["x"] and pstUAV_we[i]["y"]!=pstparking["y"]:
                       
                 ww["z"]=pstUAV_we[i]["z"]+1
                 FlyPlane.append(ww)                    #0000000000000000000000000000000000000000000000000000000000000
                 #FlyPlane.append(self_pengzhuang(ww,FlyPlane,pstUAV_we,pstMapInfo))
              #if ww["z"]==h_high and pstUAV_we[i]["x"]!=pstparking["x"] and pstUAV_we[i]["y"]!=pstparking["y"]: 
              else:                               #!!!!!!! else 和又一个 if 有区别？？？？
                  z1,g1=Type_dianliang(pstUAV_we[i],pstUAV_price)
                  pstUAV_price.sort(key=lambda x: -x['load_weight'])     # 按载重从da到小 排序 
                  pstfly_load_da=pstUAV_price
                  if pstUAV_we[i]["remain_electricity"]<=z1/5 and pstUAV_we[i]["type"]==pstfly_load_da[0]["type"] or pstUAV_we[i]["type"]==pstfly_load_da[1]["type"]:
                      if k==1:

                         w1=return_parking(ww,h_Low_build,pstMapInfo,FlyPlane,pstfly_value_xiao)
                         k=0
                      else:
                         w1=ww 
                  else:
                      w1=ww    #注意 充满电的 也会在这
                  FlyPlane.append(w1)                   #0000000000000000000000000000000000000000000000000000000000000
                 #FlyPlane.append(self_pengzhuang(w1,FlyPlane,pstUAV_we,pstMapInfo))
                  continue
          if pstUAV_we[i]["status"]!=1 and pstUAV_we[i]["goods_no"]==-1 and 0<pstUAV_we[i]["z"]<h_low and  pstUAV_we[i]["x"]==pstparking["x"] and pstUAV_we[i]["y"]==pstparking["y"]:
              zz,gg=Type_dianliang(pstUAV_we[i],pstUAV_price) 
              if pstUAV_we[i]["remain_electricity"]<zz and pstUAV_we[i]["type"]!=pstfly_value_xiao[0]["type"]  : 
                   wq=pstUAV_we[i].copy()
                   wq1=return_parking(wq,h_Low_build,pstMapInfo,FlyPlane,pstfly_value_xiao)
                   if wq1["z"]==0:
                      if zz<=wq1["remain_electricity"]+gg:
                         wq1["remain_electricity"]=zz
                      
                      else:
                          wq1["remain_electricity"]=wq1["remain_electricity"]+gg
                   
                   FlyPlane.append(wq1)                   #0000000000000000000000000000000000000000000000000000000000000
#########################################################################################
               
    for i in range(len(guihua_fly_1)):
         if  guihua_fly_1[i]["z"]>h_low:
             aa=guihua_fly_1[i].copy()
             
             aa["z"]=guihua_fly_1[i]["z"]-1
             self_xia_peng(aa,FlyPlane,pstMapInfo)
             FlyPlane.append(aa)
             #FlyPlane.append(self_pengzhuang(aa,FlyPlane,pstUAV_we,pstMapInfo))
         if  guihua_fly_1[i]["no"] in qu_bianhao(FlyPlane):
              continue
         if  guihua_fly_1[i]["no"] in qu_bianhao(guihua_fly_21):
              continue 
         path_lujing=[]
         star = guihua_fly_1[i].copy()
         end  = {"x":guihua_good_1[i]["start_x"],"y":guihua_good_1[i]["start_y"]}
  
         path0=find_path(star,end,h_Low_build,pstmap)
         path1=path0[::-1]
                              #防止把目的地 删除
         del path1[0]
         
         path_lujing.append(path1)
         
         er=guihua_fly_1[i].copy()
         
         er["x"]=path_lujing[0][0]["x"]
         er["y"]=path_lujing[0][0]["y"]

         path_lujing.clear()
      
         er=self_pengzhuang(er,FlyPlane,guihua_fly_1,pstMapInfo)
         FlyPlane.append(er)
          
        # FlyPlane.append(er)    #000000000000000000000000000000000000000000000000000000000000000000000
     
####################################################################################################
    #keguihua_good=()   #统计 所有 还未规划 的货物 决定 停机坪飞机是否 起飞
    
    kefei_fly_,FlyPlane_=kefei_fly(pstUAV_we,pstMapInfo,enemy_goal,enemy_fly,FlyPlane) 
    FlyPlane= FlyPlane + FlyPlane_  
    
    ke=1
    for i in range(len(pstUAV_we)):
        if pstUAV_we[i]["no"] in qu_bianhao(FlyPlane):
                  continue        
        if pstUAV_we[i]["status"]!=1 and pstUAV_we[i]["x"]==pstparking["x"] and pstUAV_we[i]["y"]==pstparking["y"] and pstUAV_we[i]["z"]<h_low : 
            #等于1  为坠毁  停机坪 飞机（出生  购买）
            if  pstUAV_we[i]["z"]!=0 :
                aa1=pstUAV_we[i].copy()
                aa1["z"]=pstUAV_we[i]["z"]+1
                FlyPlane.append(aa1)          #000000000000000000000000000000000000000000000000000000000000000
                #FlyPlane.append(self_pengzhuang(aa,FlyPlane,pstUAV_we,pstMapInfo))
            if  ke==1 and pstUAV_we[i]["z"]==0:
             if pstUAV_we[i]["no"] in qu_bianhao(kefei_fly_):
                  
                aa=pstUAV_we[i].copy()
                aa["z"]=pstUAV_we[i]["z"]+1
                ke=0
                FlyPlane.append(aa)          #000000000000000000000000000000000000000000000000000000000000000
                #FlyPlane.append(self_pengzhuang(aa,FlyPlane,pstUAV_we,pstMapInfo))
                
    for  i in range(len(pstUAV_we)):    #  送完后  上升阶段
       if pstUAV_we[i]["no"] in qu_bianhao(FlyPlane):
                  continue
       aa=[]
       if pstUAV_we[i]["status"]!=1 and pstUAV_we[i]["goods_no"]==-1 and pstUAV_we[i]["z"]<h_low :
           aa=pstUAV_we[i].copy()
           aa["z"]=aa["z"]+1
           FlyPlane.append(aa)
#############################################################################################################################################
    return FlyPlane
            
            
    
        
        
      
            
                
                
                
            
           
            
            
        
            
           
    
    
    
    
    
    
    
    