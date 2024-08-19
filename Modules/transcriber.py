import os
import math
from groq import Groq
from pydub import AudioSegment
from downloader import download_audio

# Set your Groq API key
os.environ["GROQ_API_KEY"] = "API_KEY_HERE" # Put your GROQ api key in here

MAX_FILE_SIZE = 25 * 1024 * 1024  # 25 MB in bytes

def clip_audio(input_file, output_file, max_size_bytes):
    audio = AudioSegment.from_mp3(input_file)
    
    # Calculate the maximum duration in milliseconds
    max_duration_ms = (max_size_bytes / len(audio.raw_data)) * len(audio)
    
    # Clip the audio
    clipped_audio = audio[:math.floor(max_duration_ms)]
    
    # Export the clipped audio
    clipped_audio.export(output_file, format="mp3")

def transcribe_youtube_audio(youtube_url):
    client = Groq()
    
    # Download the audio from YouTube
    output_file = "downloaded_audio.mp3"
    downloaded_file = download_audio(youtube_url, output_file)
    
    if not downloaded_file:
        print("Failed to download audio from YouTube")  
        return None
    
    # Transcribe the downloaded audio
    try:
        with open(downloaded_file, "rb") as file:
            transcription = client.audio.transcriptions.create(
                file=(downloaded_file, file.read()),
                model="whisper-large-v3",
                prompt="Transcription of a YouTube video",
                response_format="json",
                language="en",
                temperature=0.0
            )
        print(transcription.text)
        return transcription.text  # Return the transcribed text
    except Exception as e:
        print(f"Error during transcription: {str(e)}")
        return None
    finally:
        # Clean up: remove the downloaded file
        if os.path.exists(downloaded_file):
            os.remove(downloaded_file)
            
# Usage
if __name__ == "__main__":
    youtube_url = "https://www.youtube.com/watch?v=46gAXft4TMA"  # Replace with your YouTube URL
    transcribe_youtube_audio(youtube_url)