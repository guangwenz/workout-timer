import pygame

WIDTH = 1280
HEIGHT = 960

SET_COUNT = 1
REPS = 2
REP_TIME = 20
REST_TIME = 10
TOTAL_INTERVALS = SET_COUNT * REPS * 2
TOTAL_SECONDS = SET_COUNT * REPS * REP_TIME + SET_COUNT * REPS * REST_TIME

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


pygame.init()

print(pygame.display.get_desktop_sizes())
screen = pygame.display.set_mode((WIDTH, HEIGHT))
screen.fill('gray')

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
left_box_color = H_COLOR
seconds = REP_TIME
passed_seconds = 0
intervals = 1
count_down_rect_width = box_rect.width

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
            seconds -= 1
            passed_seconds += 1
            if passed_seconds > TOTAL_SECONDS:
                running = False
            if seconds <= 0:
                intervals += 1
                seconds = REP_TIME
                count_down_rect_width = 0
                left_box_color = H_COLOR if left_box_color == L_COLOR else L_COLOR

    count_down_rect_width += WIDTH / REP_TIME / 60.00
    box_rect.width = count_down_rect_width
    right_box_color = H_COLOR if left_box_color == L_COLOR else L_COLOR if left_box_color == H_COLOR else BG_COLOR
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
