import pygame
from moviepy.editor import VideoFileClip

# Initialize Pygame
pygame.init()

# Set up the Pygame display
screen_info = pygame.display.Info()
screen_width = screen_info.current_w
screen_height = screen_info.current_h
screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()

# Define the speedup factor
speedup_factor = 2

# Load the video clip
video_path = "WindowWall.mp4"
video_clip = VideoFileClip(video_path).resize(height=screen_height)

# Play the video while capturing user input
play_video = True
while play_video:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            play_video = False

        # Capture other user input events here
    
    # Get the current time in the video
    current_time = pygame.time.get_ticks() / 1000

    # Calculate the adjusted time for faster playback
    adjusted_time = current_time * speedup_factor

    # Display video frame
    frame = video_clip.get_frame(pygame.time.get_ticks() / 1000)
    pygame_frame = pygame.surfarray.make_surface(frame.swapaxes(0,1))
    screen.blit(pygame_frame, (0, 0))
    pygame.display.flip()

    clock.tick(video_clip.fps)

# Quit Pygame
pygame.quit()

# Close the video clip
video_clip.close()
