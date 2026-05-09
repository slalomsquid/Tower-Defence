import pygame, constants, numpy as np
from collections import deque

pygame.init()

font = pygame.font.SysFont("Arial", 40)

def render_text(text, pos, color, canv, size=1, center=False, transparent=False):
    font_obj = pygame.font.SysFont(None, size) 
    if transparent:
        text_surface = pygame.Surface((100, 100), pygame.SRCALPHA)
        text_surface = text_surface.convert_alpha()
    else:
        text_surface = font_obj.render(str(text), False, color)
    text_rect = text_surface.get_rect()
    if center:
        text_rect.center = (pos[0], pos[1])
    canv.blit(text_surface, text_rect)

def render_player_arrow(pos, ang, color, canv):
    triangle_points = [move_at_angle(pos, ang, 20), move_at_angle(pos, ang+120, 20), pos, move_at_angle(pos, ang+240, 20)]
    # p1 = move_at_angle(pos, dir + 90, 20)
    # p2 = move_at_angle(pos, dir + 210, 20)
    # p3 = move_at_angle(pos, dir + 330, 20)
    
    # triangle_points = [p1.flatten(), p2.flatten(), p3.flatten()]
    pygame.draw.polygon(canv, color, triangle_points)

def render_map(map, cell_x, cell_y, canv):
    for cell in range(len(map)):
        for tile in range(len(map[cell])):
            if map[cell][tile] == 1:
                pygame.draw.rect(canv, constants.CYAN, (tile*cell_x, cell*cell_y, cell_x, cell_y))

def draw_alpha_line(color, alpha, start, end, width, canv):
    # Calculate height of the wall slice
    height = end[1] - start[1]
    if height <= 0: return

    # Create a tiny surface just for this one ray slice
    # Note: We use a fixed width or ray_width
    line_surf = pygame.Surface((width, int(height)), pygame.SRCALPHA)
    
    # Fill it with the color and the calculated alpha
    line_surf.fill((*color, alpha))
    
    # Blit it to the main canvas at the start position
    canv.blit(line_surf, start)

def draw_rotated_rect(screen, color, rect_dims, angle, center_pos):
    # Create a surface with an alpha
    temp_surf = pygame.Surface((rect_dims[2], rect_dims[3]), pygame.SRCALPHA)
    
    # Draw rectangle on the surface
    pygame.draw.rect(temp_surf, color, (0, 0, rect_dims[2], rect_dims[3]))
    
    # Rotate the surface with -angle because pygame goes anticlockwise
    rotated_surf = pygame.transform.rotate(temp_surf, -angle)
    
    # Get the new rect and center it at the desired position
    rotated_rect = rotated_surf.get_rect(center=center_pos)
    
    # Draw it to the main screen
    screen.blit(rotated_surf, rotated_rect)

### VECTOR MATH ###

def get_difference(current, target):
    """subtracts the vectors"""
    return np.array(target) - np.array(current)

def angle_to_vector(angle):
    """Returns a vector with a length of 1 for a given angle, <angle -> left, >angl -> right"""
    return np.round(np.array([np.cos(np.radians(angle+90)),np.sin(np.radians(angle+90))]), 4)

def translate_vect(vect, displacement):
    return vect + displacement

def move_in_direction(vect, dir, velocity):
    displacement = dir * velocity
    return vect + displacement

def move_at_angle(vect, angle, velocity):
    dir = angle_to_vector(angle)
    displacement = dir * velocity
    # return np.array(vect + displacement, dtype=object)
    return vect + displacement

def get_vector_magnitude(vector):
    return np.linalg.norm(vector)

def get_distance_between(vect1, vect2):
    target = np.array(vect1)
    current = np.array(vect2)
    return np.linalg.norm(target - current)

def simplify_vector(vector):
    if np.linalg.norm(vector) != 0:
        return vector / np.linalg.norm(vector)
    # return np.array([0,0])
    return vector

def vector_to_angle(dir):
    return np.degrees(np.arctan2(dir[1], dir[0]))-90

def cast_ray(start_pos, angle, game_map, size_x, size_y, max_distance=100):
    # Get the normalized direction vector
    direction = angle_to_vector(angle)
    
    # How far we move each step (smaller = more accurate)
    step_size = 1
    ray_pos = np.array(start_pos, dtype=float)
    distance_traveled = 0

    while True:
        # Move the ray forward
        ray_pos += direction * step_size
        distance_traveled += step_size

        # Convert world position to grid coordinates
        map_x = int(ray_pos[0] // size_x)
        map_y = int(ray_pos[1] // size_y)
        
        # Check if we are out of bounds
        if distance_traveled > max_distance or map_y < 0 or map_y >= len(game_map) or map_x < 0 or map_x >= len(game_map[0]):
            break
            
        # Check if we hit a wall (1)
        if game_map[map_y][map_x] != 0:
            return (ray_pos, distance_traveled, game_map[map_y][map_x]) # Return the coordinate where we hit

def decimal_range(start, stop, increment):
    while start < stop: # and not math.isclose(start, stop): Py>3.5
        yield start
        start += increment

def lerp(start, end, t):
    """Linear interpolation between 2 points with t being the proportion between them"""
    return start + t * (end - start)

def lerp_angle(start, end, t):
    """Linear interpolation between 2 points with t being the proportion between them"""
    to_dist = (end - start + 180) % 360 - 180
    if to_dist > 180:
        to_dist -= 360
    if to_dist < -180:
        to_dist += 360
    return (start + t * to_dist) % 360

# def move_towards(current, target, max_distance_delta):
#     """Moves towards a vector/value with a max step"""
#     # to_vector = target - current
#     to_vector = get_difference(target, current)
#     dist = np.linalg.norm(to_vector)
#     if dist <= max_distance_delta or dist == 0:
#         return target
#     return current + to_vector / dist * max_distance_delta

def move_towards(current, target, max_distance_delta):
    direction = target - current
    distance = np.linalg.norm(direction)

    if distance <= max_distance_delta or distance == 0:
        return target

    return current + (direction / distance) * max_distance_delta

# def move_towards(current, target, max_distance_delta):
#     """Moves towards a vector/value with a max step"""
#     current = np.array(current)
#     target = np.array(target)
#     to_vector = target - current
#     dist = np.linalg.norm(to_vector)
    
#     # If target is closer than max_distance_delta, or already there
#     if dist <= max_distance_delta or dist < 1e-9: # 1e-9 to avoid division by zero
#         return target
        
    return current + to_vector / dist * max_distance_delta

def move_towards_angle(current : float, target : float, max_distance_delta : float):
    """Moves towards an angle, allowing to wrap from 360 to prevent going the long way as linear would have it"""
    to_dist = (target - current + 180) % 360 - 180
    if to_dist > max_distance_delta:
        return (current + max_distance_delta) % 360
    if to_dist < -max_distance_delta:
        return (current - max_distance_delta) % 360
    return target

### Other ###
# based on 'rectanglesToArray' by Marty on https://stackoverflow.com/a/25193953
# Retrieved 2026-04-26, License - CC BY-SA 3.0
def get_rectangles(grid, size):
    if not grid or not grid[0]:
        return []

    rows, cols = len(grid), len(grid[0])
    rects = []
    visited = [[False for _ in range(cols)] for _ in range(rows)]

    for r in range(rows):
        for c in range(cols):
            # Only process if it's a '1' and hasn't been part of a previous rect
            if grid[r][c] == 1 and not visited[r][c]:
                # 1. Expand Width: Scan right to find the maximum possible width
                w = 0
                while c + w < cols and grid[r][c + w] == 1 and not visited[r][c + w]:
                    w += 1
                
                # 2. Expand Height: Check subsequent rows for the same width
                h = 1
                while r + h < rows:
                    if all(grid[r + h][c + i] == 1 and not visited[r + h][c + i] for i in range(w)):
                        h += 1
                    else:
                        break
                
                # 3. Mark cells as visited so they aren't counted twice
                for i in range(r, r + h):
                    for j in range(c, c + w):
                        visited[i][j] = True
                
                rects.append((c*size, r*size, w*size, h*size))
    return rects

def is_point_in_triangle(pos, p1, p2, p3):
    def get_area(a, b, c):
        return abs((a[0] * (b[1] - c[1]) + b[0] * (c[1] - a[1]) + c[0] * (a[1] - b[1])) / 2.0)

    total_area = get_area(p1, p2, p3)
    area1 = get_area(pos, p2, p3)
    area2 = get_area(p1, pos, p3)
    area3 = get_area(p1, p2, pos)

    # Use a small epsilon for float precision
    return abs(total_area - (area1 + area2 + area3)) < 0.1

def create_view_cone_polygon(self):
    view_left = self.rotation - self.fov/2
    view_right = self.rotation + self.fov/2

    view_left_direction = angle_to_vector(view_left)
    view_right_direction = angle_to_vector(view_right)

    points = [
        (self.x, self.y), 
        (self.x + view_left_direction[0]*self.view_distance, self.y + view_left_direction[1]*self.view_distance), 
        (self.x + view_right_direction[0]*self.view_distance, self.y + view_right_direction[1]*self.view_distance)
    ]
    return points

def find_path(grid, start, end):
    """
    Finds the shortest path between start and end coordinates.
    start/end: tuples of (row, col)
    """
    rows, cols = len(grid), len(grid[0])
    
    # Validation: start/end within bounds and not on an obstacle
    for r, c in [start, end]:
        if not (0 <= r < rows and 0 <= c < cols) or grid[r][c] == 1:
            path : list = [] 
            return path

    queue = deque([start])
    parent_map = {start: None} # Tracks path lineage
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    
    while queue:
        curr = queue.popleft()
        
        if curr == end:
            # Reconstruct path from end to start
            path : list = []
            while curr is not None:
                path.append(curr)
                curr = parent_map[curr]
            return path[::-1] # Start to End
            
        for dr, dc in directions:
            nr, nc = curr[0] + dr, curr[1] + dc
            
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr][nc] == 0 and (nr, nc) not in parent_map:
                
                parent_map[(nr, nc)] = curr
                queue.append((nr, nc))

    path : list = []       
    return path

def get_grid_index(x, y, gridsize):

    offset = gridsize / 2

    # Calculate indices
    col = round((x - offset) / gridsize)
    row = round((y - offset) / gridsize)

    # Boundary check
    col = max(0, min(col, offset - 1))
    row = max(0, min(row, offset - 1))

    coord : tuple = (col, row)
    return coord

def get_centre_pos_from_idx(coord, gridsize):
    # multiply both by gridsize then add half to for the centre
    pos : tuple = (coord[0]*gridsize+gridsize*0.5, coord[1]*gridsize+gridsize*0.5)
    return pos

if __name__ == "__main__":
    print("This is a utility file, not meant to be run directly")

    # Example Usage
    grid = [
        [0, 0, 1, 0],
        [1, 0, 1, 0],
        [0, 0, 0, 0],
        [0, 1, 1, 0]
    ]

    grid = [
        [0,1,1,1,1,1,1,1,1,1,1],
        [0,1,0,0,0,0,0,0,0,0,1],
        [0,1,0,0,0,0,0,0,0,0,1],
        [0,1,0,0,0,0,0,0,0,0,1],
        [0,1,0,0,0,0,0,0,0,0,1],
        [0,1,1,1,1,0,0,0,0,1,1]
    ]

    path = find_path(grid, (2,2), (5,5))
    print(f"Path coordinates: {path}")