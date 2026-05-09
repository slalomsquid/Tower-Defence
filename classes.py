import pygame, random, pygameUtils, constants, numpy as np

class Enemy():
    def __init__(self, size, pos : tuple):
        self.rect = pygame.Rect(0, 0, size, size)
        """rect x,y is an offset from the center (declared by self.x and y)"""
        self.x : int = pos[0]
        """Not a screen pos, rather an in-game coord"""
        self.y : int = pos[1]
        self.width = size
        self.height = size
        self.speed = 10

    # def handle_movement(self, dt, array, player):
    #     path : list[tuple] = pygameUtils.find_path(array, (self.y,self.x), (player.y,player.x))
    #     if len(path) >= 2:
    #         next_pos : tuple = path[1]
    #         print((self.y,self.x))
    #         print(path)
    #         print(next_pos)
    #     else:
    #         # return "No path found"
    #         return
    #     # self.rect.x, self.rect.y = pygameUtils.move_towards(np.array([self.rect.x, self.rect.y]), np.array([player.x, player.y])*10, self.speed*dt)
    #     self.rect.centery, self.rect.centerx = pygameUtils.move_towards(np.array([self.rect.x, self.rect.y]), np.array(next_pos)*constants.GRID_SIZE, self.speed*dt)
    #     # if pygameUtils.get_grid_index(self.rect.x, self.rect.y, constants.GRID_SIZE) == next_pos:
    #     if pygameUtils.get_distance_between(np.array(pygameUtils.get_grid_index(self.rect.x, self.rect.y, constants.GRID_SIZE)), np.array(next_pos)) < 1:
    #         self.y, self.x = next_pos
    #         self.rect.x, self.rect.y = (0,0)

    def handle_movement(self, dt, array, player):
        path : list[tuple] = pygameUtils.find_path(array, (self.y, self.x), (player.y, player.x))
        # Cancel if there is not enough points (0 is always the start pos)
        if len(path) < 2:
            return
        next_coord = path[1]
        # current_rect_pos = (self.x*constants.GRID_SIZE+self.rect.centerx, self.y*constants.GRID_SIZE+self.rect.centery)
        current_rect_pos = pygameUtils.get_centre_pos_from_idx((self.x, self.y), constants.GRID_SIZE)
        player_rect_pos = pygameUtils.get_centre_pos_from_idx((player.x, player.y), constants.GRID_SIZE)
        # return [pygameUtils.get_centre_pos_from_idx(next_coord, constants.GRID_SIZE), current_rect_pos, player_rect_pos]
        return [current_rect_pos, pygameUtils.get_centre_pos_from_idx(next_coord, constants.GRID_SIZE), player_rect_pos]
        # next_rect_pos = pygameUtils.move_towards(np.array(self.rect.centerx, self.rect.centery), np.array(player.))

        

class Player():
    def __init__(self, size,  pos : tuple):
        self.rect = pygame.Rect(-size/2, -size/2, size, size)
        """rect x,y is an offset from the center (declared by self.x and y)"""
        self.x : int = pos[0]
        """Not a screen pos, rather an in-game coord"""
        self.y : int = pos[1]
        self.width = size
        self.height = size
        self.speed = 10

    def handle_movement(self, dt, array, player):
        next_pos = pygameUtils.find_path(array, (self.y,self.x), (player.y,player.x))
        self.rect.centerx, self.rect.centery = pygameUtils.move_towards((self.rect.centerx, self.rect.centery), np.array([player.x, player.y])*constants.GRID_SIZE, self.speed*dt)
        if (self.x*constants.GRID_SIZE+self.rect.centerx,self.y*constants.GRID_SIZE+self.rect.centery) == next_pos:
            print("yya")

if __name__ == "__main__":
    print("This is a utility file, not meant to be run directly")
