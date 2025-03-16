__all__ = ("app",)

import uvicorn
import asyncio

from app import app
from crud import filling_db


if __name__ == "__main__":
    asyncio.run(filling_db())
    uvicorn.run("main:app", port=8000, reload=True, log_level="debug")
