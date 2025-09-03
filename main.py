import argparse
import random
import pygame

TILE_SIZE = 16
MAP_DATA = [
    "1111111111",
    "1000000001",
    "1022222001",
    "1000000001",
    "1000030001",
    "1000030001",
    "1000000001",
    "1000000001",
    "1111111111",
]
WALKABLE = {"0", "3"}

def create_tiles():
    tiles = {}
    # Grass
    grass = pygame.Surface((TILE_SIZE, TILE_SIZE))
    grass_colors = [(63, 142, 49), (75, 160, 60)]
    for y in range(TILE_SIZE):
        for x in range(TILE_SIZE):
            grass.set_at((x, y), random.choice(grass_colors))
    tiles["0"] = grass
    # Tree / wall
    wall = pygame.Surface((TILE_SIZE, TILE_SIZE))
    wall.fill((34, 139, 34))
    pygame.draw.rect(wall, (0, 100, 0), wall.get_rect(), 2)
    tiles["1"] = wall
    # Water
    water = pygame.Surface((TILE_SIZE, TILE_SIZE))
    for y in range(TILE_SIZE):
        for x in range(TILE_SIZE):
            color = (0, 105, 148) if (x + y) % 3 else (0, 90, 130)
            water.set_at((x, y), color)
    tiles["2"] = water
    # Path
    path = pygame.Surface((TILE_SIZE, TILE_SIZE))
    path.fill((193, 154, 107))
    pygame.draw.line(path, (173, 134, 87), (0, 0), (TILE_SIZE - 1, 0))
    tiles["3"] = path
    return tiles

def create_player_sprite():
    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
    # head
    pygame.draw.rect(surf, (255, 224, 189), (4, 0, 8, 8))
    # tunic
    pygame.draw.rect(surf, (0, 128, 0), (2, 8, 12, 8))
    # boots
    pygame.draw.rect(surf, (139, 69, 19), (2, 14, 12, 2))
    return surf

def can_move(rect):
    width = len(MAP_DATA[0])
    height = len(MAP_DATA)
    for px, py in (
        (rect.left, rect.top),
        (rect.right - 1, rect.top),
        (rect.left, rect.bottom - 1),
        (rect.right - 1, rect.bottom - 1),
    ):
        tx = px // TILE_SIZE
        ty = py // TILE_SIZE
        if not (0 <= tx < width and 0 <= ty < height):
            return False
        if MAP_DATA[ty][tx] not in WALKABLE:
            return False
    return True

class Player:
    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, TILE_SIZE, TILE_SIZE)
        self.image = create_player_sprite()
        self.speed = 2

    def handle_input(self, keys):
        move = pygame.Vector2(0, 0)
        if keys[pygame.K_LEFT]:
            move.x = -self.speed
        elif keys[pygame.K_RIGHT]:
            move.x = self.speed
        if keys[pygame.K_UP]:
            move.y = -self.speed
        elif keys[pygame.K_DOWN]:
            move.y = self.speed

        new_rect = self.rect.move(move.x, 0)
        if move.x and can_move(new_rect):
            self.rect = new_rect
        new_rect = self.rect.move(0, move.y)
        if move.y and can_move(new_rect):
            self.rect = new_rect

def draw_map(surface, tiles):
    for y, row in enumerate(MAP_DATA):
        for x, tile in enumerate(row):
            surface.blit(tiles[tile], (x * TILE_SIZE, y * TILE_SIZE))

def main(frames=None):
    pygame.init()
    map_width = len(MAP_DATA[0]) * TILE_SIZE
    map_height = len(MAP_DATA) * TILE_SIZE
    window = pygame.display.set_mode((map_width * 4, map_height * 4))
    game_surface = pygame.Surface((map_width, map_height))
    clock = pygame.time.Clock()

    tiles = create_tiles()
    player = Player(5 * TILE_SIZE, 5 * TILE_SIZE)

    running = True
    frame_count = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        player.handle_input(keys)

        draw_map(game_surface, tiles)
        game_surface.blit(player.image, player.rect)

        scaled = pygame.transform.scale(game_surface, window.get_size())
        window.blit(scaled, (0, 0))
        pygame.display.flip()
        clock.tick(60)
        frame_count += 1
        if frames is not None and frame_count >= frames:
            running = False
    pygame.quit()

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--frames", type=int, help="Number of frames to run (for tests)")
    args = parser.parse_args()
    main(frames=args.frames)
