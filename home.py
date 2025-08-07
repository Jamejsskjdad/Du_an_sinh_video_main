import gradio as gr

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

def create_home_tab():
    """Tạo tab trang chủ"""
    return gr.HTML("""
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
                <li style="color: #000 !important; margin-bottom: 10px;">📄 Import văn bản từ file (.txt, .md, .doc, .docx)</li>
                <li style="color: #000 !important; margin-bottom: 10px;">🎓 Tạo video bài giảng (slide + giáo viên giảng)</li>
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
                <li style="color: #000 !important; margin-bottom: 10px;">📄 Hoặc import văn bản từ file</li>
                <li style="color: #000 !important; margin-bottom: 10px;">⚙️ Điều chỉnh các thông số</li>
                <li style="color: #000 !important; margin-bottom: 10px;">🎬 Nhấn "Sinh Video" để tạo</li>
                <li style="color: #000 !important; margin-bottom: 10px;">💾 Tải xuống kết quả</li>
            </ul>
        </div>
    </div>
    <div class="sad-home-btn-wrap">
        <button class="sad-home-btn" onclick="document.querySelectorAll('.tabitem')[1].click();">🎓 Chuyển đến giao diện Tạo Bài Giảng</button>
    </div>
    """)
