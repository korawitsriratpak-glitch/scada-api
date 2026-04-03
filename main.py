from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from influxdb_client import InfluxDBClient

app = FastAPI():
url = "https://us-east-1-1.aws.cloud2.influxdata.com"
token = "XMGZj4P_yBnZ_9uOeHJj2tTvLGckFsIIaBPR_E_2V3d6yZZ8pqnREiQL9iBnHL2OxxrEmuFjZo4LbgpGyCyRJQ=="
org = "Dev"
bucket = "plc_cloud"

client = InfluxDBClient(url=url, token=token, org=org)
query_api = client.query_api()

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
    
@app.get("/history")
def get_history(machine: str = "Piller1"):

    query = f"""
    from(bucket: "{bucket}")
      |> range(start: -12h)
      |> filter(fn: (r) => r._measurement == "scada_test")
      |> filter(fn: (r) => r._field == "pressure")
      |> filter(fn: (r) => r.machine == "{machine}")
      |> sort(columns: ["_time"])
    """

    result = query_api.query(query)

    data = []
    for table in result:
        for record in table.records:
            data.append({
                "time": record.get_time().isoformat(),
                "value": record.get_value()
            })

    return data
