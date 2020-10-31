import pygame
import math
from queue import PriorityQueue

size = 800
win = pygame.display.set_mode((size, size))
pygame.display.set_caption("A* Path Finding Algorithm")


red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
yellow = (255, 255, 0)
white = (255, 255, 255)
black = (0, 0, 0)
purple = (128, 0, 128)
orange = (255, 165, 0)
grey = (128, 128, 128)
turquoise = (64, 224, 208)

class Spot:
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = white
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows

    def getPos(self):
        return self.row, self.col

    def isClosed(self):
        return self.color == red

    def isOpen(self):
        return self.color == green

    def isBarrier(self):
        return self.color == black

    def isStart(self):
        return self.color == orange

    def isEnd(self):
        return self.color == turquoise

    def reset(self):
        self.color = white

    def makeStart(self):
        self.color = orange

    def makeClosed(self):
        self.color = red

    def makeOpen(self):
        self.color = green

    def makeBarrier(self):
        self.color = black

    def makeEnd(self):
        self.color = turquoise

    def makePath(self):
        self.color = purple

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def updateNeighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].isBarrier(): #Down
            self.neighbors.append(grid[self.row + 1][self.col])
            
        if self.row > 0 and not grid[self.row - 1][self.col].isBarrier(): #Up
            self.neighbors.append(grid[self.row - 1][self.col])
            
        if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].isBarrier(): #Right
            self.neighbors.append(grid[self.row][self.col + 1])
            
        if self.col > 0 and not grid[self.row][self.col - 1].isBarrier(): #Left
            self.neighbors.append(grid[self.row][self.col - 1])

    def __lt__(self, other):
        return False

    
def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstructPath(cameFrom, current, draw):
    while current in cameFrom:
        current = cameFrom[current]
        current.makePath()
        draw()

def algorithm(draw, grid, start, end):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0, count, start))
    cameFrom = {}
    
    gScore = {spot: float("inf") for row in grid for spot in row}
    gScore[start] = 0
    
    fScore = {spot: float("inf") for row in grid for spot in row}
    fScore[start] = h(start.getPos(), end.getPos())

    openSetHash = {start}

    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openSet.get()[2]
        openSetHash.remove(current)

        if current == end:
            reconstructPath(cameFrom, end, draw)
            end.makeEnd()
            start.makeStart()
            return True

        for neighbor in current.neighbors:
            tempGScore = gScore[current] + 1

            if tempGScore < gScore[neighbor]:
                cameFrom[neighbor] = current
                gScore[neighbor] = tempGScore
                fScore[neighbor] = tempGScore + h(neighbor.getPos(), end.getPos())
                if neighbor not in openSetHash:
                    count += 1
                    openSet.put((fScore[neighbor], count, neighbor))
                    openSetHash.add(neighbor)
                    neighbor.makeOpen()

        draw()

        if current != start:
            current.makeClosed()

    return False

def makeGrid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            spot = Spot(i, j, gap, rows)
            grid[i].append(spot)
    return grid

def drawGrid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, grey, (0, i * gap), (width, i * gap))
        for j in range(rows):
            pygame.draw.line(win, grey, (j * gap, 0), (j * gap, width))

def draw(win, grid, rows, width):
    win.fill(white)

    for row in grid:
        for spot in row:
            spot.draw(win)

    drawGrid(win, rows, width)
    pygame.display.update()
    
def getClickedPos(pos, rows, width):
    gap = width // rows
    y,x = pos

    row = y // gap
    col = x // gap
    return row, col

def main(win, width):
    rows = 50
    grid = makeGrid(rows, width)

    start = None
    end = None

    run = True

    while run:
        draw(win, grid, rows, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, rows, width)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.makeStart()

                elif not end and spot != start:
                    end = spot
                    end.makeEnd()

                elif spot != end and spot != start:
                    spot.makeBarrier()
                
            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = getClickedPos(pos, rows, width)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                elif spot == end:
                    end = None

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.updateNeighbors(grid)

                    algorithm(lambda: draw(win, grid, rows, width), grid, start, end)

                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = makeGrid(rows, width)
                    
    pygame.quit()

if __name__ == "__main__":
    main(win, size)

