# Chat with Youtube

This Streamlit application allows you to transcribe audio from a YouTube video and chat with an AI about the content of the video.

## Features

- **YouTube Video Transcription:** Extract audio from a YouTube video and transcribe it.
- **Interactive Chat:** Engage in a chat based on the transcribed video content.
- **Save Transcription:** Save the transcribed text to a file.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/Aboodseada1/Chat-with-Youtube
   cd Chat-with-Youtube
   ```
2. **Install dependencies:**

Use the following command to install the required Python packages:

```bash
pip install -r requirements.txt
```

3. **Set your Groq API key in 'app.py':**

   In the `app.py` file, replace `"API_KEY_HERE"` with your Groq API key:

   ```python
   os.environ["GROQ_API_KEY"] = "your-api-key"
   ```
4. **Set your Groq API key in 'Modules/transcriber.py':**

   In the `transcriber.py` file, replace `"API_KEY_HERE"` with your Groq API key:

```python
   os.environ["GROQ_API_KEY"] = "your-api-key"
```

## Usage

1. **Run the Streamlit app:**

   Start the application by running:

   ```bash
   streamlit run app.py
   ```
2. **Process a YouTube video:**

   - Enter the YouTube video URL in the sidebar.
   - Click "Process Video" to download and transcribe the audio.
3. **Interact with the transcribed content:**

   - Use the chat interface to ask questions about the video.
   - Save the transcription by clicking "Save Transcription."

## Project Structure

- **`app.py`:** The main application file that handles the user interface and video processing.
- **`Modules/`:** Contains additional modules like the transcriber and downloader scripts.

## License

This project is licensed under the MIT License.
