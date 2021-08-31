from os import path

from youtube_dl import YoutubeDL

from config import DURATION_LIMIT
from helpers.errors import DurationLimitError

ydl_opts = {
    "format": "bestaudio[ext=m4a]",
    "format": "bestaudio/best",
    "geo-bypass": True,
    "nocheckcertificate": True,
    "outtmpl": "downloads/%(id)s.%(ext)s",
}
ydl = YoutubeDL(ydl_opts)
def download(url: str) -> str:
    info = ydl.extract_info(url, False)
    duration = round(info["duration"] / 120)
    if duration > DURATION_LIMIT:
        raise DurationLimitError(
            f"🛑 No se permiten videos de más de {DURATION_LIMIT} minuto (s), el video proporcionado es {duration} minuto(s)"
        )
    try:
        ydl.download([url])
    except:
        raise DurationLimitError(
            f"🛑 No se permiten videos de más de {DURATION_LIMIT} minuto (s), el video proporcionado es {duration} minuto(s)"
        )
    return path.join("downloads", f"{info['id']}.{info['ext']}")
