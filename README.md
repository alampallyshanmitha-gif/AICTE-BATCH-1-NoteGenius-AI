NoteGenius AI – Smart Speech-to-Notes and Study Generator

Overview

NoteGenius AI is an AI-powered educational platform that helps students convert lecture recordings into structured study materials. The system uses Whisper Speech-to-Text technology to transcribe lecture audio and Generative AI to generate summaries, keywords, quizzes, and flashcards. It also provides translation support, an AI chatbot, analytics, saved notes, and PDF export functionality to enhance learning and revision.

---

Features

- User Registration (Signup)
- User Authentication (Login)
- Lecture Audio Upload
- Speech-to-Text Transcription
- AI-Generated Summaries
- Keyword Extraction
- Quiz Generation
- Flashcard Generation
- Translation Support
- AI Chatbot Assistance
- Analytics Dashboard
- Saved Notes Management
- PDF Export of Generated Content

---

Project Workflow

1. User Registration and Login

New users can create an account through the signup page, while existing users can log in securely to access the platform.

2. Audio Upload

Users upload lecture recordings through the dashboard.

3. Speech-to-Text Conversion

Whisper converts the uploaded audio into an accurate text transcript.

4. AI Content Generation

Generative AI analyzes the transcript and generates:

- Summaries
- Keywords
- Quizzes
- Flashcards

5. Translation Support

Users can translate generated content into different languages.

6. AI Chatbot

Students can ask questions related to lecture content and receive AI-generated explanations.

7. Saved Notes

Generated transcripts and study materials are stored for future access and revision.

8. PDF Export

Users can export generated notes, summaries, quizzes, and flashcards as PDF documents.

9. Analytics Dashboard

The dashboard provides insights into learning activities and content usage.

---

Technology Stack

Frontend

- Streamlit

Backend

- Python

Database

- SQLite

AI Technologies

- OpenAI Whisper
- Google Gemini API

---

Libraries Used

streamlit==1.36.0
openai-whisper
torch
torchaudio
torchvision
python-dotenv
fpdf
deep-translator
ffmpeg-python
yake
numpy
tqdm
regex

---

Installation

Clone the Repository

git clone <repository-url>
cd NoteGenius-AI

Install Dependencies

pip install -r requirements.txt

Configure Environment Variables

Create a ".env" file and add:

GOOGLE_API_KEY=your_api_key_here

Run the Application

streamlit run app.py

---

System Requirements

Hardware Requirements

- Intel Core i3 or higher
- 4 GB RAM minimum
- 10 GB free storage
- Internet connection

Software Requirements

- Python 3.10+
- Streamlit
- FFmpeg

---

Future Scope

- Real-time lecture transcription
- Mobile application support
- Personalized learning recommendations
- Advanced analytics and progress tracking
- Multi-language speech recognition
- Cloud storage integration

---

Conclusion

NoteGenius AI provides an intelligent solution for transforming lecture recordings into organized study materials. By combining Speech-to-Text and Generative AI technologies, the platform improves note-taking, learning, and revision efficiency. Features such as translation, AI chatbot assistance, analytics, saved notes, and PDF export make it a comprehensive learning companion for students.

---

References

1. https://docs.python.org/3/
2. https://docs.streamlit.io/
3. https://github.com/openai/whisper
4. https://pytorch.org/docs/
5. https://ai.google.dev/
6. https://deep-translator.readthedocs.io/
7. https://github.com/LIAAD/yake
8. https://github.com/
 -----------
API Key Configuration

To use NoteGenius AI, users need to provide a valid Google Gemini API key. This allows the application to access Generative AI features such as summaries, keywords, quizzes, flashcards, translations, and chatbot responses.

1. Obtain a Gemini API key from Google AI Studio.
2. Create a ".env" file in the project directory.
3. Add your API key as shown below:

GOOGLE_API_KEY=your_api_key_here

Using your own API key ensures reliable access to AI features and allows the application to function smoothly without requiring additional configuration.
