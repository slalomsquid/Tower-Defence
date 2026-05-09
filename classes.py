import pygame, random, pygameUtils, constants, numpy as np

class Enemy():
    def __init__(self, size, pos : tuple, speed=10):
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (0,0)
        """rect x,y is an offset from the center (declared by self.x and y)"""
        self.x : int = pos[0]
        """Not a screen pos, rather an in-game coord"""
        self.y : int = pos[1]
        self.width = size
        self.height = size
        self.speed = speed
        self.block = [1,5,6,7,8]

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

    def handle_movement(self, dt, array, target):
        path : list[tuple] = pygameUtils.find_path(array, (self.y, self.x), (target.y, target.x), self.block)
        # Cancel if there is not enough points (0 is always the start pos)
        if len(path) < 2:
            return
        # work out abs coord values
        next_coord = path[1]
        next_coord = (next_coord[1], next_coord[0])
        next_pos = pygameUtils.get_centre_pos_from_idx(path[1], constants.GRID_SIZE)
        # flip because it comes from the find_path func
        next_pos = (next_pos[1], next_pos[0])
        current_grid_pos = pygameUtils.get_centre_pos_from_idx((self.x, self.y), constants.GRID_SIZE)
        # current_rect_pos = np.array(pygameUtils.get_centre_pos_from_idx((self.x, self.y), constants.GRID_SIZE)) + np.array((self.rect.centerx, self.rect.centery))
        current_rect_pos = np.array(current_grid_pos) + np.array((self.rect.centerx, self.rect.centery))
        # current_rect_pos = np.array(pygameUtils.get_centre_pos_from_idx((self.x, self.y), constants.GRID_SIZE)) + np.array((self.rect.centerx, self.rect.centery))
        player_rect_pos = pygameUtils.get_centre_pos_from_idx((target.x, target.y), constants.GRID_SIZE)
        # return [pygameUtils.get_centre_pos_from_idx(next_coord, constants.GRID_SIZE), current_rect_pos, player_rect_pos]
        
        new_rect_pos = pygameUtils.move_towards(current_rect_pos, next_pos, self.speed*dt)

        # self.rect.centerx, self.rect.centery = tuple(pygameUtils.get_difference(new_rect_pos, current_rect_pos))

        # leaving this here like a gravestone for the 2+ hours i spent trying to figue out why it wouldnt move
        # subtracting 2 lists just removes it
        # diff = new_rect_pos - current_rect_pos
        # self.rect.centerx, self.rect.centery = diff[0], diff[1]
        # self.rect.centerx = diff[0]
        # self.rect.centery = diff[1]

        # new_offset = new_rect_pos - np.array(current_grid_pos)
        # use the func, its more readable
        new_offset = pygameUtils.get_difference(current_grid_pos, new_rect_pos)
        self.rect.centerx, self.rect.centery = new_offset[0], new_offset[1]

        # recalc
        current_rect_pos = np.array(current_grid_pos) + np.array((self.rect.centerx, self.rect.centery))

        if pygameUtils.get_distance_between(current_rect_pos, next_pos) < 0.1:
            self.x, self.y = next_coord
            self.rect.centerx, self.rect.centery = (0,0)

        # return [next_pos]
        # return [current_grid_pos, current_rect_pos, next_pos]
        # return [current_rect_pos, next_pos, player_rect_pos, new_rect_pos, diff]
        # return [new_rect_pos, (self.rect.centerx, self.rect.centery)]
        # return [new_rect_pos]
        # next_rect_pos = pygameUtils.move_towards(np.array(self.rect.centerx, self.rect.centery), np.array(player.))


class Player():
    def __init__(self, size, pos : tuple):
        self.rect = pygame.Rect(-size/2, -size/2, size, size)
        """rect x,y is an offset from the center (declared by self.x and y)"""
        self.x : int = pos[0]
        """Not a screen pos, rather an in-game coord"""
        self.y : int = pos[1]
        self.width = size
        self.height = size
        self.speed = 10

    def handle_movement(self, dt, array, player):
        next_pos = pygameUtils.find_path(array, (self.y,self.x), (player.y,player.x), [1,4])
        self.rect.centerx, self.rect.centery = pygameUtils.move_towards((self.rect.centerx, self.rect.centery), np.array([player.x, player.y])*constants.GRID_SIZE, self.speed*dt)
        if (self.x*constants.GRID_SIZE+self.rect.centerx,self.y*constants.GRID_SIZE+self.rect.centery) == next_pos:
            print("yya")

class Spawner():
    def __init__(self, pos, frequency, delay):
        self.pos = pos
        self.frequency : float = frequency
        self.time_since_last : float = frequency-delay

    def update(self, dt, enemies):

        if self.time_since_last >= self.frequency:
            self.time_since_last = 0.0

            # enemies.append(Enemy(15, (2, 3), 10))
            enemies.append(Enemy(15, self.pos, 10))

        self.time_since_last += dt

class Tower():
    def __init__(self, pos : tuple, health):
        self.x : int = pos[0]
        self.y : int = pos[1]
        self.rect = pygame.Rect(self.x, self.y, constants.GRID_SIZE, constants.GRID_SIZE)
        self.health = health

    def update(self, dt, enemies):

        pass

if __name__ == "__main__":
    print("This is a utility file, not meant to be run directly")
