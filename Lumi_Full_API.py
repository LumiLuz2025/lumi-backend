from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
import sqlite3

app = FastAPI(title="Lumi - Asistente Terapéutico y Profesional",
              description="API de Lumi para asistencia terapéutica, atención al cliente y gestión emocional.",
              version="1.0.0")

# -------------------- BASE DE DATOS --------------------
conn = sqlite3.connect("lumi.db", check_same_thread=False)
cursor = conn.cursor()

cursor.execute("""CREATE TABLE IF NOT EXISTS usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nombre TEXT,
    apodo TEXT,
    preferencias TEXT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS registros_terapeuticos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    tipo TEXT,
    contenido TEXT,
    fecha TEXT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS respuestas_cliente (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    canal TEXT,
    tipoCaso TEXT,
    mensajeCliente TEXT,
    tono TEXT,
    respuestaGenerada TEXT,
    fecha TEXT
)""")

cursor.execute("""CREATE TABLE IF NOT EXISTS contextos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    usuario_id INTEGER,
    casoActual TEXT,
    palabrasClave TEXT,
    tonoRecomendado TEXT,
    puntosClaves TEXT,
    fecha TEXT
)""")

conn.commit()

# -------------------- MODELOS --------------------
class ClienteMensaje(BaseModel):
    canal: str
    tipoCaso: str
    mensajeCliente: str
    tono: str
    incluirDatosCuenta: Optional[bool] = False

class RespuestaCliente(BaseModel):
    respuesta: str

class RegistroTerapia(BaseModel):
    usuario_id: int
    tipo: str
    contenido: str

# -------------------- ENDPOINTS --------------------
@app.get("/")
def home():
    return {"message": "Lumi API está funcionando correctamente."}

@app.post("/asistencia-clientes/respuesta", response_model=RespuestaCliente)
def generar_respuesta_cliente(data: ClienteMensaje):
    respuestas = {
        "techSupport": "Hola, entiendo que estás teniendo problemas técnicos. Vamos a solucionarlo juntos. ¿Podrías darme más detalles sobre el error?",
        "retention": "Lamentamos que estés considerando cancelar el servicio. ¿Hay algo en lo que podamos mejorar para que tu experiencia sea más satisfactoria?",
        "sales": "Gracias por tu interés en nuestros productos. ¿En qué puedo ayudarte para encontrar la mejor opción para ti?"
    }
    respuesta = respuestas.get(data.tipoCaso, "Gracias por tu mensaje. Vamos a atender tu solicitud.")
    cursor.execute("""INSERT INTO respuestas_cliente (canal, tipoCaso, mensajeCliente, tono, respuestaGenerada, fecha)
                      VALUES (?, ?, ?, ?, ?, datetime('now'))""",
                   (data.canal, data.tipoCaso, data.mensajeCliente, data.tono, respuesta))
    conn.commit()
    return {"respuesta": respuesta}

@app.post("/terapia/registrar")
def guardar_registro_terapeutico(data: RegistroTerapia):
    cursor.execute("""INSERT INTO registros_terapeuticos (usuario_id, tipo, contenido, fecha)
                      VALUES (?, ?, ?, datetime('now'))""",
                   (data.usuario_id, data.tipo, data.contenido))
    conn.commit()
    return {"mensaje": "Registro terapéutico guardado con éxito."}
