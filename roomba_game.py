import pygame, sys
from pathfinding.core.grid import Grid
from pathfinding.finder.a_star import AStarFinder
from pathfinding.core.diagonal_movement import DiagonalMovement
from pygame.constants import MOUSEBUTTONDOWN

class Pathfinder:
    def __init__(self, matrix):
        self.matrix = matrix
        self.grid = Grid(matrix = self.matrix)
        self.select_surf = pygame.image.load('selection.png').convert_alpha()

        self.path = []

        self.roomba = pygame.sprite.GroupSingle(Roomba(self.clear_path))
    
    def clear_path(self):
        self.path = []

    def draw_active_cell(self):
        mouse_pos = pygame.mouse.get_pos()
        self.row = mouse_pos[1] // 32
        self.col = mouse_pos[0] // 32
        if self.matrix[self.row][self.col] == 1:
            select_rect = pygame.Rect((self.col*32, self.row*32), (32,32))
            screen.blit(self.select_surf, select_rect)

    def create_path(self):
        start_xy = self.roomba.sprite.get_coord()
        start = self.grid.node(*start_xy)

        end_xy = (self.col, self.row)
        end = self.grid.node(*end_xy)

        finder = AStarFinder(diagonal_movement = DiagonalMovement.always)
        self.path,_ = finder.find_path(start, end, self.grid)
        self.roomba.sprite.set_path(self.path)
        self.grid.cleanup()

    def draw_path(self):
        if len(self.path) > 1:
            points = [(x*32+16, y*32+16) for x, y in self.path]
            pygame.draw.lines(screen, '#4a4a4a', False, points, 5)

    def update(self):
        self.draw_active_cell()
        self.draw_path()

        self.roomba.update()
        self.roomba.draw(screen)

class Roomba(pygame.sprite.Sprite):
    def __init__(self, clear_path):
        super().__init__()
        self.image = pygame.image.load('roomba.png').convert_alpha()
        self.rect = self.image.get_rect(center = (60,60))

        self.pos = self.rect.center
        self.speed = 2
        self.direction = pygame.math.Vector2(0,0)

        self.path = []
        self.collision_rects = []
        self.clear_path = clear_path
    
    def get_coord(self):
        col = self.rect.centerx // 32
        row = self.rect.centery // 32
        return (col, row)
    
    def set_path(self, path):
        self.path = path
        self.create_collision_rects()
        self.get_direction()
    
    def create_collision_rects(self):
        if self.path:
            self.collision_rects = []
            for point in self.path:
                x = point[0]*32 + 14
                y = point[1]*32 + 14
                rect = pygame.Rect((x,y), (4,4))
                self.collision_rects.append(rect)
    
    def get_direction(self):
        if self.collision_rects:
            start = pygame.math.Vector2(self.pos)
            end = pygame.math.Vector2(self.collision_rects[0].center)
            self.direction = (end - start).normalize()
        else:
            self.direction = pygame.math.Vector2(0,0)
            self.path = []
    
    def check_collision(self):
        if self.collision_rects:
            for rect in self.collision_rects:
                if rect.collidepoint(self.pos):
                    del self.collision_rects[0]
                    self.get_direction()
        else:
            self.clear_path()

    def update(self):
        self.pos += self.direction * self.speed
        self.check_collision()
        self.rect.center = self.pos

pygame.init()
icon = pygame.image.load('roomba.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('Roomba Game')
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()

bg_surf = pygame.image.load('map.png').convert()
matrix = [
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,0,0,0,0,1,1,0,0,1,1,1,1,1,0,0,0,0,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
	[0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,0,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,0,0,1,1,0,0,1,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,0,0,0,0,0,0,1,1,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
	[0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0],
	[0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,0,1,1,0,0,0,0,0,0,0,0,0,0,0,1,0,0,1,1,1,1,0,0,0],
	[0,1,1,1,1,1,0,0,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,0,0,1,1,1,1,0,0,0],
	[0,0,0,1,1,1,0,0,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,0],
	[0,0,0,1,1,1,1,1,1,1,1,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,1,1,1,1,0],
	[0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,0],
	[0,1,1,1,1,1,1,1,1,0,0,0,0,1,1,0,0,1,1,1,1,1,1,1,1,1,1,1,0,0,1,1,1,1,1,0,0,1,1,0],
	[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
pathfinder = Pathfinder(matrix)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.MOUSEBUTTONDOWN:
            pathfinder.create_path()
    
    screen.blit(bg_surf, (0,0))
    pathfinder.update()

    pygame.display.update()
    clock.tick(60)