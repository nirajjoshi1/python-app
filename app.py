from flask import Flask, render_template, request, jsonify
import yt_dlp

app = Flask(__name__)

# Route for the homepage
@app.route('/')
def home():
    return render_template('index.html')

# API for downloading videos
@app.route('/downloads', methods=['POST'])
def download_video():
    data = request.json
    url = data.get("url")
    resolution = data.get("resolution", "bestvideo[height<=720]+bestaudio")
    output_format = data.get("format", "mkv")

    try:
        ydl_opts = {
            "format": resolution,
            "outtmpl": "downloads/%(title)s.%(ext)s",
            "merge_output_format": output_format,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            result = ydl.extract_info(url, download=True)
            return jsonify({"message": "Download successful", "title": result["title"]})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
