from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

data_store = {}

@app.post("/update")
def receive_data(data: dict):
    machine = data["machine"]
    data_store[machine] = data
    return {"status": "ok"}

@app.get("/data")
def get_data():
    return data_store
