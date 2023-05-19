import pygame
import sys
import os

from . import seconds_to_time

CWDPATH = os.path.abspath(os.path.dirname(sys.argv[0]))


class RestTimer:
    def __init__(self, time, screen_height, screen_width):
        self.time = time
        self.countdown_seconds = time
        self.bell_sound = pygame.mixer.Sound(
            os.path.join(CWDPATH, 'sound', 'bell.wav'))
        self.count_down_font = pygame.font.Font(None, 400)
        self.time_info_font = pygame.font.Font(None, 50)
        self.box_rect = pygame.Rect(0, 0, 0, screen_height)
        self.count_down_rect_width = self.box_rect.width
        self.increment = screen_width / time / 60.00

    def handle_inputs(self, event, *args, **kwargs):
        if event.type == pygame.USEREVENT+1:
            self.countdown_seconds -= 1

    def update(self, screen, *args, **kwargs):
        if self.countdown_seconds <= 0:
            self.bell_sound.play()
            return True

        screen.fill("green")
        self.count_down_rect_width += self.increment
        self.box_rect.width = self.count_down_rect_width
        pygame.draw.rect(screen, "red", self.box_rect)

        screen_rect = screen.get_rect()

        elapsed_time_label_surf = self.time_info_font.render(
            "Resting", True, 'white')
        elapsed_time_label_rect = elapsed_time_label_surf.get_rect(
            center=(screen_rect.width/2, screen_rect.height/3))
        screen.blit(elapsed_time_label_surf, elapsed_time_label_rect)

        countdown_surface = self.count_down_font.render(
            seconds_to_time(self.countdown_seconds), True, 'white')
        countdown_rect = countdown_surface.get_rect(
            top=elapsed_time_label_rect.bottom, centerx=screen_rect.centerx)
        screen.blit(countdown_surface, countdown_rect)


class WorkTimer:
    def __init__(self, time, screen_height, screen_width):
        self.time = time
        self.countdown_seconds = time
        self.bell_sound = pygame.mixer.Sound(
            os.path.join(CWDPATH, 'sound', 'bell.wav'))
        self.count_down_font = pygame.font.Font(None, 400)
        self.time_info_font = pygame.font.Font(None, 50)
        self.box_rect = pygame.Rect(0, 0, 0, screen_height)
        self.count_down_rect_width = self.box_rect.width
        self.increment = screen_width / time / 60.00

    def handle_inputs(self, event, *args, **kwargs):
        if event.type == pygame.USEREVENT+1:
            self.countdown_seconds -= 1

    def update(self, screen, *args, **kwargs):
        if self.countdown_seconds <= 0:
            self.bell_sound.play()
            return True

        screen.fill("red")

        self.count_down_rect_width += self.increment
        self.box_rect.width = self.count_down_rect_width
        pygame.draw.rect(screen, "green", self.box_rect)

        screen_rect = screen.get_rect()

        elapsed_time_label_surf = self.time_info_font.render(
            "Working", True, 'white')
        elapsed_time_label_rect = elapsed_time_label_surf.get_rect(
            center=(screen_rect.width/2, screen_rect.height/3))
        screen.blit(elapsed_time_label_surf, elapsed_time_label_rect)

        countdown_surface = self.count_down_font.render(
            seconds_to_time(self.countdown_seconds), True, 'white')
        countdown_rect = countdown_surface.get_rect(
            top=elapsed_time_label_rect.bottom, centerx=screen_rect.centerx)
        screen.blit(countdown_surface, countdown_rect)
