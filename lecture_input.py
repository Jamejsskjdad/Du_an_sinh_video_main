import os
import gradio as gr
import tempfile
import zipfile
import xml.etree.ElementTree as ET
from gtts import gTTS
from pptx import Presentation
import time

def convert_text_to_audio(text, language='vi'):
    """
    Convert text to audio using gTTS
    Returns the path to the generated audio file
    """
    try:
        if not text or text.strip() == "":
            return None
        
        # Create a temporary file for the audio
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        temp_path = temp_file.name
        temp_file.close()
        
        # Convert text to speech
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(temp_path)
        
        # Return the audio file path directly for Gradio Audio component
        return temp_path
    except Exception as e:
        return None

def read_text_file(file):
    """
    Read text content from uploaded file
    """
    if file is None:
        return "", "❌ Vui lòng chọn file văn bản!"
    
    try:
        # Get file extension
        file_path = file.name
        file_ext = os.path.splitext(file_path)[1].lower()
        
        # Check if it's a supported file type
        if file_ext not in ['.txt', '.md', '.doc', '.docx', '.rtf']:
            return "", "❌ Chỉ hỗ trợ file văn bản (.txt, .md, .doc, .docx, .rtf)"
        
        content = ""
        
        # Handle different file types
        if file_ext == '.docx':
            # For .docx files, we need to extract text properly
            try:
                import zipfile
                import xml.etree.ElementTree as ET
                
                # .docx is a ZIP file containing XML
                with zipfile.ZipFile(file_path, 'r') as zip_file:
                    # Find the document.xml file
                    if 'word/document.xml' in zip_file.namelist():
                        xml_content = zip_file.read('word/document.xml')
                        root = ET.fromstring(xml_content)
                        
                        # Extract text from all text elements
                        text_elements = []
                        for elem in root.iter():
                            if elem.text and elem.text.strip():
                                text_elements.append(elem.text.strip())
                        
                        content = ' '.join(text_elements)
                    else:
                        return "", "❌ Không thể đọc nội dung từ file .docx"
                        
            except Exception as e:
                return "", f"❌ Lỗi đọc file .docx: {str(e)}"
        
        elif file_ext == '.doc':
            # For .doc files, we'll try to read as text but warn user
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                try:
                    with open(file_path, 'r', encoding='latin-1') as f:
                        content = f.read()
                except:
                    return "", "❌ Không thể đọc file .doc. Vui lòng chuyển đổi sang .txt hoặc .docx"
        
        else:
            # For .txt, .md, .rtf files
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
        
        # Clean content - remove null bytes and other control characters
        content = ''.join(char for char in content if ord(char) >= 32 or char in '\n\r\t')
        
        # Strip whitespace and check if empty
        content = content.strip()
        if not content:
            return "", "❌ File văn bản trống hoặc chỉ chứa ký tự đặc biệt!"
        
        return content, f"✅ Đã đọc thành công file: {os.path.basename(file_path)} ({len(content)} ký tự thực tế)"
    
    except Exception as e:
        return "", f"❌ Lỗi đọc file: {str(e)}"

def extract_slides_from_pptx(pptx_file):
    """
    Extract slides as images from PowerPoint file
    Returns list of slide images and their text content
    """
    try:
        slides_data = []
        prs = Presentation(pptx_file.name)
        
        for i, slide in enumerate(prs.slides):
            # Extract text from slide
            slide_text = ""
            for shape in slide.shapes:
                if hasattr(shape, "text"):
                    slide_text += shape.text + " "
            
            # Convert slide to image (simplified approach)
            # In a real implementation, you'd use a library like python-pptx with rendering
            # For now, we'll create a placeholder image with text
            slide_text = slide_text.strip()
            if slide_text:
                slides_data.append({
                    'slide_number': i + 1,
                    'text': slide_text,
                    'image_path': None  # Will be created later
                })
        
        return slides_data
    except Exception as e:
        print(f"Error extracting slides: {str(e)}")
        return []

def extract_lecture_slides(file):
    """Handler function for extracting slides from PowerPoint"""
    if file:
        slides_data = extract_slides_from_pptx(file)
        if slides_data:
            slides_text = []
            for i, slide in enumerate(slides_data):
                slides_text.append(f"Slide {i+1}: {slide['text'][:100]}...")
            return "\n\n".join(slides_text)
    return "❌ Vui lòng chọn file PowerPoint!"

def set_lecture_fast_mode():
    """Set fast mode preset for lecture generation"""
    return 256, 'crop', False, 6, False, 0

def create_lecture_input_interface():
    """Tạo giao diện input cho lecture"""
    
    with gr.Row().style(equal_height=False):
        with gr.Column(variant='panel'):
            # Source image upload
            gr.Markdown("### 👨‍🏫 Ảnh Giáo Viên")
            lecture_source_image = gr.Image(label="Ảnh khuôn mặt giáo viên", source="upload", type="filepath", elem_id="lecture_source_image").style(width=512)
            
            # PowerPoint file upload
            gr.Markdown("### 📊 File PowerPoint Bài Giảng")
            lecture_pptx_file = gr.File(
                label="Chọn file PowerPoint (.pptx)",
                file_types=[".pptx"],
                elem_id="lecture_pptx_file"
            )
            
            # Language selection
            lecture_audio_language = gr.Dropdown(
                choices=["vi", "en", "zh", "ja", "ko", "fr", "de", "es", "it", "pt"],
                value="vi",
                label="Ngôn ngữ giảng bài",
                elem_id="lecture_audio_language"
            )
            
            # Preview extracted slides
            gr.Markdown("### 📝 Nội dung từ PowerPoint")
            lecture_slides_preview = gr.Textbox(
                label="Nội dung đã trích xuất từ các slide",
                lines=8,
                interactive=False,
                elem_id="lecture_slides_preview"
            )
            
            # Extract slides button
            extract_lecture_slides_btn = gr.Button(
                '📂 Trích xuất nội dung từ PowerPoint',
                elem_id="extract_lecture_slides_btn",
                variant='secondary'
            )
            
            # Generate lecture video button
            generate_lecture_btn = gr.Button(
                '🎬 Tạo Video Bài Giảng',
                elem_id="generate_lecture_btn",
                variant='primary'
            )
            
            # Status
            lecture_status = gr.Textbox(
                label="Trạng thái xử lý",
                interactive=False,
                elem_id="lecture_status"
            )
        
        with gr.Column(variant='panel'):
            # Settings
            with gr.Tabs(elem_id="lecture_settings"):
                with gr.TabItem('⚙️ Cài đặt'):
                    gr.Markdown("Cài đặt cho video bài giảng")
                    with gr.Column(variant='panel'):
                        lecture_pose_style = gr.Slider(minimum=0, maximum=46, step=1, label="Pose style", value=0)
                        lecture_size_of_image = gr.Radio([256, 512], value=256, label='Độ phân giải ảnh', info="256 = Nhanh, 512 = Chất lượng cao")
                        lecture_preprocess_type = gr.Radio(['crop', 'resize','full', 'extcrop', 'extfull'], value='crop', label='Xử lý ảnh', info="crop = Nhanh nhất")
                        lecture_is_still_mode = gr.Checkbox(label="Still Mode (ít chuyển động đầu)")
                        lecture_batch_size = gr.Slider(label="Batch size", step=1, maximum=10, value=6, info="Tăng lên 6-8 để nhanh hơn")
                        lecture_enhancer = gr.Checkbox(label="GFPGAN làm Face enhancer (chậm hơn)")
                        
                        # Fast mode preset button
                        lecture_fast_mode_btn = gr.Button(
                            '⚡ Chế độ nhanh (256px, batch=6, không enhancer)',
                            elem_id="lecture_fast_mode_btn",
                            variant='secondary'
                        )
                        
                        lecture_fast_mode_btn.click(
                            fn=set_lecture_fast_mode,
                            outputs=[lecture_size_of_image, lecture_preprocess_type, lecture_is_still_mode, lecture_batch_size, lecture_enhancer, lecture_pose_style]
                        )
            
            # Results placeholder (will be connected to output module)
            with gr.Tabs(elem_id="lecture_results"):
                gr.Markdown("### 🎬 Video Bài Giảng")
                lecture_final_video = gr.Video(label="Video bài giảng hoàn chỉnh", format="mp4").style(width=512)
                
                gr.Markdown("### 📊 Thông tin Video")
                lecture_info = gr.Textbox(
                    label="Thông tin chi tiết",
                    lines=4,
                    interactive=False,
                    elem_id="lecture_info"
                )
    
    # Event handlers
    extract_lecture_slides_btn.click(
        fn=extract_lecture_slides,
        inputs=[lecture_pptx_file],
        outputs=[lecture_slides_preview]
    )
    
    # Return all components for connection with output module
    return {
        'source_image': lecture_source_image,
        'pptx_file': lecture_pptx_file,
        'audio_language': lecture_audio_language,
        'slides_preview': lecture_slides_preview,
        'extract_btn': extract_lecture_slides_btn,
        'generate_btn': generate_lecture_btn,
        'status': lecture_status,
        'pose_style': lecture_pose_style,
        'size_of_image': lecture_size_of_image,
        'preprocess_type': lecture_preprocess_type,
        'is_still_mode': lecture_is_still_mode,
        'batch_size': lecture_batch_size,
        'enhancer': lecture_enhancer,
        'fast_mode_btn': lecture_fast_mode_btn,
        'final_video': lecture_final_video,
        'info': lecture_info
    }
