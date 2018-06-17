# -*- coding: utf-8 -*-
"""
Created on Thu May 17 15:55:32 2018

@author: bangwei
"""

# -*- coding: utf-8 -*-
"""
Created on Mon May 14 16:20:28 2018

@author: bangwei
"""

# -*- coding: utf-8 -*-
"""
Created on Thu May 17 20:05:21 2018

@author: bangwei
"""
import math
import matplotlib.pyplot as plt
import matplotlib.patches as patches

#测试 A 算法函数
class Node_Elem:

    """
开放列表和关闭列表的元素类型，parent用来在成功的时候回溯路径
    """
    def __init__(self, parent, x, y, dist):

       self.parent = parent

       self.x = x

       self.y = y

       self.dist = dist

class A_Star:

    """
    A星算法实现类
    """

    #注意w,h两个参数，如果你修改了地图，需要传入一个正确值或者修改这里的默认参数
    def __init__(self, s_x, s_y, e_x, e_y,build,width, length):

       self.s_x = s_x

       self.s_y = s_y

       self.e_x = e_x

       self.e_y = e_y

       self.width = width

       self.length = length
       
       self.open = []

       self.close = []

       self.path = []
       self.build=build

    #查找路径的入口函数

    def find_path(self):

       #构建开始节点

       p = Node_Elem(None, self.s_x, self.s_y, 0.0)

       while True:

           #扩展F值最小的节点

           self.extend_round(p)

           #如果开放列表为空，则不存在路径，返回

           if not self.open:

               return

            #获取F值最小的节点

           idx, p = self.get_best()

            #找到路径，生成路径，返回

           if self.is_target(p):

               self.make_path(p)

               return

            #把此节点压入关闭列表，并从开放列表里删除

           self.close.append(p)

           del self.open[idx]
##############################################################
    def make_path(self,p):

        #从结束点回溯到开始点，开始点的parent == None

       while p:

           self.path.append({"x":p.x,"y":p.y})

           p = p.parent



    def is_target(self, i):

       return i.x == self.e_x and i.y == self.e_y
############################################################

    def get_best(self):

       best = None

       bv = 1000000 #如果你修改的地图很大，可能需要修改这个值

       bi = -1

       for idx, i in enumerate(self.open):

           value = self.get_dist(i)     #获取F值

           if value < bv:#比以前的更好，即F值更小

               best = i

               bv = value

               bi = idx

       return bi, best
##########################################################
       
    def get_dist(self, i):

       # F = G + H

       # G 为已经走过的路径长度， H为估计还要走多远

       # 这个公式就是A*算法的精华了。

       return i.dist + math.sqrt(

           (self.e_x-i.x)*(self.e_x-i.x)

           + (self.e_y-i.y)*(self.e_y-i.y))*1.2
#########################################################

    def extend_round(self, p):

       #可以从8个方向走

       xs = (-1, 0, 1, -1, 1, -1, 0, 1)

       ys = (-1,-1,-1,  0, 0,  1, 1, 1)

       #只能走上下左右四个方向

       #xs = (0, -1, 1, 0)

       #ys = (-1, 0, 0, 1)

       for x, y in zip(xs, ys):

           new_x, new_y = x + p.x, y + p.y

            #无效或者不可行走区域，则勿略
       
           if  self.is_in_build(new_x, new_y):

               continue

           #构造新的节点

           node = Node_Elem(p, new_x, new_y, p.dist+self.get_cost(

                       p.x, p.y, new_x, new_y))

           #新节点在关闭列表，则忽略

           if self.node_in_close(node):

               continue

           i = self.node_in_open(node)

           if i != -1:

               #新节点在开放列表

               if self.open[i].dist > node.dist:

                   #现在的路径到比以前到这个节点的路径更好~

                   #则使用现在的路径

                   self.open[i].parent = p

                   self.open[i].dist = node.dist

               continue

           self.open.append(node)
############################################################

    def get_cost(self, x1, y1, x2, y2):

       """
上下左右直走，代价为1.0，斜走，代价为1.4
        """
       if x1 == x2 or y1 == y2:

           return 1.0

       return 1.4
####################################################

    def node_in_close(self, node):

       for i in self.close:

           if node.x == i.x and node.y == i.y:

               return True

       return False
####################################################

    def node_in_open(self, node):

       for i, n in enumerate(self.open):

           if node.x == n.x and node.y == n.y:

               return i

       return -1
    def is_in_build(self,x,y):
        if x < 0 or x >= self.width or y < 0 or y >= self.length:

           return True
        for i in range(len(self.build)):
            
            b0_x=self.build[i]["x"]
            b0_y=self.build[i]["y"]
            
            b2_x=self.build[i]["x"]+self.build[i]["l"]-1
            b2_y=self.build[i]["y"]+self.build[i]["w"]-1
            
            if x >=b0_x and x <= b2_x and y >= b0_y and y <= b2_y:
               return True  
##########################################################################################

def find_path(star,end,build,pstmap):

   s_x, s_y = star["x"],star["y"]      # 起点坐标

   e_x, e_y = end["x"],end["y"]  # 终点坐标
   build=build
   
   width=pstmap["x"]
   length=pstmap["y"]
   
   a_star = A_Star(s_x, s_y, e_x, e_y,build,width,length)

   a_star.find_path()

   #searched = a_star.get_searched()

   path = a_star.path 
   #mark_path(path)
   return path
 #  print_path(path)
def print_path(l):
    
      for x,y in l:
          print((x,y),end='>')


###############################################################
if __name__ == "__main__":

    #把字符串转成列表


   find_path(star,end,build,pstMapInfo)
  