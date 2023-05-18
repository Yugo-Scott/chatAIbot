from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import StreamingResponse
# from fastapi.responses import FileResponse
from decouple import config
import openai
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
openai.api_key = config("OPEN_AI_KEY")
from starlette.staticfiles import StaticFiles

templates = Jinja2Templates(directory="templates")

# Custom Function Imports
from functions.openai_requests import convert_audio_to_text, get_chat_response
from functions.database import store_messages, reset_messages
from functions.text_to_speech import convert_text_to_speech

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
# app.mount("/audio", StaticFiles(directory="audio"), name="audio") 

@app.get("/test")
async def test(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/reset")
async def reset_conversation():
    reset_messages()
    return {"message": "Reset Conversation"}

@app.get("/post-audio-get/")
async def get_audio01():
    return {"message": "Hello World"}

@app.post("/post-audio-get/")
async def get_audio(file: UploadFile = File(...)):
    with open(f"{file.filename}", "wb") as buffer:
        buffer.write(await file.read())
    
    # get saved audio
    audio_input = open(file.filename, "rb")
    # decode audio
    message_decoded=convert_audio_to_text(audio_input)
    print(message_decoded)
    if not message_decoded:
        raise HTTPException(status_code=400, detail="Failed to decode audio")
    
    chat_response = get_chat_response(message_decoded)
    print(chat_response)

    # Guard: Ensure output
    if not chat_response:
        raise HTTPException(status_code=400, detail="Failed chat response")

    # Store messages
    store_messages(message_decoded, chat_response)
    # Convert chat response to audio
    audio_output = convert_text_to_speech(chat_response)
    print(type(audio_output))
    # # print(audio_output)
    # if not audio_output:
    #     raise HTTPException(status_code=400, detail="Failed audio output")
    # # Create a generator that yields chunks of data
    def iterfile():
        yield audio_output

    if audio_output is not None:
        with open("output.mp3", "wb") as f:
            f.write(audio_output)
    # # Use for Post: Return output audio
    return StreamingResponse(iterfile(), media_type="audio/mpeg")
    # # return FileResponse(audio_output, media_type="audio/mpeg")