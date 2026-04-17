import pygame
import datetime
import os
from clock import rotate_center


pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Mickey's Clock")
game_clock = pygame.time.Clock()


background = pygame.transform.scale(pygame.image.load("9/mickeys_clock/images/clock.png").convert_alpha(), (600, 600))
mickey_body = pygame.transform.scale(pygame.image.load("9/mickeys_clock/images/mUmrP.png").convert_alpha(), (600, 600))
right_hand = pygame.transform.scale(pygame.image.load("9/mickeys_clock/images/right-hand.png").convert_alpha(), (230, 500))
left_hand = pygame.transform.scale(pygame.image.load("9/mickeys_clock/images/left-hand.png").convert_alpha(), (230, 500))


CENTER = (350, 350)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    now = datetime.datetime.now()
    seconds = now.second
    minutes = now.minute

    sec_angle = -((seconds) * 6)
    min_angle = -((minutes + (seconds / 60)) *6)

    screen.fill((255, 255, 255))

    screen.blit(background, (50, 50))
    screen.blit(mickey_body, (50, 50))

    rot_min, min_rect = rotate_center(left_hand, min_angle, CENTER)
    screen.blit(rot_min, min_rect)

    rot_sec, sec_rect = rotate_center(right_hand, sec_angle, CENTER)
    screen.blit(rot_sec, sec_rect)

    pygame.display.flip()

pygame.quit()