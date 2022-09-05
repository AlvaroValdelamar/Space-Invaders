from turtle import width
import pygame

# Creating game window
WIDTH, HEIGHT = 500, 500 # WIDTH, HEIGHT of the screen window
WIN = pygame.display.set_mode((WIDTH, HEIGHT))

def main():

    # Game loop that terminates when the games end
    run = True
    while run:

        # Looping through events in the game
        for event in pygame.event.get():
            
            # check if user quitted the game
            if event.type == pygame.QUIT:
                run = False # Exit while loop
            
    
    pygame.quit() # End the game

if __name__ == "__main__":
    main()