from fastapi import FastAPI, UploadFile, File
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import cv2
import numpy as np


app = FastAPI()
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.get("/favicon.ico")
async def get_favicon():
    return FileResponse("app/static/favicon.ico")

@app.get("/")
async def root():
    return {
        "message": "Bienvenido a la API de Procesamiento de Imágenes",
        "endpoints": {
            "/docs": "Documentación interactiva",
            "/convert-to-gray": "Convierte imágenes a escala de grises (POST)"
        }
    }

@app.post("/convert-to-gray")
async def convert_to_gray(image: UploadFile = File(...)):
    #read image and convert to gray scale
    image_bytes = await image.read()
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #Save result temporary
    cv2.imwrite("output_gray.jpg", gray_img)

    return {"message": "Image converted to gray scale", "filename": "output_gray.jpg"}