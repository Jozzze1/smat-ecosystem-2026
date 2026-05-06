from pydantic import BaseModel
from typing import List, Optional

# Esquema para crear estaciones
class EstacionCreate(BaseModel):
    id: int
    nombre: str
    ubicacion: str

# Esquema para crear lecturas
class LecturaCreate(BaseModel):
    estacion_id: int
    valor: float

# Esquema para el Dashboard de Auditoría
class StatsResumen(BaseModel):
    total_estaciones: int
    total_lecturas: int
    estacion_critica_id: Optional[int]
    valor_maximo: float