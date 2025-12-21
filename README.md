Scripts for creating gifs like Google pronounciation animations using espeak.

# Requirements

```bash
pip install gtts pydub pillow
```

**espeak-ng**:
- **Linux**
  ```bash
  sudo apt install espeak-ng
  ```
- **macOS**
  ```bash
  brew install espeak-ng
  ```
- **Windows**
  
    https://github.com/espeak-ng/espeak-ng/releases

---

# Usage

##  `fetch_audio.py`
Creates a .mp3 file for each word in the words.txt
```bash
python fetch_audio.py words.txt
```
##  `fetch_gif.py`
Creates pronounciation gifs for each word in words.txt with a fixed frame duration.
```bash
python fetch_gif.py words.txt
```
##  `fetch_gif_synced.py`
Creates pronounciation gifs for each word in words.txt using .mp3 durations created by fetch_audio. 
```bash
python fetch_gif_synced.py words.txt
```
