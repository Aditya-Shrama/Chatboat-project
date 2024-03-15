from dotenv import load_dotenv
import base64

import elevenlabs


elevenlabs_api_key = 'a2a3e5ff57a8af84d1ca905143618598'
elevenlabs.set_api_key(elevenlabs_api_key)

def text_to_speech(input_text, voice="Veda", settings=None):
    # Use Eleven Labs API for text-to-speech
    if settings:
        audio_data = elevenlabs.generate(input_text, voice=voice, settings=settings)
    else:
        audio_data = elevenlabs.generate(input_text, voice=voice)
    
    # Save the audio file
    webm_file_path = "temp_audio_play.mp3"
    with open(webm_file_path, "wb") as f:
        f.write(audio_data)
    
    return webm_file_path
def autoplay_audio(file_path: str):
    with open(file_path, "rb") as f:
        data = f.read()
    b64 = base64.b64encode(data).decode("utf-8")
    md = f"""
    <audio autoplay>
    <source src="data:audio/mp3;base64,{b64}" type="audio/mp3">
    </audio>
    """
    st.markdown(md, unsafe_allow_html=True)
    
text = " main tumhara education bot hoon. Kya tumhe koi sawaal hai ya phir hum padhna shuru karein?"

text_to_speech(text)