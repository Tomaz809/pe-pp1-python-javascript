from fastapi import FastAPI 
from fastapi.middleware.cors import CORSMiddleware

from routers.articulos import articulos_routers 

app = FastAPI(
title="API de Farmacia",
)

app.include_router(articulos_routers, prefix="/articulos", tags=["Articulos"])

app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
)
