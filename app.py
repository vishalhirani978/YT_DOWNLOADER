import streamlit as st
from pytubefix import YouTube
import os

st.title(" YT Downloader")

url = st.text_input("Enter YouTube URL:")
option = st.radio("Select format:", ["Video", "Audio"])

if st.button("Download"):
    if url:
        try:
            
            yt = YouTube(url, client='WEB')
            st.write(f"Processing: **{yt.title}**")
            
            if option == "Video":
                stream = yt.streams.get_highest_resolution()
            else:
                stream = yt.streams.filter(only_audio=True).first()
            
            
            file_path = stream.download(output_path=".")
            
            
            with open(file_path, "rb") as f:
                st.download_button(
                    label="📥 Click here to Save File",
                    data=f,
                    file_name=os.path.basename(file_path),
                    mime="video/mp4" if option == "Video" else "audio/mpeg"
                )
            st.success("Download Ready!")
            
            
            
        except Exception as e:
            st.error(f"Error: {e}")
    else:

        st.warning("Please enter a URL first!")
