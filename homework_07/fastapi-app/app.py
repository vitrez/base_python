from fastapi import FastAPI

from views import users_router, posts_router


app = FastAPI()
app.include_router(posts_router)
app.include_router(users_router)


# root
@app.get("/")
def hello_root():
    return {"message": "Hello World!"}
