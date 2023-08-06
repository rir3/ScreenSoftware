import pygame
import sys

# Initialize Pygame
pygame.init()

# Set up the display
screen = pygame.display.set_mode((400, 300))
pygame.display.set_caption("Read Second Enter Button")

# Main loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                if pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    print("Second Enter Button Pressed")