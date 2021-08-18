import pygame
import math
from settings import *
from queue import PriorityQueue

WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Path Finding Algorithm Visualizer")

class Cell:
    
    def __init__(self, row, col, width, total_rows):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.colour = WHITE
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows

    def get_pos(self):
        return self.row, self.col

    def is_start(self):
        return self.colour == LIGHTBLUE

    def is_end(self):
        return self.colour == LIGHTPURPLE
    
    def is_closed(self):
        return self.colour == LIGHTRED

    def is_open(self):
        return self.colour == LIGHTGREEN

    def is_wall(self):
        return self.colour == BLACK

    def make_start(self):
        self.colour = LIGHTBLUE
    
    def make_end(self):
        self.colour = LIGHTPURPLE

    def make_closed(self):
        self.colour = LIGHTRED

    def make_open(self):
        self.colour = LIGHTGREEN

    def make_path(self):
        self.colour = LIGHTPINK

    def make_wall(self):
        self.colour = BLACK

    def reset(self):
        self.colour = WHITE
    
    def draw(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.width))

    def update_neighbours(self, grid):
        
        if self.row < self.total_rows - 1 and not grid [self.row+1][self.col].is_wall(): # Down
            self.neighbours.append(grid[self.row+1][self.col])
        if self.row > 0 and not grid [self.row-1][self.col].is_wall(): # Up
            self.neighbours.append(grid[self.row-1][self.col])
        if self.col < self.total_rows - 1 and not grid [self.row][self.col+1].is_wall(): # Right
            self.neighbours.append(grid[self.row][self.col+1])
        if self.col > 0 and not grid [self.row][self.col-1].is_wall(): # Left
            self.neighbours.append(grid[self.row][self.col-1])
        

    def __lt__(self, other):
        return False

def h(p1, p2):
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def path(previous_cell, current_cell, draw):
    while current_cell in previous_cell:
        current_cell = previous_cell[current_cell]
        current_cell.make_path()
        draw()

def a_star(draw, grid, start, end):
    count = 0
    open_set = PriorityQueue()
    open_set.put((0, count, start))
    previous_cell = {}
    g_score = {spot: float("inf") for row in grid for spot in row}
    g_score[start] = 0
    f_score = {spot: float("inf") for row in grid for spot in row}
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start}

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        current = open_set.get()[2]
        open_set_hash.remove(current)

        if current == end:
            path(previous_cell, end, draw)
            return True

        for neighbour in current.neighbours:
            temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbour]:
                previous_cell[neighbour] = current
                g_score[neighbour] = temp_g_score
                f_score[neighbour] = temp_g_score + h(neighbour.get_pos(), end.get_pos())
                if neighbour not in open_set_hash:
                    count+=1
                    open_set.put((f_score[neighbour], count, neighbour))
                    open_set_hash.add(neighbour)
                    neighbour.make_open()
        
        draw()

        if current != start:
            current.make_closed()
    
    return False

def make_grid(rows, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i, j, gap, rows)
            grid[i].append(cell)

    return grid

def draw_grid(win, rows, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GRAY, (0, i*gap), (width, i*gap))
        for j in range(rows):
            pygame.draw.line(win, GRAY, (j*gap, 0), (j*gap, width))

def draw(win, grid, rows, width):
    win.fill(WHITE)

    for row in grid:
        for cell in row:
            cell.draw(win)

    draw_grid(win, rows, width)
    pygame.display.update()


def get_clicked_pos(pos, rows, width):
    gap = width // rows
    y, x = pos
    
    row = y // gap
    col = x // gap

    return row, col


def main(win, width):
    grid = make_grid(ROWS, width)

    start = None
    end = None

    running = True
    solving = False

    while running:
        draw(win, grid, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                
            if pygame.mouse.get_pressed()[0]: # Left Mouse
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cell = grid[row][col]

                if not start and cell != end:
                    start = cell
                    start.make_start()

                elif not end and cell != start:
                    end = cell
                    end.make_end()

                elif cell != start and cell != end:
                    cell.make_wall()

            elif pygame.mouse.get_pressed()[2]: # Right Mouse
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                cell = grid[row][col]
                if cell == start:
                    start = None
                elif cell == end:
                    end = None
                cell.reset()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN and not solving and start and end:
                    for row in grid:
                        for cell in row:
                            cell.update_neighbours(grid)
                    a_star(lambda: draw(win, grid, ROWS, width), grid, start, end)        

                if event.key == pygame.K_SPACE:
                    start = None
                    end = None
                    grid = make_grid(ROWS, width)

    pygame.quit()

main(WIN, WIDTH)
