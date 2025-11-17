import os
from datetime import datetime
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import Appointment, Message, Project

app = FastAPI(title="MyCode API", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class IdResponse(BaseModel):
    id: str


@app.get("/")
def root():
    return {"name": "MyCode API", "status": "ok"}


@app.get("/test")
def test_database():
    from os import getenv
    try:
        connected = db is not None and db.list_collection_names() is not None
        return {
            "backend": "✅ Running",
            "database": "✅ Connected" if connected else "❌ Not Connected",
            "database_url": "✅ Set" if getenv("DATABASE_URL") else "❌ Not Set",
            "database_name": "✅ Set" if getenv("DATABASE_NAME") else "❌ Not Set",
            "collections": db.list_collection_names()[:10] if connected else []
        }
    except Exception as e:
        return {"backend": "✅ Running", "database": f"⚠️ Error: {str(e)[:120]}"}


# Portfolio projects
@app.post("/api/projects", response_model=IdResponse)
async def create_project(project: Project):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    new_id = create_document("project", project)
    return {"id": new_id}


@app.get("/api/projects", response_model=List[Project])
async def list_projects(type: Optional[str] = None, limit: int = 50):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    filt = {"type": type} if type else {}
    docs = get_documents("project", filt, limit)
    # Remove Mongo _id
    for d in docs:
        d.pop("_id", None)
    return docs


# Appointment booking
@app.post("/api/appointments", response_model=IdResponse)
async def book_appointment(appt: Appointment):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    new_id = create_document("appointment", appt)
    return {"id": new_id}


@app.get("/api/appointments")
async def list_appointments(limit: int = 50):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    docs = get_documents("appointment", {}, limit)
    for d in docs:
        d["id"] = str(d.pop("_id", ""))
    return docs


# Contact messages
@app.post("/api/contact", response_model=IdResponse)
async def send_message(msg: Message):
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    new_id = create_document("message", msg)
    return {"id": new_id}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
