import os, sys
import gradio as gr
from src.gradio_demo import SadTalker

# Import các module mới
from home import create_home_tab, custom_home_css
from lecture_input import create_lecture_input_interface
from lecture_output import generate_lecture_video_handler

try:
    import webui  # in webui
    in_webui = True
except:
    in_webui = False

def sadtalker_demo_with_home(checkpoint_path='checkpoints', config_path='src/config', warpfn=None):
    sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)

    with gr.Blocks(analytics_enabled=False, title="SadTalker", css=custom_home_css) as sadtalker_interface:
        with gr.Tabs():
            # --- TAB HOME ---
            with gr.TabItem("🏠 Trang chủ"):
                create_home_tab()
            
            # --- TAB TẠO BÀI GIẢNG ---
            with gr.TabItem("🎓 Tạo Bài Giảng"):
                gr.Markdown("<div align='center'> <h2> 🎓 SadTalker Lecture Video Generator </h2> \
                    <p>Tạo video bài giảng kết hợp slide PowerPoint và video giáo viên giảng bài</p> </div>")

                # Tạo giao diện input
                input_components = create_lecture_input_interface()
                
                # Kết nối với output handler
                input_components['generate_btn'].click(
                    fn=lambda pptx, img, lang, preprocess, still, enh, batch, size, pose: generate_lecture_video_handler(
                        sad_talker, pptx, img, lang, preprocess, still, enh, batch, size, pose
                    ),
                    inputs=[
                        input_components['pptx_file'], 
                        input_components['source_image'], 
                        input_components['audio_language'],
                        input_components['preprocess_type'], 
                        input_components['is_still_mode'], 
                        input_components['enhancer'], 
                        input_components['batch_size'], 
                        input_components['size_of_image'], 
                        input_components['pose_style']
                    ],
                    outputs=[input_components['final_video'], input_components['status']]
                )
    
    return sadtalker_interface

if __name__ == "__main__":
    demo = sadtalker_demo_with_home()
    demo.launch(
        server_name='127.0.0.1',
        server_port=7860,
        show_error=True,
        quiet=False,
        share=False,
        inbrowser=True
    )