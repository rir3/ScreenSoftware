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
staticVideo = "StaticScreen2.mp4"
loginPassword = "Rebecca"
stealingVideo = "WindowWall.mp4"   #"Stealing.mp4"   -   "outpy.avi"
mazeImage = "Maze.png"
mazeCode = 317208941

#Settings

#Window Wall Settings
scale_factor = .75 #1.75
top_border = 100
left_border = 710

#Macbook Settings
#scale_factor = 1.15
#top_border = 500

########################## STATIC SCREEN ##########################
def showStatic():
    screen.fill((0,0,0,0))
    # Load the video file
    clip = VideoFileClip(staticVideo)

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
            pygame.display.flip()

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
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
      
            if event.type == pygame.KEYDOWN:
                # Check for backspace
                if event.key == pygame.K_BACKSPACE:
                    # get text input from 0 to -1 i.e. end.
                    user_text = user_text[:-1]
                # Space for next Screen
                elif event.type == KEYDOWN and event.key == K_RIGHT:
                    return
                # Unicode standard is used for string
                # formation
                elif user_text.upper() == "REBECCA":
                    return
                elif len(user_text)<10:
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
        screen.blit(text_surface, (575+left_border, 375+top_border))
        screen.blit(text3_surface, (500+left_border, 450+top_border))
        screen.blit(text2_surface,  (400+left_border, input_rect.y+100+top_border))
        screen.blit(user_text_surface, (400+50+left_border, input_rect.y+100+top_border))
          

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

########################## MAZE SCREEN ##########################
def showMaze():
    screen.fill((0,0,0,0))
    while True:
        # get the default size
        x, y = screen.get_size()

        #print(x, y)

        # Set the dimensions of the screen
        screen_size = (x, y)

        # set the pygame window name
        pygame.display.set_caption('image')
         
        # create a surface object, image is drawn on it.
        image = pygame.image.load(mazeImage).convert()
         
        #increase width of image
        # Get the original dimensions of the image
        orig_size = image.get_size()

        # Set the scale factor
        #scale_factor = 1.75

        # Scale the image
        scaled_image = pygame.transform.scale(image, (orig_size[0]*scale_factor, orig_size[1]*scale_factor))

        # Blit the scaled image to the center of the screen
        #screen.blit(scaled_image, (screen_size[0]/2 - scaled_image.get_width()/2, screen_size[1]/2 - scaled_image.get_height()/2))


        # Using blit to copy content from one surface to other
        screen.blit(scaled_image, (left_border, top_border))
         
        # paint screen one time
        pygame.display.flip()

        # Check for events and exit if the user presses the escape key
        for event in pygame.event.get():
            if event.type == KEYDOWN and event.key == K_ESCAPE:
                pygame.quit()
                exit()
            # Space for next Screen
            if event.type == KEYDOWN and event.key == K_SPACE:
                return

########################## Decision SCREEN ##########################
def showDecision():
    run = False
    #while run:
    #    print 

#showStatic()
#showPasswordEntry()
showWindow()
#showMaze()

# Clean up Pygame resources
pygame.quit()
