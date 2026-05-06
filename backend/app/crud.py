from . import models
from sqlalchemy.orm import Session
from app import schemas

# Crear Estación
def crear_estacion(db: Session, estacion: schemas.EstacionCreate):
    db_estacion = models.EstacionDB(**estacion.dict())
    db.add(db_estacion)
    db.commit()
    db.refresh(db_estacion)
    return db_estacion

# Crear Lectura
def crear_lectura(db: Session, lectura: schemas.LecturaCreate):
    db_lectura = models.LecturaDB(**lectura.dict())
    db.add(db_lectura)
    db.commit()
    db.refresh(db_lectura)
    return db_lectura

# SOLUCIÓN RETO LAB 4.3: Dashboard de Auditoría
def obtener_estadisticas_globales(db: Session):
    total_est = db.query(models.EstacionDB).count()
    total_lec = db.query(models.LecturaDB).count()
    
    # Buscamos la lectura con el valor más alto
    lectura_max = db.query(models.LecturaDB).order_by(models.LecturaDB.valor.desc()).first()
    
    return {
        "total_estaciones": total_est,
        "total_lecturas": total_lec,
        "estacion_critica_id": lectura_max.estacion_id if lectura_max else None,
        "valor_maximo": lectura_max.valor if lectura_max else 0.0
    }