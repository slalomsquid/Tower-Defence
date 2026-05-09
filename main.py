import constants, keybinds, pygame
from classes import Enemy, Player

pygame.init()
clock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("2D Shooter")

def draw(array, enemies, player):
    SCREEN.fill(constants.BLACK)

    for row_idx, row in enumerate(array):
        for col_idx, col in enumerate(row):
            # if array[row_idx][col_idx]:
            if col:
                # Multiply by grid size to get screen coord
                pygame.draw.rect(SCREEN, constants.WHITE, pygame.Rect(col_idx*constants.GRID_SIZE, row_idx*constants.GRID_SIZE, constants.GRID_SIZE, constants.GRID_SIZE))

    for enemy in enemies:
        enemy_rect = pygame.Rect(enemy.x*10+enemy.rect.x,enemy.y*10+enemy.rect.y,enemy.rect.w,enemy.rect.h)
        pygame.draw.rect(SCREEN, constants.RED, enemy_rect)

    player_rect = pygame.Rect(player.x*10+player.rect.x,player.y*10+player.rect.y,player.rect.w,player.rect.h)
    pygame.draw.rect(SCREEN, constants.BLUE, player_rect)

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

    enemies : list[Enemy] = [Enemy(5, 5, (2, 3))] 

    player = Player(5, 5, (8, 5))

    running = True

    while running:

        delta_time = clock.tick(constants.FPS) / 1000.0

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
                print(ans)

        draw(map_array, enemies, player)

if __name__ == "__main__":
    main()