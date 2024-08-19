import streamlit as st
import os
import sys
from groq import Groq
from urllib.parse import parse_qs, urlparse

modules_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "Modules"))
sys.path.append(modules_path)

from transcriber import transcribe_youtube_audio

os.environ["GROQ_API_KEY"] = "API_KEY_HERE" # Put your GROQ api key in here

client = Groq()

def get_video_id(url):
    """Extract video ID from YouTube URL"""
    query = urlparse(url)
    if query.hostname == 'youtu.be':
        return query.path[1:]
    if query.hostname in ('www.youtube.com', 'youtube.com'):
        if query.path == '/watch':
            p = parse_qs(query.query)
            return p['v'][0]
        if query.path[:7] == '/embed/':
            return query.path.split('/')[2]
        if query.path[:3] == '/v/':
            return query.path.split('/')[2]
    return None

def save_transcription(transcribed_text, video_id):
    """Save transcribed text to a file"""
    filename = f"{video_id}_transcription.txt"
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(transcribed_text)
    return filename

def chat_with_groq(transcribed_data, user_query):
    prompt = f"""Based on this transcribed data:
{transcribed_data}
Answer the following question: {user_query}
Just answer the question without mentioning phrases like "Based on these transcribed data", Make it like a normal chat"""

    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": prompt,
            }
        ],
        model="llama3-8b-8192",
    )

    return chat_completion.choices[0].message.content

def main():
    st.set_page_config(layout="wide")
    
    # Sidebar
    with st.sidebar:
        st.title("YouTube Video Input")
        youtube_url = st.text_input("Enter YouTube URL:")
        if st.button("Process Video"):
            if youtube_url:
                with st.spinner("Processing video..."):
                    transcribed_data = transcribe_youtube_audio(youtube_url)
                    if transcribed_data:
                        st.success("Video processed successfully!")
                        st.session_state.transcribed_data = transcribed_data
                        st.session_state.chat_history = []
                        st.session_state.video_id = get_video_id(youtube_url)
                    else:
                        st.error("Failed to process the video. Please try again.")
            else:
                st.warning("Please enter a YouTube URL.")
        
        # Save transcription button
        if 'transcribed_data' in st.session_state and 'video_id' in st.session_state:
            if st.button("Save Transcription"):
                filename = save_transcription(st.session_state.transcribed_data, st.session_state.video_id)
                st.success(f"Transcription saved as {filename}")

    # Main chat interface
    st.title("Chat with YouTube Video")

    # Initialize chat history
    if 'chat_history' not in st.session_state:
        st.session_state.chat_history = []

    # Display chat history
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    # Chat input
    if 'transcribed_data' in st.session_state:
        user_query = st.chat_input("Ask a question about the video:")
        if user_query:
            # Add user message to chat history
            st.session_state.chat_history.append({"role": "user", "content": user_query})
            with st.chat_message("user"):
                st.write(user_query)

            # Generate and display AI response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    answer = chat_with_groq(st.session_state.transcribed_data, user_query)
                    st.write(answer)
                    st.session_state.chat_history.append({"role": "assistant", "content": answer})
    else:
        st.info("Please process a YouTube video using the sidebar before starting the chat.")

if __name__ == "__main__":
    main()