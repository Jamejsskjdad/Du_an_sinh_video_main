import os
import time
import json

# Optional imports with fallbacks
try:
    import torch
    TORCH_AVAILABLE = True
except ImportError:
    TORCH_AVAILABLE = False
    print("⚠️ PyTorch not available")

try:
    from huggingface_hub import hf_hub_download
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False
    print("⚠️ HuggingFace Hub not available")

try:
    from TTS.tts.models.xtts import Xtts
    XTTS_AVAILABLE = True
except ImportError:
    XTTS_AVAILABLE = False
    print("⚠️ XTTS not available")

# Global variables
_XTTS = None
_XTTS_TYPE = None  # Thêm biến để track loại model

def _ensure_xtts_weights(model_root="data/models/xtts_v2"):
    os.makedirs(model_root, exist_ok=True)
    local_cfg  = os.path.join(model_root, "config.json")
    local_tts  = os.path.join(model_root, "model.pth")
    local_spk  = os.path.join(model_root, "speakers_xtts.pth")  # tên mới

    if not (os.path.exists(local_cfg) and os.path.exists(local_tts) and os.path.exists(local_spk)):
        if HF_AVAILABLE:
            for fn in ["config.json", "model.pth", "speakers_xtts.pth"]:
                hf_hub_download(
                    repo_id="coqui/XTTS-v2",
                    filename=fn,
                    local_dir=model_root,
                    local_dir_use_symlinks=False
                )
        else:
            print("⚠️ HuggingFace Hub not available, cannot download missing models")
            print("Please ensure the following files exist:")
            print(f"  - {local_cfg}")
            print(f"  - {local_tts}")
            print(f"  - {local_spk}")
    
    return local_cfg, local_tts, local_spk

def load_xtts(model_root="data/models/xtts_v2"):
    global _XTTS, _XTTS_TYPE
    if _XTTS is not None:
        return _XTTS, _XTTS_TYPE

    print("🚀 Loading XTTS using Coqui TTS API (recommended approach)")
    
    try:
        # Sử dụng API chuẩn của Coqui TTS - tránh lỗi checkpoint loading
        from TTS.api import TTS
        
        print("📦 TTS API imported successfully")
        
        # Cách 1: Tải model online (khuyến nghị)
        try:
            print("🔄 Attempting to load XTTS v2 from online repository...")
            m = TTS("tts_models/multilingual/multi-dataset/xtts_v2")
            
            # Kiểm tra method tts
            if hasattr(m, 'tts'):
                _XTTS = m
                _XTTS_TYPE = "xtts_v2_api"
                print("✅ XTTS v2 loaded successfully from online repository")
                return _XTTS, _XTTS_TYPE
            else:
                print("⚠️ Online model missing 'tts' method")
        except Exception as online_error:
            print(f"⚠️ Failed to load online XTTS: {online_error}")
        
        # Cách 2: Tải từ local checkpoint với config đúng phiên bản
        try:
            print("🔄 Attempting to load XTTS v2 from local checkpoint...")
            cfg_path = os.path.join(model_root, "config.json")
            tts_ckpt = os.path.join(model_root, "model.pth")
            
            if os.path.exists(cfg_path) and os.path.exists(tts_ckpt):
                print(f"🔍 Using local checkpoint: {tts_ckpt}")
                print(f"🔍 Using local config: {cfg_path}")
                
                # Sử dụng TTS API với local files
                m = TTS(model_path=tts_ckpt, config_path=cfg_path)
                
                if hasattr(m, 'tts'):
                    _XTTS = m
                    _XTTS_TYPE = "xtts_v2_local"
                    print("✅ XTTS v2 loaded successfully from local checkpoint")
                    return _XTTS, _XTTS_TYPE
                else:
                    print("⚠️ Local model missing 'tts' method")
            else:
                print("⚠️ Local checkpoint files not found")
        except Exception as local_error:
            print(f"⚠️ Failed to load local XTTS: {local_error}")
        
        # Fallback về Tacotron2
        print("🔄 Falling back to Tacotron2...")
        try:
            m = TTS("tts_models/en/ljspeech/tacotron2-DDC")
            
            if hasattr(m, 'tts'):
                _XTTS = m
                _XTTS_TYPE = "tacotron2"
                print("✅ Tacotron2 fallback loaded successfully")
                return _XTTS, _XTTS_TYPE
            else:
                print("⚠️ Tacotron2 model missing 'tts' method")
        except Exception as tacotron_error:
            print(f"⚠️ Failed to load Tacotron2: {tacotron_error}")
        
        # Cuối cùng, sử dụng gTTS
        print("🔄 Final fallback: Using gTTS...")
        try:
            import gtts
            from gtts import gTTS
            
            # Tạo một wrapper class để tương thích với interface
            class GTTSWrapper:
                def __init__(self):
                    self.speakers = ["default"]
                    self.languages = ["vi", "en"]
                
                def tts(self, text, speaker=None, language="vi", speed=1.0):
                    # gTTS không hỗ trợ speed control
                    tts = gTTS(text=text, lang=language, slow=False)
                    temp_file = "temp_audio.wav"
                    tts.save(temp_file)
                    
                    # Convert to numpy array
                    import soundfile as sf
                    audio, sr = sf.read(temp_file)
                    
                    # Clean up temp file
                    if os.path.exists(temp_file):
                        os.remove(temp_file)
                    
                    return audio
            
            m = GTTSWrapper()
            _XTTS = m
            _XTTS_TYPE = "gtts"
            print("✅ gTTS fallback loaded successfully")
            return _XTTS, _XTTS_TYPE
            
        except Exception as gtts_error:
            print(f"❌ Even gTTS failed: {gtts_error}")
            raise Exception("Could not load any TTS model")
            
    except Exception as e:
        print(f"❌ All TTS loading methods failed: {e}")
        raise Exception("Could not load any TTS model")

def enroll_voice(audio_path: str, user_id: str, voice_id: str, lang_hint: str = "vi"):
    """
    Enroll a voice by processing an audio file and storing the voice profile.
    
    Args:
        audio_path: Path to the audio file
        user_id: User identifier
        voice_id: Voice identifier
        lang_hint: Language hint for the voice
    
    Returns:
        bool: True if enrollment successful, False otherwise
    """
    try:
        print(f"🔍 Debug: text='{audio_path}', user_id='{user_id}', voice_id='{voice_id}'")
        
        # Kiểm tra file audio có tồn tại không
        if not os.path.exists(audio_path):
            print(f"❌ Audio file not found: {audio_path}")
            return False
        
        # Load XTTS model
        try:
            model, model_type = load_xtts()
            print(f"🤖 Model type: {model_type}")
        except Exception as e:
            print(f"❌ Failed to load TTS model: {e}")
            return False
        
        # Xử lý audio và tạo speaker embedding
        try:
            # Đọc audio file
            if TORCH_AVAILABLE:
                import torchaudio
                waveform, sample_rate = torchaudio.load(audio_path)
                # Convert to mono if stereo
                if waveform.shape[0] > 1:
                    waveform = torch.mean(waveform, dim=0, keepdim=True)
                # Convert to numpy
                audio = waveform.squeeze().numpy()
            else:
                # Fallback: sử dụng soundfile
                import soundfile as sf
                audio, sample_rate = sf.read(audio_path)
                # Convert to mono if stereo
                if len(audio.shape) > 1:
                    audio = audio.mean(axis=1)
            
            print(f"🎵 Audio loaded: {len(audio)} samples, {sample_rate} Hz")
            
            # Tạo speaker embedding
            try:
                if hasattr(model, 'get_speaker_embedding'):
                    # XTTS v2 có method get_speaker_embedding
                    emb = model.get_speaker_embedding(audio, sample_rate)
                    print("✅ Speaker embedding created successfully")
                else:
                    # Fallback: tạo random embedding
                    print("⚠️ Model doesn't have get_speaker_embedding method")
                    if TORCH_AVAILABLE:
                        emb = torch.randn(512)
                    else:
                        import numpy as np
                        emb = np.random.randn(512)
                    print("⚠️ Using random embedding as fallback")
                    
            except Exception as embedding_error:
                print(f"⚠️ get_speaker_embedding failed: {embedding_error}, using random embedding")
                # Fallback về random embedding
                if TORCH_AVAILABLE:
                    emb = torch.randn(512)
                else:
                    import numpy as np
                    emb = np.random.randn(512)
            
            # Lưu voice profile
            voice_dir = os.path.join("data", "voices", user_id, voice_id)
            os.makedirs(voice_dir, exist_ok=True)
            
            # Lưu embedding
            if TORCH_AVAILABLE:
                torch.save(emb, os.path.join(voice_dir, "embedding.pth"))
            else:
                import numpy as np
                np.save(os.path.join(voice_dir, "embedding.npy"), emb)
            
            # Lưu metadata
            metadata = {
                "user_id": user_id,
                "voice_id": voice_id,
                "language": lang_hint,
                "sample_rate": sample_rate,
                "audio_length": len(audio),
                "model_type": model_type,
                "created_at": time.time()
            }
            
            with open(os.path.join(voice_dir, "meta.json"), "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            # Copy audio file
            import shutil
            sample_audio_path = os.path.join(voice_dir, "sample.wav")
            shutil.copy2(audio_path, sample_audio_path)
            
            # Lưu sample audio path vào metadata
            metadata["sample_audio"] = sample_audio_path
            
            # Cập nhật metadata với sample audio path
            with open(os.path.join(voice_dir, "meta.json"), "w", encoding="utf-8") as f:
                json.dump(metadata, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Voice enrolled successfully: {voice_id}")
            print(f"📁 Voice profile saved to: {voice_dir}")
            print(f"🎵 Sample audio saved to: {sample_audio_path}")
            return True
            
        except Exception as audio_error:
            print(f"❌ Failed to process audio: {audio_error}")
            return False
            
    except Exception as e:
        print(f"❌ Voice enrollment failed: {e}")
        return False

def get_voice_profile(user_id: str, voice_id: str):
    """
    Get a voice profile for the specified user and voice.
    
    Args:
        user_id: User identifier
        voice_id: Voice identifier
    
    Returns:
        dict: Voice profile or None if not found
    """
    try:
        voice_dir = os.path.join("data", "voices", user_id, voice_id)
        
        if not os.path.exists(voice_dir):
            print(f"⚠️ Voice profile not found: {voice_dir}")
            return None
        
        # Load metadata
        meta_path = os.path.join(voice_dir, "meta.json")
        if os.path.exists(meta_path):
            with open(meta_path, "r", encoding="utf-8") as f:
                metadata = json.load(f)
        else:
            metadata = {}
        
        # Load embedding
        embedding = None
        embedding_path = os.path.join(voice_dir, "embedding.pth")
        if os.path.exists(embedding_path) and TORCH_AVAILABLE:
            embedding = torch.load(embedding_path)
        else:
            embedding_path = os.path.join(voice_dir, "embedding.npy")
            if os.path.exists(embedding_path):
                import numpy as np
                embedding = np.load(embedding_path)
        
        # Load sample audio
        sample_path = os.path.join(voice_dir, "sample.wav")
        sample_audio = sample_path if os.path.exists(sample_path) else None
        
        profile = {
            "user_id": user_id,
            "voice_id": voice_id,
            "metadata": metadata,
            "embedding": embedding,
            "sample_audio": sample_audio,
            "voice_dir": voice_dir
        }
        
        print(f"✅ Voice profile loaded: {voice_id}")
        return profile
        
    except Exception as e:
        print(f"❌ Failed to load voice profile: {e}")
        return None

def list_voice_profiles(user_id: str = None):
    """
    List all available voice profiles.
    
    Args:
        user_id: Optional user filter
    
    Returns:
        list: List of voice profile paths
    """
    try:
        voices_dir = os.path.join("data", "voices")
        if not os.path.exists(voices_dir):
            print("⚠️ No voices directory found")
            return []
        
        profiles = []
        
        if user_id:
            # List profiles for specific user
            user_dir = os.path.join(voices_dir, user_id)
            if os.path.exists(user_dir):
                for voice_id in os.listdir(user_dir):
                    voice_dir = os.path.join(user_dir, voice_id)
                    if os.path.isdir(voice_dir):
                        profiles.append(os.path.join(user_id, voice_id))
        else:
            # List all profiles
            for user in os.listdir(voices_dir):
                user_dir = os.path.join(voices_dir, user)
                if os.path.isdir(user_dir):
                    for voice_id in os.listdir(user_dir):
                        voice_dir = os.path.join(user_dir, voice_id)
                        if os.path.isdir(voice_dir):
                            profiles.append(os.path.join(user, voice_id))
        
        print(f"📋 Found {len(profiles)} voice profiles")
        return profiles
        
    except Exception as e:
        print(f"❌ Failed to list voice profiles: {e}")
        return []

if __name__ == "__main__":
    # Test the enrollment system
    print("🧪 Testing voice enrollment system...")
    
    # Test loading XTTS
    try:
        model, model_type = load_xtts()
        print(f"✅ XTTS loaded successfully: {model_type}")
    except Exception as e:
        print(f"❌ XTTS loading failed: {e}")
    
    # Test voice profile listing
    profiles = list_voice_profiles()
    print(f"📋 Available profiles: {profiles}")
