"""Import Packages"""
import pygame
import os
pygame.font.init()
pygame.mixer.init()


"""Create Variables"""

# Game diameters
WIDTH, HEIGHT = 500, 900

# Spaceship dimesnions
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

# Frame refresh rate
FPS = 60

# Animation velocities
VEL = 5
BULLET_VEL = 7

# Maximum bullets on screen at one time
MAX_BULLETS = 3

# Colours
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

WINNER_FONT = pygame.font.SysFont('comicsans', 100)

"""Import Sounds"""
BULLET_HIT_SOUND = pygame.mixer.Sound('Assets/Grenade+1.mp3')
BULLET_FIRE_SOUND = pygame.mixer.Sound('Assets/Gun+Silencer.mp3')


"""Create game window"""
# Create window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Add caption in top left corner
pygame.display.set_caption("First Game!")


"""Create background"""
SPACE_IMAGE = pygame.image.load(os.path.join('Assets', 'space.png'))
SPACE = pygame.transform.rotate(pygame.transform.scale(SPACE_IMAGE, (HEIGHT, WIDTH)), 90)


"""Create yellow spaceships and events when bullet strikes"""
YELLOW_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_yellow.png'))
YELLOW_SPACESHIP_OG = pygame.transform.rotate(pygame.transform.scale(YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 0)

YELLOW_SPACESHIP = []
yellow = []
YELLOW_HIT = []
yellow_health = []
YELLOW_X = [20, 120, 220, 320, 420]
YELLOW_Y = [500, 400, 300, 200, 100 ]

for a, y in enumerate(YELLOW_Y) :
    for b, x in enumerate(YELLOW_X) :
        i = (a * len(YELLOW_X)) + b
        YELLOW_SPACESHIP.append(YELLOW_SPACESHIP_OG.copy())
        yellow.append(pygame.Rect(x, y, SPACESHIP_WIDTH, SPACESHIP_HEIGHT))
        YELLOW_HIT.append(pygame.USEREVENT + i + 1)
        yellow_health.append(5)
        


"""Create red spaceship"""
RED_SPACESHIP_IMAGE = pygame.image.load(os.path.join('Assets', 'spaceship_red.png'))
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 180)



def red_handle_movement(keys_pressed, red):
    if keys_pressed[pygame.K_LEFT] and red.x - VEL > 0:  # LEFT
        red.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and red.x + VEL + red.width < WIDTH:  # RIGHT
        red.x += VEL


def handle_bullets(red_bullets):
    
    for bullet in red_bullets:
        bullet.y -= BULLET_VEL
        for i, yell in enumerate(yellow) :
            if yell.colliderect(bullet):
                pygame.event.post(pygame.event.Event(YELLOW_HIT[i]))
                red_bullets.remove(bullet)
        
        if bullet.x < 0:
            red_bullets.remove(bullet)
    

def die(red, yellow) :
    for yell in yellow :
        if red.y - 25  < yell.y :
            winner('You Lose')



def winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width() /
                         2, HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(5000)



def draw_window(red, red_bullets, drop):
    WIN.blit(SPACE, (0, 0))
    
    WIN.blit(RED_SPACESHIP, (red.x, red.y))
    
    for i, spaceship in enumerate(YELLOW_SPACESHIP) :
        yellow[i].y += drop
        WIN.blit(spaceship, (yellow[i].x, yellow[i].y))
    
    for bullet in red_bullets:
        pygame.draw.rect(WIN, RED, bullet)
    
    pygame.display.update()



def main():
    red = pygame.Rect(200, 800, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red_bullets = []

    clock = pygame.time.Clock()
    run = True
    t = 0
    drop = 0
    while run:
        clock.tick(FPS)
        
        t += 1
        if t % 60 == 0 :
            drop += 0.2
            
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE :
                    bullet = pygame.Rect(red.x + red.width//2 - 3, red.y, 5, 10)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            for i, hit in enumerate(YELLOW_HIT) :
                if event.type == hit:
                    yellow_health[i] -= 1
                    BULLET_HIT_SOUND.play()
                    if yellow_health[i] <= 0 :
                        YELLOW_SPACESHIP.pop(i)
                        yellow.pop(i)

        
        # Identify if key pressed and call function to move spaceship
        keys_pressed = pygame.key.get_pressed()
        red_handle_movement(keys_pressed, red)
        
        handle_bullets(red_bullets)
        
        die(red, yellow) 
        
        draw_window(red, red_bullets, drop)

    pygame.quit()


if __name__ == "__main__":
    main()
