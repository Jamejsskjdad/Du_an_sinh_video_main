from flask import Flask, Response

app = Flask(__name__)

HTML_CONTENT = r"""<!DOCTYPE html>
<html lang="vi">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SadTalker - Tạo Video Nói Chuyện Từ Ảnh Với AI</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link href="https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@300;400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Be Vietnam Pro', sans-serif;
            scroll-behavior: smooth;
            background-color: #f9fafb;
        }
        .gradient-text {
            background: linear-gradient(90deg, #6d28d9, #2563eb);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        .gradient-bg {
            background: linear-gradient(135deg, #6d28d9, #2563eb);
        }
        .fade-in {
            animation: fadeIn 0.5s ease-in-out;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .parallax {
            background-attachment: fixed;
            background-position: center;
            background-repeat: no-repeat;
            background-size: cover;
        }
        .card-hover:hover {
            transform: translateY(-5px);
            box-shadow: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
        }
        .icon-hover:hover .icon-animate {
            animation: bounce 0.6s ease infinite alternate;
        }
        @keyframes bounce {
            from { transform: translateY(0); }
            to { transform: translateY(-5px); }
        }
        .video-container:hover .video-overlay {
            opacity: 1;
        }
        .timeline-step {
            position: relative;
            padding-left: 2rem;
        }
        .timeline-step:before {
            content: '';
            position: absolute;
            left: 0;
            top: 0;
            width: 24px;
            height: 24px;
            border-radius: 50%;
            background: #6d28d9;
            border: 4px solid #e9d5ff;
        }
        .timeline-step:not(:last-child):after {
            content: '';
            position: absolute;
            left: 11px;
            top: 24px;
            width: 2px;
            height: 100%;
            background: #e5e7eb;
        }
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav class="fixed w-full bg-white shadow-sm z-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="flex justify-between h-16">
                <div class="flex items-center">
                    <a href="#" class="flex-shrink-0 flex items-center">
                        <span class="text-xl font-bold gradient-text">SadTalker</span>
                    </a>
                </div>
                <div class="hidden md:flex items-center space-x-8">
                    <a href="#gioi-thieu" class="text-gray-700 hover:text-purple-600 transition">Giới thiệu</a>
                    <a href="#tinh-nang" class="text-gray-700 hover:text-purple-600 transition">Tính năng</a>
                    <a href="#huong-dan" class="text-gray-700 hover:text-purple-600 transition">Cách sử dụng</a>
                    <a href="#demo" class="text-gray-700 hover:text-purple-600 transition">Video demo</a>
                    <a href="#cta" class="px-4 py-2 rounded-full gradient-bg text-white font-medium hover:opacity-90 transition">Bắt đầu ngay</a>
                </div>
                <div class="md:hidden flex items-center">
                    <button class="text-gray-700 hover:text-purple-600 focus:outline-none">
                        <i class="fas fa-bars text-xl"></i>
                    </button>
                </div>
            </div>
        </div>
    </nav>

    <!-- Hero Section -->
    <section class="pt-24 pb-16 md:pt-32 md:pb-24 bg-gradient-to-br from-purple-50 to-blue-50 relative overflow-hidden">
        <div class="absolute inset-0 opacity-20">
            <div class="absolute inset-0 bg-gradient-to-br from-purple-100 to-blue-200 animate-gradient"></div>
        </div>
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 relative z-10">
            <div class="md:flex md:items-center md:justify-between">
                <div class="md:w-1/2 mb-12 md:mb-0 fade-in">
                    <h1 class="text-4xl md:text-6xl font-bold leading-tight mb-6">
                        <span class="gradient-text">Tạo Video Nói Chuyện</span><br>
                        <span class="gradient-text">Từ Ảnh Với AI</span>
                    </h1>
                    <p class="text-lg md:text-xl text-gray-600 mb-8">
                        Biến ảnh chân dung thành video nói chuyện sống động chỉ với vài cú nhấp chuột
                    </p>
                    <a href="#cta" class="inline-block px-8 py-4 rounded-full gradient-bg text-white font-semibold text-lg hover:opacity-90 transition transform hover:scale-105 shadow-lg">
                        Bắt đầu tạo video
                        <i class="fas fa-arrow-right ml-2"></i>
                    </a>
                </div>
                <div class="md:w-1/2 flex justify-center fade-in">
                    <div class="relative w-full max-w-md">
                        <div class="aspect-w-16 aspect-h-9 bg-white rounded-xl shadow-2xl overflow-hidden transform rotate-2">
                            <img src="https://images.unsplash.com/photo-1566753323558-f4e0952af115" alt="AI Face Demo" class="object-cover w-full h-full">
                            <div class="absolute inset-0 flex items-center justify-center">
                                <div class="w-24 h-24 rounded-full flex items-center justify-center bg-white bg-opacity-80 animate-pulse">
                                    <i class="fas fa-play text-purple-600 text-3xl"></i>
                                </div>
                            </div>
                        </div>
                        <div class="absolute -bottom-6 -left-6 w-32 h-32 bg-purple-200 rounded-full opacity-50 -z-10"></div>
                        <div class="absolute -top-6 -right-6 w-40 h-40 bg-blue-200 rounded-full opacity-50 -z-10"></div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- About Section -->
    <section id="gioi-thieu" class="py-16 md:py-24 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-16 fade-in">
                <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                    Công Nghệ <span class="gradient-text">SadTalker</span>
                </h2>
                <p class="text-lg text-gray-600 max-w-2xl mx-auto">
                    Nền tảng AI tiên tiến dựa trên nghiên cứu CVPR 2023, mang đến những video nói chuyện thực tế nhất
                </p>
            </div>
            <div class="md:flex items-center">
                <div class="md:w-1/2 mb-12 md:mb-0 fade-in">
                    <div class="relative rounded-2xl overflow-hidden shadow-xl">
                        <img src="https://images.unsplash.com/photo-1620712943543-bcc4688e7485" alt="SadTalker Technology" class="w-full h-auto parallax">
                    </div>
                </div>
                <div class="md:w-1/2 md:pl-12 fade-in" style="animation-delay: 0.2s;">
                    <div class="mb-8">
                        <h3 class="text-2xl font-bold text-gray-900 mb-4">Công nghệ Deep Learning đột phá</h3>
                        <p class="text-gray-600">
                            SadTalker sử dụng mạng nơ-ron sâu và học máy tiên tiến để tạo chuyển động môi và biểu cảm khuôn mặt tự nhiên từ ảnh tĩnh.
                        </p>
                    </div>
                    <div class="mb-8">
                        <h3 class="text-2xl font-bold text-gray-900 mb-4">Dựa trên nghiên cứu CVPR 2023</h3>
                        <p class="text-gray-600">
                            Thuật toán của chúng tôi được phát triển dựa trên những nghiên cứu mới nhất trong lĩnh vực thị giác máy tính và xử lý hình ảnh.
                        </p>
                    </div>
                    <div>
                        <h3 class="text-2xl font-bold text-gray-900 mb-4">Tính năng nổi bật</h3>
                        <div class="grid grid-cols-2 gap-4">
                            <div class="flex items-start">
                                <span class="text-purple-600 mr-2 mt-1"><i class="fas fa-check-circle"></i></span>
                                <span class="text-gray-600">Chuyển động tự nhiên</span>
                            </div>
                            <div class="flex items-start">
                                <span class="text-purple-600 mr-2 mt-1"><i class="fas fa-check-circle"></i></span>
                                <span class="text-gray-600">Xử lý nhanh chóng</span>
                            </div>
                            <div class="flex items-start">
                                <span class="text-purple-600 mr-2 mt-1"><i class="fas fa-check-circle"></i></span>
                                <span class="text-gray-600">Hỗ trợ đa nền tảng</span>
                            </div>
                            <div class="flex items-start">
                                <span class="text-purple-600 mr-2 mt-1"><i class="fas fa-check-circle"></i></span>
                                <span class="text-gray-600">Bảo mật dữ liệu</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Features Section -->
    <section id="tinh-nang" class="py-16 md:py-24 bg-gray-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-16 fade-in">
                <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                    Tính Năng <span class="gradient-text">Nổi Bật</span>
                </h2>
                <p class="text-lg text-gray-600 max-w-2xl mx-auto">
                    Khám phá những tính năng ấn tượng mà SadTalker mang đến cho bạn
                </p>
            </div>
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-8">
                <!-- Feature 1 -->
                <div class="bg-white rounded-xl p-8 shadow-md hover:shadow-xl transition duration-300 card-hover fade-in icon-hover">
                    <div class="w-16 h-16 gradient-bg rounded-full flex items-center justify-center mb-6 mx-auto icon-animate">
                        <i class="fas fa-portrait text-white text-2xl"></i>
                    </div>
                    <h3 class="text-xl font-bold text-center text-gray-900 mb-3">Tạo video từ ảnh tĩnh</h3>
                    <p class="text-gray-600 text-center">
                        Biến bất kỳ ảnh chân dung nào thành video khuôn mặt nói chuyện với chất lượng cao
                    </p>
                </div>
                
                <!-- Feature 2 -->
                <div class="bg-white rounded-xl p-8 shadow-md hover:shadow-xl transition duration-300 card-hover fade-in icon-hover" style="animation-delay: 0.1s;">
                    <div class="w-16 h-16 gradient-bg rounded-full flex items-center justify-center mb-6 mx-auto icon-animate">
                        <i class="fas fa-microphone-alt text-white text-2xl"></i>
                    </div>
                    <h3 class="text-xl font-bold text-center text-gray-900 mb-3">Hỗ trợ đa dạng âm thanh</h3>
                    <p class="text-gray-600 text-center">
                        Nhập file âm thanh hoặc văn bản để chuyển đổi thành giọng nói tự nhiên
                    </p>
                </div>
                
                <!-- Feature 3 -->
                <div class="bg-white rounded-xl p-8 shadow-md hover:shadow-xl transition duration-300 card-hover fade-in icon-hover" style="animation-delay: 0.2s;">
                    <div class="w-16 h-16 gradient-bg rounded-full flex items-center justify-center mb-6 mx-auto icon-animate">
                        <i class="fas fa-sliders-h text-white text-2xl"></i>
                    </div>
                    <h3 class="text-xl font-bold text-center text-gray-900 mb-3">Tùy chỉnh linh hoạt</h3>
                    <p class="text-gray-600 text-center">
                        Điều chỉnh nhiều thông số để có được video hoàn hảo nhất
                    </p>
                </div>
                
                <!-- Feature 4 -->
                <div class="bg-white rounded-xl p-8 shadow-md hover:shadow-xl transition duration-300 card-hover fade-in icon-hover" style="animation-delay: 0.3s;">
                    <div class="w-16 h-16 gradient-bg rounded-full flex items-center justify-center mb-6 mx-auto icon-animate">
                        <i class="fas fa-bolt text-white text-2xl"></i>
                    </div>
                    <h3 class="text-xl font-bold text-center text-gray-900 mb-3">Tốc độ xử lý nhanh</h3>
                    <p class="text-gray-600 text-center">
                        Tạo video chỉ trong vài phút với công nghệ xử lý song song hiệu quả
                    </p>
                </div>
                
                <!-- Feature 5 -->
                <div class="bg-white rounded-xl p-8 shadow-md hover:shadow-xl transition duration-300 card-hover fade-in icon-hover" style="animation-delay: 0.4s;">
                    <div class="w-16 h-16 gradient-bg rounded-full flex items-center justify-center mb-6 mx-auto icon-animate">
                        <i class="fas fa-laugh-beam text-white text-2xl"></i>
                    </div>
                    <h3 class="text-xl font-bold text-center text-gray-900 mb-3">Biểu cảm tự nhiên</h3>
                    <p class="text-gray-600 text-center">
                        Chuyển động môi chính xác và biểu cảm khuôn mặt sống động như thật
                    </p>
                </div>
                
                <!-- Feature 6 -->
                <div class="bg-white rounded-xl p-8 shadow-md hover:shadow-xl transition duration-300 card-hover fade-in icon-hover" style="animation-delay: 0.5s;">
                    <div class="w-16 h-16 gradient-bg rounded-full flex items-center justify-center mb-6 mx-auto icon-animate">
                        <i class="fas fa-download text-white text-2xl"></i>
                    </div>
                    <h3 class="text-xl font-bold text-center text-gray-900 mb-3">Xuất video chất lượng cao</h3>
                    <p class="text-gray-600 text-center">
                        Tải video kết quả với nhiều định dạng và độ phân giải khác nhau
                    </p>
                </div>
            </div>
        </div>
    </section>

    <!-- How It Works Section -->
    <section id="huong-dan" class="py-16 md:py-24 bg-white">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-16 fade-in">
                <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                    Cách <span class="gradient-text">Sử Dụng</span>
                </h2>
                <p class="text-lg text-gray-600 max-w-2xl mx-auto">
                    Tạo video AI chỉ với 5 bước đơn giản
                </p>
            </div>
            <div class="max-w-3xl mx-auto">
                <!-- Step 1 -->
                <div class="mb-12 fade-in timeline-step">
                    <div class="bg-gray-50 rounded-xl p-6 md:p-8">
                        <div class="flex items-center mb-3">
                            <span class="text-white bg-purple-600 rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold mr-3">1</span>
                            <h3 class="text-xl font-bold text-gray-900">Tải ảnh khuôn mặt</h3>
                        </div>
                        <p class="text-gray-600 pl-11">
                            Chọn một bức ảnh chân dung rõ nét với khuôn mặt thẳng. Hệ thống hỗ trợ các định dạng JPG, PNG với kích thước lên đến 10MB.
                        </p>
                    </div>
                </div>
                
                <!-- Step 2 -->
                <div class="mb-12 fade-in timeline-step" style="animation-delay: 0.1s;">
                    <div class="bg-gray-50 rounded-xl p-6 md:p-8">
                        <div class="flex items-center mb-3">
                            <span class="text-white bg-purple-600 rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold mr-3">2</span>
                            <h3 class="text-xl font-bold text-gray-900">Chọn nguồn âm thanh</h3>
                        </div>
                        <p class="text-gray-600 pl-11">
                            Tải lên file âm thanh (MP3, WAV) hoặc nhập văn bản để hệ thống chuyển thành giọng nói bằng công nghệ TTS (Text-to-Speech).
                        </p>
                    </div>
                </div>
                
                <!-- Step 3 -->
                <div class="mb-12 fade-in timeline-step" style="animation-delay: 0.2s;">
                    <div class="bg-gray-50 rounded-xl p-6 md:p-8">
                        <div class="flex items-center mb-3">
                            <span class="text-white bg-purple-600 rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold mr-3">3</span>
                            <h3 class="text-xl font-bold text-gray-900">Điều chỉnh thông số</h3>
                        </div>
                        <p class="text-gray-600 pl-11">
                            Tùy chỉnh các thông số như tốc độ nói, độ mượt chuyển động, kiểu giọng (nam/nữ) để có được kết quả mong muốn.
                        </p>
                    </div>
                </div>
                
                <!-- Step 4 -->
                <div class="mb-12 fade-in timeline-step" style="animation-delay: 0.3s;">
                    <div class="bg-gray-50 rounded-xl p-6 md:p-8">
                        <div class="flex items-center mb-3">
                            <span class="text-white bg-purple-600 rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold mr-3">4</span>
                            <h3 class="text-xl font-bold text-gray-900">Nhấn "Sinh Video"</h3>
                        </div>
                        <p class="text-gray-600 pl-11">
                            Hệ thống sẽ xử lý ảnh và âm thanh để tạo video. Thời gian xử lý phụ thuộc vào độ dài âm thanh và tải server.
                        </p>
                    </div>
                </div>
                
                <!-- Step 5 -->
                <div class="fade-in timeline-step" style="animation-delay: 0.4s;">
                    <div class="bg-gray-50 rounded-xl p-6 md:p-8">
                        <div class="flex items-center mb-3">
                            <span class="text-white bg-purple-600 rounded-full w-8 h-8 flex items-center justify-center text-sm font-bold mr-3">5</span>
                            <h3 class="text-xl font-bold text-gray-900">Tải kết quả</h3>
                        </div>
                        <p class="text-gray-600 pl-11">
                            Xem trước video đã tạo và tải xuống nếu hài lòng. Hỗ trợ định dạng MP4 với nhiều độ phân giải khác nhau.
                        </p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- Demo Section -->
    <section id="demo" class="py-16 md:py-24 bg-gray-50">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="text-center mb-16 fade-in">
                <h2 class="text-3xl md:text-4xl font-bold text-gray-900 mb-4">
                    Video <span class="gradient-text">Demo</span>
                </h2>
                <p class="text-lg text-gray-600 max-w-2xl mx-auto">
                    Những kết quả ấn tượng từ người dùng SadTalker
                </p>
            </div>
            <div class="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
                <!-- Video 1 -->
                <div class="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-xl transition duration-300 fade-in video-container">
                    <div class="aspect-w-16 aspect-h-9">
                        <img src="https://images.unsplash.com/photo-1540569014015-19a7be504e3a" alt="Demo 1" class="object-cover w-full h-full">
                        <div class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30 video-overlay transition duration-300 opacity-0">
                            <div class="w-16 h-16 rounded-full flex items-center justify-center bg-white bg-opacity-80">
                                <i class="fas fa-play text-purple-600 text-xl"></i>
                            </div>
                        </div>
                    </div>
                    <div class="p-4">
                        <h3 class="font-bold text-gray-900 mb-2">Tạo video từ ảnh chân dung</h3>
                        <p class="text-gray-600 text-sm">Biểu cảm tự nhiên, chuyển động môi chính xác</p>
                    </div>
                </div>
                
                <!-- Video 2 -->
                <div class="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-xl transition duration-300 fade-in video-container" style="animation-delay: 0.1s;">
                    <div class="aspect-w-16 aspect-h-9">
                        <img src="https://images.unsplash.com/photo-1506794778202-cad84cf45f1d" alt="Demo 2" class="object-cover w-full h-full">
                        <div class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30 video-overlay transition duration-300 opacity-0">
                            <div class="w-16 h-16 rounded-full flex items-center justify-center bg-white bg-opacity-80">
                                <i class="fas fa-play text-purple-600 text-xl"></i>
                            </div>
                        </div>
                    </div>
                    <div class="p-4">
                        <h3 class="font-bold text-gray-900 mb-2">Video với phụ đề tích hợp</h3>
                        <p class="text-gray-600 text-sm">Nhập văn bản và hệ thống tự tạo video</p>
                    </div>
                </div>
                
                <!-- Video 3 -->
                <div class="bg-white rounded-xl overflow-hidden shadow-md hover:shadow-xl transition duration-300 fade-in video-container" style="animation-delay: 0.2s;">
                    <div class="aspect-w-16 aspect-h-9">
                        <img src="https://images.unsplash.com/photo-1566492031773-4f4e44671857" alt="Demo 3" class="object-cover w-full h-full">
                        <div class="absolute inset-0 flex items-center justify-center bg-black bg-opacity-30 video-overlay transition duration-300 opacity-0">
                            <div class="w-16 h-16 rounded-full flex items-center justify-center bg-white bg-opacity-80">
                                <i class="fas fa-play text-purple-600 text-xl"></i>
                            </div>
                        </div>
                    </div>
                    <div class="p-4">
                        <h3 class="font-bold text-gray-900 mb-2">Nhân vật hoạt hình nói chuyện</h3>
                        <p class="text-gray-600 text-sm">Áp dụng cho cả ảnh vẽ tay và hoạt hình</p>
                    </div>
                </div>
            </div>
        </div>
    </section>

    <!-- CTA Section -->
    <section id="cta" class="py-16 md:py-24 gradient-bg">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 text-center fade-in">
            <h2 class="text-3xl md:text-4xl font-bold text-white mb-6">
                Sẵn sàng tạo video AI đầu tiên của bạn?
            </h2>
            <p class="text-lg text-white opacity-90 mb-8 max-w-2xl mx-auto">
                Không cần kiến thức chuyên môn, chỉ cần vài thao tác đơn giản để có ngay video ấn tượng
            </p>
            <a href="#" class="inline-block px-8 py-4 bg-white text-purple-600 rounded-full font-semibold text-lg hover:bg-gray-100 transition transform hover:scale-105 shadow-lg">
                Bắt đầu ngay
                <i class="fas fa-arrow-right ml-2"></i>
            </a>
        </div>
    </section>

    <!-- Footer -->
    <footer class="bg-gray-900 text-white pt-16 pb-8">
        <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div class="grid md:grid-cols-4 gap-12">
                <div>
                    <h3 class="text-xl font-bold mb-6 gradient-text">SadTalker</h3>
                    <p class="text-gray-400 mb-6">
                        Nền tảng AI tạo video nói chuyện từ ảnh tiên tiến nhất, dựa trên công nghệ Deep Learning.
                    </p>
                    <div class="flex space-x-4">
                        <a href="#" class="text-gray-400 hover:text-white transition">
                            <i class="fab fa-facebook-f"></i>
                        </a>
                        <a href="#" class="text-gray-400 hover:text-white transition">
                            <i class="fab fa-twitter"></i>
                        </a>
                        <a href="#" class="text-gray-400 hover:text-white transition">
                            <i class="fab fa-github"></i>
                        </a>
                        <a href="#" class="text-gray-400 hover:text-white transition">
                            <i class="fab fa-linkedin-in"></i>
                        </a>
                    </div>
                </div>
                <div>
                    <h4 class="text-white font-semibold mb-6">Liên kết</h4>
                    <ul class="space-y-3">
                        <li><a href="#gioi-thieu" class="text-gray-400 hover:text-white transition">Giới thiệu</a></li>
                        <li><a href="#tinh-nang" class="text-gray-400 hover:text-white transition">Tính năng</a></li>
                        <li><a href="#huong-dan" class="text-gray-400 hover:text-white transition">Cách sử dụng</a></li>
                        <li><a href="#demo" class="text-gray-400 hover:text-white transition">Video demo</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-white font-semibold mb-6">Tài nguyên</h4>
                    <ul class="space-y-3">
                        <li><a href="#" class="text-gray-400 hover:text-white transition">Tài liệu hướng dẫn</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-white transition">API Developer</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-white transition">GitHub Repo</a></li>
                        <li><a href="#" class="text-gray-400 hover:text-white transition">Trang báo chí</a></li>
                    </ul>
                </div>
                <div>
                    <h4 class="text-white font-semibold mb-6">Liên hệ</h4>
                    <ul class="space-y-3">
                        <li class="flex items-start">
                            <i class="fas fa-envelope text-gray-400 mt-1 mr-2"></i>
                            <span class="text-gray-400">contact@sadtalker.com</span>
                        </li>
                        <li class="flex items-start">
                            <i class="fas fa-phone-alt text-gray-400 mt-1 mr-2"></i>
                            <span class="text-gray-400">+84 123 456 789</span>
                        </li>
                        <li class="flex items-start">
                            <i class="fas fa-map-marker-alt text-gray-400 mt-1 mr-2"></i>
                            <span class="text-gray-400">Hà Nội, Việt Nam</span>
                        </li>
                    </ul>
                </div>
            </div>
            <div class="border-t border-gray-800 mt-12 pt-8 text-center text-gray-500">
                <p>© 2023 SadTalker. All rights reserved.</p>
            </div>
        </div>
    </footer>

    <script>
        // Simple animation on scroll
        document.addEventListener('DOMContentLoaded', function() {
            const fadeElements = document.querySelectorAll('.fade-in');
            
            const observer = new IntersectionObserver((entries) => {
                entries.forEach(entry => {
                    if (entry.isIntersecting) {
                        entry.target.style.opacity = 1;
                        entry.target.style.transform = 'translateY(0)';
                    }
                });
            }, {
                threshold: 0.1
            });
            
            fadeElements.forEach(el => {
                el.style.opacity = 0;
                el.style.transform = 'translateY(20px)';
                el.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
                observer.observe(el);
            });
            
            // Smooth scrolling for anchor links
            document.querySelectorAll('a[href^="#"]').forEach(anchor => {
                anchor.addEventListener('click', function(e) {
                    e.preventDefault();
                    document.querySelector(this.getAttribute('href')).scrollIntoView({
                        behavior: 'smooth'
                    });
                });
            });
        });
    </script>
</body>
</html>"""

@app.route("/")
def home():
    return Response(HTML_CONTENT, mimetype="text/html; charset=utf-8")


if __name__ == "__main__":
    # For production, use a WSGI server. This is fine for local dev.
    app.run(host="0.0.0.0", port=5000, debug=True)
