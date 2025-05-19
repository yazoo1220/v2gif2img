"""Web interface for video processing using Gradio"""
import os
import gradio as gr
from .video_processor import VideoProcessor

def convert_to_gif(video, start_time, end_time, fps, scale):
    """Convert video to GIF with UI handling"""
    if video is None:
        return None
        
    processor = VideoProcessor()
    try:
        return processor.convert_to_gif(
            video.name,
            start_time=start_time,
            end_time=end_time,
            fps=fps,
            scale=scale
        )
    except (FileNotFoundError, ValueError) as e:
        raise gr.Error(str(e))

def extract_last_frame(video):
    """Extract last frame with UI handling"""
    if video is None:
        return None
        
    processor = VideoProcessor()
    try:
        return processor.extract_last_frame(video.name)
    except FileNotFoundError as e:
        raise gr.Error(str(e))

def extract_frame_at(video, t):
    """Extract frame at specified time with UI handling"""
    if video is None:
        return None
        
    processor = VideoProcessor()
    try:
        return processor.extract_frame_at(video.name, t)
    except FileNotFoundError as e:
        raise gr.Error(str(e))

def update_slider_meta(video):
    """Update time slider based on video duration"""
    if video is None:
        return gr.update(maximum=300, value=0)
        
    clip = VideoFileClip(video.name)
    return gr.update(maximum=clip.duration, value=0)

demo = gr.Blocks()

with demo:
    gr.Markdown("## 動画→GIF & フレーム抽出ツール")
    
    with gr.Tab("GIF変換"):
        with gr.Row():
            vid = gr.Video(label="動画をアップロード (MP4推奨)")
            gif_out = gr.File(label="生成されたGIF")
        with gr.Row():
            st = gr.Number(value=0, label="開始時間 (秒)")
            ed = gr.Number(value=None, label="終了時間 (秒)")
            fps = gr.Slider(
                minimum=1,
                maximum=30,
                value=12,
                step=1,
                label="FPS"
            )
            scale = gr.Slider(
                minimum=0.1,
                maximum=2.0,
                value=1.0,
                step=0.1,
                label="リサイズ倍率"
            )
        gen_btn = gr.Button("GIFを生成")
        gen_btn.click(
            convert_to_gif,
            inputs=[vid, st, ed, fps, scale],
            outputs=gif_out
        )

    with gr.Tab("フレーム抽出"):
        with gr.Row():
            vid2 = gr.Video(label="動画をアップロード")
            frame_img = gr.Image(label="抽出フレーム")
            
        # 最後のフレーム抽出
        last_btn = gr.Button("最後のフレーム抽出")
        last_btn.click(extract_last_frame, inputs=vid2, outputs=frame_img)
        
        gr.Markdown("---")
        
        # 任意フレーム抽出
        time_slider = gr.Slider(
            minimum=0,
            maximum=300,
            value=0,
            step=0.1,
            label="抽出位置 (秒)"
        )
        
        # 動画読み込み時にスライダー更新
        vid2.change(update_slider_meta, inputs=vid2, outputs=time_slider)
        
        # スライダー操作でフレーム更新
        time_slider.change(
            extract_frame_at,
            inputs=[vid2, time_slider],
            outputs=frame_img
        )

if __name__ == "__main__":
    demo.launch()
