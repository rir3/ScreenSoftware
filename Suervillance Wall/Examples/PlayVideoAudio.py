import pygame
from pygame import mixer
#from moviepy.editor import VideoFileClip
# Import everything needed to edit video clips
from moviepy.editor import VideoFileClip
from moviepy.editor import vfx

def video_speed_modifier(video_clip, speed_factor = 1):
    # Video Already At Speed 1
    if(speed_factor == 1):
        return video_clip
    
    # Calculate the new duration for the double speed video
    new_duration = video_clip.duration / speed_factor

    # Speed up the video clip
    clip = video_clip.fx( vfx.speedx, speed_factor)

    # Trim the sped up clip to the new duration
    clip = clip.subclip(0, new_duration)

    return clip

def center_video(video_clip):
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    #Calculates top Margin for Video to be Center
    video_height = video_clip.size[1]
    top_margin = int((screen_height - video_height)/2) #int used for not float
    #does not work for when using multiple monitors

    vide_width = video_clip.size[0]
    left_margin = int((screen_width - vide_width)/2) #int used for not float

    if(top_margin > 0):
        video_clip = video_clip.margin(top=top_margin)
    if(left_margin > 0):
        video_clip = video_clip.margin(left=left_margin)

    return video_clip

def scale_video(video_clip):
    screen_info = pygame.display.Info()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    vide_width = video_clip.size[0]
    video_height = video_clip.size[1]

    if(vide_width > video_height):
        video_clip = video_clip.resize(width=screen_width)
    elif(video_height > vide_width):
        video_clip = video_clip.resize(height=screen_height)
    else:
        if(screen_width < screen_height):
            video_clip = video_clip.resize(width=screen_width)
        else:
            video_clip = video_clip.resize(height=screen_height)
        
    return video_clip

def play_video(video_path, audio_path, screen, speed_factor = 1, loop_video = False):
    # Load the video clip
    video_clip = VideoFileClip(video_path)

    # Edit the video clip
    video_clip = scale_video(video_clip)
    #video_clip = video_clip.subclip(0, 75)
    video_clip = video_speed_modifier(video_clip, speed_factor)
    video_clip = center_video(video_clip)

    #Audio
    mixer.init()
    mixer.music.load(audio_path)
    mixer.music.set_volume(0.7)

    #Add Code to handle width
    # Play the video while capturing user input
    play_video = True
    play_audio = True
    current_time = 0  # Initialize current_time

    # pygame clock instanication
    clock = pygame.time.Clock()

    while play_video:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                play_video = False
                play_audio = False
            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                play_video = False
                play_audio = False

            # Capture other user input events here
        
        # Get the current time in the video
        #current_time = pygame.time.get_ticks() / 1000

        # Display video frame
        frame = video_clip.get_frame(current_time)

        # pygame frame render
        pygame_frame = pygame.surfarray.make_surface(frame.swapaxes(0,1))
        screen.blit(pygame_frame, (0, 0))

        if(play_audio):
            play_audio = False
            mixer.music.play()#plays audio

        pygame.display.flip()

        # Check if the adjusted time exceeds the video duration
        if current_time >= video_clip.duration:
            # Reset the adjusted time to loop the video
            if loop_video:
                current_time = 0
            else:
                play_video = False
                play_audio = False

        current_time += 1 / video_clip.fps  # Increment current_time

        # pygame clock control
        clock.tick(video_clip.fps)
   
    # Close the video clip
    video_clip.close()

def create_screen():

    # Initialize Pygame
    pygame.init()

    # Get information about the available displays
    screen_info = pygame.display.Info()
    num_displays = pygame.display.get_num_displays()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    # Set up the Pygame displays
    screen = pygame.display.set_mode((screen_width*num_displays, screen_height), pygame.RESIZABLE)

    return screen

def destroy_screen():
    # Quit Pygame
    pygame.quit()

def main():
    screen = create_screen()
    video = "bad_ending.mp4"
    audio = "bad_ending.mp3"
    speed = 1

    play_video(video, audio, screen, speed)

if __name__ == "__main__":
    main()