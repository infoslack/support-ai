from fastapi import FastAPI
from routers import support

app = FastAPI(title="Marketplace Support Agent")

app.include_router(support.router)


@app.get("/")
def root():
    return {"status": "online"}
