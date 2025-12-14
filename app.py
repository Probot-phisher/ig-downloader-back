from flask import Flask, request, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)
DOWNLOADS = "downloads"
os.makedirs(DOWNLOADS, exist_ok=True)

@app.route("/")
def home():
    return "Instagram Downloader Backend is running"

@app.route("/download")
def download():
    url = request.args.get("url")
    if not url:
        return {"error": "No URL provided"}

    filename = str(uuid.uuid4())
    ydl_opts = {
        "outtmpl": f"{DOWNLOADS}/{filename}.%(ext)s",
        "format": "best",
        "quiet": True
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=True)
        ext = info.get("ext", "mp4")

    filepath = f"{DOWNLOADS}/{filename}.{ext}"
    return send_file(filepath, as_attachment=True)

if __name__ == "__main__":
    app.run()
