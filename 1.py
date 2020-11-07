import pygame 
import math 
from queue import PriorityQueue

width = 800
win = pygame.display.set_mode((width,width))
pygame.display.set_caption("Path finding algo")

Aqua	= (0,255,255)           #start
Magenta = (255,0,255)           #end
Silver	= (192,192,192)         #grid default
Gray	= (128,128,128)         #grid
Maroon	= (128,0,0)             #closed
Black	= (0,0,0)               #barrier
Green	= (0,128,0)             #open
Purple	= (128,0,128)           #path
Teal	= (0,128,128)
Navy	= (0,0,128)

class node:
    def __init__(self,row, col, width, total_rows):
        self.row = row
        self.col = col
        self.width = width
        self.x = row*width
        self.y = col*width
        self.neighbour =[]
        self.color = Silver
        self.total_rows= total_rows

    def get_pos(self):
        return self.row,self.col
    
    def is_closed(self):
        return self.color == Maroon
    
    def is_open(self):
        return self.color == Green

    def is_barrier(self):
        return self.color == Black
    
    def is_start(self):
        return self.color == Aqua
    
    def is_end(self):
        return self.color == Magenta

    def reset(self):
        self.color = Silver
    
    def make_closed(self):
        self.color = Maroon
    
    def make_open(self):
        self.color = Green

    def make_barrier(self):
        self.color = Black
    
    def make_start(self):
        self.color = Aqua
    
    def make_end(self):
        self.color = Magenta

    def make_path(self):
        self.color = Purple

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x,self.y,self.width,self.width))

    def update_next(self):
        pass

    def __it__(self):
        pass

def h(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2)+abs(y1-y2)

def reconstruct_path():
    pass

def algo():
    pass

def make_grid(rows,width):
    grid=[]
    gap = width//rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            Node = node(i, j, gap, rows)
            grid[i].append(Node)
    return grid

def draw_grid(win,rows,width):
    gap = width//rows
    for i in range(rows):
        pygame.draw.line(win,Gray, (0, gap*i), (width, gap*i))
    for i in range(rows): 
        pygame.draw.line(win,Gray, (gap*i,0), (gap*i, width))

def draw(win, grid, rows, width):
    win.fill(Silver)
    for row in grid:
        for node in row:
            node.draw(win)
    
    draw_grid(win,rows, width)
    pygame.display.update()

def get_clicked(pos, rows, width):
    
    gap = width//rows
    y,x = pos
    row = y//gap
    col = x//gap
    return row,col


def main(win, width):
    rows= 50
    grid = make_grid(rows,width)

    start = None 
    end = None
    run =True
    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            
            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row,col = get_clicked(pos, rows, width)
                Node = grid[row][col]
                if not start and Node!=end:
                    start = Node
                    start.make_start()

                elif not end and Node!=start:
                    end = Node
                    end.make_end()

                elif Node!=start and Node!=end:
                    Node.make_barrier()
                
            elif pygame.mouse.get_pressed()[2]:
                pos =pygame.mouse.get_pos()
                row,col = get_clicked(pos, rows, width)
                node = grid[row][col]            
                node.reset()
                if node == start:
                    start= None
                elif node == end:
                    end = None

            if event.type == pygame.KEYDOWN     :
                if event.key == pygame.K_SPACE and start and end:

                    for row in grid:
                        for node in grid:
                            node.update_next(grid)
    pygame.quit()

main(win, width)
