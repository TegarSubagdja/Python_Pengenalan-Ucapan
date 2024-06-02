import streamlit as st
import os
import json
import speech_recognition as sr
import pygame

st.set_page_config(layout="wide")

# Inisialisasi mixer pygame
pygame.mixer.init()

# Custom CSS
with open("css/styles.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Music directory
music_dir = 'music/'
music_files = [f for f in os.listdir(music_dir) if f.endswith('.mp3')]
music_files.sort()  # Sort the files alphabetically

# Load JSON data
def load_json(file_path):
    if os.path.exists(file_path):
        with open(file_path, 'r') as f:
            return json.load(f)
    else:
        return {"recent": [], "playlist": [], "favorite": []}

def save_json(file_path, data):
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

recent_file = 'data/recent.json'
playlist_file = 'data/playlist.json'
favorite_file = 'data/favorite.json'

recent_data = load_json(recent_file)
playlist_data = load_json(playlist_file)
favorite_data = load_json(favorite_file)

def play_audio(file_path, position=0):
    pygame.mixer.music.load(file_path)
    pygame.mixer.music.play(start=position)

def pause_audio():
    st.session_state['audio_position'] = pygame.mixer.music.get_pos() / 1000
    pygame.mixer.music.pause()

def resume_audio():
    play_audio(os.path.join(music_dir, st.session_state['selected_song']), st.session_state['audio_position'])

def stop_audio():
    pygame.mixer.music.stop()
    st.session_state['audio_position'] = 0

def add_to_favorites(song):
    if song not in favorite_data["favorite"]:
        favorite_data["favorite"].append(song)
        save_json(favorite_file, favorite_data)

def search_song(title, artist):
    for file in music_files:
        if title.lower() in file.lower() and artist.lower() in file.lower():
            return file
    return None

# Inisialisasi session state
if 'selected_page' not in st.session_state:
    st.session_state['selected_page'] = "Home"
if 'playback_state' not in st.session_state:
    st.session_state['playback_state'] = 'stopped'
if 'selected_song' not in st.session_state:
    st.session_state['selected_song'] = music_files[0] if music_files else None
if 'audio_position' not in st.session_state:
    st.session_state['audio_position'] = 0

# Sidebar navigation
st.sidebar.title(":orange[App]")

pages = ["Home", "Playlists", "Favorites", "Recently Played"]
selected_page = st.sidebar.radio("Navigate", pages, index=pages.index(st.session_state['selected_page']))

st.sidebar.caption("KEL - 3")
st.sidebar.caption("152021144 - Yuren Prisilla")
st.sidebar.caption("152021159 - Ayala Qaulam Putri")
st.sidebar.caption("152021169 - Tegar Subagdja")
st.sidebar.caption("152021175 - Nirmala Putri Ismail")
st.sidebar.caption("152020030 - Andi Muchlad Ramadani")

st.title(":orange[Music Player]")

# Page content based on selection
if selected_page == "Home":
    selected_song = st.sidebar.selectbox("Select a Song", music_files, index=music_files.index(st.session_state['selected_song']) if st.session_state['selected_song'] in music_files else 0)

    # Display the selected song and audio player
    if selected_song:
        st.session_state['selected_song'] = selected_song
        st.write(f"Currently playing: {selected_song}")
        song_path = os.path.join(music_dir, selected_song)

        if st.session_state['playback_state'] == 'playing':
            if not pygame.mixer.music.get_busy():
                play_audio(song_path, st.session_state['audio_position'])
        elif st.session_state['playback_state'] == 'paused':
            if not pygame.mixer.music.get_busy():
                play_audio(song_path, st.session_state['audio_position'])
                pygame.mixer.music.pause()

        # Update recent songs
        if selected_song not in recent_data["recent"]:
            recent_data["recent"].append(selected_song)
            if len(recent_data["recent"]) > 10:  # Keep only the last 10 recent songs
                recent_data["recent"].pop(0)
            save_json(recent_file, recent_data)

    st.write("## Latest Releases")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write("### Rizky Febian")
        st.image("https://cdns-images.dzcdn.net/images/cover/ff8c91521ca4aa9ffb63b9a212bc7a6d/264x264.jpg", use_column_width=True)
        st.write("New Album")

    with col2:
        st.write("### Lana Del Rey")
        st.image("https://m.media-amazon.com/images/I/51QRAWT6aSL._AC_UF894,1000_QL80_.jpg", use_column_width=True)
        st.write("New Album")

    with col3:
        st.write("### Mahalini")
        st.image("https://assets.crownnote.com/s3fs-public/ab67616d0000b273a8a2a99e01506f56c991a24e.jpeg", use_column_width=True)
        st.write("New Album")

    with col4:
        st.write("### Bruno Mars")
        st.image("https://upload.wikimedia.org/wikipedia/en/e/eb/Bruno_Mars_-_Doo-Wops_%26_Hooligans.png", use_column_width=True)
        st.write("New Album")

    st.write("## Tracks For You")
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.write("### Martin Garrix")
        st.image("https://i.scdn.co/image/ab67616d0000b273edba220be76f96d51bd38838", use_column_width=True)
        st.write("New Track")

    with col2:
        st.write("### Avicii")
        st.image("https://i.scdn.co/image/ab67616d0000b273182fe5b5d3e3c3fcc895a3c8", use_column_width=True)
        st.write("New Track")

elif selected_page == "Playlists":
    st.write("# Playlists")
    if "playlist" in playlist_data:
        for song in playlist_data["playlist"]:
            with st.container():
                st.write(f"### {song}")
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image("https://via.placeholder.com/150", use_column_width=True)  # Replace with actual album art URL if available
                with col2:
                    st.write(f"Playing: {song}")
                    song_path = os.path.join(music_dir, song)
                    if st.button("Play", key=song):
                        play_audio(song_path)
                        st.session_state['selected_song'] = song
                        st.session_state['playback_state'] = 'playing'
                    if st.button("Pause", key=song + "_pause"):
                        pause_audio()
                        st.session_state['playback_state'] = 'paused'
                    if st.button("Resume", key=song + "_resume"):
                        resume_audio()
                        st.session_state['playback_state'] = 'playing'
                    if st.button("Stop", key=song + "_stop"):
                        stop_audio()
                        st.session_state['playback_state'] = 'stopped'
                    if st.button("⭐ Add to Favorites", key=song + "_fav"):
                        add_to_favorites(song)
                        st.success(f"{song} added to favorites!")

elif selected_page == "Favorites":
    st.write("# Favorites")
    if "favorite" in favorite_data:
        for song in favorite_data["favorite"]:
            with st.container():
                st.write(f"### {song}")
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image("https://via.placeholder.com/150", use_column_width=True)  # Replace with actual album art URL if available
                with col2:
                    st.write(f"Playing: {song}")
                    song_path = os.path.join(music_dir, song)
                    if st.button("Play", key=song):
                        play_audio(song_path)
                        st.session_state['selected_song'] = song
                        st.session_state['playback_state'] = 'playing'
                    if st.button("Pause", key=song + "_pause"):
                        pause_audio()
                        st.session_state['playback_state'] = 'paused'
                    if st.button("Resume", key=song + "_resume"):
                        resume_audio()
                        st.session_state['playback_state'] = 'playing'
                    if st.button("Stop", key=song + "_stop"):
                        stop_audio()
                        st.session_state['playback_state'] = 'stopped'

elif selected_page == "Recently Played":
    st.write("# Recently Played")
    if "recent" in recent_data:
        for song in recent_data["recent"]:
            with st.container():
                st.write(f"### {song}")
                col1, col2 = st.columns([1, 3])
                with col1:
                    st.image("https://via.placeholder.com/150", use_column_width=True)  # Replace with actual album art URL if available
                with col2:
                    st.write(f"Playing: {song}")
                    song_path = os.path.join(music_dir, song)
                    if st.button("Play", key=song):
                        play_audio(song_path)
                        st.session_state['selected_song'] = song
                        st.session_state['playback_state'] = 'playing'
                    if st.button("Pause", key=song + "_pause"):
                        pause_audio()
                        st.session_state['playback_state'] = 'paused'
                    if st.button("Resume", key=song + "_resume"):
                        resume_audio()
                        st.session_state['playback_state'] = 'playing'
                    if st.button("Stop", key=song + "_stop"):
                        stop_audio()
                        st.session_state['playback_state'] = 'stopped'
                    if st.button("⭐ Add to Favorites", key=song + "_fav"):
                        add_to_favorites(song)
                        st.success(f"{song} added to favorites!")

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.write("Listening for commands...")
        audio = recognizer.listen(source)
        try:
            command = recognizer.recognize_google(audio, language="id-ID").lower()
            st.write(f"Perintah diterima: {command}")
            return command
        except sr.UnknownValueError:
            st.write("Tidak dapat memahami perintah")
            return ""
        except sr.RequestError as e:
            st.write(f"Tidak dapat meminta hasil; {e}")
            return ""

# Button to activate microphone and recognize speech
if st.sidebar.button("Aktifkan Mikrofon"):
    # Hanya menangkap perintah tanpa mempengaruhi pemutaran musik
    command = recognize_speech()
    if command:
        # Menunda pemrosesan perintah sampai setelah pengaktifan mikrofon
        if "mainkan" in command:
            st.session_state['playback_state'] = 'playing'
            play_audio(os.path.join(music_dir, st.session_state['selected_song']), st.session_state['audio_position'])
        elif "jeda" in command:
            st.session_state['playback_state'] = 'paused'
            pause_audio()
        elif "berhenti" in command:
            st.session_state['playback_state'] = 'stopped'
            stop_audio()
        elif "lanjutkan" in command:
            st.session_state['playback_state'] = 'playing'
            resume_audio()
        elif "buka halaman pertama" in command:
            st.session_state['selected_page'] = 'Home'
            st.experimental_rerun()
        elif "buka halaman kedua" in command:
            st.session_state['selected_page'] = 'Playlists'
            st.experimental_rerun()
        elif "buka halaman ketiga" in command:
            st.session_state['selected_page'] = 'Favorites'
            st.experimental_rerun()
        elif "buka halaman keempat" in command:
            st.session_state['selected_page'] = 'Recently Played'
            st.experimental_rerun()
        elif command.startswith("putar"):
            parts = command.split(" dari ")
            if len(parts) == 2:
                title = parts[0].replace("putar ", "").strip()
                artist = parts[1].strip()
                song_file = search_song(title, artist)
                if song_file:
                    st.write(f"Playing: {song_file}")
                    st.session_state['playback_state'] = 'playing'
                    st.session_state['selected_song'] = song_file
                    st.session_state['audio_position'] = 0
                    play_audio(os.path.join(music_dir, song_file))
                    st.experimental_rerun()
                else:
                    st.write("Lagu tidak ditemukan")

# Handling playback state changes
if st.session_state['playback_state'] == 'playing':
    if 'selected_song' in st.session_state:
        st.write(f"Currently playing: {st.session_state['selected_song']}")
elif st.session_state['playback_state'] == 'paused':
    st.write("Music paused")
elif st.session_state['playback_state'] == 'stopped':
    st.write("Music stopped")
