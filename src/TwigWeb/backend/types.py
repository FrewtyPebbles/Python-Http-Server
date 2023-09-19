
from enum import Enum


class ContentType:
    json = b"Content-Type: application/json\n"
    plain = b"Content-Type: text/plain\n"
    txt = b"Content-Type: text/plain\n"
    html = b"Content-Type: text/html\n"
    css = b"Content-Type: text/css\n"
    wasm = b"Content-Type: application/wasm\n"
    jpeg = b"Content-Type: image/jpeg\n"
    jpg = b"Content-Type: image/jpeg\n"
    ico = b"Content-Type: image/vnd.microsoft.icon\n"
    gif = b"Content-Type: image/gif\n"
    js = b"Content-Type: text/javascript\n"
    csv = b"Content-Type: text/csv\n"
    mp3 = b"Content-Type: audio/mpeg\n"
    mp4 = b"Content-Type: video/mp4\n"
    png = b"Content-Type: image/png\n"
    wav = b"Content-Type: audio/wav\n"
    xml = b"Content-Type: application/xml\n"
    zip = b"Content-Type: application/zip\n"
    

def ext_content_type(extension:str) -> bytes:
    return ContentType.__dict__[extension]