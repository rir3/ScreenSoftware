import pygame as py
from pygame import mixer #for audio
from moviepy.editor import VideoFileClip as vd #for video
from moviepy.editor import vfx #for video speed control
import time
import sys

class Type:
    def __init__(self,screen,interval = None):
        self.pygame = py
        self.screen = screen
        self.interval = interval # Millsec to Seconds
        self.exit = False
        self.start_time = int()

    #Initial Setup Code
    def setup(self):
        self.screen.fill((0,0,0,0))
        self.start_time = self.pygame.time.get_ticks()

    #Elapsed Time Trigger
    def time_elaspe(self):
        current_time = self.pygame.time.get_ticks()
        if(self.interval == 0):
            return False
        elif current_time - self.start_time >= self.interval:
            return True
        else:
            return False
    
    #Triggered After Elasped Time
    def after_time_elapsed(self):
        pass

    #Code That Runs Loop
    def main_loop(self):
        pygame = self.pygame
        clock = pygame.time.Clock()
        running = True
        self.setup()
        while running:
            running = not self.exit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    self.close()
                    self.quit()
                #elif event.type == pygame.VIDEORESIZE:
                    #self.setup()
                self.events(event)

            if(self.time_elaspe()):
                self.exit = True
                #self.after_time_elapsed()

            # GAME RENDERED HERE
            self.loop()

            pygame.display.flip()

            clock.tick(60)

    #Handles Events from Keyboard/Mouse/OS
    def events(self,event):
        pass

    #Looped Code
    def loop(self):
        pass

    #Exits Loop
    def exit_flag(self):
        pass

    #Safely Close Resources
    def close(self):
        pass

    #Quit Application
    def quit(self):
        py.quit()
        sys.exit()

class Image(Type):
    def __init__(self,screen,path,interval = int()):
        super().__init__(screen,interval)
        self.screen_width = self.pygame.display.Info().current_w
        self.screen_height = self.pygame.display.Info().current_h

        self.path = path
        self.image = self.pygame.image.load(self.path).convert()
        self.aspect_ratio = self.image.get_width() / self.image.get_height()

    def calc_height(self):
        return int(self.screen_width / self.aspect_ratio)
    
    def calc_width(self):
        return int(self.screen_height * self.aspect_ratio)
    
    def get_width(self):
        return self.image.get_size()[0]
    
    def get_height(self):
        return self.image.get_size()[1]
    
    def center(self):
        top_margin = int((self.screen_height - self.get_height())/2)
        left_margin = int((self.screen_width - self.get_width())/2)

        if(top_margin>0 or left_margin > 0):
            if(top_margin > 0):
                self.screen.blit(self.image, (0, top_margin))
            if(left_margin > 0):
                self.screen.blit(self.image, (left_margin, 0))
        else:
            self.screen.blit(self.image, (0, 0))

    def scale(self):
        if(self.get_width() > self.get_height()):
            self.image = self.pygame.transform.scale(self.image, (self.screen_width, self.calc_height()))
        elif(self.get_height()> self.get_width()):
            self.image = self.pygame.transform.scale(self.image, (self.calc_width(), self.screen_height))
        else:
            if(self.screen_width < self.screen_height):
                self.image = self.pygame.transform.scale(self.image, (self.screen_width, self.calc_height()))
            else:
                self.image = self.pygame.transform.scale(self.image, (self.calc_width(), self.screen_height))

    def setup(self):
        super().setup()
        
        # Scale the image
        self.scale()

        # Using blit to copy content from one surface to other
        self.center()

class Video(Type):
    def __init__(self, screen, path, audio_path = "na", clip = None, speed_factor = 1, looped = False, interval = int()):
        super().__init__(screen,interval)

        self.videofile = vd
        self.screen_width = self.pygame.display.Info().current_w
        self.screen_height = self.pygame.display.Info().current_h

        self.audio_path = audio_path
        #Audio
        if(self.audio_path != "na"):
            mixer.init()
            self.audio = mixer.music
            self.audio.load(self.audio_path)
            self.audio.set_volume(0.7)

        self.path = path
        self.video = self.videofile(self.path)
        if(clip != None):
            self.video = self.video.subclip(0, clip)
        #self.height = self.video.size[1]
        #self.width = self.video.size[0]

        self.looped = looped
        self.speed_factor = speed_factor

    def get_width(self):
        return self.video.size[0]

    def get_height(self):
        return self.video.size[1]
    
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
        top_margin = int((self.screen_height - self.get_height())/2) #int used for not float
        left_margin = int((self.screen_width - self.get_width())/2) #int used for not float
        
        if(top_margin > 0):
            self.video = self.video.margin(top=top_margin)
        if(left_margin > 0):
            self.video = self.video.margin(left=left_margin)

    def scale(self):
        if(self.get_width() > self.get_height()):
            self.video = self.video.resize(width=self.screen_width)
        elif(self.get_height() > self.get_width()):
            self.video = self.video.resize(height=self.screen_height)
        else:
            if(self.screen_width < self.screen_height):
                self.video = self.video.resize(width=self.screen_width)
            else:
                self.video = self.video.resize(height=self.screen_height)
    
    def close(self):
        if(self.audio_path != "na"):
            self.audio.stop()
        self.video.close()

    def setup(self):
        super().setup()

        # Edit the video clip
        self.scale()
        self.speed_modifier()
        self.center()

        self.current_time = 0
        if(self.audio_path != "na"):
            self.audio.play()    

    def loop(self):
        # Display video frame
        frame = self.video.get_frame(self.current_time)

        # pygame frame render
        pygame_frame = self.pygame.surfarray.make_surface(frame.swapaxes(0,1))
        self.screen.blit(pygame_frame, (0, 0))

        if self.current_time >= self.video.duration:
            # Reset the adjusted time to loop the video
            if self.looped:
                self.setup()
            else:
                self.exit = True

        # Check if audio is playing
        if self.pygame.mixer.music.get_busy():
            self.current_time = self.pygame.mixer.music.get_pos()/1000 #Play Video at Audio Pace
        else:
            self.current_time += 1 / self.video.fps #Increment current_time Pace Controled by clock

class UserInput(Type):
    def __init__(self,screen,interval = int()):
        super().__init__(screen, interval)
        self.time = time
        self.modal_visible = True
        self.modal_toggable = False
    
    def modal(self):
        # White Box for Text Entry
        self.screen.fill((255,255,255,255),(300,200,900,900))
        
        surface1 = self.font.render('ENTER', True, (0, 0, 0))
        surface2 = self.font.render(self.modal_text, True, (0, 0, 0))
        surface3 = self.font.render('_________________', True, (0, 0, 0))

        self.screen.blit(surface1, (575, 375))
        self.screen.blit(surface2, (500, 450))
        self.screen.blit(surface3,  (400, 718))
    
    def loop(self):
        if(self.modal_visible):
            user_text_surface = self.font.render(self.user_input, True, (0, 0, 0))
            self.screen.blit(user_text_surface, (450, 718))

    def passphrase(self,event):
        if event.key == self.pygame.K_BACKSPACE:
            self.user_input = self.user_input[:-1]
            self.modal()
        elif event.key == self.pygame.K_RETURN or event.key == self.pygame.K_KP_ENTER:
            if self.user_input.upper() == self.code.upper():
                self.exit = True
            elif self.user_input.upper() != self.code.upper():
                self.wrong_input()
                self.modal()
        elif len(self.user_input)<self.code_limit:
            self.user_input += event.unicode.upper()

    def wrong_input(self):
        self.user_input = ""
        font = py.font.Font(None, 50)
        text_surface_red = font.render(self.wrong_text, True, (255, 0, 0))
        self.screen.blit(text_surface_red, (525, 525))
        py.display.flip()
        self.time.sleep(1)
    
    def toggle_modal(self,event):
        if not self.modal_toggable:
            return
        elif event.key == self.pygame.K_LCTRL:
            self.modal_visible = not self.modal_visible
            self.setup()

    def selection(self, event):
        if event.key == self.pygame.K_BACKSPACE:
            return False
        elif event.key == self.pygame.K_RETURN or event.key == self.pygame.K_KP_ENTER:
            return True

class UIInput(UserInput):
    def __init__(self,screen,code,img_path = str(),modal_first=True,is_code=False,code_limit=7,interval = int()):
        super().__init__(screen,interval)

        self.img_path = img_path
        self.code = code
        self.user_input = ""
        self.code_limit = code_limit
        self.modal_first = modal_first

        if(not self.modal_first):
            self.modal_toggable = True
            self.modal_visible = False
        if(not is_code):
            self.modal_text = 'PASSWORD'
            self.wrong_text = 'WRONG PASSWORD!'
        else:
            self.modal_text = f'{self.code_limit} DIGIT CODE:'
            self.wrong_text = 'WRONG CODE!'

    #Initial Setup Code
    def setup(self):
        super().setup()

        self.user_input = ""
        self.font = self.pygame.font.Font(None, 100)
        
        # Aqua Background
        self.screen.fill((35,250,247,255))

        if(self.img_path != ""):
            Image(self.screen,self.img_path,100).main_loop()
        if(self.modal_visible):
            self.modal()
        
    def events(self,event):
        if event.type == self.pygame.KEYDOWN:
            self.toggle_modal(event)
            if self.modal_visible:
                self.passphrase(event)

class UIImage(UserInput):
    def __init__(self,screen,img_path = str(),interval = int()):
        super().__init__(screen,interval)
        self.img_path = img_path
        self.modal_toggable = False
        self.modal_visible = False
    
    #Initial Setup Code
    def setup(self):
        super().setup()
        Image(self.screen,self.img_path,100).main_loop()
    
    def events(self,event):
        if event.type == self.pygame.KEYDOWN:
            selection = self.selection(event)
            if(selection is not None):
                self.exit = True

def create_screen():
    # Initialize Pygame
    py.init()
    py.display.set_caption("Screen Software")

    # Get information about the available displays
    screen_info = py.display.Info()
    num_displays = py.display.get_num_displays()
    screen_width = screen_info.current_w
    screen_height = screen_info.current_h

    # Set up the Pygame displays
    screen = py.display.set_mode((screen_width*num_displays, screen_height), py.FULLSCREEN)

    return screen

def main():
    screen = create_screen()
    #UIInput(screen,"666","Maze.png",True).main_loop()
    
    lists = [Video(screen,"static2.mp4","na",5), UIInput(screen,"sam"), Video(screen,"outpy.avi"), UIInput(screen,"sam","Maze.png",False,True), UIImage(screen,"sel.jpg"),Video(screen,"bad_ending.mp4","bad_ending.mp3")]
    for i in lists:
        i.main_loop()
    
if __name__ == "__main__":
    main()