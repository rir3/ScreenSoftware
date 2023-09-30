from moviepy.editor import VideoFileClip, CompositeVideoClip

# Function to overlay frames
def overlay_frames(main_frame, overlay_frame):
    # You can manipulate the frames here to overlay them as needed
    # In this example, we'll simply overlay one frame on top of the other
    return main_frame.overlay(overlay_frame)


main_video = VideoFileClip("bad_ending.mp4")
overlay_video = VideoFileClip("outpy.avi")

overlay_video = overlay_video.resize(width=750, height=467)

# Resize the overlay video to fit the main video
#overlay_video = overlay_video.resize(height=main_video.h)

# Overlay the videos using the custom function
#final_video = CompositeVideoClip([[main_video, overlay_video.set_position((45,150))]])
final_video = CompositeVideoClip([
                        main_video,
                        overlay_video.set_position((1002,80))
                    ])

# Write the final video to a file
final_video.write_videofile("output_video.mp4", codec="libx264")