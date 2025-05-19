"""Test cases for video processor module"""
import os
import tempfile
from unittest import TestCase
import numpy as np
import pytest
from moviepy.editor import VideoFileClip
from src.video_processor import VideoProcessor

class TestVideoProcessor(TestCase):
    """Test cases for VideoProcessor class"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.processor = VideoProcessor()
        
        # Create a temporary test video file (1 second duration)
        self.temp_dir = tempfile.mkdtemp()
        self.test_video = os.path.join(self.temp_dir, "test_video.mp4")
        
        # Create a simple video clip with colored frames
        frames = []
        for i in range(30):  # 30 frames
            frame = np.zeros((100, 100, 3), dtype=np.uint8)
            frame[:, :, i % 3] = 255  # Create RGB pattern
            frames.append(frame)
            
        clip = VideoFileClip(self.test_video, duration=1)
        clip.write_videofile(self.test_video, fps=30)
        
    def tearDown(self):
        """Clean up test files"""
        for file in ["output.gif", "last_frame.png"]:
            if os.path.exists(file):
                os.remove(file)
        
        # Cleanup test video
        if os.path.exists(self.test_video):
            os.remove(self.test_video)
            
    def test_convert_to_gif_basic(self):
        """Test basic GIF conversion"""
        output = self.processor.convert_to_gif(self.test_video)
        assert os.path.exists(output)
        assert output.endswith(".gif")
        
    def test_convert_to_gif_with_params(self):
        """Test GIF conversion with parameters"""
        output = self.processor.convert_to_gif(
            self.test_video,
            start_time=0.1,
            end_time=0.5,
            fps=15,
            scale=0.5
        )
        assert os.path.exists(output)
        
        # Verify the output GIF properties
        clip = VideoFileClip(output)
        assert abs(clip.duration - 0.4) < 0.1  # About 0.4s (0.5 - 0.1)
        assert clip.size[0] == 50  # Half size (100 * 0.5)
        
    def test_convert_to_gif_invalid_time(self):
        """Test GIF conversion with invalid time parameters"""
        with pytest.raises(ValueError):
            self.processor.convert_to_gif(
                self.test_video,
                start_time=0.5,
                end_time=0.2
            )
            
    def test_convert_to_gif_missing_file(self):
        """Test GIF conversion with non-existent file"""
        with pytest.raises(FileNotFoundError):
            self.processor.convert_to_gif("nonexistent.mp4")
            
    def test_extract_last_frame(self):
        """Test last frame extraction"""
        output = self.processor.extract_last_frame(self.test_video)
        assert os.path.exists(output)
        assert output.endswith(".png")
        
    def test_extract_last_frame_missing_file(self):
        """Test last frame extraction with non-existent file"""
        with pytest.raises(FileNotFoundError):
            self.processor.extract_last_frame("nonexistent.mp4")
            
    def test_extract_frame_at(self):
        """Test frame extraction at specific time"""
        output = self.processor.extract_frame_at(self.test_video, 0.5)
        assert os.path.exists(output)
        assert "frame_" in output
        assert output.endswith(".png")
        
    def test_extract_frame_at_bounds(self):
        """Test frame extraction at boundary times"""
        # Test negative time (should use 0)
        output = self.processor.extract_frame_at(self.test_video, -1)
        assert "frame_00000000.png" in output
        
        # Test time > duration (should use duration)
        output = self.processor.extract_frame_at(self.test_video, 999)
        assert os.path.exists(output)
        
    def test_extract_frame_at_missing_file(self):
        """Test frame extraction with non-existent file"""
        with pytest.raises(FileNotFoundError):
            self.processor.extract_frame_at("nonexistent.mp4", 0)
