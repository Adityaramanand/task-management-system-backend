from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import model
from database import engine

from routers import auth, tasks, analytics

model.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(tasks.router)
app.include_router(analytics.router)


@app.get("/")
def root():
    return {"message": "Task API running"}