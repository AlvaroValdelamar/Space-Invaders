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

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 80, 80
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


def main():

    # Rectangle to keep track of the user spaceship
    user = pygame.Rect(300, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
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

        # Reading keys pressed down by the user
        # Adding movement to the spaceship
        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_LEFT]: # LEFT KEY
            user.x -= VEL
        if keys_pressed[pygame.K_RIGHT]: # RIGHT KEY
            user.x += VEL

        # Update position of the player and aliens
        draw_window(user, alien)
    
    pygame.quit() # End the game

if __name__ == "__main__":
    main()