from fastapi import FastAPI
import uvicorn

app = FastAPI()

@app.get("/ping/")
async def ping_pong():
    return {"message": "pong"}

if __name__ == '__main__':
    uvicorn.run("app:app", host='0.0.0.0', port=8000, reload=True, log_level="debug")