from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.exc import SQLAlchemyError

from app.database import check_database_connection


app = FastAPI(
    title="InkluMap API",
    description=(
        "API untuk sistem pemetaan kebutuhan akomodasi "
        "pembelajaran sekolah inklusif."
    ),
    version="0.2.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {
        "application": "InkluMap",
        "message": "InkluMap API berhasil dijalankan.",
        "version": "0.2.0",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "service": "InkluMap API",
    }


@app.get("/health/database")
def database_health_check():
    try:
        database_information = check_database_connection()

        return {
            "status": "healthy",
            "service": "PostgreSQL",
            **database_information,
        }

    except SQLAlchemyError as error:
        raise HTTPException(
            status_code=503,
            detail="Koneksi ke database PostgreSQL gagal.",
        ) from error