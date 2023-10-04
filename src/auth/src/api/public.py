from fastapi import FastAPI
from routers.public import router as public_router


app = FastAPI()
app.include_router(public_router, prefix="/users")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app=app,
        # reload=True,
        # log_level="debug"
        # host='0.0.0.0',
        # port=8000,
        # log_level='warning'
        # reload_dirs=[os.path.join(os.path.dirname(__file__), 'app')]
    )