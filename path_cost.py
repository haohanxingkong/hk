# -*- coding: utf-8 -*-
"""
Created on Thu Jun  7 09:27:23 2018

@author: bangwei
"""
from A_STAR_xiugai import*
import sys
def path_cost(fly,good,h_Low_build,pstMapInfo):   #  判断 飞机剩余燃料 是否可以支撑 货物运送
    
########################################################################    
    pstmap      =pstMapInfo["map"]
    h_low       =pstMapInfo["h_low"]
    
    
    part1=h_low   #取货后上升
    
    part2=[]      #取货后平移
    
    star = {"x":good["start_x"],"y":good["start_y"]}
    end  = {"x":good["end_x"],"y":good["end_y"]}
    path_pingyi=find_path(star,end,h_Low_build,pstmap)   
    
    part2=len(path_pingyi)
    
    part3=h_low   #  到目的地  下降送货
    
    path_cost=part1+part2+part3
    
    if path_cost*good["weight"]>fly["remain_electricity"]:
        return True
    else:
        
        return False 


    
def return_parking(fly,h_Low_build,pstMapInfo,FlyPlane,pstfly_value_xiao):
    h_high      =pstMapInfo["h_high"]
    def return_parking_pengzhuang(now,FlyPlane,fly,pstfly_value_xiao,h_high):

       for i in range(len(FlyPlane)):
          if now["x"]==FlyPlane[i]["x"] and now["y"]==FlyPlane[i]["y"] and now["z"]==FlyPlane[i]["z"] :
                 now=fly
                 
       return now
    path_lujing=[]
    pstparking  =pstMapInfo["parking"]
    pstmap      =pstMapInfo["map"]   #初始化地图 寻路要用
    star = fly
    end  = {"x":pstparking["x"],"y":pstparking["y"]}
    er=fly
    if fly["x"]!=pstparking["x"] or fly["y"]!=pstparking["y"] :
       path_1=find_path(star,end,h_Low_build,pstmap)
       path_2=path_1[::-1]
    
       del path_2[0]
        
       path_lujing.append(path_2)
          
       er["x"]=path_lujing[0][0]["x"]
       er["y"]=path_lujing[0][0]["y"]
       path_lujing.clear()
       #FlyPlane.append(return_parking_pengzhuang)
       
       
    #if fly["x"]==pstparking["x"] and fly["y"]==pstparking["y"] :
    else:
        if fly["z"]>0:
             er["z"]=er["z"]-1
        
    return return_parking_pengzhuang(er,FlyPlane,fly,pstfly_value_xiao,h_high)   #####  千万 要注意  返回的量  肯能是 None 造成 typenone 错误

def good_cost_dian(fly,good):
    if fly["goods_no"]!=-1:
       fly["remain_electricity"]=fly["remain_electricity"]-good["weight"]
    return fly