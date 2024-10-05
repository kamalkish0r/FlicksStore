from fastapi import FastAPI
from contextlib import asynccontextmanager
from controllers.movie_controller import router as movie_router 

from database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting up...")
    init_db() 
    yield
    print("Shutting down...")

app = FastAPI(lifespan=lifespan)
app.include_router(movie_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)