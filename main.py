import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import date

from database import db, create_document, get_documents
from schemas import Horoscope, Paidreading, Readingsession

app = FastAPI(title="Tarot Blog API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Tarot Blog API is running"}

# Health and DB test
@app.get("/test")
def test_database():
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": None,
        "database_name": None,
        "connection_status": "Not Connected",
        "collections": []
    }

    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Configured"
            response["database_name"] = db.name if hasattr(db, 'name') else "✅ Connected"
            response["connection_status"] = "Connected"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️  Connected but Error: {str(e)[:50]}"
        else:
            response["database"] = "⚠️  Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:50]}"

    response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
    response["database_name"] = "✅ Set" if os.getenv("DATABASE_NAME") else "❌ Not Set"
    return response

# Horoscopes: create and list
@app.post("/api/horoscopes", response_model=dict)
def create_horoscope(h: Horoscope):
    try:
        inserted_id = create_document("horoscope", h)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/horoscopes", response_model=List[dict])
def list_horoscopes(sign: Optional[str] = None, period: Optional[str] = None, limit: int = 30):
    try:
        filt = {}
        if sign:
            filt["sign"] = sign.lower()
        if period:
            filt["period"] = period
        docs = get_documents("horoscope", filt, limit)
        # Convert ObjectId to string where needed
        for d in docs:
            if "_id" in d:
                d["id"] = str(d.pop("_id"))
        return docs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Pick-a-card sessions
@app.post("/api/pick", response_model=dict)
def create_pick_session(s: Readingsession):
    try:
        inserted_id = create_document("readingsession", s)
        return {"id": inserted_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Paid readings submissions
@app.post("/api/paid-readings", response_model=dict)
def create_paid_reading(req: Paidreading):
    try:
        inserted_id = create_document("paidreading", req)
        return {"id": inserted_id, "status": req.status}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
