import pygame
import os
import time
pygame.font.init()

# Creating game window
WIDTH, HEIGHT = 500, 500 # WIDTH, HEIGHT of the screen window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

# Frames per second to update game
FPS = 60

# Velocity at which the objects in the screen move
VEL = 3
# Velocity of the bullets fired by the user
VEL_BULLET = 5.5
# Alien velocity
VEL_ALIEN = 1
# Max amount of bullets on screen
MAX_BULLETS = 10

# Changing the window's name
pygame.display.set_caption('Space Invaders')

# Health font for display
HEALT_FONT = pygame.font.SysFont('comicsans', 40)

# Subtitle font
SUB_FONT = pygame.font.SysFont('comicsans', 30)

WHITE = (255, 255, 255) # White color in RGB tuple
PURPLE = (255, 0, 255) # Purple color in RGB tuple
RED = (255, 0, 0) # Red color in RGB tuple

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 40, 40
ALIEN_WIDTH, ALIEN_HEIGHT = 25, 25

# Custom events
USER_HIT = pygame.USEREVENT + 1 # If a user hits an alien with a bullet
ALIEN_HIT = pygame.USEREVENT + 2 # If a user collides with an alien

# Importing user spaceship surface
SPACESHIP_IMAGE = pygame.image.load(os.path.join('game_images','spaceship.png'))
# Rezising the spaceship
SPACESHIP_IMAGE = pygame.transform.scale(SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT))

# Importing red alien surface
ALIEN_IMAGE = pygame.image.load(os.path.join('game_images','alien.png'))
# Rezising the red alien
ALIEN_IMAGE = pygame.transform.scale(ALIEN_IMAGE, (ALIEN_WIDTH, ALIEN_HEIGHT))

# Importing blue alien surface
ALIEN_IMAGE_BLUE = pygame.image.load(os.path.join('game_images','alien2.png'))
# Rezising the blue alien
ALIEN_IMAGE_BLUE = pygame.transform.scale(ALIEN_IMAGE_BLUE, (ALIEN_WIDTH, ALIEN_HEIGHT))

# Importing white alien surface
ALIEN_IMAGE_WHITE = pygame.image.load(os.path.join('game_images','alien3.png'))
# Rezising the white alien
ALIEN_IMAGE_WHITE = pygame.transform.scale(ALIEN_IMAGE_WHITE, (ALIEN_WIDTH, ALIEN_HEIGHT))

# Importing green alien surface
ALIEN_IMAGE_GREEN = pygame.image.load(os.path.join('game_images','alien4.png'))
# Rezising the green alien
ALIEN_IMAGE_GREEN = pygame.transform.scale(ALIEN_IMAGE_GREEN, (ALIEN_WIDTH, ALIEN_HEIGHT))

# Importing background surface
BACKGROUND_IMAGE = pygame.image.load(os.path.join('game_images','background.png'))
# Rezising the background
BACKGROUND_IMAGE = pygame.transform.scale(BACKGROUND_IMAGE, (WIDTH, HEIGHT))



#create Explosion class
class Explosion(pygame.sprite.Sprite):
	def __init__(self, x, y):
		pygame.sprite.Sprite.__init__(self)
		self.images = []
		for num in range(1, 5):
			img = pygame.image.load(f"game_images/explosion{num}.png")
			img = pygame.transform.scale(img, (50, 50))
			self.images.append(img)
		self.index = 0
		self.image = self.images[self.index]
		self.rect = self.image.get_rect()
		self.rect.center = [x, y]
		self.counter = 0

	def update(self):
		explosion_speed = 3
		#update explosion animation
		self.counter += 1

		if self.counter >= explosion_speed and self.index < len(self.images) - 1:
			self.counter = 0
			self.index += 1
			self.image = self.images[self.index]

		#if the animation is complete, reset animation index
		if self.index >= len(self.images) - 1 and self.counter >= explosion_speed:
			self.kill()

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

# Moves aliens and checks they collided with the user spaceship
def alien_movement(aliens, spaceship, explosion_group):
    for alien in aliens:
        alien.y += VEL_ALIEN
        if alien.colliderect(spaceship): # Check if a bullets hits an alien
            pygame.event.post(pygame.event.Event(ALIEN_HIT))
            aliens.remove(alien)
            explosion = Explosion(alien.x, alien.y)
            explosion_group.add(explosion)
            
        elif alien.y > HEIGHT:
            aliens.remove(alien)

# Moves bullets and check if the collided with an alien
def handle_bullets(bullets, aliens, explosion_group):
    for bullet in bullets:  # Loop through all bullets in the game
        bullet.y -= VEL_BULLET # Moving bullets
        for alien in aliens:
            if alien.colliderect(bullet): # Check if a bullets hits an alien
                pygame.event.post(pygame.event.Event(USER_HIT))
                bullets.remove(bullet) # Remove bullet from list
                aliens.remove(alien)
                explosion = Explosion(alien.x, alien.y)
                explosion_group.add(explosion)

        if bullet.y < 0:
            bullets.remove(bullet)


# Draw screen text when the user looses the game
def draw_end_screen_text(text):
    draw_text = HEALT_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, 
                        HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)

# Draw screen text when user passes the current level
def draw_next_level_screen_text(text):
    draw_text = HEALT_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, 
                        HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(3000)

# Draw screen text to signal the start of the new level to the user
def draw_new_level_text(new_level_number):
    draw_text = HEALT_FONT.render('LEVEL ' + str(new_level_number), 1, WHITE)
    WIN.blit(draw_text, (WIDTH/2 - draw_text.get_width()/2, 
                        HEIGHT/2 - draw_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(1000)

# Displays start screen
def start_game_screen():

    enter = False

    # Control the speed of the while loop
    clock = pygame.time.Clock()
    
    oldepoch = time.time()

    # Until the user presses Enter
    while enter is False:

        # Making sure the game runs at the set FPS
        clock.tick(FPS)

        # Keeps track of time
        new_epoch = time.time()

         # Filling the windows with a color RGB
        WIN.fill(WHITE)

        # Drawing surfaces in the screen
        WIN.blit(BACKGROUND_IMAGE, (0, 0))

        # Shows the game title
        game_title = HEALT_FONT.render('SPACE INVADERS', 1, RED)
        WIN.blit(game_title, (WIDTH/2 - game_title.get_width()/1.95, 
                            HEIGHT/2 - game_title.get_height()/1.7))
        
        game_title = HEALT_FONT.render('SPACE INVADERS', 1, WHITE)
        WIN.blit(game_title, (WIDTH/2 - game_title.get_width()/2, 
                            HEIGHT/2 - game_title.get_height()/2))

        # Drawing aliens from different colors on the upper side

        WIN.blit(ALIEN_IMAGE_BLUE, (WIDTH/2 - ALIEN_IMAGE.get_width(), 
                                    HEIGHT/2 - ALIEN_IMAGE.get_height()*2))
        
        WIN.blit(ALIEN_IMAGE, (WIDTH/2 - ALIEN_IMAGE.get_width() - ALIEN_IMAGE.get_width()*2, 
                                    HEIGHT/2 - ALIEN_IMAGE.get_height()*3))
        
        WIN.blit(ALIEN_IMAGE_WHITE, (WIDTH/2 - ALIEN_IMAGE.get_width() - ALIEN_IMAGE.get_width()*4, 
                                    HEIGHT/2 - ALIEN_IMAGE.get_height()*2))
        
        WIN.blit(ALIEN_IMAGE_GREEN, (WIDTH/2 - ALIEN_IMAGE.get_width() - ALIEN_IMAGE.get_width()*6, 
                                    HEIGHT/2 - ALIEN_IMAGE.get_height()*3))

        # Drawing aliens from different colors on the lower side

        WIN.blit(ALIEN_IMAGE_BLUE, (WIDTH/2 - ALIEN_IMAGE.get_width(), 
                                    HEIGHT/2 + ALIEN_IMAGE.get_height()*2))
        
        WIN.blit(ALIEN_IMAGE, (WIDTH/2 - ALIEN_IMAGE.get_width() - ALIEN_IMAGE.get_width()*2, 
                                    HEIGHT/2 + ALIEN_IMAGE.get_height()*3))
        
        WIN.blit(ALIEN_IMAGE_WHITE, (WIDTH/2 - ALIEN_IMAGE.get_width() - ALIEN_IMAGE.get_width()*4, 
                                    HEIGHT/2 + ALIEN_IMAGE.get_height()*2))
        
        WIN.blit(ALIEN_IMAGE_GREEN, (WIDTH/2 - ALIEN_IMAGE.get_width() - ALIEN_IMAGE.get_width()*6, 
                                    HEIGHT/2 + ALIEN_IMAGE.get_height()*3))

        last_text_displayed = 0

        # This is for tilting the press enter to play text
        if (new_epoch - oldepoch > 1) and (last_text_displayed == 0):
            sub_title = SUB_FONT.render('Press Enter to play', 1, WHITE)
            WIN.blit(sub_title, (WIDTH/2 - sub_title.get_width()/2, 
                                HEIGHT/2 - sub_title.get_height()/2 + game_title.get_height()))
            
            last_text_displayed = 1
            oldepoch = new_epoch

        elif last_text_displayed == 1:
            new_epoch = time.time()
            oldepoch = new_epoch
            last_text_displayed = 0


        # Looping through events in the game
        for event in pygame.event.get():
            # Creating a bullet if spacebar is pressed down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    enter = True

            # check if user quitted the game
            if event.type == pygame.QUIT:
                pygame.quit()
        
        #Update the display in every run of the loop
        pygame.display.update()
        pygame.time.wait(500)

# Draws the play again? screen for the user to decide if he wants to play again or exit the game
def draw_play_again_screen():
    enter = False

    # Control the speed of the while loop
    clock = pygame.time.Clock()
    
    oldepoch = time.time()

    # Until the user presses Enter
    while enter is False:
        # Looping through events in the game
        for event in pygame.event.get():
            # Creating a bullet if spacebar is pressed down
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    enter = True

            # check if user quitted the game
            if event.type == pygame.QUIT:
                pygame.quit()
                
        # Making sure the game runs at the set FPS
        clock.tick(FPS)

        # Keeps track of time
        new_epoch = time.time()

         # Filling the windows with a color RGB
        WIN.fill(WHITE)

        # Drawing surfaces in the screen
        WIN.blit(BACKGROUND_IMAGE, (0, 0))

        # Shows the exit game or play again text
        exit_game_txt = SUB_FONT.render('Exit game', 1, WHITE)
        WIN.blit(exit_game_txt, (WIDTH/2 - exit_game_txt.get_width()/2, 
                            HEIGHT/2 - exit_game_txt.get_height()*2))

        or_txt = SUB_FONT.render('OR', 1, WHITE)
        WIN.blit(or_txt, (WIDTH/2 - or_txt.get_width()/2, 
                            HEIGHT/2 - or_txt.get_height()/2))

        last_text_displayed = 0

        # This is for tilting the play again text
        if (new_epoch - oldepoch > 1) and (last_text_displayed == 0):
            sub_title = SUB_FONT.render('Press Enter to play again', 1, WHITE)
            WIN.blit(sub_title, (WIDTH/2 - sub_title.get_width()/2, 
                                HEIGHT/2 + sub_title.get_height()))
            
            last_text_displayed = 1
            oldepoch = new_epoch

        elif last_text_displayed == 1:
            new_epoch = time.time()
            oldepoch = new_epoch
            last_text_displayed = 0
        
        #Update the display in every run of the loop
        pygame.display.update()
        pygame.time.wait(500)

def draw_first_level_screen():
    # We add the clock to keep track of the frames
    clock = pygame.time.Clock()
    clock.tick(FPS)

    # Filling the windows with a color RGB
    WIN.fill(WHITE)

    # Drawing surfaces in the screen
    WIN.blit(BACKGROUND_IMAGE, (0, 0))

    # Shows first level text
    level_1_text = HEALT_FONT.render('LEVEL 1', 1, WHITE)
    WIN.blit(level_1_text, (WIDTH/2 - level_1_text.get_width()/2, 
                                HEIGHT/2 - level_1_text.get_height()/2))
    
    # Updates screen
    pygame.display.update()
    pygame.time.wait(1300)

# Draws the game in the loop
def draw_window(spaceship, aliens, bullets, user_score, spaceship_health, explosion_group):
    # Filling the windows with a color RGB
    WIN.fill(WHITE)

    # Drawing surfaces in the screen
    WIN.blit(BACKGROUND_IMAGE, (0, 0))

    # Draws aliens on screen
    for alien in aliens:
        WIN.blit(ALIEN_IMAGE, (alien.x, alien.y))

    # Takes care of explosions from collisions
    explosion_group.draw(WIN)
    explosion_group.update()

    # Draws the user's spaceship
    WIN.blit(SPACESHIP_IMAGE, (spaceship.x, spaceship.y))

    # Draws the current score of the player
    score_text = HEALT_FONT.render(str(user_score), 1, WHITE)
    WIN.blit(score_text, (score_text.get_width()-10, 10))

    # Draws the current health of the user
    health_text = HEALT_FONT.render("Health "+str(spaceship_health), 1, WHITE)
    WIN.blit(health_text, (WIDTH - health_text.get_width()-10, 10))

    # Draws bullets shot by the user on the screen
    for bullet in bullets:
        pygame.draw.rect(WIN, PURPLE, bullet)

    #Update the display in every run of the loop
    pygame.display.update()

# Signals if the user hasn't lost for the first time.
first_game = True
# Main function that runs the game
def main():
    global VEL_ALIEN, first_game

    # Loops through the start game screen until the user presses down the Enter key
    # and if this user hasn't lost yet
    if first_game:
        start_game_screen()
    
    # Draws the first level text on the screen
    draw_first_level_screen()

    # Rectangle to keep track of the user spaceship
    spaceship = pygame.Rect(300, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    # Rectangle to keep track of the alien
    aliens = []
    for x in range(8):
        alien = pygame.Rect(60 * x + 30, ALIEN_HEIGHT, ALIEN_WIDTH, ALIEN_HEIGHT)
        aliens.append(alien)
    # Bullets fired by the user
    bullets = []

    # Explosions from collisions
    explosion_group = pygame.sprite.Group()

    user_score = 0
    spaceship_health = 5
    level_number = 1

    # Control the speed of the while loop
    clock = pygame.time.Clock()
    # Game loop that terminates when the games end
    run = True
    oldepoch = time.time()
    while run:
        # Making sure the game runs at the set FPS
        clock.tick(FPS)

        new_epoch = time.time() 
        if new_epoch - oldepoch >= 1:
            oldepoch = new_epoch
            for x in range(8):
                alien = pygame.Rect(60 * x + 30, ALIEN_HEIGHT, ALIEN_WIDTH, ALIEN_HEIGHT)
                aliens.append(alien)

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

            if event.type == USER_HIT:
                user_score += 1

            if event.type == ALIEN_HIT:
                spaceship_health -= 1
                if spaceship_health <= 0:
                    spaceship_health = 0


        # Draw and check for bullet hits to aliens
        handle_bullets(bullets, aliens, explosion_group)

        # Read keys pressed by the user
        keys_pressed = pygame.key.get_pressed()
        # Move the user spaceship
        spaceship_movement(keys_pressed, spaceship)
        # Move the alien
        alien_movement(aliens, spaceship, explosion_group)

        # Update position of the player and aliens
        draw_window(spaceship, aliens, bullets, user_score, spaceship_health, explosion_group)

        # DISPLAY CHANGES WHEN USER LOSES THE GAME
        if spaceship_health <= 0:
            first_game = False
            game_over_text = 'GAME OVER'
            # Display text to the user to show that they have lost the game
            draw_end_screen_text(game_over_text)
            # Clear the game of the previous text screen
            draw_window(spaceship, aliens, bullets, user_score, spaceship_health, explosion_group)
            final_score_text = "FINAL SCORE " + str(user_score)
            # Display text to the user to show that they have lost the game
            draw_end_screen_text(final_score_text)
            # Display Play Again? Screen
            draw_play_again_screen()
            main()
        
        # DISPLAY CHANGES FOR NEW LEVEL
        # New level is reached when the user makes 10 points; shoots 10 aliens
        # So this screen is only displayed when the user scores 10 points and the remainder of the score and level is 10 
        # i.e. 10%1 = 10, 15%1 != 10,  20/2 = 10, and so on
        if (user_score % 10 == 0) and (user_score > 0) and (user_score / level_number == 10):
            # Text to showcase the level was cleared
            level_text = 'LEVEL CLEARED'
            # New level is gotten from when user makes 10 points; shoots 10 aliens
            new_level_number = user_score//10
            # Draws the text to signal the current level has been cleared
            aliens = []
            bullets = []
            explosion_group = pygame.sprite.Group()
            draw_next_level_screen_text(level_text)
            # Clear the game of the previous text screen
            draw_window(spaceship, aliens, bullets, user_score, spaceship_health, explosion_group)
            # Signal text to start new level
            draw_new_level_text(new_level_number + 1) # Adds 1 because we start on the first level
            if VEL_ALIEN < VEL:
                VEL_ALIEN *= new_level_number
            level_number += 1
            pygame.event.clear()
    
    pygame.quit() # End the game

if __name__ == "__main__":
    main()