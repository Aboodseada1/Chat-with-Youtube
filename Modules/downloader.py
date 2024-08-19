import os
import sys
import logging
from typing import Optional
import yt_dlp
from pytube import YouTube
from pydub import AudioSegment

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def download_audio(url: str, output_path: str = "output.mp3") -> Optional[str]:
    """
    Download audio from a YouTube URL and save it as an MP3 file.
    
    Args:
        url (str): The YouTube video URL.
        output_path (str): The path to save the output MP3 file.
    
    Returns:
        Optional[str]: The path to the downloaded MP3 file, or None if download failed.
    """
    try:
        # First attempt: Use yt-dlp
        return _download_with_ytdlp(url, output_path)
    except Exception as e:
        logger.warning(f"yt-dlp download failed: {str(e)}. Trying pytube...")
        try:
            # Second attempt: Use pytube
            return _download_with_pytube(url, output_path)
        except Exception as e:
            logger.error(f"All download attempts failed: {str(e)}")
            return None

def _download_with_ytdlp(url: str, output_path: str) -> str:
    ydl_opts = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
        'outtmpl': output_path.replace('.mp3', ''),
    }
    
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    
    return output_path

def _download_with_pytube(url: str, output_path: str) -> str:
    yt = YouTube(url)
    audio_stream = yt.streams.filter(only_audio=True).first()
    
    if not audio_stream:
        raise Exception("No audio stream found")
    
    # Download the audio stream
    temp_file = audio_stream.download(filename="temp_audio")
    
    # Convert to MP3 using pydub
    audio = AudioSegment.from_file(temp_file, format="mp4")
    audio.export(output_path, format="mp3")
    
    # Clean up temporary file
    os.remove(temp_file)
    
    return output_path

def main():
    if len(sys.argv) < 2:
        print("Usage: python script.py <YouTube URL>")
        sys.exit(1)
    
    url = sys.argv[1]
    output_file = download_audio(url)
    
    if output_file:
        print(f"Audio downloaded successfully: {output_file}")
    else:
        print("Failed to download audio")

if __name__ == "__main__":
    main()