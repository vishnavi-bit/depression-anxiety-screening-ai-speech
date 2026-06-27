import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import random
import streamlit as st
from st_audiorec import st_audiorec
import io
import soundfile as sf
import numpy as np
import librosa
import joblib
import random
from dotenv import load_dotenv
import os

load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
from groq import Groq

# Fix matplotlib backend
import matplotlib
matplotlib.use("Agg")

from langchain_groq import ChatGroq
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate


from transformers import pipeline

llm = ChatGroq(
    temperature=0.5,
    groq_api_key=GROQ_API_KEY,
    model_name="llama-3.1-8b-instant"
)

def give_suggestions(text):
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "You are a supportive and empathetic assistant that provides practical mental health suggestions "
            "based strictly on the emotional content of the given text."
        ),
        (
            "user",
            'Give the results in points wise format.'
            "Analyze the emotional tone and stress level in the following text and provide helpful mental health suggestions. "
            "Do not give any introduction, explanation, headings, bullets, numbering, markdown, emojis, or special formatting. "
            "Do not diagnose or label any mental health condition. "
            "Use simple, calm, and non-clinical language. "
            "Provide short, actionable, and compassionate suggestions focused on coping strategies, emotional regulation, "
            "and healthy daily habits. "
            "Avoid judgmental, alarming, or absolute statements. "
            "Only output the suggestions as plain text.\n\n{input_text}"
        )
    ])

    chain = prompt | llm | StrOutputParser()
    response = chain.invoke({"input_text": text})
    return response
@st.cache_resource(show_spinner=False)
def load_models():
    emotion_model = pipeline(
        "audio-classification",
        model="superb/hubert-large-superb-er"
    )

    asr_model = pipeline(
        "automatic-speech-recognition",
        model="openai/whisper-small"
    )

    depression_model = joblib.load("depression_model.pkl")
    vectorizer = joblib.load("vectorizer.pkl")

    return emotion_model, asr_model, depression_model, vectorizer


with st.spinner("⚙️ Loading AI models (first run may take time)..."):
    emotion_model, asr_model, depression_model, vectorizer = load_models()

# Load the trained model
def normal_page():
    # Navigation menu for user dashboard

    with st.sidebar:
        st.markdown(f"<h1 style='text-align: center; color: black;'><b>🏡Dashboard</b></h1>", unsafe_allow_html=True)

        selected_tab = option_menu(
            menu_title=None,
            options=['Profile',"Upload Audio",'Live Speech','ChatBot' ,'Logout'],
            icons=['person-circle','upload','mic','chat-left-dots','unlock'],
        styles={
        "nav-link-selected": {"background-color": "green", "color": "white", "border-radius": "5px"},
        }
        )
    
    if selected_tab=='Logout':
        # Logout functionality
        st.session_state.clear()  # Clear session state to "log out"
        st.experimental_rerun()
    elif selected_tab=='Profile':
        st.markdown(
            """
            <style>
            /* Apply background image to the main content area */
            .main {
                background-image: url('https://st2.depositphotos.com/32167432/48954/i/450/depositphotos_489546962-stock-photo-public-speaking-backgrounds-close-microphone.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                min-height: 100vh;  /* Ensure the background covers the whole screen */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        user=st.session_state['user']
        _, name, email, age, _, status, _ = user
        profile_images = [
            "https://cdn-icons-png.flaticon.com/512/219/219983.png",
            "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQIf4R5qPKHPNMyAqV-FjS_OTBB8pfUV29Phg&s"
        ]
        profile_img = random.choice(profile_images)
        # ------------------ CSS ------------------
        st.markdown("""
        <style>
        .profile-card {
            width: 500px;
            margin: auto;
            padding: 35px;
            border-radius: 20px;
            background: linear-gradient(275deg, #F0FFC3, #BFC6C4);
            box-shadow: 0 10px 30px rgba(0,0,0,0.80);
            text-align: center;
            font-family: 'Segoe UI', sans-serif;
        }

        .profile-card img {
            width: 120px;
            height: 120px;
            border-radius: 50%;
            margin-bottom: 10px;
            border: 4px solid #f06292;
        }

        .badge {
            display: inline-block;
            background: #f06292;
            color: white;
            padding: 6px 14px;
            border-radius: 30px;
            font-size: 14px;
            margin-bottom: 15px;
        }

        .name {
            font-size: 22px;
            font-weight: 700;
            color: #333;
        }

        .info {
            font-size: 20px;
            color: #555;
            margin-top: 6px;
        }
        </style>
        """, unsafe_allow_html=True)

        # ------------------ PROFILE CARD ------------------
        st.markdown(f"""
        <div class="profile-card">
            <img src="{profile_img}">
            <div class="badge">🙍🏻‍♂️ {status}</div>
            <div class="name">{name.title()}</div>
            <div class="info">📧 {email}</div>
            <div class="info">🎂 Age: {age}</div>
        </div>
        """, unsafe_allow_html=True)
    elif selected_tab=='Live Speech':
        st.markdown(
            """
            <style>
            /* Apply background image to the main content area */
            .main {
                background-image: url('https://static.vecteezy.com/system/resources/thumbnails/048/284/720/small/simple-soft-blank-subtle-cream-horizontal-plain-background-with-decorative-mandala-artwork-texture-vector.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                min-height: 100vh;  /* Ensure the background covers the whole screen */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown("""
            <style>
            .title-box {
                background: linear-gradient(135deg, red, yellow);
                padding: 35px;
                border-radius: 18px;
                text-align: center;
                box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
                margin-bottom: 25px;
            }

            .title-box h1 {
                color: black;
                font-size: 35px;
                font-weight: 800;
                letter-spacing: 1px;
                margin: 0;
            }

            .title-box p {
                color: #f1f1f1;
                font-size: 18px;
                margin-top: 10px;
            }
            </style>
            """, unsafe_allow_html=True)

        # ---- Title Container ----
        st.markdown("""
        <div class="title-box">
            <h1>Depression and Anxiety Screening for Pregnant Women and General Users Using AI Speech</h1>
        </div>
        """, unsafe_allow_html=True)
        wav_audio = st_audiorec()
        data, sr = None, None
        if wav_audio is not None:
            st.audio(wav_audio, format="audio/wav")
            data, sr = sf.read(io.BytesIO(wav_audio), dtype="float32")
            if data.ndim > 1:
                data = np.mean(data, axis=1)
            if sr != 16000:
                data = librosa.resample(data, orig_sr=sr, target_sr=16000)
                sr = 16000

            st.success(f"Recorded {len(data)/sr:.2f} seconds")

        recognized_text = ""

        if data is not None:

            with st.spinner("Transcribing speech..."):
                transcription = asr_model(
                    {"array": data, "sampling_rate": sr}
                )
                recognized_text = transcription["text"]

        depression_score = 0.0
        depression_label = "Unknown"
        with st.container(border=True):
            if recognized_text.strip():
                st.subheader("📘Depression Analysis")

                text_vector = vectorizer.transform([recognized_text])
                prediction = depression_model.predict(text_vector)[0]

                if hasattr(depression_model, "predict_proba"):
                    depression_score = depression_model.predict_proba(text_vector)[0][1]
                else:
                    depression_score = float(prediction)

                if prediction == 1:
                    depression_label = "Depression Risk Detected"
                    st.error("⚠️ Signs of depression detected from text")
                else:
                    depression_label = "No Depression Risk"
                    st.success("😊 No depression signs detected from text")

                st.progress(int(depression_score * 100))

            emotion_scores = {}
            dominant_emotion = None

            if data is not None:
                st.subheader("🎭Emotion Analysis")

                predictions = emotion_model(
                    {"array": data, "sampling_rate": sr}
                )

                top3 = sorted(predictions, key=lambda x: x["score"], reverse=True)[:3]

                for pred in top3:
                    emotion_scores[pred["label"]] = pred["score"]
                    st.write(f"**{pred['label'].capitalize()}** — {pred['score']*100:.1f}%")
                    st.progress(int(pred["score"] * 100))

                dominant_emotion = top3[0]["label"]

            # =========================================================
            # Step 5: Anxiety Inference (Rule-Based)
            # =========================================================
            st.subheader("🔎Anxiety Assessment")

            anxiety_score = 0.0
            anxiety_label = "Low Anxiety Risk"

            if dominant_emotion in ["angry", "fearful", "sad"]:
                anxiety_score += 0.4

            if depression_score > 0.6:
                anxiety_score += 0.4

            anxiety_score = min(anxiety_score, 1.0)

            if anxiety_score > 0.6:
                anxiety_label = "High Anxiety Risk"
                st.warning("⚠️ Anxiety indicators detected")
            else:
                st.success("😌 Low anxiety indicators")

            st.progress(int(anxiety_score * 100))

            # =========================================================
            # Step 6: Final Overall Assessment
            # =========================================================
            st.subheader("📊 Mental Health Assessment")

            overall_score = round(
                (depression_score * 0.5 + anxiety_score * 0.5) * 100, 2
            )

            if overall_score > 65:
                st.error(f"🚨 High Mental Health Risk ({overall_score}%)")
            elif overall_score > 40:
                st.warning(f"⚠️ Moderate Mental Health Risk ({overall_score}%)")
            else:
                st.success(f"✅ Low Mental Health Risk ({overall_score}%)")

            st.markdown(f"""
            **Summary:**
            - 🗣️ Dominant Emotion: **{dominant_emotion}**
            - 📘 Depression Risk: **{depression_label}**
            - 😟 Anxiety Risk: **{anxiety_label}**
            - 📊 Overall Confidence Score: **{overall_score}%**
            """)


            if recognized_text.strip():
                with st.expander("💡 Get Mental Health Improvement Suggestions"):
                    overall = f"""
                    I have a {depression_label} and {anxiety_label}.
                    My overall mental health risk score is {overall_score}%.
                    Emotion detected in my voice is {dominant_emotion}.
                    """
                    suggestions = give_suggestions(overall)
                    points = suggestions.split(".")
                    for point in points:
                        if point.strip() != "":
                            st.write(f"- {point.strip()}")


        # =========================================================
        # Footer
        # =========================================================
        st.markdown("---")
        st.caption(
            "💙 If you feel distressed, please consult a licensed mental health professional."
        )

    elif selected_tab=='Upload Audio':
        st.markdown(
            """
            <style>
            /* Apply background image to the main content area */
            .main {
                background-image: url('https://static.vecteezy.com/system/resources/thumbnails/048/284/720/small/simple-soft-blank-subtle-cream-horizontal-plain-background-with-decorative-mandala-artwork-texture-vector.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
                min-height: 100vh;  /* Ensure the background covers the whole screen */
            }
            </style>
            """,
            unsafe_allow_html=True
        )
        st.markdown("""
            <style>
            .title-box {
                background: linear-gradient(135deg, red, yellow);
                padding: 35px;
                border-radius: 18px;
                text-align: center;
                box-shadow: 0px 8px 25px rgba(0,0,0,0.15);
                margin-bottom: 25px;
            }

            .title-box h1 {
                color: black;
                font-size: 30px;
                font-weight: 800;
                letter-spacing: 1px;
                margin: 0;
            }

            .title-box p {
                color: #f1f1f1;
                font-size: 18px;
                margin-top: 10px;
            }
            </style>
            """, unsafe_allow_html=True)

        # ---- Title Container ----
        st.markdown("""
        <div class="title-box">
            <h3>Depression and Anxiety Screening for Pregnant Women and General Users Using AI Speech</h3>
        </div>
        """, unsafe_allow_html=True)
        col1,col2,col3=st.columns([1,6,1])
        uploaded_file = col2.file_uploader(
            "Upload an audio file (WAV / MP3 / OGG)",
            type=["wav", "mp3", "ogg"]
        )

        data, sr = None, None

        if uploaded_file is not None:
            st.audio(uploaded_file)

            with st.spinner("Processing audio..."):
                data, sr = sf.read(io.BytesIO(uploaded_file.read()), dtype="float32")

                # Convert to mono
                if data.ndim > 1:
                    data = np.mean(data, axis=1)

                # Resample to 16kHz
                if sr != 16000:
                    data = librosa.resample(data, orig_sr=sr, target_sr=16000)
                    sr = 16000

            st.success(f"Audio loaded ({len(data)/sr:.2f} seconds)")

        # =========================================================
        # Step 2: Speech → Text
        # =========================================================
        recognized_text = ""

        if data is not None:
            with st.spinner("Transcribing speech..."):
                transcription = asr_model(
                    {"array": data, "sampling_rate": sr}
                )
                recognized_text = transcription["text"]
        with st.container(border=True):
            # =========================================================
            # Depression Detection
            # =========================================================
            depression_score = 0.0
            depression_label = "Unknown"

            if recognized_text.strip():
                st.subheader("📘Depression Analysis")

                text_vector = vectorizer.transform([recognized_text])
                prediction = depression_model.predict(text_vector)[0]

                if hasattr(depression_model, "predict_proba"):
                    depression_score = depression_model.predict_proba(text_vector)[0][1]
                else:
                    depression_score = float(prediction)

                if prediction == 1:
                    depression_label = "Depression Risk Detected"
                    st.error("⚠️ Signs of depression detected from speech content")
                else:
                    depression_label = "No Depression Risk"
                    st.success("😊 No depression indicators detected")

                st.progress(int(depression_score * 100))

            emotion_scores = {}
            dominant_emotion = None

            if data is not None:
                st.subheader("🎭Emotion Analysis")

                predictions = emotion_model(
                    {"array": data, "sampling_rate": sr}
                )

                top3 = sorted(predictions, key=lambda x: x["score"], reverse=True)[:3]

                for pred in top3:
                    emotion_scores[pred["label"]] = pred["score"]
                    st.write(f"**{pred['label'].capitalize()}** — {pred['score']*100:.1f}%")
                    st.progress(int(pred["score"] * 100))

                dominant_emotion = top3[0]["label"]

            st.subheader("🔎 Anxiety Assessment")

            anxiety_score = 0.0
            anxiety_label = "Low Anxiety Risk"

            if dominant_emotion in ["angry", "fearful", "sad"]:
                anxiety_score += 0.4

            if depression_score > 0.6:
                anxiety_score += 0.4

            anxiety_score = min(anxiety_score, 1.0)

            if anxiety_score > 0.6:
                anxiety_label = "High Anxiety Risk"
                st.warning("⚠️ Anxiety indicators detected")
            else:
                st.success("😌 Low anxiety indicators")

            st.progress(int(anxiety_score * 100))

            st.subheader("📊 Mental Health Assessment")

            overall_score = round(
                (depression_score * 0.5 + anxiety_score * 0.5) * 100, 2
            )

            if overall_score > 65:
                st.error(f"🚨 High Mental Health Risk ({overall_score}%)")
            elif overall_score > 40:
                st.warning(f"⚠️ Moderate Mental Health Risk ({overall_score}%)")
            else:
                st.success(f"✅ Low Mental Health Risk ({overall_score}%)")

            st.markdown(f"""
            **Summary:**
            - 🗣️ Dominant Emotion: **{dominant_emotion}**
            - 📘 Depression Risk: **{depression_label}**
            - 😟 Anxiety Risk: **{anxiety_label}**
            - 📊 Overall Confidence Score: **{overall_score}%**
            """)

            # =========================================================
            # Suggestions
            # =========================================================
            if recognized_text.strip():
                with st.expander("💡 Get Mental Health Improvement Suggestions"):
                    overall = f"""
                    I have a {depression_label} and {anxiety_label}.
                    My overall mental health risk score is {overall_score}%.
                    Emotion detected in my voice is {dominant_emotion}.
                    """
                    suggestions = give_suggestions(overall)
                    points = suggestions.split(".")
                    for point in points:
                        if point.strip() != "":
                            st.write(f"- {point.strip()}")

            # =========================================================
            # Footer
            # =========================================================
            st.markdown("---")
            st.caption("💙 If you feel distressed, please consult a licensed mental health professional.")
    elif selected_tab == 'ChatBot':
        from groq import Groq

        # ---------------------------
        # Styling
        # ---------------------------
        st.markdown(
            """
            <style>
            .main {
                background-image: url('https://wallpapers.com/images/hd/plain-white-background-3qzwpiavktxg11pr.jpg');
                background-size: cover;
                background-position: center;
                background-repeat: no-repeat;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # ---------------------------
        # Configure Groq API Key
        # ---------------------------
        client = Groq(api_key=GROQ_API_KEY)

        st.title("🧠 Depression & Anxiety ChatBot")
        st.markdown("Ask me anything about Depression or Anxiety.")

        # ---------------------------
        # Initialize session state
        # ---------------------------
        if "messages" not in st.session_state:
            st.session_state.messages = []

        # ---------------------------
        # Display Chat History
        # ---------------------------
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # ---------------------------
        # User Input
        # ---------------------------
        user_input = st.chat_input("Ask me about Depression or Anxiety...")

        if user_input:

            st.session_state.messages.append({"role": "user", "content": user_input})
            with st.chat_message("user"):
                st.markdown(user_input)

            greetings = ["hi", "hello", "hey", "gm", "good morning", "good evening", "good night"]

            if user_input.lower() in greetings:
                bot_response = "Hello 😊 I'm here to help you with questions about depression and anxiety."

            else:

                # ---------------------------
                # SINGLE PROMPT (YES / NO + ANSWER)
                # ---------------------------
                single_prompt = f"""
                    You are a professional mental health assistant specialized in Depression and Anxiety disorders.

                    Follow these strict rules:

                    1. If the question is related to Depression or Anxiety:
                    - Provide a clear, supportive, and medically accurate explanation.
                    - Include symptoms, causes, coping strategies, and treatment if relevant.
                    - Be empathetic and professional.
                    - Add a short disclaimer: "This information is not a substitute for professional medical advice."

                    2. If the question is NOT related to Depression or Anxiety:
                    - Reply exactly with:
                    "⚠️ Please ask a question related to depression or anxiety only."

                    User Question: {user_input}
                """

                completion = client.chat.completions.create(
                    model="llama-3.1-8b-instant",
                    messages=[
                        {"role": "system", "content": "You are a mental health AI assistant."},
                        {"role": "user", "content": single_prompt}
                    ],
                    temperature=0.6
                )

                bot_response = completion.choices[0].message.content

            # Store response
            st.session_state.messages.append({"role": "assistant", "content": bot_response})
            with st.chat_message("assistant"):
                st.markdown(bot_response)
