from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from . import database, models, auth, management, routing

app = FastAPI(title="Re-CallRoute API")

app.include_router(auth.router)
app.include_router(management.router)
app.include_router(routing.router)

# Initialize database on startup
@app.on_event("startup")
def startup_event():
    database.init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to Re-CallRoute API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
