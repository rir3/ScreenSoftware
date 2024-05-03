from moviepy.editor import VideoFileClip, ImageClip, CompositeVideoClip

def embed(main_video,logo,output_video):
    # Load the video clip
    video_clip = VideoFileClip(main_video)

    # Load the logo image (adjust dimensions as needed)
    logo = ImageClip(logo).resize(height=300)

    # Set the duration of the logo clip to match the duration of the video clip
    logo = logo.set_duration(video_clip.duration)

    # Add the logo as an overlay on the video
    final_clip = CompositeVideoClip([video_clip, logo.set_position(("right", "bottom"))])

    # Write the final clip to a new file
    final_clip.write_videofile(output_video, codec="libx264", fps=video_clip.fps)