import os
import gradio as gr
import tempfile
import time
import shutil
from datetime import datetime
from moviepy.editor import VideoFileClip, concatenate_videoclips, CompositeVideoClip, TextClip, ImageClip, AudioFileClip
from PIL import Image, ImageDraw, ImageFont
from lecture_input import convert_text_to_audio, extract_slides_from_pptx

def get_audio_duration(audio_path):
    """
    Get duration of audio file in seconds
    """
    try:
        if audio_path and os.path.exists(audio_path):
            # Use AudioFileClip instead of VideoFileClip for audio files
            audio_clip = AudioFileClip(audio_path)
            duration = audio_clip.duration
            audio_clip.close()
            return duration
        return 0
    except Exception as e:
        print(f"Error getting audio duration: {str(e)}")
        return 0

def create_slide_image_with_text(text, output_path, width=1920, height=1080):
    """
    Create a slide image with text (placeholder for actual slide rendering)
    """
    try:
        # Create a white background image
        img = Image.new('RGB', (width, height), color='white')
        
        # For now, we'll create a simple text image
        # In a real implementation, you'd render the actual PowerPoint slide
        draw = ImageDraw.Draw(img)
        
        # Try to use a default font, fallback to basic if not available
        try:
            font = ImageFont.truetype("arial.ttf", 40)
        except:
            font = ImageFont.load_default()
        
        # Draw text in the center
        text_lines = text.split('\n')
        y_position = height // 2 - (len(text_lines) * 50) // 2
        
        for line in text_lines:
            # Get text size
            bbox = draw.textbbox((0, 0), line, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            # Calculate position to center text
            x_position = (width - text_width) // 2
            
            # Draw text
            draw.text((x_position, y_position), line, fill='black', font=font)
            y_position += text_height + 20
        
        # Save image
        img.save(output_path)
        return output_path
    except Exception as e:
        print(f"Error creating slide image: {str(e)}")
        return None

def generate_video_for_text(sad_talker, source_image, text, language, preprocess_type, is_still_mode, enhancer, batch_size, size_of_image, pose_style):
    """
    Generate video for a single text using SadTalker
    """
    try:
        # Verify source image exists
        if not source_image or not os.path.exists(source_image):
            print(f"Source image not found: {source_image}")
            return None
        
        # Convert text to audio
        audio_path = convert_text_to_audio(text, language)
        if not audio_path:
            print("Failed to convert text to audio")
            return None
        
        print(f"Generating video with image: {source_image}")
        print(f"Image exists: {os.path.exists(source_image)}")
        print(f"Audio path: {audio_path}")
        
        # Generate video using the same method as the main interface
        video_path = sad_talker.test(
            source_image, audio_path, preprocess_type, is_still_mode, 
            enhancer, batch_size, size_of_image, pose_style
        )
        
        # Clean up temporary audio file
        if os.path.exists(audio_path):
            os.remove(audio_path)
        
        if video_path and os.path.exists(video_path):
            print(f"✅ Video generated successfully: {video_path}")
            return video_path
        else:
            print(f"❌ Video generation failed or file not found: {video_path}")
            return None
            
    except Exception as e:
        print(f"Error generating video for text: {str(e)}")
        return None

def create_lecture_video(sad_talker, slides_data, source_image, language, preprocess_type, is_still_mode, enhancer, batch_size, size_of_image, pose_style):
    """
    Create a lecture video combining slides and teacher video
    """
    try:
        if not slides_data:
            return None, "❌ Không có slide nào để xử lý!"
        
        # Create output directory
        output_dir = os.path.join("results", f"lecture_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        os.makedirs(output_dir, exist_ok=True)
        
        print(f"Creating lecture video in: {output_dir}")
        
        # Copy source image to safe location
        safe_image_path = os.path.join(output_dir, "source_image.png")
        if not source_image or not os.path.exists(source_image):
            return None, "❌ Không tìm thấy ảnh nguồn!"
        
        shutil.copy2(source_image, safe_image_path)
        print(f"✅ Source image copied to safe location: {safe_image_path}")
        
        # Process each slide
        slide_clips = []
        total_duration = 0
        temp_video_files = []  # Track temporary video files for cleanup
        
        for i, slide_data in enumerate(slides_data):
            print(f"\n--- Processing slide {i+1}/{len(slides_data)} ---")
            
            # Verify source image exists before each slide processing
            if not os.path.exists(safe_image_path):
                print(f"⚠️ Source image lost, copying again...")
                if os.path.exists(source_image):
                    shutil.copy2(source_image, safe_image_path)
                    print(f"✅ Source image re-copied")
                else:
                    print(f"❌ Original source image also lost, stopping process")
                    break
            
            # Create slide image
            slide_image_path = os.path.join(output_dir, f"slide_{i+1:02d}.png")
            slide_image = create_slide_image_with_text(slide_data['text'], slide_image_path)
            
            if not slide_image:
                print(f"❌ Failed to create slide image for slide {i+1}")
                continue
            
            # Generate audio for slide text
            audio_path = convert_text_to_audio(slide_data['text'], language)
            if not audio_path:
                print(f"❌ Failed to generate audio for slide {i+1}")
                continue
            
            # Get audio duration
            audio_duration = get_audio_duration(audio_path)
            print(f"Audio duration for slide {i+1}: {audio_duration:.2f} seconds")
            
            # If audio duration is 0 or very short, set a minimum duration
            if audio_duration <= 0.1:
                audio_duration = 3.0  # Minimum 3 seconds per slide
                print(f"⚠️ Audio duration too short, setting to minimum: {audio_duration}s")
            
            # Generate teacher video
            teacher_video_path = generate_video_for_text(
                sad_talker, safe_image_path, slide_data['text'], language, 
                preprocess_type, is_still_mode, enhancer, batch_size, size_of_image, pose_style
            )
            
            if not teacher_video_path or not os.path.exists(teacher_video_path):
                print(f"❌ Failed to generate teacher video for slide {i+1}")
                # Clean up audio
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                continue
            
            # Add small delay to ensure file is fully written
            time.sleep(1)
            
            # Create slide video clip (static image for audio duration)
            slide_clip = ImageClip(slide_image_path, duration=audio_duration)
            
            # Load teacher video clip with error handling
            try:
                teacher_clip = VideoFileClip(teacher_video_path)
            except Exception as e:
                print(f"❌ Error loading teacher video for slide {i+1}: {str(e)}")
                # Clean up audio
                if os.path.exists(audio_path):
                    os.remove(audio_path)
                continue
            
            # Resize teacher video to fit in bottom-right corner (picture-in-picture)
            # Calculate size: 25% of slide width, maintain aspect ratio
            slide_width, slide_height = slide_clip.size
            teacher_width = int(slide_width * 0.25)
            teacher_height = int(teacher_width * teacher_clip.h / teacher_clip.w)
            
            # Resize teacher video
            teacher_clip = teacher_clip.resize((teacher_width, teacher_height))
            
            # Position teacher video in bottom-right corner
            teacher_x = slide_width - teacher_width - 50  # 50px margin
            teacher_y = slide_height - teacher_height - 50  # 50px margin
            teacher_clip = teacher_clip.set_position((teacher_x, teacher_y))
            
            # Composite slide and teacher video
            composite_clip = CompositeVideoClip([slide_clip, teacher_clip])
            
            # Add to clips list
            slide_clips.append(composite_clip)
            total_duration += audio_duration
            
            # Track video file for later cleanup
            temp_video_files.append(teacher_video_path)
            
            print(f"✅ Slide {i+1} processed: {audio_duration:.2f}s")
            
            # Clean up temporary files with delay
            time.sleep(0.5)  # Small delay before cleanup
            if os.path.exists(audio_path):
                try:
                    os.remove(audio_path)
                except Exception as e:
                    print(f"⚠️ Could not remove audio file: {str(e)}")
            
            # Don't delete teacher video file immediately - it might still be in use
            # We'll clean it up later in the final cleanup
            print(f"📁 Teacher video saved for slide {i+1}: {os.path.basename(teacher_video_path)}")
        
        if not slide_clips:
            return None, "❌ Không thể tạo video cho bất kỳ slide nào!"
        
        print(f"\n--- Creating final lecture video ---")
        print(f"Total slides: {len(slide_clips)}")
        print(f"Total duration: {total_duration:.2f} seconds")
        
        # Concatenate all slide clips
        final_video_path = os.path.join(output_dir, "lecture_final.mp4")
        final_video = concatenate_videoclips(slide_clips, method="compose")
        
        print(f"Writing final video to: {final_video_path}")
        final_video.write_videofile(final_video_path, codec='libx264', audio_codec='aac', verbose=False, logger=None)
        
        # Clean up clips
        for clip in slide_clips:
            try:
                clip.close()
            except Exception as e:
                print(f"⚠️ Could not close clip: {str(e)}")
        try:
            final_video.close()
        except Exception as e:
            print(f"⚠️ Could not close final video: {str(e)}")
        
        # Add delay before cleanup
        time.sleep(1)
        
        # Clean up temporary slide images
        for i in range(len(slides_data)):
            slide_image_path = os.path.join(output_dir, f"slide_{i+1:02d}.png")
            if os.path.exists(slide_image_path):
                try:
                    os.remove(slide_image_path)
                except Exception as e:
                    print(f"⚠️ Could not remove slide image {i+1}: {str(e)}")
        
        # Clean up source image copy
        if os.path.exists(safe_image_path):
            try:
                os.remove(safe_image_path)
            except Exception as e:
                print(f"⚠️ Could not remove source image copy: {str(e)}")
        
        # Clean up temporary video files
        print("🧹 Cleaning up temporary video files...")
        for video_file in temp_video_files:
            if os.path.exists(video_file):
                try:
                    os.remove(video_file)
                    print(f"  ✅ Deleted: {os.path.basename(video_file)}")
                except Exception as e:
                    print(f"  ❌ Could not delete {os.path.basename(video_file)}: {str(e)}")
        
        # Also clean up temporary SadTalker directories
        print("🗂️ Cleaning up temporary SadTalker directories...")
        temp_dirs_deleted = 0
        results_dir = "results"
        if os.path.exists(results_dir):
            for item in os.listdir(results_dir):
                item_path = os.path.join(results_dir, item)
                # Check if it's a directory with UUID-like name (temporary SadTalker dirs)
                if os.path.isdir(item_path) and len(item) == 36 and '-' in item:
                    try:
                        shutil.rmtree(item_path)
                        print(f"  ✅ Deleted temp directory: {item}")
                        temp_dirs_deleted += 1
                    except Exception as e:
                        print(f"  ❌ Failed to delete temp directory {item}: {str(e)}")
        
        print(f"🗂️ Cleanup completed: {temp_dirs_deleted} temporary directories deleted")
        
        print(f"✅ Lecture video created successfully: {final_video_path}")
        
        return final_video_path, f"✅ Hoàn thành! Đã tạo video bài giảng với {len(slides_data)} slide, tổng thời gian: {total_duration:.1f}s"
        
    except Exception as e:
        print(f"Error in create_lecture_video: {str(e)}")
        return None, f"❌ Lỗi tạo video bài giảng: {str(e)}"

def generate_lecture_video_handler(sad_talker, pptx, img, lang, preprocess, still, enh, batch, size, pose):
    """Handler function for generating lecture video"""
    if not pptx or not img:
        return None, "❌ Vui lòng chọn file PowerPoint và ảnh giáo viên!"
    
    slides_data = extract_slides_from_pptx(pptx)
    if not slides_data:
        return None, "❌ Không thể trích xuất nội dung từ PowerPoint!"
    
    return create_lecture_video(
        sad_talker, slides_data, img, lang, preprocess, still, enh, batch, size, pose
    )
