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


explosion_group = pygame.sprite.Group()



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
def alien_movement(aliens, spaceship):
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
def handle_bullets(bullets, aliens):
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
    pygame.time.delay(5000)

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

# Draws the game in the loop
def draw_window(spaceship, aliens, bullets, user_score, spaceship_health):
    # Filling the windows with a color RGB
    WIN.fill(WHITE)

    # Drawing surfaces in the screen
    WIN.blit(BACKGROUND_IMAGE, (0, 0))

    for alien in aliens:
        WIN.blit(ALIEN_IMAGE, (alien.x, alien.y))

    explosion_group.draw(WIN)
    explosion_group.update()

    WIN.blit(SPACESHIP_IMAGE, (spaceship.x, spaceship.y))

    score_text = HEALT_FONT.render(str(user_score), 1, WHITE)
    WIN.blit(score_text, (score_text.get_width()-10, 10))

    health_text = HEALT_FONT.render("Health "+str(spaceship_health), 1, WHITE)
    WIN.blit(health_text, (WIDTH - health_text.get_width()-10, 10))

    for bullet in bullets:
        pygame.draw.rect(WIN, PURPLE, bullet)

    #Update the display in every run of the loop
    pygame.display.update()

# Main function that runs the game
def main():
    global VEL_ALIEN
    # Rectangle to keep track of the user spaceship
    spaceship = pygame.Rect(300, 300, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    # Rectangle to keep track of the alien
    aliens = []
    for x in range(8):
        alien = pygame.Rect(60 * x + 30, ALIEN_HEIGHT, ALIEN_WIDTH, ALIEN_HEIGHT)
        aliens.append(alien)
    # Bullets fired by the user
    bullets = []

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
                explosions = []

            if event.type == ALIEN_HIT:
                spaceship_health -= 1
                if spaceship_health <= 0:
                    spaceship_health = 0
                explosions = []


        # Draw and check for bullet hits to aliens
        handle_bullets(bullets, aliens)

        # Read keys pressed by the user
        keys_pressed = pygame.key.get_pressed()
        # Move the user spaceship
        spaceship_movement(keys_pressed, spaceship)
        # Move the alien
        alien_movement(aliens, spaceship)

        # Update position of the player and aliens
        draw_window(spaceship, aliens, bullets, user_score, spaceship_health)

        # DISPLAY CHANGES WHEN USER LOSES THE GAME
        if spaceship_health <= 0:
            game_over_text = 'GAME OVER'
            # Display text to the user to show that they have lost the game
            draw_end_screen_text(game_over_text)
            # Clear the game of the previous text screen
            draw_window(spaceship, aliens, bullets, user_score, spaceship_health)
            final_score_text = "FINAL SCORE " + str(user_score)
            # Display text to the user to show that they have lost the game
            draw_end_screen_text(final_score_text)
            break
        
        # DISPLAY CHANGES FOR NEW LEVEL
        if (user_score % 10 == 0) and (user_score > 0) and (user_score / level_number == 10):
            level_text = 'LEVEL CLEARED'
            new_level_number = user_score//10
            # Draws the text to signal the current level has been cleared
            draw_next_level_screen_text(level_text)
            # Clear the game of the previous text screen
            draw_window(spaceship, aliens, bullets, user_score, spaceship_health)
            # Signal text to start new level
            draw_new_level_text(new_level_number)
            aliens = []
            if VEL_ALIEN < VEL:
                VEL_ALIEN *= new_level_number
            level_number += 1 
    
    pygame.quit() # End the game

if __name__ == "__main__":
    main()