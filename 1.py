import pygame 
import math 
from queue import PriorityQueue

length = 1000
play = pygame.display.set_mode((length,length))
pygame.display.set_caption("Path finding algo")

Aqua	= (0,255,255)
Magenta = (255,0,255)
Silver	= (192,192,192)
Gray	= (128,128,128)
Maroon	= (128,0,0)             #closed
Olive	= (128,128,0)
Green	= (0,128,0)
Purple	= (128,0,128)
Teal	= (0,128,128)
Navy	= (0,0,128)

class node:
    def __init__(self,row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.x = row*width
        self.y = row*width
        self.neighbour =[]
        self.color = Silver
        self.total_rows= total_rows

    def get_pos(self):
        return self.row,self.col
    
    def closed(self):
        return self.color == Maroon
    
    def open(self):
        return self.color == Green
        