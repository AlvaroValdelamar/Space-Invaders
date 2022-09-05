import pygame
import os

# Creating game window
WIDTH, HEIGHT = 500, 500 # WIDTH, HEIGHT of the screen window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Frames per second to update game
FPS = 60

# Velocity at which the objects in the screen move
VEL = 3

# Changing the window's name
pygame.display.set_caption('Space Invaders')

WHITE = (255, 255, 255) # White color in RGB tuple

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 40
ALIEN_WIDTH, ALIEN_HEIGHT = 25, 25

# Importing user spaceship surface
SPACESHIP_IMAGE = pygame.image.load(os.path.join('game_images','spaceship.png'))
# Rezising the spaceship
SPACESHIP_IMAGE = pygame.transform.scale(SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# Importing user alien surface
ALIEN_IMAGE = pygame.image.load(os.path.join('game_images','alien.png'))
# Rezising the alien
ALIEN_IMAGE = pygame.transform.scale(ALIEN_IMAGE, (ALIEN_WIDTH, ALIEN_HEIGHT))


def draw_window(user, alien):
    # Filling the windows with a color RGB
    WIN.fill(WHITE)

    # Drawing surfaces in the screen
    WIN.blit(SPACESHIP_IMAGE, (user.x, user.y))
    WIN.blit(ALIEN_IMAGE, (alien.x, alien.y))

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


def main():

    # Rectangle to keep track of the user spaceship
    spaceship = pygame.Rect(300, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    alien = pygame.Rect(100, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

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

        # Read keys pressed by the user
        keys_pressed = pygame.key.get_pressed()
        # Move the user spaceship
        spaceship_movement(keys_pressed, spaceship)
        # Move the alien
        alien_movement(alien)

        # Update position of the player and aliens
        draw_window(spaceship, alien)
    
    pygame.quit() # End the game

if __name__ == "__main__":
    main()