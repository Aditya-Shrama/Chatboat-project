from gtts import gTTS
import pygame
import os
from datetime import datetime

def text_to_audio(text, speed=1.5):
    tts = gTTS(text=text, lang='hi',tld="co.in", slow=False)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    temp_audio_path = f"audio\emp_audio_{timestamp}.mp3"
    tts.save(temp_audio_path)
    return temp_audio_path

def play_audio(audio_file):
    if os.path.exists(audio_file):
        pygame.mixer.init()
        pygame.mixer.music.load(audio_file)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            pygame.time.Clock().tick(10)
        pygame.mixer.quit()
    else:
        print(f"Error: File '{audio_file}' does not exist.")
