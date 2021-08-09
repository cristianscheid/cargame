import pygame, sys, math


class Game:

    def rotate_car(self, surface, surface_rect, angle):
        rotated_surface = pygame.transform.rotozoom(surface, angle, 1)
        rotated_rect = rotated_surface.get_rect(center=(surface_rect.centerx, surface_rect.centery))
        return rotated_surface, rotated_rect

    def move_car(self, surface_rect, angle, radius, direction):
        x = radius * math.sin(math.pi * 2 * angle / 360)
        y = radius * math.cos(math.pi * 2 * angle / 360)
        digits = 0
        if direction == 'forward':
            surface_rect.centerx -= round(x, digits)
            surface_rect.centery -= round(y, digits)
        elif direction == 'backward':
            surface_rect.centerx += round(x, digits)
            surface_rect.centery += round(y, digits)
        return surface_rect

    def start_game(self):
        pygame.init()
        clock = pygame.time.Clock()
        screen = pygame.display.set_mode([900, 600])
        track = pygame.image.load('track.png').convert()
        car = pygame.image.load('car.png').convert_alpha()
        car_rotated = car
        car_rect = car.get_rect(center=(835, 535))
        angle = 0
        step = 0
        direction = 'forward'
        move_forward = move_backward = rotate_right = rotate_left = hand_brake = False

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pygame.quit()
                        sys.exit()
                    if event.key == pygame.K_UP:
                        move_forward = True
                    if event.key == pygame.K_DOWN:
                        move_backward = True
                    if event.key == pygame.K_RIGHT:
                        rotate_right = True
                    if event.key == pygame.K_LEFT:
                        rotate_left = True
                    if event.key == pygame.K_SPACE:
                        hand_brake = True
                if event.type == pygame.KEYUP:
                    if event.key == pygame.K_UP:
                        move_forward = False
                    if event.key == pygame.K_DOWN:
                        move_backward = False
                    if event.key == pygame.K_RIGHT:
                        rotate_right = False
                    if event.key == pygame.K_LEFT:
                        rotate_left = False
                    if event.key == pygame.K_SPACE:
                        hand_brake = False

            if rotate_right and step != 0:
                angle -= 10 
            if rotate_left and step != 0:
                angle += 10

            car_rotated, car_rect = self.rotate_car(car, car_rect, angle)

            if move_forward:
                step += 0.1
            if move_backward:
                step -= 0.1
            if hand_brake:
                if step > 0:
                    step -= 0.2
                if step < 0:
                    step += 0.2
            if move_forward == move_backward == hand_brake == False:
                if step > 0:
                    step -= 0.1
                elif step < 0:
                    step += 0.1

            step = round(step, 2)
            print(step)
            
            car_rect = self.move_car(car_rect, angle, step, direction)
            screen.blit(track, (0, 0))
            screen.blit(car_rotated, car_rect)
            pygame.display.flip()
            clock.tick(30)
