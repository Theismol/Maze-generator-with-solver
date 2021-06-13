import pygame
import random
from queue import PriorityQueue
from pygame.font import Font
WIDTH, HEIGHT = 801, 601
WIN = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Maze generation")
pygame.font.init()
BLACK = (0,0,0)
WHITE = (255,255,255)
GREY = (128,128,128)
LIGHTGREY = (211,211,211)
YELLOW = (255,255,50)
GREEN = (0,255,0)
BLUE = (0,0,255)
PURPLE = (230,200,250)
PINK = (255,192,203)
OTHERPINK = (255,150,150)
textFont = pygame.font.Font("freesansbold.ttf",20)
resetText = textFont.render("Reset",True,BLACK)
searchText = textFont.render("Find path",True,BLACK)
mazeText = textFont.render("Create maze",True,BLACK)
visualizeText = textFont.render("Visualize:",True,BLACK)
visualizeoff = textFont.render("off",True,BLACK)
visualizeon = textFont.render("on",True,BLACK)
resetButton = pygame.Rect((801-160+10),100,60,20)
algorithmButton = pygame.Rect((801-160+10),200,100,20)
mazeButton = pygame.Rect((801-160+10),300,130,20)
visualizeButton = pygame.Rect((801-160+10),400,130,20)
class Node():

    def __init__(self,row,col,width,rowsInTotal,colsInTotal):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.width = width
        self.iswall = [True,True,True,True]
        self.isvisited = False
        self.color = GREY
        self.rows = rowsInTotal
        self.cols = colsInTotal
        self.startNode = False
        self.endNode = False
        self.isvisitedSearch = False
    def getPos(self):
	    return self.row, self.col
    def draw(self,win):
        if self.startNode == True:
            self.color = BLUE
            pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
        elif self.endNode == True:
            self.color = GREEN
            pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
        else:
            pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
        if self.iswall[0] == True: #Upper wall
            pygame.draw.line(win,BLACK,(self.x,self.y),(self.x + self.width,self.y))
        if self.iswall[1] == True: #Lower wall
            pygame.draw.line(win,BLACK,(self.x,self.y + self.width),(self.x + self.width,self.y + self.width))
        if self.iswall[2] == True: #Left wall
            pygame.draw.line(win,BLACK,(self.x,self.y),(self.x,self.y + self.width))
        if self.iswall[3] == True: #Right wall
            pygame.draw.line(win,BLACK,(self.x + self.width,self.y),(self.x + self.width,self.y + self.width))
    def makePath(self):
        self.color = YELLOW
    def makeOpen(self):
        self.color = PURPLE
    def createNeighbors(self,grid):
        self.neighbors = []
        if self.col > 0 and grid[self.row][self.col - 1].isvisited == False: # UP
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < self.cols -1 and grid[self.row][self.col + 1].isvisited == False: # DOWN 
            self.neighbors.append(grid[self.row][self.col + 1])
        if self.row > 0 and grid[self.row - 1][self.col].isvisited == False: # LEFT
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < self.rows -1 and grid[self.row + 1][self.col].isvisited == False: # RIGHT
            self.neighbors.append(grid[self.row + 1][self.col])
    def createNeighborsSearch(self,grid):
        self.neighborsSearch = []
        if self.col > 0 and grid[self.row][self.col - 1].isvisitedSearch == False and self.iswall[0] == False: # UP
            self.neighborsSearch.append(grid[self.row][self.col - 1])
        if self.col < self.cols -1 and grid[self.row][self.col + 1].isvisitedSearch == False and self.iswall[1] == False: # DOWN 
            self.neighborsSearch.append(grid[self.row][self.col + 1])
        if self.row > 0 and grid[self.row - 1][self.col].isvisitedSearch == False and self.iswall[2] == False: # LEFT
            self.neighborsSearch.append(grid[self.row - 1][self.col])
        if self.row < self.rows -1 and grid[self.row + 1][self.col].isvisitedSearch == False and self.iswall[3] == False: # RIGHT
            self.neighborsSearch.append(grid[self.row + 1][self.col])
    
def hCost(pos1,pos2):
    x1, y1 = pos1
    x2, y2 = pos2
    return (abs(x1-x2) + abs(y1-y2))
def createShortestPath(childParentNodes,currentNode,grid):
    while currentNode in childParentNodes:
        currentNode = childParentNodes[currentNode]
        currentNode.makePath()
        draw(grid)
def AStarAlgorithm(grid,startNode,endNode,visualize):
    count = 0
    openQueue = PriorityQueue()
    openQueue.put((0,count,startNode))
    childParentNodes = {}
    gCost = {node:float("inf") for row in grid for node in row}
    gCost[startNode] = 0
    fCost = {node:float("inf") for row in grid for node in row}
    fCost[startNode] = hCost(startNode.getPos() , endNode.getPos())
    openQueueHash = {startNode}
    while not openQueue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        currentNode = openQueue.get()[2] #Takes the node out of the queue
        openQueueHash.remove(currentNode)

        if currentNode == endNode:
            createShortestPath(childParentNodes,endNode,grid)
            endNode.endNode == True
            startNode.startNode == True
            return True
        for neighborNode in currentNode.neighborsSearch:
            newgCost = gCost[currentNode] + 1
            if newgCost < gCost[neighborNode]:
                childParentNodes[neighborNode] = currentNode
                gCost[neighborNode] = newgCost
                fCost[neighborNode] = newgCost + hCost(neighborNode.getPos(), endNode.getPos())
                if neighborNode not in openQueueHash:
                    count += 1
                    openQueue.put((fCost[neighborNode],count,neighborNode))
                    openQueueHash.add(neighborNode)
                    if visualize:
                        currentNode.makeOpen()
        if visualize:
            draw(grid)
def mazeGeneration(grid,visualize):
    stack = []
    randomrow = random.randint(1,len(grid)-1)
    randomnode = random.randint(1,len(grid[0])-1)
    currentNode = grid[randomrow][randomnode]
    currentNode.isvisited = True
    stack.append(currentNode)
    while len(stack) > 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        currentNode = stack.pop()
        currentNode.createNeighbors(grid)
        for neighbor in currentNode.neighbors:
            if currentNode not in stack:
                if neighbor.isvisited == False:
                    stack.append(currentNode)
                    nextNode = random.choice(currentNode.neighbors)
                    if currentNode.col > 0:
                        if nextNode == grid[currentNode.row][currentNode.col - 1]: #UP
                            currentNode.iswall[0] = False
                            nextNode.iswall[1] = False
                    if currentNode.col < currentNode.cols - 1:
                        if nextNode == grid[currentNode.row][currentNode.col + 1]: #DOWN
                            currentNode.iswall[1] = False
                            nextNode.iswall[0] = False
                    if currentNode.row > 0:
                        if nextNode == grid[currentNode.row - 1][currentNode.col]: #LEFT
                            currentNode.iswall[2] = False
                            nextNode.iswall[3] = False
                    if currentNode.row < currentNode.rows -1:
                        if nextNode == grid[currentNode.row + 1][currentNode.col]: #RIGHT
                            currentNode.iswall[3] = False
                            nextNode.iswall[2] = False
                    nextNode.isvisited = True
                    stack.append(nextNode)
                    break
        if visualize:
            draw(grid)
            pygame.draw.rect(WIN,"red",(currentNode.x,currentNode.y,currentNode.width,currentNode.width))
            pygame.display.update()
def mousePosition(pos,width):
    x, y = pos
    col = int(y / width)
    row = int(x / width)
    return row, col
def createGrid(row,col,width):
    grid = []
    for i in range(row):
        grid.append([])
        for j in range(col):
            node = Node(i,j,width,row,col)
            grid[i].append(node)
    return grid
def drawbuttons(hoverpos,visualize):
    WIN.fill(LIGHTGREY)
    pygame.draw.rect(WIN,PINK,resetButton)
    pygame.draw.rect(WIN,PINK,algorithmButton)
    pygame.draw.rect(WIN,PINK,mazeButton)
    pygame.draw.rect(WIN,PINK,visualizeButton)
    if hoverpos:
        if resetButton.collidepoint(hoverpos):
            pygame.draw.rect(WIN,OTHERPINK,resetButton)
        if algorithmButton.collidepoint(hoverpos):
            pygame.draw.rect(WIN,OTHERPINK,algorithmButton)
        if mazeButton.collidepoint(hoverpos):
            pygame.draw.rect(WIN,OTHERPINK,mazeButton)
        if visualizeButton.collidepoint(hoverpos):
            pygame.draw.rect(WIN,OTHERPINK,visualizeButton)
    pygame.Surface.blit(WIN,resetText,(resetButton.x,resetButton.y))
    pygame.Surface.blit(WIN,searchText,(algorithmButton.x,algorithmButton.y))
    pygame.Surface.blit(WIN,mazeText,(mazeButton.x,mazeButton.y))
    pygame.Surface.blit(WIN,visualizeText,(visualizeButton.x,visualizeButton.y))
    if visualize == True:
        pygame.Surface.blit(WIN,visualizeon,(755,visualizeButton.y))
    if visualize == False:
        pygame.Surface.blit(WIN,visualizeoff,(755,visualizeButton.y))

def draw(grid):
    for row in grid:
        for node in row:
            node.draw(WIN)
    pygame.display.update()
def main():
    widthOfNode = 20
    row = int((WIDTH-160)/widthOfNode)
    col = int(HEIGHT/widthOfNode)
    run = True
    grid = createGrid(row,col,widthOfNode)
    startNode = None
    endNode = None
    hoverpos = None
    visualize = True
    while run:
        drawbuttons(hoverpos,visualize)
        draw(grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    mazeGeneration(grid,visualize)
                if event.key == pygame.K_SPACE and startNode and endNode:
                    for row in grid:
                        for node in row:
                            node.createNeighborsSearch(grid)
                    AStarAlgorithm(grid,startNode,endNode,visualize)
                if event.key == pygame.K_r:
                    for row in grid:
                        for node in row:
                            node.color = GREY
                            node.isvisited = False
                            node.isvisitedSearch = False
                            node.startNode = False
                            node.endNode = False
                            node.iswall = [True,True,True,True]
                            startNode = None
                            endNode = None
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: #LEFT MOUSE BUTTON
                startEndPos = pygame.mouse.get_pos()
                print(startEndPos)
                if startEndPos[0] < (801-160):
                    row, col = mousePosition(startEndPos,widthOfNode)
                    node = grid[row][col]
                    if not startNode and node != endNode:
                        startNode = node
                        startNode.startNode = True
                    elif not endNode and node != startNode:
                        endNode = node
                        endNode.endNode = True
                else:
                    if resetButton.collidepoint(startEndPos):
                        for row in grid:
                            for node in row:
                                node.color = GREY
                                node.isvisited = False
                                node.isvisitedSearch = False
                                node.startNode = False
                                node.endNode = False
                                node.iswall = [True,True,True,True]
                                startNode = None
                                endNode = None
                    elif algorithmButton.collidepoint(startEndPos) and startNode and endNode:
                        for row in grid:
                            for node in row:
                                node.createNeighborsSearch(grid)
                        AStarAlgorithm(grid,startNode,endNode,visualize)
                    elif mazeButton.collidepoint(startEndPos):
                        mazeGeneration(grid,visualize)
                    elif visualizeButton.collidepoint(startEndPos):
                        if visualize == True:
                            visualize = False
                        elif visualize == False:
                            visualize = True
            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3:
                mousepos = pygame.mouse.get_pos()
                if mousepos[0] < (801-160):
                    row, col = mousePosition(mousepos,widthOfNode)
                    node = grid[row][col]
                    if node == startNode:
                        startNode = None
                        node.startNode = False
                        node.color = GREY
                    elif node == endNode:
                        endNode = None
                        node.endNode = False
                        node.color = GREY
            hoverpos = pygame.mouse.get_pos()
    pygame.quit()
main()