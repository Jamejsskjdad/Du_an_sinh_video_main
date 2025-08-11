import gradio as gr

def create_home_tab():
    """Tạo tab Home với Gradio + HTML/CSS/JS thuần"""
    
    # HTML content với tất cả CSS inline
    html_content = """
    <!DOCTYPE html>
    <html lang="vi">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>SadTalker - Create Talking Videos From Photos</title>
    </head>
    <body style="margin: 0; padding: 0; font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #111827; overflow-x: hidden;">
        <!-- Navbar -->
        <nav style="position: fixed; top: 0; left: 0; right: 0; background: rgba(255, 255, 255, 0.95); backdrop-filter: blur(10px); border-bottom: 1px solid rgba(0, 0, 0, 0.1); z-index: 1000; transition: all 0.3s ease;">
            <div style="max-width: 1200px; margin: 0 auto; padding: 0 24px;">
                <div style="display: flex; justify-content: space-between; align-items: center; padding: 16px 0;">
                    <div style="font-size: 24px; font-weight: bold; background: linear-gradient(135deg, #8B5CF6, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">SadTalker</div>
                    <ul style="display: flex; gap: 32px; list-style: none; margin: 0; padding: 0;">
                        <li><a href="#features" onclick="scrollToSection('#features')" style="text-decoration: none; color: #111827; font-weight: 500; transition: color 0.3s ease; cursor: pointer;">Features</a></li>
                        <li><a href="#howitworks" onclick="scrollToSection('#howitworks')" style="text-decoration: none; color: #111827; font-weight: 500; transition: color 0.3s ease; cursor: pointer;">How It Works</a></li>
                        <li><a href="#showcase" onclick="scrollToSection('#showcase')" style="text-decoration: none; color: #111827; font-weight: 500; transition: color 0.3s ease; cursor: pointer;">Showcase</a></li>
                        <li><a href="#about" onclick="scrollToSection('#about')" style="text-decoration: none; color: #111827; font-weight: 500; transition: color 0.3s ease; cursor: pointer;">About</a></li>
                    </ul>
                    <button style="background: linear-gradient(135deg, #8B5CF6, #3B82F6); color: white; padding: 12px 24px; border: none; border-radius: 8px; font-weight: 600; cursor: pointer; transition: transform 0.3s ease;" onclick="(function(){var b=document.querySelector('#nav_get_started_btn'); if(b){ b.click(); }})();">Get Started</button>
                </div>
            </div>
        </nav>

        <!-- Hero Section -->
        <section style="min-height: 100vh; background: linear-gradient(135deg, #1e1b4b 0%, #312e81 50%, #1e40af 100%); position: relative; display: flex; align-items: center; overflow: hidden;">
            <div style="max-width: 1200px; margin: 0 auto; padding: 0 24px; width: 100%;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; position: relative; z-index: 2;">
                    <div>
                        <h1 style="font-size: 56px; font-weight: bold; line-height: 1.1; margin-bottom: 24px; color: white;">
                            <span style="background: linear-gradient(135deg, #fbbf24, #f59e0b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Create Talking Videos</span><br>
                            From Photos With AI
                        </h1>
                        <p style="font-size: 20px; color: rgba(255, 255, 255, 0.8); margin-bottom: 32px; line-height: 1.6;">
                            Transform any portrait photo into a realistic talking video using advanced AI technology. No technical skills required.
                        </p>
                        <button style="background: linear-gradient(135deg, #8B5CF6, #3B82F6); color: white; padding: 16px 32px; border: none; border-radius: 12px; font-size: 18px; font-weight: 600; cursor: pointer; transition: all 0.3s ease; box-shadow: 0 10px 30px rgba(139, 92, 246, 0.3);" onclick="(function(){var b=document.querySelector('#nav_get_started_btn'); if(b){ b.click(); }})();">Start Creating Videos</button>
                    </div>
                    <div style="position: relative;">
                        <div style="background: rgba(255, 255, 255, 0.1); border-radius: 16px; padding: 8px; backdrop-filter: blur(10px); border: 1px solid rgba(255, 255, 255, 0.2); box-shadow: 0 25px 50px rgba(0, 0, 0, 0.3);">
                            <video style="width: 100%; border-radius: 12px; display: block;" autoplay muted loop>
                                <source src="https://assets.mixkit.co/videos/preview/mixkit-woman-talking-on-a-video-call-3980-large.mp4" type="video/mp4">
                            </video>
                        </div>
                    </div>
                </div>
                <div style="position: absolute; bottom: 32px; left: 50%; transform: translateX(-50%); color: white; text-align: center; cursor: pointer;" onclick="scrollToSection('#about')">
                    <div>Scroll Down</div>
                    <div style="font-size: 24px; animation: bounce 2s infinite;">↓</div>
                </div>
            </div>
        </section>

        <!-- About Section -->
        <section id="about" style="padding: 120px 0; background: #f8fafc;">
            <div style="max-width: 1200px; margin: 0 auto; padding: 0 24px;">
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center;">
                    <div style="position: relative;">
                        <video style="width: 100%; border-radius: 16px; box-shadow: 0 20px 40px rgba(0, 0, 0, 0.1);" autoplay muted loop>
                            <source src="https://assets.mixkit.co/videos/preview/mixkit-man-talking-on-a-video-call-3981-large.mp4" type="video/mp4">
                        </video>
                    </div>
                    <div>
                        <h2 style="font-size: 42px; font-weight: bold; margin-bottom: 24px; background: linear-gradient(135deg, #8B5CF6, #3B82F6); -webkit-background-clip: text; -webkit-text-fill-color: transparent; background-clip: text;">Advanced AI Technology</h2>
                        <p style="font-size: 18px; color: #6B7280; margin-bottom: 24px; line-height: 1.7;">
                            Our cutting-edge artificial intelligence transforms static photos into lifelike talking videos with remarkable accuracy and natural expressions.
                        </p>
                        <p style="font-size: 18px; color: #6B7280; margin-bottom: 24px; line-height: 1.7;">
                            Using deep learning algorithms trained on millions of facial expressions and speech patterns, SadTalker creates videos that are virtually indistinguishable from real recordings.
                        </p>
                        <div style="display: flex; gap: 32px; margin-top: 32px;">
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="width: 12px; height: 12px; background: linear-gradient(135deg, #8B5CF6, #3B82F6); border-radius: 50%;"></div>
                                <span style="font-weight: 600; color: #111827;">Deep Learning</span>
                            </div>
                            <div style="display: flex; align-items: center; gap: 12px;">
                                <div style="width: 12px; height: 12px; background: linear-gradient(135deg, #8B5CF6, #3B82F6); border-radius: 50%;"></div>
                                <span style="font-weight: 600; color: #111827;">AI Generated</span>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Features Section -->
        <section id="features" style="padding: 120px 0; background: white;">
            <div style="max-width: 1200px; margin: 0 auto; padding: 0 24px;">
                <div style="text-align: center; margin-bottom: 80px;">
                    <h2 style="font-size: 42px; font-weight: bold; margin-bottom: 16px; color: #111827;">Powerful Features</h2>
                    <p style="font-size: 20px; color: #6B7280; max-width: 600px; margin: 0 auto;">Everything you need to create amazing talking videos from photos</p>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 32px;">
                    <div style="background: white; padding: 32px; border-radius: 16px; border: 1px solid #e5e7eb; transition: all 0.3s ease; text-align: center;">
                        <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #8B5CF6, #3B82F6); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 24px; font-size: 24px; color: white;">🎬</div>
                        <h3 style="font-size: 24px; font-weight: bold; margin-bottom: 16px; color: #111827;">Photo to Video</h3>
                        <p style="color: #6B7280; line-height: 1.6;">Transform any portrait photo into a realistic talking video with natural lip-sync and facial expressions.</p>
                    </div>
                    <div style="background: white; padding: 32px; border-radius: 16px; border: 1px solid #e5e7eb; transition: all 0.3s ease; text-align: center;">
                        <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #8B5CF6, #3B82F6); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 24px; font-size: 24px; color: white;">🎵</div>
                        <h3 style="font-size: 24px; font-weight: bold; margin-bottom: 16px; color: #111827;">Audio Support</h3>
                        <p style="color: #6B7280; line-height: 1.6;">Upload your own audio or use text-to-speech to make your photos speak with perfect synchronization.</p>
                    </div>
                    <div style="background: white; padding: 32px; border-radius: 16px; border: 1px solid #e5e7eb; transition: all 0.3s ease; text-align: center;">
                        <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #8B5CF6, #3B82F6); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 24px; font-size: 24px; color: white;">🎨</div>
                        <h3 style="font-size: 24px; font-weight: bold; margin-bottom: 16px; color: #111827;">Customization</h3>
                        <p style="color: #6B7280; line-height: 1.6;">Fine-tune expressions, adjust timing, and customize the output to match your creative vision.</p>
                    </div>
                    <div style="background: white; padding: 32px; border-radius: 16px; border: 1px solid #e5e7eb; transition: all 0.3s ease; text-align: center;">
                        <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #8B5CF6, #3B82F6); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 24px; font-size: 24px; color: white;">⚡</div>
                        <h3 style="font-size: 24px; font-weight: bold; margin-bottom: 16px; color: #111827;">Fast Processing</h3>
                        <p style="color: #6B7280; line-height: 1.6;">Generate high-quality talking videos in minutes, not hours. Our optimized AI ensures quick results.</p>
                    </div>
                    <div style="background: white; padding: 32px; border-radius: 16px; border: 1px solid #e5e7eb; transition: all 0.3s ease; text-align: center;">
                        <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #8B5CF6, #3B82F6); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 24px; font-size: 24px; color: white;">🔒</div>
                        <h3 style="font-size: 24px; font-weight: bold; margin-bottom: 16px; color: #111827;">Privacy Focused</h3>
                        <p style="color: #6B7280; line-height: 1.6;">Your photos and videos are processed securely and never stored on our servers after processing.</p>
                    </div>
                    <div style="background: white; padding: 32px; border-radius: 16px; border: 1px solid #e5e7eb; transition: all 0.3s ease; text-align: center;">
                        <div style="width: 64px; height: 64px; background: linear-gradient(135deg, #8B5CF6, #3B82F6); border-radius: 50%; display: flex; align-items: center; justify-content: center; margin: 0 auto 24px; font-size: 24px; color: white;">📱</div>
                        <h3 style="font-size: 24px; font-weight: bold; margin-bottom: 16px; color: #111827;">Multiple Formats</h3>
                        <p style="color: #6B7280; line-height: 1.6;">Export in various formats and resolutions suitable for social media, presentations, or personal use.</p>
                    </div>
                </div>
            </div>
        </section>

        <!-- How It Works -->
        <section id="howitworks" style="padding: 120px 0; background: #f8fafc;">
            <div style="max-width: 1200px; margin: 0 auto; padding: 0 24px;">
                <div style="text-align: center; margin-bottom: 80px;">
                    <h2 style="font-size: 42px; font-weight: bold; margin-bottom: 16px; color: #111827;">How It Works</h2>
                    <p style="font-size: 20px; color: #6B7280; max-width: 600px; margin: 0 auto;">Create talking videos in just 5 simple steps</p>
                </div>
                <div style="max-width: 800px; margin: 0 auto;">
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; margin-bottom: 80px;">
                        <div>
                            <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #8B5CF6, #3B82F6); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px; margin-bottom: 24px;">1</div>
                            <h3 style="font-size: 28px; font-weight: bold; margin-bottom: 16px; color: #111827;">Upload Photo</h3>
                            <p style="font-size: 18px; color: #6B7280; line-height: 1.6;">Choose a clear portrait photo with the face clearly visible. Our AI works best with front-facing photos.</p>
                        </div>
                        <div style="background: white; border-radius: 16px; padding: 32px; text-align: center; border: 1px solid #e5e7eb; font-size: 48px;">📸</div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; margin-bottom: 80px;">
                        <div style="order: 2;">
                            <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #8B5CF6, #3B82F6); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px; margin-bottom: 24px;">2</div>
                            <h3 style="font-size: 28px; font-weight: bold; margin-bottom: 16px; color: #111827;">Add Audio</h3>
                            <p style="font-size: 18px; color: #6B7280; line-height: 1.6;">Upload an audio file or use our text-to-speech feature to generate the voice for your talking video.</p>
                        </div>
                        <div style="background: white; border-radius: 16px; padding: 32px; text-align: center; border: 1px solid #e5e7eb; font-size: 48px; order: 1;">🎤</div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; margin-bottom: 80px;">
                        <div>
                            <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #8B5CF6, #3B82F6); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px; margin-bottom: 24px;">3</div>
                            <h3 style="font-size: 28px; font-weight: bold; margin-bottom: 16px; color: #111827;">AI Processing</h3>
                            <p style="font-size: 18px; color: #6B7280; line-height: 1.6;">Our advanced AI analyzes the photo and audio to create natural facial movements and lip synchronization.</p>
                        </div>
                        <div style="background: white; border-radius: 16px; padding: 32px; text-align: center; border: 1px solid #e5e7eb; font-size: 48px;">🤖</div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; margin-bottom: 80px;">
                        <div style="order: 2;">
                            <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #8B5CF6, #3B82F6); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px; margin-bottom: 24px;">4</div>
                            <h3 style="font-size: 28px; font-weight: bold; margin-bottom: 16px; color: #111827;">Preview & Edit</h3>
                            <p style="font-size: 18px; color: #6B7280; line-height: 1.6;">Review your talking video and make adjustments to timing, expressions, or other parameters as needed.</p>
                        </div>
                        <div style="background: white; border-radius: 16px; padding: 32px; text-align: center; border: 1px solid #e5e7eb; font-size: 48px; order: 1;">👁️</div>
                    </div>
                    <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 64px; align-items: center; margin-bottom: 80px;">
                        <div>
                            <div style="width: 48px; height: 48px; background: linear-gradient(135deg, #8B5CF6, #3B82F6); border-radius: 50%; display: flex; align-items: center; justify-content: center; color: white; font-weight: bold; font-size: 20px; margin-bottom: 24px;">5</div>
                            <h3 style="font-size: 28px; font-weight: bold; margin-bottom: 16px; color: #111827;">Download</h3>
                            <p style="font-size: 18px; color: #6B7280; line-height: 1.6;">Export your finished talking video in your preferred format and resolution, ready to share or use.</p>
                        </div>
                        <div style="background: white; border-radius: 16px; padding: 32px; text-align: center; border: 1px solid #e5e7eb; font-size: 48px;">⬇️</div>
                    </div>
                </div>
            </div>
        </section>

        <!-- Showcase -->
        <section id="showcase" style="padding: 120px 0; background: white;">
            <div style="max-width: 1200px; margin: 0 auto; padding: 0 24px;">
                <div style="text-align: center; margin-bottom: 80px;">
                    <h2 style="font-size: 42px; font-weight: bold; margin-bottom: 16px; color: #111827;">Video Showcase</h2>
                    <p style="font-size: 20px; color: #6B7280; max-width: 600px; margin: 0 auto;">See what's possible with SadTalker AI technology</p>
                </div>
                <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(350px, 1fr)); gap: 32px; margin-bottom: 64px;">
                    <div style="position: relative; border-radius: 16px; overflow: hidden; background: #000; cursor: pointer; transition: transform 0.3s ease;">
                        <video style="width: 100%; height: 250px; object-fit: cover; transition: opacity 0.3s ease;" muted>
                            <source src="https://assets.mixkit.co/videos/preview/mixkit-woman-talking-on-a-video-call-3980-large.mp4" type="video/mp4">
                        </video>
                        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(transparent 60%, rgba(0,0,0,0.8)); display: flex; align-items: center; justify-content: center; opacity: 1; transition: opacity 0.3s ease;">
                            <div style="width: 64px; height: 64px; background: rgba(255, 255, 255, 0.9); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; color: #111827;">▶</div>
                        </div>
                        <div style="position: absolute; bottom: 16px; left: 16px; color: white; font-weight: 600;">Portrait Animation</div>
                    </div>
                    <div style="position: relative; border-radius: 16px; overflow: hidden; background: #000; cursor: pointer; transition: transform 0.3s ease;">
                        <video style="width: 100%; height: 250px; object-fit: cover; transition: opacity 0.3s ease;" muted>
                            <source src="https://assets.mixkit.co/videos/preview/mixkit-man-talking-on-a-video-call-3981-large.mp4" type="video/mp4">
                        </video>
                        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(transparent 60%, rgba(0,0,0,0.8)); display: flex; align-items: center; justify-content: center; opacity: 1; transition: opacity 0.3s ease;">
                            <div style="width: 64px; height: 64px; background: rgba(255, 255, 255, 0.9); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; color: #111827;">▶</div>
                        </div>
                        <div style="position: absolute; bottom: 16px; left: 16px; color: white; font-weight: 600;">Speech Synthesis</div>
                    </div>
                    <div style="position: relative; border-radius: 16px; overflow: hidden; background: #000; cursor: pointer; transition: transform 0.3s ease;">
                        <video style="width: 100%; height: 250px; object-fit: cover; transition: opacity 0.3s ease;" muted>
                            <source src="https://assets.mixkit.co/videos/preview/mixkit-woman-talking-on-a-video-call-3980-large.mp4" type="video/mp4">
                        </video>
                        <div style="position: absolute; top: 0; left: 0; right: 0; bottom: 0; background: linear-gradient(transparent 60%, rgba(0,0,0,0.8)); display: flex; align-items: center; justify-content: center; opacity: 1; transition: opacity 0.3s ease;">
                            <div style="width: 64px; height: 64px; background: rgba(255, 255, 255, 0.9); border-radius: 50%; display: flex; align-items: center; justify-content: center; font-size: 24px; color: #111827;">▶</div>
                        </div>
                        <div style="position: absolute; bottom: 16px; left: 16px; color: white; font-weight: 600;">Realistic Expression</div>
                    </div>
                </div>
                <div style="text-align: center;">
                    <button style="background: linear-gradient(135deg, #8B5CF6, #3B82F6); color: white; padding: 16px 32px; border: none; border-radius: 12px; font-size: 18px; font-weight: 600; cursor: pointer; transition: all 0.3s ease;" onclick="(function(){var b=document.querySelector('#nav_get_started_btn'); if(b){ b.click(); }})();">Try It Yourself</button>
                </div>
            </div>
        </section>

        <!-- CTA Section -->
        <section id="cta" style="padding: 120px 0; background: linear-gradient(135deg, #8B5CF6, #3B82F6); text-align: center; color: white;">
            <div style="max-width: 1200px; margin: 0 auto; padding: 0 24px;">
                <h2 style="font-size: 48px; font-weight: bold; margin-bottom: 24px;">Ready to Create Amazing Talking Videos?</h2>
                <p style="font-size: 20px; margin-bottom: 48px; opacity: 0.9; max-width: 600px; margin-left: auto; margin-right: auto;">
                    Join thousands of creators who are already using SadTalker to bring their photos to life with AI technology.
                </p>
                <div style="display: flex; gap: 24px; justify-content: center; flex-wrap: wrap;">
                    <button style="background: white; color: #8B5CF6; padding: 16px 32px; border: none; border-radius: 12px; font-size: 18px; font-weight: 600; cursor: pointer; transition: all 0.3s ease;" onclick="(function(){var b=document.querySelector('#nav_get_started_btn'); if(b){ b.click(); }})();">Start Creating Now</button>
                    <button style="background: transparent; color: white; padding: 16px 32px; border: 2px solid white; border-radius: 12px; font-size: 18px; font-weight: 600; cursor: pointer; transition: all 0.3s ease;" onclick="scrollToSection('#about')">Learn More</button>
                </div>
            </div>
        </section>

        <style>
            @keyframes bounce {
                0%, 20%, 50%, 80%, 100% { transform: translateY(0); }
                40% { transform: translateY(-10px); }
                60% { transform: translateY(-5px); }
            }
            
            /* Responsive */
            @media (max-width: 768px) {
                .hero-content {
                    grid-template-columns: 1fr !important;
                    text-align: center;
                }
                
                .hero-text h1 {
                    font-size: 42px !important;
                }
                
                .about-content {
                    grid-template-columns: 1fr !important;
                }
                
                .step {
                    grid-template-columns: 1fr !important;
                }
                
                .step:nth-child(even) .step-content,
                .step:nth-child(even) .step-visual {
                    order: unset !important;
                }
                
                .features-grid {
                    grid-template-columns: 1fr !important;
                }
                
                .showcase-grid {
                    grid-template-columns: 1fr !important;
                }
                
                .features-list {
                    flex-direction: column !important;
                    gap: 16px !important;
                }
                
                .nav-links {
                    display: none !important;
                }
                
                .cta-buttons {
                    flex-direction: column !important;
                    align-items: center !important;
                }
            }
        </style>

        <script>
            // Định nghĩa các function trong global scope ngay từ đầu
            function scrollToSection(target) {
                console.log('scrollToSection called with:', target);
                const element = document.querySelector(target);
                if (element) {
                    element.scrollIntoView({ 
                        behavior: 'smooth',
                        block: 'start'
                    });
                } else {
                    console.log('Element not found:', target);
                }
            }
            
            function triggerStartBtn() {
                console.log('triggerStartBtn called');
                
                // Thử dispatch event trước
                try {
                    const customEvent = new CustomEvent('startVideoCreation', {
                        detail: { action: 'navigate_to_video_tab' },
                        bubbles: true
                    });
                    document.dispatchEvent(customEvent);
                    console.log('Custom event dispatched');
                } catch (e) {
                    console.error('Error dispatching custom event:', e);
                }
                
                // Thử tìm button Gradio
                setTimeout(() => {
                    const selectors = [
                        '#nav_get_started_btn',
                        'button[data-testid="start_btn"]',
                        'button[id*="start"]',
                        'button[id*="nav"]'
                    ];
                    
                    let found = false;
                    for (const selector of selectors) {
                        const btn = document.querySelector(selector);
                        if (btn) {
                            console.log('Found button with selector:', selector);
                            btn.click();
                            found = true;
                            break;
                        }
                    }
                    
                    if (!found) {
                        // Tìm tất cả button và log ra
                        const allButtons = document.querySelectorAll('button');
                        console.log('All buttons found:', allButtons.length);
                        allButtons.forEach((btn, index) => {
                            console.log(`Button ${index}:`, {
                                id: btn.id,
                                className: btn.className,
                                textContent: btn.textContent?.trim(),
                                onclick: btn.onclick
                            });
                        });
                        
                        // Thử tìm button có text liên quan
                        for (const btn of allButtons) {
                            const text = btn.textContent?.toLowerCase() || '';
                            if (text.includes('start') || text.includes('create') || text.includes('get started')) {
                                console.log('Clicking button with text:', btn.textContent);
                                btn.click();
                                found = true;
                                break;
                            }
                        }
                    }
                    
                    if (!found) {
                        console.log('No suitable button found, trying parent elements...');
                        // Thử tìm trong các tab hoặc container
                        const tabButtons = document.querySelectorAll('[role="tab"], .tab-nav button, .gradio-tabs button');
                        tabButtons.forEach((btn, index) => {
                            console.log(`Tab button ${index}:`, btn.textContent?.trim());
                        });
                    }
                }, 100);
            }
            
            // Đặt function vào window object để chắc chắn
            window.scrollToSection = scrollToSection;
            window.triggerStartBtn = triggerStartBtn;
            
            // Navbar scroll effect
            window.addEventListener('scroll', () => {
                const navbar = document.querySelector('nav');
                if (navbar) {
                    if (window.scrollY > 100) {
                        navbar.style.background = 'rgba(255, 255, 255, 0.98)';
                        navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.1)';
                    } else {
                        navbar.style.background = 'rgba(255, 255, 255, 0.95)';
                        navbar.style.boxShadow = '0 1px 3px rgba(0, 0, 0, 0.1)';
                    }
                }
            });
            
            // Video hover effects cho showcase
            document.addEventListener('DOMContentLoaded', function() {
                const showcaseVideos = document.querySelectorAll('#showcase video');
                showcaseVideos.forEach(video => {
                    const card = video.closest('div');
                    if (card) {
                        card.addEventListener('mouseenter', () => {
                            video.play().catch(e => console.log('Video play failed:', e));
                        });
                        
                        card.addEventListener('mouseleave', () => {
                            video.pause();
                            video.currentTime = 0;
                        });
                        
                        card.addEventListener('click', () => {
                            if (video.paused) {
                                video.play().catch(e => console.log('Video play failed:', e));
                            } else {
                                video.pause();
                            }
                        });
                    }
                });
                
                // Log để debug
                console.log('Page loaded, functions available:', {
                    scrollToSection: typeof window.scrollToSection,
                    triggerStartBtn: typeof window.triggerStartBtn
                });
            });
            
            // Listen for custom events
            document.addEventListener('startVideoCreation', function(e) {
                console.log('Custom event received:', e.detail);
            });
            
            // Additional debugging
            console.log('Script loaded successfully');
        </script>
    </body>
    </html>
    """
    
    # Tạo Gradio interface với HTML content
    with gr.Row():
        html_component = gr.HTML(html_content)
    
    # Tạo button ẩn để tích hợp với app chính
    nav_button = gr.Button("Get Started", elem_id="nav_get_started_btn", visible=False)
    
    return nav_button

def custom_home_css():
    """Trả về CSS tùy chỉnh cho Gradio"""
    return """
    /* Ẩn các button kỹ thuật của Gradio nhưng vẫn có thể tương tác */
    #nav_get_started_btn {
        position: absolute !important;
        left: -9999px !important;
        opacity: 0 !important;
        pointer-events: auto !important;
        z-index: -1 !important;
    }
    
    /* Đảm bảo HTML component chiếm toàn bộ không gian */
    .gradio-container {
        max-width: none !important;
        padding: 0 !important;
        margin: 0 !important;
    }
    
    /* Ẩn header và footer mặc định của Gradio */
    .gradio-container > .main > .wrap {
        padding: 0 !important;
    }
    
    /* Responsive cho mobile */
    @media (max-width: 768px) {
        .gradio-container {
            padding: 0 !important;
        }
    }
    """

def home():
    """Hàm tương thích ngược"""
    return "Trang home đã được chuyển đổi sang Gradio"