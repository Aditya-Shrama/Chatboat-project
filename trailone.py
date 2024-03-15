import streamlit as st    
from gtts import gTTS
import os
import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import content_generator as cg
import audio_maker as AM
import speech_recognition as sr
import random

# Define database connection and session
engine = create_engine('sqlite:///user_profiles.db', echo=True)
Base = declarative_base()

class UserProfile(Base):
    __tablename__ = 'user_profiles'

    id = Column(Integer, primary_key=True)
    username = Column(String)
    favorite_topics = Column(String)
    learning_history = Column(String)

Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)

def create_user_profile(username):
    session = Session()
    new_profile = UserProfile(username=username)
    session.add(new_profile)
    session.commit()
    session.close()

def get_user_profile(username):
    session = Session()
    profile = session.query(UserProfile).filter_by(username=username).first()
    session.close()
    return profile

def update_favorite_topics(username, topics):
    session = Session()
    profile = session.query(UserProfile).filter_by(username=username).first()
    profile.favorite_topics = topics
    session.commit()
    session.close()

def update_learning_history(username, history):
    session = Session()
    profile = session.query(UserProfile).filter_by(username=username).first()
    profile.learning_history = history
    session.commit()
    session.close()

topics = ["Introduction to the importance of water conservation","Understanding the factors affecting the speed and direction of an object in motion","Introduction to different types of materials used in construction"]
true_false_questions = {
    "0": {
        "question": "Water covers most of the Earth's surface, so there is no need to conserve it",
        "answer": "false"
    },
    "1": {
        "question": "An object in motion will stay in motion forever unless acted upon by a force.",
        "answer": "true"
    },
    "2": {
        "question": "Steel is the strongest and most durable construction material.",
        "answer": "false"
    },
    # Add more questions as needed...
}

# Function for multiple-choice question
def multiple_choice_question(question, choices, correct_answer):
    st.write(question)
    user_answer = st.radio("Choose the correct answer:", choices)
    if user_answer.lower() == correct_answer.lower():
        st.write("Correct!")
    else:
        st.write("Incorrect!")

# Function for fill-in-the-blank exercise
def fill_in_the_blank_question(question, correct_answer):
    user_answer = st.text_input("Fill in the blank:")
    if user_answer.lower() == correct_answer.lower():
        st.write("Correct!")
    else:
        st.write("Incorrect!")

# Function for coding challenge (example: simple addition)
def coding_challenge():
    num1 = random.randint(1, 10)
    num2 = random.randint(1, 10)
    answer = num1 + num2
    user_answer = st.number_input(f"What is the result of {num1} + {num2}?", min_value=0, max_value=20)
    if user_answer == answer:
        st.write("Correct!")
    else:
        st.write("Incorrect!")

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        st.write("Listening...")
        audio = recognizer.listen(source)
    try:
        user_input = recognizer.recognize_google(audio)
        st.write(f"User input: {user_input}")
        return user_input
    except sr.UnknownValueError:
        print("Sorry, I could not understand what you said.")
        return None
    except sr.RequestError:
        print("Sorry, unable to access Google Speech Recognition service.")
        return None

def main():
    st.set_page_config("voice_chat_trainer")
    username = "student"

    # Check if user profile exists, if not, create one
    profile = get_user_profile(username)
    if not profile:
        create_user_profile(username)
        st.write("Welcome, new user!")

    Greet = f"Hey {username} main tumhara education bot hoon. Kya tumhe koi sawaal hai ya phir hum padhna shuru karein?"
    temp_audio_path = AM.text_to_audio(Greet)
    print(temp_audio_path)
    st.write(Greet + "\n - Question or Doubt \n - Start Learning-")
    AM.play_audio(temp_audio_path)

    while True:
        user_input = recognize_speech()
        if user_input:
            if "question" in user_input.lower() or "doubt" in user_input.lower():
                AM.play_audio(AM.text_to_audio("say"))
                question = recognize_speech()
                answer = cg.get_answer(question)
                small_answer = cg.small_answer(answer)
                temp_audio_path = AM.text_to_audio(small_answer + "Read the given explanation then we go forward.")
                print(temp_audio_path)
                st.write(answer)
                AM.play_audio(temp_audio_path)
                # Clear the Streamlit page
                st.empty()
                pass
            elif "start learning" in user_input.lower():
                AM.play_audio(AM.text_to_audio("Now we start learning.......last topic you was learnt....."+ topics[1] + "Do you wants to go forward or once revise last "))
                # Add learning logic here
                pass
            elif "stop" in user_input.lower():
                break
            else:
                pass

if __name__ == '__main__':
    main()
