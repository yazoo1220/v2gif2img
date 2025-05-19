"""Video processing module for converting video to GIF and extracting frames"""
from moviepy.editor import VideoFileClip
import imageio.v2 as imageio
import os

class VideoProcessor:
    """Class for handling video processing operations"""
    
    def convert_to_gif(self, video_path, start_time=0, end_time=None, fps=12, scale=1.0):
        """Convert video to GIF with specified parameters
        
        Args:
            video_path (str): Path to input video file
            start_time (float): Start time in seconds
            end_time (float): End time in seconds
            fps (int): Frames per second for output GIF
            scale (float): Scale factor for output GIF
            
        Returns:
            str: Path to output GIF file
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        output_path = "output.gif"
        clip = VideoFileClip(video_path)
        
        # Handle end time
        if end_time is None or end_time > clip.duration:
            end_time = clip.duration
            
        # Validate time range
        if start_time < 0:
            start_time = 0
        if start_time >= end_time:
            raise ValueError("Start time must be less than end time")
            
        # Process video
        clip = clip.subclip(start_time, end_time)
        if scale != 1.0:
            clip = clip.resize(scale)
            
        clip.write_gif(output_path, fps=fps)
        return output_path
        
    def extract_last_frame(self, video_path):
        """Extract the last frame from a video
        
        Args:
            video_path (str): Path to input video file
            
        Returns:
            str: Path to output image file
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        clip = VideoFileClip(video_path)
        frame = clip.get_frame(clip.duration)
        
        output_path = "last_frame.png"
        imageio.imwrite(output_path, frame)
        return output_path
        
    def extract_frame_at(self, video_path, time):
        """Extract a frame at specified time
        
        Args:
            video_path (str): Path to input video file
            time (float): Time in seconds
            
        Returns:
            str: Path to output image file
        """
        if not os.path.exists(video_path):
            raise FileNotFoundError(f"Video file not found: {video_path}")
            
        clip = VideoFileClip(video_path)
        
        # Validate time
        if time < 0:
            time = 0
        if time > clip.duration:
            time = clip.duration
            
        frame = clip.get_frame(time)
        output_path = f"frame_{int(time*1000):08d}.png"
        imageio.imwrite(output_path, frame)
        return output_path
