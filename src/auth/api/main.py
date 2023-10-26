from fastapi import FastAPI
from api.routers import users, auth


app = FastAPI()
app.include_router(users.router, prefix="/users", tags=["users"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app=app,
        port=8000,
        # reload=True,
        # log_level="debug"
        # host='0.0.0.0',
        # log_level='warning'
        # reload_dirs=[os.path.join(os.path.dirname(__file__), 'app')]
    )
