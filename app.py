import streamlit as st
import requests
import json
from sonos_control import SonosController

def main():
    st.title("Sonos Control Panel")
    st.write("Control your Sonos speakers from this web interface")
    
    # Initialize Sonos controller
    sonos = SonosController()
    
    # Get available speakers
    speakers = sonos.get_speakers()
    
    if speakers:
        st.subheader("Available Speakers")
        for speaker in speakers:
            st.write(f"- {speaker['name']} ({speaker['ip']})")
        
        # Speaker selection
        selected_speaker = st.selectbox(
            "Select a speaker",
            [speaker['name'] for speaker in speakers]
        )
        
        # Control buttons
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("Play"):
                sonos.play(selected_speaker)
                st.success(f"Playing on {selected_speaker}")
        
        with col2:
            if st.button("Pause"):
                sonos.pause(selected_speaker)
                st.success(f"Paused {selected_speaker}")
        
        with col3:
            if st.button("Stop"):
                sonos.stop(selected_speaker)
                st.success(f"Stopped {selected_speaker}")
        
        # Volume control
        volume = st.slider("Volume", 0, 100, 50)
        if st.button("Set Volume"):
            sonos.set_volume(selected_speaker, volume)
            st.success(f"Volume set to {volume}% on {selected_speaker}")
        
        # Now playing info
        st.subheader("Now Playing")
        try:
            info = sonos.get_now_playing(selected_speaker)
            if info:
                st.write(f"**Track:** {info.get('title', 'Unknown')}")
                st.write(f"**Artist:** {info.get('artist', 'Unknown')}")
                st.write(f"**Album:** {info.get('album', 'Unknown')}")
        except Exception as e:
            st.error(f"Could not get track info: {e}")
    
    else:
        st.error("No Sonos speakers found on the network")

if __name__ == "__main__":
    main()
