import sys
from moviepy.editor import VideoFileClip
import pygame
from pygame.locals import *
import time
import RecordWebCam
import COGS_Communication
import threading
from queue import Queue


#Settings
recording = True
comms_mode = False #Disables/Enables Communication Mode for COGS Communication (Arduino)
adminMode = True #Allows you to skip screens and view mouse
macBook = True #Enables screen settings for macBook pro 15

pygame.display.set_caption('SA-Wall')#Window Name

#Resources
arduinoPort = '/dev/tty.usbmodem14201'
staticVideo = "StaticScreen.mp4"
loginPassword = "Rebecca"
breakInVideo = "WebCamVideo.avi"#Must have end with .avi extension
mazeImage = "Maze.png"
mazeCode = "317208941"
choice_text = ""
status_found = False
goodEnding = "good_ending.mp4"
badEnding = "bad_ending.mp4"
good_ending = False

#Comms Resources
comms_started = False
tasks = Queue()
statuses = Queue()

# Initialize Pygame
pygame.init()

if macBook:
    #Macbook Settings
    print("Using Macbook Settings")
    scale_factor = 1.15
    top_border = 0
    arduinoPort = '/dev/tty.usbmodem14201'
else:
    #Screen Wall Settings
    print("Using Screen Wall Settings")
    scale_factor = 1.75
    top_border = 325
    extra = 0
    arduinoPort = 'COM3'

#Hides Mouse and Enables Screen Skip Settings
if not adminMode:
    #pygame.mouse.set_visible(False)
    print("Admin Mode: OFF")
else:
    print("Admin Mode: ON")
    mazeCode = "111111111"
    #staticVideo = "StaticScreen4k.mp4"

if comms_mode:
    print("Communication Mode: ON")
else:
    print("Communication Mode: OFF")


#Records Video from WebCam
#if recording:
#    print("Recording: ON")
    #Wait Time: 2min
#    RecordWebCam.record()
#else:
#    print("Recording: OFF")



# Set up the Pygame display
#pygame.event.pump()
screen = pygame.display.set_mode((2160, 1920), pygame.RESIZABLE)
#pygame.event.pump()
#def playVideo(videoName,)

def comms_start():
    global comms_started
    comms_started = True
    COGS_Communication.comms_helper(tasks, statuses)

def comms_rw(action, status="N/A"):
    reset_status = "Game Started"
    if(not comms_started):
        comms_start()
    elif(action == "write"):
        tasks.put(status)
    elif(action == "read"):
        while not statuses.empty():
            s = statuses.get()
            if(s == reset_status):
                return True, True
            elif(s == status):
                return True, False #Found status
        return False, False
    return False, False

def delay(delay_time):
    start_time = time.time()
    trigger_time = start_time + delay_time
    while True:
        pygame.event.pump() # Keeps from Idle
        time.sleep(0.1) #(20 fps)
        if time.time() > trigger_time:
            return 

def check_close_event():
    for event in pygame.event.get():
        pygame.event.pump() # Keeps from Idle
        time.sleep(0.1) #(20 fps)
        if event.type == KEYDOWN and event.key == K_ESCAPE and event.type == pygame.MOUSEBUTTONDOWN:
            pygame.quit()
            exit()

def record():
    RecordWebCam.record(breakInVideo)

def record_helper():
    global status_found
    status_found = False

    screen.fill((255,255,255,255),(300+top_border,200+top_border,900,900))#White Box
    text_font = pygame.font.Font(None, 50)#Font 50 Size
    text_surface = text_font.render('RECORDING IN PROGRESS!', True, (0, 0, 0))#Text Black Font
    screen.blit(text_surface, (575+top_border, 375+top_border))
    pygame.display.flip()

    record_thread = threading.Thread(target=record)
    record_thread.start()
    
    while record_thread.is_alive():
        delay(1)# Add Code to wait for thread to finish before continueing

########################## RECORD SCREEN ##########################
def show_record():
    global status_found
    screen.fill((0,0,0,0))     
    pygame.display.flip()
    #Records Video from WebCam
    if not recording:
        return False
    elif status_found:
        record_helper()
        return False
    elif comms_mode:
        while True:
            pygame.event.pump() # Keeps from Idle
            time.sleep(0.05) #(20 fps)
            status_found, break_loop = comms_rw("read", "Game Started")
            if status_found:
                record_helper()
                return False
    else:
        record_helper()
        return False
        
########################## STATIC SCREEN ##########################
def show_static(): 
    screen.fill((0,0,0,0))
    # Load the video file
    clip = VideoFileClip(staticVideo)
    #clip = clip.subclip(1, 9)
    
    #print("Here:1")
    #print("Here:2")
    while True:
        pygame.event.pump() # Keeps from Idle
        time.sleep(0.05) #(20 fps)
        #print("Here:3")
        # Iterate over each frame of the video and display it in the Pygame window
        for frame in clip.iter_frames(fps=clip.fps):
            pygame.event.pump() # Keeps from Idle
            time.sleep(0.15) #(20 fps)
            #print("Here:4")
            #pygame.event.pump()
            surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))

            # Get the original dimensions of the image
            orig_size = surface.get_size()

            # Set the scale factor
            #scale_factor = 1.75
            scale_adj_factor = .67

            # Scale the image
            scaled_surface = pygame.transform.scale(surface, (orig_size[0]*scale_factor*scale_adj_factor, orig_size[1]*scale_factor*scale_adj_factor))

            screen.blit(scaled_surface, (0, top_border))
            #time.sleep(.05)
            pygame.display.flip()

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
                        pygame.quit()
                        exit()
                    if event.type == KEYDOWN and event.key == K_ESCAPE and event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        exit()
                    # Space for next Screen
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        return False
            else:
                for event in pygame.event.get():
                    if event.type == KEYDOWN and event.key == K_ESCAPE and event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.quit()
                        exit()

########################## PASSWORD ENTRY SCREEN ##########################
def show_password_entry():
    screen.fill((0,0,0,0))

    clock = pygame.time.Clock()

    # basic font for user typed
    base_font = pygame.font.Font(None, 32)
    user_text = ''
      
    # create rectangle
    # Rect(left, top, width, height)
    input_rect = pygame.Rect(650, 618, 10, 32)
      
    # color of input box.
    color = pygame.Color('white')

    # Font for On Screen Text
    text = 'ENTER'
    text_pos = pygame.Rect(100, 618, 10, 32)
    text_font = pygame.font.Font(None, 100)

    text2 = '_________________'
    text2_pos = pygame.Rect(100, 618, 10, 32)
    text2_font = pygame.font.Font(None, 100)

    while True:
        pygame.event.pump() # Keeps from Idle
        time.sleep(0.05) #(20 fps)
        for event in pygame.event.get():
            pygame.event.pump() # Keeps from Idle
            time.sleep(0.05) #(20 fps)
      
          # if user types QUIT then the screen will close
            if event.type == pygame.QUIT and adminMode:
                pygame.quit()
                sys.exit()
                    
            if event.type == pygame.KEYDOWN:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                # Right Arrow for next Screen
                elif event.key == K_RIGHT and adminMode:
                    return
                elif event.key == K_RETURN:
                    if user_text.upper() == loginPassword.upper():
                        return False
                    else:
                        user_text = ""
                        text_font_Red = pygame.font.Font(None, 50)
                        text_surface = text_font_Red.render("WRONG PASSWORD!", True, (255, 0, 0))
                        screen.blit(text_surface, (525+top_border, 525+top_border))
                        pygame.display.flip()
                        time.sleep(1)
                
                elif len(user_text)<7:
                    user_text += event.unicode
                    user_text = user_text.upper()

        if comms_mode:
                status_found, break_loop = comms_rw("read")
                if break_loop:
                    return True
        # Aqua Background
        screen.fill((35,250,247,255))
        #screen.fill((0,0,0,0))
        
        # White Box for Text Entry
        screen.fill((255,255,255,255),(300+top_border,200+top_border,900,900))

        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(screen, color, input_rect)
      
        user_text_surface = text_font.render(user_text, True, (0, 0, 0))
        text2_surface = text_font.render(text2, True, (0, 0, 0))
        text_surface = text_font.render(text, True, (0, 0, 0))
        text3_surface = text_font.render('PASSWORD:', True, (0, 0, 0))
          
        # render at position stated in argumentsre
        screen.blit(text_surface, (575+top_border, 375+top_border))
        screen.blit(text3_surface, (500+top_border, 450+top_border))
        screen.blit(text2_surface,  (400+top_border, input_rect.y+100+top_border))
        screen.blit(user_text_surface, (400+50+top_border, input_rect.y+100+top_border))
          

        # set width of textfield so that text cannot get
        # outside of user's text input
        #input_rect.w = max(10, user_text_surface.get_width()+10)
          
        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()
          
        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)

########################## STEALING SCREEN ##########################
def show_break_in():
    screen.fill((0,0,0,0))
    # Load the video file
    clip = VideoFileClip(breakInVideo)
    #clip = clip.subclip(0, 14)#starts at \ sec end \ sec

    # Iterate over each frame of the video and display it in the Pygame window
    for frame in clip.iter_frames(fps=clip.fps):
        pygame.event.pump() # Keeps from Idle
        time.sleep(0.05) #(20 fps)
        surface = pygame.surfarray.make_surface(frame.swapaxes(0,1))
        # Get the original dimensions of the image
        orig_size = surface.get_size()

        # Set the scale factor
        scale_adj_factor = .67

        # Scale the image
        scaled_surface = pygame.transform.scale(surface, (orig_size[0]*scale_factor*scale_adj_factor, orig_size[1]*scale_factor*scale_adj_factor))
        
        screen.blit(scaled_surface, (0, top_border))
        time.sleep(.1)
        pygame.display.flip()

        if comms_mode:
                status_found, break_loop = comms_rw("read")
                if break_loop:
                    return True

        if adminMode:
            # Check for events and exit if the user presses the escape key
            for event in pygame.event.get():
                pygame.event.pump() # Keeps from Idle
                time.sleep(0.05) #(20 fps)
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                # Space for next Screen
                if event.type == KEYDOWN and event.key == K_SPACE:
                    return

########################## MAZE SCREEN ##########################
def show_maze():
    screen.fill((0,0,0,0))
    #Scale Factor Change
    scale_factor_diff = .325
    # get the default size
    x, y = screen.get_size()

    #print(x, y)

    # Set the dimensions of the screen
    screen_size = (x, y)

    # set the pygame window name
    #pygame.display.set_caption('image')
        
    # create a surface object, image is drawn on it.
    image = pygame.image.load(mazeImage).convert()
        
    #increase width of image
    # Get the original dimensions of the image
    orig_size = image.get_size()

    # Set the scale factor
    #scale_factor = 1.75

    # Scale the image
    scaled_image = pygame.transform.scale(image, (orig_size[0]*scale_factor*scale_factor_diff, orig_size[1]*scale_factor*scale_factor_diff))

    # Blit the scaled image to the center of the screen
    #screen.blit(scaled_image, (screen_size[0]/2 - scaled_image.get_width()/2, screen_size[1]/2 - scaled_image.get_height()/2))


    # Using blit to copy content from one surface to other
    screen.blit(scaled_image, (0, top_border))
        
    # paint screen one time
    pygame.display.flip()

    while True:
        pygame.event.pump() # Keeps from Idle
        time.sleep(0.05) #(20 fps)
        if comms_mode:
                status_found, break_loop = comms_rw("read")
                if break_loop:
                    return True
        if adminMode:
            # Check for events and exit if the user presses the escape key
            for event in pygame.event.get():
                pygame.event.pump() # Keeps from Idle
                time.sleep(0.1) #(20 fps)
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                # Space for next Screen
                if event.type == KEYDOWN and event.key == K_SPACE:
                    return False
                if event.type == KEYDOWN and event.key == K_RIGHT:
                    show_maze_password_entry()
                    return False
        else:
            # Check for events and exit if the user presses the escape key
            for event in pygame.event.get():
                pygame.event.pump() # Keeps from Idle
                time.sleep(0.1) #(20 fps)
                if event.type == KEYDOWN and event.key == K_RIGHT:
                    show_maze_password_entry()
                    return False
                if event.type == KEYDOWN and event.key == K_ESCAPE and event.type == pygame.MOUSEBUTTONDOWN:
                    pygame.quit()
                    exit()
########################## Maze PASSWORD ENTRY SCREEN ##########################
def show_maze_password_entry():
    screen.fill((0,0,0,0))

    clock = pygame.time.Clock()

    # basic font for user typed
    base_font = pygame.font.Font(None, 32)
    user_text = ''
      
    # create rectangle
    # Rect(left, top, width, height)
    input_rect = pygame.Rect(650, 618, 10, 32)
      
    # color of input box.
    color = pygame.Color('white')

    # Font for On Screen Text
    text = 'ENTER'
    text_pos = pygame.Rect(100, 618, 10, 32)
    text_font = pygame.font.Font(None, 100)

    text2 = '_________________'
    text2_pos = pygame.Rect(100, 618, 10, 32)
    text2_font = pygame.font.Font(None, 100)

    while True:
        pygame.event.pump() # Keeps from Idle
        time.sleep(0.05) #(20 fps)
        if comms_mode:
                status_found, break_loop = comms_rw("read")
                if break_loop:
                    return True
        for event in pygame.event.get():
            pygame.event.pump() # Keeps from Idle
            time.sleep(0.05) #(20 fps)
          # if user types QUIT then the screen will close
            if event.type == pygame.QUIT and adminMode:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                # Right Arrow for next Screen
                elif event.key == K_LEFT:
                    show_maze()
                    return
                elif event.key == K_RETURN:
                    if user_text == mazeCode:
                        if comms_mode:
                            comms_rw("write", "Maze Solved")
                        #showDecision()
                        return
                    else:
                        user_text = ""
                        text_font_Red = pygame.font.Font(None, 50)
                        text_surface = text_font_Red.render("WRONG CODE!", True, (255, 0, 0))
                        screen.blit(text_surface, (525+top_border, 525+top_border))
                        pygame.display.flip()
                        time.sleep(1)
                
                elif len(user_text)<9:
                    user_text += event.unicode
                    user_text = user_text.upper()

        # Aqua Background
        #screen.fill((35,250,247,255))
        #screen.fill((0,0,0,0))
        
        # White Box for Text Entry
        screen.fill((255,255,255,255),(300+top_border,200+top_border,900,900))

        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(screen, color, input_rect)
      
        user_text_surface = text_font.render(user_text, True, (0, 0, 0))
        text2_surface = text_font.render(text2, True, (0, 0, 0))
        text_surface = text_font.render(text, True, (0, 0, 0))
        text3_surface = text_font.render('9 DIGIT CODE:', True, (0, 0, 0))
          
        # render at position stated in argumentsre
        screen.blit(text_surface, (500+top_border, 375+top_border))
        screen.blit(text3_surface, (500+top_border, 450+top_border))
        screen.blit(text2_surface,  (400+top_border, input_rect.y+100+top_border))
        screen.blit(user_text_surface, (400+50+top_border, input_rect.y+100+top_border))
          

        # set width of textfield so that text cannot get
        # outside of user's text input
        #input_rect.w = max(10, user_text_surface.get_width()+10)
          
        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()
          
        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)

########################## Decision SCREEN ##########################
def show_decision():
    global choice_text
    global good_ending
    screen.fill((0,0,0,0))

    clock = pygame.time.Clock()

    # basic font for user typed
    base_font = pygame.font.Font(None, 32)
    user_text = ''
      
    # create rectangle
    # Rect(left, top, width, height)
    input_rect = pygame.Rect(650, 618, 10, 32)
      
    # color of input box.
    color = pygame.Color('white')

    while True:
        pygame.event.pump() # Keeps from Idle
        time.sleep(0.05) #(20 fps)
        if comms_mode:
                status_found, break_loop = comms_rw("read")
                if break_loop:
                    return True
        for event in pygame.event.get():
            pygame.event.pump() # Keeps from Idle
            time.sleep(0.05) #(20 fps)
            if event.type == pygame.QUIT and adminMode:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                # Right Arrow for next Screen
                #if event.key == K_RIGHT and adminMode:
                    #print("Duah")
                    #return
                # Delete Video
                if event.key == pygame.K_BACKSPACE:
                    if comms_mode:
                            comms_rw("write", "Bad Ending")
                    choice_text = "SECURITY DOOR OVERIDDEN"
                    good_ending = False
                    return False
                    #showChoice("VIDEO DELETED!")
                    #return
                # Leave Video
                elif event.key == K_RETURN:
                    if comms_mode:
                            comms_rw("write", "Good Ending")
                    choice_text = "DIAMOND THEFT REPORTED"
                    good_ending = True
                    return False
                    #showChoice("VIDEO NOT DELETED")
                    #return
        
        # White Box for Text Entry
        #screen.fill((255,255,255,255),(100+top_border+300,200+top_border,725,725))
        screen.fill((255,255,255,255),(300+top_border,200+top_border,900,900))

        # draw rectangle and argument passed which should
        # be on screen
        pygame.draw.rect(screen, color, input_rect)

        text_font = pygame.font.Font(None, 60)
        sub_text_font = pygame.font.Font(None, 40)


        text_surface = text_font.render('SECURITY FOOTAGE DELETED!', True, (0, 0, 0))
        text2_surface = text_font.render('SECURITY ALERT:', True, (0, 0, 0))
        text3_surface = sub_text_font.render('PRESS DELETE TO ESCAPE WITH DIAMOND ', True, (0, 0, 0))
        text4_surface = sub_text_font.render('PRESS ENTER TO REPORT DIAMOND THEFT', True, (0, 0, 0))
        
        
        left = 450
        sub = 50
        dub = 0#-100

        #For Testing
        #text_font_dup = pygame.font.Font(None, 60)
        #text_surface_dup = text_font_dup.render('ARE YOU SURE YOU WANT TO DELETE VIDEO!', True, (0, 0, 0))
        #screen.blit(text_surface_dup, (200+top_border, 375+top_border-70))

        # render at position stated in argumentsre
        screen.blit(text_surface, (left+top_border, 375+top_border))
        screen.blit(text2_surface, (left+top_border+100, 425+top_border))
        screen.blit(text3_surface, (left+top_border+sub-50, 550+top_border+dub))
        screen.blit(text4_surface, (left+top_border+sub-50, 590+top_border+dub))
          

        # set width of textfield so that text cannot get
        # outside of user's text input
        #input_rect.w = max(10, user_text_surface.get_width()+10)
          
        # display.flip() will update only a portion of the
        # screen to updated, not full area
        pygame.display.flip()
          
        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)

def show_choice():
    global choice_text
    #started = False
    #start_time = time.time()
    #trigger_time = start_time + 15

    #while True:
    screen.fill((0,0,0,0))
    # White Box for Text Entry
    #screen.fill((255,255,255,255),(100+top_border,200+top_border,1200,1200))
    #screen.fill((255,255,255,255),(100+top_border+300,200+top_border,725,725))
    screen.fill((255,255,255,255),(300+top_border,200+top_border,900,900))
     # draw rectangle and argument passed which should

    text_font = pygame.font.Font(None, 60)

    text_surface = text_font.render(choice_text, True, (0, 0, 0))
    # render at position stated in argumentsre
    screen.blit(text_surface, (500+top_border-50, 375+top_border))
      
    pygame.display.flip()

    start_time = time.time()
    trigger_time = start_time + 1
    while True:
        pygame.event.pump() # Keeps from Idle
        time.sleep(0.05) #(20 fps)
        if comms_mode:
                status_found, break_loop = comms_rw("read")
                if break_loop:
                    return True
        pygame.event.pump()
        if time.time() > trigger_time:
            return False

def show_ending():
    global good_ending
    screen.fill((0,0,0,0))
    # Load the video file

    if good_ending:
        clip = VideoFileClip(goodEnding)
    else:
        clip = VideoFileClip(badEnding)
        clip = clip.subclip(1, 10)
    # Chooses one ending or the other depending on choice made

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

        if adminMode:
            # Check for events and exit if the user presses the escape key
            for event in pygame.event.get():
                pygame.event.pump() # Keeps from Idle
                time.sleep(0.05) #(20 fps)
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                # Space for next Screen
                if event.type == KEYDOWN and event.key == K_SPACE:
                    return

def main_loop():
    global status_found
    show_list = [show_record, show_static, show_password_entry, show_break_in, show_maze, show_decision, show_choice, show_ending]
    
    while True:     
        for func in show_list:
            break_flag = func()
            if(break_flag):
                status_found = True
                break

def main():
    main_loop()
    #main_thread = threading.Thread(target=main_loop)
    #main_thread.start()

if __name__ == "__main__":
    main()
