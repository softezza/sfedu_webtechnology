from fastapi import FastAPI, UploadFile, APIRouter, File, UploadFile
from mysql_connector import MySQLConnector
from pydantic import BaseModel
import json
import traceback
import pydub

file_router = APIRouter()


@file_router.post("/convert_file/")
async def convert_file(file: bytes = File(), format: str = "mp3"):
    temp_path = "/srv/cut_temp/file.wav"
    with open(temp_path, "wb") as tempfile:
        tempfile.write(file)
    save_path = "/srv/temp_files/file.mp3"
    pydub.AudioSegment.from_wav(temp_path).export(save_path, format="mp3")
    return {"file_size": len(File("/srv/temp_files/file.mp3"))}


@file_router.post("/change_file")
async def update_audio(file: bytes = File(), params: dict = {}):
    temp_path = "/srv/update_temp/file.wav"
    with open(temp_path, "wb") as tempfile:
        tempfile.write(file)
    save_path = "/srv/temp_files/file.wav"
    # TODO: Change audio pitch, speed, etc...
    return {"WIP": "Sorry, this service is not available"}


@file_router.post("/update_metadata")
async def update_audio_metadata(file: bytes = File(), params: dict = {}):
    temp_path = "/srv/update_temp/file.wav"
    with open(temp_path, "wb") as tempfile:
        tempfile.write(file)
    save_path = "/srv/temp_files/file.wav"
    # TODO: Change audio metadata
    return {"WIP": "Sorry, this service is not available"}


@file_router.post("/cut_file/")
async def cut_audio_file(file: bytes = File(), start: int = 0, finish: int = 0):
    temp_path = "/srv/cut_temp/file.wav"
    with open(temp_path, "wb") as tempfile:
        tempfile.write(file)
    save_path = "/srv/temp_files/file.mp3"
    pydub.AudioSegment.from_wav(temp_path).export(save_path, format="mp3")
    return {"file_size": len(File("/srv/temp_files/file.mp3"))}

