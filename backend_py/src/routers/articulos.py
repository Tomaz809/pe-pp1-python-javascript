from typing import Annotated
from fastapi import APIRouter, HTTPException, Path, Query
from schemas.articulos import ArticuloFarmaciaSchema, ArticuloFarmaciaUpdateSchema

articulos_routers = APIRouter()
NOT_FOUND_RESPONSE = {
    404: {
        "description": "Response not found si no se encuentra el id",
        "content": {
            "application/json": {
                "example": {
                    "detail": "Articulo no encontrado",
                }
            }
        },
    }
}

articulos_farmacia = [
    {"id": 1, "nombre": "Actron 600", "precio": 10200, "receta": False, "activo": True},
    {"id": 2, "nombre": "Actron 400", "precio": 7000, "receta": False, "activo": True},
    {"id": 3, "nombre": "Amoxicilina 500 mg", "precio": 10500, "receta": True, "activo": True},
]


@articulos_routers.get("/", response_model=list[ArticuloFarmaciaSchema])
async def get_ArticulosFarmacia(
    receta: Annotated[bool | None, Query(description="Filtrar por si se necesita receta")] = None
):
    if receta is None:
        return articulos_farmacia
    return [a for a in articulos_farmacia if a["receta"] == receta]


@articulos_routers.get(
    "/{id}",
    responses=NOT_FOUND_RESPONSE,
    response_model=ArticuloFarmaciaSchema,
)
async def get_articulos_farmacia_by_id(id: Annotated[int, Path(gt=0)]):
    for articulo in articulos_farmacia:
        if articulo["id"] == id:
            return articulo
    raise HTTPException(status_code=404, detail="Articulo no encontrado")


@articulos_routers.post("/", response_model=list[ArticuloFarmaciaSchema])
async def crear_articulo(articulo_nuevo: ArticuloFarmaciaSchema):
    articulos_farmacia.append(articulo_nuevo.model_dump())
    return articulos_farmacia


@articulos_routers.delete(
    "/{id}",
    responses=NOT_FOUND_RESPONSE,
    response_model=ArticuloFarmaciaSchema,
)
async def borrar_articulo(
    id: Annotated[int, Path(gt=0)],
    logico: Annotated[bool, Query(description="Mantener registro?")] = False,
) -> ArticuloFarmaciaSchema:
    for articulo in articulos_farmacia:
        if articulo["id"] == id:
            if logico:
                articulo["activo"] = False  
            else:
                articulos_farmacia.remove(articulo)
            return articulo
    raise HTTPException(status_code=404, detail="Articulo no encontrado")


@articulos_routers.put(
    "/{id}",
    responses=NOT_FOUND_RESPONSE,
    response_model=ArticuloFarmaciaSchema,
)
async def editar_articulo(
    id: Annotated[int, Path(gt=0, description="Id del producto, >0")],
    articulo_editar: ArticuloFarmaciaUpdateSchema,
):
    for articulo in articulos_farmacia:
        if articulo["id"] == id:
            articulo["nombre"] = articulo_editar.nombre
            articulo["precio"] = articulo_editar.precio
            articulo["activo"] = articulo_editar.activo
            articulo["receta"] = articulo_editar.receta
            return articulo
    raise HTTPException(status_code=404, detail="Articulo no encontrado")