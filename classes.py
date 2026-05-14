import pygame, random, pygameUtils, constants, numpy as np

class Enemy():
    def __init__(self, size, pos : tuple, speed=10, health=100):
        self.rect = pygame.Rect(0, 0, size, size)
        self.rect.center = (0,0)
        """rect x,y is an offset from the center (declared by self.x and y)"""
        self.x : int = pos[0]
        """Not a screen pos, rather an in-game coord"""
        self.y : int = pos[1]
        self.width = size
        self.height = size
        self.speed = speed
        self.block = [1,4,5,6,7,8]
        self.max_health = health
        self.health = health
        self.damage = 10

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
        
        new_rect_pos = pygameUtils.move_towards(current_rect_pos, next_pos, (self.speed+random.randrange(-10,10))*dt)

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

        # realign if close
        if pygameUtils.get_distance_between(current_rect_pos, next_pos) < 0.1:
            self.x, self.y = next_coord
            self.rect.centerx, self.rect.centery = (0,0)

        # return [next_pos]
        # return [current_grid_pos, current_rect_pos, next_pos]
        # return [current_rect_pos, next_pos, player_rect_pos, new_rect_pos, diff]
        # return [new_rect_pos, (self.rect.centerx, self.rect.centery)]
        # return [new_rect_pos]
        # next_rect_pos = pygameUtils.move_towards(np.array(self.rect.centerx, self.rect.centery), np.array(player.))

    def draw(self):
        surf : pygame.Surface = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
        grid_pos = pygameUtils.get_centre_pos_from_idx((self.x, self.y), constants.GRID_SIZE)
        center_pos = np.array(grid_pos + np.array([self.rect.centerx, self.rect.centery]))
        enemy_rect = self.rect.copy()
        enemy_rect.centerx, enemy_rect.centery = center_pos
        pygame.draw.rect(surf, constants.RED, enemy_rect)
        health_rect = pygame.Rect(0,0,15,2)
        health_rect.center = (center_pos[0], center_pos[1]-self.height)
        tl = health_rect.topleft
        pygame.draw.rect(surf, constants.LIGHT_GREY, health_rect)
        health_rect = pygame.Rect(0,0,15*(self.health/self.max_health),2)
        health_rect.topleft = tl
        pygame.draw.rect(surf, constants.RED, health_rect)

        return surf

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
    def __init__(self, pos, frequency, max_enemies, delay=0):
        self.pos = pos
        self.frequency : float = frequency
        self.time_since_last : float = frequency-delay
        self.enemies_released : int = 0 # trying not to say produced
        self.max_enemies = max_enemies

    def update(self, dt, enemies):

        self.time_since_last += dt

        if self.time_since_last < self.frequency or self.enemies_released >= self.max_enemies:
            return

        self.time_since_last = 0.0

        enemies.append(Enemy(15, self.pos, 20))
        self.enemies_released +=1

class Tower():
    def __init__(self, pos : tuple, health, frequency):
        self.x = pos[0]
        self.y = pos[1]
        self.rect = pygame.Rect(self.x, self.y, constants.GRID_SIZE, constants.GRID_SIZE)
        self.health = health

class Bullet():
    def __init__(self, pos : tuple, size, speed, direction_vector, damage, max_dist=1000):
        self.pos : tuple = pos
        self.velocity = np.array(direction_vector * speed)
        self.damage = damage
        self.max_dist = max_dist
        self.speed = speed
        # seld
        self.distance_travelled = 0.0
        self.size = size
        self.kill = False

    def update(self, dt, enemies : list[Enemy]):

        # self.time_since_last += dt

        # self.time_since_last = 0.0

        self.distance_travelled += self.speed

        self.pos = tuple(np.array(self.pos) + np.array(self.velocity))

        # self.enemies = [
        #     enemy for enemy in enemies 
        #     if pygameUtils.get_distance_between(tuple(pygameUtils.get_centre_pos_from_idx(enemy.x, enemy.y)), tuple(self.pos)) >= constants.GRID_SIZE
        # ]

        for enemy in enemies:
            # enemy_pos = pygameUtils.get_centre_pos_from_idx(enemy.x, enemy.y)
            enemy_grid_pos = pygameUtils.get_centre_pos_from_idx((enemy.x, enemy.y), constants.GRID_SIZE)
            enemy_center_pos = np.array(enemy_grid_pos + np.array([enemy.rect.centerx, enemy.rect.centery]))
            if pygameUtils.get_distance_between(tuple(enemy_center_pos), tuple(self.pos)) < enemy.height:
                enemy.health -= self.damage
                if enemy.health <= 0:
                    enemies.remove(enemy)
                self.kill = True
                break

        if self.distance_travelled >= self.max_dist:
            self.kill = True

        # Gahh so repetetive, but good, its good right? its so good actually object oriented, thankyou abhisek 

class Turret():
    def __init__(self, coord : tuple, health, frequency):
        self.x : int = coord[0]
        self.y : int = coord[1]
        self.rect = pygame.Rect(self.x, self.y, constants.GRID_SIZE, constants.GRID_SIZE)
        self.max_health = health
        self.health = health
        self.frequency : float = frequency
        self.angle : float = 0.0
        self.range = 100
        self.time_since_last = 0.0

    # def update(self, dt, enemies, bullets):

    #     self.time_since_last += dt

    #     if self.time_since_last < self.frequency:
    #         return

    #     self.time_since_last = 0.0

    #     to_angle = 0

    #     bullets.append(Bullet((self.x, self.y), 10, to_angle, 100))

    def update(self, dt, enemies, bullets):
            points = []
            self.time_since_last += dt

            # Get the turret's actual screen position (center of its tile)
            self.center = pygameUtils.get_centre_pos_from_idx((self.x, self.y), constants.GRID_SIZE)

            target_pos = None
            distance_to_target = self.range

            for enemy in enemies:
                # Calculate Enemy Screen Position: 
                # (Grid Center) + (Sub-pixel Rect Offset)
                enemy_grid_center = pygameUtils.get_centre_pos_from_idx((enemy.x, enemy.y), constants.GRID_SIZE)
                enemy_pixel_x = enemy_grid_center[0] + enemy.rect.centerx
                enemy_pixel_y = enemy_grid_center[1] + enemy.rect.centery

                # Calculate distance from Turret Center to Enemy Pixel Position
                dx = enemy_pixel_x - self.center[0]
                dy = enemy_pixel_y - self.center[1]
                # distance = pygameUtils.get_distance_between(dx, dy)
                distance = pygameUtils.get_distance_between(enemy_grid_center, pygameUtils.get_centre_pos_from_idx((self.x,self.y), constants.GRID_SIZE))

                # Track the closest one within range
                if distance <= self.range and distance < distance_to_target:
                    distance_to_target = distance
                    target_pos = (enemy_pixel_x, enemy_pixel_y)

            # 4. Update Rotation (Tracking)
            if target_pos:
                points.append((target_pos[0], target_pos[1]))
                # Calculate vector from turret to the pixel target
                rel_x = target_pos[0] - self.center[0]
                rel_y = target_pos[1] - self.center[1]
                
                # Update angle so the draw() function reflects the new direction
                # Assuming vector_to_angle takes (x, y)
                self.angle = pygameUtils.vector_to_angle((rel_x, rel_y))

                # 5. Shooting Logic
                if self.time_since_last >= self.frequency:
                    bullets.append(Bullet(self.center, 2, 10, pygameUtils.angle_to_vector(self.angle+random.randrange(-1,1)*0.5), 50))
                    self.time_since_last = 0.0

            # else:
            #     self.angle += 10*dt

            return points

    def draw(self):
        surf : pygame.Surface = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
        target_pos : tuple = pygameUtils.get_centre_pos_from_idx((self.x, self.y), constants.GRID_SIZE)
        pygame.draw.circle(surf, constants.GREY, target_pos, constants.GRID_SIZE//4-1)
        # pygame.draw.polygon(surf, constants.LIGHT_GREY+(100,), pygameUtils.create_view_cone_polygon(target_pos, self.angle, 30, self.range))
        pygame.draw.line(surf, constants.LIGHT_GREY, (target_pos), tuple(pygameUtils.move_at_angle(target_pos, self.angle, 20)), 2)
        # pygame.draw.circle(surf, constants.DARK_GREY, target_pos+(pygameUtils.angle_to_vector(self.angle)*self.range), 10)
        return surf

class Cursor():
    def __init__(self, pos : tuple, color : tuple, alpha : int):
        self.x : int = pos[0]
        self.y : int = pos[1]
        self.rect = pygame.Rect(self.x, self.y, constants.GRID_SIZE, constants.GRID_SIZE)
        self.color : tuple = color + (alpha,)

    def move_to_mouse(self, pos : tuple):
        coord = pygameUtils.get_grid_index(pos, constants.GRID_SIZE)
        if coord[0] <= constants.GRID_X and coord[1] <= constants.GRID_Y:
            self.x, self.y = coord

    def place(self, pos : tuple, turrets : list[Turret], array, spawners : list[Spawner], tower : Tower):
        coord = pygameUtils.get_grid_index(pos, constants.GRID_SIZE)
        x, y = coord
        if array[y][x] != 0:
            return
        for spawner in spawners:
            array[y][x] = 4
            path = pygameUtils.find_path(array, (spawner.pos[1], spawner.pos[0]), (tower.y, tower.x), [1,4])
            if not path:
                array[y][x] = 0 # Clean up before leaving lol
                return
        turrets.append(Turret(coord, 100, 1))
        array[y][x] = 4

    def update_pos(self, dt, enemies):

        pass

if __name__ == "__main__":
    print("This is a utility file, not meant to be run directly")
