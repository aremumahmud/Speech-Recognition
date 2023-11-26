from flask import Flask, request, jsonify
from flask_cors import CORS
import speech_recognition as sr
import requests

app = Flask(__name__)
CORS(app)

@app.route('/transcribe', methods=['POST'])
def transcribe_audio():
    try:
        # Get the audio URL from the request
        audio_url = request.json['audio_url']

        # Fetch the audio file from the remote URL
        audio_response = requests.get(audio_url, stream=True)
        audio_response.raise_for_status()

        # Initialize the SpeechRecognition recognizer
        recognizer = sr.Recognizer()

        # Open the audio stream from the fetched data
        with sr.AudioFile(audio_response.raw) as audio_file:
            audio_data = recognizer.record(audio_file)

        # Perform Speech-to-Text
        transcript = recognizer.recognize_google(audio_data)

        return jsonify({'transcript': transcript})

    except requests.exceptions.RequestException as e:
        return jsonify({'error': f'Request error: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
