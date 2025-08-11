import gradio as gr
import os

def create_home_tab():
    """Tạo tab trang chủ với giao diện đẹp"""
    
    with gr.Column(elem_classes=["home-container"]):
        # Hero Section
        with gr.Row(elem_classes=["hero-section"], elem_attrs={"style": "background: linear-gradient(135deg, #f3f4f6, #e5e7eb); padding: 4rem 2rem; border-radius: 1rem; margin: 2rem 0; align-items: center;"}):
            with gr.Column(scale=1):
                gr.HTML("""
                    <div class="hero-content" style="padding-right: 2rem;">
                        <h1 class="hero-title" style="font-size: 3rem; font-weight: 700; line-height: 1.2; margin-bottom: 1.5rem;">
                            <span class="gradient-text" style="background: linear-gradient(90deg, #6d28d9, #2563eb); -webkit-background-clip: text; background-clip: text; color: transparent;">Tạo Video Nói Chuyện</span><br>
                            <span class="gradient-text" style="background: linear-gradient(90deg, #6d28d9, #2563eb); -webkit-background-clip: text; background-clip: text; color: transparent;">Từ Ảnh Với AI</span>
                        </h1>
                        <p class="hero-description" style="font-size: 1.25rem; color: #374151; margin-bottom: 2rem; font-weight: 500;">
                            Biến ảnh chân dung thành video nói chuyện sống động chỉ với vài cú nhấp chuột
                        </p>
                        <div class="hero-buttons" style="display: flex; gap: 1rem;">
                            <button class="btn-primary" onclick="scrollToSection('features')" style="background: linear-gradient(135deg, #6d28d9, #2563eb); color: white; padding: 0.75rem 1.5rem; border: none; border-radius: 2rem; font-weight: 600; font-size: 1rem; cursor: pointer; transition: all 0.3s ease; display: inline-flex; align-items: center; gap: 0.5rem;">
                                Khám phá tính năng
                                <i class="fas fa-arrow-right"></i>
                            </button>
                        </div>
                    </div>
                """)
            with gr.Column(scale=1):
                gr.HTML("""
                    <div class="hero-image" style="display: flex; justify-content: center; align-items: center;">
                        <div class="demo-video-container" style="position: relative; width: 100%; max-width: 400px; border-radius: 1rem; overflow: hidden; box-shadow: 0 20px 25px rgba(0, 0, 0, 0.1); transform: rotate(2deg);">
                            <img src="https://images.unsplash.com/photo-1566753323558-f4e0952af115" alt="AI Face Demo" class="demo-image" style="width: 100%; height: auto; display: block;">
                            <div class="play-button" style="position: absolute; top: 50%; left: 50%; transform: translate(-50%, -50%); width: 4rem; height: 4rem; background: rgba(255, 255, 255, 0.9); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: #6d28d9; font-size: 1.5rem;">
                                <i class="fas fa-play"></i>
                            </div>
                        </div>
                    </div>
                """)
        
        # About Section
        with gr.Row(elem_classes=["section"], elem_id="about"):
            gr.HTML("""
                <div class="section-header" style="text-align: center; margin-bottom: 3rem;">
                    <h2 style="font-size: 2.5rem; font-weight: 700; color: #1f2937; margin-bottom: 1rem;">Công Nghệ <span class="gradient-text" style="background: linear-gradient(90deg, #6d28d9, #2563eb); -webkit-background-clip: text; background-clip: text; color: transparent;">SadTalker</span></h2>
                    <p style="font-size: 1.125rem; color: #6b7280; max-width: 600px; margin: 0 auto;">Nền tảng AI tiên tiến dựa trên nghiên cứu CVPR 2023, mang đến những video nói chuyện thực tế nhất</p>
                </div>
            """)
            
            with gr.Row():
                with gr.Column(scale=1):
                    gr.HTML("""
                        <div class="about-image">
                            <img src="https://images.unsplash.com/photo-1620712943543-bcc4688e7485" alt="SadTalker Technology" style="width: 100%; border-radius: 1rem; box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);">
                        </div>
                    """)
                with gr.Column(scale=1):
                    gr.HTML("""
                        <div class="about-content" style="padding-left: 2rem;">
                            <div class="feature-item" style="margin-bottom: 2rem;">
                                <h3 style="font-size: 1.5rem; font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">🎯 Công nghệ Deep Learning đột phá</h3>
                                <p style="color: #6b7280; line-height: 1.6;">SadTalker sử dụng mạng nơ-ron sâu và học máy tiên tiến để tạo chuyển động môi và biểu cảm khuôn mặt tự nhiên từ ảnh tĩnh.</p>
                            </div>
                            <div class="feature-item" style="margin-bottom: 2rem;">
                                <h3 style="font-size: 1.5rem; font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">📚 Dựa trên nghiên cứu CVPR 2023</h3>
                                <p style="color: #6b7280; line-height: 1.6;">Thuật toán của chúng tôi được phát triển dựa trên những nghiên cứu mới nhất trong lĩnh vực thị giác máy tính và xử lý hình ảnh.</p>
                            </div>
                            <div class="feature-item" style="margin-bottom: 2rem;">
                                <h3 style="font-size: 1.5rem; font-weight: 600; color: #1f2937; margin-bottom: 0.5rem;">✨ Tính năng nổi bật</h3>
                                <div class="feature-grid" style="display: grid; grid-template-columns: repeat(2, 1fr); gap: 0.5rem; margin-top: 1rem;">
                                    <div class="feature-tag" style="background: #f3f4f6; color: #374151; padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.875rem; font-weight: 500;">Chuyển động tự nhiên</div>
                                    <div class="feature-tag" style="background: #f3f4f6; color: #374151; padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.875rem; font-weight: 500;">Xử lý nhanh chóng</div>
                                    <div class="feature-tag" style="background: #f3f4f6; color: #374151; padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.875rem; font-weight: 500;">Hỗ trợ đa nền tảng</div>
                                    <div class="feature-tag" style="background: #f3f4f6; color: #374151; padding: 0.5rem 1rem; border-radius: 0.5rem; font-size: 0.875rem; font-weight: 500;">Bảo mật dữ liệu</div>
                                </div>
                            </div>
                        </div>
                    """)

def custom_home_css():
    """CSS tùy chỉnh cho trang home"""
    return """
    <style>
        /* Import fonts */
        @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap');
        @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
        
        /* Global styles */
        .home-container {
            font-family: 'Be Vietnam Pro', sans-serif;
            background-color: #f9fafb;
            min-height: 100vh;
        }
        
        /* Section styles */
        .section {
            padding: 4rem 0;
            margin: 0;
        }
        
        /* Animation */
        .fade-in {
            animation: fadeIn 0.6s ease-out;
        }
        
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
    
    <script>
        function scrollToSection(sectionId) {
            const element = document.getElementById(sectionId);
            if (element) {
                element.scrollIntoView({ behavior: 'smooth' });
            }
        }
        
        function scrollToTop() {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        }
        
        // Add fade-in animation to elements
        document.addEventListener('DOMContentLoaded', function() {
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.classList.add('fade-in');
                    }
                });
            }, { threshold: 0.1 });
            
            document.querySelectorAll('.section, .feature-card, .demo-card, .timeline-step').forEach(el => {
                observer.observe(el);
            });
        });
    </script>
    """

# Giữ lại hàm cũ để tương thích ngược
def home():
    """Hàm cũ để tương thích với Flask - không sử dụng trong Gradio"""
    return "Trang home đã được chuyển đổi sang Gradio"

