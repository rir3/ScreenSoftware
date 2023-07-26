import sys
from moviepy.editor import VideoFileClip
import pygame
from pygame.locals import *
import time
import serial #pyserial
import RecordWebCam
import COGS_Communication
import threading
from queue import Queue


#Settings
recording = True
macBook = False #Enables screen settings for macBook pro 15
adminMode = False #Allows you to skip screens and view mouse
serialMode = True #Disables/Enables Serial Mode need arduino connected if enabled
comms_mode = True #Disables/Enables Communication Mode for COGS Communication (Arduino)
pygame.display.set_caption('SA-Wall')#Window Name

#Resources
arduinoPort = '/dev/tty.usbmodem14201'
staticVideo = "StaticScreen.mp4"
loginPassword = "Rebecca"
breakInVideo = "WebCamVideo.avi"#Must have end with .avi extension
#breakInVideo = "Stealing.mp4"
mazeImage = "Maze.png"
mazeCode = "317208941"

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
    pygame.mouse.set_visible(False)
    print("Admin Mode: OFF")
else:
    print("Admin Mode: ON")
    mazeCode = "111111111"
    #staticVideo = "StaticScreen4k.mp4"

#Enable Serial Comms with Arduino
if serialMode:
    #ser = serial.Serial(arduinoPort, 9600)  # open serial port, change the port name as per your system
    print("Serial Mode: ON")
else:
    print("Serial Mode: OFF")

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

############ Legacy Code ############
def serialWrite(action, status):
    ser = serial.Serial(arduinoPort, 9600)
    while True:
        #pygame.event.pump()
        #print("donkey")
        foundStatus = COGS_Communication.write(arduinoPort, action, status, ser)
        #print(foundStatus)
        if foundStatus:
            print("Found: " + status)
            break
    ser.close() 

def serialRead(status):
    ser = serial.Serial(arduinoPort, 9600)
    while True:
        #pygame.event.pump()
        #print("donkey")
        foundStatus = COGS_Communication.read(arduinoPort, status, ser)
        #print(foundStatus)
        if foundStatus:
            print("Found: " + status)
            break
    ser.close()
############/ Legacy Code ############

def comms_start():
    global comms_started
    comms_started = True
    COGS_Communication.comms_helper(tasks, statuses)

def comms_rw(action, status):
    if(not comms_started):
        comms_start()
    elif(action == "write"):
        tasks.put(status)
    elif(action == "read"):
        while not statuses.empty():
            if(statuses.get() == status):
                return True #Found status
        return False

def record():
    #Records Video from WebCam
    if comms_mode:
        while True:
            status_found = comms_rw("read", "Game Started")
            pygame.event.pump()

            if status_found:
                RecordWebCam.record(breakInVideo)
                return
    else:
        RecordWebCam.record(breakInVideo)

########################## BLANK SCREEN ##########################
def showBlank():
    screen.fill((0,0,0,0))     
    pygame.display.flip()
########################## STATIC SCREEN ##########################
def showStatic(): 
    screen.fill((0,0,0,0))
    # Load the video file
    clip = VideoFileClip(staticVideo)
    #clip = clip.subclip(1, 9)
    
    #print("Here:1")

    if serialMode:
        serialThread = threading.Thread(target=serialRead, args=("Show Login",))
        serialThread.start()
    #print("Here:2")
    while True:
        #pygame.event.pump()
        #print("Here:3")
        # Iterate over each frame of the video and display it in the Pygame window
        for frame in clip.iter_frames(fps=clip.fps):
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

            if serialMode:
                if not serialThread.is_alive():
                    return

            if adminMode:
                # Check for events and exit if the user presses the escape key
                for event in pygame.event.get():
                    if event.type == KEYDOWN and event.key == K_ESCAPE:
                        pygame.quit()
                        exit()
                    # Space for next Screen
                    if event.type == KEYDOWN and event.key == K_SPACE:
                        return

########################## PASSWORD ENTRY SCREEN ##########################
def showPasswordEntry():
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
        for event in pygame.event.get():
      
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
                        return
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
def showBreakIn():
    screen.fill((0,0,0,0))
    # Load the video file
    clip = VideoFileClip(breakInVideo)
    #clip = clip.subclip(0, 14)#starts at \ sec end \ sec

    # Iterate over each frame of the video and display it in the Pygame window
    for frame in clip.iter_frames(fps=clip.fps):
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

        if adminMode:
            # Check for events and exit if the user presses the escape key
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                # Space for next Screen
                if event.type == KEYDOWN and event.key == K_SPACE:
                    return

########################## MAZE SCREEN ##########################
def showMaze():
    screen.fill((0,0,0,0))
    while True:
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


        if adminMode:
            # Check for events and exit if the user presses the escape key
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_ESCAPE:
                    pygame.quit()
                    exit()
                # Space for next Screen
                if event.type == KEYDOWN and event.key == K_SPACE:
                    return
                if event.type == KEYDOWN and event.key == K_RIGHT:
                    showMazePasswordEntry()
                    return
        else:
            # Check for events and exit if the user presses the escape key
            for event in pygame.event.get():
                if event.type == KEYDOWN and event.key == K_RIGHT:
                        showMazePasswordEntry()
                        return
########################## Maze PASSWORD ENTRY SCREEN ##########################
def showMazePasswordEntry():
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
        for event in pygame.event.get():
      
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
                    showMaze()
                    return
                elif event.key == K_RETURN:
                    if user_text == mazeCode:
                        if serialMode:
                            #COGS_Communication.write(arduinoPort, "3", "Maze Solved")
                            serialThread = threading.Thread(target=serialWrite, args=("3", "Maze Solved",))#fixxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
                            serialThread.start()
                            #time.sleep(1)
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
def showDecision():
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
        for event in pygame.event.get():
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
                    if serialMode:
                            time.sleep(4)
                            #COGS_Communication.write(arduinoPort, "5", "Bad Ending")
                            serialThread = threading.Thread(target=serialWrite, args=("5", "Bad Ending",))
                            serialThread.start()
                    return "SECURITY DOOR OVERIDDEN"
                    #showChoice("VIDEO DELETED!")
                    #return
                # Leave Video
                elif event.key == K_RETURN:
                    if serialMode:
                            time.sleep(4)
                            #COGS_Communication.write(arduinoPort, "4", "Good Ending")
                            serialThread = threading.Thread(target=serialWrite, args=("4", "Good Ending",))
                            serialThread.start()
                    return "DIAMOND THEFT REPORTED"
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

def showChoice(text):
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

    text_surface = text_font.render(text, True, (0, 0, 0))
    # render at position stated in argumentsre
    screen.blit(text_surface, (500+top_border-50, 375+top_border))
      
    pygame.display.flip()

    #pygame.time.wait(15000)
    #return
    #if not started:
    #    start_time = time.time()
    #    trigger_time = start_time + 15
    #    started = True
    start_time = time.time()
    trigger_time = start_time + 15
    while True:
        pygame.event.pump()
        if time.time() > trigger_time:
            return


while True:
    showBlank()#<--Start
    record()
    showStatic()
    showPasswordEntry()
    showBreakIn()
    showMaze()
    choice = showDecision()
    showChoice(choice)#<--End


#sys.exit()
# Clean up Pygame resources
#pygame.quit()
