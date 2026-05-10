import constants, keybinds, pygame, pygameUtils, numpy as np
from classes import Enemy, Player, Spawner, Tower, Turret, Cursor

pygame.init()
clock = pygame.time.Clock()

SCREEN = pygame.display.set_mode((constants.WIDTH, constants.HEIGHT))
pygame.display.set_caption("Tower defence")

# def draw(array : list[list], enemies : list[Enemy], player : Player, points : list[tuple], money):
def draw(array : list[list], enemies : list[Enemy], turrets : list[Turret], points : list[tuple], money, cursor : Cursor):
    SCREEN.fill(constants.BLACK)
    
    for row_idx, row in enumerate(array):
        pygame.draw.line(SCREEN, constants.WHITE, (0,row_idx*constants.GRID_SIZE), (constants.WIDTH,row_idx*constants.GRID_SIZE))
        for col_idx, col in enumerate(row):
            pygame.draw.line(SCREEN, constants.WHITE, (col_idx*constants.GRID_SIZE,0), (col_idx*constants.GRID_SIZE,constants.HEIGHT))
            # if array[row_idx][col_idx]:
            match col:
                case 1:
                    # Multiply by grid size to get screen coord
                    pygame.draw.rect(SCREEN, constants.WHITE, pygame.Rect(col_idx*constants.GRID_SIZE, row_idx*constants.GRID_SIZE, constants.GRID_SIZE, constants.GRID_SIZE))
                case 2:
                    pygame.draw.rect(SCREEN, constants.DARK_PURPLE, pygame.Rect(col_idx*constants.GRID_SIZE, row_idx*constants.GRID_SIZE, constants.GRID_SIZE, constants.GRID_SIZE))
                case 3:
                    pygame.draw.rect(SCREEN, constants.CYAN, pygame.Rect(col_idx*constants.GRID_SIZE, row_idx*constants.GRID_SIZE, constants.GRID_SIZE, constants.GRID_SIZE))
                # case 4:
                #     pygame.draw.circle(SCREEN, constants.GREY, pygameUtils.get_centre_pos_from_idx((col_idx, row_idx), constants.GRID_SIZE), constants.GRID_SIZE//2-1)

    for enemy in enemies:
        # enemy_rect = pygame.Rect(0,0, enemy.width, enemy.height)
        enemy_rect = enemy.rect.copy()
        enemy_rect.centerx, enemy_rect.centery = np.array(pygameUtils.get_centre_pos_from_idx((enemy.x, enemy.y), constants.GRID_SIZE)) + np.array([enemy.rect.centerx, enemy.rect.centery])
        # enemy_rect = pygame.Rect(enemy.x*constants.GRID_SIZE+enemy.rect.x,enemy.y*constants.GRID_SIZE+enemy.rect.y,enemy.rect.w,enemy.rect.h)
        pygame.draw.rect(SCREEN, constants.RED, enemy_rect)

    for turret in turrets:
        target_pos = pygameUtils.get_centre_pos_from_idx((turret.x, turret.y), constants.GRID_SIZE)
        pygame.draw.circle(SCREEN, constants.GREY, target_pos, constants.GRID_SIZE//2-1)

    # left here so i dont forget how to make them
    # player_rect = pygame.Rect(player.x*constants.GRID_SIZE+player.rect.x,player.y*constants.GRID_SIZE+player.rect.y,player.rect.w,player.rect.h)
    # player_rect = player.rect.copy()
    # player_rect.centerx, player_rect.centery = pygameUtils.get_centre_pos_from_idx((player.x, player.y), constants.GRID_SIZE)
    # pygame.draw.rect(SCREEN, constants.BLUE, player_rect)

    for point in points:
        pygame.draw.circle(SCREEN, constants.GREEN, point, 2)

    pygameUtils.render_text(str(money), (constants.WIDTH-70, 10), constants.GREEN, SCREEN, 25)

    cursor_rect = cursor.rect.copy()
    cursor_rect.centerx, cursor_rect.centery = pygameUtils.get_centre_pos_from_idx((cursor.x, cursor.y), constants.GRID_SIZE)
    display = pygame.Surface((constants.WIDTH, constants.HEIGHT), pygame.SRCALPHA)
    pygame.draw.rect(display, cursor.color, cursor_rect)
    SCREEN.blit(display, (0,0))

    pygame.display.update()

def main():

    map_array = [
        [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [2,0,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,1,0,0,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,1,0,0,0,0,1,3,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [0,1,1,0,1,0,1,0,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,2,0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
        [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    ]

    spawners : list[Spawner] = []

    tower = Tower((0,0), 100)

    for row_idx, row in enumerate(map_array):
        for col_idx, item in enumerate(row):
            match item:
                case 2:
                    spawners.append(Spawner((col_idx, row_idx), 2, 0))
                case 3:
                    tower.x, tower.y = col_idx, row_idx


    # enemies : list[Enemy] = [Enemy(15, (2, 3), 10)]
    enemies : list[Enemy] = []

    turrets : list[Turret] = []

    # player = Player(10, (8, 4))

    cursor = Cursor((0,0), constants.BLUE, 150)

    points : list[tuple] = []

    money : int = 100

    timer : float = 0.0

    running = True

    while running:

        # var resets
        points.clear()

        delta_time : float = clock.tick(constants.FPS) / 1000.0
        timer += delta_time

        if timer >= 2:
            timer = 0.0
            print(clock.get_fps())

        # Event handling

        for event in pygame.event.get():
            match event.type:
                # Use a switch statment because its more effieient and easier to read than ifs
                case pygame.QUIT:
                    running = False
                case pygame.MOUSEMOTION:
                    mouse_pos = (event.pos[0], event.pos[1])
                    cursor.move_to_mouse(mouse_pos)
                    # mouse_rel = event.rel   
                    pass
                case pygame.MOUSEBUTTONDOWN:
                    match event.button:
                        case 1: # 1 represents the left mouse button
                            cursor.place(mouse_pos, turrets, map_array, spawners, tower)
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

        for spawner in spawners:
            spawner.update(delta_time, enemies)

        for enemy in enemies:
            if ans := enemy.handle_movement(delta_time, map_array, tower):
                # print(ans)
                points += ans

        draw(map_array, enemies, turrets, points, money, cursor)

if __name__ == "__main__":
    main()