import streamlit as st
import hashlib
from midi2audio import FluidSynth
import pretty_midi
import numpy as np
import io
from scipy.io import wavfile

import note_seq
from note_seq.protobuf import music_pb2

from algo import generateSong
from algo import clean

st.set_page_config(
    page_title="Melodify | Text to Melody Generator", page_icon="images/square-logo-hd.png",
)

menu = ["🎺 Try out Melodify!", "🧙‍♂️ View Secret Algorithm", "🔨 Data Mining"]

with st.sidebar:
    st.image(
        "images/melodify-logo-hd.png",
        use_column_width = True
    )
    
    st.write("## Menu Select")
    st.markdown(
        """
        <style>
        [data-baseweb="select"] {
            margin-top: -50px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    screen = st.sidebar.selectbox("", menu, index=0)

    st.info(
        "Made with 💖 for **AIST2010** by: Albert, Angelica & Figo",
        )
    
    # st.error(
    #     "Found a bug?"
    # )

if screen == menu[0]:
    
    st.title(screen[2:])
    
    st.write(
        "Melodify takes in your text and using our secret recipe 🧪 will create a unique melody just for you!"
    )
    
    st.write("## 👇 Enter Text")
    
    inputText = st.text_area('')
    
    if st.button('Generate Melody'):
        st.write("## 🎶 Generated Song")
                        
        hsh = hashlib.sha256(inputText.encode()).hexdigest()
        hsh = hsh[:10]
        
        new = generateSong(clean(inputText))
        
        # plot note sequence
        note_seq.plot_sequence(new)

        # save song as midi
        note_seq.play_sequence(new, synth=note_seq.fluidsynth)
        note_seq.sequence_proto_to_midi_file(new, f"gens/{hsh}_song.mid")
        
        # load and convert midi to be displayed as wav
        # credits to: https://discuss.streamlit.io/t/midi-to-wav-streamlit-app/9839
        with st.spinner(f"Transcribing to Audio"):
            midi_data = pretty_midi.PrettyMIDI(f"gens/{hsh}_song.mid")
            audio_data = midi_data.fluidsynth()
            audio_data = np.int16(
                audio_data / np.max(np.abs(audio_data)) * 32767 * 0.9
            )

            virtualfile = io.BytesIO()
            wavfile.write(virtualfile, 44100, audio_data)

        st.audio(virtualfile)
        st.markdown("Download the melody by right-clicking on the media player!")

if screen == menu[1]:
    
    st.title(screen[4:])
    
    st.write("In progress 🔨")
    pass

if screen == menu[2]:
    
    st.title(screen[2:])
    
    st.write("In progress 🔨")
    pass