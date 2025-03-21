from pydantic import BaseModel
from ytmusicapi import YTMusic
import yt_dlp
from fastapi import FastAPI

app = FastAPI()

class Song(BaseModel):
    video_id: str
    title: str
    artist: str
    artwork: str

class Details(BaseModel):
    url: str
    artwork: str

@app.get("/search/{name}")
def search(name: str):
    results = []
    with YTMusic() as ytm:
        for item in ytm.search(name):
            if item.get("category") == "Songs":
                results.append(Song(
                    video_id=item["videoId"],
                    title=item["title"],
                    artist=item["artists"][0]["name"],
                    artwork=item["thumbnails"][-1]["url"]
                ))
    return results

class SongDetails:
    def __init__(self, video_id: str):
        self.ytm = YTMusic()
        self.video_id = video_id
        self.video_url = f"https://youtu.be/{video_id}"
        self.song_data = self._fetch_song_data()

    def _fetch_song_data(self):
        try:
            return self.ytm.get_watch_playlist(self.video_id, limit=0)
        except Exception:
            return {}

    def get_lyrics(self):
        lyrics_id = self.song_data.get("lyrics")
        if not lyrics_id:
            return "No lyrics found"
        try:
            lyrics = self.ytm.get_lyrics(browseId=lyrics_id, timestamps=False)
            return lyrics.get("lyrics", "No lyrics found")
        except Exception:
            return "No lyrics found"

    def get_song_url(self):
        options = {'format': 'bestaudio[ext=webm]/bestaudio', 'noplaylist': True, 'quiet': True}
        try:
            with yt_dlp.YoutubeDL(options) as ydl:
                info = ydl.extract_info(self.video_url, download=False)
                return info.get("url", "Audio URL not found"), info.get("thumbnail", "Thumbnail not found")
        except Exception:
            return "Audio URL not found", "Thumbnail not found"

    def get_song_json(self):
        url, thumbnail = self.get_song_url()
        return Details(url=url, artwork=thumbnail)

@app.get("/get-audio/{video_id}")
def get_audio(video_id: str):
    try:
        return SongDetails(video_id).get_song_json()
    except Exception as e:
        return {"error": str(e)}