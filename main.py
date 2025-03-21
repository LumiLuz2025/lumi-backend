
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from datetime import date
import uuid

app = FastAPI()

class Reflexion(BaseModel):
    usuario: str
    tipo: str
    contenido: str
    fecha: date

# Memoria temporal en lugar de una base de datos real
registro_reflexiones = []

@app.post("/terapia/registrar")
async def registrar_reflexion(data: Reflexion):
    reflexion_id = str(uuid.uuid4())
    registro_reflexiones.append({
        "id": reflexion_id,
        "usuario": data.usuario,
        "tipo": data.tipo,
        "contenido": data.contenido,
        "fecha": data.fecha.isoformat()
    })
    return {"mensaje": "Reflexión registrada con éxito", "id": reflexion_id}
