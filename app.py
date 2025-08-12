# main api router
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware
from main.modules import api_router
import uvicorn
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"Hello": "World"}

app.include_router(
    router=api_router,
    prefix="/api"
)

port = int(os.getenv('PORT', 5050))
if __name__ == '__main__':
    uvicorn.run(app, port=port, host='0.0.0.0')
