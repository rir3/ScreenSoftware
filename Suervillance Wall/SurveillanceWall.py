import sys
from moviepy.editor import VideoFileClip
import pygame
from pygame.locals import *
import time
import RecordWebCam
import COGS_Communication
import threading
from queue import Queue
import platform
import VideoPlayer
import VideoInVideo
import LoggingConfig
import HttpServer
import os
import add_logo
from datetime import datetime

#Settings
recording = True
comms_mode = True #Disables/Enables Communication Mode for COGS Communication
adminMode = False #Allows you to skip screens and view mouse
macBook = False #Enables screen settings for macBook pro 15
infinite_main_loop = False #breaks infinite main loop
arduino_enabled = True

#Mac Devs Change Settings here
if(platform.system() == "Darwin"): #For Mac
    macBook = True 
    adminMode = True
    comms_mode = True
    recording = False #(Needs Camera)
    infinite_main_loop = True
    arduino_enabled = False #(Needs Arduino)

pygame.display.set_caption('SA-Wall')#Window Name

# Use the logger defined in the logging settings module
logger = LoggingConfig.logger

#Resources
media_directory = "Media/"
endings_directory = media_directory + "Endings/" 
edited_directory = media_directory + "Editied_Endings/"
arduinoPort = '/dev/tty.usbmodem14201'
staticVideo = media_directory + "StaticScreen.mp4"
loginPassword = "Rebecca"
breakInVideo = media_directory + "WebCamVideo.avi"#Must have end with .avi extension
mazeImage = media_directory + "Maze.png"
decisionImage = media_directory + "sel.jpg"
mazeCode = "317208941"
choice_text = ""
status_found = False
goodEnding = endings_directory + "good_ending.mp4"
goodEndingAudio = endings_directory + "good_ending.mp3"
goodEndingEdited = edited_directory + "good_ending_edited.mp4"
badEnding = endings_directory + "bad_ending.mp4"
badEndingAudio = endings_directory + "bad_ending.mp3"
badEndingEdited = edited_directory + "bad_ending_edited.mp4"
logo = media_directory + "Logo/logo_w.png"
good_ending = False
folder = ""
folder_path = 'Robbin_Videos/'

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
    global httpd
    comms_started = True
    httpd = HttpServer.start_helper(statuses)

    if(arduino_enabled):
        COGS_Communication.comms_helper(tasks, statuses)
    
def destroy():
    httpd.shutdown()
    httpd.server_close()
    time.sleep(1)
    pygame.quit()
    sys.exit(1)
    #os._exit(1)
    

def comms_rw(action, status="N/A"):
    global status_found
    global skip
    
    start_status = "Game Started"
    reset_status = "Show_Reset"
    skip_status = "Show_Next"
    quit_status = "Quit"
    if(not comms_started):
        comms_start()
    elif(action == "write"):
        tasks.put(status)
    elif(action == "read"):
        while not statuses.empty():
            s = statuses.get()
            if(s == start_status):
                status_found = True
                return True, True
            elif(s == quit_status):
                destroy()
            elif(s == reset_status):
                status_found = False
                return False, True
            elif(s == skip_status):
                skip = True
                return True, False #Skip to show next screen
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

def logo_overlay(input_video,logo, output_video):
    add_logo.embed(input_video,logo, output_video)

def logo_overlay_helper(input_video,logo, output_video):
    video_edit_thread = threading.Thread(target=logo_overlay, args=(input_video, logo, output_video))
    video_edit_thread.start()
    return video_edit_thread

def video_edit(main_video, overlay_video, output_video):
    VideoInVideo.overlay_video(main_video, overlay_video, output_video)

def video_edit_helper(main_video, overlay_video, output_video):
    video_edit_thread = threading.Thread(target=video_edit, args=(main_video, overlay_video, output_video))
    video_edit_thread.start()
    return video_edit_thread

def make_folder():
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    folder = folder_path + timestamp
    os.makedirs(folder)

    return folder

def show_video_edit():
    logger.info("Reached: show_video_edit()")

    if not recording:
        return False
    #Shows Recording Modal
    screen.fill((255,255,255,255),(300+top_border,200+top_border,900,900))#White Box
    text_font = pygame.font.Font(None, 50)#Font 50 Size
    text_surface = text_font.render('VIDEO EDITING IN PROGRESS!', True, (0, 0, 0))#Text Black Font
    screen.blit(text_surface, (500+top_border, 375+top_border))
    pygame.display.flip()

    
    folder = make_folder()+"/"
    print(folder)
    vid1_thread = video_edit_helper(goodEnding, breakInVideo, goodEndingEdited)
    vid2_thread = video_edit_helper(badEnding, breakInVideo, badEndingEdited)

    while vid1_thread.is_alive() or vid2_thread.is_alive():
        delay(1)
        
    vid3_thread = logo_overlay_helper(breakInVideo, logo, folder+"break_in.mp4")
    vid4_thread = logo_overlay_helper(goodEndingEdited, logo, folder+"good_ending.mp4")
    vid5_thread = logo_overlay_helper(badEndingEdited, logo, folder+"bad_ending.mp4")

    while vid3_thread.is_alive() or vid4_thread.is_alive() or vid5_thread.is_alive():
        delay(1)

def record():
    RecordWebCam.record(breakInVideo)

def record_helper():
    global status_found
    status_found = False

    #Shows Recording Modal
    screen.fill((255,255,255,255),(300+top_border,200+top_border,900,900))#White Box
    text_font = pygame.font.Font(None, 50)#Font 50 Size
    text_surface = text_font.render('RECORDING IN PROGRESS!', True, (0, 0, 0))#Text Black Font
    screen.blit(text_surface, (500+top_border, 375+top_border))
    pygame.display.flip()

    record_thread = threading.Thread(target=record)
    record_thread.start()
    
    while record_thread.is_alive():
        delay(1)# Add Code to wait for thread to finish before continueing

########################## RECORD SCREEN ##########################
def show_record():
    logger.info("Reached: show_record()")
    global status_found
    global skip
    skip = False
    screen.fill((0,0,0,0))     
    pygame.display.flip()
    #Records Video from WebCam
    if not recording:
        return False
    elif arduino_enabled:
        while True:
            pygame.event.pump() # Keeps from Idle
            time.sleep(0.05) #(20 fps)
            status_found, break_loop = comms_rw("read", "Game Started")
            if skip:
                    skip = False
                    return False
            elif status_found:
                record_helper()
                show_video_edit()
                return False
    elif status_found:
        record_helper()
        show_video_edit()
        return False
    else:
        record_helper()
        show_video_edit()
        
########################## STATIC SCREEN ##########################
def show_static():
    logger.info("Reached: show_static()")
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

def reset_password_entry():
    text_font = pygame.font.Font(None, 100)

    # White Box for Text Entry
    screen.fill((255,255,255,255),(300+top_border,200+top_border,900,900))
    
    text2_surface = text_font.render('_________________', True, (0, 0, 0))
    text_surface = text_font.render('ENTER', True, (0, 0, 0))
    text3_surface = text_font.render('PASSWORD:', True, (0, 0, 0))

    screen.blit(text_surface, (575+top_border, 375+top_border))
    screen.blit(text3_surface, (500+top_border, 450+top_border))
    screen.blit(text2_surface,  (400+top_border, 618+100+top_border))

########################## PASSWORD ENTRY SCREEN ##########################
def show_password_entry():
    logger.info("Reached: show_password_entry()")
    screen.fill((0,0,0,0))

    clock = pygame.time.Clock()

    user_text = ''
    text_font = pygame.font.Font(None, 100)

    # Aqua Background
    screen.fill((35,250,247,255))

    reset_password_entry()

    while True:
        pygame.event.pump() # Keeps from Idle
        time.sleep(0.05) #(20 fps)
        for event in pygame.event.get():
            pygame.event.pump() # Keeps from Idle
            #time.sleep(0.05) #(20 fps)
      
          # if user types QUIT then the screen will close
            if event.type == pygame.QUIT and adminMode:
                pygame.quit()
                sys.exit()
                    
            if event.type == pygame.KEYDOWN:
                logger.info("KeyDown")
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    logger.info("Backspace: " + user_text)
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                    reset_password_entry()
                # Right Arrow for next Screen
                elif event.key == K_RIGHT and adminMode:
                    return
                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                    logger.info("Password Input Attempt: " + user_text)
                    if user_text.upper() == loginPassword.upper():
                        logger.info("Password Passed: " + user_text)
                        return False
                    elif user_text.upper() != loginPassword.upper():
                        logger.info("Password Failed:" + user_text)
                        user_text = ""
                        text_font_red = pygame.font.Font(None, 50)
                        text_surface_red = text_font_red.render("WRONG PASSWORD! Hint Favorite Book!", True, (255, 0, 0))
                        screen.blit(text_surface_red, (425+top_border, 525+top_border))
                        pygame.display.flip()
                        time.sleep(1)
                        reset_password_entry()

                elif len(user_text)<7:
                    logger.info("Single Key:" + event.unicode)
                    user_text += event.unicode
                    user_text = user_text.upper()

        if comms_mode:
                status_found, break_loop = comms_rw("read")
                if break_loop:
                    return True
                if status_found:
                    return False

        user_text_surface = text_font.render(user_text, True, (0, 0, 0))
        screen.blit(user_text_surface, (400+50+top_border, 618+100+top_border))
          

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
    logger.info("Reached: show_break_in()")

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
                if status_found:
                    return False

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
    logger.info("Reached: show_maze()")

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
                if status_found:
                    return False
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
    logger.info("Reached: show_maze_password_entry()")

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
                if status_found:
                    return False
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
                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                    if user_text == mazeCode:
                        if comms_mode:
                            comms_rw("write", "Maze Solved")
                        #showDecision()
                        return
                    elif user_text != mazeCode:
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
    logger.info("Reached: show_decision()")

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

    screen.fill((0,0,0,0))
    scale_factor_diff = .65
    image = pygame.image.load(decisionImage).convert()
    orig_size = image.get_size()
    scaled_image = pygame.transform.scale(image, (orig_size[0]*scale_factor*scale_factor_diff, orig_size[1]*scale_factor*scale_factor_diff))
    screen.blit(scaled_image, (0, top_border))

    while True:
        pygame.event.pump() # Keeps from Idle
        time.sleep(0.05) #(20 fps)
        if comms_mode:
                status_found, break_loop = comms_rw("read")
                if break_loop:
                    return True
                if status_found:
                    return False
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
                    choice_text = "DIAMOND THEFT REPORTED"
                    good_ending = True
                    return False
                    #showChoice("VIDEO DELETED!")
                    #return
                # Leave Video
                elif event.key == K_RETURN or event.key == K_KP_ENTER:
                    if comms_mode:
                            comms_rw("write", "Good Ending")
                    choice_text = "SECURITY DOOR OVERIDDEN"
                    good_ending = False
                    return False
                    #showChoice("VIDEO NOT DELETED")
                    #return
        '''
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
        '''
        pygame.display.flip()
          
        # clock.tick(60) means that for every second at most
        # 60 frames should be passed.
        clock.tick(60)

def show_choice():
    logger.info("Reached: show_choice()")

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
                if status_found:
                    return False
        pygame.event.pump()
        if time.time() > trigger_time:
            return False

def show_ending():
    logger.info("Reached: show_ending()")

    global good_ending
    screen.fill((0,0,0,0))
    # Load the video file

    if good_ending:
        VideoPlayer.play_video(goodEndingEdited,goodEndingAudio,screen)
    else:
        VideoPlayer.play_video(badEndingEdited,badEndingAudio,screen)

def main_loop():
    logger.info("main_loop - started")
    show_list = [show_record, show_static, show_password_entry, show_break_in, show_maze, show_decision, show_choice, show_ending]
    
    running = True
    while running:     
        for func in show_list:
            break_flag = func()
            if(break_flag):
                break
        if infinite_main_loop:
           running = False

def main():
    main_loop()

if __name__ == "__main__":
    main()
