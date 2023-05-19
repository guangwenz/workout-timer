import pygame
from workout_timer.warmup_timer import WarmupTimer
from workout_timer.work_timer import WorkTimer, RestTimer

if __name__ == '__main__':
    pygame.init()
    screen = pygame.display.set_mode((1280, 960))
    screen_rect = screen.get_rect()
    pygame.display.set_caption('Workout Timer')
    pygame.time.set_timer(pygame.USEREVENT+1, 1000)

    clock = pygame.time.Clock()
    running = True
    current_level = 0

    levels = [WarmupTimer(3),
              WorkTimer(7, screen_rect.height, screen_rect.width),
              RestTimer(5, screen_rect.height, screen_rect.width),
              WorkTimer(10, screen_rect.height, screen_rect.width),
              RestTimer(8, screen_rect.height, screen_rect.width),
              ]
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                    running = False
                if event.key == pygame.K_f:
                    pygame.display.toggle_fullscreen()
            elif event.type == pygame.QUIT:
                running = False
            else:
                levels[current_level].handle_inputs(event)
        if levels[current_level].update(screen) == True:
            current_level += 1
        if current_level >= len(levels):
            running = False
        pygame.display.update()
    pygame.quit()
