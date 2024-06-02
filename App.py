import streamlit as st
import pygame
import os

# Inisialisasi mixer pygame
pygame.mixer.init()

# Music directory
music_dir = 'music/'
music_files = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]

# Function to play audio
def play_audio(file_path):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play()

# Function to stop audio
def stop_audio():
    pygame.mixer.music.stop()

st.title("Simple Audio Player")

selected_song = st.selectbox("Select a Song", music_files)

# Play button
if st.button("Play"):
    song_path = os.path.join(music_dir, selected_song)
    play_audio(song_path)

# Stop button
if st.button("Stop"):
    stop_audio()

# Display the selected song
if selected_song:
    st.write(f"Currently selected: {selected_song}")
