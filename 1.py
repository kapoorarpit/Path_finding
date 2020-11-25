import pygame 
import math 
from queue import PriorityQueue

width = 800
WIN = pygame.display.set_mode((width,width))
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

    def update_next(self,grid):
        self.neighbours=[]
        if self.row < self.total_rows -1 and not grid[self.row+1][self.col].is_barrier(): #Down
            self.neighbour.append(grid[self.row+1][self.col])
        if self.row > 0 and not grid[self.row-1][self.col].is_barrier():                   #Up
            self.neighbour.append(grid[self.row-1][self.col])
        if self.col < self.total_rows -1 and not grid[self.row][self.col+1].is_barrier():  #right
            self.neighbour.append(grid[self.row][self.col+1])
        if self.col >0 and not grid[self.row][self.col-1].is_barrier():                    #left
            self.neighbour.append(grid[self.row][self.col-1])    
        
    def __it__(self,other):
        return False

def h(p1,p2):
    x1,y1=p1
    x2,y2=p2
    return abs(x1-x2)+abs(y1-y2)

def reconstruct_path(from1,current, draw):
    while current in from1:
        current= from1[current]
        current.make_path()
        draw()
    

def algo(draw, grid, start, end):
    count =0
    set1 = PriorityQueue()
    set1.put((0, count, start))
    from1 ={}
    g_score = {node: float("inf") for row in grid for node in row}
    g_score[start] = 0                               #g score is the distance of start node to node we are talking about  
    f_score = {node: float("inf") for row in grid for node in row}
    f_score = h(start.get_pos(), end.get_pos())      #f score is the manhattan distance from current node to end  

    set1_hash ={start}

    while not set1.empty():
        for event in pygame.event.get():
            if event.type() == pygame.QUIT:
                pygame.quit()

        current = set1.get()[2]
        set1_hash.remove(current)

        if current == end:
            reconstruct_path(from1, end, draw)
            end.make_end()
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current]+1

            if temp_g_score < g_score[neighbour]:
                from1[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = g_score[neighbour] + h(neighbour.get_pos(),end.get_pos())
                if neighbour not in set1_hash:
                    count+=1
                    set1.put((f_score[neighbour], count, neighbour))
                    set1_hash.add(neighbour)
                    neighbour.make_open()

        draw()

        if current!= start:
            current.make_closed()

    return False 

         
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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_next(grid)
                            
                algo(lambda: draw(win, grid, rows, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = make_grid(rows, width)
    
    pygame.quit()

main(WIN, width)
