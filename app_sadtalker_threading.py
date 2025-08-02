import os, sys
import gradio as gr
from src.gradio_demo import SadTalker  
import time
import threading
import queue

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

def sadtalker_demo(checkpoint_path='checkpoints', config_path='src/config', warpfn=None):

    sad_talker = SadTalker(checkpoint_path, config_path, lazy_load=True)
    
    # Global variables for threading
    result_queue = queue.Queue()
    status_queue = queue.Queue()

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

        def generate_video_threaded(source_image, driven_audio, preprocess_type, is_still_mode, enhancer, batch_size, size_of_image, pose_style):
            """Function that runs in a separate thread to avoid queue timeout"""
            
            def worker():
                try:
                    # Update status
                    status_queue.put("🔄 Initializing...")
                    time.sleep(1)
                    
                    status_queue.put("👁️ Detecting face landmarks...")
                    time.sleep(1)
                    
                    status_queue.put("📐 Extracting 3DMM coefficients...")
                    time.sleep(1)
                    
                    status_queue.put("🎵 Processing audio features...")
                    time.sleep(1)
                    
                    status_queue.put("🎬 Rendering face animation (this may take 3-5 minutes)...")
                    
                    # Call the actual function
                    result = sad_talker.test(
                        source_image=source_image,
                        driven_audio=driven_audio,
                        preprocess=preprocess_type,
                        still_mode=is_still_mode,
                        use_enhancer=enhancer,
                        batch_size=batch_size,
                        size=size_of_image,
                        pose_style=pose_style
                    )
                    
                    # Put result in queue
                    result_queue.put(("✅ Generation completed successfully!", result))
                    
                except Exception as e:
                    error_msg = f"❌ Error: {str(e)}"
                    print(f"Error in worker thread: {error_msg}")
                    result_queue.put((error_msg, None))
            
            # Start worker thread
            thread = threading.Thread(target=worker)
            thread.daemon = True
            thread.start()
            
            # Return initial status
            return "🔄 Starting generation... Please wait, this may take 3-5 minutes.", None

        def check_status():
            """Check for status updates and results"""
            try:
                # Check for status updates
                while not status_queue.empty():
                    status = status_queue.get_nowait()
                    yield gr.update(value=status), None
                
                # Check for final result
                if not result_queue.empty():
                    status, result = result_queue.get_nowait()
                    yield gr.update(value=status), result
                else:
                    # Continue checking
                    yield gr.update(value="Processing... Please wait."), None
                    
            except Exception as e:
                yield gr.update(value=f"Error checking status: {str(e)}"), None

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
            # Start generation
            submit.click(
                        fn=generate_video_threaded, 
                        inputs=[source_image,
                                driven_audio,
                                preprocess_type,
                                is_still_mode,
                                enhancer,
                                batch_size,                            
                                size_of_image,
                                pose_style
                                ], 
                        outputs=[status_text, gen_video]
                        )
            
            # Check status every 5 seconds
            status_text.change(
                fn=check_status,
                outputs=[status_text, gen_video],
                every=5
            )

    return sadtalker_interface
 

if __name__ == "__main__":

    demo = sadtalker_demo()
    
    # Minimal queue configuration
    demo.queue(
        concurrency_count=1,
        max_size=1
    )
    
    # Launch
    demo.launch(
        server_name='127.0.0.1',  # Sử dụng localhost thay vì 0.0.0.0
        server_port=7860,
        show_error=True,
        quiet=False,
        share=False,
        inbrowser=True
    ) 