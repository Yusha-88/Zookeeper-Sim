import pygame
import random
import time

pygame.init()

screen = pygame.display.set_mode((1280,720))
SCREEN_MIN_WIDTH = 2
SCREEN_MAX_WIDTH = 1280
SCREEN_MIN_HEIGHT = 2
SCREEN_MAX_HEIGHT = 720

pygame.display.set_caption("Zookeeper")

clock = pygame.time.Clock()

game_running = True

# Initialising variables
ZOO_BACKGROUND_COLOUR = (126, 200, 80) # Light green
ZOOKEEPER_STARTING_X_POS = 30
ZOOKEEPER_STARTING_Y_POS = 30
x_direction = 0
y_direction = 0

# Creating timed events of Pygame's queue
penguin_move_event = pygame.USEREVENT + 1
penguin_move_time_ms = random.randint(1000,5000)
pygame.time.set_timer(penguin_move_event, penguin_move_time_ms)
# Timed event for draining animal's hunger
penguin_hunger_event = pygame.USEREVENT + 2
pygame.time.set_timer(penguin_hunger_event, 30000)

# TODO: Implement Animal class
class Animal:
    def __init__(self, species, x_pos, y_pos, height, width, colour, movement_speed):
        self.species = species
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.height = height
        self.width = width
        self.colour = colour
        self.movement_speed = movement_speed
        self.hunger = 100.0

        self.animalRect = pygame.Rect(x_pos, y_pos, height, width)
        # Blit of animal to screen
        self.animalRect = pygame.draw.rect(screen, self.colour, self.animalRect)

    def display(self):
        self.animalRect = pygame.draw.rect(screen,self.colour, self.animalRect)

    def move(self):
        self.movement_speed = random.randint(0,self.movement_speed+1)
        x_direction = random.randint(-1,1)
        y_direction = random.randint(-1, 1)
        self.animalRect.x += self.movement_speed * 1
        self.animalRect.y += self.movement_speed * y_direction
        if self.animalRect.y <= SCREEN_MIN_HEIGHT:
            self.animalRect.y = 5
        if self.animalRect.y >= SCREEN_MAX_HEIGHT - self.height:
            self.animalRect.y = self.animalRect.y - 10
        if self.animalRect.x <= SCREEN_MIN_WIDTH:
            self.animalRect.x = 5
        if self.animalRect.x >= SCREEN_MAX_WIDTH - self.width:
            self.animalRect.x = self.animalRect.x - 10
        print(f"{self.species} Movement Logging: x: {self.animalRect.x}, y: {self.animalRect.y}, movement_speed:{self.movement_speed}")

    def drain_hunger(self):
        if self.hunger > 0:
            self.hunger = self.hunger - 10
        print(f"{self.species} Hunger: {self.hunger}")

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

    # TODO: Feed animal method

zookeeper = Zookeeper(ZOOKEEPER_STARTING_X_POS, ZOOKEEPER_STARTING_Y_POS, 20, 20, "white", 10)
penguin = Animal("Penguin", 4, 5, 10, 10, "white", 10)
penguin2 = Animal("Penguin", 1260, 50, 10, 10, "white", 10)
penguin_list = [penguin, penguin2]

while game_running:
    keys = pygame.key.get_pressed()

    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            raise SystemExit
        elif event.type == penguin_move_event:
            for penguin in penguin_list:
                penguin.move()
        elif event.type == penguin_hunger_event:
            for penguin in penguin_list:
                penguin.drain_hunger()

    # Do logical updates here.
    if keys[pygame.K_d] and zookeeper.zookeeperRect.x < SCREEN_MAX_WIDTH - zookeeper.width:
        zookeeper.move(1, 0)
    if keys[pygame.K_a] and zookeeper.zookeeperRect.x > SCREEN_MIN_WIDTH:
        zookeeper.move(-1, 0)
    if keys[pygame.K_w] and zookeeper.zookeeperRect.y > SCREEN_MIN_HEIGHT:
        zookeeper.move(0, -1)
    if keys[pygame.K_s] and zookeeper.zookeeperRect.y < SCREEN_MAX_HEIGHT - zookeeper.height:
        zookeeper.move(0, 1)

    screen.fill(ZOO_BACKGROUND_COLOUR)  # Fill the display with a solid colour

    # Render the graphics here.
    zookeeper.display()
    for penguin in penguin_list:
        penguin.display()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)