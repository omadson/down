from pytube import YouTube, Playlist
from pydantic import BaseModel, HttpUrl
import streamlit as st
from streamlit.components.v1 import html
import streamlit_pydantic as sp


class URL(BaseModel):
    url: HttpUrl



def main():
    st.title("Down")
    st.markdown("""
    Baixe vídeos do Youtube de maneira gratuita! Feito por [@omadson](https://github.com/omadson).
    """)
    data = sp.pydantic_form(
        key="first",
        model=URL,
        submit_label="Download",
        lowercase_labels=True
    )

    if data:
        with st.spinner("Processando"):
            if 'list=' in data.url:
                playlist =  Playlist(data.url)
                bt_down = []
                st.markdown("##### Clique nos links para realizar o download:") 
                for i, video_info in enumerate(playlist.videos):
                    video = (
                        video_info
                        .streams
                        .filter(progressive=True, file_extension='mp4')
                        .order_by('resolution')
                        .desc()
                        .first()
                    )
                    link = f' - <a href="{video.url}&title={video.title}" target="_blank">{video.title}</a>'
                    st.markdown(link, unsafe_allow_html=True)
            else:
                video = (
                    YouTube(data.url)
                    .streams
                    .filter(progressive=True, file_extension='mp4')
                    .order_by('resolution')
                    .desc()
                    .first()
                )
            
                html(f"""
                    <script>window.location.href = '{video.url}&title={video.title}';</script>
                """)
                
if __name__ == '__main__':
    main()