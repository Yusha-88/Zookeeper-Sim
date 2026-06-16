import pygame
import random
import time

from pygame.math import Vector2

pygame.init()

screen = pygame.display.set_mode((1280,720))
SCREEN_MIN_WIDTH = 0
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
flip_image = False

# Sounds and music
penguin_squeak = pygame.mixer.Sound('sounds/penguin_squeak.wav')
elephant_sound = pygame.mixer.Sound('sounds/elephant_sound.mp3')
eating_sound = pygame.mixer.Sound('sounds/eating_sound.wav')
penguin_sounds = [penguin_squeak]
elephant_sounds = [elephant_sound]

# Creating timed events of Pygame's queue
penguin_move_event = pygame.USEREVENT + 1
penguin_move_time_ms = random.randint(1000,5000)
pygame.time.set_timer(penguin_move_event, penguin_move_time_ms)
# Timed event for draining animal's hunger
penguin_hunger_event = pygame.USEREVENT + 2
pygame.time.set_timer(penguin_hunger_event, 5000) #Change back to 30000

class Animal:
    def __init__(self, species, x_pos, y_pos, height, width, colour, movement_speed, sounds, animal_sprite_sheet, hunger=100):
        self.species = species
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.x_direction = 0
        self.y_direction = 0
        self.height = height
        self.width = width
        self.colour = colour
        self.movement_speed = movement_speed
        self.starting_movement_speed = movement_speed
        self.sounds = sounds
        if hunger < 100:
            raise ValueError("Hunger must be equal to or greater than 100")
        self.hunger = hunger
        self.starting_hunger = hunger # Used to compare in-game hunger level to it's initial level via react_to_hunger
        self.alive = True
        self.animalRect = pygame.Rect(x_pos, y_pos, height, width)
        self.animal_sprite_sheet = animal_sprite_sheet
        self.image = ''

    def display(self, frame):
        # self.animalRect = pygame.draw.rect(screen,self.colour, self.animalRect)
        scale = 3
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        self.image.blit(self.animal_sprite_sheet, (0, 0), (self.width * frame, 0, self.width, self.height))
        self.image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))
        return self.image

    # TODO: Might need to make the constants into arguments to allow for custom boundaries for different animals
    def move(self):
        if self.alive:
            self.movement_speed = random.randint(0,self.starting_movement_speed+1)
            x_direction = random.randint(-1,1)
            y_direction = random.randint(-1, 1)
            # Comment out below to control NPCs for screen boundary testing
            # x_direction = 1
            # y_direction = -1
            self.animalRect.x += self.movement_speed * x_direction
            self.animalRect.y += self.movement_speed * y_direction

    def check_boundary(self, min_height, max_height, min_width, max_width):
        if self.animalRect.y <= min_height:
            self.animalRect.y = 5
        if self.animalRect.y >= max_height - (self.width + 40):
            self.animalRect.y = max_height - (self.width + 40)
        if self.animalRect.x <= min_width:
            self.animalRect.x = 5
        if self.animalRect.x >= max_width - (self.height + 40):
            self.animalRect.x = max_width - (self.height + 40)
        print(f"{self.species} Movement Logging: x: {self.animalRect.x}, y: {self.animalRect.y}, movement_speed:{self.movement_speed}")

    def drain_hunger(self):
        if self.hunger > 0:
            self.hunger = self.hunger - 10
            print(f"{self.species} Hunger: {self.hunger}")

    def react_to_hunger(self):
        if self.alive:
            if self.hunger == (self.starting_hunger * 0.5):
                self.starting_movement_speed = int(self.starting_movement_speed * 0.75)
                self.ask_for_food()
                print(f"{self.species} is hungry! Movement speed: {self.starting_movement_speed}")
            elif self.hunger == (self.starting_hunger * 0.2):
                self.starting_movement_speed = int(self.starting_movement_speed * 0.50)
                print(f"{self.species} is starving! Movement speed: {self.starting_movement_speed}")
                self.cry_for_food()
            elif self.hunger == 0:
                self.alive = False
                self.colour = "Black"
                print(f"{self.species} has died of starvation!")

    def ask_for_food(self):
        pygame.mixer.Sound.play(self.sounds[0])

    def cry_for_food(self):
        loop_no = random.randint(1,3)
        pygame.mixer.Sound.play(self.sounds[0], loop_no)

    def eat_food(self):
        if self.alive:
            if self.hunger < (self.starting_hunger * 0.7):
                self.hunger = self.starting_hunger
                pygame.mixer.Sound.play(eating_sound)
                print(f"{self.species} hunger level: {self.hunger}. {self.species} fed!")
            else:
                print(f"{self.species} is full!")
        else:
            print(f"{self.species} is dead.")

class Zookeeper(pygame.sprite.Sprite):
    def __init__(self, x_pos, y_pos, height, width, colour, movement_speed):
        super().__init__()
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.height = height
        self.width = width
        self.colour = colour
        self.movement_speed = movement_speed
        self.zookeeper_sprite_sheet = pygame.image.load("images/DinoSprites.png").convert_alpha()
        self.image = ''
        # Rect of the zookeeper
        self.zookeeperRect = pygame.Rect(x_pos,y_pos, height, width)

    def display(self, frame):
        scale = 3
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA).convert_alpha()
        self.image.blit(self.zookeeper_sprite_sheet, (0, 0), (self.width * frame, 0, self.width, self.height))
        self.image = pygame.transform.scale(self.image, (self.width * scale, self.height * scale))
        return self.image

    def move(self, x_direction, y_direction):
        self.zookeeperRect.x += self.movement_speed * x_direction
        self.zookeeperRect.y += self.movement_speed * y_direction
        print(f"Zookeeper x-position: {self.zookeeperRect.x}, y_position: {self.zookeeperRect.y}, right: {self.zookeeperRect.right}, height: {self.zookeeperRect.width}, width: {self.zookeeperRect.height}")

    def collide(self, animal):
        if (self.zookeeperRect.right - animal.animalRect.left) < (self.zookeeperRect.bottom - animal.animalRect.top):
            self.zookeeperRect.right = animal.animalRect.left
        elif (animal.animalRect.right - self.zookeeperRect.left) < (self.zookeeperRect.bottom - animal.animalRect.top):
            self.zookeeperRect.left = animal.animalRect.right
        elif animal.animalRect.top < self.zookeeperRect.bottom < animal.animalRect.bottom:
            self.zookeeperRect.bottom = animal.animalRect.top
        elif animal.animalRect.top < self.zookeeperRect.top < animal.animalRect.bottom and self.zookeeperRect.bottom > animal.animalRect.top:
            self.zookeeperRect.top = animal.animalRect.bottom

    def check_boundary(self, min_width, max_width, min_height, max_height):
        if self.zookeeperRect.x <= min_width:
            self.zookeeperRect.x = min_width
        if self.zookeeperRect.x >= max_width - (self.zookeeperRect.height+40):
            self.zookeeperRect.x = max_width - (self.zookeeperRect.height+40)
        if self.zookeeperRect.y <= min_height:
            self.zookeeperRect.y = min_height
        if self.zookeeperRect.y >= max_height - (self.zookeeperRect.width+40):
            self.zookeeperRect.y = max_height - (self.zookeeperRect.width+40)

    def feed(self, animal):
        distance_to_animal = Vector2(self.zookeeperRect.center).distance_to(animal.animalRect.center)
        if distance_to_animal < 60:
            return True
        else:
            return False

zookeeper = Zookeeper(ZOOKEEPER_STARTING_X_POS, ZOOKEEPER_STARTING_Y_POS, 24, 24, "white", 5)
penguin = Animal("Penguin", 10, 10, 35, 64, "white", 10,penguin_sounds, pygame.image.load("images/penguin_simple.png").convert_alpha(), 100)
elephant = Animal("Elephant", 1200, 600, 24, 24, "grey", 10, elephant_sounds, pygame.image.load("images/DinoSprites.png").convert_alpha(), 200)
current_animals_in_game = [penguin, elephant]

# Create animation list
animation_list = []
animation_list_penguin = []
animation_list_elephant = []
animation_step = [4,6]
action = 0 # This picks a set of animation from animation list
previous_action = action
animal_action = 0 # Same as above but for the Animal NPCs
previous_animal_action = 0
step_counter = 0 # Used to iterate through the nested animation for loop
last_update = pygame.time.get_ticks()
cooldown = 100
frame = 0
penguin_frame = 0
elephant_frame = 0
current_zookeeper_image = ""
previous_key = ""

# Add first four images in sheet to animation list for an idle animation
for animation in animation_step:
    temp_img_list = []
    temp_img_list2 = []
    temp_img_list3 = []
    for _ in range(animation):
        temp_img_list.append(zookeeper.display(step_counter))
        temp_img_list2.append(penguin.display(step_counter))
        temp_img_list3.append(elephant.display(step_counter))
        step_counter += 1
    animation_list.append(temp_img_list)
    animation_list_penguin.append(temp_img_list2)
    animation_list_elephant.append(temp_img_list3)

while game_running:
    keys = pygame.key.get_pressed()

    animal_action = 0
    for event in pygame.event.get():
        if event.type == pygame.QUIT or keys[pygame.K_ESCAPE]:
            pygame.quit()
            raise SystemExit
        elif event.type == penguin_move_event:
            for animal in current_animals_in_game:
                animal.move()
                animal_action = 1
        elif event.type == penguin_hunger_event:
            for animal in current_animals_in_game:
                animal.drain_hunger()
                animal.react_to_hunger()

    # Reset frame to stop it from starting mid-iteration and going out of bounds
    if animal_action != previous_animal_action:
        penguin_frame = 0
        elephant_frame = 0
        previous_animal_action = animal_action

    # # Do logical updates here.
    action = 0 # Reset action to stop infinite animation loop
    if zookeeper.zookeeperRect.colliderect(penguin.animalRect):
        zookeeper.collide(penguin)
        if keys[pygame.K_e]:
            penguin.eat_food()
    if zookeeper.zookeeperRect.colliderect(elephant.animalRect):
        zookeeper.collide(elephant)
        if keys[pygame.K_e]:
            elephant.eat_food()
    if keys[pygame.K_d]:
        zookeeper.move(1, 0)
        action = 1
        previous_key = "d"
    if keys[pygame.K_a]:
        zookeeper.move(-1, 0)
        action = 1
        previous_key = "a"
    if keys[pygame.K_w]: #and zookeeper.zookeeperRect.y > SCREEN_MIN_HEIGHT:
        zookeeper.move(0, -1)
        action = 1
    if keys[pygame.K_s]: #and zookeeper.zookeeperRect.y < SCREEN_MAX_HEIGHT - zookeeper.height:
        zookeeper.move(0, 1)
        action = 1

    # Reset frame to stop it from starting mid-iteration and going out of bounds
    if action != previous_action:
        frame = 0
        previous_action = action

    # This stops zookeeper from leaving boundary when colliding with animal
    zookeeper.check_boundary(SCREEN_MIN_WIDTH, SCREEN_MAX_WIDTH, SCREEN_MIN_HEIGHT, SCREEN_MAX_HEIGHT)

    screen.fill(ZOO_BACKGROUND_COLOUR)  # Fill the display with a solid colour

    # Update animation
    current_time = pygame.time.get_ticks()
    if current_time - last_update >= cooldown:
        frame += 1
        penguin_frame += 1
        elephant_frame += 1
        last_update = current_time
        if frame >= len(animation_list[action]):
            frame = 0
        if penguin_frame >= len(animation_list_penguin[animal_action]):
            penguin_frame = 0
        if elephant_frame >= len(animation_list_elephant[animal_action]):
            elephant_frame = 0

    # Show zookeeper frame
    current_zookeeper_image = animation_list[action][frame]
    current_penguin_image = animation_list_penguin[animal_action][penguin_frame]
    current_elephant_image = animation_list_elephant[animal_action][elephant_frame]

    # Flip the zookeeper sprite in the direction of movement
    if previous_key == "a":
        current_zookeeper_image = pygame.transform.flip(current_zookeeper_image, True, False)
    screen.blit(current_zookeeper_image, zookeeper.zookeeperRect)
    if penguin.alive:
        screen.blit(current_penguin_image, penguin.animalRect)
    else: # Show death sprite
        penguin_death_sprite = pygame.transform.grayscale(animation_list_penguin[0][0])
        screen.blit(penguin_death_sprite, penguin.animalRect)
    if elephant.alive:
        screen.blit(current_elephant_image, elephant.animalRect)
    else:
        elephant_death_sprite = pygame.transform.grayscale(animation_list_elephant[0][0])
        screen.blit(elephant_death_sprite, elephant.animalRect)

    # Below is for testing purposes
    # length = len(animation_list[action])
    # print(f"action: {action}, frame: {frame}, length: {length}")

    for animal in current_animals_in_game:
        # Stops animal from leaving screen
        animal.check_boundary(SCREEN_MIN_HEIGHT, SCREEN_MAX_HEIGHT, SCREEN_MIN_WIDTH, SCREEN_MAX_WIDTH)
        if zookeeper.feed(animal) and keys[pygame.K_e]:
            animal.eat_food()

    pygame.display.flip()  # Refresh on-screen display
    clock.tick(60)         # wait until next frame (at 60 FPS)