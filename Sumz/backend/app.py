import re
from flask import Flask, request, jsonify
from youtube_transcript_api import YouTubeTranscriptApi
from transformers import pipeline
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Load the summarization pipeline
summarizer = pipeline("summarization")

def get_video_id(url):
    """
    Extracts the YouTube video ID from a URL.
    """
    regex = r"(?:https?:\/\/)?(?:www\.)?(?:youtube\.com\/(?:[^\/\n\s]+\/\S+\/|(?:v|e(?:mbed)?)\/|\S*?[?&]v=)|youtu\.be\/)([a-zA-Z0-9_-]{11})"
    match = re.search(regex, url)
    return match.group(1) if match else None

@app.route('/api/summarize', methods=['GET'])
def summarize_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    try:
        video_id = get_video_id(video_url)
        if not video_id:
            return jsonify({"error": "Invalid YouTube URL"}), 400

        transcript = YouTubeTranscriptApi.get_transcript(video_id)

        transcript_text = ""
        for item in transcript:
            transcript_text += item["text"] + " "

        summary = summarizer(transcript_text, max_length=150, min_length=30, do_sample=False)

        return jsonify({"summary": summary[0]['summary_text']})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)
