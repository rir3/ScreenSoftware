import pygame as py
from pygame import mixer #for audio
from moviepy.editor import VideoFileClip as vd #for video
from moviepy.editor import vfx #for video speed control

class Type:
    def __init__(self,py,screen):
        self.pygame = py
        self.screen = screen
        self.screen.fill((0,0,0,0))
        print("started")

    #Initial Setup Code
    def set_up(self):
        pass

    #Looped Code
    def loop(self):
        pass

    #Exits Loop
    def exit_flag(self):
        pass

class Image(Type):
    def __init__(self,py, screen,path):
        self.pygame = py

        self.screen = screen
        self.screen.fill((0,0,0,0))
        self.screen_width = self.pygame.display.Info().current_w
        self.screen_height = self.pygame.display.Info().current_h

        self.path = path
        self.image = self.pygame.image.load(self.path).convert()
        self.aspect_ratio = self.image.get_width() / self.image.get_height()
        self.image_width = self.image.get_size()[0]
        self.image_height = self.image.get_size()[1]
        print("Started")

    def calc_height(self):
        return int(self.screen_width / self.aspect_ratio)
    
    def calc_width(self):
        return int(self.screen_height * self.aspect_ratio)
    
    def center(self):
        top_margin = int((self.screen_height - self.image_height)/2)
        left_margin = int((self.screen_width - self.image_width)/2)

        if(top_margin>0 or left_margin > 0):
            if(top_margin > 0):
                self.screen.blit(self.image, (0, top_margin))
            if(left_margin > 0):
                self.screen.blit(self.image, (left_margin, 0))
        else:
            self.screen.blit(self.image, (0, 0))

    def scale(self):
        if(self.image_width > self.image_height):
            self.image = self.pygame.transform.scale(self.image, (self.screen_width, self.calc_height()))
        elif(self.image_height> self.image_width):
            self.image = self.pygame.transform.scale(self.image, (self.calc_width(), self.screen_height))
        else:
            if(self.screen_width < self.screen_height):
                self.image = self.pygame.transform.scale(self.image, (self.screen_width, self.calc_height()))
            else:
                self.image = self.pygame.transform.scale(self.image, (self.calc_width(), self.screen_height))

    def setup(self):
        # Scale the image
        self.scale()

        # Using blit to copy content from one surface to other
        self.center()

    def exit_flag(self):
        print("Exit")
        return False

    def loop(self):
        return super().view_loop()

class Video(Type):
    def __init__(self,py,screen,path,vd, speed_factor = 1, looped = False):
        self.pygame = py
        self.videofile = vd

        self.screen = screen
        self.screen.fill((0,0,0,0))
        self.screen.width = self.pygame.display.Info().current_w
        self.screen.height = self.pygame.display.Info().current_h

        self.path = path
        self.video = self.videofile(self.path)
        self.aspect_ratio = self.image.get_width() / self.image.get_height()
        self.height =self.video.size[1]
        self.width = self.video.size[0]
        
        self.looped = looped
        self.speed_factor = speed_factor
        print("Started")

    def speed_modifier(self,speed_factor = 1):
        # Video Already At Speed 1
        if(speed_factor == 1):
            return
        
        # Calculate the new duration for the double speed video
        new_duration = self.video.duration / speed_factor

        # Speed up the video clip
        clip = self.video.fx( vfx.speedx, speed_factor)

        # Trim the sped up clip to the new duration
        self.video = clip.subclip(0, new_duration)

    def center(self):
        #Calculates top Margin for Video to be Center
        #does not work for when using multiple monitors
        top_margin = int((self.screen.height - self.height)/2) #int used for not float
        left_margin = int((self.screen.width - self.width)/2) #int used for not float

        if(top_margin > 0):
            self.video = self.video.margin(top=top_margin)
        if(left_margin > 0):
            self.video = self.video.margin(left=left_margin)

    def scale(self):
        if(self.width > self.height):
            self.video = self.video.resize(width=self.screen.width)
        elif(self.height > self.width):
            self.video = self.video.resize(height=self.screen.height)
        else:
            if(self.screen.width < self.screen.height):
                self.video = self.video.resize(width=self.screen.width)
            else:
                self.video = self.video.resize(height=self.screen.height)

    def play(self):
        # Edit the video clip
        video_clip = scale_video(video_clip)
        video_clip = video_speed_modifier(video_clip, speed_factor)
        video_clip = center_video(video_clip)

        #Audio
        if(audio_path != "na"):
            mixer.init()
            mixer.music.load(audio_path)
            mixer.music.set_volume(0.7)

        play_video = True
        play_audio =  False if audio_path == "na" else True
        current_time = 0 
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
                    play_audio = False if audio_path == "na" else True
                else:
                    play_video = False
                    play_audio = False

            # Check if audio is playing
            if pygame.mixer.music.get_busy():
                current_time = pygame.mixer.music.get_pos()/1000 #Play Video at Audio Pace
            else:
                current_time += 1 / video_clip.fps #Increment current_time Pace Controled by clock

            # pygame clock control
            clock.tick(video_clip.fps)
    
        # Close the video clip
        video_clip.close()

def create_screen():
    # Initialize Pygame
    py.init()

    # Get information about the available displays
    screen_info = py.display.Info()
    num_displays = py.display.get_num_displays()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    # Set up the Pygame displays
    screen = py.display.set_mode((screen_width*num_displays, screen_height), py.RESIZABLE)

    return screen

def loop(type):
    pygame = py
    clock = pygame.time.Clock()
    running = True
    type.setup()
    while running:
        running = type.exit_flag()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.VIDEORESIZE:
                type.setup()
        
        # RENDER YOUR GAME HERE
        type.loop()

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

def blah():
    print("dog")

def main():
    screen = create_screen()
    dog = Image(py, screen, "Maze.png")
    #dog.set_up()
    loop(dog)
    

if __name__ == "__main__":
    main()