from moviepy.editor import VideoFileClip
import pygame
from pygame.locals import *
import time
import VideoPlayer

def clear():
    screen.fill((0,0,0,0))

def destroy():
    pygame.quit()
    exit()
########################## STATIC SCREEN ##########################
def show_static():
    logger.info("Reached: show_static()")
    VideoPlayer.play_video_helper(staticVideo,"na",screen, 1, True)
    clear()

    while True:
        if comms_mode:
            status_found, break_loop = comms_rw("read", "Show Login")
            if break_loop:
                return True
            if status_found:
                return False
        
        if adminMode:
            # Check for events and exit if the user presses the escape key
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    destroy()
                # Space for next Screen
                if event.type == KEYDOWN and event.key == K_SPACE:
                    return False