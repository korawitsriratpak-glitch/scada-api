from fastapi import FastAPI
from typing import Dict

app = FastAPI()

db: Dict[str, dict] = {}

@app.get("/")
def home():
    return {"status": "SCADA API Running"}

@app.post("/update")
def update(data: dict):
    machine = data["machine"]
    db[machine] = data
    return {"status": "ok"}

@app.get("/data")
def get_data():
    return db
