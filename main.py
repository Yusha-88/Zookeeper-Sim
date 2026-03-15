import pygame

pygame.init()

screen = pygame.display.set_mode((1280,720))
SCREEN_MIN_WIDTH = 0
SCREEN_MAX_WIDTH = 1280
SCREEN_MIN_HEIGHT = 0
SCREEN_MAX_HEIGHT = 720

clock = pygame.time.Clock()

game_running = True

# Initialising variables
ZOO_BACKGROUND_COLOUR = (126, 200, 80) # Light green
ZOOKEEPER_STARTING_X_POS = 30
ZOOKEEPER_STARTING_Y_POS = 30
x_direction = 0
y_direction = 0

# TODO: Implement Animal class

# TODO: Implement Zookeeper class
class Zookeeper:
    def __init__(self, x_pos, y_pos, height, width, colour, movement_speed):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.height = height
        self.width = width
        self.colour = colour
        self.movement_speed = movement_speed

        # Rect of the zookeeper
        self.zookeeperRect = pygame.Rect(x_pos,y_pos, height, width)
        # Blit of zookeeper to screen
        self.zookeeperRect = pygame.draw.rect(screen, self.colour, self.zookeeperRect)

    def display(self):
        self.zookeeperRect = pygame.draw.rect(screen, self.colour, self.zookeeperRect)

    def move(self, x_direction, y_direction):
        self.zookeeperRect.x += self.movement_speed * x_direction
        self.zookeeperRect.y += self.movement_speed * y_direction

zookeeper = Zookeeper(ZOOKEEPER_STARTING_X_POS, ZOOKEEPER_STARTING_Y_POS, 20, 20, "white", 10)

while game_running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            raise SystemExit

    # Do logical updates here.
    if keys[pygame.K_d] and zookeeper.zookeeperRect.x < SCREEN_MAX_WIDTH - zookeeper.width:
        zookeeper.move(1, 0)
    if keys[pygame.K_a] and zookeeper.zookeeperRect.x > SCREEN_MIN_WIDTH:
        zookeeper.move(-1, 0)
    if keys[pygame.K_w] and zookeeper.zookeeperRect.y > SCREEN_MIN_HEIGHT:
        zookeeper.move(0, -1)
    if keys[pygame.K_s] and zookeeper.zookeeperRect.y < SCREEN_MAX_HEIGHT - zookeeper.height:
        zookeeper.move(0, 1)

    screen.fill(ZOO_BACKGROUND_COLOUR)  # Fill the display with a solid color

    # Render the graphics here.
    zookeeper.display()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)