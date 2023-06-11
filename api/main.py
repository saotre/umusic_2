from os.path import exists

import uvicorn
from fastapi import FastAPI, UploadFile, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from db import DbManager
from users import create_user, create_mp3, get_mp3
from convert import wav_to_mp3



app = FastAPI(title="UMusic")


class InputData(BaseModel):
    name: str = Field(title='Name of user')


@app.get("/record")
def download_file(id: str, user: str) -> FileResponse:
    path_to_mp3 = get_mp3(id, user)
    if path_to_mp3:
        return FileResponse(path=path_to_mp3, filename=f"{id}.mp3", media_type='multipart/form-data')
    else:
        raise HTTPException(status_code=404, detail="File audio is not found")


@app.post("/user")
async def post_user(item: InputData):
    data_user = create_user(item.name)
    return data_user


@app.post("/audio")
async def post_audio(file: UploadFile, user_id: str, token: str):
    path_to_mp3 = f"mp3/{user_id}.mp3"
    wav_to_mp3(file.file.read(), path_to_mp3)
    if exists(path_to_mp3):
        with open(path_to_mp3, "rb") as f:
            data_file = f.read()
        url = create_mp3(data_file, user_id, token)
        if url:
            return url
        else:
            raise HTTPException(status_code=404, detail="Doesn't exist such user + token")

    else:
        return {"error": True, "error_text": "failed to create file mp3"}


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host='0.0.0.0',
        port=8000,
    )
