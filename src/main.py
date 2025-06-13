from fastapi import FastAPI
import uvicorn

from src import router, middlewares


app = FastAPI()
app.include_router(router)
for middleware in middlewares:
    app.add_middleware(middleware)

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8005)