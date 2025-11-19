import pygame
import os
import sys
import random
#activates fonts and music
pygame.font.init() 
pygame.mixer.init()

WIDTH, HEIGHT = 1024, 768
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) # creating window
pygame.display.set_caption("Tank Battle 2025")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
RED = (255,0,0)

BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hit.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'gunshot.mp3'))
LASER_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'laser0.wav'))
MACHINE_GUN_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'machinegun.mp3'))
WIN_SOUND = pygame.mixer.Sound(os.path.join('Assets', '1.mp3'))
MENU_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'menusound.mp3'))
KOROBEINIKI = pygame.mixer.Sound(os.path.join('Assets', 'korobeiniki.mp3'))

BORDER = pygame.Rect(WIDTH//2 - 7, 0, 8, HEIGHT)

HEALTH_FONT = pygame.font.SysFont('Calibri', 40)
WINNER_FONT = pygame.font.SysFont('Calibri', 100)
MENU_TITLE_FONT = pygame.font.SysFont('Calibri', 50)
MENU_OPTION_FONT = pygame.font.SysFont('Calibri', 40)
MENU_INSTRUCTIONS_FONT = pygame.font.SysFont('Calibri', 22)

FPS = 60
VEL = 10
BULLET_VEL = 15
MAX_BULLETS = 3
MAX_LASERS = 1
LASER_VEL = 25
MACHINE_GUN_VEL = 10
TANK_WIDTH, TANK_HEIGHT = 142, 71

YELLOW_TANK_IMAGE = pygame.image.load(os.path.join('Assets', 'yellow_tank.png'))
YELLOW_TANK = pygame.transform.scale(YELLOW_TANK_IMAGE, (TANK_WIDTH, TANK_HEIGHT))
GREEN_TANK_IMAGE = pygame.image.load(os.path.join('Assets', 'green_tank.png'))
GREEN_TANK = pygame.transform.scale(GREEN_TANK_IMAGE, (TANK_WIDTH, TANK_HEIGHT))
OBSTACLE_IMAGE = pygame.image.load(os.path.join('Assets', 'bomb.png'))
OBSTACLE = pygame.transform.scale(OBSTACLE_IMAGE, (100, 100))
#pygame.transform.rotate ((....), angle)

SNOW = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets','snow.png')), (WIDTH,HEIGHT)) 
GROUND = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets','ground.jpg')), (WIDTH,HEIGHT)) 
CITY = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets','city.jpg')), (WIDTH,HEIGHT))
WALLPAPER = pygame.transform.scale(pygame.image.load(
    os.path.join('Assets','tanks.png')), (WIDTH,HEIGHT))

class Obstacle:
    def __init__(self, x, y, width = 100, height = 100, image=None):
        self.rect = pygame.Rect(x,y, width, height)
        self.image = image
    
    def move(self, speed):
        self.rect.x -= speed
    
    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.rect.x, self.rect.y)) 

    def collides(self, other_rect):
        return self.rect.colliderect(other_rect)

    def is_off_screen(self):
        return self.rect.right < 0

class Projectile: #base class for all projectiles 
    def __init__(self, owner_tank,width,height, velocity,color, damage):
        self.owner = owner_tank
        self.velocity = velocity
        self.color = color
        self.damage = damage

        if self.owner.x < WIDTH // 2: #setting direction
            self.direction = 1
            start_x = self.owner.x + self.owner.width + 10
        else:
            self.direction = -1
            start_x = self.owner.x - width - 10

        start_y = self.owner.y + self.owner.height//2 - height//2
        self.rect = pygame.Rect(start_x, start_y, width, height) #creating rectangle

    def move(self):
        self.rect.x += self.velocity * self.direction
    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect) #drawing rectangle for projectile
    
class Bullet(Projectile): #subclasses inheriting from base clss
    def __init__(self, owner_tank): 
        super().__init__(owner_tank=owner_tank, width=10, height=5,velocity=BULLET_VEL,
                         color=YELLOW if owner_tank.x < WIDTH//2 else GREEN, damage=1)
        BULLET_FIRE_SOUND.play()
class Laser(Projectile):
    def __init__(self, owner_tank):
        super().__init__(owner_tank=owner_tank, width=100, height=10,velocity=LASER_VEL,
                         color=YELLOW if owner_tank.x < WIDTH//2 else GREEN, damage=2)
        LASER_FIRE_SOUND.play()
class Shot(Projectile):
    def __init__(self, owner_tank):
        super().__init__(owner_tank=owner_tank, width=7, height=3,velocity=MACHINE_GUN_VEL,
                         color=YELLOW if owner_tank.x < WIDTH//2 else GREEN, damage=0.25)
        MACHINE_GUN_SOUND.play()

class HealthSystem:
    def __init__(self, start_health=10):
        self.current_health = start_health

    def decrease(self, amount=1):
        self.current_health -= amount
    
    def is_dead(self):
        return self.current_health <= 0

    def get_health_str(self):
        return str(self.current_health)

def draw_window(green, yellow, projectiles, green_health, yellow_health, game_background):
    WIN.blit(game_background, (0,0))
    pygame.draw.rect(WIN, BLACK, BORDER) 

    green_health_text = HEALTH_FONT.render('HEALTH: ' + green_health.get_health_str(), 1, WHITE) #1 for smooth edges
    yellow_health_text = HEALTH_FONT.render('HEALTH: ' + yellow_health.get_health_str(), 1, WHITE)
    WIN.blit(green_health_text, (WIDTH - green_health_text.get_width()-40, 10)) 
    WIN.blit(yellow_health_text, (10,10))

    WIN.blit(YELLOW_TANK, (yellow.x, yellow.y))
    WIN.blit(GREEN_TANK, (green.x, green.y))

    for p in projectiles: # looping list of projectiles and using draw method
        p.draw(WIN)

    pygame.display.update()

def yellow_movement(keys_pressed,yellow):
    if keys_pressed[pygame.K_a] and yellow.x - VEL > -11:
        yellow.x -= VEL
    if keys_pressed[pygame.K_d] and yellow.x + VEL + yellow.width < BORDER.x + 14:
        yellow.x += VEL
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT + 5:
        yellow.y += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > -5:
        yellow.y -= VEL

def yellow_movement_bonus(keys_pressed, yellow): 
    if keys_pressed[pygame.K_s] and yellow.y + VEL + yellow.height < HEIGHT + 5:
        yellow.y += VEL
    if keys_pressed[pygame.K_w] and yellow.y - VEL > -5:
        yellow.y -= VEL

def green_movement(keys_pressed,green):
    if keys_pressed[pygame.K_LEFT] and green.x - VEL > BORDER.x: 
        green.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and green.x + VEL + green.width < WIDTH + 10:
        green.x += VEL
    if keys_pressed[pygame.K_DOWN] and green.y + VEL + green.height < HEIGHT + 4:
        green.y += VEL
    if keys_pressed[pygame.K_UP] and green.y - VEL > -9.5: 
        green.y -= VEL

def handle_multiplayer_shooting_controls(event, yellow, green, projectiles):
    if event.type == pygame.KEYDOWN:
        
        if event.key == pygame.K_1 and len([p for p in projectiles if isinstance(p, Bullet) and p.owner == yellow]) < MAX_BULLETS:
            projectiles.append(Bullet(owner_tank=yellow))
        if event.key == pygame.K_2 and len([p for p in projectiles if isinstance(p, Laser) and p.owner == yellow]) < MAX_LASERS:
            projectiles.append(Laser(owner_tank=yellow))
        if event.key == pygame.K_3:
            projectiles.append(Shot(owner_tank=yellow))

        
        if event.key == pygame.K_0 and len([p for p in projectiles if isinstance(p, Bullet) and p.owner == green]) < MAX_BULLETS:
            projectiles.append(Bullet(owner_tank=green))
        if event.key == pygame.K_9 and len([p for p in projectiles if isinstance(p, Laser) and p.owner == green]) < MAX_LASERS:
            projectiles.append(Laser(owner_tank=green))
        if event.key == pygame.K_8:
            projectiles.append(Shot(owner_tank=green))

def handle_singleplayer_shooting_controls(event,yellow, green, projectiles):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_1 and len([p for p in projectiles if isinstance(p, Bullet) and p.owner == yellow]) < MAX_BULLETS: #checking if key pressed and length of the list of projectiles(subclass) is less than MAX_BULLETS 
            projectiles.append(Bullet(owner_tank=yellow))

        if event.key == pygame.K_2 and len([p for p in projectiles if isinstance(p, Laser) and p.owner == yellow]) < MAX_LASERS:
            projectiles.append(Laser(owner_tank=yellow))

        if event.key == pygame.K_3:
            projectiles.append(Shot(owner_tank=yellow))

def handle_ai(green, projectiles, current_time, green_x_direction, green_y_direction):
        if green.top <= 0 or green.bottom >= HEIGHT: #staying inside the screen
            green_y_direction *= -1
        green.y += green_y_direction * 4
        if green.left <= 550 or green.right >= WIDTH :
            green_x_direction *= -1
        green.x += green_x_direction * 2
        
        if pygame.time.get_ticks() % 50 == 0:
            projectiles.append(Shot(owner_tank=green))

        if pygame.time.get_ticks() % 500 == 0 and len([p for p in projectiles if isinstance(p, Laser) and p.owner == green]) < MAX_LASERS:
            projectiles.append(Laser(owner_tank=green))
        
        if pygame.time.get_ticks() % 150 == 0 and len([p for p in projectiles if isinstance(p, Bullet) and p.owner == green]) < MAX_BULLETS:
            projectiles.append(Bullet(owner_tank=green))

        return green_x_direction, green_y_direction

def check_winner(yellow_health, green_health):
    if green_health.is_dead():
        winner_text = 'Yellow Wins!'
    elif yellow_health.is_dead():
        winner_text = 'Green Wins!'
    else:
        return False
    KOROBEINIKI.stop()
    WIN_SOUND.play()
    draw_winner(winner_text)
    return True

def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000) #5 seconds

def main_menu():

    KOROBEINIKI.play(loops=-1)

    background_options = [("Berlin", CITY), ("Winter countryside", SNOW), ("Summer countryside", GROUND)]
    mode_options = ['Single mode', 'Two player mode', 'Bonus mode']

    selected_option = 0
    selected_mode = 0
    mode_active =  False

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if not mode_active:
                    if event.key == pygame.K_UP:
                        selected_option = (selected_option - 1) % len(background_options)
                        MENU_SOUND.play()
                    if event.key == pygame.K_DOWN:
                        selected_option = (selected_option + 1) % len(background_options)
                        MENU_SOUND.play()
                    if event.key == pygame.K_RETURN:
                        MENU_SOUND.play()
                        mode_active = True
                else:
                    if event.key == pygame.K_UP:
                        selected_mode = (selected_mode - 1) % len(mode_options)
                        MENU_SOUND.play()
                    if event.key == pygame.K_DOWN:
                        MENU_SOUND.play()
                        selected_mode = (selected_mode + 1) % len(mode_options)
                    if event.key == pygame.K_RETURN:
                        MENU_SOUND.play()
                        return mode_options[selected_mode], background_options[selected_option][1] #2 element of tuple
        
        WIN.fill(BLACK)
        WIN.blit(WALLPAPER, (0,0))

        if not mode_active:
        
            title_text = MENU_TITLE_FONT.render("Select Location", True, YELLOW)
            WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, 250))

            for i, (name, _) in enumerate(background_options): # (name, _) - 'berlin' CITY in enumerate -> (0 , 'berlin' CITY)
                if i == selected_option: # i is a number
                    color = RED
                else:
                    color = YELLOW
                option_text = MENU_OPTION_FONT.render(name, 1, color)
                WIN.blit(option_text, (WIDTH // 2 - option_text.get_width() // 2, (HEIGHT//2-50) + i * 45)) #45 pixels between the lines

        else:
            WIN.blit(background_options[selected_option][1], (0, 0))


            for i, mode in enumerate(mode_options):
                if i == selected_mode:
                    color = RED
                else:
                    color = YELLOW
                mode_text = MENU_OPTION_FONT.render(mode, 1, color)
                WIN.blit(mode_text, (WIDTH // 2 - mode_text.get_width() // 2, (HEIGHT//2-50) + i * 65)) #(WIDTH // 2 - (len(mode_options) * 270) // 2 + i * 300, HEIGHT//3))

        title_text = MENU_TITLE_FONT.render("Tank Battle 2025", 1, YELLOW)
        WIN.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 6))
        
        instructions_text = MENU_INSTRUCTIONS_FONT.render(
            "Press UP/DOWN & return to select", 1, YELLOW)
        game_instructions_text = MENU_INSTRUCTIONS_FONT.render(
            "1 and 0 - fire cannon | 2 and 9 - fire laser | 3 and 8 - fire machine gun | wasd and arrows to move", 1, YELLOW)
        WIN.blit(instructions_text, (WIDTH // 2 - instructions_text.get_width() // 2, HEIGHT - 100))
        WIN.blit(game_instructions_text, (WIDTH // 2 - game_instructions_text.get_width() // 2, HEIGHT - 150))

        pygame.display.update()
        pygame.time.Clock().tick(FPS)

def multiplayer(selected_game_background):
    
    green = pygame.Rect(800, 300, TANK_WIDTH, TANK_HEIGHT)
    yellow = pygame.Rect(100, 300, TANK_WIDTH, TANK_HEIGHT)

    projectiles = []
    
    green_health = HealthSystem(10)
    yellow_health = HealthSystem(10)

    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        events = pygame.event.get()

        for event in events:
        
            if event.type == pygame.QUIT:
                run = False
            
            handle_multiplayer_shooting_controls(event, yellow, green, projectiles)

        if check_winner(yellow_health, green_health):
            break

        current_time = pygame.time.get_ticks()
        keys_pressed = pygame.key.get_pressed()

        yellow_movement(keys_pressed, yellow)
        green_movement(keys_pressed, green)

        for p in projectiles[:]:
            p.move()

            if p.owner == yellow and p.rect.colliderect(green):
                green_health.decrease(p.damage)
                BULLET_HIT_SOUND.play()
                projectiles.remove(p)
            elif p.owner == green and p.rect.colliderect(yellow):
                yellow_health.decrease(p.damage)
                BULLET_HIT_SOUND.play()
                projectiles.remove(p)
            
            elif p.rect.x > WIDTH or p.rect.right < 0:
                projectiles.remove(p)

        draw_window(green, yellow, projectiles, green_health, 
                    yellow_health, selected_game_background)

def single(selected_game_background): 
    green = pygame.Rect(800, 300, TANK_WIDTH, TANK_HEIGHT)
    yellow = pygame.Rect(100, 300, TANK_WIDTH, TANK_HEIGHT)
    projectiles = []
    yellow_health = HealthSystem(10)
    green_health = HealthSystem(10)
    green_y_direction = 1
    green_x_direction = 1
    clock = pygame.time.Clock()
    run = True

    while run:
        clock.tick(FPS)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                run = False
            handle_singleplayer_shooting_controls(event,yellow, green, projectiles)
        
        current_time = pygame.time.get_ticks()
        keys_pressed = pygame.key.get_pressed()
        yellow_movement(keys_pressed, yellow)

        green_x_direction, green_y_direction = handle_ai(green, projectiles, current_time, green_x_direction, 
                                                         green_y_direction)
        
        for p in projectiles[:]:
            p.move()

            if p.owner == yellow and p.rect.colliderect(green):
                green_health.decrease(p.damage)
                BULLET_HIT_SOUND.play()
                projectiles.remove(p)
            elif p.owner == green and p.rect.colliderect(yellow):
                yellow_health.decrease(p.damage)
                BULLET_HIT_SOUND.play()
                projectiles.remove(p)
            
            elif p.rect.x > WIDTH or p.rect.right < 0:
                projectiles.remove(p)

        if check_winner(yellow_health, green_health):
            break

        draw_window(green, yellow, projectiles, green_health, yellow_health, 
                    selected_game_background)

def bonus(selected_game_background):
    yellow = pygame.Rect(100, 300, TANK_WIDTH, TANK_HEIGHT)
    yellow_health = HealthSystem(10)

    clock = pygame.time.Clock()
    run = True
    BACKGROUND_X_SPEED = 5
    BACKGROUND_X = 0
    obstacles = []
    obstacles_timer = 0
    obstacles_spawn = 1500

    while run:
            clock.tick(FPS)
            current_time = pygame.time.get_ticks()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    run = False
                
            BACKGROUND_X -= BACKGROUND_X_SPEED
            if BACKGROUND_X_SPEED < 20: #limits the speed
                BACKGROUND_X_SPEED +=0.0005
            if BACKGROUND_X <= - WIDTH:
                BACKGROUND_X = 0

            if current_time - obstacles_timer > obstacles_spawn:
                obstacle_y = random.randint(0, HEIGHT)
                new_obstacle = Obstacle(WIDTH, obstacle_y, 100, 100, image=OBSTACLE)
                obstacles.append(new_obstacle)
                obstacles_timer = current_time #reset
                if obstacles_spawn > 300:
                    obstacles_spawn -= 20
                else:
                    obstacles_spawn = 300
            
            for obstacle in obstacles[:]:
                obstacle.move(BACKGROUND_X_SPEED)
                
                if obstacle.collides(yellow): 
                    obstacles.remove(obstacle)
                    yellow_health.decrease(1)
                    BULLET_HIT_SOUND.play()
                    if yellow_health.is_dead():
                        winner_text = 'Game over!'
                        KOROBEINIKI.stop()
                        WIN_SOUND.play()
                        draw_winner(winner_text)
                        run = False
                elif obstacle.is_off_screen(): 
                    obstacles.remove(obstacle)   
        
            WIN.blit(selected_game_background, (BACKGROUND_X, 0))
            WIN.blit(selected_game_background, (BACKGROUND_X + WIDTH, 0)) #second bckground 

            for obstacle in obstacles:
                obstacle.draw(WIN)
            
            WIN.blit(YELLOW_TANK, (yellow.x, yellow.y))
            
            health_text = HEALTH_FONT.render(f'HEALTH: {yellow_health.get_health_str()}', 1, WHITE)
            WIN.blit(health_text, (15,15))
            
            keys_pressed = pygame.key.get_pressed()
            yellow_movement_bonus(keys_pressed, yellow)

            pygame.display.update()

def main():

    selected_mode, selected_game_background = main_menu()

    if selected_mode == 'Single mode':
        single(selected_game_background)
    elif selected_mode == 'Bonus mode':
        bonus(selected_game_background)
    elif selected_mode == 'Two player mode':
        multiplayer(selected_game_background)
        
    pygame.quit()

if __name__ == '__main__':
    main()