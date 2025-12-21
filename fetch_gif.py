import os
import re
import subprocess
from PIL import Image

# ------------------------------------------
# SETTINGS
# ------------------------------------------
FRAME_DURATION = 250  # ms per frame
VISEME_DIR = "visemes"
OUTPUT_DIR = "output"

MULTI_PHONEMES = ["tʃ", "dʒ", "aɪ", "ɔɪ", "aʊ"]

# ------------------------------------------
VISEME_MAP = {
    0: set([""]),
    1: set(["æ", "ə", "ʌ"]),
    2: set(["ɑ"]),
    3: set(["ɔ"]),
    4: set(["ɛ", "ʊ"]),
    5: set(["ɝ"]),
    6: set(["j", "i", "ɪ"]),
    7: set(["w", "u"]),
    8: set(["o"]),
    9: set(["aʊ"]),
    10: set(["ɔɪ"]),
    11: set(["aɪ"]),
    12: set(["h"]),
    13: set(["ɹ"]),
    14: set(["l"]),
    15: set(["s", "z"]),
    16: set(["ʃ", "tʃ", "dʒ", "ʒ"]),
    17: set(["ð"]),
    18: set(["f", "v"]),
    19: set(["d", "t", "n", "θ"]),
    20: set(["k", "g", "ŋ"]),
    21: set(["p", "b", "m"]),
}

# ------------------------------------------
def clean_ipa(t):
    return t.replace("ˈ", "").replace("ˌ", "").replace("ː", "").strip()

def viseme_for_phoneme(ph):
    for vid, s in VISEME_MAP.items():
        if ph in s:
            return vid
    return 0

def ipa_to_visemes(ipa):
    ipa = clean_ipa(ipa)
    out = []
    i = 0
    while i < len(ipa):
        for m in MULTI_PHONEMES:
            if ipa[i:].startswith(m):
                out.append(viseme_for_phoneme(m))
                i += len(m)
                break
        else:
            if ipa[i] not in " ,.|‖":
                out.append(viseme_for_phoneme(ipa[i]))
            i += 1
    return out

def phonemes_for_word(word):
    r = subprocess.run(
        ["espeak-ng", "-q", "--ipa=3", "--pho", word],
        stdout=subprocess.PIPE,
        text=True,
        encoding="utf-8",
    )
    return clean_ipa(re.sub(r"\s+", " ", r.stdout))

def load_viseme_images():
    imgs = {}
    for vid in VISEME_MAP:
        p = os.path.join(VISEME_DIR, f"{vid}.png")
        if os.path.exists(p):
            imgs[vid] = Image.open(p).convert("RGBA")
    return imgs

# ------------------------------------------
def create_gif(word, visemes, images):
    frames = [images[0]]
    frames += [images.get(v, images[0]) for v in visemes]
    frames.append(images[0])

    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, f"{word}.gif")

    frames[0].save(
        out,
        save_all=True,
        append_images=frames[1:],
        duration=FRAME_DURATION,
        loop=0
    )

    print(f"[OK] Fixed-timing GIF: {out}")

# ------------------------------------------
def main():
    import sys
    if len(sys.argv) < 2:
        print("Usage: python generate_gif_no_audio.py words.txt")
        return

    with open(sys.argv[1], encoding="utf-8") as f:
        words = [w.strip().lower() for w in f if w.strip()]

    images = load_viseme_images()

    for word in words:
        ipa = phonemes_for_word(word)
        visemes = ipa_to_visemes(ipa)
        create_gif(word, visemes, images)

if __name__ == "__main__":
    main()
