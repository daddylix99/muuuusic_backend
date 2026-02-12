from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
import re

app = Flask(__name__)
CORS(app)

@app.route('/api/search')
def search():
    query = request.args.get('q', '')
    if not query:
        return jsonify({'tracks': []})
    
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info(f"ytsearch10:{query}", download=False)
            
            tracks = []
            for entry in results.get('entries', []):
                tracks.append({
                    'id': entry['id'],
                    'title': entry['title'],
                    'artist': entry['uploader'],
                    'thumbnail': entry.get('thumbnail', ''),
                    'duration': entry.get('duration', 0)
                })
            
            return jsonify({'tracks': tracks})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/popular')
def popular():
    try:
        ydl_opts = {
            'quiet': True,
            'no_warnings': True,
            'extract_flat': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            results = ydl.extract_info("ytsearch20:top hits 2026", download=False)
            
            tracks = []
            for entry in results.get('entries', []):
                tracks.append({
                    'id': entry['id'],
                    'title': entry['title'],
                    'artist': entry['uploader'],
                    'thumbnail': entry.get('thumbnail', ''),
                    'duration': entry.get('duration', 0)
                })
            
            return jsonify({'tracks': tracks})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/stream/<video_id>')
def stream(video_id):
    try:
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(f"https://youtube.com/watch?v={video_id}", download=False)
            audio_url = info['url']
            
            return jsonify({'url': audio_url})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
