from typing import Annotated
from pydantic import BaseModel, Field

IntPositivo = Annotated[int, Field(gt=0)]
StrProducto = Annotated[str, Field(max_length=30)]
FloatPrecioVenta = Annotated[float, Field(gt=1000, lt=9999999)]
BoolActivo = Annotated[bool, Field(description="Sigue disponible?")]

