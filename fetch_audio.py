import os
import sys
from gtts import gTTS

# ------------------------------------------
# SETTINGS
# ------------------------------------------
VOICE_LANG = "en-GB"
AUDIO_DIR = "audio"

# ------------------------------------------
# GENERATE TTS AUDIO
# ------------------------------------------
def generate_audio(word):
    os.makedirs(AUDIO_DIR, exist_ok=True)
    audio_path = os.path.join(AUDIO_DIR, f"{word}.mp3")

    if os.path.exists(audio_path):
        print(f"[SKIP] Audio exists: {audio_path}")
        return audio_path

    tts = gTTS(text=word, lang=VOICE_LANG, tld="co.uk")
    tts.save(audio_path)
    print(f"[OK] Audio saved: {audio_path}")
    return audio_path

# ------------------------------------------
# MAIN
# ------------------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_audio.py words.txt")
        return

    with open(sys.argv[1], "r", encoding="utf-8") as f:
        words = [w.strip().lower() for w in f if w.strip()]

    for word in words:
        generate_audio(word)

if __name__ == "__main__":
    main()
