from . import crud, models
from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from . import schemas
from .database import engine, get_db
from .auth import crear_token_acceso, obtener_identidad_actual

# Crear tablas
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="SMAT - Sistema de Monitoreo de Alerta Temprana",
    version="1.0.0"
)

# ✅ DATOS INICIALES (solo si la BD está vacía)
@app.on_event("startup")
def startup_event():
    db: Session = next(get_db())

    existe = db.query(models.EstacionDB).first()
    if existe:
        print("⚠️ Ya hay datos")
        return

    estaciones = [
        models.EstacionDB(id=1, nombre="Río Rímac", ubicacion="Lima"),
        models.EstacionDB(id=2, nombre="Estación Norte", ubicacion="Comas"),
        models.EstacionDB(id=3, nombre="Estación Sur", ubicacion="VES"),
    ]

    db.add_all(estaciones)
    db.commit()

    print("✅ Datos iniciales insertados")


# ✅ CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ✅ LOGIN CORRECTO (IMPORTANTE PARA AUTHORIZE 🔓)
@app.post("/token", tags=["Seguridad"])
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    return {
        "access_token": crear_token_acceso({"sub": form_data.username}),
        "token_type": "bearer"
    }

# ✅ GET estaciones (solo UNO, evita duplicados)
@app.get("/estaciones/", tags=["Gestión de Infraestructura"])
def listar_estaciones(db: Session = Depends(get_db)):
    return db.query(models.EstacionDB).all()

# ✅ POST estaciones (PROTEGIDO)
@app.post("/estaciones/", status_code=201, tags=["Gestión de Infraestructura"])
def crear_estacion(
    estacion: schemas.EstacionCreate,
    db: Session = Depends(get_db),
    token: str = Depends(obtener_identidad_actual)
):
    return crud.crear_estacion(db=db, estacion=estacion)

# ✅ POST lecturas
@app.post("/lecturas/", status_code=201, tags=["Telemetría de Sensores"])
def registrar_lectura(
    lectura: schemas.LecturaCreate,
    db: Session = Depends(get_db),
    token: str = Depends(obtener_identidad_actual)
):
    estacion_db = db.query(models.EstacionDB).filter(
        models.EstacionDB.id == lectura.estacion_id
    ).first()

    if not estacion_db:
        raise HTTPException(status_code=404, detail="La estación no existe")

    return crud.crear_lectura(db=db, lectura=lectura)

# ✅ HISTORIAL
@app.get("/estaciones/{id}/historial")
def obtener_historial(id: int, db: Session = Depends(get_db)):
    estacion = db.query(models.EstacionDB).filter(
        models.EstacionDB.id == id
    ).first()

    if not estacion:
        raise HTTPException(status_code=404, detail="Estación no encontrada")

    valores = [l.valor for l in estacion.lecturas]
    conteo = len(valores)
    promedio = sum(valores) / conteo if conteo > 0 else 0.0

    return {
        "estacion_id": id,
        "lecturas": valores,
        "conteo": conteo,
        "promedio": promedio
    }