import constants, keybinds, pygame, pygameUtils, numpy as np
from classes import Enemy, Player

pygame.init()
clock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("2D Shooter")

def draw(array : list[list], enemies : list[Enemy], player : Player, points : list[tuple]):
    SCREEN.fill(constants.BLACK)
    
    for row_idx, row in enumerate(array):
        pygame.draw.line(SCREEN, constants.WHITE, (0,row_idx*constants.GRID_SIZE), (constants.WIDTH,row_idx*constants.GRID_SIZE))
        for col_idx, col in enumerate(row):
            pygame.draw.line(SCREEN, constants.WHITE, (col_idx*constants.GRID_SIZE,0), (col_idx*constants.GRID_SIZE,constants.HEIGHT))
            # if array[row_idx][col_idx]:
            if col:
                # Multiply by grid size to get screen coord
                pygame.draw.rect(SCREEN, constants.WHITE, pygame.Rect(col_idx*constants.GRID_SIZE, row_idx*constants.GRID_SIZE, constants.GRID_SIZE, constants.GRID_SIZE))

    for enemy in enemies:
        # enemy_rect = pygame.Rect(0,0, enemy.width, enemy.height)
        enemy_rect = enemy.rect.copy()
        enemy_rect.centerx, enemy_rect.centery = np.array(pygameUtils.get_centre_pos_from_idx((enemy.x, enemy.y), constants.GRID_SIZE)) + np.array([enemy.rect.centerx, enemy.rect.centery])
        # enemy_rect = pygame.Rect(enemy.x*constants.GRID_SIZE+enemy.rect.x,enemy.y*constants.GRID_SIZE+enemy.rect.y,enemy.rect.w,enemy.rect.h)
        pygame.draw.rect(SCREEN, constants.RED, enemy_rect)

    # player_rect = pygame.Rect(player.x*constants.GRID_SIZE+player.rect.x,player.y*constants.GRID_SIZE+player.rect.y,player.rect.w,player.rect.h)
    player_rect = player.rect.copy()
    player_rect.centerx, player_rect.centery = pygameUtils.get_centre_pos_from_idx((player.x, player.y), constants.GRID_SIZE)
    pygame.draw.rect(SCREEN, constants.BLUE, player_rect)

    for point in points:
        pygame.draw.circle(SCREEN, constants.GREEN, point, 2)

    pygame.display.update()

def main():

    map_array = [
        [0,1,1,1,1,1,1,1,1,1,1],
        [0,1,0,0,0,0,0,0,0,0,1],
        [0,1,0,0,0,0,0,0,0,0,1],
        [0,1,0,0,0,0,0,0,0,0,1],
        [0,1,0,0,0,0,0,0,0,0,1],
        [0,1,1,1,1,0,0,0,0,1,1]
    ]

    enemies : list[Enemy] = [Enemy(10, (2, 3), 10)] 

    player = Player(10, (8, 4))

    points : list[tuple] = []

    running = True

    while running:

        # var resets
        points.clear()

        delta_time : float = clock.tick(constants.FPS) / 1000.0

        # Event handling

        for event in pygame.event.get():
            match event.type:
                # Use a switch statment because its more effieient and easier to read than ifs
                case pygame.QUIT:
                    running = False
                case pygame.MOUSEMOTION:
                    # mouse_pos = [event.pos[0] + offset_x, event.pos[1] + offset_y]
                    # mouse_rel = event.rel   
                    pass
                case pygame.KEYDOWN:
                    if any(event.key == key for key in keybinds.shoot):
                        # bullet = Bullet(player.rect.centerx, player.rect.centery, player.rotation, 5)
                        # bullets.append(bullet)
                        pass

                    if event.key == pygame.K_SPACE:
                        pass

        keys = pygame.key.get_pressed()
        if any(keys[k] for k in keybinds.exit):
            pygame.quit()
            running = False

        for enemy in enemies:
            if ans := enemy.handle_movement(delta_time, map_array, player):
                # print(ans)
                points += ans
                

        draw(map_array, enemies, player, points)

if __name__ == "__main__":
    main()