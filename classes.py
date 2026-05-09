import pygame, random, pygameUtils, numpy as np

class Enemy():
    def __init__(self, width, height, pos : tuple):
        self.rect = pygame.Rect(0, 0, width, height)
        """rect x,y is an offset from the center (declared by self.x and y)"""
        self.x : int = pos[0]
        """Not a screen pos, rather an in-game coord"""
        self.y : int = pos[1]
        self.width = width
        self.height = height
        self.speed = 10

    def handle_movement(self, dt, array, player):
        path : list = pygameUtils.find_path(array, (self.y,self.x), (player.y,player.x))
        if len(path) >= 2:
            next_pos = path[1]
            print((self.y,self.x))
            print(path)
            print(next_pos)
        else:
            # return "No path found"
            return
        # self.rect.x, self.rect.y = pygameUtils.move_towards(np.array([self.rect.x, self.rect.y]), np.array([player.x, player.y])*10, self.speed*dt)
        # self.rect.x, self.rect.y = pygameUtils.move_towards(np.array([self.rect.x, self.rect.y]), next_pos, self.speed*dt)
        # if (self.x*10+self.rect.x,self.y*10+self.rect.y) == next_pos:
        #     self.rect.x, self.rect.y = (0,0)
        #     self.x, self.y = next_pos
        #     print("yya")
        # print("Moved")
        self.y, self.x = next_pos

class Player():
    def __init__(self, width, height, pos : tuple):
        self.rect = pygame.Rect(0, 0, width, height)
        """rect x,y is an offset from the center (declared by self.x and y)"""
        self.x : int = pos[0]
        """Not a screen pos, rather an in-game coord"""
        self.y : int = pos[1]
        self.width = width
        self.height = height
        self.speed = 10

    def handle_movement(self, dt, array, player):
        next_pos = pygameUtils.find_path(array, (self.y,self.x), (player.y,player.x))
        self.rect.x, self.rect.y = pygameUtils.move_towards((self.rect.x, self.rect.y), np.array([player.x, player.y])*10, self.speed*dt)
        if (self.x*10+self.rect.x,self.y*10+self.rect.y) == next_pos:
            print("yya")

if __name__ == "__main__":
    print("This is a utility file, not meant to be run directly")
