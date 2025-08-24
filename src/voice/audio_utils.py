import librosa, soundfile as sf
try:
    import pyloudnorm as pyln
except Exception:
    pyln = None

def preprocess_audio(in_path: str, out_path: str, sr: int = 24000):
    # Load mono + resample
    y, _ = librosa.load(in_path, sr=sr, mono=True)
    # Trim im lặng
    y, _ = librosa.effects.trim(y, top_db=30)
    # (Tuỳ chọn) Chuẩn hoá loudness về ~-16 LUFS
    if pyln is not None and len(y) > 0:
        meter = pyln.Meter(sr)
        loudness = meter.integrated_loudness(y)
        y = pyln.normalize.loudness(y, loudness, -16.0)
    sf.write(out_path, y, sr)
    dur = len(y)/sr if sr else 0.0
    return out_path, sr, dur
