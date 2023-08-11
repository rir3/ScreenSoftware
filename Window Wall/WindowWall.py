#StaticScreen.mp4
#StaticScreen.mov
from moviepy.editor import VideoFileClip
import pygame
from pygame.locals import *
import time

# Initialize Pygame
pygame.init()

# Set up the Pygame display
screen = pygame.display.set_mode((2160, 1920), pygame.RESIZABLE)

#Hides Mouse
#pygame.mouse.set_visible(False)

#Resources
stealingVideo = "WindowWall.mp4"   #"Stealing.mp4"   -   "outpy.avi"

#Settings

#Window Wall Settings
scale_factor = .75 #1.75
top_border = 100
left_border = 710

#Macbook Settings
#scale_factor = 1.15
#top_border = 500

########################## Window SCREEN ##########################
def showWindow():
    screen.fill((0,0,0,0))
    # Load the video file
    clip = VideoFileClip(stealingVideo)
    clip = clip.subclip(1, 76)#starts at 24 sec end 48 sec

    while True:
        # Iterate over each frame of the video and display it in the Pygame window
        for frame in clip.iter_frames(fps=clip.fps):
            surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))
            # Get the original dimensions of the image
            orig_size = surface.get_size()

            # Set the scale factor
            #scale_factor = 1.75

            # Scale the image
            scaled_surface = pygame.transform.scale(surface, (orig_size[0]*scale_factor, orig_size[1]*scale_factor))
            
            screen.blit(scaled_surface, (left_border, top_border))
            time.sleep(.025)
            pygame.display.flip()

            # Check for events and exit if the user presses the escape key
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                # Space for next Screen
                if event.type == KEYDOWN and event.key == K_SPACE:
                    return


showWindow()
