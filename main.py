from fastapi.responses import FileResponse
from fastapi import FastAPI, HTTPException
import hashlib
import qrcode
import os

app = FastAPI()


def clear_cache(path: str):
    dir = os.listdir(path)
    for item in dir:
        if item.endswith(".jpg"):
            os.remove(os.path.join(path, item))


res = "Welcome to the Fast QR API made by jebediah47, github: https://github.com/jebediah47"


@app.get("/")
def root_response(data=res):
    clear_cache(os.getcwd())
    return data


@app.get("/qr", response_class=FileResponse)
def generate_qr(data: str = "hello"):
    clear_cache(os.getcwd())
    if data == "":
        raise HTTPException(status_code=404, detail="You cannot send an empty query!")
    elif len(data) > 1024:
        raise HTTPException(status_code=403, detail="The query must not be over 1024 characters!")
    else:
        md5 = hashlib.md5(str(data).encode("utf-8"))
        qr = qrcode.make(data)
        name = md5.hexdigest()
        file = f"{name}.jpg"
        qr.save(f"{file}")
        return file
