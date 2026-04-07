import pygame

def run():
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    pygame.display.set_caption("Moving Ball")
    x = 960
    y = 540
    vel = 20
    clock = pygame.time.Clock()
    running = True
    
    while running:
        clock.tick(60)  # 60 FPS
        screen.fill((255, 255, 255))
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            y -= vel
        if keys[pygame.K_s]:
            y += vel
        if keys[pygame.K_a]:
            x -= vel
        if keys[pygame.K_d]:
            x += vel
        
        radius = 25
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        
        if x - radius < 0:
            x = radius
        if x + radius > screen_width:
            x = screen_width - radius
        if y - radius < 0:
            y = radius
        if y + radius > screen_height:
            y = screen_height - radius
        
        ball = pygame.draw.circle(screen, (255, 0, 0), (x, y), radius)
        pygame.display.update()
    
    pygame.quit()
run()