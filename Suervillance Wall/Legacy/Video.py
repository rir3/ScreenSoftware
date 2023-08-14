from moviepy.editor import VideoFileClip
from moviepy.editor import vfx

class Video:
    def __init__(self, video_path, screen_width, screen_height, speed_factor = 1):
        self.video_clip = VideoFileClip(video_path)
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.fps = self.video_clip.fps
        self.scale()
        self.set_playback_speed(speed_factor)
        self.center()
   
    def set_playback_speed(self, speed_factor = 1):
        # Video Already At Speed 1
        if(speed_factor == 1):
            return self.video_clip
        
        video_clip = self.video_clip
        
        # Calculate the new duration for the double speed video
        new_duration = video_clip.duration / speed_factor

        # Speed up the video clip
        video_clip = video_clip.fx( vfx.speedx, speed_factor)

        # Trim the sped up clip to the new duration
        video_clip = video_clip.subclip(0, new_duration)
    
    def scale(self):
        screen_width = self.screen_width
        screen_height = self.screen_height
        video_clip = self.video_clip

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

    def center(self):
        screen_width = self.screen_width
        screen_height = self.screen_height
        video_clip = self.video_clip

        # Get Video Info
        video_height = video_clip.size[1]
        vide_width = video_clip.size[0]

        #Calculates Top/Left Margin for Video to be Center
        top_margin = int((screen_height - video_height)/2) #int used for not float
        left_margin = int((screen_width - vide_width)/2) #int used for not float

        if(top_margin > 0):
            video_clip = video_clip.margin(top=top_margin)
        if(left_margin > 0):
            video_clip = video_clip.margin(left=left_margin)

    def get_frame(self, time):
        return self.video_clip.get_frame(time)
    
    def close(self):
        # Close the video clip
        self.video_clip.close()