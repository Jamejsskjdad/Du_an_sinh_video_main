import soundfile as sf, torch
import os
from .store import load_profile
from .enrollment import load_xtts

def synthesize(text: str, user_id: str, voice_id: str,
               lang: str = "vi", speed: float = 1.0,
               out_path: str = "data/tmp/voice_out.wav"):
    
    # Language handling for XTTS compatibility
    def get_xtts_language(lang_code):
        """Get XTTS language - XTTS không support tiếng Việt nên dùng English"""
        if lang_code.lower() in ['vi', 'vi-vn']:
            # XTTS không support tiếng Việt, dùng English để giữ giọng clone
            print(f"🌐 XTTS không support tiếng Việt, dùng English để giữ giọng clone")
            return 'en'
        else:
            # Các ngôn ngữ khác giữ nguyên
            return lang_code.lower()
    
    # Get XTTS language - XTTS dùng English, gTTS dùng tiếng Việt
    xtts_lang = get_xtts_language(lang)
    print(f"🌐 Language for XTTS: {xtts_lang} (XTTS dùng English, gTTS dùng {lang})")
    try:
        # Tạo thư mục output nếu chưa tồn tại
        os.makedirs(os.path.dirname(out_path), exist_ok=True)
        
        model, model_type = load_xtts()
        emb, meta = load_profile(user_id, voice_id)
        
        # Kiểm tra loại model để quyết định cách synthesize
        if model_type in ["xtts_v2", "xtts_v2_api"]:
            # XTTS v2 có thể sử dụng speaker_embedding
            print(f"🎤 {model_type}: Synthesizing with speaker embedding")
            
            # Kiểm tra xem model có method tts không
            if not hasattr(model, 'tts'):
                print("❌ Model doesn't have 'tts' method - checkpoint loading may have failed")
                print("🔄 Falling back to gTTS...")
                # Fallback về gTTS
                try:
                    from gtts import gTTS
                    import tempfile
                    
                    # Tạo file tạm
                    temp_file = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
                    temp_path = temp_file.name
                    temp_file.close()
                    
                    # Sử dụng gTTS
                    tts = gTTS(text=text, lang=lang, slow=False)
                    tts.save(temp_path)
                    
                    # Convert to numpy array
                    audio, sr = sf.read(temp_path)
                    
                    # Clean up
                    os.unlink(temp_path)
                    
                    wav = audio
                    print("✅ gTTS fallback successful")
                    
                except Exception as gtts_error:
                    print(f"❌ gTTS fallback also failed: {gtts_error}")
                    return None
            else:
                # Thử các phương pháp TTS khác nhau
                wav = None
                
                # Method 1: Speaker embedding với speaker parameter
                if emb is not None:
                    try:
                        print("🔄 Trying speaker embedding with speaker parameter...")
                        # XTTS cần speaker ID đúng format, thử với 'speaker' parameter
                        wav = model.tts(text=text, speaker=voice_id, speaker_embedding=emb,
                                        language=xtts_lang, speed=speed)
                        if wav is not None:
                            print("✅ Speaker embedding with speaker parameter successful")
                        else:
                            print("⚠️ Speaker embedding with speaker parameter failed: 'myVoice'")
                    except Exception as e:
                        print(f"⚠️ Speaker embedding with speaker parameter failed: {e}")
                
                # Method 2: Speaker parameter trực tiếp (thử với speaker ID khác)
                if wav is None:
                    try:
                        print(f"🔄 Trying with speaker parameter: {voice_id}")
                        # Thử với speaker ID khác nếu có
                        wav = model.tts(text=text, speaker=voice_id, language=xtts_lang, speed=speed)
                        if wav is not None:
                            print("✅ Speaker parameter successful")
                        else:
                            print("⚠️ Speaker parameter failed: 'myVoice'")
                    except Exception as e:
                        print(f"⚠️ Speaker parameter failed: {e}")
                
                # Method 3: Speaker_wav từ voice profile
                if wav is None:
                    try:
                        sample_audio_path = meta.get('sample_audio')
                        if sample_audio_path and os.path.exists(sample_audio_path):
                            print(f"🔄 Trying speaker_wav: {sample_audio_path}")
                            # Convert sample audio to 16kHz mono if needed
                            try:
                                import subprocess
                                temp_16k_path = sample_audio_path.replace('.wav', '_16k_mono.wav')
                                
                                # Use FFmpeg to convert to 16kHz mono
                                cmd = [
                                    'ffmpeg', '-y',
                                    '-i', sample_audio_path,
                                    '-ac', '1',  # Mono
                                    '-ar', '16000',  # 16kHz
                                    '-sample_fmt', 's16',  # 16-bit PCM
                                    temp_16k_path
                                ]
                                
                                result = subprocess.run(cmd, capture_output=True, text=True)
                                
                                if result.returncode == 0 and os.path.exists(temp_16k_path):
                                    print(f"🔧 Converted sample audio to 16kHz mono: {temp_16k_path}")
                                    wav = model.tts(text=text, speaker_wav=temp_16k_path, language=xtts_lang, speed=speed)
                                    # Clean up temp file
                                    try:
                                        os.unlink(temp_16k_path)
                                    except:
                                        pass
                                else:
                                    print(f"⚠️ Sample audio conversion failed, using original")
                                    wav = model.tts(text=text, speaker_wav=sample_audio_path, language=xtts_lang, speed=speed)
                                    
                            except Exception as convert_error:
                                print(f"⚠️ Sample audio conversion failed: {convert_error}, using original")
                                wav = model.tts(text=text, speaker_wav=sample_audio_path, language=xtts_lang, speed=speed)
                            
                            if wav is not None:
                                print("✅ Speaker_wav successful")
                        else:
                            print("⚠️ No sample audio found in voice profile")
                            print(f"🔍 Available metadata keys: {list(meta.keys()) if meta else 'None'}")
                    except Exception as e:
                        print(f"⚠️ Speaker_wav failed: {e}")
                        import traceback
                        traceback.print_exc()
                
                # Method 4: Không có speaker (default voice)
                if wav is None:
                    try:
                        print("🔄 Trying without speaker...")
                        wav = model.tts(text=text, language=xtts_lang, speed=speed)
                        if wav is not None:
                            print("✅ Default voice successful")
                    except Exception as e:
                        print(f"⚠️ Default voice failed: {e}")
                
                # Method 5: Fallback về gTTS với format chuẩn PCM 16-bit
                if wav is None:
                    print("🔄 All XTTS methods failed, falling back to gTTS with PCM 16-bit format...")
                    try:
                        from gtts import gTTS
                        import tempfile
                        import subprocess
                        
                        # Tạo file tạm MP3 trước
                        with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as temp_file:
                            temp_mp3 = temp_file.name
                        
                        # Sử dụng gTTS để tạo MP3 với language gốc (tiếng Việt)
                        print(f"🎤 gTTS fallback: Sử dụng language '{lang}' để giữ tiếng Việt")
                        tts = gTTS(text=text, lang=lang, slow=False)
                        tts.save(temp_mp3)
                        
                        # Convert MP3 sang WAV 16kHz mono PCM s16 với padding
                        temp_wav = temp_mp3.replace('.mp3', '_16k_mono_pcm.wav')
                        
                        try:
                            # Sử dụng FFmpeg để convert format chuẩn PCM 16-bit
                            cmd = [
                                'ffmpeg', '-y',
                                '-i', temp_mp3,
                                '-ac', '1',  # Mono
                                '-ar', '16000',  # 16kHz
                                '-sample_fmt', 's16',  # 16-bit PCM (không phải float)
                                '-af', 'apad=pad_dur=0.5',  # Pad 0.5s để đủ frame
                                '-f', 'wav',  # Ép format WAV
                                temp_wav
                            ]
                            
                            print(f"🔄 Converting to PCM 16-bit format: {' '.join(cmd)}")
                            result = subprocess.run(cmd, capture_output=True, text=True)
                            
                            if result.returncode == 0 and os.path.exists(temp_wav):
                                # Đọc WAV đã convert
                                audio, sr = sf.read(temp_wav)
                                wav = audio
                                print("✅ gTTS fallback with PCM 16-bit format successful")
                                print(f"🔧 Audio format: {sr}Hz, {len(audio)} samples, mono, PCM 16-bit")
                                
                                # Verify audio format
                                if sr == 16000 and len(audio.shape) == 1:
                                    print("✅ Audio format verified: 16kHz mono")
                                else:
                                    print(f"⚠️ Audio format mismatch: {sr}Hz, shape: {audio.shape}")
                                
                            else:
                                # Fallback nếu FFmpeg thất bại
                                print(f"⚠️ FFmpeg conversion failed: {result.stderr}")
                                print("🔄 Falling back to direct MP3 reading")
                                audio, sr = sf.read(temp_mp3)
                                wav = audio
                                print("✅ gTTS fallback successful (MP3 format)")
                        
                        except Exception as convert_error:
                            print(f"⚠️ Format conversion failed: {convert_error}")
                            # Fallback về đọc MP3 trực tiếp
                            audio, sr = sf.read(temp_mp3)
                            wav = audio
                            print("✅ gTTS fallback successful (MP3 format)")
                        
                        # Clean up
                        try:
                            os.unlink(temp_mp3)
                            if os.path.exists(temp_wav):
                                os.unlink(temp_wav)
                        except:
                            pass
                        
                    except Exception as gtts_error:
                        print(f"❌ Even gTTS failed: {gtts_error}")
                        return None
                
        elif model_type == "gtts":
            # gTTS wrapper
            print("🎤 gTTS: Synthesizing with language hint")
            wav = model.tts(text=text, language=lang, speed=speed)
            
        else:
            # Tacotron2 hoặc model khác
            print(f"Warning: Using {model_type} model. Voice cloning not available.")
            try:
                # Thử với language parameter
                wav = model.tts(text=text, speaker=model.speakers[0] if hasattr(model, 'speakers') else None,
                                language=lang)
            except Exception as e:
                print(f"⚠️ Language parameter failed, trying without: {e}")
                # Thử không có language parameter
                wav = model.tts(text=text, speaker=model.speakers[0] if hasattr(model, 'speakers') else None)
        
        if wav is None:
            print("❌ TTS returned None")
            return None
            
        sf.write(out_path, wav, 24000)
        print(f"✅ Audio saved to: {out_path}")
        return out_path
        
    except Exception as e:
        print(f"❌ Error in synthesize: {str(e)}")
        return None
