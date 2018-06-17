# -*- coding: utf-8 -*-
"""
Created on Fri May 25 22:22:03 2018

@author: bangwei
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 24 21:53:07 2018

@author: bangwei
"""
import sys
#######购买飞机  策略  分类  按比例购买

def purchasefly(pstMapInfo, pstMatchStatus):
    purchase_plane=[]
    pstUAV_price=pstMapInfo["UAV_price"]
    
    pstUAV_we=pstMatchStatus["UAV_we"]
    pstgoods=pstMatchStatus["goods"]
    we_value=pstMatchStatus["we_value"]
    pstUAV_enemy=pstMatchStatus["UAV_enemy"]
    
    
    pstfly_load_xiao=[]
    pstfly_load_da=[]
    
    goods_keguihua=[]
    for i in range(len(pstgoods)):
       if  pstgoods[i]["status"]==0: 
           goods_keguihua.append(pstgoods[i])
    
    
    pstUAV_price.sort(key=lambda x: x['load_weight']) 
    pstfly_load_xiao=pstUAV_price                                             # 按载重从小到大 排序 
    
##########################################################
    
    def qu_bianhao(zidian):    #取编号
        result=[]                  
        for i in range(len(zidian)):
           result.append(zidian[i]["type"])
        return result 

#######################################################
    pstUAV_price.sort(key=lambda x: x['value'])
    pstfly_value_xiao=pstUAV_price
    ab=0  
    for i in range(len(pstUAV_enemy)):
        if pstUAV_enemy[i]["status"]!=1:
            ab=ab+1                      #  敌军在役 飞机总数
    cd=0
    for i in range(len(pstUAV_we)):
      
        if  pstUAV_we[i]["type"]==pstfly_value_xiao[0]["type"] and pstUAV_we[i]["status"]!=1:
               cd=cd+1                    #  我军在役 最烂无人机数
        
    while ab > cd:
       if  we_value <pstfly_value_xiao[0]["value"]:      # 购买最烂无人机  攻击敌军  保卫我军
            break
       
       if  we_value >= pstfly_value_xiao[0]["value"]:
           aa={"purchase": pstfly_value_xiao[0]["type"]}
           purchase_plane.append(aa)
           we_value=we_value-pstfly_value_xiao[0]["value"]
           cd=cd+1
#########################################################            
    pstUAV_price.sort(key=lambda x: -x['load_weight'])     # 按载重从da到小 排序 
    pstfly_load_da=pstUAV_price
#最重飞机  购买      
    cc=0
    bb=0
    
    for i in range(len(pstgoods)):
        if  pstfly_load_da[1]["load_weight"]< pstgoods[i]["weight"] <=pstfly_load_da[0]["load_weight"]:   
               cc=cc+1
    if  3<=cc:
          for m in range(len(pstUAV_we)):
                 if pstUAV_we[m]["type"]==pstfly_load_da[0]["type"]:
                         bb=bb+1
                         if cc/3 > bb:
                             if we_value >=pstfly_load_da[0]["value"]:
                                
                                 aa={"purchase":pstfly_load_da[0]["type"]}
                                 purchase_plane.append(aa)
                                 we_value=we_value-pstfly_load_da[0]["value"]
#第二重飞机  购买    
    cc=0
    bb=0
    
    for i in range(len(pstgoods)):
        if  pstfly_load_da[2]["load_weight"]< pstgoods[i]["weight"] <=pstfly_load_da[1]["load_weight"]:   
                     cc=cc+1
    if 4<=cc:
          for m in range(len(pstUAV_we)):
               if pstUAV_we[m]["type"]==pstfly_load_da[1]["type"]:
                       bb=bb+1
                       if cc/4 > bb:
                             if we_value >=pstfly_load_da[1]["value"]:
                                
                                 aa={"purchase":pstfly_load_da[1]["type"]}
                                 purchase_plane.append(aa)
                                 we_value=we_value-pstfly_load_da[1]["value"]
#第3重飞机  购买    
    
    if len(pstfly_load_da)>=4:
        cc=0
        bb=0
        for i in range(len(pstgoods)):
           if  pstfly_load_da[3]["load_weight"]< pstgoods[i]["weight"] <=pstfly_load_da[2]["load_weight"]:   
                     cc=cc+1
        if 4<=cc:
             for m in range(len(pstUAV_we)):
                  if pstUAV_we[m]["type"]==pstfly_load_da[2]["type"]:
                        bb=bb+1
                        if cc/4 > bb:
                             if we_value >=pstfly_load_da[2]["value"]:
                                
                                 aa={"purchase":pstfly_load_da[2]["type"]}
                                 purchase_plane.append(aa)
                                 we_value=we_value-pstfly_load_da[2]["value"]
#第4重飞机  购买  
    if len(pstfly_load_da)>=5:
       cc=0
       bb=0
    
       for i in range(len(pstgoods)):
            if  pstfly_load_da[4]["load_weight"]< pstgoods[i]["weight"] <=pstfly_load_da[3]["load_weight"]:   
                     cc=cc+1
       if 5<=cc:
           for m in range(len(pstUAV_we)):
                if pstUAV_we[m]["type"]==pstfly_load_da[3]["type"]:
                     bb=bb+1
                     if cc/5 > bb:
                             if we_value >=pstfly_load_da[3]["value"]:
                                
                                 aa={"purchase":pstfly_load_da[3]["type"]}
                                 purchase_plane.append(aa)
                                 we_value=we_value-pstfly_load_da[3]["value"] 
#第5重飞机  购买  
    if len(pstfly_load_da)>=6:
       cc=0
       bb=0
    
       for i in range(len(pstgoods)):
            if  pstfly_load_da[5]["load_weight"]< pstgoods[i]["weight"] <=pstfly_load_da[4]["load_weight"]:   
                     cc=cc+1
       if 5<=cc:
           for m in range(len(pstUAV_we)):
                if pstUAV_we[m]["type"]==pstfly_load_da[4]["type"]:
                     bb=bb+1
                     if cc/5 > bb:
                             if we_value >=pstfly_load_da[4]["value"]:
                                
                                 aa={"purchase":pstfly_load_da[4]["type"]}
                                 purchase_plane.append(aa)
                                 we_value=we_value-pstfly_load_da[4]["value"]                                  
########################################################################    
    return  purchase_plane   
