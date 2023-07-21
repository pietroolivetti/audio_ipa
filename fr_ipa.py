import streamlit as st
from pydub import AudioSegment
import io
import epitran
import speech_recognition as sr
from pydub.silence import split_on_silence


langs = {'Português': 'pt-BR', 'English': 'en', 'Italiano': 'it', 'Español': 'es-AR', 'Français': 'fr-FR', 'Deutsch': 'de-DE', 'Polski': 'pl'}

st.title('Choosing seconds to trim')

fr = epitran.Epitran('fra-Latn')


uploaded_file = st.file_uploader("Upload a file:")
if uploaded_file is not None:
    file = uploaded_file.read()
    st.audio(file)

    selected_lang = st.selectbox('Select a language:', langs, index=0)
    st.write(f"You've selected: {selected_lang}")

    n0 = st.text_input('Start', placeholder='minutes:seconds')
    sep0 = n0.split(':')
    t0 = (float(sep0[0]) * 60) * 1000 + (float(sep0[1]) * 1000)
    n1 = st.text_input('End', placeholder='minutes:seconds')
    sep1 = n1.split(':')
    t1 = (float(sep1[0]) * 60) * 1000 + (float(sep1[1]) * 1000)
    # st.write('Trim your file:')
    # start = st.number_input('Start: ', step=0.1) * 1000
    # end = st.number_input('End: ', step=0.1) * 1000


    audio_segment = AudioSegment.from_file(io.BytesIO(file), format="mp3")
    #cut_audio = audio_segment[start:end]
    cut_audio = audio_segment[t0:t1]
    trimmed = cut_audio.export('trimmed.mp3', format="mp3")
    st.audio('trimmed.mp3')

    r = sr.Recognizer()
    cut_audio.export('trimmed.flac', format="flac")
    with sr.AudioFile("trimmed.flac") as source:
        audio = r.record(source)
        transcription = r.recognize_google(audio, language=langs[selected_lang])

    st.write("Transcription:")
    st.info(transcription)
    
    f = fr.transliterate(transcription)
    
    st.write(f)
