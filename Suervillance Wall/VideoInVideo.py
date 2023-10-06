from moviepy.editor import VideoFileClip, CompositeVideoClip

# Function to overlay frames
def overlay_video(main_video, overlay_video, output_video="output_video.mp4"):
    main_clip = VideoFileClip(main_video)
    overlay_clip = VideoFileClip(overlay_video)

    overlay_clip = overlay_clip.resize(width=750, height=467)
    overlay_clip = overlay_clip.subclip(0, 33)
    overlay_clip = overlay_clip.set_start(13)
    
    final_video = CompositeVideoClip([
                            main_clip,
                            overlay_clip.set_position((1002,80))
                        ])

    # Write the final video to a file
    final_video.write_videofile(output_video, codec="libx264")

def main():
    overlay_video("good_ending.mp4", "WebCamVideo.avi")

if __name__ == "__main__":
    main()