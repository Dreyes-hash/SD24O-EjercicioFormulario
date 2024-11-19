from fastapi import FastAPI, UploadFile, File, Form
from typing import Optional
from pydantic import BaseModel
import shutil
import os
import uuid

# creación del servidor
app = FastAPI()

class UsuarioBase(BaseModel):
    nombre:str
    direccion:str
    foto: str
    vip:bool    

usuarios = [{
    "nombre": "Homero Simpson",
    "direccion": "Av. Simpre Viva",
    "foto": "ruta",
    "vip": "False"
}]

@app.post('/usuarios')
async def nuevaFoto(nombre:str = Form(None), direccion:str = Form(None), foto:UploadFile = File(...), vip:bool = Form(None)):
    vip = str(vip).lower() in ["true", "on", "1"] if vip is not None else False
    home_usuario = os.path.expanduser("~")
    if vip:
        carpetaVIP = "NoVip"

    else: 
        carpetaVIP = "VIP"
    respuesta = (nombre, direccion, vip)
    ruta_directorio = os.path.join(home_usuario, carpetaVIP)
    os.makedirs(ruta_directorio, exist_ok=True)
    ruta = os.path.join(ruta_directorio, f"{uuid.uuid4()}{os.path.splitext(foto.filename)[1]}")
    with open(ruta,"wb") as imagen:
        contenido = await foto.read()
        imagen.write(contenido)
    usuarioNuevo ={
        "nombre": "{nombre}",
        "direccion": "{direccion}",
        "foto": "{ruta}",
        "vip": "{vip}"
    }
    usuarios.append(usuarioNuevo)
    print(ruta)
    print(respuesta)
    return respuesta
