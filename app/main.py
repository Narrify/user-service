"""
Main file for the FastAPI application
"""
import logging
import uvicorn
import os
from fastapi import FastAPI, status

from app.api.auth import router as auth_router
from app.db.database import Base, engine
from app.router.users_router import router as user_router

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
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

# Include routers
app.include_router(auth_router)
app.include_router(user_router)

if __name__ == "__main__":
    # Construct an absolute path for log_conf.yaml
    log_config_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../log_conf.yaml")
    
    uvicorn.run("app.main:app", host="localhost", port=8000, workers=1, log_config=log_config_path)
    # Assign workers equal to the number of processor cores of the host
