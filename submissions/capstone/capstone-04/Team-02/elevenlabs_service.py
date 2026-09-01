import os
import json
import urllib.request
import urllib.error

CONFIG_PATH = os.path.join(os.path.dirname(__file__), "email_config.json")

POPULAR_VOICES = {
    "Bella (Professional Warm Female)": "hpp4J3VqNfWAUOO0d1Us",
    "Sarah (Mature Confident Female)": "EXAVITQu4vr4xnSDxMaL",
    "Matilda (Knowledgeable Female)": "XrExE9yKIg1WjnnlVkGX",
    "Alice (Clear British Female)": "Xb7hH8MSUJpSbSDYk0k2",
    "Jessica (Bright Warm Female)": "cgSgspJ2msm6clMCkdW9",
    "Lily (Velvety British Female)": "pFZP5JQG7iQjIQuC4Bku",
    "Adam (Executive Deep Male)": "pNInz6obpgDQGcFmaJgB"
}

def get_elevenlabs_config():
    """Reads ElevenLabs API key and voice ID from config or environment."""
    api_key = os.environ.get("ELEVENLABS_API_KEY", "")
    voice_id = os.environ.get("ELEVENLABS_VOICE_ID", "hpp4J3VqNfWAUOO0d1Us")
    
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
                if not api_key:
                    api_key = cfg.get("elevenlabs_api_key", "")
                if cfg.get("elevenlabs_voice_id"):
                    voice_id = cfg.get("elevenlabs_voice_id")
        except Exception:
            pass
            
    return api_key.strip(), voice_id.strip()

def save_elevenlabs_config(api_key="", voice_id="hpp4J3VqNfWAUOO0d1Us"):
    """Saves ElevenLabs configuration to local email_config.json."""
    cfg = {}
    if os.path.exists(CONFIG_PATH):
        try:
            with open(CONFIG_PATH, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except Exception:
            cfg = {}
            
    if api_key:
        cfg["elevenlabs_api_key"] = api_key.strip()
    if voice_id:
        cfg["elevenlabs_voice_id"] = voice_id.strip()
        
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(cfg, f, indent=2)
    print("Saved ElevenLabs configuration successfully!")

def generate_speech_mp3(text, output_file="executive_audio_briefing.mp3", api_key=None, voice_id=None):
    """Generates MP3 audio file using ElevenLabs Text-to-Speech API."""
    cfg_key, cfg_voice = get_elevenlabs_config()
    api_key = api_key or cfg_key
    voice_id = voice_id or cfg_voice
    
    if not api_key:
        print("Error: No ElevenLabs API Key provided. Set ELEVENLABS_API_KEY environment variable or save in email_config.json")
        return False
        
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    
    payload = json.dumps({
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            audio_bytes = resp.read()
            with open(output_file, "wb") as out_f:
                out_f.write(audio_bytes)
            print(f"Success! ElevenLabs MP3 saved to: {output_file}")
            return True
    except urllib.error.HTTPError as e:
        print(f"HTTPError generating speech: {e.code} - {e.read().decode('utf-8')}")
        return False
    except Exception as e:
        print(f"Error generating speech: {str(e)}")
        return False

def generate_speech_b64(text, api_key=None, voice_id=None):
    """Generates speech and returns base64 string."""
    import base64
    cfg_key, cfg_voice = get_elevenlabs_config()
    api_key = api_key or cfg_key
    voice_id = voice_id or cfg_voice
    
    if not api_key:
        return None
        
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    payload = json.dumps({
        "text": text,
        "model_id": "eleven_multilingual_v2",
        "voice_settings": {
            "stability": 0.5,
            "similarity_boost": 0.75
        }
    }).encode("utf-8")
    
    req = urllib.request.Request(
        url,
        data=payload,
        headers={
            "Accept": "audio/mpeg",
            "Content-Type": "application/json",
            "xi-api-key": api_key
        },
        method="POST"
    )
    
    try:
        with urllib.request.urlopen(req) as resp:
            audio_bytes = resp.read()
            return base64.b64encode(audio_bytes).decode("utf-8")
    except Exception as e:
        print(f"Error generating speech b64: {e}")
        return None

if __name__ == "__main__":
    key, voice = get_elevenlabs_config()
    print(f"ElevenLabs Service Loaded. Key configured: {bool(key)}, Voice ID: {voice}")

