#to run PYTHONPATH=./src uvicorn src.main:app --reload

from fastapi import FastAPI
from src.api.router import router

app = FastAPI(title="Battery Peak Shaving Simulator API")

app.include_router(router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
