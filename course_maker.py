import math

import pygame

import util

pygame.init()


class NoRowColExists(Exception):
    pass


SCREEN_SIZE = 1000, 750
TILE_WIDTH = 128
ROWS = 30
COLS = 30
MAX_COURSE_SIZE = COLS*TILE_WIDTH, ROWS*TILE_WIDTH
SCREEN_START_POS = TILE_WIDTH*10, TILE_WIDTH*10

PYGAME_NUM_KEYS = pygame.K_0, pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6, pygame.K_7, pygame.K_8, pygame.K_9


window = util.Window(SCREEN_SIZE, "Course Maker")
screen_rect = pygame.Rect(
    SCREEN_START_POS[0], SCREEN_START_POS[1], SCREEN_SIZE[0], SCREEN_SIZE[1])

BG_TILE = util.load_image("background_blue", "assets")
HOVER_SURF = pygame.Surface((TILE_WIDTH, TILE_WIDTH))
HOVER_SURF.fill(util.Color.WHITE)
HOVER_SURF.set_alpha(100)


def from_world_coords(world_pos: tuple[int, int]) -> tuple[int, int]:
    return world_pos[0] - screen_rect.x, world_pos[1] - screen_rect.y


def to_world_coords(screen_pos: tuple[int, int]) -> tuple[int, int]:
    return screen_pos[0] + screen_rect.x, screen_pos[1] + screen_rect.y


def load_block_images() -> list[pygame.Surface]:
    block_images = []
    for file_number in range(0, 11):
        block_images.append(util.load_image(str(file_number),
                                            "assets/blocks", convert=True))
    return block_images


def render_blocks(blocks: dict[str, any], screen: pygame.Surface) -> None:
    for block in blocks:
        image = util.load_image(str(block["type"]), "assets/blocks")
        pos = from_world_coords(
            (block["col"]*TILE_WIDTH, block["row"]*TILE_WIDTH))
        screen.blit(image, pos)


def get_row_col(world_pos: tuple[int, int]) -> tuple[int, int]:
    row = math.floor(world_pos[1]/TILE_WIDTH)
    col = math.floor(world_pos[0]/TILE_WIDTH)
    if row >= ROWS or col >= COLS:
        raise NoRowColExists()
    return row, col


block_images = load_block_images()
blocks = [{"type": 9, "row": 2, "col": 5}]
block_type_to_be_generated = 0

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key in PYGAME_NUM_KEYS:
                block_type_to_be_generated = PYGAME_NUM_KEYS.index(event.key)

    if pygame.mouse.get_pressed() == (1, 0, 0):
        row, col = get_row_col(to_world_coords(mouse_pos))
        for block in blocks:
            if block["row"] == row and block["col"] == col:
                break
        else:
            blocks.append({
                "type": block_type_to_be_generated,
                "row": row,
                "col": col
            })
        print(len(blocks))
    elif pygame.mouse.get_pressed() == (0, 0, 1):
        row, col = get_row_col(to_world_coords(mouse_pos))
        for block in blocks:
            if block["row"] == row and block["col"] == col:
                blocks.remove(block)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_UP]:
        screen_rect.y -= 10
    if keys[pygame.K_DOWN]:
        screen_rect.y += 10
    if keys[pygame.K_LEFT]:
        screen_rect.x -= 10
    if keys[pygame.K_RIGHT]:
        screen_rect.x += 10

    for row in range(ROWS):
        bottom_y = TILE_WIDTH*(row+1)
        top_y = bottom_y - TILE_WIDTH
        if bottom_y < screen_rect.top:
            continue
        if top_y > screen_rect.bottom:
            continue
        for col in range(COLS):
            right_x = TILE_WIDTH*(col+1)
            left_x = right_x - TILE_WIDTH
            if right_x < screen_rect.left:
                continue
            if left_x > screen_rect.right:
                continue
            window.screen.blit(BG_TILE, from_world_coords((
                col*TILE_WIDTH, row*TILE_WIDTH)))

    render_blocks(blocks, window.screen)

    try:
        row, col = get_row_col(to_world_coords(mouse_pos))
        window.screen.blit(HOVER_SURF, from_world_coords(
            (col*TILE_WIDTH, row*TILE_WIDTH)))
    except NoRowColExists:
        pass

    window.update()
