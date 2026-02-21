from fastapi import FastAPI, UploadFile, File
from fastapi.responses import StreamingResponse
from protect import protect_image
from io import BytesIO

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Cloak backend running"}

@app.post("/protect")
async def protect(file: UploadFile = File(...)):
    image_bytes = await file.read()
    protected_image = protect_image(image_bytes)

    return StreamingResponse(
        BytesIO(protected_image),
        media_type="image/png"
    )