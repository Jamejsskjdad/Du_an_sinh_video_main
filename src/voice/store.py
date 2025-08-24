from pathlib import Path
import json, numpy as np, time
from typing import Optional

ROOT = Path("data/voices")

def voice_dir(user_id: str, voice_id: str) -> Path:
    return ROOT/str(user_id)/voice_id

def save_profile(user_id: str, voice_id: str, embedding: np.ndarray, meta: dict):
    d = voice_dir(user_id, voice_id)
    d.mkdir(parents=True, exist_ok=True)
    np.save(d/"embedding.npy", embedding)
    with open(d/"meta.json", "w", encoding="utf-8") as f:
        json.dump(meta, f, ensure_ascii=False, indent=2)

def load_profile(user_id: str, voice_id: str):
    d = voice_dir(user_id, voice_id)
    emb = np.load(d/"embedding.npy")
    with open(d/"meta.json","r",encoding="utf-8") as f:
        meta = json.load(f)
    return emb, meta

def list_voices(user_id: Optional[str] = None):
    out = []
    bases = [ROOT/str(user_id)] if user_id else [p for p in ROOT.glob("*") if p.is_dir()]
    for base in bases:
        if not base.exists(): continue
        for vid in base.iterdir():
            mpath = vid/"meta.json"
            if mpath.exists():
                with open(mpath,"r",encoding="utf-8") as f:
                    out.append(json.load(f))
    return sorted(out, key=lambda m: m.get("created_at", 0), reverse=True)

def has_voice(user_id: str, voice_id: str) -> bool:
    d = voice_dir(user_id, voice_id)
    return (d/"embedding.npy").exists() and (d/"meta.json").exists()
