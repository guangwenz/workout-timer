import pygame
import os
import sys

CWDPATH = os.path.abspath(os.path.dirname(sys.argv[0]))

WIDTH = 1280
HEIGHT = 960

SET_COUNT = 10
REPS = 2
REP_TIME = 30
REST_TIME = 30
TOTAL_INTERVALS = SET_COUNT * REPS * 2 - 1
TOTAL_SECONDS = SET_COUNT * REPS * REP_TIME + (SET_COUNT * REPS-1) * REST_TIME

TEXT_COLOR = 'white'
BG_COLOR = 'gray'
H_COLOR = 'green'
L_COLOR = 'red'
TIMER_EVT = pygame.USEREVENT


def seconds_to_time(seconds):
    min, sec = divmod(seconds, 60)
    hour, min = divmod(min, 60)
    if hour == 0:
        return '%02d:%02d' % (min, sec)
    else:
        return '%d:%02d:%02d' % (hour, min, sec)


def get_count_down_seconds(is_rest):
    return REST_TIME if is_rest else REP_TIME


def get_bg_color(is_rest):
    return L_COLOR if is_rest else H_COLOR


pygame.init()
bell_sound = pygame.mixer.Sound(os.path.join(CWDPATH, 'sound', 'bell.wav'))
applause_sound = pygame.mixer.Sound(
    os.path.join(CWDPATH, 'sound', 'applause.wav'))

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("HIIT Workout Timer")

clock = pygame.time.Clock()
pygame.time.set_timer(TIMER_EVT, 1000)
box_surf = pygame.Surface((0, HEIGHT))
box_rect = box_surf.get_rect()

count_down_font = pygame.font.Font(None, 400)
time_info_font = pygame.font.Font(None, 50)
elapsed_time_label_surf = time_info_font.render("ELAPSED", True, TEXT_COLOR)
remaining_time_label_surf = time_info_font.render(
    "REMAINING", True, TEXT_COLOR)
interval_label_surf = time_info_font.render("INTERVALS", True, TEXT_COLOR)

running = True
passed_seconds = 0
intervals = 1
count_down_rect_width = box_rect.width
is_rest = False
left_box_color = get_bg_color(is_rest)
seconds = get_count_down_seconds(is_rest)

while running:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False
            if event.key == pygame.K_f:
                pygame.display.toggle_fullscreen()
        elif event.type == pygame.QUIT:
            running = False
        elif event.type == TIMER_EVT:
            if seconds <= 0:
                intervals += 1
                is_rest = not is_rest
                seconds = get_count_down_seconds(is_rest)
                count_down_rect_width = 0
                left_box_color = get_bg_color(is_rest)
                bell_sound.play()
            else:
                seconds -= 1
                passed_seconds += 1

            if passed_seconds > TOTAL_SECONDS:
                applause_sound.play()
                pygame.time.delay(5000)
                running = False

    if running and intervals <= TOTAL_INTERVALS:
        count_down_rect_width += WIDTH / \
            get_count_down_seconds(is_rest) / 60.00
        box_rect.width = count_down_rect_width
        right_box_color = get_bg_color(not is_rest)
        screen.fill(right_box_color)
        pygame.draw.rect(screen, left_box_color, box_rect)
        screen.blit(box_surf, (0, 0))

        count_down_time_surf = count_down_font.render(
            seconds_to_time(seconds), True, TEXT_COLOR)
        count_down_time_rect = count_down_time_surf.get_rect(
            center=(WIDTH/2, HEIGHT/2))
        screen.blit(count_down_time_surf, count_down_time_rect)

        interval_surf = time_info_font.render(
            f'{intervals}/{TOTAL_INTERVALS}', True, TEXT_COLOR)
        interval_rect = interval_surf.get_rect(
            centerx=count_down_time_rect.centerx, bottom=count_down_time_rect.top)
        screen.blit(interval_surf, interval_rect)
        interval_label_rect = interval_label_surf.get_rect(
            center=interval_rect.center, bottom=interval_rect.top)
        screen.blit(interval_label_surf, interval_label_rect)

        elapsed_time_label_rect = elapsed_time_label_surf.get_rect(
            topleft=count_down_time_rect.bottomleft)
        screen.blit(elapsed_time_label_surf, elapsed_time_label_rect)
        elapsed_time_surf = time_info_font.render(
            seconds_to_time(passed_seconds), True, TEXT_COLOR)
        elapsed_time_rect = elapsed_time_surf.get_rect(
            center=elapsed_time_label_rect.center, top=elapsed_time_label_rect.bottom)
        screen.blit(elapsed_time_surf, elapsed_time_rect)

        remaining_time_label_rect = remaining_time_label_surf.get_rect(
            topright=count_down_time_rect.bottomright)
        screen.blit(remaining_time_label_surf, remaining_time_label_rect)
        remaining_time_surf = time_info_font.render(
            seconds_to_time(TOTAL_SECONDS - passed_seconds), True, TEXT_COLOR)
        remaining_time_rect = remaining_time_surf.get_rect(
            center=remaining_time_label_rect.center, top=remaining_time_label_rect.bottom)
        screen.blit(remaining_time_surf, remaining_time_rect)

        pygame.display.update()

    clock.tick(60)

pygame.quit()
