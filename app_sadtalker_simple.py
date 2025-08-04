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

# CSS nhẹ chỉ cho home (card bo góc, shadow, xanh nhạt)
custom_home_css = """
.sad-home-cards-row {
    display: flex; gap: 52px; justify-content: center; margin: 52px 0 36px 0;
}
.sad-home-card {
    background: #f5f9ff;
    border-radius: 30px;
    box-shadow: 0 12px 40px rgba(50,130,255,0.16), 0 2px 10px rgba(180,192,240,0.13);
    padding: 44px 54px;
    min-width: 350px; max-width: 540px; width: 100%;
    border: 2.8px solid #b1d1ff;
    transition: box-shadow 0.2s, border 0.2s;
}
.sad-home-card:hover {
    box-shadow: 0 16px 60px rgba(44, 110, 255,0.22), 0 4px 16px rgba(60,110,255,0.17);
    border: 2.8px solid #347cff;
}
.sad-home-card h3 {
    color: #1460a5;
    font-size: 2rem;
    font-weight: 900;
    margin-bottom: 24px;
    display: flex; align-items: center; gap: 13px;
    letter-spacing: 0.5px;
    text-shadow: 0 2px 8px #e0edfa;
}
.sad-home-card ul, .sad-home-card ol {
    font-size: 1.19rem;
    color: #000;
    font-weight: 600;
    margin-left: 12px; margin-top: 3px; line-height: 1.85;
    letter-spacing: 0.2px;
}
.sad-home-card li {
margin-bottom: 10px;
list-style:none;
}
.sad-home-btn-wrap {display: flex; justify-content: center; margin: 18px 0 6px 0;}
.sad-home-btn {
    background: linear-gradient(90deg, #468fff, #54b1ff 80%);
    color: #fff; border: none; border-radius: 16px; font-size: 1.18rem;
    padding: 18px 50px; font-weight: bold; letter-spacing: 1px;
    box-shadow: 0 6px 18px rgba(48,124,247,0.12);
    cursor: pointer; transition: background .13s, transform .12s;
}
.sad-home-btn:hover {
    background: linear-gradient(90deg, #357aff, #468fff 80%);
    transform: translateY(-2px) scale(1.04);
}
.sad-home-title {
    text-align: center; color: #2165c3; font-size: 2.5rem;
    font-weight: bold; margin-top: 38px; margin-bottom: 12px; letter-spacing: 1.1px;
}
.sad-home-desc {text-align: center; color: #222; font-size: 1.23rem; opacity: 0.92;}
@media (max-width: 1100px){
    .sad-home-cards-row { flex-direction: column; align-items: center; gap: 26px;}
    .sad-home-card { min-width: 200px; max-width: 99vw;}
}
"""


def sadtalker_demo_with_home(checkpoint_path='checkpoints', config_path='src/config', warpfn=None):
    sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)

    with gr.Blocks(analytics_enabled=False, title="SadTalker", css=custom_home_css) as sadtalker_interface:
        with gr.Tabs():
            # --- TAB HOME ---
            with gr.TabItem("🏠 Trang chủ"):
                gr.HTML("""
                <div class="sad-home-title"><span style="font-size:2.2rem;">🎭</span> SadTalker</div>
                <div class="sad-home-desc">Tạo video nói chuyện từ ảnh tĩnh và âm thanh với AI<br>
                    <span style="font-size:0.98rem;">Chào mừng bạn đến với SadTalker - Công cụ tạo video nói chuyện thông minh dựa trên nghiên cứu CVPR 2023</span>
                </div>
                <div class="sad-home-cards-row">
                    <div class="sad-home-card">
                        <h3 style="color: #000 !important;">🚀 Tính năng nổi bật</h3>
                        <ul style="color: #000 !important; font-size: 1.19rem; font-weight: 600; margin-left: 12px; margin-top: 3px; line-height: 1.85; letter-spacing: 0.2px;">
                            <li style="color: #000 !important; margin-bottom: 10px;">✨ Tạo video nói chuyện từ ảnh tĩnh</li>
                            <li style="color: #000 !important; margin-bottom: 10px;">🎵 Hỗ trợ âm thanh từ file hoặc văn bản</li>
                            <li style="color: #000 !important; margin-bottom: 10px;">🎨 Nhiều tùy chọn xử lý ảnh</li>
                            <li style="color: #000 !important; margin-bottom: 10px;">⚡ Tốc độ xử lý nhanh</li>
                            <li style="color: #000 !important; margin-bottom: 10px;">🤖 Hiệu ứng chuyển động tự nhiên</li>
                        </ul>
                    </div>
                    <div class="sad-home-card">
                        <h3 style="color: #000 !important;">💡 Hướng dẫn sử dụng</h3>
                        <ul style="color: #000 !important; font-size: 1.19rem; font-weight: 600; margin-left: 12px; margin-top: 3px; line-height: 1.85; letter-spacing: 0.2px;">
                            <li style="color: #000 !important; margin-bottom: 10px;">📸 Tải lên ảnh khuôn mặt</li>
                            <li style="color: #000 !important; margin-bottom: 10px;">🎤 Chọn file âm thanh hoặc nhập văn bản</li>
                            <li style="color: #000 !important; margin-bottom: 10px;">⚙️ Điều chỉnh các thông số</li>
                            <li style="color: #000 !important; margin-bottom: 10px;">🎬 Nhấn "Sinh Video" để tạo</li>
                            <li style="color: #000 !important; margin-bottom: 10px;">💾 Tải xuống kết quả</li>
                        </ul>
                    </div>
                </div>
                <div class="sad-home-btn-wrap">
                    <button class="sad-home-btn" onclick="document.querySelectorAll('.tabitem')[1].click();">🎬 Chuyển đến giao diện Sinh Video</button>
                </div>
                """)
            
            # --- TAB SINH VIDEO (nguyên gốc từ code bạn gửi) ---
            with gr.TabItem("🎬 Sinh Video"):
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
                        inputs=[source_image, driven_audio, preprocess_type, is_still_mode, enhancer, batch_size, size_of_image, pose_style], 
                        outputs=[gen_video]
                    )
                else:
                    submit.click(
                        fn=sad_talker.test, 
                        inputs=[source_image, driven_audio, preprocess_type, is_still_mode, enhancer, batch_size, size_of_image, pose_style], 
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
    demo = sadtalker_demo_with_home()
    demo.launch(
        server_name='127.0.0.1',
        server_port=7860,
        show_error=True,
        quiet=False,
        share=False,
        inbrowser=True
    )