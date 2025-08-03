import os, sys
import gradio as gr
from src.gradio_demo import SadTalker  
from gtts import gTTS
from datetime import datetime
import tempfile

try:
    import webui  # in webui
    in_webui = True
except:
    in_webui = False

def toggle_audio_file(choice):
    if choice == False:
        return gr.update(visible=True), gr.update(visible=False)
    else:
        return gr.update(visible=False), gr.update(visible=True)
    
def ref_video_fn(path_of_ref_video):
    if path_of_ref_video is not None:
        return gr.update(value=True)
    else:
        return gr.update(value=False)

def convert_text_to_audio(text, language='vi'):
    """
    Convert text to audio using gTTS
    Returns the path to the generated audio file and status message
    """
    try:
        if not text or text.strip() == "":
            return None, "Vui lòng nhập nội dung văn bản!", gr.update(visible=False)
        
        # Create a temporary file for the audio
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_path = temp_file.name
        temp_file.close()
        
        # Convert text to speech
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(temp_path)
        
        # Return the audio file path directly for Gradio Audio component
        return temp_path, f"✅ Chuyển đổi thành công! Đã tạo file âm thanh cho văn bản: {text[:50]}{'...' if len(text) > 50 else ''}"
    except Exception as e:
        return None, f"❌ Lỗi khi chuyển đổi: {str(e)}"

def sadtalker_demo(checkpoint_path='checkpoints', config_path='src/config', warpfn=None):

    sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)

    with gr.Blocks(analytics_enabled=False, title="SadTalker") as sadtalker_interface:
        gr.Markdown("<div align='center'> <h2> 😭 SadTalker: Learning Realistic 3D Motion Coefficients for Stylized Audio-Driven Single Image Talking Face Animation (CVPR 2023) </span> </h2> \
                    <a style='font-size:18px;color: #efefef' href='https://arxiv.org/abs/2211.12194'>Arxiv</a> &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
                    <a style='font-size:18px;color: #efefef' href='https://sadtalker.github.io'>Homepage</a>  &nbsp;&nbsp;&nbsp;&nbsp;&nbsp; \
                     <a style='font-size:18px;color: #efefef' href='https://github.com/Winfredy/SadTalker'> Github </div>")
        
        with gr.Row().style(equal_height=False):
            with gr.Column(variant='panel'):
                with gr.Tabs(elem_id="sadtalker_source_image"):
                    with gr.TabItem('Upload image'):
                        with gr.Row():
                            source_image = gr.Image(label="Source image", source="upload", type="filepath", elem_id="img2img_image").style(width=512)

                with gr.Tabs(elem_id="sadtalker_driven_audio"):
                    with gr.TabItem('Upload OR TTS'):
                        with gr.Column(variant='panel'):
                            driven_audio = gr.Audio(label="Input audio", source="upload", type="filepath")

                        if sys.platform != 'win32' and not in_webui: 
                            from src.utils.text2speech import TTSTalker
                            tts_talker = TTSTalker()
                            with gr.Column(variant='panel'):
                                input_text = gr.Textbox(label="Generating audio from text", lines=5, placeholder="please enter some text here, we genreate the audio from text using @Coqui.ai TTS.")
                                tts = gr.Button('Generate audio',elem_id="sadtalker_audio_generate", variant='primary')
                                tts.click(fn=tts_talker.test, inputs=[input_text], outputs=[driven_audio])
                        
                        # Make Audio Section
                        with gr.Column(variant='panel'):
                            gr.Markdown("### 🎵 Make Audio - Chuyển văn bản thành âm thanh")
                            audio_text_input = gr.Textbox(
                                label="Nhập văn bản để chuyển thành âm thanh", 
                                lines=4, 
                                placeholder="Nhập nội dung văn bản tại đây để chuyển thành file âm thanh MP3...",
                                elem_id="audio_text_input"
                            )
                            audio_language = gr.Dropdown(
                                choices=["vi", "en", "zh", "ja", "ko", "fr", "de", "es", "it", "pt"],
                                value="vi",
                                label="Ngôn ngữ",
                                elem_id="audio_language"
                            )
                            convert_audio_btn = gr.Button(
                                '🔄 Chuyển văn bản thành âm thanh', 
                                elem_id="convert_audio_btn", 
                                variant='primary'
                            )
                            audio_status = gr.Textbox(
                                label="Trạng thái", 
                                interactive=False,
                                elem_id="audio_status"
                            )
                            generated_audio = gr.Audio(
                                label="Âm thanh đã tạo", 
                                elem_id="generated_audio"
                            )
                            
            with gr.Column(variant='panel'): 
                with gr.Tabs(elem_id="sadtalker_checkbox"):
                    with gr.TabItem('Settings'):
                        gr.Markdown("need help? please visit our [best practice page](https://github.com/OpenTalker/SadTalker/blob/main/docs/best_practice.md) for more detials")
                        with gr.Column(variant='panel'):
                            pose_style = gr.Slider(minimum=0, maximum=46, step=1, label="Pose style", value=0) # 
                            size_of_image = gr.Radio([256, 512], value=256, label='face model resolution', info="use 256/512 model?") # 
                            preprocess_type = gr.Radio(['crop', 'resize','full', 'extcrop', 'extfull'], value='crop', label='preprocess', info="How to handle input image?")
                            is_still_mode = gr.Checkbox(label="Still Mode (fewer head motion, works with preprocess `full`)")
                            batch_size = gr.Slider(label="batch size in generation", step=1, maximum=10, value=2)
                            enhancer = gr.Checkbox(label="GFPGAN as Face enhancer")
                            submit = gr.Button('Generate', elem_id="sadtalker_generate", variant='primary')
                            
                with gr.Tabs(elem_id="sadtalker_genearted"):
                        gen_video = gr.Video(label="Generated video", format="mp4").style(width=256)
                        status_text = gr.Textbox(label="Status", value="Ready", interactive=False)

        if warpfn:
            submit.click(
                        fn=warpfn(sad_talker.test), 
                        inputs=[source_image,
                                driven_audio,
                                preprocess_type,
                                is_still_mode,
                                enhancer,
                                batch_size,                            
                                size_of_image,
                                pose_style
                                ], 
                        outputs=[gen_video]
                        )
        else:
            submit.click(
                        fn=sad_talker.test, 
                        inputs=[source_image,
                                driven_audio,
                                preprocess_type,
                                is_still_mode,
                                enhancer,
                                batch_size,                            
                                size_of_image,
                                pose_style
                                ], 
                        outputs=[gen_video]
                        )

        # Make Audio event handlers
        convert_audio_btn.click(
            fn=convert_text_to_audio,
            inputs=[audio_text_input, audio_language],
            outputs=[generated_audio, audio_status]
        )

    return sadtalker_interface
 

if __name__ == "__main__":

    demo = sadtalker_demo()
    
    # Không sử dụng queue để tránh lỗi
    # demo.queue()  # Comment out queue
    
    # Launch đơn giản
    demo.launch(
        server_name='127.0.0.1',  # Sử dụng localhost thay vì 0.0.0.0
        server_port=7860,
        show_error=True,
        quiet=False,
        share=False,
        inbrowser=True
    ) 