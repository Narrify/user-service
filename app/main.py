"""
Main file for the FastAPI application
"""

import uvicorn, logging
from fastapi import FastAPI, status

from app.api.auth import router as auth_router
from app.db.database import Base, engine
from app.router.users_router import router as user_router

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Narrify | User Management API",
    description="User management API for Narrify.",
    version="1.0.0",
)

logger = logging.getLogger(__name__)

logger.info("Probando el sistema de logging")

@app.get("/", status_code=status.HTTP_200_OK)
async def hello_world():
    """
    TODO
    """
    logger.info("Endpoint '/' llamado OOO")

    return "Hello World"


app.include_router(auth_router)
app.include_router(user_router)

if __name__ == "__main__":
    uvicorn.run("app.main:app",host="localhost", port=8000, workers=1,log_config="../log_conf.yaml")
    #asignar la cantidad de workers igual a la cantidad de nucleos del procesador del host