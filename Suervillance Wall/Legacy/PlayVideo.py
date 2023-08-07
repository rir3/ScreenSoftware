import pygame
from moviepy.editor import VideoFileClip
import time


pygame.display.set_caption('SA-Wall')#Window Name

#Resources
video = "bad_ending.mp4"

# Initialize Pygame
pygame.init()

screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
print(screen_width)

screen = pygame.display.set_mode((2160, 1920), pygame.RESIZABLE)

#Macbook Settings
scale_factor = 1.15
top_border = 0

def play_video(video):
    screen.fill((0,0,0,0))
    # Load the video file
    clip = VideoFileClip(video)

    for frame in clip.iter_frames(fps=clip.fps):
        pygame.event.pump() # Keeps from Idle
        time.sleep(0.05) #(20 fps)
        surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))
        # Get the original dimensions of the image
        orig_size = surface.get_size()

        # Set the scale factor
        scale_adj_factor = 1

        # Scale the image
        scaled_surface = pygame.transform.scale(surface, (orig_size[0]*scale_factor*scale_adj_factor, orig_size[1]*scale_factor*scale_adj_factor))
            
        screen.blit(scaled_surface, (0, top_border))
        time.sleep(.05)
        pygame.display.flip()

def play_video_2(video):
    clip = VideoFileClip(video).resize(width=screen_width)

    #Calculates top Margin for Video to be Center
    video_height = clip.size[1]
    top_margin = int((screen_height - video_height)/2) #int used for not float

    clip = clip.margin(top=top_margin)
    clip.preview(fullscreen=True)

#play_video(video)
play_video_2(video)
pygame.quit()