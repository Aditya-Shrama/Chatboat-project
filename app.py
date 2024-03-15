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

# Base = declarative_base()

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

# # Define your SQLAlchemy models
# class LearningHistory(Base):
#     __tablename__ = "learning_history"
#     student_id = Column(Integer, primary_key=True)
#     english_key = Column(Integer)
#     mathematics_key = Column(Integer)
#     science_key = Column(Integer)

# class Science(Base):
#     __tablename__ = "5_science"
#     chapter_id = Column(Integer, primary_key=True)
#     chapter_number = Column(Integer)
#     chapter_name = Column(String(100))
#     topic_name = Column(String(1000))

# # Initialize the SQLAlchemy engine
# engine = create_engine('mysql+mysqlconnector://root:mim1430@localhost:3306/generative_trainer')

# # Create session maker
# Session = sessionmaker(bind=engine)

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
    # # Create a session
    # session = Session()
    # # Query the database
    # student = session.query(LearningHistory).filter_by(student_id=501).first()
    # if student:
    #     current_key = student.science_key
    #     previous_topic = session.query(Science).filter_by(chapter_id=current_key).first()

    st.set_page_config("voice_chat_trainer")
    username = "student"
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
                # student = session.query(LearningHistory).filter_by(student_id=501).first()
                # if student:
                #     current_key = student.science_key
                #     current_topic = session.query(Science).filter_by(chapter_id=current_key).first()
                #     print(current_topic.topic_name)
                # pass
                while True:
                    user_command = recognize_speech()
                    if user_command:
                        if "previous topic" in user_command.lower():
                            # previous_key = student.science_key-1
                            # previous_topic = session.query(Science).filter_by(chapter_id=previous_key).first()
                            # explanation = cg.explain_topic(previous_topic.topic_name)
                            explanation = cg.explain_topic(topics[0])
                            small_explaination = cg.small_answer(explanation)
                            st.write(explanation)
                            path = AM.text_to_audio(small_explaination + "Read the given explanation then we go forward.")
                            AM.play_audio(path)
                            while True :
                                Done_command = recognize_speech()
                                if Done_command:
                                    if "done" in Done_command.lower() or "complete" in Done_command.lower():
                                        while True:
                                            txt = st.write("True/False\n",true_false_questions["0"]["question"])
                                            print(true_false_questions["0"]["answer"])
                                            while True:
                                                AM.play_audio(AM.text_to_audio("Before going forward answer this question"))
                                                User_answer = recognize_speech()
                                                if User_answer:
                                                    if true_false_questions["0"]["answer"] in User_answer.lower():
                                                        AM.play_audio(AM.text_to_audio("Correct Answer ..........Now we going forward"))
                                                        st.write("Correct!")
                                                        break
                                                    else:
                                                        AM.play_audio(AM.text_to_audio("Wrong Answer ..........Try Once again"))
                                                        st.write("Wrong!")
                                                        continue
                                            break
                                break 
                            AM.play_audio(AM.text_to_audio("So! we completed this topic"))
                            pass       
                        elif "revise last topic" in user_command.lower() or "revised last topic" in user_command.lower():
                            # next_topic = session.query(Science).filter_by(chapter_id=student.science_key).first()
                            # explanation = cg.explain_topic(next_topic.topic_name)
                            explanation = cg.explain_topic(topics[1])
                            small_explaination = cg.small_answer(explanation)
                            st.write(explanation)
                            path = AM.text_to_audio(small_explaination + "Read the given explanation then we go forward.")
                            AM.play_audio(path)
                            while True :
                                Done_command = recognize_speech()
                                if Done_command:
                                    if "done" in Done_command.lower() or "complete" in Done_command.lower():
                                        while True:
                                            txt = st.write("True/False\n",true_false_questions["1"]["question"])
                                            print(true_false_questions["1"]["answer"])
                                            while True:
                                                AM.play_audio(AM.text_to_audio("Before going forward answer this question"))
                                                User_answer = recognize_speech()
                                                if User_answer:
                                                    if true_false_questions["1"]["answer"] in User_answer.lower():
                                                        AM.play_audio(AM.text_to_audio("Correct Answer ..........Now we going forward"))
                                                        st.write("Correct!")
                                                        break
                                                    else:
                                                        AM.play_audio(AM.text_to_audio("Wrong Answer ..........Try Once again"))
                                                        st.write("Wrong!")
                                                        continue
                                            break
                                break
                            AM.play_audio(AM.text_to_audio("So! we completed this topic"))
                            pass    
                        elif "next topic" in user_command.lower():
                            # next_key = student.science_key+1
                            # next_topic = session.query(Science).filter_by(chapter_id=next_key).first()
                            # explanation = cg.explain_topic(next_topic.topic_name)
                            explanation = cg.explain_topic(topics[2])
                            small_explaination = cg.small_answer(explanation)
                            st.write(explanation)
                            path = AM.text_to_audio(small_explaination + "Read the given explanation then we go forward.")
                            AM.play_audio(path)
                            while True :
                                Done_command = recognize_speech()
                                if Done_command:
                                    if "done" in Done_command.lower() or "complete" in Done_command.lower():
                                        while True:
                                            txt = st.write("True/False\n",true_false_questions["2"]["question"])
                                            print(true_false_questions["2"]["answer"])
                                            while True:
                                                AM.play_audio(AM.text_to_audio("Before going forward answer this question"))
                                                User_answer = recognize_speech()
                                                if User_answer:
                                                    if true_false_questions["1"]["answer"] in User_answer.lower():
                                                        AM.play_audio(AM.text_to_audio("Correct Answer ..........Now we going forward"))
                                                        st.write("Correct!")
                                                        break
                                                    else:
                                                        AM.play_audio(AM.text_to_audio("Wrong Answer ..........Try Once again"))
                                                        st.write("Wrong!")
                                                        continue
                                            break
                                break
                            AM.play_audio(AM.text_to_audio("So! we completed this topic"))
                            pass
                        elif "stop learning" in user_command.lower():
                            st.write("Back to main menu")
                            break
                        else:
                            pass
                    else:
                        pass                        
                pass
            elif "stop" in user_input.lower():
                break
            else:
                pass
            
            
            
    # Close the session
    # session.close()

if __name__ == '__main__':
    main()
