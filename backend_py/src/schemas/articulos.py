from typing import Annotated
from pydantic import BaseModel, Field

IntPositivo = Annotated[int, Field(gt=0, description="debe ser mayor que 0")]
StrCorto = Annotated[str, Field(min_length=1, max_length=50, description="Nombre del articulo")]
FloatPrecioVenta = Annotated[float, Field(gt=500, lt=9999999, description="Precio en pesos ARG")]
BoolDisponibilidad = Annotated[bool, Field(description="Sigue disponible?")]
BoolReceta = Annotated[bool, Field(description="Se requiere receta medica")]

class ArticuloFarmaciaSchema(BaseModel):
    id: IntPositivo
    nombre: StrCorto
    precio: FloatPrecioVenta
    activo: BoolDisponibilidad = True
    requiere_receta: BoolReceta 

class ArticuloFarmaciaUpdateSchema(BaseModel):
    nombre: StrCorto
    precio: FloatPrecioVenta
    activo: BoolDisponibilidad = True
    requiere_receta: BoolReceta
