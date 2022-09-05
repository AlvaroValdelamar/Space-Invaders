import pygame
import os

# Creating game window
WIDTH, HEIGHT = 500, 500 # WIDTH, HEIGHT of the screen window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Frames per second to update game
FPS = 60

# Velocity at which the objects in the screen move
VEL = 3

# Velocity of the bullets fired by the user
VEL_BULLET = 5.5
# Max amount of bullets on screen
MAX_BULLETS = 10

# Changing the window's name
pygame.display.set_caption('Space Invaders')

WHITE = (255, 255, 255) # White color in RGB tuple
PURPLE = (255, 0, 255)

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 40
ALIEN_WIDTH, ALIEN_HEIGHT = 25, 25

# Custom events
USER_HIT = pygame.USEREVENT + 1 # If a user hits an alien with a bullet
ALIEN_HIT = pygame.USEREVENT + 2 # If a user collides with an alien

# Importing user spaceship surface
SPACESHIP_IMAGE = pygame.image.load(os.path.join('game_images','spaceship.png'))
# Rezising the spaceship
SPACESHIP_IMAGE = pygame.transform.scale(SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# Importing user alien surface
ALIEN_IMAGE = pygame.image.load(os.path.join('game_images','alien.png'))
# Rezising the alien
ALIEN_IMAGE = pygame.transform.scale(ALIEN_IMAGE, (ALIEN_WIDTH, ALIEN_HEIGHT))


def draw_window(user, alien, bullets):
    # Filling the windows with a color RGB
    WIN.fill(WHITE)

    # Drawing surfaces in the screen
    WIN.blit(SPACESHIP_IMAGE, (user.x, user.y))
    WIN.blit(ALIEN_IMAGE, (alien.x, alien.y))

    for bullet in bullets:
        pygame.draw.rect(WIN, PURPLE, bullet)

    #Update the display in every run of the loop
    pygame.display.update()

# Change spaceship positions for keys pressed
def spaceship_movement(keys_pressed, spaceship):
    # Adding movement to the spaceship
    # and making sure they can't move past the window's border
    if keys_pressed[pygame.K_LEFT] and spaceship.x > VEL: # LEFT KEY
        spaceship.x -= VEL
    if keys_pressed[pygame.K_RIGHT] and spaceship.x + spaceship.width < WIDTH - VEL: # RIGHT KEY
        spaceship.x += VEL
    if keys_pressed[pygame.K_UP] and spaceship.y > VEL: # UP KEY
        spaceship.y -= VEL
    if keys_pressed[pygame.K_DOWN] and spaceship.y + spaceship.height < HEIGHT - VEL: # DOWN KEY
        spaceship.y += VEL

def alien_movement(alien):
    alien.y += 1

# Moves bullets and check if the collided with an alien
def handle_bullets(bullets, alien):
    for bullet in bullets:  # Loop through all bullets in the game
        bullet.y -= VEL_BULLET # Moving bullets
        if alien.colliderect(bullet): # Check if a bullets hits an alien
            pygame.event.post(pygame.event.Event(USER_HIT))
            bullets.remove(bullet) # Remove bullet from list


def main():

    # Rectangle to keep track of the user spaceship
    spaceship = pygame.Rect(300, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    # Rectangle to keep track of the alien
    alien = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    # Bullets fired by the user
    bullets = []

    # Control the speed of the while loop
    clock = pygame.time.Clock()
    # Game loop that terminates when the games end
    run = True
    while run:
        # Making sure the game runs at the set FPS
        clock.tick(FPS)

        # Looping through events in the game
        for event in pygame.event.get():
            
            # check if user quitted the game
            if event.type == pygame.QUIT:
                run = False # Exit while loop
            
            # Creating a bullet if spacebar is pressed down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(spaceship.x + spaceship.width//2,
                                        spaceship.y - spaceship.height//2, 10, 5)
                    bullets.append(bullet)
        
        handle_bullets(bullets, alien)

        # Read keys pressed by the user
        keys_pressed = pygame.key.get_pressed()
        # Move the user spaceship
        spaceship_movement(keys_pressed, spaceship)
        # Move the alien
        alien_movement(alien)

        # Update position of the player and aliens
        draw_window(spaceship, alien, bullets)
    
    pygame.quit() # End the game

if __name__ == "__main__":
    main()