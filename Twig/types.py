
from enum import Enum


class ContentType:
    json = b"Content-Type: application/json\n"
    plain = b"Content-Type: text/plain\n"
    txt = b"Content-Type: text/plain\n"
    html = b"Content-Type: text/html\n"
    css = b"Content-Type: text/css\n"
    wasm = b"Content-Type: application/wasm\n"
    jpeg = b"image/jpeg"
    jpg = b"image/jpeg"
    ico = b"image/vnd.microsoft.icon"
    gif = b"image/gif"
    js = b"text/javascript"
    csv = b"text/csv"
    mp3 = b"audio/mpeg"
    mp4 = b"video/mp4"
    png = b"image/png"
    wav = b"audio/wav"
    xml = b"application/xml"
    zip = b"application/zip"
    

def ext_content_type(extension:str) -> bytes:
    return ContentType.__dict__[extension]