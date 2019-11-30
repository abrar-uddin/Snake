import pygame
import random

pygame.init()
pygame.font.init()

# GLOBALS VARS

# Color
black = (0, 0, 0)
red = (255, 0, 0)
green = (0, 255, 0)

# Screen Dimensions
screen_width = 500
screen_height = 500

# Snake Dimensions
snake_width = 10
snake_height = 10
snake_margin = 3

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Snake')


class Food(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([snake_width, snake_height])
        self.image.fill(green)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


class Blocks(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()

        # Set height, width
        self.image = pygame.Surface([snake_width, snake_height])
        self.image.fill(red)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y


def spawn_food(x, y):
    return Food(x, y)


def message(msg,color):
    font = pygame.font.SysFont('solpro', 50, bold=True)
    mesg = font.render(msg, True, color)
    font_size = font.size(msg)
    screen.blit(mesg, [screen_width/2 - font_size[0]/2, screen_height/2 - font_size[1]/2])


def main():
    run = True

    # Initial Speed
    dy_x = snake_width + snake_margin
    dy_y = 0

    all_sprites = pygame.sprite.Group()
    food_sprite = pygame.sprite.GroupSingle()
    snake_blocks = []

    block = Blocks(250, 250)
    snake_blocks.append(block)
    all_sprites.add(block)

    clock = pygame.time.Clock()

    while run:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                quit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    dy_x = (snake_width + snake_margin) * -1
                    dy_y = 0
                if event.key == pygame.K_RIGHT:
                    dy_x = (snake_width + snake_margin)
                    dy_y = 0
                if event.key == pygame.K_UP:
                    dy_x = 0
                    dy_y = (snake_width + snake_margin) * -1
                if event.key == pygame.K_DOWN:
                    dy_x = 0
                    dy_y = (snake_width + snake_margin)

        if len(snake_blocks) == 1:
            # Get rid of last segment of the snake
            old_segment = snake_blocks.pop()
            all_sprites.remove(old_segment)

            # Figure out where new segment will be
            x = old_segment.rect.x + dy_x
            y = old_segment.rect.y + dy_y
            block = Blocks(x, y)

            # Collision Detection
            if pygame.sprite.spritecollide(block, all_sprites, False) or \
                    (block.rect.x < 0 or block.rect.y < 0) or \
                    (block.rect.x > 500 or block.rect.y > 500):
                lost = True
                while lost:
                    message("You lost!", red)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            pygame.display.quit()
                            quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                main()

            # Insert new segment into the list
            snake_blocks.insert(0, block)
            all_sprites.add(block)
        else:
            # Get rid of last segment of the snake
            old_segment = snake_blocks.pop()
            all_sprites.remove(old_segment)

            # Figure out where new segment will be
            x = snake_blocks[0].rect.x + dy_x
            y = snake_blocks[0].rect.y + dy_y
            block = Blocks(x, y)

            # Collision Detection
            if pygame.sprite.spritecollide(block, all_sprites, False) or \
                    (block.rect.x < 0 or block.rect.y < 0) or \
                    (block.rect.x > 500 or block.rect.y > 500):
                lost = True
                while lost:
                    message("You lost!", red)
                    pygame.display.update()
                    for event in pygame.event.get():
                        if event.type == pygame.QUIT:
                            run = False
                            pygame.display.quit()
                            quit()
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE:
                                main()

            # Insert new segment into the list
            snake_blocks.insert(0, block)
            all_sprites.add(block)

        if not food_sprite:
            food = spawn_food(random.randrange(350), random.randrange(350))
            food_sprite.add(food)

        if pygame.sprite.groupcollide(all_sprites, food_sprite, False, True, collided=None):
            food_sprite.empty()
            block = Blocks(snake_blocks[0].rect.x + dy_x,
                           snake_blocks[0].rect.y + dy_y)
            snake_blocks.insert(0, block)
            all_sprites.add(block)

        # Draw everything
        # Clear screen
        screen.fill(black)

        all_sprites.draw(screen)
        food_sprite.draw(screen)

        # Flip screen
        pygame.display.flip()

        # Pause
        clock.tick(10)


main()
