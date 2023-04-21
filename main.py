import pygame
import sys
import random


pygame.init()

WIDTH = 350
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("nFactorial Test Game")

WHITE = (255, 255, 255)

IMAGE_SIZE = 35
image_list = ['rock.png', 'scissors.png', 'scroll.png']


class GameObject:
    def __init__(self, x, y, speed_x, speed_y, image, type, hitbox_scale=0.8):
        self.x = x
        self.y = y
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.image = image
        hitbox_width = int(image.get_width() * hitbox_scale)
        hitbox_height = int(image.get_height() * hitbox_scale)
        hitbox_x_offset = (image.get_width() - hitbox_width) // 2
        hitbox_y_offset = (image.get_height() - hitbox_height) // 2
        self.rect = pygame.Rect(x + hitbox_x_offset, y + hitbox_y_offset, hitbox_width, hitbox_height)
        self.type = type

    def move(self):
        self.x += self.speed_x
        self.y += self.speed_y
        self.rect.x = self.x
        self.rect.y = self.y

    def change_direction(self):
        self.speed_x = -self.speed_x
        self.speed_y = -self.speed_y

    def change_type(self, type_):
        match self.type:
            case "scissors":
                if type_ == "rock":
                    self.type = "rock"
                    self.image = pygame.transform.scale(pygame.image.load("rock.png"), (IMAGE_SIZE, IMAGE_SIZE))
            case "rock":
                if type_ == "scroll":
                    self.type = "scroll"
                    self.image = pygame.transform.scale(pygame.image.load("scroll.png"), (IMAGE_SIZE, IMAGE_SIZE))
            case "scroll":
                if type_ == "scissors":
                    self.type = "scissors"
                    self.image = pygame.transform.scale(pygame.image.load("scissors.png"), (IMAGE_SIZE, IMAGE_SIZE))
            case _:
                return


def all_same_object(logos):
    type_ = logos[0].type
    return all(logo.type == type_ for logo in logos)


num_images = random.randint(10, 50)
objects = []
for _ in range(num_images):
    x = random.randint(0, WIDTH - IMAGE_SIZE)
    y = random.randint(0, HEIGHT - IMAGE_SIZE)
    speed_x = 0.5
    speed_y = 0.5
    image_name = random.choice(image_list)
    image_surf = pygame.image.load(f"{image_name}")
    image_surf = pygame.transform.scale(image_surf, (IMAGE_SIZE, IMAGE_SIZE))
    game_object = GameObject(x, y, speed_x, speed_y, image_surf, image_name.split(".")[0])
    objects.append(game_object)


running = True
same_type = False
while running:
    screen.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            sys.exit()

    for game_object in objects:
        game_object.move()

        if game_object.x <= 0 or game_object.x + IMAGE_SIZE >= WIDTH:
            game_object.speed_x = -game_object.speed_x
            game_object.x = max(0, min(game_object.x, WIDTH - IMAGE_SIZE))
            game_object.rect.x = game_object.x + (game_object.image.get_width() - game_object.rect.width) // 2
        if game_object.y <= 0 or game_object.y + IMAGE_SIZE >= HEIGHT:
            game_object.speed_y = -game_object.speed_y
            game_object.y = max(0, min(game_object.y, HEIGHT - IMAGE_SIZE))
            game_object.rect.y = game_object.y + (game_object.image.get_height() - game_object.rect.height) // 2

        for other_object in objects:
            if game_object != other_object and game_object.rect.colliderect(other_object.rect):
                game_object.change_direction()
                game_object.change_type(other_object.type)
                other_object.change_direction()
                other_object.change_type(game_object.type)

                overlap_x = game_object.rect.clip(other_object.rect).width
                overlap_y = game_object.rect.clip(other_object.rect).height

                if overlap_x < overlap_y:
                    min_overlap = overlap_x
                    separation_axis = "x"
                else:
                    min_overlap = overlap_y
                    separation_axis = "y"

                separation_distance = min_overlap / 2
                if separation_axis == "x":
                    if game_object.rect.centerx < other_object.rect.centerx:
                        game_object.x -= separation_distance
                        other_object.x += separation_distance
                    else:
                        game_object.x += separation_distance
                        other_object.x -= separation_distance
                else:
                    if game_object.rect.centery < other_object.rect.centery:
                        game_object.y -= separation_distance
                        other_object.y += separation_distance
                    else:
                        game_object.y += separation_distance
                        other_object.y -= separation_distance

                game_object.rect.x = game_object.x + (game_object.image.get_width() - game_object.rect.width) // 2
                game_object.rect.y = game_object.y + (game_object.image.get_height() - game_object.rect.height) // 2
                other_object.rect.x = other_object.x + (other_object.image.get_width() - other_object.rect.width) // 2
                other_object.rect.y = other_object.y + (other_object.image.get_height() - other_object.rect.height) // 2

    if all_same_object(objects):
        running = False
        same_type = True

    for game_object in objects:
        screen.blit(game_object.image, (game_object.x, game_object.y))

    pygame.display.flip()

    pygame.time.delay(10)

if same_type:
    image = objects[0].image
    screen.fill(WHITE)
    screen.blit(image, ((WIDTH - image.get_width()) // 2, (HEIGHT - image.get_height()) // 2))
    pygame.display.flip()
    pygame.time.delay(30000)

pygame.quit()
